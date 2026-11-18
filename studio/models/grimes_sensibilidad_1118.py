"""Ideas 18 nov: Grimes (binomial y encogimiento Beta) y sensibilidad de umbrales NFL."""
import pandas as pd,numpy as np
from scipy.stats import binom,binomtest,beta,norm,ttest_1samp
# Grimes
for c in (.366,.371):
    print('c',c,'P>=10/14',binom.sf(9,14,c),'1 en',round(1/binom.sf(9,14,c)),'P>=15/20',binom.sf(14,20,c),'1 en',round(1/binom.sf(14,20,c)))
m,a=round(.434*round(13*7.6)),round(13*7.6); print('temporada aprox',m,a,m/a,'p vs .366',binomtest(m,a,.366).pvalue)
m2,a2=m-15,a-20; print('sin ultimos 2:',m2,a2,round(m2/a2,3),'p',round(binomtest(m2,a2,.366).pvalue,3))
for k in (400,750,1000):
    A=.366*k+m;B=(1-.366)*k+a-m; print('k',k,'post',round(A/(A+B),4),'IC80',beta.ppf([.1,.9],A,B).round(3))
A=.366*750+m;B=.634*750+a-m;pm=A/(A+B)
rng=np.random.default_rng(1118);th=rng.beta(A,B,200000);x=rng.binomial(8,th)
print('esperado triples en 7.6 intentos',round(7.6*pm,2),'P(>=5 de 8)',round((x>=5).mean(),3),'dist 80%',np.percentile(x,[10,90]))
# NFL sensibilidad y exactos
O=pd.read_pickle('O.pkl');h=O[O.season<2026]
print('p exacto debut',ttest_1samp(h[h.new].res,0).pvalue,'n',h.new.sum())
g=pd.read_csv('g2.csv');G=g[(g.game_type=='REG')&g.result.notna()&g.season.between(2002,2025)]
T=pd.concat([G[['season','week','home_team','result']].set_axis(['s','w','t','m'],axis=1),G.assign(m=-G.result)[['season','week','away_team','m']].set_axis(['s','w','t','m'],axis=1)]).sort_values(['s','t','w']);T['n']=T.groupby(['s','t']).cumcount()+1
R=[]
for (s,t),a in T.groupby(['s','t']):
    f,l=a[a.n<=9],a[a.n>9]
    if len(f)==9 and len(l)>=6: R.append((s,t,((f.m>0)+.5*(f.m==0)).mean(),f.m.mean(),((l.m>0)+.5*(l.m==0)).mean()))
D=pd.DataFrame(R,columns=['s','t','w1','d1','w2']);D['gap']=D.w1-norm.cdf(D.d1/13.5)
for c in (.10,.15,.20,.25):
    x=D[D.gap>=c];print('gap>=',c,'n',len(x),round(x.w1.mean(),3),'->',round(x.w2.mean(),3),'bajan',round((x.w2<x.w1).mean(),3),'p',ttest_1samp(x.w2-x.w1,0).pvalue)
x=D[D.gap>=.15];b=[(lambda s:(s.w2<s.w1).mean())(x.sample(len(x),replace=True,random_state=i)) for i in range(2000)];print('bajan IC80',np.percentile(b,[10,90]).round(3))
y=D[(D.w1>=.7)&(D.gap>=.15)];print('7-2 o mejor con gap: n',len(y),round(y.w1.mean(),3),round(y.w2.mean(),3),'bajan',round((y.w2<y.w1).mean(),3))
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['posteam','defteam','play_type','epa']);p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
n=p.groupby('posteam').epa.mean()-p.groupby('defteam').epa.mean();r=n.rank(ascending=False).astype(int);print({t:int(r[t]) for t in ['DEN','TB','HOU','CLE','LV']})
