"""Ideas 17 nov (semana 11). Ejecutar en carpeta con g2.csv, pbp26.csv.gz y boot10b.pkl/net10.pkl (de nfl_1117.py)."""
import pandas as pd,numpy as np
from scipy.stats import norm, ttest_1samp, pearsonr, chisquare
rng=np.random.default_rng(11171)
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success','pass_oe','qb_dropback','sack','yards_gained','down','third_down_converted','third_down_failed'])
p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
g=pd.read_csv('g2.csv'); G=g[(g.season==2026)&(g.game_type=='REG')]; s=G[G.result.notna()]
net=pd.read_pickle('net10.pkl'); BN=pd.read_pickle('boot10b.pkl'); rk=net.rank(ascending=False).astype(int)
nets=lambda q:q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean()
prob=lambda h,a,n,neu=False: norm.cdf((0.5*(n[h]-n[a])*61.6+(0 if neu else 1.5))/13.5)
T=pd.DataFrame({'net':net,'rk':rk})
T['off']=p.groupby('posteam').epa.mean(); T['def']=p.groupby('defteam').epa.mean()
for pt in ['pass','run']:
    q=p[p.play_type==pt]; T[pt+'_o']=q.groupby('posteam').epa.mean(); T[pt+'_d']=q.groupby('defteam').epa.mean()
for c in ['off','pass_o','run_o']: T[c+'_rk']=T[c].rank(ascending=False).astype(int)
for c in ['def','pass_d','run_d']: T[c+'_rk']=T[c].rank().astype(int)
T['sr_o']=p.groupby('posteam').success.mean(); T['sr_d']=p.groupby('defteam').success.mean()
db=p[p.qb_dropback==1]; T['sack_o']=db.groupby('posteam').sack.mean(); T['sack_d']=db.groupby('defteam').sack.mean()
T['sack_d_rk']=T.sack_d.rank(ascending=False).astype(int); T['sack_o_rk']=T.sack_o.rank().astype(int)
t3=p[p.down==3]; T['3rd_o']=t3.groupby('posteam').third_down_converted.sum()/(t3.groupby('posteam').third_down_converted.sum()+t3.groupby('posteam').third_down_failed.sum())
def info(t):
    h=s[s.home_team==t]; a=s[s.away_team==t]
    m=np.concatenate([h.result.values,-a.result.values]); pf=h.home_score.sum()+a.away_score.sum(); pa=h.away_score.sum()+a.home_score.sum()
    close=m[np.abs(m)<=8]
    return dict(W=int((m>0).sum()),L=int((m<0).sum()),T=int((m==0).sum()),pf=round(pf/len(m),1),pa=round(pa/len(m),1),diff=round(m.mean(),1),pyth=round(pf**2.37/(pf**2.37+pa**2.37)*len(m),1),closeW=int((close>0).sum()),closeL=int((close<0).sum()))
pd.set_option('display.width',250)
for t in ['MIN','SF','IND','HOU']: print(t,info(t))
print(T.loc[['MIN','SF','IND','HOU']].round(3).T.to_string())
# last 4 weeks form
n4=nets(p[p.week>=7]); print('last4 net rk',n4.rank(ascending=False).loc[['MIN','SF','IND','HOU']].to_dict(), 'MIN-SF P last4',round(prob('SF','MIN',n4,True),3),'IND-HOU',round(prob('HOU','IND',n4),3))
# Mexico City history
H=g[g.result.notna()]
mx=H[H.stadium.fillna('').str.contains('Azteca|Banorte|Mexico',case=False)]
print(mx[['season','week','away_team','away_score','home_team','home_score','spread_line','stadium']].to_string())
mx=mx[mx.spread_line.notna()]; print('MX fav market wins',((np.sign(mx.result)==np.sign(mx.spread_line))).sum(),'of',len(mx),'exp',norm.cdf(abs(mx.spread_line)/13.5).sum().round(2),'total pts',(mx.home_score+mx.away_score).mean(), 'vs total_line',mx.total_line.mean())
# IND-HOU: Thursday short week both. history thursday home fav vs market (2002-2025) quick
# D) Week 11 upsets: Poisson-binomial
W11=G[G.week==11]; ps=np.array([prob(r.home_team,r.away_team,net,r.location=='Neutral') for r in W11.itertuples()]); fav=np.maximum(ps,1-ps)
dist=np.array([1.0])
for q in fav: dist=np.convolve(dist,[1-q,q])
k=np.arange(len(dist)); print('W11 n',len(fav),'exp fav wins',fav.sum().round(2),'exp upsets',(1-fav).sum().round(2),'P(all fav win)',np.prod(fav).round(4),'P(0 upsets)',dist[-1].round(4))
print(' upsets dist',{int(len(fav)-i):round(dist[i],3) for i in k[::-1]})
# bootstrap range of expected upsets
eu=[]
for b in range(len(BN)):
    pb=np.array([prob(r.home_team,r.away_team,BN.iloc[b],r.location=='Neutral') for r in W11.itertuples()]); eu.append((1-np.maximum(pb,1-pb)).sum())
print(' exp upsets 10-90',np.percentile(eu,[10,90]).round(2))
# OOS weeks 4-10: predicted vs actual upsets per week
rows=[]
for w in range(4,11):
    n=nets(p[p.week<w])
    for r in G[(G.week==w)&G.result.notna()].itertuples():
        if r.result==0: continue
        q=prob(r.home_team,r.away_team,n,r.location=='Neutral'); rows.append((w,max(q,1-q),(q>.5)!=(r.result>0)))
O=pd.DataFrame(rows,columns=['w','fav','upset']); W=O.groupby('w').agg(n=('fav','size'),exp=('fav',lambda x:(1-x).sum()),act=('upset','sum'))
print(W.round(2).to_string()); print('total exp',W.exp.sum().round(1),'act',W.act.sum())
# dispersion test: variance of weekly upsets vs Poisson-binomial variance
var_pb=O.groupby('w').fav.apply(lambda x:(x*(1-x)).sum()); chi=(((W.act-W.exp)**2)/var_pb).sum(); from scipy.stats import chi2
print('dispersion chi2',chi.round(2),'df',len(W),'p',chi2.sf(chi,len(W)).round(3))
# historical market: upsets per week 2010-2025 (market favorite loses)
Hm=g[(g.season.between(2010,2025))&(g.game_type=='REG')&g.result.notna()&g.spread_line.notna()&(g.spread_line!=0)&(g.result!=0)]
Hm=Hm.assign(up=np.sign(Hm.result)!=np.sign(Hm.spread_line)); per=Hm.groupby(['season','week']).agg(n=('up','size'),u=('up','sum'))
print('hist market upsets/wk mean',per.u.mean().round(2),'rate',Hm.up.mean().round(3),'weeks with 0 upsets',(per.u==0).sum(),'of',len(per),'max',per.u.max())
print(' share of weeks with >=4 upsets (n>=13)',(per[per.n>=13].u>=4).mean().round(3))
# C) Rompemitos: snapping long losing streak
H=g[(g.season.between(2002,2025))&(g.game_type=='REG')&g.result.notna()].sort_values(['season','gameday'])
L=[]
for r in H.itertuples():
    L.append((r.season,r.gameday,r.home_team,r.result,r.spread_line)); L.append((r.season,r.gameday,r.away_team,-r.result,-r.spread_line if pd.notna(r.spread_line) else np.nan))
L=pd.DataFrame(L,columns=['season','day','team','m','exp']).sort_values(['season','team','day'])
L['loss']=(L.m<0).astype(int)
L['lstreak_before']=L.groupby(['season','team']).loss.transform(lambda x:x.groupby((x!=x.shift()).cumsum()).cumsum().shift(1).fillna(0)*(x.shift(1)==1))
L['res']=L.m-L.exp
L['next_res']=L.groupby(['season','team']).res.shift(-1); L['next_m']=L.groupby(['season','team']).m.shift(-1); L['next_exp']=L.groupby(['season','team']).exp.shift(-1)
B=L.dropna(subset=['next_res','res'])
hyp={'cortó racha 5+ (siguiente)':(B.lstreak_before>=5)&(B.m>0),
     'cortó racha 8+ (siguiente)':(B.lstreak_before>=8)&(B.m>0),
     'el partido que corta: perdedor de 5+ vs mercado (mismo partido)':None,
     'llega con 5+ derrotas seguidas (siguiente tras perder 5ta+)':None}
L['lstreak_after']=L.lstreak_before*(L.m<0)+(L.m<0)
B=L.dropna(subset=['next_res','res'])
out=[]
def rep(name,res,win,expw):
    t=ttest_1samp(res,0); out.append(t.pvalue); print('C',name,'n',len(res),'res',round(res.mean(),2),'p',round(t.pvalue,3),'win',round(win.mean(),3),'exp',round(expw.mean(),3))
m1=(B.lstreak_before>=5)&(B.m>0); rep('tras cortar racha 5+',B[m1].next_res,B[m1].next_m>0,norm.cdf(B[m1].next_exp/13.5))
m2=(B.lstreak_before>=8)&(B.m>0); rep('tras cortar racha 8+',B[m2].next_res,B[m2].next_m>0,norm.cdf(B[m2].next_exp/13.5))
m3=(L.lstreak_before>=5)&L.res.notna(); rep('equipo con 5+ seguidas, siguiente partido',L[m3].res,L[m3].m>0,norm.cdf(L[m3].exp/13.5))
m4=(L.lstreak_before>=10)&L.res.notna(); rep('equipo con 10+ seguidas, siguiente partido',L[m4].res,L[m4].m>0,norm.cdf(L[m4].exp/13.5))
ps_=np.array(out); o=np.argsort(ps_); mm=len(ps_); bh=np.minimum.accumulate((ps_[o]*mm/np.arange(1,mm+1))[::-1])[::-1]; print('BH',dict(zip(o,bh.round(3))))
# effect size sd
print('sd res',B.res.std().round(1))
# E) Altitud: ventaja de localía de Denver vs resto (2002–2025), cruda y vs mercado
from scipy.stats import ttest_ind, binomtest
H=g[(g.season.between(2002,2025))&(g.game_type=='REG')&g.result.notna()&(g.location=='Home')]
den=H[H.home_team=='DEN']; oth=H[H.home_team!='DEN']
# home-minus-away split per team-season
A=g[(g.season.between(2002,2025))&(g.game_type=='REG')&g.result.notna()&(g.location=='Home')]
hm=A.groupby(['season','home_team']).result.mean(); am=(-A.groupby(['season','away_team']).result.mean())
sp=(hm-am.reindex(hm.index.set_names(['season','away_team']),fill_value=np.nan).values).dropna()
d_=sp[sp.index.get_level_values(1)=='DEN']; o_=sp[sp.index.get_level_values(1)!='DEN']
print('E home-away split DEN',round(d_.mean(),2),'n',len(d_),'others',round(o_.mean(),2),'n',len(o_),ttest_ind(d_,o_,equal_var=False))
print('E DEN home margin vs market',(den.result-den.spread_line).mean().round(2),ttest_1samp((den.result-den.spread_line).dropna(),0).pvalue.round(3),'n',len(den))
print('E home cover rate DEN',((den.result-den.spread_line)>0).mean().round(3))
print('HOU close binom P(<=1 of 6)',binomtest(1,6,.5,alternative='less').pvalue.round(4))
