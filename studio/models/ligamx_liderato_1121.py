"""Liga MX J17: ¿quién termina 1°? Cruz Azul 32 (+11), América 30 (+15), Chivas 30 (+11) tras J16 (futboltotal; Claro Sports, Record; ver ligamx_j17_1119.py).
Partidos que deciden: Tigres–América (sáb 21, 21:00 CDMX) y Chivas–Cruz Azul (dom 22, 17:07). Los juegos del viernes no afectan el 1° lugar.
Modelo xGol Liga MX v0 (dif. de goles encogida, Poisson, localía +0.35) + Monte Carlo 400,000. Desempate: diferencia de goles, luego goles a favor."""
import numpy as np, io, contextlib, importlib.util, os
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'ligamx_j17_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
T,GD,GF,MU=m.T,m.GD,m.GF,m.MU
def sim(K=8,HADV=0.35,N=400000,seed=1121):
    r={k:GD[k]/(16+K) for k in T};b=2/MU;h=HADV/MU;rng=np.random.default_rng(seed);o={}
    for H,A in [('Tigres','América'),('Chivas','Cruz Azul')]:
        d=r[H]-r[A];lh=MU/2*np.exp(b*d/2+h);la=MU/2*np.exp(-b*d/2-h);o[(H,A)]=(rng.poisson(lh,N),rng.poisson(la,N),lh,la)
    x1,y1,_,_=o[('Tigres','América')];x2,y2,_,_=o[('Chivas','Cruz Azul')]
    pts={'Cruz Azul':32+np.where(y2>x2,3,np.where(x2==y2,1,0)),'América':30+np.where(y1>x1,3,np.where(x1==y1,1,0)),'Chivas':30+np.where(x2>y2,3,np.where(x2==y2,1,0))}
    gd={'Cruz Azul':GD['Cruz Azul']+y2-x2,'América':GD['América']+y1-x1,'Chivas':GD['Chivas']+x2-y2}
    gf={'Cruz Azul':GF['Cruz Azul']+y2,'América':GF['América']+y1,'Chivas':GF['Chivas']+x2}
    tm=list(pts);key=np.stack([pts[t]*1e6+gd[t]*1e3+gf[t]+rng.uniform(0,1e-3,N) for t in tm]);lead=np.array(tm)[key.argmax(0)]
    return o,lead,(x1,y1,x2,y2)
o,lead,(x1,y1,x2,y2)=sim()
for k,(x,y,lh,la) in o.items(): print(k,'goles esp',round(lh,2),round(la,2),'L',(x>y).mean().round(3),'E',(x==y).mean().round(3),'V',(x<y).mean().round(3))
for t in ['Cruz Azul','América','Chivas']: print('líder',t,(lead==t).mean().round(3))
R1={'AME gana':y1>x1,'empate':x1==y1,'AME pierde':y1<x1};R2={'CHV gana':x2>y2,'empate':x2==y2,'CAZ gana':y2>x2}
print('escenarios (filas Tigres–América, columnas Chivas–CAZ): líder más probable y %')
for a,ma in R1.items():
    row=[]
    for b,mb in R2.items():
        mm=ma&mb;vals={t:(lead[mm]==t).mean() for t in ['Cruz Azul','América','Chivas']};best=max(vals,key=vals.get);row.append(f"{b}: {best} {vals[best]:.2f} (p esc {mm.mean():.3f})")
    print(a,'|',' ; '.join(row))
print('AME líder si gana',(lead[y1>x1]=='América').mean().round(3),'| CAZ líder si gana',(lead[y2>x2]=='Cruz Azul').mean().round(3),'| CHV líder si gana',(lead[x2>y2]=='Chivas').mean().round(3))
for K,H in [(0,.35),(16,.35),(8,0),(8,.6)]:
    _,l2,_=sim(K,H,N=100000,seed=7);print('sens',K,H,{t:round((l2==t).mean(),3) for t in ['Cruz Azul','América','Chivas']})
