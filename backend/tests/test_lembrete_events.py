# Lembrete de pagamento: feed event + email link origem + email_click tracking
import os, re, sys, time, random
import pytest, requests
from pymongo import MongoClient

sys.path.insert(0, '/app/backend')
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')


def gen_cpf():
    n = [random.randint(0, 9) for _ in range(9)]
    for k in (10, 11):
        s = sum(v * (k - i) for i, v in enumerate(n)) % 11
        n.append(0 if s < 2 else 11 - s)
    return ''.join(map(str, n))


CPF = gen_cpf()
NOME = 'TEST_LEMBRETE CANDIDATO'


@pytest.fixture(scope='module')
def db():
    c = MongoClient(MONGO_URL)
    d = c[DB_NAME]
    # Temporarily un-finalize any non-test registrations so no real emails go out
    others = [x['cpf'] for x in d.inscricoes.find({'finalized': True, 'email': {'$ne': 'delivered@resend.dev'}}, {'cpf': 1})]
    d.inscricoes.update_many({'cpf': {'$in': others}}, {'$set': {'finalized': False}})
    yield d
    d.inscricoes.update_many({'cpf': {'$in': others}}, {'$set': {'finalized': True}})
    d.inscricoes.delete_many({'cpf': CPF}); d.cadastros.delete_many({'cpf': CPF})


@pytest.fixture(scope='module')
def admin():
    s = requests.Session()
    r = s.post(f'{BASE_URL}/api/admin/auth/login', json={'username': 'donas', 'password': 'Seinao10@@'})
    assert r.status_code == 200, r.text
    tok = r.json().get('token') or r.json().get('access_token')
    if tok:
        s.headers['Authorization'] = f'Bearer {tok}'
    return s


def test_email_html_origem():
    from email_service import build_inscricao_email_html
    h1 = build_inscricao_email_html(nome='A', cpf='123.456.789-09', protocolo='P', cargo='C', concurso='', valor=200,
                                    base_url='https://x.com', lembrete_prazo='x')
    assert 'pagamento-pix.html?cpf=12345678909&amp;origem=lembrete' in h1 or 'pagamento-pix.html?cpf=12345678909&origem=lembrete' in h1
    h2 = build_inscricao_email_html(nome='A', cpf='123.456.789-09', protocolo='P', cargo='C', concurso='', valor=200,
                                    base_url='https://x.com')
    assert re.search(r'pagamento-pix\.html\?cpf=12345678909&(amp;)?origem=email', h2)


def test_create_registration(db):
    r = requests.post(f'{BASE_URL}/api/track/registration', json={'page': '/inscricao', 'extra': {
        'nome': NOME, 'cpf': CPF, 'email': 'delivered@resend.dev', 'finalized': True, 'stage': 'inscricao_finalizada',
        'cargo_codigo': '1', 'cargo_titulo': 'TEST Cargo 1', 'protocolo': 'TESTP' + CPF[:5]}})
    assert r.status_code == 200, r.text
    doc = db.inscricoes.find_one({'cpf': CPF})
    assert doc and doc.get('finalized') and doc.get('email') == 'delivered@resend.dev'


def test_lembrete_job_and_event(admin, db):
    r = admin.get(f'{BASE_URL}/api/admin/inscricoes/lembrete-pagamento/resumo')
    assert r.status_code == 200
    total = r.json()['total']
    assert total >= 1
    assert db.inscricoes.count_documents({'finalized': True, 'email': {'$ne': 'delivered@resend.dev'}}) == 0
    job = admin.post(f'{BASE_URL}/api/admin/inscricoes/lembrete-pagamento').json()
    st = job
    for _ in range(60):
        st = admin.get(f'{BASE_URL}/api/admin/inscricoes/lembrete-pagamento/status/{job["id"]}').json()
        if st['status'] != 'enviando':
            break
        time.sleep(1)
    assert st['status'] == 'concluido', st
    assert st['enviados'] + st['falhas'] >= 1, st  # preview Resend key may be invalid (401)
    time.sleep(1)
    ev = admin.get(f'{BASE_URL}/api/admin/dashboard/realtime?limit=50').json()
    m = [e for e in ev if e['kind'] == 'lembrete_pagamento' and e.get('meta', {}).get('job_id') == job['id']]
    assert m, 'no lembrete_pagamento event'
    assert m[0]['description'].startswith(f"Lembrete de pagamento enviado para {st['enviados']} inscrito(s)")
    print(m[0]['description'])


def test_resumo_hydration(db):
    r = requests.get(f'{BASE_URL}/api/inscricao/resumo/{CPF}')
    assert r.status_code == 200
    j = r.json()
    assert j['nome'] == NOME
    assert float(j['valor']) == 200.0
