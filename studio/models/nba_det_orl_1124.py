"""NBA Cup mar 24 nov: Pistons (10-6) en Magic (7-9), 18:00 CDMX. Modelo NBA v1 (SRS B-Ref al 18 nov + prior; nba_srs_1119.py), igual que nba_copa_1123.py.
Récords y bajas hoy: Sportbusy (24 nov): DET sin Duren, Robinson, Prince, Okorie; Cunningham día a día. ORL sin Banchero, Isaac, Penda, Nelson.
Mercado: probabilidad sin margen de la casa a partir de los precios de Sportbusy (no se publican precios). Splits casa/visita: Sportbusy."""
import numpy as np, io, contextlib, importlib.util, os
from scipy.stats import norm, fisher_exact, binom
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nba_srs_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S,Q,K,H,SIG,rk=m.S,m.Q,m.K,m.H,m.SIG,m.rk
h,a='Magic','Pistons';mg=Q[h]-Q[a]+H;p=1-norm.cdf(mg/SIG)
rng=np.random.default_rng(1124);N=200000
qh=rng.normal(Q[h],SIG/np.sqrt(sum(S[h][:2])+K),N);qa=rng.normal(Q[a],SIG/np.sqrt(sum(S[a][:2])+K),N);pp=1-norm.cdf((qh-qa+H)/SIG)
print(f'P(DET) {p:.3f} 80% {np.percentile(pp,10):.3f}-{np.percentile(pp,90):.3f} margen DET {-mg:+.1f} | Q DET {Q[a]:.2f} ({rk[a]}) ORL {Q[h]:.2f} ({rk[h]})')
for adj,lab in [(-3,'sin Cunningham (aprox −3)'),(-4.5,'sin Cunningham, peor caso (−4.5)')]:print(lab,round(norm.cdf((-mg+adj)/SIG),3))
def imp(o):return 100/(100+o) if o>0 else -o/(-o+100)
x,y=imp(-128),imp(128);print('mercado DET sin margen',round(x/(x+y),3))
# Magic 1-5 en casa vs 6-4 fuera: ¿es real?
print('Fisher Magic casa 1-5 vs fuera 6-4 p',round(fisher_exact([[1,5],[6,4]])[1],3))
print('Fisher Pistons casa 3-3 vs fuera 7-3 p',round(fisher_exact([[3,3],[7,3]])[1],3))
# Magic: P(1 o menos de 6 en casa) si su prob. real en casa fuera la de un equipo de su nivel (Q + localía)
pc=norm.cdf((Q[h]+H)/SIG);print('Magic prob. por partido en casa (nivel promedio rival)',round(pc,3),'P(<=1 de 6)',round(binom.cdf(1,6,pc),3))
print('Pistons MOV hoy +4.8 (TeamRankings, 23 nov) récord esp 10.0 de 16; Magic MOV?')
