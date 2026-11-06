import pandas as pd,numpy as np; from scipy.stats import norm, ttest_1samp, binomtest, ttest_ind
g=pd.read_csv('games.csv'); g=g[g.home_score.notna()&(g.game_type=='REG')&(g.season<2026)&g.spread_line.notna()]
g['margin']=g.home_score-g.away_score; g['tot']=g.home_score+g.away_score
g['res']=g.margin-g.spread_line; g['tres']=g.tot-g.total_line
I=g[g.location=='Neutral']; H=g[g.location=='Home']
print('neutral n',len(I), I.season.min(), I.season.max())
print(I.groupby('season').size().to_dict())
for lab,s in [('intl',I),('home',H)]:
    fav=np.where(s.spread_line>0, s.margin>0, s.margin<0); push=s.spread_line==0
    e=norm.cdf(abs(s.spread_line)/13.5)
    print(lab,'fav win',fav[~push].mean(),'exp',e[~push].mean(),'n',(~push).sum())
    print(lab,'margin-res mean',s.res.mean(),'sd',s.res.std(),'tot-res mean',s.tres.mean(), 'p tot',ttest_1samp(s.tres,0).pvalue,'p marg',ttest_1samp(s.res,0).pvalue)
    print(lab,'avg total',s.tot.mean(),'avg line',s.total_line.mean())
fav=np.where(I.spread_line>0, I.margin>0, I.margin<0); push=I.spread_line==0
k=fav[~push].sum(); n=(~push).sum(); e=norm.cdf(abs(I.spread_line[~push])/13.5).mean()
print('binom fav', k,n, binomtest(int(k),int(n),e).pvalue)
# favorites' margin vs expected
fm=np.where(I.spread_line>0,I.res,-I.res); print('fav margin over exp',fm.mean(), ttest_1samp(fm,0).pvalue, 'cohen d',fm.mean()/fm.std())
print('totals diff intl vs home', ttest_ind(I.tres,H.tres,equal_var=False).pvalue, (I.tres.mean()-H.tres.mean())/g.tres.std())
# designated home team win rate intl
print('designated home win', (I.margin>0).mean(), 'exp', norm.cdf(I.spread_line/13.5).mean())
# model CIN ATL
p=pd.read_csv('pbp.csv.gz',low_memory=False); p=p[p.play_type.isin(['pass','run'])&p.epa.notna()]
off=p.groupby('posteam').epa.mean(); de=p.groupby('defteam').epa.mean(); net=off-de
print('CIN',off['CIN'],de['CIN'],'ATL',off['ATL'],de['ATL'])
print('off rank CIN',off.rank(ascending=False)['CIN'],'ATL',off.rank(ascending=False)['ATL'],'def rank (lower better) CIN',de.rank()['CIN'],'ATL',de.rank()['ATL'])
m=0.5*(net['CIN']-net['ATL'])*61.6; print('margin CIN',m,'P',norm.cdf(m/13.5))
for f in [.35,.65]: print(f, norm.cdf(f*(net['CIN']-net['ATL'])*61.6/13.5))
pa=p[p.posteam=='CIN']; print('CIN pass epa',pa[pa.play_type=='pass'].epa.mean(),'run',pa[pa.play_type=='run'].epa.mean())
pa=p[p.defteam=='ATL']; print('ATL def pass',pa[pa.play_type=='pass'].epa.mean(),'run',pa[pa.play_type=='run'].epa.mean())
pa=p[p.posteam=='ATL']; print('ATL pass epa',pa[pa.play_type=='pass'].epa.mean(),'run',pa[pa.play_type=='run'].epa.mean())
pa=p[p.defteam=='CIN']; print('CIN def pass',pa[pa.play_type=='pass'].epa.mean(),'run',pa[pa.play_type=='run'].epa.mean())
print('success',p[p.posteam=='CIN'].success.mean(),p[p.posteam=='ATL'].success.mean())
