"""IND@HOU 19 nov: regresión de récord en cerrados (2002–2025) y modelo v0 con bootstrap. Ejecutar con g2.csv y pbp26.csv.gz de nflverse."""
import pandas as pd,numpy as np
from scipy.stats import norm,pearsonr,ttest_1samp,linregress
g=pd.read_csv('g2.csv');G=g[(g.game_type=='REG')&g.result.notna()]
T=pd.concat([G[['season','week','home_team','result']].set_axis(['s','w','t','m'],axis=1),G.assign(m=-G.result)[['season','week','away_team','m']].set_axis(['s','w','t','m'],axis=1)]).sort_values(['s','t','w'])
T['n']=T.groupby(['s','t']).cumcount()+1
R=[]
for (s,t),a in T[T.s.between(2002,2025)].groupby(['s','t']):
    f,l=a[a.n<=9],a[a.n>9]
    cf=f[f.m.abs()<=8]; cl=l[l.m.abs()<=8]
    if len(cf)>=4 and len(cl)>=3:
        R.append((s,t,len(cf),((cf.m>0)+.5*(cf.m==0)).mean(),len(cl),((cl.m>0)+.5*(cl.m==0)).mean(),f.m.mean(),((l.m>0)+.5*(l.m==0)).mean(),((f.m>0)+.5*(f.m==0)).mean()))
D=pd.DataFrame(R,columns=['s','t','nc1','c1','nc2','c2','d1','w2','w1'])
r,p=pearsonr(D.c1,D.c2);print('close-close n',len(D),'r',round(r,3),'p',p)
lr=linregress(D.c1,D.c2);print('slope',lr.slope,lr.intercept)
bad=D[D.c1<=0.25];print('<=25% close first9 n',len(bad),'c1',bad.c1.mean().round(3),'c2',bad.c2.mean().round(3),'p vs .5',ttest_1samp(bad.c2-.5,0).pvalue,'w1',bad.w1.mean(),'w2',bad.w2.mean())
good=D[D.c1>=0.75];print('>=75% n',len(good),good.c1.mean().round(3),good.c2.mean().round(3))
# diff predicts close? regress c2 on c1 and d1
import numpy.linalg as la
X=np.c_[np.ones(len(D)),D.c1,D.d1];b=la.lstsq(X,D.c2,rcond=None)[0];print('c2 ~ c1 + d1',b)
# HOU / IND 2026
for t in ['HOU','IND']:
    a=T[(T.s==2026)&(T.t==t)];c=a[a.m.abs()<=8]
    print(t,'W-L',(a.m>0).sum(),(a.m<0).sum(),'diff',round(a.m.mean(),2),'close',(c.m>0).sum(),(c.m<0).sum(),'margins',list(a.m))
import pandas as pd,numpy as np
from scipy.stats import norm
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success','qb_dropback','sack','down','third_down_converted','third_down_failed','passer_player_name'])
p=p[p.play_type.isin(['pass','run'])&p.epa.notna()&(p.week<=10)]
print('max week',p.week.max())
nets=lambda q:q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean()
net=nets(p);prob=lambda n:norm.cdf((0.5*(n['HOU']-n['IND'])*61.6+1.5)/13.5)
print('HOU P',round(prob(net),4),'margin',round(0.5*(net['HOU']-net['IND'])*61.6+1.5,2))
rng=np.random.default_rng(1119);gids=p.game_id.unique();B=[]
for i in range(400):
    s=rng.choice(gids,len(gids));q=pd.concat([p[p.game_id==x] for x in s[:0]]) if False else None
gp={k:v for k,v in p.groupby('game_id')}
for i in range(400):
    s=rng.choice(gids,len(gids));q=pd.concat([gp[x] for x in s]);n=nets(q)
    if 'HOU' in n and 'IND' in n: B.append(prob(n))
print('80%',np.percentile(B,[10,90]).round(3))
rk=net.rank(ascending=False).astype(int);print('rk HOU',rk['HOU'],'IND',rk['IND'])
for t in ['HOU','IND']:
    o=p[p.posteam==t];d=p[p.defteam==t]
    db=o[o.qb_dropback==1];dd=d[d.qb_dropback==1]
    print(t,'off',round(o.epa.mean(),3),'def',round(d.epa.mean(),3),'pass_o',round(o[o.play_type=='pass'].epa.mean(),3),'run_o',round(o[o.play_type=='run'].epa.mean(),3),
      'pass_d',round(d[d.play_type=='pass'].epa.mean(),3),'run_d',round(d[d.play_type=='run'].epa.mean(),3),'sr_o',round(o.success.mean(),3),'sack_o',round(db.sack.mean(),3),'sack_d',round(dd.sack.mean(),3))
def rkc(col,asc):
    return col.rank(ascending=asc).astype(int)
pt=p[p.play_type=='pass'];ru=p[p.play_type=='run']
R=pd.DataFrame({'pass_o':rkc(pt.groupby('posteam').epa.mean(),False),'run_o':rkc(ru.groupby('posteam').epa.mean(),False),'pass_d':rkc(pt.groupby('defteam').epa.mean(),True),'run_d':rkc(ru.groupby('defteam').epa.mean(),True),
 'sack_d':rkc(p[p.qb_dropback==1].groupby('defteam').sack.mean(),False),'sack_o':rkc(p[p.qb_dropback==1].groupby('posteam').sack.mean(),True)})
print(R.loc[['HOU','IND']])
n4=nets(p[p.week>=7]);print('last4 P',round(prob(n4),3))
