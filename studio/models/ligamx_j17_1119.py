"""Modelo xGol Liga MX (diferencia de goles, Poisson) + Monte Carlo J17 Apertura 2026. Tabla tras J16 + pendiente QRO-MTY (futboltotal; Claro Sports, Record)."""
import numpy as np
T={ # pts, GF, GA (16 PJ)
'Cruz Azul':(32,37,26),'América':(30,38,23),'Chivas':(30,26,15),'Toluca':(27,35,21),'Atlas':(27,27,30),'Santos':(25,23,20),
'Monterrey':(24,27,25),'León':(23,None,None),'Pachuca':(22,29,20),'Tijuana':(22,25,22),'Pumas':(21,24,26),'Querétaro':(20,18,24),
'Puebla':(19,19,23),'San Luis':(19,19,24),'Tigres':(15,17,25),'Atlante':(14,16,26),'Necaxa':(13,17,28),'Juárez':(11,13,34)}
GD={k:(v[1]-v[2] if v[1] is not None else 2) for k,v in T.items()}
GF={k:(v[1] if v[1] is not None else np.nan) for k,v in T.items()}
tot=sum(v[1] for v in T.values() if v[1])+0; n17=sum(16 for v in T.values() if v[1])
MU=2*sum(v[1] for v in T.values() if v[1])/n17  # goles por partido (ambos equipos)
FIX=[('Puebla','San Luis'),('Juárez','Atlas'),('Tijuana','Atlante'),('Pachuca','Toluca'),('Santos','León'),('Pumas','Monterrey'),('Tigres','América'),('Chivas','Cruz Azul'),('Querétaro','Necaxa')]
def run(K=8,HADV=0.35,N=200000,seed=1119,verbose=True):
    r={k:GD[k]/(16+K) for k in T}  # encogimiento: K partidos ficticios con diferencia 0
    rng=np.random.default_rng(seed); teams=list(T); ix={t:i for i,t in enumerate(teams)}
    pts=np.tile(np.array([T[t][0] for t in teams],float),(N,1)); gd=np.tile(np.array([GD[t] for t in teams],float),(N,1))
    gf=np.tile(np.array([GF[t] for t in teams],float),(N,1)); probs={}
    b=2/MU; h=HADV/MU
    for H,A in FIX:
        d=r[H]-r[A]; lh=MU/2*np.exp(b*d/2+h); la=MU/2*np.exp(-b*d/2-h)
        x=rng.poisson(lh,N); y=rng.poisson(la,N)
        probs[(H,A)]=((x>y).mean(),(x==y).mean(),(x<y).mean(),lh,la)
        i,j=ix[H],ix[A]
        pts[:,i]+=np.where(x>y,3,np.where(x==y,1,0)); pts[:,j]+=np.where(y>x,3,np.where(x==y,1,0))
        gd[:,i]+=x-y; gd[:,j]+=y-x; gf[:,i]+=x; gf[:,j]+=y
    gfx=np.where(np.isnan(gf),rng.uniform(15,35,gf.shape),gf)  # León GF desconocido: desempate aleatorio
    key=pts*1e6+gd*1e3+gfx+rng.uniform(0,1e-3,pts.shape)
    rank=(-key).argsort(1).argsort(1)+1
    res={t:((rank[:,ix[t]]<=8).mean(),(rank[:,ix[t]]==1).mean(),np.bincount(rank[:,ix[t]],minlength=19)[1:]/N) for t in teams}
    if verbose:
        print('MU',round(MU,3),'K',K,'HADV',HADV)
        for (H,A),p in probs.items(): print(f'{H}-{A}: L {p[0]:.3f} E {p[1]:.3f} V {p[2]:.3f}  xG {p[3]:.2f}-{p[4]:.2f}')
        for t in teams[:12]: print(f'{t:10s} top8 {res[t][0]:.3f} lider {res[t][1]:.3f}')
    return res,probs
res,probs=run()
# sensibilidad
for K,H in [(0,0.35),(16,0.35),(8,0.0),(8,0.6)]:
    r2,_=run(K,H,N=100000,verbose=False); print('sens K',K,'H',H,{t:round(r2[t][0],3) for t in ['Santos','Monterrey','León','Pachuca','Tijuana','Pumas','Querétaro']},'lider CAZ',round(r2['Cruz Azul'][1],3))
# error MC
p=res['León'][0];print('MC se León',np.sqrt(p*(1-p)/200000))
# escenarios clave: Monterrey
