"""NBA lun 23 nov: SAS@SAC (19:00 PT = 21:00 CDMX). Modelo NBA v1 (SRS B-Ref hasta 18 nov; nba_srs_1119.py). Récords hoy: SAS 14-3, SAC 2-14 (landofbasketball);
MOV hoy (TeamRankings): SAS +11.9 (1°), SAC −12.3 (29°). Bajas (Sportbusy): Wembanyama y Fox día a día; Dylan Harper y Tobias Harris fuera.
Ninguno en back-to-back (no jugaron el domingo 22 según calendario nba.com)."""
import numpy as np, io, contextlib, importlib.util, os
from scipy.stats import norm, binom
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nba_srs_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S,Q,K,H,SIG,rk,W25=m.S,m.Q,m.K,m.H,m.SIG,m.rk,m.W25
h,a='Kings','Spurs';mg=Q[h]-Q[a]+H
rng=np.random.default_rng(1123);N=200000
qh=rng.normal(Q[h],SIG/np.sqrt(sum(S[h][:2])+K),N);qa=rng.normal(Q[a],SIG/np.sqrt(sum(S[a][:2])+K),N);pp=norm.cdf((qa-qh-H)/SIG)
print(f'P(SAS) {norm.cdf(-mg/SIG):.3f} 80% {np.percentile(pp,10):.3f}-{np.percentile(pp,90):.3f} margen SAS {-mg:+.1f} | Q SAS {Q[a]:.2f} ({rk[a]}) SAC {Q[h]:.2f} ({rk[h]})')
print('S',S[a],S[h],'W25',W25[a],W25[h])
for adj,lab in [(-3,'sin Wembanyama aprox −3'),(-5,'sin Wembanyama y Fox aprox −5')]:
    print(lab,'P(SAS)',round(norm.cdf((-mg+adj)/SIG),3))
# margen > 10 / >20
print('P(SAS por 10+)',round(norm.sf((10+mg)/SIG),3),'P(por 20+)',round(norm.sf((20+mg)/SIG),3))
# Kings: 2-14 con MOV −12.3: victorias esperadas
for t,w,l,mov in [('Kings',2,14,-12.3),('Spurs',14,3,11.9)]:
    n=w+l;pg=norm.cdf(mov/SIG);print(t,'esp',round(n*pg,1),'P(<=W)',round(binom.cdf(w,n,pg),3),'P(>=W)',round(binom.sf(w-1,n,pg),3))
# diferencia de calidad entre ambos vs distribución de diferencias en la liga (¿partido más desigual?)
qs=np.array(list(Q.values()));d=np.abs(qs[:,None]-qs[None,:]);print('dif Q SAS-SAC',round(Q[a]-Q[h],1),'percentil entre todos los pares',round((d[np.triu_indices(30,1)]<abs(Q[a]-Q[h])).mean()*100,1))
# Spurs regresión: SRS hoy vs prior
print('Spurs prior',round(0.9*(W25[a]-41)/2.7,2),'SRS',S[a][4],'| Kings prior',round(0.9*(W25[h]-41)/2.7,2),'SRS',S[h][4])
