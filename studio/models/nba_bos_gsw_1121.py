"""BOS@GSW (dom 22 nov, 19:30 CDMX). Modelo NBA v1 (SRS de Basketball-Reference hasta mié 18; nba_srs_1119.py) + ajuste de back-to-back de Boston
(−2.1 pts al margen; laboratorio xGol NBA 2025-26, p = 0.011). Boston juega el sábado en Sacramento (calendario NBA). Bajas GSW (ESPN, 20 nov):
Curry fuera (oblicuo, ~12 dic), Butler fuera (ligamento cruzado), Porziņģis fuera (ausente del equipo), Moody fuera; Green día a día. El modelo no ve bajas."""
import numpy as np, io, contextlib, importlib.util, os
from scipy.stats import norm
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nba_srs_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S,Q,K,H,SIG,rk=m.S,m.Q,m.K,m.H,m.SIG,m.rk
h,a='Warriors','Celtics';B2B=2.1
for lab,adj in [('sin ajuste',0),('con back-to-back BOS',B2B)]:
    mg=Q[h]-Q[a]+H+adj;p=norm.cdf(mg/SIG)
    rng=np.random.default_rng(1121);N=200000;n1,n2=sum(S[h][:2]),sum(S[a][:2])
    qh=rng.normal(Q[h],SIG/np.sqrt(n1+K),N);qa=rng.normal(Q[a],SIG/np.sqrt(n2+K),N);bb=rng.normal(adj,0.8 if adj else 0,N)
    pp=norm.cdf((qh-qa+H+bb)/SIG);print(lab,'P(GSW)',round(p,3),'80%',np.percentile(pp,[10,90]).round(3),'margen GSW',round(mg,1))
print('Q',{t:round(Q[t],2) for t in (h,a)},'rank',rk[h],rk[a],'S',S[h],S[a])
# sensibilidad: cuántos puntos de bajas harían falta para cambiar al favorito; y escenario de -3/-5 por bajas
for inj in [0,3,5]:
    mg=Q[h]-Q[a]+H+B2B-inj;print('bajas GSW -',inj,'P(GSW)',round(norm.cdf(mg/SIG),3),'margen',round(mg,1))
# Prueba: ¿el MOV de Boston (+10.5) es real o calendario? SRS = MOV + SOS: SOS −2.94 (rivales flojos). Z del MOV ajustado vs 0
n=sum(S[a][:2]);z=S[a][4]/(SIG/np.sqrt(n));print('BOS SRS z',round(z,2),'p',round(2*norm.sf(z),4),'n',n)
# regresión a la media: margen esperado resto de temporada = Q (mezcla) vs MOV crudo
print('BOS MOV',S[a][2],'SRS',S[a][4],'Q (encogido)',round(Q[a],2),'→ encogimiento',round(1-Q[a]/S[a][2],2))
