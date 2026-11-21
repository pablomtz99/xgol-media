"""NFL semana 11 (dom 22 nov) — Modelo NFL v0 con jugadas semanas 1–11 (incl. IND@HOU del jueves). Prueba: ¿la semana de descanso (bye) ayuda?
Datos: nflverse (games.csv, play_by_play_2026). Ejecutar en carpeta con g2.csv y pbp26.csv.gz."""
import pandas as pd,numpy as np
from scipy.stats import norm
def ols(y,X,names):
    X=np.column_stack([np.ones(len(y))]+X);y=np.asarray(y,float);XtXi=np.linalg.inv(X.T@X);b=XtXi@X.T@y;e=y-X@b;n,k=X.shape
    V=XtXi@(X.T*(e**2))@X@XtXi*n/(n-k);se=np.sqrt(np.diag(V));z=b/se
    for nm,bb,ss,zz in zip(['const']+names,b,se,z): print(f'  {nm:6s} {bb:+.3f} (ee {ss:.3f}) p={2*norm.sf(abs(zz)):.4f}')
    return b,se
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success','pass_oe' if False else 'epa'])
p=pd.read_csv('pbp26.csv.gz',low_memory=False,usecols=['game_id','week','posteam','defteam','play_type','epa','success'])
p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
print('semanas en pbp',p.week.min(),p.week.max(),'jugadas',len(p))
g=pd.read_csv('g2.csv')
off=p.groupby('posteam').epa.mean();de=p.groupby('defteam').epa.mean();net=off-de
offp=p[p.play_type=='pass'].groupby('posteam').epa.mean();defp=p[p.play_type=='pass'].groupby('defteam').epa.mean()
offr=p[p.play_type=='run'].groupby('posteam').epa.mean();defr=p[p.play_type=='run'].groupby('defteam').epa.mean()
rk=lambda s,t,asc=False: int(s.rank(ascending=asc)[t])
W=g[(g.season==2026)&(g.week==11)&(g.gameday>='2026-11-22')]
# incertidumbre: bootstrap por partido
gids=p.game_id.unique();rng=np.random.default_rng(1121);B=[]
grp={k:v for k,v in p.groupby('game_id')}
for b in range(300):
    q=pd.concat([grp[x] for x in rng.choice(gids,len(gids))]);n=q.groupby('posteam').epa.mean()-q.groupby('defteam').epa.mean();B.append(n.reindex(net.index).fillna(net))
for r in W.itertuples():
    h,a=r.home_team,r.away_team;neu=r.location=='Neutral'
    mg=0.5*(net[h]-net[a])*61.6+(0 if neu else 1.5);pr=norm.cdf(mg/13.5)
    bs=[norm.cdf((0.5*(n[h]-n[a])*61.6+(0 if neu else 1.5))/13.5) for n in B];lo,hi=np.percentile(bs,[10,90])
    print(f"{a}@{h} rest {r.away_rest}/{r.home_rest} P(local) {pr:.3f} [{lo:.3f}-{hi:.3f}] margen {mg:+.1f} | net {net[a]:+.3f}({rk(net,a)}) vs {net[h]:+.3f}({rk(net,h)})")
for t in ['TB','DET','PIT','PHI','NO','CHI','LV','DEN']:
    print(t,'off',round(off[t],3),rk(off,t),'def',round(de[t],3),rk(de,t,True),'pass off',rk(offp,t),'pass def',rk(defp,t,True),'run off',rk(offr,t),'run def',rk(defr,t,True))
# ---- prueba histórica: bye ----
h=g[(g.season>=2010)&(g.season<=2025)&(g.game_type=='REG')&g.result.notna()].copy()
h['rd']=h.home_rest-h.away_rest
h['hbye']=(h.home_rest>=13)&(h.away_rest<=8);h['abye']=(h.away_rest>=13)&(h.home_rest<=8)
# calidad previa: diferencial por partido del equipo en la temporada hasta antes del juego
rows=[]
for s,gs in h.groupby('season'):
    gs=gs.sort_values('gameday');pdiff={};gp={}
    for r in gs.itertuples():
        qh=pdiff.get(r.home_team,0)/max(gp.get(r.home_team,0),1);qa=pdiff.get(r.away_team,0)/max(gp.get(r.away_team,0),1)
        rows.append((r.game_id,qh-qa,gp.get(r.home_team,0),gp.get(r.away_team,0)))
        pdiff[r.home_team]=pdiff.get(r.home_team,0)+r.result;pdiff[r.away_team]=pdiff.get(r.away_team,0)-r.result
        gp[r.home_team]=gp.get(r.home_team,0)+1;gp[r.away_team]=gp.get(r.away_team,0)+1
q=pd.DataFrame(rows,columns=['game_id','qd','gph','gpa']);h=h.merge(q,on='game_id')
h['bye']=h.hbye.astype(int)-h.abye.astype(int)
hh=h[(h.gph>=3)&(h.gpa>=3)&(h.home_rest<=15)&(h.away_rest<=15)&(h.location=='Home')]
ols(hh.result,[hh.bye,hh.qd],['bye','qd']);print('n',len(hh),'n con bye',(hh.bye!=0).sum())
# win% del equipo con bye (sin ajustar)
b1=hh[hh.bye==1];b2=hh[hh.bye==-1]
wins=(b1.result>0).sum()+(b2.result<0).sum();n=len(b1)+len(b2);print('equipo con bye gana',wins,'/',n,round(wins/n,3))
# local con bye vs local sin bye
print('local con bye margen',b1.result.mean().round(2),'| local normal',hh[hh.bye==0].result.mean().round(2),'| visitante con bye: margen local',b2.result.mean().round(2))
# recientes 2018-2025
r8=hh[hh.season>=2018];print('2018+ n bye',(r8.bye!=0).sum());ols(r8.result,[r8.bye,r8.qd],['bye','qd'])
