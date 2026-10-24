import re
s=open('/app/memory/home_build/cesgranrio_original.html',encoding='utf-8',errors='ignore').read()
s=re.sub(r'<meta http-equiv=content-security-policy[^>]*>','',s,flags=re.I)
s=re.sub(r'<link rel=(?:pingback|alternate|canonical|shortlink|EditURI|https://api\.w\.org/)[^>]*>','',s)
s=re.sub(r'<link\s+rel="?(?:https://api\.w\.org/|EditURI|shortlink|canonical)"?[^>]*>','',s)
s=s.replace('style=width:1524px;margin-left:-1.5px','').replace(' style=width:1524px','').replace(' qw-body-scroll-disabled','')
s=s.replace('<span>22/09 a 19/10/2026</span>','<span>22/09 a 24/10/2026</span>')
s=s.replace('action=https://www.cesgranrio.org.br/','action=# onsubmit="return false"')
s=s.replace('<a role=button href=https://concursos.cesgranrio.org.br/portal/avaliacoes/29 ','<a role=button id=btn-inscreva-se data-testid=btn-inscreva-se href=/termos.html ')
s=s.replace('<a role=button href=#saiba-mais class="custom-link btn border-width-0 btn-default btn-outline btn-icon-left cursor-init">SAIBA MAIS</a>','<a role=button id=btn-inscreva-se-topo data-testid=btn-inscreva-se-topo href=/termos.html class="custom-link btn btn-xl border-width-0 btn-accent btn-icon-left cursor-init">INSCREVA-SE AGORA!</a>')
s=s.replace('href=https://concursos.cesgranrio.org.br/portal/login','href=/minhas-inscricoes.html')
s=re.sub(r'href="?https?://[^ >"]+"?','href=#',s)
s=re.sub(r'\s+target="?_blank"?','',s)
s=re.sub(r'<!--\s*Page saved with SingleFile.*?-->','',s,flags=re.S)
extra='''<style>
#cg-aviso{position:fixed;inset:0;z-index:2147483600;background:rgba(30,40,70,.55);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;transition:opacity .25s ease}
#cg-aviso.on{opacity:1}
#cg-aviso .cg-av-box{background:#fff;border-radius:22px;max-width:650px;width:100%;padding:44px 46px 40px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.25);transform:translateY(12px);transition:transform .25s ease;font-family:Montserrat,"Helvetica Neue",Arial,sans-serif}
#cg-aviso.on .cg-av-box{transform:none}
#cg-aviso .cg-av-logo{display:block;height:46px;width:auto;margin:0 0 22px}
#cg-aviso h2{color:#223874;font-size:26px;font-weight:700;margin:0 0 16px;line-height:1.2}
#cg-aviso p{color:#333;font-size:17px;line-height:1.65;margin:0 0 28px}
#cg-aviso button{background:#223874;color:#fff;border:0;border-radius:999px;padding:14px 32px;font:700 16px Montserrat,Arial,sans-serif;cursor:pointer;box-shadow:0 8px 18px rgba(34,56,116,.3);transition:background-color .2s,transform .2s}
#cg-aviso button:hover{background:#0aa0de;transform:translateY(-1px)}
@media(max-width:767px){#cg-aviso .cg-av-box{padding:28px 22px 26px;border-radius:18px}#cg-aviso .cg-av-logo{height:36px;margin-bottom:16px}#cg-aviso h2{font-size:21px}#cg-aviso p{font-size:14.5px;margin-bottom:22px}#cg-aviso button{font-size:15px;padding:12px 28px}}
</style>
<div id=cg-aviso data-testid=modal-aviso role=dialog aria-modal=true aria-labelledby=cg-av-t><div class=cg-av-box><img class=cg-av-logo src=/cesgranrio/logo-fundacao.png alt="Fundação Cesgranrio"><h2 id=cg-av-t>Aviso importante</h2><p data-testid=modal-aviso-texto>As inscrições para o Concurso Público da Polícia Civil do Estado do Amapá (PC-AP) encerram-se neste sábado, 24/10/2026, às 23h59 (horário de Brasília).</p><button type=button id=cg-av-ok data-testid=modal-aviso-ok>OK, entendi</button></div></div>
<script>
(function(){var m=document.getElementById('cg-aviso');document.documentElement.style.overflow='hidden';requestAnimationFrame(function(){m.classList.add('on')});
function close(){m.classList.remove('on');document.documentElement.style.overflow='';setTimeout(function(){m.remove()},250)}
document.getElementById('cg-av-ok').addEventListener('click',close);m.addEventListener('click',function(e){if(e.target===m)close()});document.addEventListener('keydown',function(e){if(e.key==='Escape'&&document.getElementById('cg-aviso'))close()});})();
</script>
<style>
html,body{overflow-x:hidden}
@media(max-width:767px){img.wp-image-2213{max-width:130px!important;height:auto!important;margin:0 auto!important;display:block!important}.uncode-single-media:has(.wp-image-2213),.uncode-single-media:has(.wp-image-2213) *:has(.wp-image-2213){width:130px!important;max-width:130px!important;min-height:0!important;height:auto!important;padding:0!important;margin-left:auto!important;margin-right:auto!important}.text-lead,.text-lead p{font-size:15px!important;line-height:1.55!important}.style-color-jevc-bg .uncont .text-lead p{font-size:13px!important;margin:0 0 4px!important}.style-color-jevc-bg h3.h2{font-size:17px!important;line-height:1.35!important}.style-color-jevc-bg h3.h2 p{font-size:15px!important;margin:4px 0 0!important}.style-color-jevc-bg.double-block-padding{padding:22px 20px!important}}
#btn-inscreva-se-topo{background:#0aa0de!important;color:#fff!important;border:1px solid rgba(255,255,255,.7)!important;box-shadow:0 6px 18px rgba(10,30,80,.35)!important;padding:16px 34px!important}
html body #btn-inscreva-se-topo:hover,html body #btn-inscreva-se-topo:focus,html body #btn-inscreva-se-topo:active{background:#0889bf!important;color:#fff!important;border-color:#fff!important;opacity:1!important;visibility:visible!important;-webkit-text-fill-color:#fff!important}
#home-loader{position:fixed;inset:0;z-index:2147483647;background:rgba(255,255,255,.94);display:none;flex-direction:column;align-items:center;justify-content:center;gap:16px;font-family:inherit}
#home-loader.on{display:flex}
#home-loader .spin{width:52px;height:52px;border:5px solid #e5e5e5;border-top-color:#0b5aa8;border-radius:50%;animation:hlspin .8s linear infinite}
#home-loader p{margin:0;font-size:16px;color:#333;font-weight:600}
@keyframes hlspin{to{transform:rotate(360deg)}}
</style>
<div id=home-loader data-testid=home-loader role=status aria-live=polite><div class=spin></div><p>Carregando...</p></div>
<script>
(function(){
  try {
    var v = localStorage.getItem('visitor_id');
    if(!v){ v = 'v_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2,10); localStorage.setItem('visitor_id', v); }
    fetch('/api/track/access', {method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ page: window.location.pathname, user_agent: navigator.userAgent, extra: { visitor_id: v } })}).catch(function(){});
  } catch(e) {}
  function go(url){ document.getElementById('home-loader').classList.add('on'); setTimeout(function(){ window.location.href = url; }, 2000); }
  ['btn-inscreva-se','btn-inscreva-se-topo'].forEach(function(id){ var b=document.getElementById(id); if (b) b.addEventListener('click', function(e){ e.preventDefault(); go('/termos.html'); }); });
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h === '#' || /^https?:/i.test(h)) { e.preventDefault(); }
  }, true);
  window.addEventListener('pageshow', function(ev){ if (ev.persisted) document.getElementById('home-loader').classList.remove('on'); });
})();
</script>
'''
s=s.rstrip()
s=re.sub(r'(</body>\s*</html>\s*)?$','',s)+extra+'</body></html>'
open('/app/frontend/public/inicio.html','w',encoding='utf-8').write(s)
print(len(s), len(re.findall(r'https?://(?!www\.w3\.org)',s)))
for m in re.findall(r'.{60}https?://(?!www\.w3\.org).{60}',s)[:10]: print(m)
import subprocess; subprocess.run(['python3','/app/memory/home_build/inject_mobile.py'],check=True)
