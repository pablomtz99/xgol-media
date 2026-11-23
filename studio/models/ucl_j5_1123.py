"""Modelo xGol UCL v0.1 + J4 miércoles 4 nov (Sports Mole y El País Cali, 4 nov) → 72 partidos. Validación fuera de muestra: J4 completa (18 partidos)
predicha con el ajuste de J1–J3 (54). Previa J5 martes 24 nov (14:00 CDMX): Arsenal–Dortmund, Man City–Napoli, Real Madrid–PSV.
Tabla tras J4: fcbayern.com y NBC Sports (coinciden en diferencias). Ejecutar desde la raíz del repo."""
import numpy as np, io, contextlib
from scipy.stats import poisson
src=open("studio/models/ucl_model_v01_1104.py").read().split('if __name__')[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
J4W=[("Lens",1,9,"Como"),("AEK Athens",2,3,"Real Madrid"),("Fenerbahçe",3,2,"Liverpool"),("Viking",4,1,"Sabah"),("Leipzig",2,3,"Man City"),
     ("Dortmund",2,1,"Real Betis"),("Porto",4,1,"Napoli"),("PSV",1,2,"Club Brugge"),("Slavia Praha",1,2,"Arsenal")]
G=G+J4W
H=np.array([ix[g[0]] for g in G]); A=np.array([ix[g[3]] for g in G]); X=np.array([g[1] for g in G]); Y=np.array([g[2] for g in G])
def o_(g): return np.array([g[1]>g[2],g[1]==g[2],g[1]<g[2]],float)
p54=fit(np.arange(54)); br=[];hit=0;bu=[]
for g in G[54:72]:
    pr=p3(*lam_(p54,g[0],g[3]));o=o_(g);br.append(((pr-o)**2).sum());hit+=pr.argmax()==o.argmax();bu.append(((np.ones(3)/3-o)**2).sum())
br=np.array(br);print('J4 fuera de muestra n=18 Brier',br.mean().round(3),'uniforme',np.mean(bu).round(3),'aciertos',hit)
# referencia "localía histórica" 45/27/28
ref=np.array([.45,.27,.28]);bref=np.mean([((ref-o_(g))**2).sum() for g in G[54:72]]);print('ref local-base Brier',round(bref,3))
# bootstrap diferencia Brier modelo vs uniforme
rng=np.random.default_rng(23);d=br-np.array(bu);bs=[d[rng.integers(0,18,18)].mean() for _ in range(5000)];print('mejora vs uniforme',(-d.mean()).round(3),'P(mejora)',(np.array(bs)<0).mean().round(3))
full=fit(np.arange(72));a,d_,c,h,ba,bd=unpack(full);att=ba*z+a;de=bd*z+d_
print('localía x',np.exp(h).round(3),'base',np.exp(c).round(3))
rkA=sorted(T,key=lambda t:-att[ix[t]]);rkD=sorted(T,key=lambda t:-de[ix[t]])
W=[("Arsenal","Dortmund"),("Man City","Napoli"),("Real Madrid","PSV")]
B=[]
for b in range(300):
    idx=rng.integers(0,72,72);pp=fit(idx);B.append([p3(*lam_(pp,x,y)) for x,y in W])
B=np.array(B)
for k,(x,y) in enumerate(W):
    l=lam_(full,x,y);pt=p3(*l);lo=np.percentile(B[:,k],10,0);hi=np.percentile(B[:,k],90,0)
    cs=poisson.pmf(0,l[1]);print(f"{x}-{y} L/E/V {pt.round(3)} goles {np.round(l,2)} 80% L {lo[0]:.2f}-{hi[0]:.2f} | P(portería en cero local) {cs:.2f} | ataque rk {rkA.index(x)+1},{rkA.index(y)+1} defensa rk {rkD.index(x)+1},{rkD.index(y)+1}")
# goles reales por equipo vs esperados (modelo sin cada equipo no; simple: GF/GC 4 partidos)
for t in ['Arsenal','Dortmund','Man City','Napoli','Real Madrid','PSV']:
    gf=sum(g[1] for g in G if g[0]==t)+sum(g[2] for g in G if g[3]==t);ga=sum(g[2] for g in G if g[0]==t)+sum(g[1] for g in G if g[3]==t)
    print(t,'GF',gf,'GC',ga)
