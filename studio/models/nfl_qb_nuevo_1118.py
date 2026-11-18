"""Ideas 18 nov: efecto de mariscal nuevo sobre el error del modelo NFL v0 (2019-2026). Requiere g2.csv y pbp<año>.csv.gz de nflverse."""
import pandas as pd,numpy as np
from scipy.stats import norm,ttest_1samp,ttest_ind
g=pd.read_csv('g2.csv')
cols=['game_id','season','week','season_type','posteam','defteam','play_type','epa','qb_dropback','passer_player_id','passer_player_name']
P=[]
for y in list(range(2019,2026))+[26]:
    f=f'pbp{y}.csv.gz' if y!=26 else 'pbp26.csv.gz'
    q=pd.read_csv(f,low_memory=False,usecols=cols); q=q[(q.season_type=='REG')&q.play_type.isin(['pass','run'])&q.epa.notna()]; P.append(q)
P=pd.concat(P)
nets=lambda q:q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean()
# QB principal por equipo-partido
db=P[P.passer_player_id.notna()]
m=db.groupby(['season','week','game_id','posteam','passer_player_id','passer_player_name']).size().reset_index(name='n')
m=m.sort_values('n',ascending=False).drop_duplicates(['game_id','posteam']).sort_values(['season','posteam','week'])
rows=[]
for (s,t),a in m.groupby(['season','posteam']):
    a=a.sort_values('week'); seen={}; prev=None; tot=0
    for r in a.itertuples():
        share=seen.get(r.passer_player_id,0)/tot if tot else np.nan
        rows.append(dict(game_id=r.game_id,team=t,season=s,week=r.week,qb=r.passer_player_name,changed=(prev is not None and r.passer_player_id!=prev),share=share))
        d=db[(db.game_id==r.game_id)&(db.posteam==t)].passer_player_id.value_counts()
        for k,v in d.items(): seen[k]=seen.get(k,0)+v; tot+=v
        prev=r.passer_player_id
Q=pd.DataFrame(rows)
# Predicciones v0 fuera de muestra (solo semanas previas)
out=[]
for s in sorted(P.season.unique()):
    Gs=g[(g.season==s)&(g.game_type=='REG')&g.result.notna()&(g.result!=0)]
    ps=P[P.season==s]
    for w in sorted(Gs.week.unique()):
        if w<4: continue
        n=nets(ps[ps.week<w])
        for r in Gs[Gs.week==w].itertuples():
            if r.home_team not in n or r.away_team not in n: continue
            hfa=0 if r.location=='Neutral' else 1.5
            mg=0.5*(n[r.home_team]-n[r.away_team])*61.6+hfa
            out.append(dict(game_id=r.game_id,season=s,week=w,team=r.home_team,opp=r.away_team,pred=mg,act=r.result))
            out.append(dict(game_id=r.game_id,season=s,week=w,team=r.away_team,opp=r.home_team,pred=-mg,act=-r.result))
O=pd.DataFrame(out).merge(Q[['game_id','team','qb','changed','share']],on=['game_id','team'],how='left')
O=O.merge(Q[['game_id','team','changed','share']].rename(columns={'team':'opp','changed':'opp_changed','share':'opp_share'}),on=['game_id','opp'],how='left')
O['res']=O.act-O.pred; O['p']=norm.cdf(O.pred/13.5); O['win']=(O.act>0).astype(float)
O['new']=(O.share.fillna(0)<.25)&(O.changed==True)      # QB con <25% de los pases previos y distinto al partido anterior
O['ret']=(O.changed==True)&~O.new
hist=O[O.season<2026]
def rep(n,x):
    t=ttest_1samp(x.res,0); print(f'{n:32s} n={len(x):5d} res={x.res.mean():+.2f} se={x.res.std()/np.sqrt(len(x)):.2f} p={t.pvalue:.4f} win={x.win.mean():.3f} model={x.p.mean():.3f} brier={((x.p-x.win)**2).mean():.4f}')
rep('todos 2019-25',hist); rep('QB nuevo (<25%)',hist[hist.new]); rep('QB regresa (cambio, >=25%)',hist[hist.ret]); rep('sin cambio',hist[~hist.changed.fillna(False).astype(bool)])
rep('nuevo, solo rival sin cambio',hist[hist.new&~hist.opp_changed.fillna(False).astype(bool)])
for lo,hi,l in [(-99,-3,'modelo lo daba perdedor 3+'),(-3,3,'parejo'),(3,99,'favorito 3+')]:
    rep('nuevo · '+l,hist[hist.new&(hist.pred>=lo)&(hist.pred<hi)])
print(ttest_ind(hist[hist.new].res,hist[~hist.changed.fillna(False).astype(bool)].res,equal_var=False))
# por temporada, estabilidad
print(hist[hist.new].groupby('season').res.agg(['size','mean']).round(2).T.to_string())
# bootstrap IC 80% del efecto
rng=np.random.default_rng(1118); x=hist[hist.new].res.values
b=[x[rng.integers(0,len(x),len(x))].mean() for _ in range(5000)]; print('efecto IC80',np.percentile(b,[10,90]).round(2))
# Mejora Brier: corregir fuera de muestra (estimar efecto con temporadas previas)
rec=[]
for s in range(2020,2027):
    tr=O[(O.season<s)&O.new]; te=O[(O.season==s)]; eff=tr.res.mean()
    te=te[te.team<te.opp].copy()
    adj=te.pred+eff*(te.new.astype(int)-te.opp.map(lambda _:0))
    # efecto del rival
    k=O[(O.season==s)].set_index(['game_id','team']).new
    oppnew=[k.get((a,b),False) for a,b in zip(te.game_id,te.opp)]
    adj=te.pred+eff*(te.new.astype(int)-np.array(oppnew).astype(int))
    rec.append((s,len(te),((norm.cdf(te.pred/13.5)-te.win)**2).mean(),((norm.cdf(adj/13.5)-te.win)**2).mean(),eff, (te.new|np.array(oppnew)).sum()))
R=pd.DataFrame(rec,columns=['s','n','b0','b1','eff','nnew']);print(R.round(4).to_string());print('tot',(R.b0*R.n).sum()/R.n.sum(),(R.b1*R.n).sum()/R.n.sum())
# 2026 casos
c=O[(O.season==2026)&O.new][['week','team','opp','qb','share','pred','act','res']];print(c.round(2).to_string()); print('2026 nuevo n',len(c),'res',c.res.mean().round(2))
O.to_pickle('O.pkl'); Q.to_pickle('Q.pkl')
print(Q[(Q.season==2026)&Q.team.isin(['BAL','MIN','TB','NYJ'])].sort_values(['team','week'])[['team','week','qb','changed','share']].round(2).to_string())
