"""NFL semana 11, MNF lun 23 nov: CIN (7-2) en WAS (3-5-1), 19:15 CDMX. Sin nflverse (bloqueado en esta ejecución) → no hay EPA propia: Modelo NFL v0-b
= mismo esquema que v0 pero con diferencial de puntos por partido en lugar de EPA: margen local = 0.5 × (dif/pp local − dif/pp visita) + 1.5; P = Φ(margen/13.5).
Puntos: CIN 30.9 a favor / 21.4 en contra por partido (commanders.com, Fox Sports), WAS 196 / 223 (ESPN). Pase: CIN 298.8 yd/p (1°), WAS permite 244.8 (31°)
(commanders.com; Fox y ESPN coinciden en WAS). QBs: Burrow y Daniels titulares (Rotowire, Fox)."""
import numpy as np
from scipy.stats import norm, binom
cin=(9,30.9*9,21.4*9,7,2,0);was=(9,196,223,3,5,1)
dc=(cin[1]-cin[2])/9;dw=(was[1]-was[2])/9
mg=0.5*(dw-dc)+1.5;print(f'dif/pp CIN {dc:+.1f} WAS {dw:+.1f} | margen WAS {mg:+.1f} → P(CIN) {norm.cdf(-mg/13.5):.3f}')
# incertidumbre: error estándar del dif/pp ≈ 13.5/√9 por equipo; bootstrap normal
rng=np.random.default_rng(1123);N=200000;a=rng.normal(dc,13.5/3,N);b=rng.normal(dw,13.5/3,N);pp=norm.cdf(-(0.5*(b-a)+1.5)/13.5)
print('80%',np.percentile(pp,[10,90]).round(3))
for f in [0.3,0.7]: print('sens factor',f,'P(CIN)',round(norm.cdf(-(f*(dw-dc)+1.5)/13.5),3))
# Pitágoras NFL (exponente 2.37): victorias esperadas vs reales
for t,(n,pf,pa,w,l,ti) in [('CIN',cin),('WAS',was)]:
    pe=pf**2.37/(pf**2.37+pa**2.37);print(t,'pitag',round(pe,3),'esp',round(n*pe,1),'reales',w+ti/2,'P(>=W)',round(binom.sf(w-1,n,pe),3),'P(<=W)',round(binom.cdf(w,n,pe),3))
# Tensión: mejor pase vs 31° defensa contra el pase; promedio liga pase ~ 215 yd (NO VERIFICADO → no se usa)
print('total esperado (pts a favor/en contra promedio cruzado)',round(((30.9+24.8)/2+(21.8+21.4)/2),1))
