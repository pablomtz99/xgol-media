"""Modelo NBA v1 (versión SRS) para el viernes 20 nov (9 juegos, NBA Cup). Datos: Basketball-Reference (tabla avanzada, revisada 19-nov,
partidos hasta el miércoles 18; ningún equipo del viernes jugó el jueves 19 → récords vigentes y sin back-to-back).
Calidad = promedio ponderado SRS 2026-27 y prior 90% del nivel 2025-26 (peso 16). Local +2.0; σ = 14.7. Incertidumbre por error del nivel (MC)."""
import numpy as np, sys, os
from scipy.stats import norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nba_srs_1119.py'))
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S,Q,K,H,SIG=m.S,m.Q,m.K,m.H,m.SIG
G=[("Hornets","Hawks"),("Raptors","Pistons"),("Magic","Nets"),("Pacers","Cavaliers"),("Wizards","Bulls"),("Pelicans","Thunder"),("Suns","Jazz"),("Kings","Lakers"),("Rockets","Nuggets")]
rng=np.random.default_rng(1120);N=200000
P=[];FAV=[]
for a,h in G:
    mg=Q[h]-Q[a]+H;p=norm.cdf(mg/SIG)
    n1,n2=sum(S[h][:2]),sum(S[a][:2])
    qh=rng.normal(Q[h],SIG/np.sqrt(n1+K),N);qa=rng.normal(Q[a],SIG/np.sqrt(n2+K),N);pp=norm.cdf((qh-qa+H)/SIG)
    lo,hi=np.percentile(pp,[10,90]);P.append(p);f=h if p>=.5 else a;pf=max(p,1-p);FAV.append((f,pf))
    print(f"{a:13s}@ {h:10s} P(local) {p:.3f} [{lo:.3f} {hi:.3f}] margen {mg:+.1f}  fav {f} {pf:.3f}")
pf=np.array([x[1] for x in FAV])
print('P(todos los favoritos)',pf.prod().round(4),'1 en',round(1/pf.prod(),1))
print('sorpresas esperadas',(1-pf).sum().round(2))
# MC distribución de sorpresas
up=(rng.random((N,len(pf)))>pf).sum(1);print('dist sorpresas',np.bincount(up,minlength=10)[:7]/N,'80%',np.percentile(up,[10,90]))
print('P(>=2 sorpresas)',(up>=2).mean().round(3),'P(0)',(up==0).mean().round(4))
# HOU@DEN matchup
for t in ['Rockets','Nuggets']: print(t,S[t],round(Q[t],2))
