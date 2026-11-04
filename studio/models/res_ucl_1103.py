import numpy as np
from scipy.stats import poisson
P={'SHA-SCP':((.494,.22,.286),3.38,.657,(0,1)),'GAL-VFB':((.518,.205,.277),3.77,.725,(2,0)),
'ATM-BAY':((.479,.207,.314),3.85,.74,(0,2)),'BAR-AVL':((.60,.169,.231),4.76,.854,(3,0)),
'FEY-INT':((.421,.214,.364),3.74,.721,(0,3)),'BOD-LIL':((.597,.179,.224),4.27,.80,(0,0)),
'MUN-ROM':((.445,.207,.348),3.95,.756,(3,2)),'VIL-PSG':((.323,.18,.497),4.95,.871,(0,6))}
br=[];hits=0;ph=[];ov=[];oo=[]
for k,(p,xg,o,(h,a)) in P.items():
    r=0 if h>a else (1 if h==a else 2); y=np.eye(3)[r]; b=((np.array(p)-y)**2).sum(); br.append(b)
    fav=int(np.argmax(p)); hits+=fav==r; ph.append(max(p)); ov.append(o); oo.append(h+a>=3)
    print(k,h,a,'fav',fav,'res',r,'p_res',p[r],'brier',round(b,3), 'ok' if fav==r else 'X')
br=np.array(br); print('Brier',br.mean(),'unif',2/3, 'hits',hits,'exp hits',sum(ph))
# poisson-binomial of hits
d=np.array([1.]); 
for q in ph: d=np.convolve(d,[1-q,q])
print('P(hits=k)',np.round(d,3),'P(<=4)',d[:5].sum(),'P(>=4)',d[4:].sum())
G=sum(h+a for *_, (h,a) in P.values()); L=sum(v[1] for v in P.values()); print('goals',G,'exp',L,'P(X<=G)',poisson.cdf(G,L))
print('over2.5 hits',sum(oo),'exp',sum(ov),'brier over',np.mean((np.array(ov)-np.array(oo))**2))
# baseline historic UCL home/draw/away ~ (.46,.24,.30)
base=np.array([.46,.24,.30]); bb=[]
for k,(p,xg,o,(h,a)) in P.items():
    r=0 if h>a else (1 if h==a else 2); bb.append(((base-np.eye(3)[r])**2).sum())
print('base brier',np.mean(bb))
# result-prob mean
