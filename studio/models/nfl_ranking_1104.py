import pandas as pd, numpy as np
from scipy.stats import norm, pearsonr
p=pd.read_csv('pbp.csv.gz',low_memory=False); p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
gm=p.groupby(['game_id','posteam','defteam']).agg(epa=('epa','mean'),n=('epa','size')).reset_index()
T=sorted(gm.posteam.unique()); ix={t:i for i,t in enumerate(T)}; n=len(T)
X=np.zeros((len(gm),2*n+1)); y=gm.epa.values; w=gm.n.values
for k,r in enumerate(gm.itertuples()): X[k,ix[r.posteam]]=1; X[k,n+ix[r.defteam]]=-1; X[k,-1]=1
import sys
LAMG=float(sys.argv[1]) if len(sys.argv)>1 else 3.0
P=np.eye(2*n+1)*LAMG; P[-1,-1]=0
b=np.linalg.solve(X.T@X+P, X.T@y)
O=b[:n]; D=b[n:2*n]; net=O+D
raw_off=p.groupby('posteam').epa.mean(); raw_def=p.groupby('defteam').epa.mean(); raw=raw_off-raw_def
g=pd.read_csv('games.csv'); s=g[(g.season==2026)&g.home_score.notna()]
rec={}
for t in T:
    h=s[s.home_team==t]; a=s[s.away_team==t]
    W_=(h.home_score>h.away_score).sum()+(a.away_score>a.home_score).sum(); L=(h.home_score<h.away_score).sum()+(a.away_score<a.home_score).sum(); Tt=(h.home_score==h.away_score).sum()+(a.away_score==a.home_score).sum()
    pf=h.home_score.sum()+a.away_score.sum(); pa=h.away_score.sum()+a.home_score.sum(); gp=len(h)+len(a)
    rec[t]=(W_,L,Tt,pf,pa,gp)
df=pd.DataFrame({'t':T,'adj_net':net,'adj_off':O,'adj_def':D,'raw_net':[raw[t] for t in T]})
df['W']=[rec[t][0] for t in T]; df['L']=[rec[t][1] for t in T]; df['T']=[rec[t][2] for t in T]; df['gp']=[rec[t][5] for t in T]
df['pd']=[(rec[t][3]-rec[t][4])/rec[t][5] for t in T]
df['wp']=(df.W+0.5*df['T'])/df.gp
# expected win% from adj net via model v0: per-game margin = net*61.6*? (neutral) -> P = Phi(m/13.5) vs avg team
df['exp_wp']=norm.cdf(df.adj_net*61.6/13.5)
df['exp_W']=df.exp_wp*df.gp
df=df.sort_values('adj_net',ascending=False).reset_index(drop=True); df.index+=1
pd.set_option('display.width',200); print(df.round(3).to_string())
print('corr adj vs raw',pearsonr(df.adj_net,df.raw_net))
# out-of-sample validation: fit wks1-4 adj vs raw -> predict wks5-8 game margins

# out-of-sample: fit weeks 1-5, predict margin sign of weeks 6-8 games using adj vs raw
def fitw(sub,lamg):
    gm2=sub.groupby(['game_id','posteam','defteam']).epa.mean().reset_index()
    X2=np.zeros((len(gm2),2*n+1)); y2=gm2.epa.values
    for k,r in enumerate(gm2.itertuples()): X2[k,ix[r.posteam]]=1; X2[k,n+ix[r.defteam]]=-1; X2[k,-1]=1
    P2=np.eye(2*n+1)*lamg; P2[-1,-1]=0; bb=np.linalg.solve(X2.T@X2+P2,X2.T@y2); return bb[:n]+bb[n:2*n]
tr=p[p.week<=5]; te=s[(s.week>=6)&(s.week<=8)]
ro=tr.groupby('posteam').epa.mean()-tr.groupby('defteam').epa.mean()
for lab,nets in [('raw',{t:ro[t] for t in T}),('adj',dict(zip(T,fitw(tr,LAMG))))]:
    pr=[];o=[]
    for r in te.itertuples():
        m=0.5*(nets[r.home_team]-nets[r.away_team])*61.6+1.5; pr.append(norm.cdf(m/13.5)); o.append(float(r.home_score>r.away_score))
    pr=np.array(pr);o=np.array(o); print(lab,'n',len(o),'brier',round(((pr-o)**2).mean(),4),'hits',round(((pr>.5)==(o==1)).mean(),3))
