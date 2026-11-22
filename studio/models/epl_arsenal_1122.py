"""Premier League tras J11 (parcial): ¿Arsenal (28 pts, 17-7) es tan superior como dice la tabla? Brighton 22 pts en 10 PJ (26-7) juega hoy en Hull (14:00 UK = 8:00 CDMX).
Tabla J10: Sky Sports (8 nov) en epl_new_ars_1120.py; J11: Newcastle 2-2 Arsenal (ESPN UK; Eze 33', Barnes 49', Thiaw 62', Madueke 78'). ESPN UK: Arsenal 28 (11, +10), Brighton 22 (10, +19), Man City 22 (11, +8).
Prueba: puntos reales vs esperados por goles (Poisson con tasas GF/GA por partido de cada equipo). Modelo xGol Europa v0 para Hull–Brighton."""
import numpy as np, io, contextlib, importlib.util, os
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'epl_new_ars_1120.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
T=dict(m.T)
T['Arsenal']=(11,9,1,1,17,7,28);T['Newcastle']=(11,3,4,4,15,18,13);T['Man City']=(11,7,1,3,22,14,22)
lh,la,pw,pd_,pl,*_=m.match('Hull','Brighton');print(f'Hull–Brighton goles esp {lh:.2f}-{la:.2f} | HUL {pw:.3f} E {pd_:.3f} BHA {pl:.3f}')
for K,H in [(0,.3),(16,.3),(8,0),(8,.5)]:
    r=m.match('Hull','Brighton',K,H,N=200000,seed=3);print('sens',K,H,'HUL',round(r[2],3),'E',round(r[3],3),'BHA',round(r[4],3))
print('equipo pj pts esp 80% P(>=real)')
res={}
for t in ['Arsenal','Brighton','Man City','Liverpool','Chelsea']:
    v=T[t];n=v[0];rng=np.random.default_rng(5);x=rng.poisson(v[4]/n,(400000,n));y=rng.poisson(v[5]/n,(400000,n));p=(3*(x>y)+(x==y)).sum(1)
    res[t]=p;print(t,n,v[6],round(p.mean(),1),np.percentile(p,[10,90]),(p>=v[6]).mean().round(3),'ppg real',round(v[6]/n,2),'ppg esp',round(p.mean()/n,2))
# misma comparación por partido: Arsenal vs Brighton en puntos por partido esperados
print('dif goles por partido ARS',round(10/11,2),'BHA',round(19/10,2))
# Benjamini-Hochberg sobre 5 pruebas (unilateral P(>=real))
ps={t:(res[t]>=T[t][6]).mean() for t in res};o=sorted(ps.items(),key=lambda z:z[1]);mm=len(o)
for i,(t,p) in enumerate(o,1): print('BH',t,round(p,3),'umbral',round(0.05*i/mm,3))
