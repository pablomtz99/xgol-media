"""Chivas–Cruz Azul (J17, dom 22 nov, 17:07 CDMX, Estadio Akron). Tras Tigres 1-0 América (sáb; Noticias MXM, Heraldo, SDP): AME 30 pts, dif. +14 (38-24).
CAZ 32 (37-26, +11), CHV 30 (26-15, +11) (futboltotal/Claro/Record tras J16; Telemundo coincide). Modelo xGol Liga MX v0 (ligamx_j17_1119.py): Poisson, encogimiento K=8, localía +0.35.
Escenarios del 1er lugar: CHV gana → CHV 33 líder; empate → CAZ 33 líder, CHV 31 2°; CAZ gana → CAZ 35 líder, AME 2° (dif. +14 > CHV +11−margen)."""
import numpy as np, io, contextlib, importlib.util, os
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'ligamx_j17_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
T,GD,MU=m.T,m.GD,m.MU
def sim(K=8,HADV=0.35,N=400000,seed=1122):
    r={k:GD[k]/(16+K) for k in T};b=2/MU;h=HADV/MU;d=r['Chivas']-r['Cruz Azul']
    lh=MU/2*np.exp(b*d/2+h);la=MU/2*np.exp(-b*d/2-h);rng=np.random.default_rng(seed);x=rng.poisson(lh,N);y=rng.poisson(la,N);return lh,la,x,y
lh,la,x,y=sim()
pos={}
chv=np.where(x>y,1,np.where(x==y,2,3));caz=np.where(y>=x,1,np.where(32>=31,2,3))
# CAZ si pierde: 32 pts vs AME 30 → CAZ 2°. CHV si pierde: 30, dif 11−margen < AME 14 → 3°
caz=np.where(y>=x,1,2);ame=np.where(y>x,2,3)
print(f'goles esp CHV {lh:.2f} CAZ {la:.2f} | CHV {(x>y).mean():.3f} E {(x==y).mean():.3f} CAZ {(y>x).mean():.3f} | 3+ goles {(x+y>=3).mean():.3f} | 0-0 {((x==0)&(y==0)).mean():.3f}')
for t,p in [('Chivas',chv),('Cruz Azul',caz),('América',ame)]: print(t,'1°',(p==1).mean().round(3),'2°',(p==2).mean().round(3),'3°',(p==3).mean().round(3))
# incertidumbre 80% en P(CAZ líder) por remuestreo de goles de la temporada (Poisson en GF/GA)
rng=np.random.default_rng(22);B=[]
for i in range(3000):
    g1=rng.poisson(26)-rng.poisson(15);g2=rng.poisson(37)-rng.poisson(26);b=2/MU;d=g1/24-g2/24
    l1=MU/2*np.exp(b*d/2+.35/MU);l2=MU/2*np.exp(-b*d/2-.35/MU);from scipy.stats import poisson;k=np.arange(15);M=np.outer(poisson.pmf(k,l1),poisson.pmf(k,l2));B.append(np.triu(M,0).sum())
print('P(CAZ líder) 80%',np.percentile(B,[10,90]).round(3))
for K,H in [(0,.35),(16,.35),(8,0),(8,.6)]:
    a,b_,xx,yy=sim(K,H,N=200000,seed=7);print('sens',K,H,'CHV gana',(xx>yy).mean().round(3),'CAZ líder',(yy>=xx).mean().round(3))
# prueba: puntos reales vs esperados por goles (16 PJ)
for t,(pts,gf,ga) in [('Cruz Azul',(32,37,26)),('Chivas',(30,26,15)),('América',(30,38,24))]:
    n=16 if t!='América' else 17;rng=np.random.default_rng(5);X=rng.poisson(gf/n,(400000,n));Y=rng.poisson(ga/n,(400000,n));p=(3*(X>Y)+(X==Y)).sum(1)
    print(t,n,'pj pts',pts,'esp',p.mean().round(1),np.percentile(p,[10,90]),'P(>=real)',(p>=pts).mean().round(3),'P(<=real)',(p<=pts).mean().round(3))
