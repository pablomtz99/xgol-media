"""Ideas 18 nov: efecto por inicio consecutivo (1°,2°,3°) y probabilidades ajustadas semana 11. Ejecutar tras nfl_qb_nuevo_1118.py."""
import pandas as pd,numpy as np
from scipy.stats import norm,ttest_1samp,ttest_ind,binom,pearsonr
rng=np.random.default_rng(11181)
O=pd.read_pickle('O.pkl');Q=pd.read_pickle('Q.pkl');g=pd.read_csv('g2.csv')
# Robustez: titular oficial de games.csv
Gq=g[(g.season.between(2019,2025))&(g.game_type=='REG')]
L=pd.concat([Gq[['game_id','season','week','home_team','home_qb_id']].set_axis(['game_id','season','week','team','sid'],axis=1),Gq[['game_id','season','week','away_team','away_qb_id']].set_axis(['game_id','season','week','team','sid'],axis=1)]).sort_values(['season','team','week'])
L['prev']=L.groupby(['season','team']).sid.shift(1); L['chg_off']=(L.sid!=L.prev)&L.prev.notna()
L['starts_before']=L.groupby(['season','team','sid']).cumcount()
H=O[O.season<2026].merge(L[['game_id','team','chg_off','starts_before']],on=['game_id','team'])
x=H[H.chg_off&(H.starts_before==0)]; print('ROBUST titular oficial, 1a titularidad del año: n',len(x),'res',x.res.mean().round(2),'p',ttest_1samp(x.res,0).pvalue, 'win',x.win.mean().round(3),'model',x.p.mean().round(3))
# Consecutive starts of a new QB: 1st,2nd,3rd
Q=Q.sort_values(['season','team','week']); rows=[]
for (s,t),a in Q.groupby(['season','team']):
    run=0;cur=None
    for r in a.itertuples():
        if r.changed and (r.share if r.share==r.share else 0)<.25: run=1;cur=r.qb
        elif run>0 and r.qb==cur: run+=1
        else: run=0;cur=None
        rows.append((r.game_id,t,run))
R=pd.DataFrame(rows,columns=['game_id','team','run']); O2=O.merge(R,on=['game_id','team'])
h=O2[O2.season<2026]
eff={}
for k in [1,2,3]:
    x=h[h.run==k]; b=[x.res.values[rng.integers(0,len(x),len(x))].mean() for _ in range(4000)]
    eff[k]=x.res.mean(); print(f'inicio #{k}: n={len(x)} res={x.res.mean():+.2f} IC80={np.percentile(b,[10,90]).round(2)} p={ttest_1samp(x.res,0).pvalue:.4f} gana={x.win.mean():.3f} modelo={x.p.mean():.3f}')
x=h[h.run>=4]; print('inicio 4+: n',len(x),'res',x.res.mean().round(2),'p',ttest_1samp(x.res,0).pvalue.round(3))
print('BH family p:',[round(ttest_1samp(h[h.run==k].res,0).pvalue,4) for k in [1,2,3]])
y=O2[(O2.season==2026)&(O2.run>0)]; print('2026 run>0: n',len(y),'res',y.res.mean().round(2)); print(O2[(O2.season==2026)&(O2.week==10)&(O2.run>0)][['team','qb','run','pred','act']].round(1).to_string())
# Aplicar a semana 11
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa']); p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
nets=lambda q:q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean()
net=nets(p); gids=p.game_id.unique(); grp={k:v for k,v in p.groupby('game_id')}
BN=pd.DataFrame([nets(pd.concat([grp[k] for k in rng.choice(gids,len(gids))])) for _ in range(400)]).fillna(0)
W=g[(g.season==2026)&(g.week==11)]
second={'MIN','BAL','ARI','LV','MIA'}   # 2o inicio consecutivo tras debut en sem.10 (pbp)
e2=eff[2]
print('Efecto 2o inicio aplicado',round(e2,2))
for r in W.itertuples():
    neu=r.location=='Neutral'; hfa=0 if neu else 1.5
    m=lambda n:0.5*(n[r.home_team]-n[r.away_team])*61.6+hfa
    adj=(e2 if r.home_team in second else 0)-(e2 if r.away_team in second else 0)
    bs=np.array([m(BN.iloc[i]) for i in range(400)])
    pa=norm.cdf((bs+adj)/13.5); p0=norm.cdf(bs/13.5)
    print(f'{r.away_team}@{r.home_team} base={norm.cdf(m(net)/13.5):.3f} [{np.percentile(p0,10):.3f}-{np.percentile(p0,90):.3f}] ajustada={norm.cdf((m(net)+adj)/13.5):.3f} [{np.percentile(pa,10):.3f}-{np.percentile(pa,90):.3f}] adj={adj:+.2f}')
