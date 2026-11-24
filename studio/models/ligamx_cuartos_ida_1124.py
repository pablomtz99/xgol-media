"""Liga MX Apertura 2026, cuartos de ida mié 25 nov: Toluca (5°) vs Atlas (4°) 19:00; Monterrey (6°) vs América (3°) 21:10 (Claro Sports 23/11).
Mismo Modelo xGol Liga MX v0 de ligamx_liguilla_1123.py (GF/GC tabla final J17). El mejor ubicado cierra en casa y avanza con empate global.
Monte Carlo 200,000: P(avanza), resultado de la ida y P(avanza | ida). Validación: no hay validación fuera de muestra propia en Liguilla (decirlo)."""
import numpy as np, io, contextlib, importlib.util, os
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'ligamx_j17_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
MU=m.MU
GF={'Chivas':(27,15),'Cruz Azul':(37,27),'América':(38,24),'Atlas':(30,33),'Toluca':(35,23),'Monterrey':(29,25),'León':(25,22),'Pachuca':(31,20)}
def tie(lo,hi,K=8,HADV=.35,N=200000,seed=1125):
    rng=np.random.default_rng(seed);r={t:(GF[t][0]-GF[t][1])/(17+K) for t in GF};b=2/MU;h=HADV/MU
    def leg(H,A):d=r[H]-r[A];return rng.poisson(MU/2*np.exp(b*d/2+h),N),rng.poisson(MU/2*np.exp(-b*d/2-h),N)
    x1,y1=leg(lo,hi);y2,x2=leg(hi,lo)  # ida en casa del peor ubicado (lo)
    adv=(y1+y2)>=(x1+x2);return x1,y1,adv
for lo,hi in [('Toluca','Atlas'),('Monterrey','América')]:
    x1,y1,adv=tie(lo,hi);pL=(x1>y1).mean();pE=(x1==y1).mean();pV=(x1<y1).mean()
    print(f'{lo}–{hi} ida L/E/V {pL:.3f}/{pE:.3f}/{pV:.3f} goles ida esp {(x1+y1).mean():.2f} | P({hi} avanza) {adv.mean():.3f}')
    for lab,msk in [(f'gana {lo} ida',x1>y1),('empate ida',x1==y1),(f'gana {hi} ida',x1<y1),(f'{lo} gana por 2+',x1-y1>=2)]:
        print('   ',lab,f'P={msk.mean():.3f}',f'P({hi} avanza | eso)={adv[msk].mean():.3f}')
    for K,HA in [(0,.35),(16,.35),(8,0),(8,.6)]:
        print('    sens K',K,'loc',HA,round(tie(lo,hi,K,HA,60000,7)[2].mean(),3))
# Atlas: 4° con diferencia −3 (30-33). ¿Puntos acordes a sus goles? Pitágoras futbol (exp 1.3) — 17 PJ
from scipy.stats import norm
for t,(pts,gf,ga) in {'Atlas':(30,30,33),'Toluca':(None,35,23),'Monterrey':(None,29,25),'América':(None,38,24)}.items():
    pe=gf**1.3/(gf**1.3+ga**1.3);print(t,'pitag %',round(pe,3),'pts esperados aprox (2.7*17*pe+...)',round(pe*17*2.75,1),'pts reales',pts)
