"""Thunder doble jornada: dom 22 en Miami (18:00 ET = 17:00 CDMX) y lun 23 en Indiana (19:30 ET = 18:30 CDMX; ambos equipos en back-to-back).
Modelo NBA v1 (SRS B-Ref hasta 18 nov). Récords hoy (Fox Sports/StatMuse 22 nov): OKC 10-6, MIA 9-6, IND 5-11. Back-to-back −2.1 (lab xGol, p = 0.011).
MIA jugó el sábado? → ver contexto; aquí MIA sin ajuste (no aparece en el domingo previo; verificar)."""
import numpy as np, io, contextlib, importlib.util, os
from scipy.stats import norm
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nba_srs_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S,Q,K,H,SIG,rk=m.S,m.Q,m.K,m.H,m.SIG,m.rk
rng=np.random.default_rng(1122);N=400000
q={t:rng.normal(Q[t],SIG/np.sqrt(sum(S[t][:2])+K),N) for t in ['Thunder','Heat','Pacers']}
m1=q['Thunder']-q['Heat']-H; m2=q['Thunder']-q['Pacers']-H  # OKC visitante; IND y OKC ambos b2b → se cancela
p1=norm.cdf(m1/SIG);p2=norm.cdf(m2/SIG)
x1=rng.random(N)<p1;x2=rng.random(N)<p2
print('P(OKC en MIA)',round(norm.cdf((Q['Thunder']-Q['Heat']-H)/SIG),3),'80%',np.percentile(p1,[10,90]).round(3),'margen',round(Q['Thunder']-Q['Heat']-H,1))
print('P(OKC en IND)',round(norm.cdf((Q['Thunder']-Q['Pacers']-H)/SIG),3),'80%',np.percentile(p2,[10,90]).round(3),'margen',round(Q['Thunder']-Q['Pacers']-H,1))
print('P(gana ambos)',round((x1&x2).mean(),3),'P(pierde ambos)',round((~x1&~x2).mean(),3),'P(1 de 2)',round((x1^x2).mean(),3))
# ¿bajón real? H0: nivel = prior 2025-26 (90% de nivel por victorias: 7.67). SRS 5.79 con ee σ/√n
n=15;z=(S['Thunder'][4]-7.67)/(SIG/np.sqrt(n));print('OKC SRS vs nivel previo z',round(z,2),'p',round(2*norm.sf(abs(z)),3))
# tamaño del efecto en victorias por 82 juegos: Φ(Q/σ) aprox vs equipo promedio
print('ritmo de victorias por nivel Q',round(82*norm.cdf(Q['Thunder']/SIG),1),'| por SRS actual',round(82*norm.cdf(5.79/SIG),1),'| por nivel previo',round(82*norm.cdf(7.67/SIG),1),'| ritmo récord 10-6',round(82*10/16,1))
print('Heat Q',round(Q['Heat'],2),'rank',rk['Heat'],'S',S['Heat'],'| OKC rank',rk['Thunder'],'| IND rank',rk['Pacers'])
