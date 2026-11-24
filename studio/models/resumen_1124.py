"""Resumen lun 23 nov: 2 partidos con probabilidad fijada ANTES (portadas_1123 ideas 1-2, commit 2620921; no publicadas: sin aprobación).
Resultados: Commanders 22-20 Bengals (NFL.com, NBC Sports; gol de campo de 26 yardas de Drew Stevens, su 5°, en la última jugada tras el 56 de McPherson a 46 s);
Spurs 123-107 Kings sin Wembanyama ni Fox (ESPN recap y nota, Sky Sports, Yahoo)."""
import numpy as np
from scipy.stats import norm
pb=np.array([.638,.855]);yb=np.array([0.,1.])
print('aciertos',int(yb.sum()),'esperados',pb.sum().round(2),'P(<=1)',round(1-pb.prod(),3))
b=(pb-yb)**2;print('Brier',b.round(3),'media',b.mean().round(3))
rng=np.random.default_rng(1124);Y=rng.random((200000,2))<pb;B=((pb-Y)**2).mean(1)
print('Brier esperado',B.mean().round(3),'80%',np.percentile(B,[10,90]).round(3),'P(>=obs)',(B>=b.mean()).mean().round(3))
# Spurs: escenario sin Wembanyama ni Fox (76%), margen esperado completo +15.6; real +16
print('SAS margen esperado +15.6 (con todos) real +16; escenario sin ambos: 76%')
# CIN: 64%, perdió por 2 con FG en la última jugada; margen esperado CIN +4.7, real −2 → error 6.7 pts vs σ 13.5: z
print('CIN error de margen',-2-4.7,'z',round((-2-4.7)/13.5,2),'P(|z|>=)',round(2*norm.sf(6.7/13.5),3))
