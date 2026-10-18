import re
s=open('/app/memory/home_build/termos_cesgranrio_original.html',encoding='utf-8',errors='ignore').read()
s=re.sub(r'<meta http-equiv=content-security-policy[^>]*>','',s,flags=re.I)
s=re.sub(r'<link rel=canonical[^>]*>','',s)
s=re.sub(r'<!--\s*Page saved with SingleFile.*?-->','',s,flags=re.S)
s=s.replace('href=https://concursos.cesgranrio.org.br/portal/inscricao/26/bb8e8359-6151-4394-a327-139ed657575c>','href=/inscricao.html data-cargo=1 id=btn-inscrever-delegado data-testid=btn-inscrever-delegado>')
s=s.replace('href=https://concursos.cesgranrio.org.br/portal/inscricao/26/ebfc6857-646d-456b-8066-e1f574f040cd>','href=/inscricao.html data-cargo=2 id=btn-inscrever-investigador data-testid=btn-inscrever-investigador>')
s=s.replace('href=https://concursos.cesgranrio.org.br/portal/avaliacoes>','href=/>')
s=s.replace('href=https://concursos.cesgranrio.org.br/portal/login>','href=/minhas-inscricoes.html>')
s=re.sub(r'href="?https?://[^ >"]+"?','href=#',s)
s=re.sub(r'\s+target="?_blank"?','',s)
extra='''<style>
#home-loader{position:fixed;inset:0;z-index:2147483647;background:rgba(255,255,255,.94);display:none;flex-direction:column;align-items:center;justify-content:center;gap:16px;font-family:inherit}
#home-loader.on{display:flex}
#home-loader .spin{width:52px;height:52px;border:5px solid #e5e5e5;border-top-color:#0aa0de;border-radius:50%;animation:hlspin .8s linear infinite}
#home-loader p{margin:0;font-size:16px;color:#333;font-weight:600}
@keyframes hlspin{to{transform:rotate(360deg)}}
app-card-collapse .card-body{transition:height .25s ease}
@media(max-width:767px){body{font-size:14px!important}.list-group-item{font-size:14px!important;padding:10px 16px!important}.card-title.titulo{font-size:19px!important}.badge{font-size:11px!important}.card-text,.evento-descricao p{font-size:13.5px!important;line-height:1.5!important}.card-header-titulo,.titulo-collapse{font-size:13.5px!important}app-card-collapse .btn{font-size:12px!important;padding:6px 10px!important}app-card-collapse .card-body,app-card-collapse .card-body p,app-card-collapse .card-body li{font-size:13.5px!important}#cg-cargos-mobile{margin:14px 0 6px}#cg-cargos-mobile app-card-collapse{display:block;margin-bottom:10px}}
app-card-collapse .card-header{cursor:pointer}
app-card-collapse .card-header-titulo i{display:inline-block;transition:transform .25s ease}
app-card-collapse .card-header.expanded .card-header-titulo i{transform:rotate(180deg)}
html,body{overflow-x:hidden}
.evento-descricao,.evento-descricao .card-text{max-height:none!important;overflow:visible!important;-webkit-line-clamp:unset!important;display:block!important}
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
  function go(url){ document.getElementById('home-loader').classList.add('on'); setTimeout(function(){ window.location.href = url; }, 1500); }
  document.querySelectorAll('a[data-cargo]').forEach(function(a){
    a.addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); try{ localStorage.setItem('cargo_pre', a.getAttribute('data-cargo')); }catch(x){} go('/inscricao.html'); });
  });
  if (window.matchMedia('(max-width: 767px)').matches) {
    var lg = document.querySelector('.list-group'), cards = document.querySelectorAll('app-card-collapse');
    if (lg && cards.length) {
      var anchor = lg.closest('.card') || lg, box = document.createElement('div');
      box.id = 'cg-cargos-mobile'; box.setAttribute('data-testid','cargos-mobile');
      cards.forEach(function(c){ box.appendChild(c); });
      anchor.parentNode.insertBefore(box, anchor.nextSibling);
    }
  }
  document.querySelectorAll('app-card-collapse').forEach(function(c, i){
    var h=c.querySelector('.card-header'), b=c.querySelector('.card-body'), ic=h && h.querySelector('.card-header-titulo i');
    if(!h||!b) return;
    h.setAttribute('data-testid','cargo-toggle-'+(i+1)); b.setAttribute('data-testid','cargo-detalhes-'+(i+1));
    h.addEventListener('click', function(e){
      if(e.target.closest('a')) return;
      var open = h.classList.contains('collapsed');
      h.classList.toggle('collapsed', !open); h.classList.toggle('expanded', open);
      b.classList.toggle('collapsed', !open); b.classList.toggle('expanded', open);
      if(open){ b.style.overflow='hidden'; b.style.height=b.scrollHeight+'px'; setTimeout(function(){ if(b.classList.contains('expanded')){ b.style.height=''; b.style.overflow=''; } }, 260); }
      else { b.style.overflow='hidden'; b.style.height=b.scrollHeight+'px'; b.offsetHeight; b.style.height='0px'; }
    });
  });
  document.querySelectorAll('button.btn-outline-primary').forEach(function(bt){ if(/VOLTAR/i.test(bt.textContent)){ bt.setAttribute('data-testid','btn-voltar-termos'); bt.addEventListener('click', function(){ go('/'); }); } });
  document.querySelectorAll('a.list-group-item').forEach(function(a){
    a.addEventListener('click', function(e){ e.preventDefault(); var t=a.textContent.trim().toUpperCase();
      var el=[].slice.call(document.querySelectorAll('h1,h2,h3,h4,h5,h6,.card-header span,span.fw-bold')).filter(function(x){ return x.textContent.trim().toUpperCase()===t && !x.closest('.list-group'); })[0];
      if(el) el.scrollIntoView({behavior:'smooth', block:'start'}); });
  });
  document.addEventListener('click', function(e){ var a=e.target.closest && e.target.closest('a'); if(!a) return; var h=a.getAttribute('href'); if(h==='#'||h===null&&!a.classList.contains('list-group-item')){ e.preventDefault(); } }, true);
})();
</script>
'''
s=s.rstrip()
s=re.sub(r'(</body>\s*</html>\s*)?$','',s)+extra+'</body></html>'
open('/app/frontend/public/termos.html','w',encoding='utf-8').write(s)
print(len(s), len(re.findall(r'href="?https?://',s)))
