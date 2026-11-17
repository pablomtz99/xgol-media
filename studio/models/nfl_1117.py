"""Cálculos 17 nov (NFL tras semana 10 completa, incl. LAC@BAL). Ejecutar en carpeta con g2.csv y pbp26.csv.gz (nflverse)."""
import pandas as pd,numpy as np
from scipy.stats import norm
rng=np.random.default_rng(1117)
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success','yards_gained','qtr'])
p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
g=pd.read_csv('g2.csv'); G=g[(g.season==2026)&(g.game_type=='REG')]
nets=lambda q:q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean()
prob=lambda h,a,n,neu=False: norm.cdf((0.5*(n[h]-n[a])*61.6+(0 if neu else 1.5))/13.5)
pr=[];o=[];wk=[]
for w in range(4,11):
    n=nets(p[p.week<w])
    for r in G[(G.week==w)&G.result.notna()].itertuples():
        if r.result==0: continue
        pr.append(prob(r.home_team,r.away_team,n,r.location=='Neutral')); o.append(float(r.result>0)); wk.append(w)
pr=np.array(pr);o=np.array(o); fav=np.maximum(pr,1-pr); hit=((pr>.5)==(o==1))
z=((o-pr)*(1-2*pr)).sum()/np.sqrt((((1-2*pr)**2)*pr*(1-pr)).sum())
br=(pr-o)**2
bb=[br[rng.integers(0,len(br),len(br))].mean() for _ in range(4000)]
print('OOS n',len(o),'hits',hit.sum(),'exp',fav.sum().round(1),'brier',br.mean().round(3),np.percentile(bb,[10,90]).round(3),'spieg p',(2*norm.sf(abs(z))).round(2))
for lo,hi in [(.5,.6),(.6,.7),(.7,1)]:
    m=(fav>=lo)&(fav<hi); print(' band',lo,hi,m.sum(),'hits',hit[m].sum(),'exp',fav[m].sum().round(1),'said',fav[m].mean().round(3),'happened',hit[m].mean().round(3))
# upsets: favorites >=70% that lost
print('70%+ favs lost:',(~hit[fav>=.7]).sum(),'of',(fav>=.7).sum())
# LAC@BAL game stats
q=p[p.game_id=='2026_10_LAC_BAL']
for t in ['LAC','BAL']:
    a=q[q.posteam==t]; print(t,'plays',len(a),'epa/play',a.epa.mean().round(3),'success',a.success.mean().round(3),
      'pass epa',a[a.play_type=='pass'].epa.mean().round(3),'run epa',a[a.play_type=='run'].epa.mean().round(3),'run yds',a[a.play_type=='run'].yards_gained.sum())
n9=nets(p[p.week<10]); print('pre BAL p',round(prob('BAL','LAC',n9),3),'margin',round(0.5*(n9['BAL']-n9['LAC'])*61.6+1.5,1))
n5=nets(p[(p.week>=6)&(p.week<10)]); print('pre BAL last-month p',round(prob('BAL','LAC',n5),3))
# full net through wk10
net=nets(p); net.to_pickle('net10.pkl'); rk=net.rank(ascending=False).astype(int)
print('rank top12', rk.sort_values().head(12).to_dict()); print('LAC',rk['LAC'],'BAL',rk['BAL'])
gids=p.game_id.unique(); grp={k:v for k,v in p.groupby('game_id')}; B=400; boots=[]
for b in range(B):
    s=rng.choice(gids,len(gids)); boots.append(nets(pd.concat([grp[k] for k in s])))
BN=pd.DataFrame(boots).fillna(0); BN.to_pickle('boot10b.pkl')
for r in G[G.week==11].itertuples():
    neu=r.location=='Neutral'; ps=np.array([prob(r.home_team,r.away_team,BN.iloc[i],neu) for i in range(B)])
    print('W11',r.away_team,'@',r.home_team,'neu' if neu else '','P home',round(prob(r.home_team,r.away_team,net,neu),3),np.percentile(ps,[10,90]).round(3),'margin',round(0.5*(net[r.home_team]-net[r.away_team])*61.6+(0 if neu else 1.5),1))
