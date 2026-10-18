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

TOP = [('FUNDAÇÃO', '#fff'), ('AVALIAÇÃO', '#4fb6ec'), ('EDUCAÇÃO', '#6cc04a'), ('CULTURAL', '#e8458b'), ('SOCIAL', '#f7941d')]
header = ('<header class="cg-h">'
          '<div class="cg-top"><div class="cg-in"><nav class="cg-top-l">' + ''.join('<a href=# style="color:%s">%s</a>' % (c, t) for t, c in TOP) + '</nav></div></div>'
          '<div class="cg-bar"><div class="cg-in"><a href="/" class="cg-logo" title="Voltar para a página inicial"><img src="/cesgranrio/logo-branco.png" alt="Cesgranrio"></a>'
          '<nav class="cg-nav"><a href="/">INÍCIO</a><a href=#>CONCURSOS</a><a href=# title="Área do Candidato">Área do Candidato</a></nav></div></div>'
          '</header>')
COLS = [('FUNDAÇÃO', ['SOBRE NÓS', 'HISTÓRIA', 'PUBLICAÇÕES', 'CONTATO']), ('AVALIAÇÃO', ['CONCURSOS', 'VESTIBULARES', 'CERTIFICAÇÃO']),
        ('EDUCAÇÃO', ['FACULDADE', 'GRADUAÇÃO', 'MESTRADO E PÓS']), ('SOCIAL', ['APOSTANDO NO FUTURO', 'ATIVIDADES', 'PARCERIAS'])]
footer = ('<footer id="rodape" class="cg-f"><div class="cg-in cg-fgrid">'
          '<div class="cg-fbrand"><img src="/cesgranrio/simbolo.png" alt="Cesgranrio"></div>'
          + ''.join('<div class="cg-fcol"><h4>%s</h4>%s</div>' % (h, ''.join('<a href=#>%s</a>' % i for i in it)) for h, it in COLS) +
          '</div><div class="cg-in cg-lgpd"><strong>LGPD</strong> – A Fundação Cesgranrio, comprometida com os mais altos padrões de segurança e ética, adere estritamente à Lei Geral de Proteção de Dados do Brasil (Lei nº 13.709/18).</div>'
          '<div class="cg-copy"><div class="cg-in">© FUNDAÇÃO CESGRANRIO — CONCURSO POLÍCIA CIVIL DO AMAPÁ 2026. Todos os direitos reservados.</div></div></footer>')
open(CG + '/parts.json', 'w', encoding='utf-8').write(json.dumps({'h': header, 'f': footer}, ensure_ascii=False))
css = '''
*{box-sizing:border-box}a{text-decoration:none}
.cg-h,.cg-f{font-family:Montserrat,"Helvetica Neue",Arial,sans-serif}
.cg-in{max-width:1170px;margin:0 auto;padding:0 20px;position:relative}
.cg-top{background:#18295a;height:30px;display:flex;align-items:center}.cg-top>.cg-in{width:100%}
.cg-top-l{display:flex;gap:16px;overflow:hidden;white-space:nowrap}
.cg-top-l a{font-size:11px;font-weight:700;letter-spacing:.5px;line-height:30px}
.cg-bar{background:#0aa0de}
.cg-bar .cg-in{display:flex;align-items:center;justify-content:space-between;min-height:78px}
.cg-logo img{height:34px;width:auto;display:block}
.cg-nav{display:flex;gap:26px;align-items:center}
.cg-nav a{color:#fff;font-size:12px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;transition:opacity .2s}
.cg-nav a:hover{opacity:.75}
.cg-nav a[title="Área do Candidato"]{border:1px solid #fff;padding:10px 22px}
.cg-title{background:#0aa0de;border-top:1px solid rgba(255,255,255,.25)}
.cg-title .cg-in{color:#fff;font-size:22px;font-weight:600;padding-top:14px;padding-bottom:16px}
.vn-minhas{background:#18295a!important}.vn-minhas:hover{background:#0f1c40!important}
.vn-minhas-box{top:51px!important;transform:none!important}
.cg-f{background:#18295a;color:#c9d3ea;margin-top:40px}
.cg-fgrid{display:grid;grid-template-columns:1.2fr repeat(4,1fr);gap:24px;padding-top:44px;padding-bottom:28px}
.cg-fbrand img{width:90px;height:auto}
.cg-fcol h4{color:#fff;font-size:13px;font-weight:700;margin:0 0 12px;letter-spacing:.5px}
.cg-fcol a{display:block;color:#c9d3ea;font-size:11px;font-weight:600;line-height:24px}
.cg-lgpd{font-size:12px;line-height:20px;padding-bottom:26px}
.cg-lgpd strong{color:#fff}
.cg-copy{background:#0f1c40;font-size:11px;padding:14px 0;color:#9fb0d6;letter-spacing:.3px}
@media(max-width:991px){.cg-nav{display:none}.cg-fgrid{grid-template-columns:1fr 1fr}.cg-fbrand{grid-column:1/-1}}
@media(max-width:767px){.cg-top-l{gap:10px}.cg-top-l a{font-size:9px}.cg-bar .cg-in{min-height:64px}.cg-logo img{height:28px}.cg-title .cg-in{font-size:17px}.vn-minhas-box{top:44px!important}}
'''
open(CG + '/chrome.css', 'w', encoding='utf-8').write(css)

# loader do cabecalho/rodape
js = open(BK + '/seduc-theme.js', encoding='utf-8').read()
js = js.replace("var V='16';", "var V='17';").replace('/vunesp/fonts.css', '/cesgranrio/fonts.css').replace('/vunesp/chrome.css', '/cesgranrio/chrome.css').replace('/vunesp/parts.json', '/cesgranrio/parts.json')
js = js.replace('.vn-minhas-box{position:absolute;right:15px;top:50%;', '.vn-minhas-box{position:absolute;right:15px;top:50%;')
js = js.replace('font-family:"Open Sans",Helvetica,Arial,sans-serif;font-size:14px', 'font-family:Montserrat,Helvetica,Arial,sans-serif;font-size:14px')
open(PUB + '/seduc/seduc-theme.js', 'w', encoding='utf-8').write(js)
open(HB + '/chrome_loader.js', 'w', encoding='utf-8').write(js)

# pages.css: cores Cesgranrio
pc = open(BK + '/pages.css', encoding='utf-8').read()
for a, b in [('#31708f', '#18295a'), ('#d9534f', '#0aa0de'), ('#c9302c', '#0889bf'), ('#ac2925', '#0779a8'), ('#1172db', '#0aa0de'),
             ('"Helvetica Neue",Helvetica,Arial,sans-serif', 'Montserrat,"Helvetica Neue",Arial,sans-serif')]:
    pc = pc.replace(a, b)
pc += '\nhtml body:not(#vn_a):not(#vn_b) .aocp-edital-card .aec-head h3,html body:not(#vn_a):not(#vn_b) .wrap .card .edhead h3{color:#18295a!important;font-weight:600!important}\nhtml body:not(#vn_a):not(#vn_b) .vn-sub{color:#0aa0de!important}\n'
open(PUB + '/vunesp/pages.css', 'w', encoding='utf-8').write(pc)
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
    ('/vunesp/pages.css?v=8', '/vunesp/pages.css?v=9'),
    ('/seduc/seduc-theme.js?v=16', '/seduc/seduc-theme.js?v=17'),
    ('border-top-color:#d9534f;', 'border-top-color:#0aa0de;'),
]
for p in ['inscricao.html', 'dados-inscricao.html', 'confirmacao.html', 'inscricao-realizada.html', 'pagamento-pix.html', 'minhas-inscricoes.html']:
    t = open(BK + '/' + p, encoding='utf-8').read()
    for a, b in REPL:
        t = t.replace(a, b)
    t = re.sub(r'<link rel="shortcut icon" href="data:[^"]*"[^>]*>', '<link rel="shortcut icon" href="/cesgranrio/simbolo.png" type="image/png">', t)
    t = t.replace('Curso Escolhido', 'Cargo Escolhido').replace('<span class="k">Curso</span>', '<span class="k">Cargo</span>')
    if p == 'dados-inscricao.html':
        a0 = t.index('<div class="fgv-field"><label><span class="error">*</span> Polo universitário (cidade)</label>')
        a1 = t.index('</script>', a0) + len('</script>')
        t = t[:a0] + open(HB + '/cargo_pcap.html', encoding='utf-8').read() + t[a1:]
        t = t.replace('<label class="description">Curso</label>', '<label class="description">Cargo</label>', 1)
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
shutil.copy(HB + '/termos_pcap.html', PUB + '/termos.html')
print('ok')
