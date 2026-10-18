import re, json, os, shutil
from PIL import Image
PUB = '/app/frontend/public'
BK = '/app/memory/backups/pages_vunesp'
HB = '/app/memory/home_build'
CG = PUB + '/cesgranrio'
os.makedirs(CG, exist_ok=True)

# logo azul (para fundo branco / impressao)
im = Image.open(CG + '/logo-branco.png').convert('RGBA')
px = im.load()
for y in range(im.size[1]):
    for x in range(im.size[0]):
        a = px[x, y][3]
        px[x, y] = (10, 160, 222, a)
im.save(CG + '/logo-azul.png', optimize=True)

# fontes Montserrat da pagina original
orig = open(HB + '/cesgranrio_original.html', encoding='utf-8', errors='ignore').read()
ff = [f for f in re.findall(r'@font-face\{[^}]*\}', orig) if 'Montserrat' in f]
open(CG + '/fonts.css', 'w', encoding='utf-8').write(''.join(ff))

header = ('<header class="cg-h"><div class="cg-in">'
          '<a href="/" class="cg-logo" title="Voltar para a página inicial"><img src="/cesgranrio/logo-fundacao.png" alt="Fundação Cesgranrio"></a>'
          '<nav class="cg-nav"><a href="/" class="cg-link cg-active">Avaliações e Concursos</a><a href=# class="cg-link">Contato</a><a href=# title="Área do Candidato">Área do Candidato</a></nav>'
          '</div></header>')
footer = ('<footer id="rodape" class="cg-f"><div class="cg-fbar"><img src="/cesgranrio/logo-fundacao-branco.png" alt="Fundação Cesgranrio"><span>v 1.0.20261007.3</span></div></footer>')
open(CG + '/parts.json', 'w', encoding='utf-8').write(json.dumps({'h': header, 'f': footer}, ensure_ascii=False))
css = '''
*{box-sizing:border-box}a{text-decoration:none}
.cg-h,.cg-f{font-family:Roboto,"Helvetica Neue",Arial,sans-serif}
.cg-h{background:#fff;box-shadow:0 1px 0 rgba(0,0,0,.04)}
.cg-in{max-width:1320px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;min-height:80px;position:relative}
.cg-logo img{height:44px;width:auto;display:block}
.cg-nav{display:flex;gap:26px;align-items:center}
.cg-link{color:#4e5f8f;font-size:16px;font-weight:500;text-transform:uppercase;padding:6px 8px;position:relative}
.cg-link:before{content:"";position:absolute;left:0;bottom:-4px;height:3px;width:0;background:#4e5f8f;transition:width .3s ease}
.cg-link:hover:before,.cg-active:before{width:100%}
.cg-nav a[title="Área do Candidato"],.vn-minhas-desk{background:#4e5f8f!important;color:#fff!important;font:700 13px Roboto,Arial,sans-serif!important;text-transform:uppercase;padding:10px 14px!important;border-radius:4px!important;letter-spacing:0!important;transition:background-color .2s}
.cg-nav a[title="Área do Candidato"]:hover,.vn-minhas-desk:hover{background:#42517a!important}
.vn-minhas{background:#4e5f8f!important;border-radius:4px!important}.vn-minhas:hover{background:#42517a!important}
.vn-minhas-box{top:22px!important;transform:none!important}
.cg-f{margin-top:40px}
.cg-fbar{background:#223874;min-height:48px;display:flex;align-items:center;justify-content:space-between;padding:0 48px;flex-wrap:wrap;gap:8px}
.cg-fbar img{max-height:26px;width:auto;display:block}
.cg-fbar span{color:#fff;font-size:14px;font-style:italic}
@media(max-width:991px){.cg-nav{display:none}}
@media(max-width:767px){.cg-in{min-height:64px;padding:0 14px}.cg-logo img{height:36px}.vn-minhas-box{top:14px!important}.cg-fbar{padding:10px 16px;justify-content:center}.cg-fbar img{max-height:22px}}
'''
open(CG + '/chrome.css', 'w', encoding='utf-8').write(css)

# loader do cabecalho/rodape
js = open(BK + '/seduc-theme.js', encoding='utf-8').read()
js = js.replace("var V='16';", "var V='17';").replace('/vunesp/fonts.css', '/cesgranrio/fonts.css').replace('/vunesp/chrome.css', '/cesgranrio/chrome.css').replace('/vunesp/parts.json', '/cesgranrio/parts.json')
js = js.replace('.vn-minhas-box{position:absolute;right:15px;top:50%;', '.vn-minhas-box{position:absolute;right:15px;top:50%;')
js = js.replace("vunesp-footer-host", "cg-footer-host")
js = js.replace("if(MINHAS){hh=hh.replace(", "if(!MINHAS){hh=hh.replace('<a href=# title=\"Área do Candidato\">','<a href=\"/minhas-inscricoes.html\" title=\"Área do Candidato\">');}if(MINHAS){hh=hh.replace(", 1)
js = js.replace('font-family:"Open Sans",Helvetica,Arial,sans-serif;font-size:14px', 'font-family:Roboto,Helvetica,Arial,sans-serif;font-size:14px').replace("var V='17';", "var V='18';")
open(PUB + '/seduc/seduc-theme.js', 'w', encoding='utf-8').write(js)
open(HB + '/chrome_loader.js', 'w', encoding='utf-8').write(js)

# pages.css: cores Cesgranrio
pc = open(BK + '/pages.css', encoding='utf-8').read()
for a, b in [('#31708f', '#18295a'), ('#d9534f', '#0aa0de'), ('#c9302c', '#0889bf'), ('#ac2925', '#0779a8'), ('#1172db', '#0aa0de'),
             ('"Helvetica Neue",Helvetica,Arial,sans-serif', 'Montserrat,"Helvetica Neue",Arial,sans-serif')]:
    pc = pc.replace(a, b)
pc += '\nhtml,html body,html body:not(#vn_a):not(#vn_b):not(#vn_c){background-color:#f2f2f2!important}'
pc += '\nhtml body:not(#vn_a):not(#vn_b) .aocp-edital-card .aec-head h3,html body:not(#vn_a):not(#vn_b) .wrap .card .edhead h3{color:#18295a!important;font-weight:600!important}\nhtml body:not(#vn_a):not(#vn_b) .vn-sub{color:#0aa0de!important}\n'
open(PUB + '/cesgranrio/pages.css', 'w', encoding='utf-8').write(pc)
open(HB + '/pages.css', 'w', encoding='utf-8').write(pc)

REPL = [
    (' | Fundação VUNESP', ' | Cesgranrio'),
    ('Vestibular Unesp 2027 - Fundação VUNESP', 'Concurso Polícia Civil do Amapá 2026 - Cesgranrio'),
    ('Vestibular Unesp 2027 - VNSP2514', 'Concurso Polícia Civil do Amapá 2026'),
    ('Universidade Estadual Paulista (Unesp) - VNSP2514', 'Polícia Civil do Estado do Amapá (PC-AP)'),
    ('Universidade Estadual Paulista - UNESP', 'Polícia Civil do Estado do Amapá - PC-AP'),
    ('© FUNDAÇÃO VUNESP — VESTIBULAR UNESP 2027', '© FUNDAÇÃO CESGRANRIO — CONCURSO POLÍCIA CIVIL DO AMAPÁ 2026'),
    ('Fundação VUNESP — Vestibulares e Concursos', 'Fundação Cesgranrio — Concursos'),
    ('<img src="/vunesp/vunesp-logo.png" alt="Fundação VUNESP"', '<img src="/cesgranrio/logo-azul.png" alt="Cesgranrio"'),
    ('Fundação VUNESP', 'Fundação Cesgranrio'),
    ('Vestibular Unesp 2027', 'Concurso Polícia Civil do Amapá 2026'),
    ('atendimento@vunesp.com.br', 'atendimento@cesgranrio.org.br'),
    ('VNSP2514', 'PC-AP 2026'),
    ('fins deste vestibular', 'fins deste concurso'),
    ('concursos pï¿½blicos, vestibular', 'concursos públicos'),
    ('/vunesp/pages.css?v=8', '/cesgranrio/pages.css?v=11'),
    ('/seduc/seduc-theme.js?v=16', '/seduc/seduc-theme.js?v=18'),
    ('border-top-color:#d9534f;', 'border-top-color:#0aa0de;'),
]
def cut_el(t, eid):
    m = re.search(r'<(\w+)\b[^>]*\b(?:id="%s"|class="%s")[^>]*>' % (re.escape(eid), re.escape(eid)), t)
    if not m:
        return t
    tag = m.group(1); depth = 0
    for mm in re.finditer(r'<(/?)%s\b[^>]*>' % tag, t[m.start():]):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            return t[:m.start()] + t[m.start() + mm.end():]
    return t
LEGACY = ['__fgv_topbar', 'TopoMobile', 'TopMenu', 'Topo', 'bgConcurso', 'Rodape', '__fgv_footer', '__cebraspe_footer_root']
for p in ['inscricao.html', 'dados-inscricao.html', 'confirmacao.html', 'inscricao-realizada.html', 'pagamento-pix.html', 'minhas-inscricoes.html']:
    t = open(BK + '/' + p, encoding='utf-8').read()
    for a, b in REPL:
        t = t.replace(a, b)
    t = re.sub(r'<link rel="shortcut icon" href="data:[^"]*"[^>]*>', '<link rel="shortcut icon" href="/cesgranrio/simbolo.png" type="image/png">', t)
    for eid in LEGACY:
        t = cut_el(t, eid)
    t = re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + re.sub(r'/\*.*?\*/', '', m.group(2), flags=re.S) + m.group(3), t, flags=re.S)
    t = t.replace('a reserva de vagas prevista na Lei Estadual nº 17.432/2021 para pessoas negras', 'a reserva de vagas para pessoas negras, nos termos da decisão do Tribunal de Justiça do Estado do Amapá')
    t = t.replace('a reserva de vagas previstas na Lei Estadual nº 17.433/2021 para pessoas com deficiência', 'a reserva de vagas prevista no art. 4º, parágrafo único, da Lei Estadual nº 066/1993 para pessoas com deficiência')
    t = t.replace('a reserva de vagas prevista na Lei Estadual nº 17.433/2021 para pessoas com deficiência', 'a reserva de vagas prevista no art. 4º, parágrafo único, da Lei Estadual nº 066/1993 para pessoas com deficiência')
    t = t.replace('Curso Escolhido', 'Cargo Escolhido').replace('<span class="k">Curso</span>', '<span class="k">Cargo</span>')
    if p == 'dados-inscricao.html':
        a0 = t.index('<div class="fgv-field"><label><span class="error">*</span> Polo universitário (cidade)</label>')
        a1 = t.index('</script>', a0) + len('</script>')
        t = t[:a0] + open(HB + '/cargo_pcap.html', encoding='utf-8').read() + t[a1:]
        t = t.replace('<label class="description">Curso</label>', '<label class="description">Cargo</label>', 1)
        t, n = re.subn(r'(<select class="select" data-testid="select-municipio-prova" id="MUNICIPIO_PROVA" name="MUNICIPIO_PROVA" required="">).*?</select>', r'\1\n<option value="MACAPA/AP" data-uf="AP" selected="">MACAPÁ</option>\n</select>', t, count=1, flags=re.S)
        assert n == 1
        t = t.replace('<input type="hidden" id="UF_PROVA" name="UF_PROVA" value="SP">', '<input type="hidden" id="UF_PROVA" name="UF_PROVA" value="AP">')
        t = t.replace("function syncUf(){ var o = mp && mp.options[mp.selectedIndex]; if(uf) uf.value = (o && o.getAttribute('data-uf')) || 'SP'; }", "function syncUf(){ if(mp && !mp.value){ mp.value='MACAPA/AP'; } var o = mp && mp.options[mp.selectedIndex]; if(uf) uf.value = (o && o.getAttribute('data-uf')) || 'AP'; }")
        assert "mp.value='MACAPA/AP'" in t
    t = t.replace("({'SP':'São Paulo','DF':'Distrito Federal','MS':'Mato Grosso do Sul','PR':'Paraná','MG':'Minas Gerais'}[d.UF_PROVA]", "({'AP':'Amapá'}[d.UF_PROVA]")
    if p == 'inscricao.html':
        a0 = t.index('<fieldset class="vn-quest" data-testid="questionario-fieldset">')
        a1 = t.index('</fieldset>', a0) + len('</fieldset>')
        t = t[:a0] + t[a1:]
    if p == 'confirmacao.html':
        t = re.sub(r'<div class="conf-row"><span class="conf-lbl">Estado civil</span>.*?</div>', '', t, count=1)
        t = re.sub(r'<div class="conf-sec" data-testid="conf-sec-2">Ensino médio</div>(?:<div class="conf-row">.*?</div>){3}', '', t, count=1)
        for k in ["  set('c-estado-civil', d.ESTADO_CIVIL || '');\n", "  set('c-tipo-em', d.TIPO_ENSINO_MEDIO || '');\n", "  set('c-uf-em', d.UF_ENSINO_MEDIO || '');\n", "  set('c-ano-em', d.ANO_ENSINO_MEDIO || '');\n"]:
            assert k in t, k
            t = t.replace(k, '')
    if p == 'inscricao-realizada.html':
        t = t.replace('var __v = 225;', "var __v = ({'1':200,'2':150})[String(d.__cargo_codigo || d.VAGA || '')] || 150;")
    open(PUB + '/' + p, 'w', encoding='utf-8').write(t)
    body = re.sub(r'data:[^"\')\s]{100,}', '', t)
    print(p, sorted(set(re.findall(r'(?i)vunesp(?!/pages)|unesp|vestibular', body))))
import subprocess; subprocess.run(['python3', HB + '/build_termos.py'], check=True)
print('ok')
import subprocess; subprocess.run(['python3','/app/memory/home_build/clean_legacy.py'],check=True); subprocess.run(['python3','/app/memory/home_build/inject_mobile.py'],check=True)
