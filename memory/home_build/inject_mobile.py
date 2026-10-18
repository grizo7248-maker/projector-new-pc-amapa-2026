P='/app/frontend/public/'
TAG='<script src="/cesgranrio/mobile-clean.js?v=3"></script>'
for f in ['inicio','termos','inscricao','dados-inscricao','confirmacao','inscricao-realizada','pagamento-pix','minhas-inscricoes']:
    t=open(P+f+'.html',encoding='utf-8').read()
    if TAG not in t:
        i=t.rfind('</body>'); t=(t[:i]+TAG+t[i:]) if i>=0 else t+TAG
        open(P+f+'.html','w',encoding='utf-8').write(t)
print('injected')
