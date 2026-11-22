"""NBA lunes 23 nov: POR@PHI (19:00 ET = 18:00 CDMX) y OKC@IND (19:30 ET = 18:30 CDMX). Modelo NBA v1 (SRS B-Ref hasta 18 nov; nba_srs_1119.py).
Récords actuales (Fox Sports y StatMuse, 22 nov): PHI 14-3, POR 10-6, OKC 10-6, IND 5-11. Calendario (nbacalendar): OKC en MIA y IND en NYK el domingo 22 → ambos en back-to-back.
POR y PHI: el domingo no juegan (lista de 7 juegos del domingo) → sin back-to-back."""
import numpy as np, io, contextlib, importlib.util, os
from scipy.stats import norm, binom
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nba_srs_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S,Q,K,H,SIG,rk=m.S,m.Q,m.K,m.H,m.SIG,m.rk
def pi(h,a,adj=0,N=200000,seed=1122):
    rng=np.random.default_rng(seed);n1,n2=sum(S[h][:2]),sum(S[a][:2])
    qh=rng.normal(Q[h],SIG/np.sqrt(n1+K),N);qa=rng.normal(Q[a],SIG/np.sqrt(n2+K),N);pp=norm.cdf((qh-qa+H+adj)/SIG);return np.percentile(pp,[10,90])
for h,a in [('76ers','Trail Blazers'),('Pacers','Thunder')]:
    mg=Q[h]-Q[a]+H;print(h,'vs',a,'P(local)',round(norm.cdf(mg/SIG),3),'80%',pi(h,a).round(3),'margen local',round(mg,1),'| Q',round(Q[h],2),round(Q[a],2),'rank',rk[h],rk[a],'S',S[h],S[a])
# 76ers: récord vs calidad. Con MOV 2.94 en 16 juegos (al 18 nov): victorias esperadas y P(>=13)
for t in ['76ers','Trail Blazers','Thunder','Pacers']:
    v=S[t];n=v[0]+v[1];pg=norm.cdf(v[2]/SIG);print(t,'n',n,'W',v[0],'esp por margen',round(n*pg,1),'P(>=W)',round(binom.sf(v[0]-1,n,pg),4),'P(<=W)',round(binom.cdf(v[0],n,pg),4))
# 76ers juegos cerrados: Pythagorean-like: win% esperado por MOV (Φ(MOV/σ)) vs real
v=S['76ers'];print('76ers win% real',round(v[0]/16,3),'esperado por margen',round(norm.cdf(v[2]/SIG),3))
# Monte Carlo: récord final 76ers con su nivel Q (resto 82-17=65 juegos, mitad en casa), incluye 14-3 actual
rng=np.random.default_rng(1122);N=100000;rem=65;q=rng.normal(Q['76ers'],SIG/np.sqrt(16+K),N)
home=np.r_[np.ones(33),np.zeros(32)];pw=norm.cdf((q[:,None]-0+np.where(home==1,H,-H)[None,:])/SIG)
w=14+(rng.random((N,rem))<pw).sum(1);print('76ers victorias finales',w.mean().round(1),'80%',np.percentile(w,[10,90]),'P(>=50)',(w>=50).mean().round(3),'ritmo actual 14/17*82',round(14/17*82,1))
# back-to-back: OKC@IND ambos en b2b → ajustes se cancelan (−2.1 cada uno)
mg=Q['Pacers']-Q['Thunder']+H-2.1+2.1;print('OKC@IND con ambos b2b P(IND)',round(norm.cdf(mg/SIG),3))
mg2=Q['Pacers']-Q['Thunder']+H+2.1;print('si solo OKC en b2b P(IND)',round(norm.cdf(mg2/SIG),3),'| P(OKC) base',round(1-norm.cdf((Q['Pacers']-Q['Thunder']+H)/SIG),3))
# Thunder: récord 9-6 vs MOV 4.4 / SRS 5.79 ; nivel previo
print('Thunder W25 64 → prior',round(0.9*(64-41)/2.7,2),'SRS',S['Thunder'][4],'Q',round(Q['Thunder'],2))
print('Pacers W25 19 → prior',round(0.9*(19-41)/2.7,2),'SRS',S['Pacers'][4],'Q',round(Q['Pacers'],2))
