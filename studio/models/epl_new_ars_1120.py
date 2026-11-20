"""Newcastle–Arsenal (Premier League J11, sáb 21 nov 17:30 UK = 11:30 CDMX). Tabla tras J10 (Sky Sports, act. 8 nov; coincide nigfooty 20 nov; Sports Mole: Arsenal 5 pts sobre Brighton).
Modelo xGol Europa v0: fuerza = dif. de goles/(10+K), K=8; Poisson con goles por partido de la liga; localía +0.30 (supuesto). Sin xG (sin fuente).
Prueba: puntos reales vs esperados por goles (Poisson con sus tasas GF/GA por partido) → regresión a la media."""
import numpy as np
from scipy.stats import poisson
T={'Arsenal':(10,9,0,1,15,5,27),'Brighton':(10,7,1,2,26,7,22),'Man City':(10,7,0,3,21,13,21),'Liverpool':(10,5,3,2,14,10,18),'Chelsea':(10,5,1,4,19,16,16),
'Everton':(10,4,4,2,12,10,16),'Bournemouth':(10,4,3,3,16,14,15),'Brentford':(10,3,5,2,16,11,14),'Leeds':(10,3,5,2,10,8,14),'Aston Villa':(10,3,4,3,14,17,13),
'Tottenham':(10,3,3,4,10,11,12),'Newcastle':(10,3,3,4,13,16,12),'Hull':(10,2,5,3,11,11,11),'Ipswich':(10,3,2,5,15,20,11),'Fulham':(10,2,4,4,10,12,10),
'Nottm Forest':(10,2,3,5,9,13,9),'Coventry':(10,3,0,7,10,19,9),'Man Utd':(10,1,5,4,14,19,8),'Sunderland':(10,2,2,6,8,17,8),'Crystal Palace':(10,2,1,7,10,24,7)}
assert all(v[1]*3+v[2]==v[6] and v[1]+v[2]+v[3]==10 for v in T.values())
GFt=sum(v[4] for v in T.values());GAt=sum(v[5] for v in T.values());assert GFt==GAt
MU=2*GFt/200;print('goles/partido',MU)
def match(h,a,K=8,HADV=0.30,N=400000,seed=1120):
    r={k:(v[4]-v[5])/(10+K) for k,v in T.items()};b=2/MU;hh=HADV/MU;d=r[h]-r[a]
    lh=MU/2*np.exp(b*d/2+hh);la=MU/2*np.exp(-b*d/2-hh);rng=np.random.default_rng(seed);x=rng.poisson(lh,N);y=rng.poisson(la,N)
    return lh,la,(x>y).mean(),(x==y).mean(),(x<y).mean(),((x==0)).mean(),((y==0)).mean(),(x+y>=3).mean()
lh,la,pw,pd_,pl,cs_a,cs_n,o3=match('Newcastle','Arsenal')
print(f'NEW-ARS goles esp {lh:.2f}-{la:.2f} | NEW {pw:.3f} E {pd_:.3f} ARS {pl:.3f} | ARS sin recibir {cs_a:.3f} NEW sin recibir {cs_n:.3f} | 3+ goles {o3:.3f}')
for K,H in [(0,.3),(16,.3),(8,0),(8,.5)]:
    r=match('Newcastle','Arsenal',K,H,N=200000,seed=3);print('sens',K,H,'NEW',round(r[2],3),'E',round(r[3],3),'ARS',round(r[4],3))
# incertidumbre del nivel: remuestreo de goles (Poisson) de la temporada
rng=np.random.default_rng(11);B=[]
for i in range(3000):
    gf={k:rng.poisson(v[4]) for k,v in T.items()};ga={k:rng.poisson(v[5]) for k,v in T.items()}
    d=(gf['Newcastle']-ga['Newcastle'])/18-(gf['Arsenal']-ga['Arsenal'])/18;b=2/MU
    l1=MU/2*np.exp(b*d/2+.3/MU);l2=MU/2*np.exp(-b*d/2-.3/MU)
    # P(ARS gana) analítica
    k=np.arange(0,15);px=poisson.pmf(k,l1);py=poisson.pmf(k,l2);M=np.outer(px,py);B.append(np.triu(M,1).sum())
print('ARS 80%',np.percentile(B,[10,90]).round(3))
# regresión a la media: puntos esperados con sus tasas por partido (vs rival promedio)
print('equipo  pts  esperados  80%   P(>=real)')
for t in ['Arsenal','Brighton','Man City','Newcastle','Chelsea']:
    v=T[t];lf,la_=v[4]/10,v[5]/10;rng=np.random.default_rng(5)
    x=rng.poisson(lf,(200000,10));y=rng.poisson(la_,(200000,10));p=(3*(x>y)+(x==y)).sum(1)
    print(t,v[6],round(p.mean(),1),np.percentile(p,[10,90]),'P(>=)',(p>=v[6]).mean().round(3),'P(<=)',(p<=v[6]).mean().round(3))
