import numpy as np, json
from scipy.optimize import minimize
exec(open("studio/models/ucl_data_1102.py").read().split("T=sorted")[0])
C={"PSG":132,"Bayern":147.5,"Real Madrid":144.5,"Liverpool":130,"Inter":127,"Man City":125.5,"Arsenal":119,"Barcelona":113.25,"Atlético":104.75,"Dortmund":100.75,"Roma":97.75,"Sporting CP":84,"Aston Villa":83,"Porto":80.75,"Man Utd":76.5,"Club Brugge":75.25,"Real Betis":74.5,"PSV":71.25,"Feyenoord":71,"Lille":68.75,"Bodø/Glimt":64,"Napoli":63,"Leipzig":61,"Villarreal":59,"Fenerbahçe":57.75,"Shakhtar":56.25,"Galatasaray":53.5,"Slavia Praha":44,"Slovan Bratislava":36,"Stuttgart":27.5,"AEK Athens":24,"LASK":21,"Como":19.989,"Lens":16.699,"Viking":8.247,"Sabah":6}
T=sorted(C); ix={t:i for i,t in enumerate(T)}; n=len(T)
assert all(g[0] in C and g[3] in C for g in G)
z=np.log([C[t] for t in T]); z=(z-z.mean())/z.std()
H=np.array([ix[g[0]] for g in G]); A=np.array([ix[g[3]] for g in G]); X=np.array([g[1] for g in G]); Y=np.array([g[2] for g in G])
MD=np.repeat([1,2,3],18)
LAM=12.0
def unpack(p): return p[:n],p[n:2*n],p[-4],p[-3],p[-2],p[-1]
def nll(p,idx):
    a,d,c,h,ba,bd=unpack(p)
    att=ba*z+a; de=bd*z+d
    l1=np.exp(c+h+att[H[idx]]-de[A[idx]]); l2=np.exp(c+att[A[idx]]-de[H[idx]])
    return -(X[idx]*np.log(l1)-l1+Y[idx]*np.log(l2)-l2).sum()+LAM/2*(a@a+d@d)+4*(h-np.log(1.25))**2
def fit(idx):
    return minimize(nll,np.r_[np.zeros(2*n),np.log(1.6),0.2,0.2,0.2],args=(idx,),method="L-BFGS-B").x
def lam(p,Hn,An):
    a,d,c,h,ba,bd=unpack(p); att=ba*z+a; de=bd*z+d; i,j=ix[Hn],ix[An]
    return np.exp(c+h+att[i]-de[j]), np.exp(c+att[j]-de[i])
from scipy.stats import poisson
def p3(l1,l2,K=15):
    px=poisson.pmf(np.arange(K),l1); py=poisson.pmf(np.arange(K),l2); M=np.outer(px,py)
    return np.array([np.tril(M,-1).sum(),np.trace(M),np.triu(M,1).sum()])
# validation: fit MD1-2, predict MD3
p12=fit(np.where(MD<3)[0]); br=[];bu=[];bb=[]
base=np.array([71,25,48])/144
for k in np.where(MD==3)[0]:
    pr=p3(*lam(p12,G[k][0],G[k][3])); o=np.array([G[k][1]>G[k][2],G[k][1]==G[k][2],G[k][1]<G[k][2]],float)
    br.append(((pr-o)**2).sum()); bu.append(((1/3-o)**2).sum()); bb.append(((base-o)**2).sum())
print("MD3 out-of-sample Brier model",np.mean(br).round(3),"uniform",np.mean(bu).round(3),"home/draw/away base",np.mean(bb).round(3), "hits", )
full=fit(np.arange(54)); a,d,c,h,ba,bd=unpack(full); print("beta att",ba.round(3),"beta def",bd.round(3),"home",np.exp(h).round(3),"base",np.exp(c).round(3))
M=[("Atlético","Bayern"),("Fenerbahçe","Liverpool"),("Leipzig","Man City"),("Dortmund","Real Betis"),("Barcelona","Aston Villa"),("Villarreal","PSG"),("Slavia Praha","Arsenal")]
rng=np.random.default_rng(3); B=[]
for b in range(400):
    idx=rng.integers(0,54,54); p=fit(idx); B.append([np.r_[p3(*lam(p,h_,a_)),lam(p,h_,a_)] for h_,a_ in M])
B=np.array(B); out={}
for k,(h_,a_) in enumerate(M):
    l=lam(full,h_,a_); pt=p3(*l); lo=np.percentile(B[:,k,:3],10,0); hi=np.percentile(B[:,k,:3],90,0)
    out[f"{h_}-{a_}"]=dict(p=pt.tolist(),lo=lo.tolist(),hi=hi.tolist(),xg=list(l))
    print(f"{h_}-{a_} H/D/A {pt.round(3)} xg {np.round(l,2)} 80% {lo.round(2)}-{hi.round(2)}")
json.dump(dict(out=out,p=full.tolist(),T=T),open("/tmp/xgol-ucl-fit.json","w"))
