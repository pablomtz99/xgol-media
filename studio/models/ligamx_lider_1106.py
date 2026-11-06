import numpy as np
T={ 'America':(15,29,36,21),'Chivas':(15,29,25,14),'Cruz Azul':(15,29,34,24),'Atlas':(15,27,26,26),'Toluca':(15,24,31,21),
 'Pumas':(15,20,22,24),'Tigres':(15,15,15,22),'Leon':(15,22,22,20),'Pachuca':(15,19,25,19),'Juarez':(15,8,12,34),'Monterrey':(14,21,26,21)}
allGF=36+25+34+26+31+25+22+22+21+26+18+25+19+17+15+16+16+12; allPJ=15*16+14*2  # QRO,MTY 14
mu=allGF/allPJ; print('mu',mu)
SH=0.5
att={t:1+SH*((v[2]/v[0])/mu-1) for t,v in T.items()}; de={t:1+SH*((v[3]/v[0])/mu-1) for t,v in T.items()}
att['AVG']=de['AVG']=1
HF=1.15
fix=[('Pumas','America'),('Tigres','Cruz Azul'),('Leon','Chivas'),('Atlas','Pachuca'),('Toluca','Monterrey'),
     ('Tigres','America'),('Chivas','Cruz Azul'),('Juarez','Atlas'),('Toluca','AVG')]
rng=np.random.default_rng(11); N=200000
top=['America','Chivas','Cruz Azul','Atlas','Toluca']
pts={t:np.full(N,T[t][1],float) for t in top}; gd={t:np.full(N,T[t][2]-T[t][3],float) for t in top}; gf={t:np.full(N,T[t][2],float) for t in top}
for h,a in fix:
    lh=mu*att[h]*de[a]*HF; la=mu*att[a]*de[h]/HF
    x=rng.poisson(lh,N); y=rng.poisson(la,N)
    for t,s,c in [(h,x,y),(a,y,x)]:
        if t in pts: pts[t]+=3*(s>c)+(s==c); gd[t]+=s-c; gf[t]+=s
    if (h,a) in [('Pumas','America'),('Tigres','Cruz Azul'),('Leon','Chivas'),('Chivas','Cruz Azul'),('Tigres','America')]:
        print(h,a,'pH %.2f pD %.2f pA %.2f  lh %.2f la %.2f'%((x>y).mean(),(x==y).mean(),(x<y).mean(),lh,la))
key=np.stack([pts[t]*1e6+(gd[t]+100)*1e3+gf[t]+rng.random(N)*0.1 for t in top])
win=key.argmax(0)
for i,t in enumerate(top): print(t,'P lider %.3f'%(win==i).mean(), 'E pts %.1f'%pts[t].mean())
# top-4 probability? (home in quarters)
rank=(-key).argsort(0).argsort(0)
for i,t in enumerate(top): print(t,'P top4 among these %.3f'%(rank[i]<4).mean())
