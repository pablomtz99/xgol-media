"""NFL semana 12: Thanksgiving jue 26 nov (CHI@DET 12:00, PHI@DAL 15:30, KC@BUF 19:20 CDMX) + GB@LA mié 25. Modelo NFL v0 (EPA nflverse 2026, sem 1-11).
Validación fuera de muestra: semanas 4-11 (predicción con datos previos a cada semana). Incertidumbre: bootstrap por partido (400).
Ejecutar con SCR=<carpeta con games.csv y pbp.csv.gz>."""
import pandas as pd,numpy as np,os
from scipy.stats import norm,binom
D=os.environ.get('SCR','.');rng=np.random.default_rng(1124)
p=pd.read_csv(f'{D}/pbp.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success','season_type'])
p=p[p.play_type.isin(['pass','run'])&p.epa.notna()&(p.season_type=='REG')]
g=pd.read_csv(f'{D}/games.csv');G=g[(g.season==2026)&(g.game_type=='REG')]
nets=lambda q:q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean()
net=nets(p)
def prob(h,a,n,neu=False):return norm.cdf((0.5*(n[h]-n[a])*61.6+(0 if neu else 1.5))/13.5)
pr=[];o=[]
for w in range(4,12):
    n=nets(p[p.week<w])
    for r in G[(G.week==w)&G.result.notna()].itertuples():
        if r.result==0:continue
        pr.append(prob(r.home_team,r.away_team,n,r.location=='Neutral'));o.append(float(r.result>0))
pr=np.array(pr);o=np.array(o)
print('OOS sem 4-11 n',len(o),'aciertos',((pr>.5)==(o==1)).sum(),'esp',np.maximum(pr,1-pr).sum().round(1),'Brier',((pr-o)**2).mean().round(3),'vs 0.25')
z=((o-pr)*(1-2*pr)).sum()/np.sqrt((((1-2*pr)**2)*pr*(1-pr)).sum());print('Spiegelhalter z',z.round(2),'p',(2*norm.sf(abs(z))).round(2))
gids=p.game_id.unique();grp={k:v for k,v in p.groupby('game_id')};BN=[]
for b in range(400):BN.append(nets(pd.concat([grp[k] for k in rng.choice(gids,len(gids))])))
BN=pd.DataFrame(BN).fillna(0)
GM=[('DET','CHI'),('DAL','PHI'),('BUF','KC'),('LA','GB')];PP=[];PB=[]
for h,a in GM:
    ps=np.array([prob(h,a,BN.iloc[i]) for i in range(400)]);PB.append(ps);PP.append(prob(h,a,net))
    print(f'{a}@{h} P(local) {prob(h,a,net):.3f} 80% {np.percentile(ps,10):.3f}-{np.percentile(ps,90):.3f} margen local {0.5*(net[h]-net[a])*61.6+1.5:+.1f}')
T=pd.DataFrame({'net':net})
for pt in ['pass','run']:
    q=p[p.play_type==pt];T[pt+'_o']=q.groupby('posteam').epa.mean();T[pt+'_d']=q.groupby('defteam').epa.mean()
T['sr_o']=p.groupby('posteam').success.mean();T['sr_d']=p.groupby('defteam').success.mean()
for c in list(T.columns):T[c+'_rk']=T[c].rank(ascending=c.endswith('_d')).astype(int)
s=G[G.result.notna()]
rec={}
for t in net.index:
    hm=s[s.home_team==t];aw=s[s.away_team==t];w=(hm.result>0).sum()+(aw.result<0).sum();l=(hm.result<0).sum()+(aw.result>0).sum();ti=(hm.result==0).sum()+(aw.result==0).sum()
    pf=hm.home_score.sum()+aw.away_score.sum();pa=hm.away_score.sum()+aw.home_score.sum();n=w+l+ti;pe=pf**2.37/(pf**2.37+pa**2.37)
    rec[t]=(w,l,ti,pf,pa,n*pe,binom.cdf(w,n,pe),binom.sf(w-1,n,pe))
for t in ['DET','CHI','DAL','PHI','BUF','KC','LA','GB']:
    w,l,ti,pf,pa,ew,plo,phi=rec[t];print(t,f'{w}-{l}-{ti}',f'pf {pf:.0f} pa {pa:.0f} pitag esp {ew:.1f} P(<=W) {plo:.3f} P(>=W) {phi:.3f}',T.loc[t,['net','net_rk','pass_o_rk','pass_d_rk','run_o_rk','run_d_rk','sr_o_rk','sr_d_rk']].round(3).to_dict())
# compuesta Thanksgiving: 3 favoritos ganan
fav=[max(x,1-x) for x in PP[:3]];print('favoritos',np.round(fav,3),'ganan los 3',np.prod(fav).round(3))
Y=rng.random((200000,3))<np.array(fav);k=Y.sum(1);print('dist # favoritos que ganan',[round((k==i).mean(),3) for i in range(4)])
# con incertidumbre del modelo (bootstrap)
F3=np.prod([PB[i] if PP[i]>.5 else 1-PB[i] for i in range(3)],axis=0);print('P(3 favoritos) 80%',np.percentile(F3,[10,90]).round(3))
# historial: Thanksgiving locales 2010-2025 (games.csv): gameday = 4o jueves nov
h=g[(g.season>=2010)&(g.season<=2025)&(g.game_type=='REG')].copy();h['d']=pd.to_datetime(h.gameday)
tg=h[(h.d.dt.month==11)&(h.d.dt.weekday==3)&(h.d.dt.day>=22)&(h.d.dt.day<=28)]
print('Thanksgiving 2010-25 n',len(tg),'local gana',(tg.result>0).sum(),'empates',(tg.result==0).sum(),'tasa',round((tg.result>0).mean(),3))
oth=h[~h.index.isin(tg.index)&(h.location!='Neutral')];print('resto local gana',round((oth.result>0).mean(),3),'n',len(oth))
from scipy.stats import binomtest;print('binom vs resto p',round(binomtest(int((tg.result>0).sum()),len(tg),(oth.result>0).mean()).pvalue,3))
for t in ['DET','DAL']:
    x=tg[tg.home_team==t];print(t,'en Thanksgiving',(x.result>0).sum(),'-',(x.result<0).sum())
