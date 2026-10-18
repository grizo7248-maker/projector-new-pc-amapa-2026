"""PC-AP cargo/fee tests: cargo 1 (Delegado)=R$200, cargo 2 (Oficial Investigador)=R$150."""
import os
import time
import uuid
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
CPF1 = '52998224725'
CPF2 = '11144477735'


@pytest.fixture(scope='module')
def H():
    r = requests.post(f'{BASE_URL}/api/admin/auth/login', json={'username': 'donas', 'password': 'Seinao10@@'}, timeout=15)
    assert r.status_code == 200
    h = {'Authorization': f"Bearer {r.json()['token']}"}
    yield h
    for c in (CPF1, CPF2):
        requests.delete(f'{BASE_URL}/api/admin/cadastros/{c}', headers=h, timeout=15)


# Pix generate per cargo (no cpf)
@pytest.mark.parametrize('cod,val', [('1', 200.0), ('2', 150.0), ('01', 200.0)])
def test_pix_generate_by_cargo(cod, val):
    r = requests.post(f'{BASE_URL}/api/pix/generate', json={'cargo_codigo': cod, 'valor': 1, 'txid': 'TESTCARGO'}, timeout=15)
    assert r.status_code == 200, r.text
    d = r.json()
    assert d['valor'] == val
    assert f'54{len(f"{val:.2f}"):02d}{val:.2f}' in d['pix_code']


# Registration + resumo + admin inscriptions + pix with cpf
@pytest.mark.parametrize('cpf,cod,titulo,val,taxa', [
    (CPF1, '1', 'DELEGADO DE POLÍCIA CIVIL', 200.0, 'R$ 200,00'),
    (CPF2, '2', 'OFICIAL INVESTIGADOR DE POLÍCIA CIVIL', 150.0, 'R$ 150,00'),
])
def test_registration_flow(H, cpf, cod, titulo, val, taxa):
    body = {'page': '/inscricao-realizada', 'extra': {
        'nome': 'TEST CARGO', 'cpf': cpf, 'email': 'test@example.com', 'concurso': 'PC-AP',
        'cargo_codigo': cod, 'cargo_titulo': titulo, 'stage': 'inscricao_finalizada', 'finalized': True,
        'valor': 1.0, 'taxa': 'R$ 1,00', 'protocolo': f'TEST-{uuid.uuid4().hex[:8]}'}}
    r = requests.post(f'{BASE_URL}/api/track/registration', json=body, timeout=15)
    assert r.status_code == 200, r.text
    time.sleep(0.5)
    r = requests.get(f'{BASE_URL}/api/inscricao/resumo/{cpf}', timeout=15)
    assert r.status_code == 200
    d = r.json()
    assert d['valor'] == val and d['taxa'] == taxa and d['cargo_codigo'] == cod
    r = requests.get(f'{BASE_URL}/api/admin/inscriptions?q={cpf}', headers=H, timeout=15)
    assert r.status_code == 200
    data = r.json()
    items = data if isinstance(data, list) else (data.get('items') or data.get('inscriptions') or [])
    found = [i for i in items if i.get('cpf') == cpf]
    assert found, data
    assert all(i['valor'] == val for i in found), found
    # pix with cpf only -> uses inscription cargo
    r = requests.post(f'{BASE_URL}/api/pix/generate', json={'cpf': cpf, 'txid': 'TESTCARGO'}, timeout=15)
    assert r.status_code == 200 and r.json()['valor'] == val


def test_pix_tracking_by_cargo(H):
    for ep in ['pix-generated', 'pix-copied']:
        r = requests.post(f'{BASE_URL}/api/track/{ep}', json={'page': '/pagamento-pix', 'extra': {'cpf': CPF1, 'nome': 'TEST CARGO', 'valor': 1, 'cargo_codigo': '1'}}, timeout=15)
        assert r.status_code == 200, r.text


def test_kpis(H):
    r = requests.get(f'{BASE_URL}/api/admin/dashboard/kpis', headers=H, timeout=15)
    assert r.status_code == 200
    print('KPIS', r.json())
