"""HOU@DEN (vie 20 nov, NBA Cup, 21:00 CDMX aprox.). Cuatro factores: Basketball-Reference (tabla avanzada, hasta mié 18; resumen del sitio, verificado W-L/SRS).
Prueba: ¿el rebote ofensivo de Houston es real? Proporción vs promedio liga, con ~44 oportunidades de rebote ofensivo por partido (supuesto aprox.)."""
import numpy as np
from scipy.stats import norm
ORB={'SAS':29.3,'BOS':30.5,'MIN':30.0,'HOU':33.2,'MEM':29.8,'DET':27.3,'NYK':31.2,'LAL':29.4,'POR':27.4,'OKC':26.0,'PHI':22.9,'CLE':26.7,'ATL':28.6,'DEN':25.1,'GSW':28.8,
'MIA':24.4,'TOR':29.2,'DAL':28.7,'PHX':26.0,'IND':21.3,'ORL':25.7,'LAC':23.9,'WAS':24.6,'NOP':25.1,'UTA':25.3,'CHI':28.2,'BKN':27.2,'CHA':32.7,'MIL':28.6,'SAC':22.9}
DRB={'SAS':76.0,'BOS':71.6,'MIN':73.9,'HOU':72.8,'MEM':73.4,'DET':71.0,'NYK':76.4,'LAL':69.3,'POR':74.3,'OKC':74.1,'PHI':75.0,'CLE':73.9,'ATL':73.7,'DEN':69.8,'GSW':71.7,
'MIA':72.2,'TOR':71.6,'DAL':70.9,'PHX':68.4,'IND':73.2,'ORL':76.1,'LAC':71.4,'WAS':69.0,'NOP':72.8,'UTA':74.6,'CHI':69.4,'BKN':72.4,'CHA':77.3,'MIL':68.9,'SAC':74.8}
avg=np.mean(list(ORB.values()));print('ORB liga',round(avg,1),'DRB liga',round(np.mean(list(DRB.values())),1))
rk=lambda d,t,rev=True: sorted(d,key=d.get,reverse=rev).index(t)+1
print('HOU ORB rank',rk(ORB,'HOU'),'DEN DRB rank (de mejor a peor)',rk(DRB,'DEN'),'de 30')
n=16*44;p0=avg/100;z=(0.332-p0)/np.sqrt(p0*(1-p0)/n);print('HOU z',round(z,2),'p',2*norm.sf(z))
nd=13*44;q0=1-p0;zd=(0.698-q0)/np.sqrt(q0*(1-q0)/nd);print('DEN DRB z',round(zd,2),'p',2*norm.sf(abs(zd)))
# rebote ofensivo esperado de HOU en este duelo (log5 simple)
oh,dd=0.332,1-0.698;exp=oh*dd/p0/(oh*dd/p0+(1-oh)*(1-dd)/(1-p0));print('ORB% esperado HOU vs DEN',round(exp,3))
print('extra rebotes ofensivos por partido vs promedio:',round((exp-p0)*44,1))
