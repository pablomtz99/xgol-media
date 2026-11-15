import pandas as pd,numpy as np
from scipy.stats import norm, levene
rng=np.random.default_rng(1115)
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success'])
p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
g=pd.read_csv('g2.csv'); G=g[(g.season==2026)&(g.game_type=='REG')]
def nets(q):
    return q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean()
net=nets(p); rk=net.rank(ascending=False).astype(int)
def prob(h,a,n,neutral=False): return norm.cdf((0.5*(n[h]-n[a])*61.6+(0 if neutral else 1.5))/13.5)
# OOS validation weeks 4-9
pr=[];o=[]
for w in range(4,10):
    n=nets(p[p.week<w]); 
    for r in G[(G.week==w)&G.result.notna()].itertuples():
        if r.result==0: continue
        pr.append(prob(r.home_team,r.away_team,n,r.location=='Neutral')); o.append(float(r.result>0))
pr=np.array(pr);o=np.array(o); hits=((pr>.5)==(o==1)).sum(); exph=np.maximum(pr,1-pr).sum()
z=((o-pr)*(1-2*pr)).sum()/np.sqrt((((1-2*pr)**2)*pr*(1-pr)).sum())
print('OOS n',len(o),'hits',hits,'exp',exph.round(1),'brier',((pr-o)**2).mean().round(3),'spieg z',z.round(2),'p',(2*norm.sf(abs(z))).round(2))
# bootstrap
gids=p.game_id.unique(); B=400; boots=[]
grp={k:v for k,v in p.groupby('game_id')}
for b in range(B):
    s=rng.choice(gids,len(gids)); q=pd.concat([grp[k] for k in s]); boots.append(nets(q))
BN=pd.DataFrame(boots).fillna(0)
for a,h in [('LA','ARI'),('SEA','LV')]:
    ps=np.array([prob(h,a,BN.iloc[i]) for i in range(B)])
    print(a,h,'P away',round(1-prob(h,a,net),3),'10-90',np.percentile(1-ps,[10,90]).round(3),'margin',round(0.5*(net[h]-net[a])*61.6+1.5,1))
# metrics
T=pd.DataFrame({'net':net,'rk':rk})
for pt in ['pass','run']:
    q=p[p.play_type==pt]; T[pt+'_o']=q.groupby('posteam').epa.mean(); T[pt+'_d']=q.groupby('defteam').epa.mean()
T['off']=p.groupby('posteam').epa.mean(); T['def']=p.groupby('defteam').epa.mean()
T['ork']=T.off.rank(ascending=False).astype(int); T['drk']=T['def'].rank().astype(int)
T['po_rk']=T.pass_o.rank(ascending=False).astype(int); T['pd_rk']=T.pass_d.rank().astype(int); T['ro_rk']=T.run_o.rank(ascending=False).astype(int); T['rd_rk']=T.run_d.rank().astype(int)
T['sr_o']=p.groupby('posteam').success.mean(); T['sr_d']=p.groupby('defteam').success.mean()
print(T.loc[['LA','ARI','SEA','LV','SF']].round(3).to_string())
# record, pythag, close games, turnovers
s=G[G.result.notna()]
def info(t):
    h=s[s.home_team==t]; a=s[s.away_team==t]
    m=np.concatenate([h.result.values,-a.result.values]); pf=h.home_score.sum()+a.away_score.sum(); pa=h.away_score.sum()+a.home_score.sum()
    pyth=pf**2.37/(pf**2.37+pa**2.37)*len(m)
    close=m[np.abs(m)<=8]
    return dict(W=(m>0).sum(),L=(m<0).sum(),pf=round(pf/len(m),1),pa=round(pa/len(m),1),diff=round(m.mean(),1),pyth=round(pyth,1),closeW=(close>0).sum(),closeL=(close<0).sum(), rest=None)
for t in ['LA','ARI','SEA','LV','SF']: print(t,info(t))
BN.to_pickle('boot.pkl'); net.to_pickle('net.pkl')
