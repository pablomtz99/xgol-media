import sys; sys.path.insert(0,'/home/claude/xgol-media/studio/models')
import numpy as np, pandas as pd
from scipy.stats import norm
import nba_ridge_1103 as M
d=M.load(); b=M.fit(d)
def bootm(games,B=400,seed=7):
    rng=np.random.default_rng(seed); R=[]
    for _ in range(B):
        s=d.iloc[rng.integers(0,len(d),len(d))]; bb=M.fit(s); R.append([M.pred(bb,h,v)['m'] for h,v in games])
    return np.array(R)
R=bootm([('Lakers','Trail Blazers'),('Cavaliers','Knicks')])
for k,(adj,lab) in enumerate([(0,'LAL'),(-2.1,'CLE')]):
    P=norm.cdf((R[:,k]+adj)/M.SIG); print(lab,'P10-90',np.percentile(P,[10,50,90]))
# pre-game probabilities sequence per team
dates=sorted(d.date.unique())
def seq(team):
    out=[]
    for dt in dates:
        te=d[(d.date==dt)&((d.home==team)|(d.visitor==team))]
        if len(te)==0: continue
        tr=d[d.date<dt]
        r=te.iloc[0]
        if len(tr)<20: # use prior only
            pr=M.PRIOR; m=(pr[M.ix[r.home]]-pr[M.ix[r.visitor]]+M.H0)
        else:
            bb=M.fit(tr); m=M.pred(bb,r.home,r.visitor)['m']
        ph=norm.cdf(m/M.SIG); p=ph if r.home==team else 1-ph
        won=(r.hpts>r.vpts)==(r.home==team); mg=(r.hpts-r.vpts)*(1 if r.home==team else -1)
        out.append((dt,r.home==team,p,won,mg))
    return out
for t in ['Trail Blazers','Lakers','Knicks','Cavaliers']:
    s=seq(t); ps=np.array([x[2] for x in s]); w=sum(x[3] for x in s)
    dist=np.array([1.]); 
    for q in ps: dist=np.convolve(dist,[1-q,q])
    mg=np.array([x[4] for x in s])
    print(t,'games',len(s),'wins',w,'exp %.2f'%ps.sum(),'P(>=w) %.3f'%dist[w:].sum(),'avg margin %.1f'%mg.mean(), 'home',[(x[3]) for x in s if x[1]].count(True),'/',sum(1 for x in s if x[1]))
    print('   ', [(str(x[0])[5:],'H' if x[1] else 'A',round(x[2],2),'W' if x[3] else 'L',x[4]) for x in s])
# adjusted ranks, ataque/defensa ranks
T=M.T; a={t:b[M.ix[t]] for t in T}; de={t:b[M.n+M.ix[t]] for t in T}; nt={t:a[t]+de[t] for t in T}
rk=lambda dct,t: sorted(dct,key=lambda x:-dct[x]).index(t)+1
for t in ['Trail Blazers','Lakers','Knicks','Cavaliers']: print(t,'net',round(nt[t],1),rk(nt,t),'att',round(a[t],1),rk(a,t),'def',round(de[t],1),rk(de,t))
# strength of schedule: avg net of opponents
for t in ['Trail Blazers','Lakers','Knicks','Cavaliers']:
    opp=[r.visitor if r.home==t else r.home for r in d.itertuples() if t in (r.home,r.visitor)]
    print(t,'SOS',round(np.mean([nt[o] for o in opp]),2))
# MC LAL-POR
rng=np.random.default_rng(3); p=M.pred(b,'Lakers','Trail Blazers'); sims=rng.normal(p['m'],M.SIG,200000)
print('LAL m',p['m'],'P(|m|<=5)',(abs(sims)<=5).mean(),'tot',p['tot'],p['ph'],p['pv'])
p=M.pred(b,'Cavaliers','Knicks'); print('CLE m',p['m'],p['tot'],p['ph'],p['pv'])
