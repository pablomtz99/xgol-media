"""Pumas–Monterrey (J17, sáb 21 nov 19:00 CDMX): probabilidades condicionadas a cada resultado. Reutiliza ligamx_j17_1119.py (tabla tras J16; futboltotal/Claro/Record).
Modelo xGol Liga MX v0 (diferencia de goles encogida, Poisson, localía +0.35)."""
import numpy as np, io, contextlib, importlib.util, os
spec=importlib.util.spec_from_file_location('m',os.path.join(os.path.dirname(os.path.abspath(__file__)),'ligamx_j17_1119.py'))
with contextlib.redirect_stdout(io.StringIO()):
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
T,GD,GF,MU,FIX=m.T,m.GD,m.GF,m.MU,m.FIX
def sim(K=8,HADV=0.35,N=200000,seed=1120):
    r={k:GD[k]/(16+K) for k in T};rng=np.random.default_rng(seed);teams=list(T);ix={t:i for i,t in enumerate(teams)}
    pts=np.tile(np.array([T[t][0] for t in teams],float),(N,1));gd=np.tile(np.array([GD[t] for t in teams],float),(N,1));gf=np.tile(np.array([GF[t] for t in teams],float),(N,1))
    b=2/MU;h=HADV/MU;out={}
    for H,A in FIX:
        d=r[H]-r[A];lh=MU/2*np.exp(b*d/2+h);la=MU/2*np.exp(-b*d/2-h);x=rng.poisson(lh,N);y=rng.poisson(la,N);out[(H,A)]=(x,y,lh,la)
        i,j=ix[H],ix[A];pts[:,i]+=np.where(x>y,3,np.where(x==y,1,0));pts[:,j]+=np.where(y>x,3,np.where(x==y,1,0));gd[:,i]+=x-y;gd[:,j]+=y-x;gf[:,i]+=x;gf[:,j]+=y
    gfx=np.where(np.isnan(gf),rng.uniform(15,35,gf.shape),gf);key=pts*1e6+gd*1e3+gfx+rng.uniform(0,1e-3,pts.shape);rank=(-key).argsort(1).argsort(1)+1
    return out,rank,ix
out,rank,ix=sim()
x,y,lh,la=out[('Pumas','Monterrey')]
print('xG',round(lh,2),round(la,2),'P PUM',(x>y).mean().round(3),'E',(x==y).mean().round(3),'MTY',(x<y).mean().round(3))
for t in ['Pumas','Monterrey','Tijuana','Pachuca','León','Santos']:
    t8=rank[:,ix[t]]<=8
    print(f"{t:10s} top8 {t8.mean():.3f} | PUM gana {t8[x>y].mean():.3f} | empate {t8[x==y].mean():.3f} | MTY gana {t8[x<y].mean():.3f}")
for K,Hd in [(0,.35),(16,.35),(8,0),(8,.6)]:
    o,r2,ix2=sim(K,Hd,N=100000,seed=7);x2,y2,_,_=o[('Pumas','Monterrey')]
    print('sens',K,Hd,'PUM',(x2>y2).mean().round(3),'top8 PUM',(r2[:,ix2['Pumas']]<=8).mean().round(3),'| si gana',(r2[:,ix2['Pumas']]<=8)[x2>y2].mean().round(3),'MTY top8',(r2[:,ix2['Monterrey']]<=8).mean().round(3))
