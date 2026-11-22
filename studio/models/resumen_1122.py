"""Resumen sáb 21 nov: 3 partidos con probabilidades fijadas ANTES (commits 9a28c51 y ee90b02; no publicados por falta de aprobación).
Pumas–Monterrey (ligamx_pum_mty_1120.py), Newcastle–Arsenal (epl_new_ars_1120 en portadas_1120), Tigres–América (ligamx_liderato_1121.py).
Resultados: Pumas 0-2 Monterrey (Bolavip, Noticias MXM); Newcastle 2-2 Arsenal (ESPN UK, Arseblog, arsenal.com titular); Tigres 1-0 América (Noticias MXM, Heraldo de México, SDP)."""
import numpy as np
# (local, visita, p_local, p_empate, p_visita, resultado idx 0=L 1=E 2=V)
G=[("Pumas","Monterrey",.421,.240,.339,2),("Newcastle","Arsenal",.278,.249,.473,1),("Tigres","América",.254,.228,.518,0)]
P=np.array([g[2:5] for g in G]);r=np.array([g[5] for g in G]);O=np.eye(3)[r]
fav=P.argmax(1);hit=(fav==r);print('aciertos',hit.sum(),'esperados',P.max(1).sum().round(2))
print('P(0 aciertos)',np.prod(1-P.max(1)).round(3))
br=((P-O)**2).sum(1);print('Brier 3 res por partido',br.round(3),'media',br.mean().round(3),'uniforme',round(2/3,3))
c=np.cumsum(P,1)[:,:2];co=np.cumsum(O,1)[:,:2];rps=((c-co)**2).sum(1)/2;print('RPS',rps.round(3),'media',rps.mean().round(3),'uniforme por partido',[round(((np.cumsum([1/3]*3)[:2]-x)**2).sum()/2,3) for x in co])
print('prob dada al resultado real',P[np.arange(3),r].round(3),'media',P[np.arange(3),r].mean().round(3))
rng=np.random.default_rng(1122);N=200000;U=rng.random((N,3));R=(U[:,:,None]>np.cumsum(P,1)[None]).sum(2)
Bs=((P[None]-np.eye(3)[R])**2).sum(2).mean(1);print('Brier esperado si calibrado',Bs.mean().round(3),'80%',np.percentile(Bs,[10,90]).round(3),'P(B>=obs)',(Bs>=br.mean()).mean().round(3))
H=(R==fav[None]).sum(1);print('dist aciertos',[(H==k).mean().round(3) for k in range(4)])
