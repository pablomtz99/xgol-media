"""Modelo NBA v1 (reconstruido 3 nov sin acceso a xgol-data): puntos local = mu + h/2 + A_local - D_visita;
puntos visita = mu - h/2 + A_visita - D_local. Ridge (λ=16) hacia un prior = 90% del nivel 2025-26
(neto ≈ (V-41)/2.7 por récord final, mitad ataque / mitad defensa). P(gana) = Φ(margen/σ), σ=14.7.
Datos: marcadores 2026-27 (Land of Basketball), ruta en $NBA_CSV (no se versiona)."""
import os, numpy as np, pandas as pd
from scipy.stats import norm
CSV = os.environ.get("NBA_CSV", "nba_2627.csv")
W25 = {"Hawks":46,"Celtics":56,"Nets":20,"Hornets":44,"Bulls":31,"Cavaliers":52,"Mavericks":26,"Nuggets":54,"Pistons":60,
"Warriors":37,"Rockets":52,"Pacers":19,"Clippers":42,"Lakers":53,"Grizzlies":25,"Heat":43,"Bucks":32,"Timberwolves":49,
"Pelicans":26,"Knicks":53,"Thunder":64,"Magic":45,"76ers":45,"Suns":45,"Trail Blazers":42,"Kings":22,"Spurs":62,
"Raptors":46,"Jazz":22,"Wizards":17}
T = sorted(W25); ix = {t: i for i, t in enumerate(T)}; n = len(T)
PRIOR = np.array([0.9 * (W25[t] - 41) / 2.7 for t in T])
LAM, SIG, H0 = 16.0, 14.7, 2.0

def load():
    return pd.read_csv(CSV)

def fit(d, lam=LAM):
    # params: a(30), d(30), mu, h
    rows, y, w = [], [], []
    for r in d.itertuples():
        i, j = ix[r.home], ix[r.visitor]
        x = np.zeros(2 * n + 2); x[i] = 1; x[n + j] = -1; x[-2] = 1; x[-1] = .5; rows.append(x); y.append(r.hpts)
        x = np.zeros(2 * n + 2); x[j] = 1; x[n + i] = -1; x[-2] = 1; x[-1] = -.5; rows.append(x); y.append(r.vpts)
    X = np.array(rows); y = np.array(y, float)
    P = np.zeros((2 * n + 2, 2 * n + 2)); t = np.zeros(2 * n + 2)
    P[:2 * n, :2 * n] = np.eye(2 * n) * lam; t[:n] = PRIOR / 2; t[n:2 * n] = PRIOR / 2
    P[-1, -1] = 4.0; t[-1] = H0
    b = np.linalg.solve(X.T @ X + P, X.T @ y + P @ t)
    return b

def pred(b, home, vis):
    i, j = ix[home], ix[vis]; a, dd, mu, h = b[:n], b[n:2 * n], b[-2], b[-1]
    ph = mu + h / 2 + a[i] - dd[j]; pv = mu - h / 2 + a[j] - dd[i]
    m = ph - pv
    return dict(m=m, p=norm.cdf(m / SIG), tot=ph + pv, ph=ph, pv=pv)

def net(b, t):
    return b[ix[t]] + b[n + ix[t]]

def validate(d):
    dates = sorted(d.date.unique()); out = []
    for dt in dates[3:]:
        tr = d[d.date < dt]; te = d[d.date == dt]; b = fit(tr)
        for r in te.itertuples():
            p = pred(b, r.home, r.visitor)["p"]; p0 = norm.cdf((PRIOR[ix[r.home]] - PRIOR[ix[r.visitor]] + H0) / SIG)
            o = float(r.hpts > r.vpts); out.append((p, p0, o))
    o = np.array(out)
    return dict(n=len(o), brier=((o[:, 0] - o[:, 2]) ** 2).mean(), brier_prior=((o[:, 1] - o[:, 2]) ** 2).mean(),
                brier_coin=0.25, hits=((o[:, 0] > .5) == (o[:, 2] == 1)).mean(), arr=o)

def boot(d, games, B=400, seed=7):
    rng = np.random.default_rng(seed); R = []
    for _ in range(B):
        s = d.iloc[rng.integers(0, len(d), len(d))]; b = fit(s); R.append([pred(b, h, v)["p"] for h, v in games])
    R = np.array(R); return np.percentile(R, 10, 0), np.percentile(R, 90, 0)
