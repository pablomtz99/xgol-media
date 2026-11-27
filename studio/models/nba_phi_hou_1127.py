"""NBA sáb 28 nov: 76ers (15-4) en Rockets (14-5), 19:30 CDMX (calendario NBA, PDF ago; récords ESPN 27 nov). PHI juega vie 27 en IND → back-to-back.
Modelo NBA v1 (versión SRS, nba_srs_1119.py): hoy B-Ref no cargó → calidad = MOV actual (ESPN, 27 nov) + SOS de B-Ref al 19 nov (último dato verificado);
prior 90% de 2025-26, K=16, local +2.0, σ=14.7. Back-to-back −2.1 al margen (lab xgol-data, p=0.011). Ratings ofensivo/defensivo y ritmo: StatMuse.
Lesiones (ESPN 22–26 nov): PHI Embiid duda, J. Brown fuera (regreso est. 28 nov), Hukporti fuera. HOU: no verificadas."""
import numpy as np, io, contextlib, importlib.util
from scipy.stats import norm, binom
spec=importlib.util.spec_from_file_location('m','studio/models/nba_srs_1119.py')
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
NOW={'76ers':(15,4,2.2),'Rockets':(14,5,8.1)}
K,H,SIG,B2B=16,2.0,14.7,-2.1
def q(t):w,l,mov=NOW[t];n=w+l;srs=mov+m.S[t][3];return (n*srs+K*0.9*(m.W25[t]-41)/2.7)/(n+K),n,srs
qh,nh,sh=q('Rockets');qa,na,sa=q('76ers')
for b2b,lab in [(0,'sin descanso'),(B2B,'con back-to-back PHI')]:
    mg=qh-qa+H-b2b;print(lab,'margen HOU',round(mg,1),'P(HOU)',round(norm.cdf(mg/SIG),3))
mg=qh-qa+H-B2B;rng=np.random.default_rng(1127);N=200000
p=norm.cdf((rng.normal(qh,SIG/np.sqrt(nh+K),N)-rng.normal(qa,SIG/np.sqrt(na+K),N)+H-B2B)/SIG);print('80%',np.percentile(p,[10,90]).round(3))
for d,lab in [(+3,'PHI sin Embiid (aprox +3 HOU)'),(-1.5,'PHI con Brown de vuelta (aprox −1.5)')]:print(lab,round(norm.cdf((mg+d)/SIG),3))
print('SRS aprox HOU',round(sh,2),'PHI',round(sa,2))
# 76ers: récord vs diferencial (Pitágoras NBA exp 14)
for t,w,l,pf,pa in [('76ers',15,4,115.1,112.9),('Rockets',14,5,118.0,109.9)]:
    py=pf**14/(pf**14+pa**14);n=w+l;print(t,f'pitag {py:.3f} -> {py*n:.1f} de {n}; P(>={w}) = {binom.sf(w-1,n,py):.3f}')
# regresión: del lab, arranque predice ~27% del margen futuro (r=0.40) → récord futuro esperado de PHI
py=115.1**14/(115.1**14+112.9**14);print('PHI ritmo 82 con récord',round(15/19*82),'con pitágoras resto',round(15+py*63))
