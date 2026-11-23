"""Resumen dom 22 nov: 9 partidos con probabilidades fijadas ANTES (portadas_1121 ideas 1-3, commit ee90b02; portadas_1122 ideas 1, 3, 4, commit ca3e0b7;
no publicados por falta de aprobación).
Resultados (leídos en páginas, 22-23 nov): Chivas 1-0 Cruz Azul (Claro Sports, Noroeste); Atalanta 4-4 Inter (LaPresse, DAZN); Hull 2-0 Brighton (Sky Sports, ESPN);
Heat 123-113 Thunder, sin Gilgeous-Alexander (ESPN, Daily Thunder); Warriors 88-87 Celtics (NBA.com, ESPN); Bears 21-13 Saints (ESPN, CBS);
Broncos 38-24 Raiders (Denver Gazette, ESPN); Lions 31-21 Buccaneers (detroitlions.com, buccaneers.com); Eagles 19-16 Steelers (SI, ESPN)."""
import numpy as np
from scipy.stats import norm
# Futbol 3 resultados: (local, visita, pL, pE, pV, idx resultado)
F=[("Chivas","Cruz Azul",.457,.238,.305,0),("Atalanta","Inter",.250,.223,.527,1),("Hull","Brighton",.215,.231,.554,0)]
# Binarios: (favorito, p_fav, ganó_fav)
B=[("Bears",.663,True),("Broncos",.636,True),("Lions",.566,True),("Steelers",.622,False),("Thunder",.616,False),("Celtics",.540,False)]
P=np.array([f[2:5] for f in F]);r=np.array([f[5] for f in F]);O=np.eye(3)[r]
hf=(P.argmax(1)==r);pb=np.array([b[1] for b in B]);yb=np.array([b[2] for b in B]).astype(float)
pf=P.max(1);allp=np.r_[pf,pb];hits=np.r_[hf,yb]
print('futbol aciertos',hf.sum(),'esp',pf.sum().round(2),'| binarios',int(yb.sum()),'esp',pb.sum().round(2),'| total',int(hits.sum()),'de 9 esp',allp.sum().round(2))
d=np.array([1.])
for q in allp: d=np.convolve(d,[1-q,q])
print('P(k aciertos)',d.round(3),'P(<=4)',d[:5].sum().round(3))
bf=((P-O)**2).sum(1);bb=(pb-yb)**2
print('Brier futbol 3res',bf.round(3),'media',bf.mean().round(3),'(uniforme 0.667) | Brier binario',bb.round(3),'media',bb.mean().round(3),'(50/50 = 0.25)')
print('prob dada al resultado real futbol',P[np.arange(3),r].round(3),'binarios',np.where(yb==1,pb,1-pb).round(3))
rng=np.random.default_rng(1123);N=200000
Yb=rng.random((N,6))<pb;Bb=((pb-Yb)**2).mean(1)
print('Brier binario esperado',Bb.mean().round(3),'80%',np.percentile(Bb,[10,90]).round(3),'P(>=obs)',(Bb>=bb.mean()).mean().round(3))
U=rng.random((N,3));R=(U[:,:,None]>np.cumsum(P,1)[None]).sum(2);Bf=((P[None]-np.eye(3)[R])**2).sum(2).mean(1)
print('Brier futbol esperado',Bf.mean().round(3),'80%',np.percentile(Bf,[10,90]).round(3),'P(>=obs)',(Bf>=bf.mean()).mean().round(3))
z=((yb-pb)*(1-2*pb)).sum()/np.sqrt(((1-2*pb)**2*pb*(1-pb)).sum());print('Spiegelhalter binarios z',z.round(2),'p',(2*norm.sf(abs(z))).round(3))
# NFL vs NBA
print('NFL 3 de 4 esp',pb[:4].sum().round(2),'| NBA 0 de 2 esp',pb[4:].sum().round(2),'P(0 de 2)',np.prod(1-pb[4:]).round(3))
# Liderato Liga MX: CAZ líder 54.3% → Chivas líder (45.7%)
# Acumulado de resúmenes recientes (20 nov NBA 6/9 esp ver resumen_1121; 21 nov 0/3 esp 1.41; hoy)
