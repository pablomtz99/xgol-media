import pandas as pd,numpy as np
from scipy.stats import norm
g=pd.read_csv('g2.csv'); s=g[(g.season==2026)&g.home_score.notna()&(g.game_type=='REG')]
def rec(t):
    h=s[s.home_team==t]; a=s[s.away_team==t]
    W=(h.home_score>h.away_score).sum()+(a.away_score>a.home_score).sum(); L=(h.home_score<h.away_score).sum()+(a.away_score<a.home_score).sum()
    T=len(h)+len(a)-W-L; pf=h.home_score.sum()+a.away_score.sum(); pa=h.away_score.sum()+a.home_score.sum()
    return W,L,T,pf/(len(h)+len(a)),pa/(len(h)+len(a))
for t in ['LA','ARI','SEA','LV','SF']: print(t,rec(t))
# H2H and context
for a,b in [('LA','ARI'),('SEA','LV')]:
    hh=g[((g.home_team==a)&(g.away_team==b))|((g.home_team==b)&(g.away_team==a))].tail(6)
    print(hh[['season','week','away_team','away_score','home_team','home_score']].to_string())
# division test 2010-2025
h=g[(g.season.between(2010,2025))&(g.game_type=='REG')&(g.location=='Home')&g.result.notna()&g.spread_line.notna()].copy()
h['fav_home']=h.spread_line>0; h['exp']=h.spread_line.abs(); h['fav_win']=np.where(h.fav_home,h.result>0,h.result<0).astype(int)
h=h[h.result!=0]; h=h[h.exp>0]
h['res']=np.where(h.fav_home,h.result,-h.result)-h.exp
print('n',len(h),'div',h.div_game.sum())

from scipy.optimize import minimize
X=np.column_stack([np.ones(len(h)),h.exp.values,h.div_game.values]); y=h.fav_win.values
nll=lambda b: -(y*(X@b)-np.log1p(np.exp(X@b))).sum()
b=minimize(nll,np.zeros(3),method='BFGS').x; pr=1/(1+np.exp(-X@b)); H=(X*(pr*(1-pr))[:,None]).T@X; se=np.sqrt(np.diag(np.linalg.inv(H)))
print('logit b',b.round(4),'se',se.round(4),'z',(b/se).round(2),'p',(2*norm.sf(abs(b/se))).round(4))
# effect at exp=3,7: 
for e in [3,7]: 
  for d in [0,1]: print('exp',e,'div',d,round(1/(1+np.exp(-(b[0]+b[1]*e+b[2]*d))),3))

for d in [0,1]:
    q=h[h.div_game==d]; print(d,len(q),'favwin',q.fav_win.mean().round(3),'sd res',q.res.std().round(2),'mean res',q.res.mean().round(2), 'abs margin',np.where(q.fav_home,q.result,-q.result).mean().round(2),'exp',q.exp.mean().round(2))
# home field: div vs non div
from scipy.stats import ttest_ind
for d in [0,1]:
    q=h[h.div_game==d]; print('home margin',d,q.result.mean().round(2),'homewin',(q.result>0).mean().round(3))
print(ttest_ind(h[h.div_game==1].res,h[h.div_game==0].res))

# sweep: second meeting
h['pair']=h.apply(lambda r:'-'.join(sorted([r.home_team,r.away_team])),axis=1)
