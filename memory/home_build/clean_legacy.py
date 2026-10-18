import re
P='/app/frontend/public/'
for f in ['inscricao','dados-inscricao','confirmacao','inscricao-realizada','pagamento-pix','minhas-inscricoes']:
    t=open(P+f+'.html',encoding='utf-8').read()
    t=re.sub(r'(<style[^>]*>)(.*?)(</style>)',lambda m: m.group(1)+re.sub(r'[^{}]*(?:cebraspe|\.ceb-)[^{}]*\{[^{}]*\}','',m.group(2))+m.group(3),t,flags=re.S)
    t=t.replace(' data-cebraspe-marker="__cebraspe_layout_v1"','').replace(' __cebraspe-applied','')
    open(P+f+'.html','w',encoding='utf-8').write(t)
print('clean ok')
