"""UCL J5 miércoles 25 nov (11:45 y 14:00 CDMX). Modelo xGol UCL v0.1 ajustado con J1–J4 (72 partidos; ucl_j5_1123.py). Calendario: ParisFans y Sport News Africa (24 nov).
Rangos 80% por bootstrap (300). Monte Carlo 200,000 jornadas: # de 'sorpresas' (no gana el favorito del modelo) y goles totales. Ejecutar desde la raíz."""
import numpy as np, io, contextlib
from scipy.stats import poisson
src=open("studio/models/ucl_j5_1123.py").read()
with contextlib.redirect_stdout(io.StringIO()): exec(src)
full=fit(np.arange(len(G)))
W=[("Sabah","Barcelona"),("Slavia Praha","Villarreal"),("Atlético","Viking"),("Club Brugge","Liverpool"),("Inter","Stuttgart"),
   ("Lille","Bayern"),("PSG","Roma"),("Shakhtar","Fenerbahçe"),("Sporting CP","Man Utd")]
rng=np.random.default_rng(1125);B=[]
for b in range(300):
    idx=rng.integers(0,len(G),len(G));pp=fit(idx);B.append([p3(*lam_(pp,x,y)) for x,y in W])
B=np.array(B);P=[];L=[]
for k,(x,y) in enumerate(W):
    l=lam_(full,x,y);pt=p3(*l);P.append(pt);L.append(l);lo=np.percentile(B[:,k],10,0);hi=np.percentile(B[:,k],90,0)
    print(f"{x}-{y} L/E/V {pt.round(3)} 80% L {lo[0]:.2f}-{hi[0]:.2f} V {lo[2]:.2f}-{hi[2]:.2f} goles esp {sum(l):.2f} ({l[0]:.2f}-{l[1]:.2f})")
P=np.array(P);L=np.array(L);fav=P.argmax(1);pf=P.max(1)
print('favoritos',[('L','E','V')[f] for f in fav],pf.round(3));print('ganan todos los favoritos',np.prod(pf).round(4),'sorpresas esperadas',(1-pf).sum().round(2))
N=200000;gx=rng.poisson(L[:,0],(N,9));gy=rng.poisson(L[:,1],(N,9));res=np.where(gx>gy,0,np.where(gx==gy,1,2));sur=(res!=fav).sum(1)
print('dist sorpresas',[round((sur==i).mean(),3) for i in range(7)],'P(>=3)',(sur>=3).mean().round(3))
tot=(gx+gy).sum(1);print('goles jornada esp',tot.mean().round(1),'80%',np.percentile(tot,[10,90]))
# visitantes grandes: Barcelona, Liverpool, Bayern ganan los 3
print('Barcelona+Liverpool+Bayern ganan',np.prod(P[[0,3,5],2]).round(3))
# fuerza: ataque/defensa ajustados
a,d,c,h,ba,bd=unpack(full);att=ba*z+a;de=bd*z+d
for t in ['Bayern','Liverpool','Barcelona','PSG','Inter','Lille','Club Brugge','Roma','Sabah','Viking','Atlético','Man Utd','Sporting CP']:
    print(t,'ataque',round(att[ix[t]],2),'defensa',round(de[ix[t]],2),'rk ataque',int((att>att[ix[t]]).sum()+1),'rk def',int((de>de[ix[t]]).sum()+1))
# tabla J1-J4 (pts, GF, GA) de los partidos en G
pts={t:[0,0,0,0] for t in T}
for g in G:
    x,gx_,gy_,y=g;pts[x][1]+=gx_;pts[x][2]+=gy_;pts[y][1]+=gy_;pts[y][2]+=gx_;pts[x][3]+=1;pts[y][3]+=1
    if gx_>gy_:pts[x][0]+=3
    elif gx_<gy_:pts[y][0]+=3
    else:pts[x][0]+=1;pts[y][0]+=1
tb=sorted(pts.items(),key=lambda kv:(-kv[1][0],-(kv[1][1]-kv[1][2]),-kv[1][1]))
for i,(t,v) in enumerate(tb,1):
    if t in [w for p_ in W for w in p_]:print(i,t,v)
