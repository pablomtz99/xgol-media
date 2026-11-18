"""Ideas 18 nov: regresión a la media (récord vs diferencial, 2002-2025), jueves vs domingo y matchup IND@HOU."""
import pandas as pd,numpy as np
from scipy.stats import norm,ttest_1samp,ttest_ind,binom,t as tdist
g=pd.read_csv('g2.csv'); rng=np.random.default_rng(11182)
def ols(X,y):
    X=np.column_stack([np.ones(len(X)),X]); b=np.linalg.lstsq(X,y,rcond=None)[0]; r=y-X@b; s2=r@r/(len(y)-X.shape[1]); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X))); return b,se,2*tdist.sf(abs(b/se),len(y)-X.shape[1]),np.sqrt(s2)
pr=lambda b,X:np.column_stack([np.ones(len(X)),X])@b
G=g[(g.game_type=='REG')&g.result.notna()&g.season.between(2002,2025)]
T=pd.concat([G[['season','week','home_team','result']].set_axis(['s','w','t','m'],axis=1),G.assign(m=-G.result)[['season','week','away_team','m']].set_axis(['s','w','t','m'],axis=1)]).sort_values(['s','t','w'])
T['n']=T.groupby(['s','t']).cumcount()+1
rows=[]
for (s,t),a in T.groupby(['s','t']):
    f=a[a.n<=9]; l=a[a.n>9]
    if len(f)<9 or len(l)<6: continue
    rows.append(dict(s=s,t=t,w1=((f.m>0)+.5*(f.m==0)).mean(),d1=f.m.mean(),w2=((l.m>0)+.5*(l.m==0)).mean(),n2=len(l)))
D=pd.DataFrame(rows); D['py']=norm.cdf(D.d1/13.5)
se={k:0 for k in ['media','record','dif','ambos']}
for s in sorted(D.s.unique()):
    tr,te=D[D.s!=s],D[D.s==s]; se['media']+=((te.w2-tr.w2.mean())**2).sum()
    for nm,c in [('record',['w1']),('dif',['d1']),('ambos',['w1','d1'])]:
        b,*_=ols(tr[c].values,tr.w2.values); se[nm]+=((te.w2.values-pr(b,te[c].values))**2).sum()
N=len(D); print('n',N,'RMSE',{k:round((v/N)**.5,4) for k,v in se.items()},'R2oos',{k:round(1-v/se['media'],3) for k,v in se.items()})
b,sb,pb,sig=ols(D[['w1','d1']].values,D.w2.values); print('coef const,w1,d1',b.round(4),'p',pb.round(4),'sigma',round(sig,3))
print('corr w1~w2',round(D.w1.corr(D.w2),3),'d1~w2',round(D.d1.corr(D.w2),3))
D['gap']=D.w1-D.py
for nm,x in [('mejor récord que diferencial (gap>=.15)',D[D.gap>=.15]),('peor (gap<=-.15)',D[D.gap<=-.15])]:
    tt=ttest_1samp(x.w2-x.w1,0); print(nm,'n',len(x),'w1',round(x.w1.mean(),3),'w2',round(x.w2.mean(),3),'dif',round((x.w2-x.w1).mean(),3),'p',tt.pvalue,'bajan/suben %',round((x.w2<x.w1).mean(),3),round((x.w2>x.w1).mean(),3))
Gs=g[(g.season==2026)&(g.game_type=='REG')&g.result.notna()]
A=pd.concat([Gs[['week','home_team','result']].set_axis(['w','t','m'],axis=1),Gs.assign(m=-Gs.result)[['week','away_team','m']].set_axis(['w','t','m'],axis=1)])
S=A.groupby('t').agg(n=('m','size'),W=('m',lambda x:(x>0).sum()),L=('m',lambda x:(x<0).sum()),T=('m',lambda x:(x==0).sum()),d=('m','mean')).reset_index()
S['w1']=(S.W+.5*S['T'])/S.n; S['py']=norm.cdf(S.d/13.5); S['gap']=S.w1-S.py; S['exp']=pr(b,S[['w1','d']].values)
S['rem']=17-S.n; S['lo']=S.exp-1.2816*sig; S['hi']=S.exp+1.2816*sig; S['finW']=S.W+S.exp*S.rem
print(S.sort_values('gap',ascending=False).round(3).to_string())
# Validación: mismo corte, últimos años backtest: error de victorias restantes
# C jueves
H=g[(g.game_type=='REG')&g.result.notna()&g.season.between(2012,2025)&(g.location=='Home')&g.spread_line.notna()].copy()
H['thu']=(H.weekday=='Thursday')&(H.week>1); H['res']=H.result-H.spread_line; sun=H[H.weekday=='Sunday']; thu=H[H.thu]
for nm,x in [('jueves',thu),('domingo',sun)]:
    print(nm,'n',len(x),'local gana',round((x.result>0).mean(),3),'margen',round(x.result.mean(),2),'vs mercado',round(x.res.mean(),2),'total',round(x.total.mean(),1))
print('p margen jue vs dom',round(ttest_ind(thu.result,sun.result,equal_var=False).pvalue,3),'p vs mercado',round(ttest_ind(thu.res,sun.res,equal_var=False).pvalue,3),'p total vs mercado jue',round(ttest_1samp((thu.total-thu.total_line).dropna(),0).pvalue,3))
# IND@HOU matchup
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success','qb_dropback','sack','pass_attempt','air_yards','yards_gained','down','third_down_converted','third_down_failed','qb_hit','week'])
p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
def tb(tm):
    o=p[p.posteam==tm]; d=p[p.defteam==tm]; pa=o[o.play_type=='pass']; ru=o[o.play_type=='run']; dp=d[d.play_type=='pass']; dr=d[d.play_type=='run']
    return dict(off=o.epa.mean(),pass_o=pa.epa.mean(),run_o=ru.epa.mean(),de=d.epa.mean(),pass_d=dp.epa.mean(),run_d=dr.epa.mean(),sr_o=o.success.mean(),sr_d=d.success.mean(),sack_o=o[o.qb_dropback==1].sack.mean(),sack_d=d[d.qb_dropback==1].sack.mean())
Tb=pd.DataFrame({t:tb(t) for t in p.posteam.dropna().unique()}).T
Rk=pd.DataFrame({c:Tb[c].rank(ascending=c in['de','pass_d','run_d','sr_d','sack_o']) for c in Tb.columns}).astype(int)
for t in ['HOU','IND']: print(t,Tb.loc[t].round(3).to_dict()); print(' rk',Rk.loc[t].to_dict())
# pass rush sin Hunter: semanas en que no jugó? por semana sack rate HOU def
d=p[(p.defteam=='HOU')&(p.qb_dropback==1)].groupby('week').agg(db=('sack','size'),sk=('sack','sum'),epa=('epa','mean')).round(3); print(d.to_string())
print('rest',g[(g.season==2026)&(g.week==11)&(g.home_team=='HOU')][['away_rest','home_rest','temp','roof']].to_dict('records'))
