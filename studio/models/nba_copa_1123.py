"""NBA Cup martes 24 nov (fase de grupos): DET@ORL 18:00, BOS@WAS 19:00, DAL@DEN 21:00 CDMX. Modelo NBA v1 (SRS B-Ref hasta 18 nov; nba_srs_1119.py).
Récords hoy: landofbasketball + Sportbusy (BOS 11-6, WAS 7-11, DET 10-6, ORL 7-9, DAL 10-7, DEN 10-5). MOV hoy: TeamRankings (BOS +9.1, WAS −5.1, ...).
Ninguno juega el lunes → sin back-to-back. Bajas (Sportbusy): BOS sin George ni M. Robinson; ORL sin Banchero ni Isaac; DET sin Duren; DAL sin Washington ni Lively."""
import numpy as np, io, contextlib, importlib.util, os
from scipy.stats import norm, binom
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nba_srs_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S,Q,K,H,SIG,rk=m.S,m.Q,m.K,m.H,m.SIG,m.rk
rng=np.random.default_rng(1124);N=200000
for h,a in [('Magic','Pistons'),('Wizards','Celtics'),('Nuggets','Mavericks')]:
    mg=Q[h]-Q[a]+H;qh=rng.normal(Q[h],SIG/np.sqrt(sum(S[h][:2])+K),N);qa=rng.normal(Q[a],SIG/np.sqrt(sum(S[a][:2])+K),N);pp=norm.cdf((qh-qa+H)/SIG)
    print(f'{a}@{h} P(visita) {1-norm.cdf(mg/SIG):.3f} 80% {1-np.percentile(pp,90):.3f}-{1-np.percentile(pp,10):.3f} margen visita {-mg:+.1f} | Q {Q[a]:.2f}({rk[a]}) vs {Q[h]:.2f}({rk[h]})')
# Boston: récord vs margen (hoy 11-6, MOV +9.1, TeamRankings)
for t,w,l,mov in [('Celtics',11,6,9.1),('76ers',14,3,2.9),('Spurs',14,3,11.9),('Pistons',10,6,4.8),('Nuggets',10,5,1.8),('Wizards',7,11,-5.1)]:
    n=w+l;pg=norm.cdf(mov/SIG);print(t,f'{w}-{l} MOV {mov:+.1f} victorias esperadas {n*pg:.1f} P(<=W) {binom.cdf(w,n,pg):.3f} P(>=W) {binom.sf(w-1,n,pg):.3f}')
# Celtics: margen en derrotas (MOV alto con 6 derrotas → derrotas cerradas?) — sin datos juego a juego verificados: no se usa.
# Proyección récord final BOS: nivel Q con incertidumbre, 65 juegos restantes
q=rng.normal(Q['Celtics'],SIG/np.sqrt(15+K),N);pw=norm.cdf(q/SIG);w=11+rng.binomial(65,pw);print('BOS victorias finales',w.mean().round(1),np.percentile(w,[10,90]),'ritmo récord',round(11/17*82,1))
