"""Resumen mar 24 nov: 4 partidos con probabilidad fijada ANTES (portadas_1123 idea 3 UCL martes, commit 2620921; portadas_1124 idea 4 DET@ORL, commit 14fdb31;
no publicadas: sin aprobación). Resultados (leídos 25 nov): Arsenal 1-1 Dortmund, Man City 2-2 Napoli, Real Madrid 5-1 PSV (ESPN recap, ParisFans, AfricaSoccer;
PSV anotó primero); Pistons 104-86 Magic sin Cunningham, baja de último momento (ESPN recap, Washington Post/AP, Yahoo Sports)."""
import numpy as np
from scipy.stats import norm
F=[("Arsenal","Dortmund",.597,.204,.199,1),("Man City","Napoli",.748,.134,.117,1),("Real Madrid","PSV",.681,.169,.149,0)]
B=[("Pistons",.618,True)]
P=np.array([f[2:5] for f in F]);r=np.array([f[5] for f in F]);O=np.eye(3)[r]
hf=(P.argmax(1)==r);pb=np.array([b[1] for b in B]);yb=np.array([b[2] for b in B]).astype(float)
allp=np.r_[P.max(1),pb];hits=np.r_[hf,yb]
print('aciertos',int(hits.sum()),'de 4 esp',allp.sum().round(2))
d=np.array([1.])
for q in allp:d=np.convolve(d,[1-q,q])
print('P(k)',d.round(3),'P(<=2)',d[:3].sum().round(3))
print('3 locales UCL ganan (fijado 30.4%)',np.prod(P[:,0]).round(3),'| P(ARS y MCI ambos empatan)',(P[0,1]*P[1,1]).round(3))
bf=((P-O)**2).sum(1);bb=(pb-yb)**2
print('Brier futbol',bf.round(3),'media',bf.mean().round(3),'uniforme 0.667 | Brier NBA',bb.round(3))
rng=np.random.default_rng(1125);N=200000
U=rng.random((N,3));R=(U[:,:,None]>np.cumsum(P,1)[None,:,:2]).sum(2);Bf=((P[None]-np.eye(3)[R])**2).sum(2).mean(1)
print('Brier futbol esperado',Bf.mean().round(3),'80%',np.percentile(Bf,[10,90]).round(3),'P(>=obs)',(Bf>=bf.mean()).mean().round(3))
Hl=(R==0).sum(1);print('dist locales que ganan',[(Hl==k).mean().round(3) for k in range(4)])
# DET: margen esperado DET +? (nba_det_orl_1124), real +18; sin Cunningham ~54%
print('DET real +18; escenario sin Cunningham 54% (fijado)')
