"""Amapá law text + legacy (Unesp/VUNESP/Cebraspe/São Paulo) removal tests."""
import os
import re
import sys
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
PAGES = ['/', '/inicio.html', '/termos.html', '/inscricao.html', '/dados-inscricao.html', '/confirmacao.html',
         '/inscricao-realizada.html', '/pagamento-pix.html', '/minhas-inscricoes.html', '/donaspainel',
         '/donaspainel-documentos.html', '/cesgranrio/pages.css']
BANNED = ['Unesp', 'UNESP', 'VUNESP', 'Vestibular Unesp', 'VNSP2514', 'Cebraspe', 'CEBRASPE', 'São Paulo',
          'Sao Paulo', 'SÃO PAULO', '17.432', '17.433', 'SEDUC']
LEGACY_IDS = ['id="Topo"', 'id="TopoMobile"', 'id="TopMenu"', 'id="Rodape"', 'id="__fgv_topbar"',
              'id="__fgv_footer"', 'id="__cebraspe_footer_root"', 'bgConcurso']


def _get(p):
    return requests.get(f'{BASE_URL}{p}', timeout=20)


# Page source free of legacy brand strings (ignoring hostname)
@pytest.mark.parametrize('page', PAGES)
def test_no_banned_strings(page):
    r = _get(page)
    assert r.status_code == 200, page
    txt = r.text.replace(BASE_URL, '').replace('vunesp.preview', '')
    hits = [b for b in BANNED if b in txt]
    # SEDUC allowed only as path identifier /seduc/
    if 'SEDUC' in hits and not re.search(r'SEDUC(?![-/\w]*\.js)', txt.replace('/seduc/', '')):
        hits.remove('SEDUC')
    assert not hits, f'{page}: {hits}'


# Legacy DOM blocks removed
@pytest.mark.parametrize('page', ['/inscricao.html', '/dados-inscricao.html', '/confirmacao.html',
                                  '/inscricao-realizada.html', '/pagamento-pix.html'])
def test_no_legacy_blocks(page):
    txt = _get(page).text
    hits = re.findall(r'id="(Topo|TopoMobile|TopMenu|Rodape|__fgv_topbar|__fgv_footer|__cebraspe_footer_root)"', txt)
    hits += re.findall(r'class="[^"]*\bbgConcurso\b[^"]*"', txt)
    assert not hits, f'{page}: {hits}'


# Amapá law text present
@pytest.mark.parametrize('page', ['/dados-inscricao.html', '/confirmacao.html'])
def test_amapa_law_text(page):
    txt = _get(page).text
    assert 'decisão do Tribunal de Justiça do Estado do Amapá' in txt or 'decis&atilde;o do Tribunal' in txt, page
    assert 'Lei Estadual nº 066/1993' in txt or 'Lei Estadual n&ordm; 066/1993' in txt, page
    assert 'art. 4º, parágrafo único' in txt or 'art. 4&ordm;' in txt, page


# Pix merchant/city
def test_pix_merchant():
    r = requests.post(f'{BASE_URL}/api/pix/generate', json={'cargo_codigo': '1', 'valor': 1, 'txid': 'TESTAP'}, timeout=15)
    assert r.status_code == 200
    d = r.json()
    assert d['valor'] == 200.0
    assert 'CONCURSO PC AP 2026' in d['pix_code'] and 'MACAPA AP' in d['pix_code'], d['pix_code']


# Admin login + listing
def test_admin_login_listing():
    r = requests.post(f'{BASE_URL}/api/admin/auth/login', json={'username': 'donas', 'password': 'Seinao10@@'}, timeout=15)
    assert r.status_code == 200
    h = {'Authorization': f"Bearer {r.json()['token']}"}
    r = requests.get(f'{BASE_URL}/api/admin/inscriptions', headers=h, timeout=15)
    assert r.status_code == 200
    # note: legacy DB records may still hold old concurso names (data, not code)
    assert 'items' in r.json()


# Email HTML builder
def test_email_html():
    sys.path.insert(0, '/app/backend')
    import email_service as es
    import inspect
    sig = inspect.signature(es.build_inscricao_email_html)
    kwargs = {}
    for n, p in sig.parameters.items():
        if p.default is inspect.Parameter.empty:
            kwargs[n] = {'nome': 'TEST', 'cpf': '52998224725'}.get(n, 'TEST')
    try:
        html = es.build_inscricao_email_html(**kwargs)
    except Exception:
        html = es.build_inscricao_email_html({'nome': 'TEST', 'cpf': '52998224725', 'cargo_codigo': '1'})
    if isinstance(html, tuple):
        html = ' '.join(str(x) for x in html)
    assert 'Concurso Polícia Civil do Amapá 2026 - Cesgranrio' in html
    assert '19/10/2026' in html
    for b in ['VUNESP', 'Unesp', 'São Paulo', 'Cebraspe']:
        assert b not in html, b
