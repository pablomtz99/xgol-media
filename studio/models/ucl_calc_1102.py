import numpy as np, json
from scipy.stats import poisson, binom
exec(open("studio/models/ucl_model_v0.py").read().split("# validation")[0])
F=json.load(open("/tmp/xgol-ucl-fit.json")); full=np.array(F["p"])
a,d,c,h,ba,bd=unpack(full)
# Bayern typical lambda vs avg opp, neutral-ish (average of home/away)
i=ix["Bayern"]; att=ba*z+a; de=bd*z+d
lam_avg=np.mean([ (np.exp(c+h+att[i]-de[j])+np.exp(c+att[i]-de[j]))/2 for j in range(n) if j!=i])
lb=lam(full,"Atlético","Bayern")[1]; f=lb/lam_avg
for rate in (37/41,58/73):
    lk=rate*f; print("Kane rate",round(rate,3),"factor",round(f,3),"lamK",round(lk,3),"P score",round(1-np.exp(-lk),3), "P score base",round(1-np.exp(-rate),3))
# streak rarity: p per game
p=1-np.exp(-37/41); print("p per game",p, "P(10 straight)",p**10, "1 en",1/p**10)
rng=np.random.default_rng(1); N=200000; S=rng.random((N,41))<p
def longest(row):
    m=r=0
    for v in row:
        r=r+1 if v else 0; m=max(m,r)
    return m
L=np.array([longest(r) for r in S[:50000]]); print("P(any >=10 streak in 41 Bayern UCL games)",(L>=10).mean(),"P>=11",(L>=11).mean(), "median longest",np.median(L))
# Liverpool no draws
for pd_ in (25/144,0.15,0.12):
    print("pdraw",round(pd_,3),"P(0 in 46)",(1-pd_)**46,"1 en",round(1/(1-pd_)**46))
# selection: 36 clubs, each with window of 120 UEFA games, P(any run >=46 without draw)
pd_=25/144; rng=np.random.default_rng(2); K=20000; hits=0
for k in range(K):
    D=rng.random((36,120))<pd_
    ok=False
    for row in D:
        r=m=0
        for v in row:
            r=0 if v else r+1; m=max(m,r)
        if m>=46: ok=True;break
    hits+=ok
print("P(some club of 36 has 46+ no-draw run in 120 games)",hits/K)
# Liverpool model draw prob vs Fenerbahce
print("Fen-Liv",F["out"]["Fenerbahçe-Liverpool"])
# Haaland
lamH=8*61/60; print("Haaland lam8",lamH,"P(>=12)",1-poisson.cdf(11,lamH))
print("Leipzig-City",F["out"]["Leipzig-Man City"])
# Betis 3 wins expected points with full model
fx=[("Lille","Real Betis","A"),("Real Betis","Porto","H"),("Real Betis","Feyenoord","H")]
P=[]; E=0
for hh,aa,s in fx:
    pr=p3(*lam(full,hh,aa)); w=pr[2] if s=="A" else pr[0]; P.append(w); E+=3*w+pr[1]
print("Betis win probs",np.round(P,3),"P(3/3)",np.prod(P),"E pts",E)
# one-goal margins: P(win by exactly 1 | win)
print("Dortmund-Betis",F["out"]["Dortmund-Real Betis"])
print("Atl-Bay",F["out"]["Atlético-Bayern"])
