"""Resumen vie 20 nov: 9 juegos NBA (probabilidades de studio/models/nba_viernes_1120.py, fijadas en portadas_1120 antes de los partidos).
Resultados: NBA.com (recap Copa NBA 20 nov) y SI scoreboard (coinciden los 9)."""
import numpy as np
from scipy.stats import norm
# (fav, p_fav, margen_est_fav, ganó_fav, margen_real_fav)
G=[("Hawks",.692,7.4,True,111-97),("Pistons",.680,6.9,False,102-105),("Magic",.644,5.4,True,113-111),("Cavaliers",.764,10.6,True,128-119),
("Bulls",.637,5.2,False,94-98),("Thunder",.845,14.9,True,126-120),("Suns",.598,3.7,True,111-101),("Lakers",.841,14.7,True,106-104),("Rockets",.537,1.4,False,124-133)]
p=np.array([g[1] for g in G]);y=np.array([g[3] for g in G]).astype(float)
print('aciertos',int(y.sum()),'esperados',p.sum().round(2),'sorpresas',int(9-y.sum()),'esperadas',(1-p).sum().round(2))
b=((1-p)*y+p*(1-y))**2;print('Brier',b.mean().round(3),'por juego',b.round(3))
# distribución exacta de aciertos (Poisson-binomial)
d=np.array([1.]);
for q in p: d=np.convolve(d,[1-q,q])
print('P(aciertos=k)',d.round(3));print('P(<=6)',d[:7].sum().round(3),'P(=6)',d[6].round(3),'P(>=6)',d[6:].sum().round(3))
# Brier esperado bajo calibración y su distribución (MC)
rng=np.random.default_rng(1121);Y=rng.random((200000,9))<p;B=(((1-p)*Y+p*(1-Y))**2).mean(1)
print('Brier esperado',B.mean().round(3),'80%',np.percentile(B,[10,90]).round(3),'P(B>=obs)',(B>=b.mean()).mean().round(3))
# Spiegelhalter z (noche)
z=((y-p)*(1-2*p)).sum()/np.sqrt(((1-2*p)**2*p*(1-p)).sum());print('Spiegelhalter z',z.round(2),'p',(2*norm.sf(abs(z))).round(3))
# márgenes
e=np.array([g[4]-g[2] for g in G]);print('errores margen',e,'MAE',np.abs(e).mean().round(1),'en sigma',(e/14.7).round(2))
lo=np.array([g[2] for g in G])-1.2816*14.7;hi=np.array([g[2] for g in G])+1.2816*14.7
inn=[(g[4]>=l)&(g[4]<=h) for g,l,h in zip(G,lo,hi)];print('dentro rango 80%',sum(inn),'de 9')
# fuertes vs parejos
s=p>=.7;print('fav >=70%',int(y[s].sum()),'/',s.sum(),'esp',p[s].sum().round(2),'| <70%',int(y[~s].sum()),'/',(~s).sum(),'esp',p[~s].sum().round(2))
