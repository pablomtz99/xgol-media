"""Modelo xGol Europa v0 (mismo de epl_new_ars_1120.py, generalizado): fuerza = dif. de goles/(PJ+K), K=8; goles Poisson; localía +0.30 (supuesto).
Ideas 27 nov: (1) Arsenal–Man City, PL J12, dom 29 10:30 CDMX; (2) Dortmund–Leverkusen, Bundesliga J11, dom 29 12:30 CDMX.
Tablas: PL tras J11 — ESPN (GF/GC) + NBC Sports 26 nov (G-E-P, DG, Pts coinciden). Bundesliga tras J10 — Sportschau + sozone (idénticas).
xG PL: FotMob (Arsenal 17.6, City 21.9; sin xGA). Sin validación fuera de muestra propia de este modelo en estas ligas (se dice)."""
import numpy as np
from scipy.stats import poisson, norm
PL={'Arsenal':(11,9,1,1,17,7,28),'Brighton':(11,7,1,3,26,9,22),'Man City':(11,7,1,3,22,14,22),'Liverpool':(11,6,3,2,18,10,21),'Bournemouth':(11,5,3,3,18,14,18),
'Brentford':(11,4,5,2,20,11,17),'Leeds':(11,4,5,2,14,9,17),'Chelsea':(11,5,1,5,20,20,16),'Everton':(11,4,4,3,12,14,16),'Tottenham':(11,4,3,4,12,11,15),
'Hull':(11,3,5,3,13,11,14),'Aston Villa':(11,3,5,3,14,17,14),'Newcastle':(11,3,4,4,15,18,13),'Coventry':(11,4,0,7,13,21,12),'Fulham':(11,2,5,4,11,13,11),
'Ipswich':(11,3,2,6,15,22,11),'Nottingham Forest':(11,2,3,6,9,15,9),'Sunderland':(11,2,3,6,8,17,9),'Man Utd':(11,1,5,5,14,23,8),'Crystal Palace':(11,2,1,8,12,27,7)}
BL={'Dortmund':(10,7,3,0,17,7,24),'Bayern':(10,6,4,0,30,10,22),'Freiburg':(10,7,1,2,21,10,22),'Leipzig':(10,7,0,3,32,14,21),'Leverkusen':(10,6,1,3,24,17,19),
'Werder Bremen':(10,5,3,2,21,15,18),'Frankfurt':(10,4,3,3,16,20,15),'Stuttgart':(10,4,1,5,15,15,13),'Elversberg':(10,4,1,5,17,19,13),'Augsburg':(10,3,3,4,23,21,12),
'Hoffenheim':(10,4,0,6,16,18,12),'Hamburgo':(10,4,0,6,10,24,12),'Mainz':(10,3,1,6,19,22,10),'Köln':(10,2,4,4,11,15,10),'Paderborn':(10,2,4,4,8,15,10),
'Schalke':(10,1,4,5,5,11,7),'Union Berlin':(10,1,4,5,8,26,7),'Gladbach':(10,1,1,8,12,26,4)}
for T in (PL,BL):
    assert all(v[1]*3+v[2]==v[6] and sum(v[1:4])==v[0] for v in T.values()); assert sum(v[4] for v in T.values())==sum(v[5] for v in T.values())
def mu(T):n=sum(v[0] for v in T.values())/2;return sum(v[4] for v in T.values())/n
def match(T,h,a,K=8,HADV=.30,N=400000,seed=1127,gf=None,ga=None):
    M=mu(T);r={k:(v[4]-v[5])/(v[0]+K) for k,v in T.items()}
    if gf is not None: r[h]=(gf[0]-ga[0])/(T[h][0]+K); r[a]=(gf[1]-ga[1])/(T[a][0]+K)
    b=2/M;hh=HADV/M;d=r[h]-r[a];lh=M/2*np.exp(b*d/2+hh);la=M/2*np.exp(-b*d/2-hh)
    rng=np.random.default_rng(seed);x=rng.poisson(lh,N);y=rng.poisson(la,N);return lh,la,(x>y).mean(),(x==y).mean(),(x<y).mean(),x,y
def report(T,h,a):
    lh,la,pw,pd_,pl,x,y=match(T,h,a);print(f'\n{h}–{a}: goles esp {lh:.2f}-{la:.2f} | L {pw:.3f} E {pd_:.3f} V {pl:.3f} | 3+ goles {(x+y>=3).mean():.3f} | {h} sin recibir {(y==0).mean():.3f}')
    for K,H in [(0,.3),(16,.3),(8,0),(8,.5)]:
        r=match(T,h,a,K,H,N=100000,seed=3);print('  sens K',K,'loc',H,'L',round(r[2],3),'E',round(r[3],3),'V',round(r[4],3))
    # incertidumbre: remuestreo Poisson de GF/GC de ambos equipos (3000)
    rng=np.random.default_rng(9);W=[];D=[];L=[]
    for i in range(3000):
        gf=(rng.poisson(T[h][4]),rng.poisson(T[a][4]));ga=(rng.poisson(T[h][5]),rng.poisson(T[a][5]))
        r=match(T,h,a,gf=gf,ga=ga,N=20000,seed=i);W.append(r[2]);D.append(r[3]);L.append(r[4])
    print('  80% L',np.percentile(W,[10,90]).round(3),'E',np.percentile(D,[10,90]).round(3),'V',np.percentile(L,[10,90]).round(3))
def pts_vs_goals(T,t,N=400000):
    v=T[t];n=v[0];rng=np.random.default_rng(5);x=rng.poisson(v[4]/n,(N,n));y=rng.poisson(v[5]/n,(N,n));p=(3*(x>y)+(x==y)).sum(1)
    print(f'  {t}: pts {v[6]} | esperados por goles {p.mean():.1f} (80% {np.percentile(p,10):.0f}–{np.percentile(p,90):.0f}) | P(>=real) {(p>=v[6]).mean():.3f}')
    return (p>=v[6]).mean()
print('PL goles/partido',round(mu(PL),3),'| BL',round(mu(BL),3))
report(PL,'Arsenal','Man City')
print('Puntos vs goles PL:');ps=[pts_vs_goals(PL,t) for t in ['Arsenal','Man City','Brighton']]
# Arsenal: goles vs xG (FotMob) — regresión a la media: goles reales ≈ xG → sin sobre-rendimiento ofensivo
print('  ARS goles 17 vs xG 17.6; CITY 22 vs 21.9 → ataque de ambos acorde a ocasiones')
# Defensa de Arsenal: 7 GC en 11 (0.64/p) vs liga
print('  GC por partido ARS',round(7/11,2),'CITY',round(14/11,2),'media liga',round(mu(PL)/2,2))
report(BL,'Dortmund','Leverkusen')
print('Puntos vs goles BL:');ps2=[pts_vs_goals(BL,t) for t in ['Dortmund','Bayern','Leipzig','Freiburg','Leverkusen']]
# ranking por fuerza (DG por partido) vs tabla
r={k:(v[4]-v[5])/(v[0]+8) for k,v in BL.items()};R=sorted(r,key=r.get,reverse=True);print('  ranking fuerza BL',R[:6])
# BH sobre las pruebas de puntos vs goles (PL 3 + BL 5)
allp=sorted(zip(['ARS','MCI','BHA','BVB','FCB','RBL','SCF','B04'],ps+ps2),key=lambda z:z[1])
for i,(t,p) in enumerate(allp,1):print('  BH',t,round(p,3),'umbral',round(.05*i/8,4))
# Dortmund invicto: P(0 derrotas en 10 | nivel por goles)
v=BL['Dortmund'];rng=np.random.default_rng(6);x=rng.poisson(v[4]/10,(400000,10));y=rng.poisson(v[5]/10,(400000,10));print('  BVB P(invicto en 10 | sus goles)',((x<y).sum(1)==0).mean().round(3))
# Descanso: Leverkusen 3 días (Europa League jue) vs BVB 5 → supuesto sensibilidad −0.15 goles a Leverkusen
lh,la,pw,pd_,pl,x,y=match(BL,'Dortmund','Leverkusen');rng=np.random.default_rng(2);y2=rng.poisson(la*0.92,400000);x2=rng.poisson(lh,400000)
print('  sens descanso (Leverkusen −8% goles):','L',(x2>y2).mean().round(3),'E',(x2==y2).mean().round(3),'V',(x2<y2).mean().round(3))
