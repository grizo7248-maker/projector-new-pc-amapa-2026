import re
s=open('/app/memory/home_build/cesgranrio_original.html',encoding='utf-8',errors='ignore').read()
s=re.sub(r'<meta http-equiv=content-security-policy[^>]*>','',s,flags=re.I)
s=re.sub(r'<link rel=(?:pingback|alternate|canonical|shortlink|EditURI|https://api\.w\.org/)[^>]*>','',s)
s=re.sub(r'<link\s+rel="?(?:https://api\.w\.org/|EditURI|shortlink|canonical)"?[^>]*>','',s)
s=s.replace('style=width:1524px;margin-left:-1.5px','').replace(' style=width:1524px','').replace(' qw-body-scroll-disabled','')
s=s.replace('action=https://www.cesgranrio.org.br/','action=# onsubmit="return false"')
s=s.replace('<a role=button href=https://concursos.cesgranrio.org.br/portal/avaliacoes/29 ','<a role=button id=btn-inscreva-se data-testid=btn-inscreva-se href=/termos.html ')
s=s.replace('<a role=button href=#saiba-mais class="custom-link btn border-width-0 btn-default btn-outline btn-icon-left cursor-init">SAIBA MAIS</a>','<a role=button id=btn-inscreva-se-topo data-testid=btn-inscreva-se-topo href=/termos.html class="custom-link btn btn-xl border-width-0 btn-accent btn-icon-left cursor-init">INSCREVA-SE AGORA!</a>')
s=s.replace('href=https://concursos.cesgranrio.org.br/portal/login','href=/minhas-inscricoes.html')
s=re.sub(r'href="?https?://[^ >"]+"?','href=#',s)
s=re.sub(r'\s+target="?_blank"?','',s)
s=re.sub(r'<!--\s*Page saved with SingleFile.*?-->','',s,flags=re.S)
extra='''<style>
html,body{overflow-x:hidden}
#btn-inscreva-se-topo{background:#0aa0de!important;color:#fff!important;border:1px solid rgba(255,255,255,.7)!important;box-shadow:0 6px 18px rgba(10,30,80,.35)!important;padding:16px 34px!important}
#btn-inscreva-se-topo:hover{background:#0889bf!important}
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
