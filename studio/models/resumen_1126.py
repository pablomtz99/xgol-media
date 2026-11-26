"""Resumen mié 25 nov: 12 partidos con probabilidad fijada ANTES (portadas_1124 ideas 2 y 3 — UCL J5 miércoles (9, ucl_j5_mie_1124.py) y Liga MX cuartos ida
(ligamx_cuartos_ida_1124.py); portadas_1125 idea 2 MIN@OKC (53% con bajas) e idea 4 Sporting–Man Utd; no publicadas: sin aprobación).
Resultados (leídos 26 nov): UCL — Yahoo Sports y Sporting Tribune (coinciden en los 9): Sabah 1-4 Barcelona, Slavia 0-1 Villarreal, Atlético 2-0 Viking,
Brugge 0-3 Liverpool, Inter 2-0 Stuttgart, Lille 2-1 Bayern, PSG 2-2 Roma, Shakhtar 0-1 Fenerbahçe, Sporting 2-2 Man Utd.
Liga MX — Toluca 2-0 Atlas (La Silla Rota, En Juego); Monterrey 0-0 América (365Scores, En Juego; MTY con 10). NBA — MIN 113-106 OKC (ESPN/AP, VAVEL). Ejecutar desde la raíz."""
import numpy as np, io, contextlib, importlib.util
F=[("Sabah","Barcelona",.051,.084,.865,2),("Slavia","Villarreal",.419,.208,.373,2),("Atlético","Viking",.830,.105,.065,0),
   ("Club Brugge","Liverpool",.465,.194,.341,2),("Inter","Stuttgart",.729,.153,.118,0),("Lille","Bayern",.259,.201,.539,0),
   ("PSG","Roma",.755,.128,.117,1),("Shakhtar","Fenerbahçe",.564,.208,.228,2),("Sporting","Man Utd",.556,.207,.238,1),
   ("Toluca","Atlas",.595,.209,.196,0),("Monterrey","América",.368,.243,.389,1)]
P=np.array([f[2:5] for f in F]);r=np.array([f[5] for f in F]);O=np.eye(3)[r]
fav=P.argmax(1);hf=fav==r;pnba=.53;ynba=0.
allp=np.r_[P.max(1),pnba];hits=np.r_[hf,[False]]
print('aciertos',int(hits.sum()),'de',len(allp),'esperados',allp.sum().round(2),'| UCL',int(hf[:9].sum()),'de 9 esp',P[:9].max(1).sum().round(2))
d=np.array([1.])
for q in allp:d=np.convolve(d,[1-q,q])
print('P(<=4 de 12)',d[:5].sum().round(4),'| dist',d.round(3))
dU=np.array([1.])
for q in P[:9].max(1):dU=np.convolve(dU,[1-q,q])
print('UCL P(<=3 de 9)',dU[:4].sum().round(4),'= P(>=6 sorpresas)')
bf=((P-O)**2).sum(1);print('Brier por partido',dict(zip([f[0] for f in F],bf.round(2))))
print('Brier UCL',bf[:9].mean().round(3),'LigaMX',bf[9:].mean().round(3),'futbol 11',bf.mean().round(3),'uniforme 0.667 | NBA',(pnba-ynba)**2)
rng=np.random.default_rng(1126);N=200000
def sim(Pm):
    U=rng.random((N,len(Pm)));R=(U[:,:,None]>np.cumsum(Pm,1)[None,:,:2]).sum(2);return R,((Pm[None]-np.eye(3)[R])**2).sum(2).mean(1)
R9,B9=sim(P[:9]);print('Brier UCL esperado',B9.mean().round(3),'80%',np.percentile(B9,[10,90]).round(3),'P(>=obs)',(B9>=bf[:9].mean()).mean().round(4))
R11,B11=sim(P);print('Brier futbol esperado',B11.mean().round(3),'P(>=obs)',(B11>=bf.mean()).mean().round(4))
# visitantes ganan: 4 de 9 en UCL (Barcelona, Villarreal, Liverpool, Fenerbahçe); empates 2
print('UCL locales/empates/visitas real',[(r[:9]==k).sum() for k in range(3)],'esperado',P[:9].sum(0).round(2))
# calibración por tramos de probabilidad asignada a CADA resultado (33 + 2 eventos)
pr=np.r_[P.ravel(),[pnba,1-pnba]];oc=np.r_[O.ravel(),[0,1]]
for lo,hi in [(0,.25),(.25,.5),(.5,1.01)]:
    m=(pr>=lo)&(pr<hi);print(f'tramo {lo:.2f}-{hi:.2f}: n={m.sum()} prob media {pr[m].mean():.2f} ocurrió {oc[m].mean():.2f} ({int(oc[m].sum())})')
# Liguilla: condicional exacto a la ida
spec=importlib.util.spec_from_file_location('m','studio/models/ligamx_j17_1119.py')
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
MU=m.MU;GF={'Atlas':(30,33),'Toluca':(35,23),'Monterrey':(29,25),'América':(38,24)}
def vuelta(lo,hi,g_lo,g_hi,K=8,HADV=.35,N=400000):
    rr={t:(GF[t][0]-GF[t][1])/(17+K) for t in GF};b=2/MU;h=HADV/MU;dd=rr[hi]-rr[lo]
    y2=rng.poisson(MU/2*np.exp(b*dd/2+h),N);x2=rng.poisson(MU/2*np.exp(-b*dd/2-h),N);return ((g_hi+y2)>=(g_lo+x2)).mean()
print('Toluca avanza tras 2-0 (antes 61.2%)',round(1-vuelta('Toluca','Atlas',2,0),3))  # vuelta en casa de Atlas (4°), que avanza con global empatado
print('América avanza tras 0-0 (antes 70.4%)',round(vuelta('Monterrey','América',0,0),3))
from scipy.stats import norm
print('OKC margen esperado',round(norm.ppf(.53)*14.7,1),'real -7; base sin bajas',round(norm.ppf(.556)*14.7,1))
