"""Liga MX Apertura 2026 cuartos, vuelta dom 29 nov: Chivas (1°, 33 pts) vs Pachuca (8°, 25) 19:07 Estadio Akron (ida 1-2); Cruz Azul vs León 21:00 Azteca (ida 4-0).
Horarios: Latinus, ClaroSports, Azteca Jalisco. Desempate: global empatado → mejor ubicado (ClaroSports, TUDN). Idrissi suspendido (365Scores, ESPN).
Modelo xGol Liga MX v0 (ligamx_j17_1119.py; GF/GC del torneo, K=8, localía +0.35). El modelo no ve la baja de Idrissi."""
import numpy as np, io, contextlib, importlib.util
from scipy.stats import fisher_exact, chi2_contingency
spec=importlib.util.spec_from_file_location('m','studio/models/ligamx_j17_1119.py')
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
MU=m.MU;GF={'Chivas':(27,15),'Pachuca':(31,20),'Cruz Azul':(37,27),'León':(25,22)}
rng=np.random.default_rng(1129);N=400000
def leg(H,A,K=8,HADV=.35,att=1.0):
    r={t:(GF[t][0]-GF[t][1])/(17+K) for t in GF};b=2/MU;h=HADV/MU;d=r[H]-r[A]
    return rng.poisson(MU/2*np.exp(b*d/2+h),N),rng.poisson(MU/2*np.exp(-b*d/2-h)*att,N)
x,y=leg('Chivas','Pachuca');d=x-y
print(f'goles esp Chivas {x.mean():.2f} Pachuca {y.mean():.2f}')
print('Chivas gana vuelta (avanza)',(d>=1).mean().round(3),'| empate',(d==0).mean().round(3),'| Pachuca gana',(d<0).mean().round(3))
print('Chivas gana por exactamente 1',(d==1).mean().round(3),'por 2+',(d>=2).mean().round(3),'| Chivas sin recibir',(y==0).mean().round(3),'| 0-0',((x==0)&(y==0)).mean().round(3))
for K,HA in [(0,.35),(16,.35),(8,0),(8,.6)]:
    a,b=leg('Chivas','Pachuca',K,HA);print('  sens K',K,'loc',HA,((a-b)>=1).mean().round(3))
a,b=leg('Chivas','Pachuca',att=0.85);print('  escenario sin Idrissi (Pachuca −15% goles, supuesto)',((a-b)>=1).mean().round(3))
# incertidumbre del nivel: remuestreo Poisson de GF/GC
P=[]
for i in range(2000):
    g={t:(rng.poisson(v[0]),rng.poisson(v[1])) for t,v in GF.items()};r={t:(g[t][0]-g[t][1])/25 for t in g};b=2/MU;dd=r['Chivas']-r['Pachuca']
    l1=MU/2*np.exp(b*dd/2+.35/MU);l2=MU/2*np.exp(-b*dd/2-.35/MU);xx=rng.poisson(l1,20000);yy=rng.poisson(l2,20000);P.append(((xx-yy)>=1).mean())
print('80% Chivas avanza',np.percentile(P,[10,90]).round(3))
# Chivas local 6-1-2 (El Futbolero 5-1-2 antes de J17 + 1-0 a Cruz Azul) vs visitante 3-5-0 (Récord): ¿rinde distinto?
print('Chivas pts/partido local',round(19/9,2),'visita',round(14/8,2),'| chi2 G-E-P p',round(chi2_contingency([[6,1,2],[3,5,0]])[1],3),'| Fisher ganar vs no ganar p',round(fisher_exact([[6,3],[3,5]])[1],3))
a,b=leg('Cruz Azul','León');print('León gana por 5+',((b-a)>=5).mean().round(4),'| Cruz Azul avanza',1-((b-a)>=5).mean().round(4))
