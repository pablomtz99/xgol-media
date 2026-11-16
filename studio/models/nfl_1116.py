"""Cálculos 16 nov (NFL tras semana 10). Ejecutar en una carpeta con g2.csv (nflverse games.csv) y pbp26.csv.gz (play_by_play_2026)."""
import pandas as pd,numpy as np
from scipy.stats import norm, ttest_1samp, binomtest, pearsonr
rng=np.random.default_rng(1116)
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success'])
p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
g=pd.read_csv('g2.csv'); G=g[(g.season==2026)&(g.game_type=='REG')]
nets=lambda q:q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean()
net=nets(p)
prob=lambda h,a,n,neu=False: norm.cdf((0.5*(n[h]-n[a])*61.6+(0 if neu else 1.5))/13.5)
print('plays',len(p))
gids=p.game_id.unique(); grp={k:v for k,v in p.groupby('game_id')}; B=400; boots=[]
for b in range(B):
    s=rng.choice(gids,len(gids)); boots.append(nets(pd.concat([grp[k] for k in s])))
BN=pd.DataFrame(boots).fillna(0); BN.to_pickle('boot10.pkl')
# A) LAC@BAL
ps=np.array([prob('BAL','LAC',BN.iloc[i]) for i in range(B)])
print('A BAL',round(prob('BAL','LAC',net),3),np.percentile(ps,[10,90]).round(3),'margin',round(0.5*(net['BAL']-net['LAC'])*61.6+1.5,1))
T=pd.DataFrame({'net':net})
for pt in ['pass','run']:
    q=p[p.play_type==pt]; T[pt+'_o']=q.groupby('posteam').epa.mean(); T[pt+'_d']=q.groupby('defteam').epa.mean()
T['sr_o']=p.groupby('posteam').success.mean(); T['sr_d']=p.groupby('defteam').success.mean()
for c in T: T[c+'_rk']=T[c].rank(ascending=c.endswith('_d')==False).astype(int) if not c.endswith('_d') else T[c].rank().astype(int)
print(T.loc[['LAC','BAL']].round(3).T.to_string())
# historical: winless teams 0-8+ entering a game, 2002-2025
H=g[(g.season.between(2002,2025))&(g.game_type=='REG')&g.result.notna()&g.spread_line.notna()].sort_values(['season','week'])
rows=[]
for (se),q in H.groupby('season'):
    rec={}
    for r in q.itertuples():
        for t,side in [(r.home_team,1),(r.away_team,-1)]:
            w,l=rec.get(t,(0,0))
            if w==0 and l>=8:
                rows.append(dict(season=se,team=t,L=l,exp=side*r.spread_line,act=side*r.result))
        hw=r.result>0; aw=r.result<0
        w,l=rec.get(r.home_team,(0,0)); rec[r.home_team]=(w+hw,l+aw)
        w,l=rec.get(r.away_team,(0,0)); rec[r.away_team]=(w+aw,l+hw)
d=pd.DataFrame(rows); d['win']=(d.act>0).astype(float); d['pexp']=norm.cdf(d.exp/13.5); d['res']=d.act-d.exp
print('A winless 0-8+: n',len(d),'teams',d.groupby(['season','team']).ngroups,'wins',d.win.sum(),'exp',d.pexp.sum().round(1),'res',d.res.mean().round(2),ttest_1samp(d.res,0).pvalue.round(3))
fin=d.groupby(['season','team']).agg(n=('win','size'),w=('win','sum')); print('finished winless (of those reaching 0-8):',(fin.w==0).sum(),'of',len(fin))
# MC rest of season LAC
DIV={'AFC Este':['BUF','MIA','NE','NYJ'],'AFC Norte':['BAL','CIN','CLE','PIT'],'AFC Sur':['HOU','IND','JAX','TEN'],'AFC Oeste':['DEN','KC','LV','LAC'],
'NFC Este':['DAL','NYG','PHI','WAS'],'NFC Norte':['CHI','DET','GB','MIN'],'NFC Sur':['ATL','CAR','NO','TB'],'NFC Oeste':['ARI','LA','SF','SEA']}
t2d={t:d for d,ts in DIV.items() for t in ts}; TT=sorted(t2d); ix={t:i for i,t in enumerate(TT)}
played=G[G.result.notna()]; rem=G[G.result.isna()]
W0=np.zeros(32)
for r in played.itertuples():
    if r.result>0: W0[ix[r.home_team]]+=1
    elif r.result<0: W0[ix[r.away_team]]+=1
    else: W0[ix[r.home_team]]+=.5; W0[ix[r.away_team]]+=.5
Hh=np.array([ix[t] for t in rem.home_team]); A=np.array([ix[t] for t in rem.away_team]); neu=(rem.location=='Neutral').values
N=10000; per=N//B; res={k:np.zeros(32) for k in ['po','div','seed1']}; WA=[]
for b in range(B):
    n=BN.iloc[b].reindex(TT).fillna(0).values; pr=norm.cdf((0.5*(n[Hh]-n[A])*61.6+np.where(neu,0,1.5))/13.5)
    for k in range(per):
        hw=rng.random(len(pr))<pr; W=W0.copy(); np.add.at(W,Hh[hw],1); np.add.at(W,A[~hw],1); WA.append(W)
        key=W+rng.random(32)*1e-3
        for conf in ['AFC','NFC']:
            dv=[]
            for dd,ts in DIV.items():
                if not dd.startswith(conf): continue
                w=max([ix[t] for t in ts],key=lambda i:key[i]); dv.append(w); res['div'][w]+=1
            oth=[ix[t] for t in TT if t2d[t].startswith(conf) and ix[t] not in dv]
            for i in dv+sorted(oth,key=lambda i:-key[i])[:3]: res['po'][i]+=1
            res['seed1'][max(dv,key=lambda i:key[i])]+=1
WA=np.array(WA)
out=pd.DataFrame({'t':TT,'W':W0,'net':net.reindex(TT).values,'rk':net.rank(ascending=False).reindex(TT).values,'expW':WA.mean(0),'w10':np.percentile(WA,10,0),'w90':np.percentile(WA,90,0),
  'P_po':res['po']/N,'P_div':res['div']/N,'P_1':res['seed1']/N,'P0':(WA==0).mean(0)}).sort_values('P_po',ascending=False)
pd.set_option('display.width',220); print(out.round(3).to_string(index=False)); out.to_csv('mc10.csv',index=False)

# B) 7-2 teams after 9 games, 2002-2025: rest-of-season win% vs first-9 point diff
H=g[(g.season.between(2002,2025))&(g.game_type=='REG')&g.result.notna()].sort_values(['season','gameday'])
L=[]
for r in H.itertuples():
    L.append((r.season,r.home_team,r.result,r.spread_line)); L.append((r.season,r.away_team,-r.result,-r.spread_line if pd.notna(r.spread_line) else np.nan))
L=pd.DataFrame(L,columns=['season','team','m','exp'])
L['k']=L.groupby(['season','team']).cumcount()
f=L[L.k<9].groupby(['season','team']).agg(w9=('m',lambda x:(x>0).sum()+0.5*(x==0).sum()),d9=('m','mean'),n9=('m','size'))
r_=L[L.k>=9].groupby(['season','team']).agg(wr=('m',lambda x:((x>0).sum()+0.5*(x==0).sum())/len(x)),nr=('m','size'))
F=f.join(r_).dropna(); F=F[F.n9==9]
X=np.column_stack([np.ones(len(F)),(F.w9-F.w9.mean())/F.w9.std(),(F.d9-F.d9.mean())/F.d9.std()]); y=F.wr.values
b,res_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b; s2=e@e/(len(y)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
from scipy.stats import t as tdist
print('B n',len(F),'beta std (rec, diff)',b[1:].round(3),'se',se[1:].round(3),'p',(2*tdist.sf(abs(b/se),len(y)-3))[1:].round(4))
S=F[F.w9==7]; print('7-2 teams',len(S),'rest win',S.wr.mean().round(3))
for lo,hi in [(-99,3),(3,8),(8,99)]:
    q=S[(S.d9>lo)&(S.d9<=hi)]; print(' diff',lo,hi,len(q),'rest win',q.wr.mean().round(3),'playoff-ish proj wins',(7+q.wr*8).mean().round(1))
lowd=S[S.d9<=3]; hid=S[S.d9>8]
from scipy.stats import ttest_ind, mannwhitneyu
print(' t low vs high',ttest_ind(lowd.wr,hid.wr,equal_var=False))
print(' low list',lowd.reset_index()[['season','team','d9','wr']].round(2).to_string())

# C) Rompemitos palizas: next game after winning by >=20 / losing by >=20 / scoring 40+  (vs market expectation)
L['res']=L.m-L.exp; L['next_res']=L.groupby(['season','team']).res.shift(-1); L['next_m']=L.groupby(['season','team']).m.shift(-1)
L['next_exp']=L.groupby(['season','team']).exp.shift(-1)
base=L.dropna(subset=['next_res'])
hyp={'gano por 20+':base.m>=20,'perdio por 20+':base.m<=-20,'gano por 20+ siendo no favorito':(base.m>=20)&(base.exp<0),'gano 3+ seguidos':None}
# streak
L['win']=(L.m>0).astype(int); L['st']=L.groupby(['season','team']).win.transform(lambda x:x.groupby((x!=x.shift()).cumsum()).cumsum()*x)
base=L.dropna(subset=['next_res']); hyp['gano 4+ seguidos']=base.st>=4; del hyp['gano 3+ seguidos']
ps=[]
for k,msk in hyp.items():
    q=base[msk]; t_=ttest_1samp(q.next_res,0); ps.append(t_.pvalue)
    print('C',k,'n',len(q),'next res',q.next_res.mean().round(2),'p',round(t_.pvalue,3),'next win',(q.next_m>0).mean().round(3),'exp',norm.cdf(q.next_exp/13.5).mean().round(3))
ps=np.array(ps); o=np.argsort(ps); m=len(ps); bh=np.minimum.accumulate((ps[o]*m/np.arange(1,m+1))[::-1])[::-1]; print('BH q',dict(zip(np.array(list(hyp))[o],bh.round(3))))

# D) close games luck: correlation first 9 vs rest close win%
L['close']=L.m.abs()<=8
c1=L[(L.k<9)&L.close].groupby(['season','team']).m.agg(lambda x:(x>0).mean()).rename('c1'); c2=L[(L.k>=9)&L.close].groupby(['season','team']).m.agg(lambda x:(x>0).mean()).rename('c2')
n1=L[(L.k<9)&L.close].groupby(['season','team']).size().rename('n1')
C=pd.concat([c1,c2,n1],axis=1).dropna(); C=C[C.n1>=4]; print('D r close',pearsonr(C.c1,C.c2))
for lab,q in [('<=1 of 5+ close',C[(C.n1>=5)&(C.c1<=0.2)]),('>=0.8 of 5+',C[(C.n1>=5)&(C.c1>=0.8)])]: print(' ',lab,len(q),'rest close win',q.c2.mean().round(3))
print('TB binom P(<=1 of 7)',binomtest(1,7,.5,alternative='less').pvalue.round(4),'DEN P(6 of 6)',0.5**6)
