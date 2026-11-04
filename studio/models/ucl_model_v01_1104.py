"""Modelo xGol UCL v0.1 (4 nov): v0 + los 9 partidos del martes 3 nov (J4) → 63 partidos.
Lección del martes (22 goles vs 32.7 esperados): ridge más fuerte (λ=20, antes 12) y localía con prior más firme
(×1.25, peso 12 antes 4) y prior de goles: 3.39 por partido (fase liga 2025-26, UEFA.com), peso CW. Rangos 10–90% por bootstrap (300). Validación: J4 martes fuera de muestra con v0 y v0.1."""
import numpy as np, json, sys
from scipy.optimize import minimize
from scipy.stats import poisson
exec(open("studio/models/ucl_data_1102.py").read().split("T=sorted")[0])
J4 = [("Shakhtar",0,1,"Sporting CP"),("Galatasaray",2,0,"Stuttgart"),("Man Utd",3,2,"Roma"),("Villarreal",0,6,"PSG"),
      ("Barcelona",3,0,"Aston Villa"),("Atlético",0,2,"Bayern"),("LASK",4,0,"Slovan Bratislava"),("Bodø/Glimt",0,0,"Lille"),("Feyenoord",0,3,"Inter")]
G = G + J4
C={"PSG":132,"Bayern":147.5,"Real Madrid":144.5,"Liverpool":130,"Inter":127,"Man City":125.5,"Arsenal":119,"Barcelona":113.25,"Atlético":104.75,"Dortmund":100.75,"Roma":97.75,"Sporting CP":84,"Aston Villa":83,"Porto":80.75,"Man Utd":76.5,"Club Brugge":75.25,"Real Betis":74.5,"PSV":71.25,"Feyenoord":71,"Lille":68.75,"Bodø/Glimt":64,"Napoli":63,"Leipzig":61,"Villarreal":59,"Fenerbahçe":57.75,"Shakhtar":56.25,"Galatasaray":53.5,"Slavia Praha":44,"Slovan Bratislava":36,"Stuttgart":27.5,"AEK Athens":24,"LASK":21,"Como":19.989,"Lens":16.699,"Viking":8.247,"Sabah":6}
T=sorted(C); ix={t:i for i,t in enumerate(T)}; n=len(T)
z=np.log([C[t] for t in T]); z=(z-z.mean())/z.std()
H=np.array([ix[g[0]] for g in G]); A=np.array([ix[g[3]] for g in G]); X=np.array([g[1] for g in G]); Y=np.array([g[2] for g in G])
LAM, HW, CW = 20.0, 12.0, 124.0   # CW≈goles/2: mismo peso a 2025-26 que a esta temporada
C0 = np.log(3.39/2.25)
def unpack(p): return p[:n],p[n:2*n],p[-4],p[-3],p[-2],p[-1]
def nll(p,idx,lam=LAM,hw=HW,cw=CW):
    a,d,c,h,ba,bd=unpack(p); att=ba*z+a; de=bd*z+d
    l1=np.exp(c+h+att[H[idx]]-de[A[idx]]); l2=np.exp(c+att[A[idx]]-de[H[idx]])
    return -(X[idx]*np.log(l1)-l1+Y[idx]*np.log(l2)-l2).sum()+lam/2*(a@a+d@d)+hw*(h-np.log(1.25))**2+cw*(c-C0)**2
def fit(idx,lam=LAM,hw=HW,cw=CW):
    return minimize(nll,np.r_[np.zeros(2*n),np.log(1.6),0.2,0.2,0.2],args=(idx,lam,hw,cw),method="L-BFGS-B").x
def lam_(p,Hn,An):
    a,d,c,h,ba,bd=unpack(p); att=ba*z+a; de=bd*z+d; i,j=ix[Hn],ix[An]
    return np.exp(c+h+att[i]-de[j]), np.exp(c+att[j]-de[i])
def p3(l1,l2,K=15):
    px=poisson.pmf(np.arange(K),l1); py=poisson.pmf(np.arange(K),l2); M=np.outer(px,py)
    return np.array([np.tril(M,-1).sum(),np.trace(M),np.triu(M,1).sum()])
if __name__=="__main__":
    # out-of-sample on J4 Tuesday: v0 (12,4) vs v0.1 (20,12), both fitted on first 54
    for lab,(l,hw,cw) in {"v0":(12,4,0),"v0.1":(20,12,CW)}.items():
        p=fit(np.arange(54),l,hw,cw); br=[];gl=0
        for k in range(54,63):
            l1,l2=lam_(p,G[k][0],G[k][3]); pr=p3(l1,l2); o=np.array([G[k][1]>G[k][2],G[k][1]==G[k][2],G[k][1]<G[k][2]],float)
            br.append(((pr-o)**2).sum()); gl+=l1+l2
        print(lab,"J4-mar Brier",round(np.mean(br),3),"goles esperados",round(gl,1),"reales",sum(g[1]+g[2] for g in J4))
    full=fit(np.arange(len(G))); a,d,c,h,ba,bd=unpack(full)
    print("home",np.exp(h).round(3),"base",np.exp(c).round(3))
    W=[("AEK Athens","Real Madrid"),("Fenerbahçe","Liverpool"),("Dortmund","Real Betis"),("Porto","Napoli"),("PSV","Club Brugge"),
       ("Leipzig","Man City"),("Lens","Como"),("Slavia Praha","Arsenal"),("Viking","Sabah")]
    rng=np.random.default_rng(4); B=[]
    for b in range(300):
        idx=rng.integers(0,len(G),len(G)); pp=fit(idx); B.append([p3(*lam_(pp,x,y)) for x,y in W])
    B=np.array(B); out={}
    for k,(x,y) in enumerate(W):
        l=lam_(full,x,y); pt=p3(*l); lo=np.percentile(B[:,k],10,0); hi=np.percentile(B[:,k],90,0)
        o25=1-sum(poisson.pmf(i,l[0]+l[1]) for i in range(3))
        out[f"{x}-{y}"]=dict(p=pt.tolist(),lo=lo.tolist(),hi=hi.tolist(),xg=list(l),o25=o25)
        print(f"{x}-{y} H/D/A {pt.round(3)} xg {np.round(l,2)} tot {sum(l):.2f} o25 {o25:.2f} 80% {lo.round(2)}-{hi.round(2)}")
    json.dump(dict(out=out),open("/tmp/xgol-m/ucl_v01.json","w"))
