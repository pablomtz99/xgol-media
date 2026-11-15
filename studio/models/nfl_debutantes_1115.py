import pandas as pd,numpy as np
from scipy.stats import norm, ttest_1samp, binomtest
g=pd.read_csv('g2.csv'); g=g.sort_values(['season','gameday','gametime']).reset_index(drop=True)
seen=set(); rows=[]
for r in g.itertuples():
    for side,qid,qn in [('home',r.home_qb_id,r.home_qb_name),('away',r.away_qb_id,r.away_qb_name)]:
        if pd.isna(qid): continue
        first = qid not in seen
        seen.add(qid)
        if first and 2010<=r.season<=2025 and pd.notna(r.result) and pd.notna(r.spread_line):
            sgn=1 if side=='home' else -1
            exp=sgn*r.spread_line; act=sgn*r.result
            rows.append(dict(season=r.season,qb=qn,team=r.home_team if side=='home' else r.away_team,gtype=r.game_type,exp=exp,act=act,res=act-exp,win=float(act>0) if act!=0 else 0.5,loc=r.location,side=side,div=r.div_game))
d=pd.DataFrame(rows); print(len(d)); print(d.tail(8).to_string())
d=d[d.gtype=='REG']
print('n',len(d),'win',d.win.mean().round(3),'exp margin',d.exp.mean().round(2),'act',d.act.mean().round(2),'res',d.res.mean().round(2), ttest_1samp(d.res,0))
pexp=norm.cdf(d.exp/13.5); print('exp wins',pexp.sum().round(1),'act wins',d.win.sum(), 'exp win%',pexp.mean().round(3))
# away debut
for s in ['home','away']:
    q=d[d.side==s]; print(s,len(q),q.win.mean().round(3),norm.cdf(q.exp/13.5).mean().round(3),q.res.mean().round(2),ttest_1samp(q.res,0).pvalue.round(3))
# debut as home underdog etc; effect size
print('cohen d',(d.res.mean()/d.res.std()).round(3),'sd',d.res.std().round(2))
# compare vs all games residual sd baseline
# bootstrap CI for mean res
rng=np.random.default_rng(0); bs=[rng.choice(d.res.values,len(d)).mean() for _ in range(5000)]; print('CI95',np.percentile(bs,[2.5,97.5]).round(2))
# second starts
d.to_csv('debuts.csv',index=False)
