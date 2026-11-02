import numpy as np, re, json
R="""AEK Athens 1-0 LASK; Club Brugge 2-3 Aston Villa; Borussia Dortmund 3-2 Villarreal; Porto 0-2 Man City; Lille 2-3 Real Betis; Real Madrid 2-1 Inter; Barcelona 5-1 Feyenoord; Stuttgart 3-1 Viking; Liverpool 2-1 Atlético; PSG 6-1 Slovan Bratislava; Sporting CP 3-1 Galatasaray; Napoli 0-1 Arsenal; Fenerbahçe 1-1 Roma; PSV 1-1 Shakhtar; Como 4-1 Leipzig; Bayern 5-0 Bodø/Glimt; Man Utd 4-0 Sabah; Slavia Praha 2-3 Lens; Lens 0-2 Sporting CP; Sabah 2-0 Slavia Praha; Arsenal 3-0 Lille; Atlético 2-0 Man Utd; Inter 3-4 Club Brugge; Galatasaray 1-4 Barcelona; Leipzig 1-0 PSV; Viking 3-3 Bayern; Villarreal 3-1 Napoli; Feyenoord 3-2 Como; LASK 3-6 Liverpool; Roma 3-4 Real Madrid; Aston Villa 6-0 Fenerbahçe; Shakhtar 3-1 AEK Athens; Bodø/Glimt 1-0 Dortmund; Man City 2-4 PSG; Real Betis 3-2 Porto; Slovan Bratislava 0-3 Stuttgart; Fenerbahçe 2-2 Slavia Praha; Sabah 1-2 Dortmund; Roma 4-0 Slovan Bratislava; Porto 0-1 PSV; Liverpool 4-3 Villarreal; Man City 5-1 AEK Athens; PSG 4-2 Barcelona; Napoli 4-3 Bodø/Glimt; Stuttgart 1-1 Atlético; Como 4-1 Man Utd; Lille 2-4 Galatasaray; Aston Villa 3-1 Viking; Club Brugge 3-0 Lens; Bayern 2-2 Arsenal; Inter 1-0 Shakhtar; Real Madrid 4-1 Leipzig; Real Betis 1-0 Feyenoord; Sporting CP 2-3 LASK"""
G=[]
for m in R.split("; "):
    h,hs,as_,a=re.match(r"(.+?) (\d+)-(\d+) (.+)",m).groups(); G.append((h.replace("Borussia ",""),int(hs),int(as_),a.replace("Borussia ","")))
T=sorted({g[0] for g in G}|{g[3] for g in G}); ix={t:i for i,t in enumerate(T)}
hg=np.mean([g[1] for g in G]); ag=np.mean([g[2] for g in G]); mu=(hg+ag)/2
print(len(G),"games",len(T),"teams; home",hg,"away",ag,"draws",sum(g[1]==g[2] for g in G))
# Poisson GLM with ridge (prior strength) via IRLS-ish gradient
def fit(lam):
    n=len(T); a=np.zeros(n); d=np.zeros(n); c=np.log(mu); h=0.
    for it in range(4000):
        ga=np.zeros(n); gd=np.zeros(n); gc=0; gh=0
        for H,x,y,A in G:
            i,j=ix[H],ix[A]
            l1=np.exp(c+h+a[i]-d[j]); l2=np.exp(c+a[j]-d[i])
            ga[i]+=x-l1; gd[j]-=x-l1; ga[j]+=y-l2; gd[i]-=y-l2; gc+=x-l1+y-l2; gh+=x-l1
        ga-=lam*a; gd-=lam*d
        a+=0.01*ga; d+=0.01*gd; c+=0.002*gc; h+=0.004*gh
    return a,d,c,h
lam=3.0
a,d,c,h=fit(lam)
print("home adv",np.exp(h),"base",np.exp(c))
def pred(H,A,N=200000,seed=1):
    i,j=ix[H],ix[A]; l1=np.exp(c+h+a[i]-d[j]); l2=np.exp(c+a[j]-d[i])
    rng=np.random.default_rng(seed); x=rng.poisson(l1,N); y=rng.poisson(l2,N)
    return dict(lh=l1,la=l2,ph=(x>y).mean(),pd=(x==y).mean(),pa=(x<y).mean(),tot=(x+y).mean(),o25=((x+y)>2).mean())
for H,A in [("Atlético","Bayern"),("Fenerbahçe","Liverpool"),("Leipzig","Man City"),("Dortmund","Real Betis")]:
    print(H,A,{k:round(v,3) for k,v in pred(H,A).items()})
for t in ["Atlético","Bayern","Fenerbahçe","Liverpool","Leipzig","Man City","Dortmund","Real Betis"]:
    gf=sum(g[1] for g in G if g[0]==t)+sum(g[2] for g in G if g[3]==t); ga_=sum(g[2] for g in G if g[0]==t)+sum(g[1] for g in G if g[3]==t)
    print(t,"GF",gf,"GA",ga_,"att",round(np.exp(a[ix[t]]),2),"def",round(np.exp(-d[ix[t]]),2))
json.dump(dict(T=T,a=a.tolist(),d=d.tolist(),c=c,h=h),open("/tmp/claude-0/m/fit.json","w"))
