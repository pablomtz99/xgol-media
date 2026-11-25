"""Liga MX Apertura 2026, cuartos de ida jue 26 nov: Pachuca (8°) vs Chivas (1°) 19:00, Estadio Hidalgo; León (7°) vs Cruz Azul (2°) 21:10, Estadio León (ESPN 23/11).
Mismo Modelo xGol Liga MX v0 (ligamx_j17_1119.py). Base: ligamx_cuartos_ida_1124.py. Sin validación propia en Liguilla."""
import numpy as np, io, contextlib, importlib.util, os
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'ligamx_j17_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
MU=m.MU
GF={'Chivas':(27,15),'Cruz Azul':(37,27),'América':(38,24),'Atlas':(30,33),'Toluca':(35,23),'Monterrey':(29,25),'León':(25,22),'Pachuca':(31,20)}
def tie(lo,hi,K=8,HADV=.35,N=200000,seed=1126):
    rng=np.random.default_rng(seed);r={t:(GF[t][0]-GF[t][1])/(17+K) for t in GF};b=2/MU;h=HADV/MU
    def leg(H,A):d=r[H]-r[A];return rng.poisson(MU/2*np.exp(b*d/2+h),N),rng.poisson(MU/2*np.exp(-b*d/2-h),N)
    x1,y1=leg(lo,hi);y2,x2=leg(hi,lo)  # ida en casa del peor ubicado (lo)
    adv=(y1+y2)>=(x1+x2);return x1,y1,adv
for lo,hi in [('Pachuca','Chivas'),('León','Cruz Azul')]:
    x1,y1,adv=tie(lo,hi);pL=(x1>y1).mean();pE=(x1==y1).mean();pV=(x1<y1).mean()
    print(f'{lo}–{hi} ida L/E/V {pL:.3f}/{pE:.3f}/{pV:.3f} goles ida esp {(x1+y1).mean():.2f} | P({hi} avanza) {adv.mean():.3f}')
    for lab,msk in [(f'gana {lo} ida',x1>y1),('empate ida',x1==y1),(f'gana {hi} ida',x1<y1),(f'{lo} gana por 2+',x1-y1>=2)]:
        print('   ',lab,f'P={msk.mean():.3f}',f'P({hi} avanza | eso)={adv[msk].mean():.3f}')
    for K,HA in [(0,.35),(16,.35),(8,0),(8,.6)]:
        print('    sens K',K,'loc',HA,round(tie(lo,hi,K,HA,60000,7)[2].mean(),3))
# Atlas: 4° con diferencia −3 (30-33). ¿Puntos acordes a sus goles? Pitágoras futbol (exp 1.3) — 17 PJ
from scipy.stats import norm
for t,(pts,gf,ga) in {'Chivas':(None,27,15),'Pachuca':(None,31,20),'Cruz Azul':(None,37,27),'León':(None,25,22)}.items():
    pe=gf**1.3/(gf**1.3+ga**1.3);print(t,'pitag %',round(pe,3),'pts esperados aprox (2.7*17*pe+...)',round(pe*17*2.75,1),'pts reales',pts)
