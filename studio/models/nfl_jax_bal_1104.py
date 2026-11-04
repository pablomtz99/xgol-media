import pandas as pd, numpy as np
from scipy.stats import norm, binomtest
p=pd.read_csv('pbp.csv.gz',low_memory=False); p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
off=p.groupby('posteam').epa.mean(); de=p.groupby('defteam').epa.mean(); net=off-de
b=p[p.posteam=='BAL']
noL=b[~b.game_id.isin(['2026_01_BAL_IND','2026_02_NO_BAL','2026_03_BAL_DAL','2026_04_TEN_BAL'])]
# plays without Lamar at QB: games 5-7 plus wk8 plays after he left? approximate with passer not Jackson in weeks5-8
w8=b[b.game_id=='2026_08_BAL_BUF']
print('BAL off EPA all',off['BAL'],'wk5-7',b[b.week.isin([5,6,7])].epa.mean(), 'n',len(b[b.week.isin([5,6,7])]))
adj_off=b[b.week.isin([5,6,7])].epa.mean()
net_adj=adj_off-de['BAL']
for lab,nb in [('season',net['BAL']),('sinLamar',net_adj)]:
    m=0.5*(nb-net['JAX'])*61.6+1.5; print(lab,'margin',round(m,2),'P(BAL)',round(norm.cdf(m/13.5),3))
# bootstrap by game for interval (resample plays within team)
rng=np.random.default_rng(1); R=[]
J=p[p.posteam=='JAX'].epa.values; Jd=p[p.defteam=='JAX'].epa.values; Bo=b[b.week.isin([5,6,7])].epa.values; Bd=p[p.defteam=='BAL'].epa.values
for _ in range(4000):
    nj=rng.choice(J,len(J)).mean()-rng.choice(Jd,len(Jd)).mean(); nb=rng.choice(Bo,len(Bo)).mean()-rng.choice(Bd,len(Bd)).mean()
    R.append(norm.cdf((0.5*(nb-nj)*61.6+1.5)/13.5))
print('P(JAX) 80%',1-np.percentile(R,90),1-np.percentile(R,10))
# Monte Carlo of margin distribution with the adjusted model
m=0.5*(net_adj-net['JAX'])*61.6+1.5; sims=rng.normal(m,13.5,200000)
print('P(JAX by >=10)',(sims<=-10).mean(),'P(BAL by 1+)',(sims>0).mean())
# history: home underdogs of >=9.5 (spread_line<=-9.5) 1999-2025
g=pd.read_csv('games.csv'); h=g[(g.season<2026)&g.home_score.notna()&(g.spread_line<=-9.5)&(g.game_type=='REG')]
w=(h.home_score>h.away_score).sum(); print('home dogs >=9.5:',len(h),'wins',w,w/len(h), 'implied avg',norm.cdf(h.spread_line/13.5).mean())
h2=g[(g.season<2026)&g.home_score.notna()&(g.spread_line<=-9.5)]
# how rare per season
print(h.groupby('season').size().tail(10))
# JAX ranks w/ adjusted, games played
print('JAX net', net['JAX'], 'BAL net adj', net_adj, 'BAL def', de['BAL'])
# JAX point diff per game, BAL
