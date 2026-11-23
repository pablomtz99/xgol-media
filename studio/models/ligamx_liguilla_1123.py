"""Liguilla Apertura 2026 (cuartos ida 25-26 nov, vuelta 28-29; semis 2-3 y 5-6 dic). Sin play-in. Tabla final J17: 88.9 Noticias, El Imparcial (pts, dif);
GF-GC = ESPN tras J16 + resultados J17 (cuadran con las diferencias publicadas). Modelo xGol Liga MX v0 (ligamx_j17_1119.py): fuerza = dif. de goles encogida
(K=8 partidos de 0), Poisson, localía +0.35. Reglas: ida y vuelta, el mejor ubicado cierra en casa y avanza con empate global; semis re-sembradas;
final: empate global → tiempo extra (1/3 de goles) y penales 50/50. Histórico: superlíder campeón 13 de 59 torneos cortos (Claro Sports 21/05/2026 + Clausura 2026);
eliminado en cuartos 22 de 59 (Excélsior 25/11/2025: 22 de 57; AP25 y CL26 sin casos)."""
import numpy as np, io, contextlib, importlib.util, os
from scipy.stats import binomtest
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'ligamx_j17_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
MU=m.MU
SEED=['Chivas','Cruz Azul','América','Atlas','Toluca','Monterrey','León','Pachuca']
GF={'Chivas':(27,15),'Cruz Azul':(37,27),'América':(38,24),'Atlas':(30,33),'Toluca':(35,23),'Monterrey':(29,25),'León':(25,22),'Pachuca':(31,20)}
def run(K=8,HADV=0.35,N=200000,seed=1123):
    rng=np.random.default_rng(seed);r={t:(GF[t][0]-GF[t][1])/(17+K) for t in SEED};b=2/MU;h=HADV/MU
    def leg(H,A):
        d=r[H]-r[A];return rng.poisson(MU/2*np.exp(b*d/2+h),N),rng.poisson(MU/2*np.exp(-b*d/2-h),N)
    def tie(hi,lo,final=False):  # hi = mejor ubicado (vuelta en casa); arrays de índices por simulación
        out=np.empty(N,dtype=object)
        # vectorizar por par único
        res=np.zeros(N,bool)
        for x in set(zip(hi,lo)):
            msk=(hi==x[0])&(lo==x[1])
            if not msk.any(): continue
            a1,b1=leg(SEED[x[1]],SEED[x[0]]);b2,a2=leg(SEED[x[0]],SEED[x[1]])  # ida en casa del peor
            g_hi=b1+b2;g_lo=a1+a2
            if final:
                d=r[SEED[x[0]]]-r[SEED[x[1]]];e1=rng.poisson(MU/6*np.exp(b*d/2+h),N);e2=rng.poisson(MU/6*np.exp(-b*d/2-h),N)
                pen=rng.random(N)<.5;win=(g_hi>g_lo)|((g_hi==g_lo)&((e1>e2)|((e1==e2)&pen)))
            else: win=g_hi>=g_lo
            res[msk]=win[msk]
        return np.where(res,hi,lo)
    qf=[(0,7),(1,6),(2,5),(3,4)];w=[tie(np.full(N,a),np.full(N,c)) for a,c in qf]
    W=np.stack(w,1);W.sort(1)  # re-sembrar: 1° vs 4°, 2° vs 3° entre semifinalistas
    s1=tie(W[:,0],W[:,3]);s2=tie(W[:,1],W[:,2])
    hi=np.minimum(s1,s2);lo=np.maximum(s1,s2);ch=tie(hi,lo,final=True)
    semi={t:np.isin(i,W).mean() if False else (W==i).any(1).mean() for i,t in enumerate(SEED)}
    fin={t:((s1==i)|(s2==i)).mean() for i,t in enumerate(SEED)};camp={t:(ch==i).mean() for i,t in enumerate(SEED)}
    return semi,fin,camp
semi,fin,camp=run()
for t in SEED: print(f'{t:10s} semis {semi[t]:.3f} final {fin[t]:.3f} campeón {camp[t]:.3f}')
for K,HA in [(0,.35),(16,.35),(8,0),(8,.6)]:
    s,f,c=run(K,HA,N=60000,seed=7);print('sens',K,HA,'Chivas camp',round(c['Chivas'],3),'semis',round(s['Chivas'],3),'| Pachuca semis',round(s['Pachuca'],3),'| máx camp',max(c,key=c.get),round(max(c.values()),3))
print('MU',round(MU,3))
bt=binomtest(13,59,1/8,alternative='greater');print('superlíder campeón 13/59 =',round(13/59,3),'vs 1/8: p',round(bt.pvalue,4),'IC95',[round(x,3) for x in bt.proportion_ci(0.95)])
bt2=binomtest(22,59,1/2);print('eliminado en cuartos 22/59 =',round(22/59,3),'vs 1/2 p',round(bt2.pvalue,3))
