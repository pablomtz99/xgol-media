"""Atalanta–Inter (Serie A J12, dom 22 nov, 20:45 CET = 13:45 CDMX, Bergamo). Tabla tras J11: vavel (act. 8 nov; puntos coinciden con TMW 9 nov y fantacalcio).
Modelo xGol Europa v0 (igual que epl_new_ars_1120.py): fuerza = dif. de goles/(11+K), K=8; Poisson; localía +0.30 (supuesto). Sin xG verificado.
Prueba: puntos reales vs esperados por goles (Poisson con tasas GF/GA por partido)."""
import numpy as np
from scipy.stats import poisson
T={'Lazio':(11,9,2,0,25,9,29),'Inter':(11,9,1,1,28,13,28),'Roma':(11,8,3,0,31,10,27),'Milan':(11,7,3,1,23,13,24),'Como':(11,7,2,2,18,10,23),
'Frosinone':(11,6,2,3,24,15,20),'Juventus':(11,5,3,3,15,12,18),'Bologna':(11,5,2,4,16,14,17),'Cagliari':(11,5,1,5,10,15,16),'Napoli':(11,4,3,4,18,14,15),
'Torino':(11,4,2,5,15,17,14),'Atalanta':(11,4,2,5,17,20,14),'Genoa':(11,4,1,6,11,16,13),'Lecce':(11,3,1,7,12,22,10),'Fiorentina':(11,2,3,6,17,25,9),
'Parma':(11,2,2,7,9,17,8),'Sassuolo':(11,2,2,7,16,29,8),'Monza':(11,2,1,8,17,25,7),'Venezia':(11,2,0,9,8,21,6),'Udinese':(11,1,2,8,12,25,5)}
assert all(v[1]*3+v[2]==v[6] and v[1]+v[2]+v[3]==11 for v in T.values())
assert sum(v[4] for v in T.values())==sum(v[5] for v in T.values())
MU=2*sum(v[4] for v in T.values())/220;print('goles/partido',round(MU,3))
def match(h,a,K=8,HADV=0.30,N=400000,seed=1121):
    r={k:(v[4]-v[5])/(11+K) for k,v in T.items()};b=2/MU;hh=HADV/MU;d=r[h]-r[a]
    lh=MU/2*np.exp(b*d/2+hh);la=MU/2*np.exp(-b*d/2-hh);rng=np.random.default_rng(seed);x=rng.poisson(lh,N);y=rng.poisson(la,N)
    return lh,la,(x>y).mean(),(x==y).mean(),(x<y).mean(),(x==0).mean(),(y==0).mean(),(x+y>=3).mean()
lh,la,pw,pd_,pl,csi,csa,o3=match('Atalanta','Inter')
print(f'ATA-INT goles esp {lh:.2f}-{la:.2f} | ATA {pw:.3f} E {pd_:.3f} INT {pl:.3f} | INT sin recibir {csi:.3f} ATA sin recibir {csa:.3f} | 3+ goles {o3:.3f}')
for K,H in [(0,.3),(16,.3),(8,0),(8,.5)]:
    r=match('Atalanta','Inter',K,H,N=200000,seed=3);print('sens',K,H,'ATA',round(r[2],3),'E',round(r[3],3),'INT',round(r[4],3))
rng=np.random.default_rng(11);B=[]
for i in range(3000):
    gf={k:rng.poisson(v[4]) for k,v in T.items()};ga={k:rng.poisson(v[5]) for k,v in T.items()}
    d=(gf['Atalanta']-ga['Atalanta'])/19-(gf['Inter']-ga['Inter'])/19;b=2/MU
    l1=MU/2*np.exp(b*d/2+.3/MU);l2=MU/2*np.exp(-b*d/2-.3/MU);k=np.arange(0,15);M=np.outer(poisson.pmf(k,l1),poisson.pmf(k,l2));B.append(np.triu(M,1).sum())
print('INT 80%',np.percentile(B,[10,90]).round(3))
print('equipo pts esperados 80% P(>=real) P(<=real)')
for t in ['Lazio','Inter','Roma','Atalanta','Napoli','Juventus','Frosinone','Cagliari']:
    v=T[t];rng=np.random.default_rng(5);x=rng.poisson(v[4]/11,(200000,11));y=rng.poisson(v[5]/11,(200000,11));p=(3*(x>y)+(x==y)).sum(1)
    print(t,v[6],round(p.mean(),1),np.percentile(p,[10,90]),(p>=v[6]).mean().round(3),(p<=v[6]).mean().round(3))
# ranking por diferencia de goles
gd=sorted(T,key=lambda t:T[t][4]-T[t][5],reverse=True);print('rank dif goles',[(t,T[t][4]-T[t][5]) for t in gd[:6]],'Atalanta',gd.index('Atalanta')+1)
