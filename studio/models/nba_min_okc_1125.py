"""NBA mié 25 nov: Timberwolves (13-5) en Thunder (10-8), 18:30 CDMX. Modelo NBA v1 (SRS B-Ref al 18-19 nov + prior; nba_srs_1119.py).
Bajas (KFAN/iHeart 25 nov; Sportsmole): OKC fuera Holmgren, Jalen Williams, Cason Wallace, Sorber; Caruso día a día. MIN fuera Edwards, DiVincenzo, J. Clark.
Récords: Sportsmole 25 nov. El modelo no ve bajas → escenarios."""
import numpy as np, io, contextlib, importlib.util, os
from scipy.stats import norm, binomtest
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nba_srs_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S,Q,K,H,SIG,rk,W25=m.S,m.Q,m.K,m.H,m.SIG,m.rk,m.W25
h,a='Thunder','Timberwolves';mg=Q[h]-Q[a]+H;p=norm.cdf(mg/SIG)
rng=np.random.default_rng(1125);N=200000
qh=rng.normal(Q[h],SIG/np.sqrt(sum(S[h][:2])+K),N);qa=rng.normal(Q[a],SIG/np.sqrt(sum(S[a][:2])+K),N);pp=norm.cdf((qh-qa+H)/SIG)
print(f'P(OKC) {p:.3f} 80% {np.percentile(pp,10):.3f}-{np.percentile(pp,90):.3f} margen OKC {mg:+.1f} | Q OKC {Q[h]:.2f} ({rk[h]}) MIN {Q[a]:.2f} ({rk[a]})')
print('SRS 2026-27 OKC',S[h][4],'MIN',S[a][4],'| 2025-26 victorias OKC',W25[h],'MIN',W25[a])
for d,lab in [(0,'ambos completos (modelo)'),(-4,'OKC sin Holmgren y J. Williams (aprox −4)'),(-4+3,'… y MIN sin Edwards (aprox +3)'),(-6+3,'peor caso OKC −6, MIN −3')]:
    print(lab,round(norm.cdf((mg+d)/SIG),3))
# Thunder: campeón 2025 con 64 victorias, hoy 10-8. ¿Caída real o azar? Con nivel previo (prior 90%) esperado por partido:
q0=0.9*(W25[h]-41)/2.7;pg=norm.cdf(q0/SIG);print('OKC prob por partido con nivel 2025-26 (90%)',round(pg,3),'P(<=10 de 18)',round(binomtest(10,18,pg,alternative='less').pvalue,4))
pg2=norm.cdf(S[h][4]/SIG);print('OKC prob por partido con SRS actual',round(pg2,3))
# MIN 13-5 con MOV 10.6 (1 de los 3 mejores márgenes)
print('MIN MOV',S[a][2],'SOS',S[a][3],'| OKC MOV',S[h][2],'SOS',S[h][3])
