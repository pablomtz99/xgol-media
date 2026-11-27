"""Resumen jue 26 nov (Thanksgiving + Liga MX cuartos ida): 5 partidos con probabilidad fijada ANTES.
NFL: portadas_1124 idea 1 (nfl_thanksgiving_1124.py): DET 56.1% vs CHI, DAL 69.9% vs PHI, BUF 48.8% (KC 51.2%); 'ganan los 3 favoritos' 20.1%.
Liga MX: ligamx_cuartos_jue_1125.py (portadas_1125 idea 3 y portadas_1126 idea 2): Pachuca–Chivas 44.9/23.9/31.2; León–Cruz Azul 39.4/24.2/36.4.
Resultados (leídos 27 nov): CHI 39-35 DET (ClickOnDetroit, Detroit News); PHI 39-38 DAL (CBS Texas/AP, ESPN); BUF 13-10 KC (Audacy WGR, NBC Sports, Yahoo);
Pachuca 2-1 Chivas (La Silla Rota, 24 Horas, Claro Sports); León 0-4 Cruz Azul (EFE vía Infobae, La Jornada, SI). Ejecutar desde la raíz."""
import numpy as np, io, contextlib, importlib.util
NFL=[("DET","CHI",.561,0),("DAL","PHI",.699,0),("BUF","KC",.488,1)]  # p local, y=1 si gana local
pn=np.array([x[2] for x in NFL]);yn=np.array([x[3] for x in NFL],float)
favn=np.maximum(pn,1-pn);hitn=(pn>.5)==(yn==1)
F=[("Pachuca","Chivas",.449,.239,.312,0),("León","Cruz Azul",.394,.242,.364,2)]
P=np.array([f[2:5] for f in F]);r=np.array([f[5] for f in F]);O=np.eye(3)[r];hitf=P.argmax(1)==r
allp=np.r_[favn,P.max(1)];hits=np.r_[hitn,hitf]
print('aciertos',int(hits.sum()),'de',len(hits),'esperados',allp.sum().round(2))
d=np.array([1.])
for q in allp:d=np.convolve(d,[1-q,q])
print('dist',d.round(3),'P(<=1)',d[:2].sum().round(4))
print('NFL ganan 0 de 3 favoritos',np.prod(1-favn).round(4),'| ganan los 3',np.prod(favn).round(3))
bn=(pn-yn)**2;print('Brier NFL',bn.round(3),bn.mean().round(3),'vs 0.25')
bf=((P-O)**2).sum(1);print('Brier futbol',bf.round(3),bf.mean().round(3),'vs 0.667')
rng=np.random.default_rng(1127);N=400000
Y=(rng.random((N,3))<pn).astype(float);B=((pn-Y)**2).mean(1);print('NFL Brier esperado',B.mean().round(3),'P(>=obs)',(B>=bn.mean()-1e-12).mean().round(3))
U=rng.random((N,2));R=(U[:,:,None]>np.cumsum(P,1)[None,:,:2]).sum(2);BF=((P[None]-np.eye(3)[R])**2).sum(2).mean(1)
print('futbol Brier esperado',BF.mean().round(3),'P(>=obs)',(BF>=bf.mean()-1e-12).mean().round(3))
# Thanksgiving: locales 2010-25 20 de 47 (nfl_thanksgiving_1124) + 2026: 1 de 3
from scipy.stats import binomtest
print('Thanksgiving locales 2010-26',21,'de',50,binomtest(21,50,.555).pvalue.round(3))
# Liguilla vuelta: condicional al resultado de la ida (mismo modelo)
spec=importlib.util.spec_from_file_location('m','studio/models/ligamx_j17_1119.py')
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
MU=m.MU;GF={'Chivas':(27,15),'Cruz Azul':(37,27),'León':(25,22),'Pachuca':(31,20)}
def vuelta(lo,hi,g_lo,g_hi,K=8,HADV=.35,N=400000):
    rr={t:(GF[t][0]-GF[t][1])/(17+K) for t in GF};b=2/MU;h=HADV/MU;dd=rr[hi]-rr[lo]
    y2=rng.poisson(MU/2*np.exp(b*dd/2+h),N);x2=rng.poisson(MU/2*np.exp(-b*dd/2-h),N)
    adv=(g_hi+y2)>=(g_lo+x2);return adv.mean(),((y2-x2)>=1).mean(),((y2-x2)>=2).mean()
a,w1,w2=vuelta('Pachuca','Chivas',2,1);print(f'Chivas avanza tras 1-2 (antes 59.3%) {a:.3f}; gana vuelta por 1+ {w1:.3f}, 2+ {w2:.3f}')
a,w1,w2=vuelta('León','Cruz Azul',0,4);print(f'Cruz Azul avanza tras 4-0 (antes 66.7%) {a:.3f}; León remonta {1-a:.3f}')
