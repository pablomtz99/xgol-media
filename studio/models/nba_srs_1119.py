"""Modelo NBA v1 (versión SRS, 19 nov): calidad = promedio ponderado entre SRS 2026-27 (margen ajustado por rival; Basketball-Reference, 19 nov)
y prior = 90% del nivel 2025-26 ((V-41)/2.7). Peso del prior = 16 partidos (igual a λ del ridge v1). Local +2.0; σ = 14.7."""
import numpy as np
from scipy.stats import norm, pearsonr, spearmanr
W25={"Hawks":46,"Celtics":56,"Nets":20,"Hornets":44,"Bulls":31,"Cavaliers":52,"Mavericks":26,"Nuggets":54,"Pistons":60,"Warriors":37,"Rockets":52,"Pacers":19,"Clippers":42,"Lakers":53,"Grizzlies":25,"Heat":43,"Bucks":32,"Timberwolves":49,"Pelicans":26,"Knicks":53,"Thunder":64,"Magic":45,"76ers":45,"Suns":45,"Trail Blazers":42,"Kings":22,"Spurs":62,"Raptors":46,"Jazz":22,"Wizards":17}
S={ # W,L,MOV,SOS,SRS
"Spurs":(12,3,11.20,0.57,11.77),"Celtics":(11,4,10.47,-2.94,7.53),"Timberwolves":(11,4,10.60,0.40,11.00),"Rockets":(12,4,8.69,0.94,9.62),"Grizzlies":(11,4,9.00,-3.00,6.00),
"Pistons":(10,4,6.43,-1.96,4.47),"Knicks":(8,6,6.14,-2.06,4.09),"Lakers":(13,3,6.44,-1.53,4.90),"Trail Blazers":(9,5,6.00,2.84,8.84),"Thunder":(9,6,4.40,1.39,5.79),
"76ers":(13,3,2.94,-2.10,0.83),"Cavaliers":(8,8,1.94,-0.59,1.34),"Hawks":(9,6,1.93,-2.78,-0.84),"Nuggets":(8,5,0.92,1.07,2.00),"Warriors":(8,7,0.87,1.93,2.79),
"Heat":(9,6,0.67,-0.52,0.14),"Raptors":(5,10,0.00,-0.54,-0.54),"Mavericks":(8,7,-0.87,2.56,1.69),"Suns":(7,7,-1.64,2.01,0.36),"Pacers":(5,10,-3.27,-1.43,-4.69),
"Magic":(6,8,-3.43,-0.12,-3.55),"Clippers":(4,9,-5.77,0.19,-5.58),"Wizards":(5,11,-7.19,-1.34,-8.53),"Pelicans":(5,11,-7.44,0.07,-7.37),"Jazz":(3,13,-7.25,4.04,-3.22),
"Bulls":(4,10,-8.36,1.25,-7.11),"Nets":(3,11,-8.36,-1.58,-9.93),"Hornets":(4,10,-10.29,-1.38,-11.66),"Bucks":(1,14,-13.13,1.45,-11.69),"Kings":(1,13,-14.00,3.55,-10.46)}
K,H,SIG=16,2.0,14.7
Q={t:((v[0]+v[1])*v[4]+K*0.9*(W25[t]-41)/2.7)/(v[0]+v[1]+K) for t,v in S.items()}
R=sorted(Q,key=Q.get,reverse=True); rk={t:i+1 for i,t in enumerate(R)}
rec=sorted(S,key=lambda t:(S[t][0]/(S[t][0]+S[t][1])),reverse=True); rrk={t:i+1 for i,t in enumerate(rec)}
for t in R: print(f"{rk[t]:2d} {t:14s} {S[t][0]}-{S[t][1]} rec#{rrk[t]:2d} SRS {S[t][4]:6.2f} SOS {S[t][3]:5.2f} Q {Q[t]:6.2f}")
def P(h,a):
    m=Q[h]-Q[a]+H; return norm.cdf(m/SIG),m
# incertidumbre: error típico de SRS ~ sigma/sqrt(n) por equipo
def PI(h,a,N=200000,seed=1):
    rng=np.random.default_rng(seed);n1=sum(S[h][:2]);n2=sum(S[a][:2])
    se1=SIG/np.sqrt(n1+K)*1.0; se2=SIG/np.sqrt(n2+K)  # error del nivel estimado (aprox.)
    q1=rng.normal(Q[h],se1,N);q2=rng.normal(Q[a],se2,N); p=norm.cdf((q1-q2+H)/SIG); return np.percentile(p,[10,90])
for h,a in [("Grizzlies","Warriors"),("Spurs","Clippers"),("Timberwolves","Knicks"),("Bucks","Trail Blazers")]:
    p,m=P(h,a);print(h,'vs',a,'P local',round(p,3),'margen',round(m,2),'80%',PI(h,a).round(3))
# 76ers: record vs quality
v=S["76ers"];print('76ers pyth14',round(13+3,0), 'exp win% from MOV (Φ(MOV/σ·?))')
# expected wins given SRS per game ~ Φ(SRS-adjusted margin/σ) vs avg opponent, home/away split 8/8
for t in ["76ers","Trail Blazers","Bucks","Lakers"]:
    n=sum(S[t][:2]); pg=norm.cdf(S[t][2]/SIG); ew=n*pg
    # P(W >= actual | per-game pg) binomial
    from scipy.stats import binom
    print(t,'n',n,'exp wins by MOV',round(ew,2),'actual',S[t][0],'P(>=actual)',round(binom.sf(S[t][0]-1,n,pg),4),'P(<=actual)',round(binom.cdf(S[t][0],n,pg),4))
# corr record vs SRS
wp=[S[t][0]/(S[t][0]+S[t][1]) for t in S]; srs=[S[t][4] for t in S]; print('r record-SRS',pearsonr(wp,srs))
# Bucks: P(lose tonight) and Monte Carlo rest of season (82 games, avg opponent, half home)
p,m=P("Bucks","Trail Blazers");print('Bucks gana hoy',round(p,3))
rng=np.random.default_rng(1119);N=100000;rem=82-15
qb=rng.normal(Q["Bucks"],SIG/np.sqrt(15+K),N)
home=np.r_[np.ones(rem//2+1),np.zeros(rem-rem//2-1)]
pw=norm.cdf((qb[:,None]+np.where(home==1,H,-H)[None,:])/SIG)
w=1+(rng.random((N,rem))<pw).sum(1); print('Bucks final wins mean',w.mean().round(1),'80%',np.percentile(w,[10,90]),'P(<=9)',(w<=9).mean().round(3),'P(<=15)',(w<=15).mean().round(3),'P(>=30)',(w>=30).mean().round(3))
