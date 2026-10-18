"""Resend email on inscricao finalizada + lembrete-pagamento resumo + cleanup (iteration 50)."""
import os
import subprocess
import time
import pytest
import requests

BASE_URL = (os.environ.get("REACT_APP_BACKEND_URL") or "").rstrip("/")
if not BASE_URL:
    for line in open("/app/frontend/.env"):
        if line.startswith("REACT_APP_BACKEND_URL="):
            BASE_URL = line.split("=", 1)[1].strip().rstrip("/")

CPF = "11144477735"
NOME = "TEST_RESEND_CANDIDATO"
EMAIL = "delivered@resend.dev"


@pytest.fixture(scope="module")
def auth():
    r = requests.post(f"{BASE_URL}/api/admin/auth/login",
                      json={"username": "donas", "password": "Seinao10@@"}, timeout=30)
    assert r.status_code == 200, r.text
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {r.json()['token']}"
    return s


@pytest.fixture(scope="module", autouse=True)
def cleanup(auth):
    def _clean():
        r = auth.get(f"{BASE_URL}/api/admin/inscriptions", params={"q": NOME}, timeout=30)
        if r.ok:
            for i in r.json().get("items", []):
                if i.get("cpf") == CPF:
                    auth.delete(f"{BASE_URL}/api/admin/inscriptions/{i['id']}", timeout=15)
        auth.delete(f"{BASE_URL}/api/admin/cadastros/{CPF}", timeout=15)
    _clean()
    yield
    _clean()


def test_lembrete_resumo(auth):
    r = auth.get(f"{BASE_URL}/api/admin/inscricoes/lembrete-pagamento/resumo", timeout=60)
    assert r.status_code == 200, r.text
    d = r.json()
    for k in ("total", "ja_enviados_hoje", "pendentes", "hoje"):
        assert k in d
    assert isinstance(d["total"], int)


def test_lembrete_resumo_requires_auth():
    r = requests.get(f"{BASE_URL}/api/admin/inscricoes/lembrete-pagamento/resumo", timeout=30)
    assert r.status_code in (401, 403)


def test_cadastro_then_finalize_sends_resend_email(auth):
    base = {"nome": NOME, "cpf": "111.444.777-35", "email": EMAIL}
    r = requests.post(f"{BASE_URL}/api/track/registration", json={
        "page": "/inscricao.html", "user_agent": "pytest-resend",
        "extra": {**base, "stage": "cadastro", "form_data": {"NOME": NOME, "EMAIL": EMAIL}}}, timeout=30)
    assert r.status_code == 200 and r.json().get("ok") is True
    r = requests.post(f"{BASE_URL}/api/track/registration", json={
        "page": "/confirmacao.html", "user_agent": "pytest-resend",
        "extra": {**base, "concurso": "PC-AP 2026", "cargo_titulo": "TEST Cargo",
                  "cargo_codigo": "TEST-01", "taxa": "R$ 100,00", "finalized": True,
                  "stage": "inscricao_finalizada"}}, timeout=60)
    assert r.status_code == 200, r.text
    time.sleep(3)
    logs = subprocess.run("tail -n 300 /var/log/supervisor/backend.*.log", shell=True,
                          capture_output=True, text=True).stdout
    assert f"[email] enviado: 'Inscrição realizada com sucesso' -> {EMAIL}" in logs, logs[-3000:]
    r2 = auth.get(f"{BASE_URL}/api/admin/inscriptions", params={"q": NOME}, timeout=30)
    match = [i for i in r2.json()["items"] if i.get("cpf") == CPF]
    assert match and match[0]["finalized"] is True
