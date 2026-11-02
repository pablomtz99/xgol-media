import numpy as np, json
exec(open("studio/models/ucl_model_v0.py").read().split("# validation")[0])
rng=np.random.default_rng(5); ks=[]
for b in range(300):
    idx=rng.integers(0,54,54); p=fit(idx); a,d,c,h,ba,bd=unpack(p); att=ba*z+a; de=bd*z+d; i=ix["Bayern"]
    avg=np.mean([(np.exp(c+h+att[i]-de[j])+np.exp(c+att[i]-de[j]))/2 for j in range(n) if j!=i])
    f=lam(p,"Atlético","Bayern")[1]/avg
    rate=rng.gamma(37,1/41)  # uncertainty in Kane rate
    ks.append(1-np.exp(-rate*f))
print(np.percentile(ks,[10,50,90]).round(3))
