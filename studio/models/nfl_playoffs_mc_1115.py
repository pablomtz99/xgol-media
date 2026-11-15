import pandas as pd,numpy as np
from scipy.stats import norm
rng=np.random.default_rng(2026)
DIV={'AFC Este':['BUF','MIA','NE','NYJ'],'AFC Norte':['BAL','CIN','CLE','PIT'],'AFC Sur':['HOU','IND','JAX','TEN'],'AFC Oeste':['DEN','KC','LV','LAC'],
'NFC Este':['DAL','NYG','PHI','WAS'],'NFC Norte':['CHI','DET','GB','MIN'],'NFC Sur':['ATL','CAR','NO','TB'],'NFC Oeste':['ARI','LA','SF','SEA']}
t2d={t:d for d,ts in DIV.items() for t in ts}
g=pd.read_csv('g2.csv'); G=g[(g.season==2026)&(g.game_type=='REG')]
played=G[G.result.notna()]; rem=G[G.result.isna()]
print('played',len(played),'remaining',len(rem))
T=sorted(t2d); ix={t:i for i,t in enumerate(T)}
W0=np.zeros(32)
for r in played.itertuples():
    if r.result>0: W0[ix[r.home_team]]+=1
    elif r.result<0: W0[ix[r.away_team]]+=1
    else: W0[ix[r.home_team]]+=.5; W0[ix[r.away_team]]+=.5
BN=pd.read_pickle('boot.pkl'); net=pd.read_pickle('net.pkl')
H=np.array([ix[t] for t in rem.home_team]); A=np.array([ix[t] for t in rem.away_team]); neu=(rem.location=='Neutral').values
N=10000; per=N//len(BN)
res={k:np.zeros(32) for k in ['po','div','seed1','wins']}; winsall=[]
for b in range(len(BN)):
    n=BN.iloc[b].reindex(T).fillna(0).values
    m=0.5*(n[H]-n[A])*61.6+np.where(neu,0,1.5); pr=norm.cdf(m/13.5)
    for k in range(per):
        hw=rng.random(len(pr))<pr
        W=W0.copy(); np.add.at(W,H[hw],1); np.add.at(W,A[~hw],1)
        key=W+rng.random(32)*1e-3  # random tiebreak
        res['wins']+=W; winsall.append(W)
        for conf in ['AFC','NFC']:
            divw=[]
            for d,ts in DIV.items():
                if not d.startswith(conf): continue
                ii=[ix[t] for t in ts]; w=max(ii,key=lambda i:key[i]); divw.append(w); res['div'][w]+=1
            others=[ix[t] for t in T if t2d[t].startswith(conf) and ix[t] not in divw]
            wc=sorted(others,key=lambda i:-key[i])[:3]
            for i in divw+wc: res['po'][i]+=1
            res['seed1'][max(divw,key=lambda i:key[i])]+=1
WA=np.array(winsall)
out=pd.DataFrame({'t':T,'div':[t2d[t] for t in T],'W':W0,'net':net.reindex(T).values,'expW':res['wins']/N,'w10':np.percentile(WA,10,axis=0),'w90':np.percentile(WA,90,axis=0),
 'P_po':res['po']/N,'P_div':res['div']/N,'P_1':res['seed1']/N}).sort_values('P_po',ascending=False)
pd.set_option('display.width',200); print(out.round(3).to_string(index=False))
out.to_csv('mc.csv',index=False)
