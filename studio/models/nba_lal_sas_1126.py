"""NBA Cup vie 27 nov: Lakers (15-3) en Spurs (15-4), Frost Bank Center, 20:30 CDMX (Sportsmole: 2:30 GMT sáb). Modelo NBA v1 (SRS B-Ref al 19 nov + prior; nba_srs_1119.py).
Contexto (Sportsmole 26 nov; Sporting News 25 nov): Wembanyama (espalda) y Fox (espinilla) duda de último momento; Reaves (talón) duda; SAS sin Harper, Harris, Quaintance.
Diferencial por partido (Sportsmole): LAL +3.4 (112.2 a favor), SAS +6.8 (113.0). LAL 7-1 de visita, SAS 7-3 en casa. Mercado: SAS −6.5 (Newsminimalist) → no se muestra."""
import numpy as np, io, contextlib, importlib.util
from scipy.stats import norm, binomtest
spec=importlib.util.spec_from_file_location('m','studio/models/nba_srs_1119.py')
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p,mg=m.P('Spurs','Lakers');lo,hi=m.PI('Spurs','Lakers');print(f'P(SAS) {p:.3f} 80% {lo:.3f}-{hi:.3f} margen {mg:+.1f}')
for d,lab in [(0,'completos'),(-4,'sin Wembanyama (aprox −4)'),(-5.5,'sin Wembanyama ni Fox (aprox −5.5)'),(+1.5,'LAL sin Reaves (aprox +1.5 SAS)')]:print(lab,round(norm.cdf((mg+d)/m.SIG),3))
# Lakers: récord vs diferencial (Pitágoras NBA exp 14 y vía margen)
for t,w,l,pf,dif in [('Lakers',15,3,112.2,3.4),('Spurs',15,4,113.0,6.8)]:
    pa=pf-dif;py=pf**14/(pf**14+pa**14);pm=norm.cdf(dif/m.SIG*1.0)
    n=w+l;print(t,f'pitag {py:.3f} -> {py*n:.1f} victorias esperadas de {n} (real {w}); P(>= {w}) = {1-binomtest(w,n,py).pvalue if False else sum(__import__("scipy.stats",fromlist=["binom"]).binom.pmf(k,n,py) for k in range(w,n+1)):.3f}')
# regresión: ritmo de 82 con récord vs con pitágoras
py=112.2**14/(112.2**14+108.8**14);print('LAL proyección 82 con récord',round(15/18*82),'con pitágoras',round(15+py*64))
