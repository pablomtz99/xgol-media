"""NFL Black Friday vie 27 nov 14:00 CDMX: DEN (8-2) en PIT (6-4). Regresión a la media: ¿qué pasa después con equipos cuyo récord supera a sus puntos?
nflverse games.csv 2010-2025 (temporada regular). Ejecutar con SCR=<carpeta con games.csv>. Probabilidad del juego: nfl_1125.py (Modelo NFL v0)."""
import pandas as pd,numpy as np,os
from scipy.stats import ttest_ind, mannwhitneyu
D=os.environ.get('SCR','.');g=pd.read_csv(f'{D}/games.csv');g=g[(g.game_type=='REG')]
s=g[(g.season==2026)&g.result.notna()]
for t in ['DEN','PIT']:
    r=[];
    for x in s.itertuples():
        if t in (x.home_team,x.away_team):
            m=x.result if x.home_team==t else -x.result;r.append(m)
    r=np.array(r);print(t,'margenes',r.tolist(),'por 1-8 pts',f'{(r>0)[abs(r)<=8].sum()}-{(r<0)[abs(r)<=8].sum()}','por 9+',f'{(r>0)[abs(r)>8].sum()}-{(r<0)[abs(r)>8].sum()}','dif',r.sum())
rows=[]
for se in range(2010,2026):
    G=g[(g.season==se)&g.result.notna()].sort_values(['gameday','gametime'])
    for t in pd.unique(G[['home_team','away_team']].values.ravel()):
        x=G[(G.home_team==t)|(G.away_team==t)]
        m=np.where(x.home_team==t,x.result,-x.result);pf=np.where(x.home_team==t,x.home_score,x.away_score);pa=np.where(x.home_team==t,x.away_score,x.home_score)
        if len(m)<14:continue
        f=slice(0,10);w=(m[f]>0).sum()+0.5*(m[f]==0).sum();pe=pf[f].sum()**2.37/(pf[f].sum()**2.37+pa[f].sum()**2.37)
        rest=m[10:];rows.append((se,t,w,10*pe,w-10*pe,((rest>0).sum()+0.5*(rest==0).sum())/len(rest)))
R=pd.DataFrame(rows,columns=['se','t','w10','pyt10','luck','rest'])
L=R[R.luck>=2];O=R[(R.luck.abs()<1)]
print('equipos con récord ≥2 victorias sobre Pitágoras tras 10 juegos n',len(L),'gan% antes',(L.w10/10).mean().round(3),'gan% después',L.rest.mean().round(3),'pitag% antes',(L.pyt10/10).mean().round(3))
L8=R[(R.w10>=8)&(R.luck>=2)];print('8+ victorias y ≥2 sobre Pitágoras n',len(L8),'después',L8.rest.mean().round(3),'pitag',(L8.pyt10/10).mean().round(3))
# regresión: rest ~ w10 + pyt10
import numpy.linalg as la
X=np.c_[np.ones(len(R)),R.w10/10,R.pyt10/10];b=la.lstsq(X,R.rest,rcond=None)[0];res=R.rest-X@b;se_=np.sqrt(res.var()*np.diag(la.inv(X.T@X)))
print('rest% = a + b1*W% + b2*Pyt%  coef',b.round(3),'se',se_.round(3),'t',(b/se_).round(1))
print('predicho DEN (8-2, pyt 5.7)',(np.array([1,.8,.57])@b).round(3))
t,p=ttest_ind(L.rest,(L.w10/10),equal_var=False);print('caída de gan% (antes vs después) en el grupo: t',round(t,2),'p',f'{p:.2g}','dif',(L.rest-(L.w10/10)).mean().round(3))
