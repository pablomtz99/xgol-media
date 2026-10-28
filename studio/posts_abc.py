"""xGol — posts A (hipótesis localía), B (récord vs realidad), C (power ranking S8)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, kicker, wrap, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M, OUT
import pandas as pd
from PIL import ImageDraw

D = os.environ.get("XGOL_DATA", "/tmp/xgol-data/")
t = pd.read_csv(D + "team_2026_thru_w7.csv", index_col=0)
t["wpct"] = (t.w + 0.5 * t.t) / t.gp

def title(d, y, lines, size=88):
    f = font("InterDisplay-Black.otf", size)
    for ln in lines:
        d.text((M, y), ln, font=f, fill=TXT); y += int(size * 1.1)
    return y

def fx(v):
    v = round(v, 2)
    return "0.00" if v == 0 else f"{v:+.2f}"

def rec(team):
    r = t.loc[team]
    s = f"{int(r.w)}-{int(r.l)}"
    if r.t: s += f"-{int(r.t)}"
    return s

# ======================= POST A =======================
SEASONS = list(range(2015, 2027))
HM = [1.48, 2.60, 2.50, 2.34, -0.05, 0.14, 1.57, 2.12, 2.71, 1.72, 2.18, -0.07]
TA = 4

def a1():
    im, d = base()
    kicker(d, 110, "NFL · Prueba de hipótesis")
    y = title(d, 160, ["¿Se acabó", "la ventaja", "de local?"], 104)
    y += 40
    fb = font("InterDisplay-Black.otf", 150)
    fl = font("Inter-Medium.otf", 32)
    d.text((M, y), "−0.1", font=fb, fill=NEG)
    para(d, (M + 330, y + 30), "puntos de margen promedio para el local en 2026 (semanas 1–7).", fl, TXT, W - 2 * M - 330, 44)
    y += 210
    d.text((M, y), "+1.8", font=fb, fill=ACC)
    para(d, (M + 330, y + 30), "puntos era el promedio de 2015 a 2025.", fl, TXT, W - 2 * M - 330, 44)
    footer(d, 1, TA)
    return im

def a2():
    im, d = base()
    kicker(d, 110, "Margen del local por temporada")
    title(d, 160, ["12 temporadas"], 88)
    para(d, (M, 270), "Puntos promedio que gana el equipo local. Solo partidos en casa (sin sedes neutrales).",
         font("Inter-Regular.otf", 30), MUTED, W - 2 * M, 42)
    # chart
    x0, x1, yb, ytop = M + 20, W - M, 1050, 470
    vmax = 3.0
    zero = yb - (0 - (-1)) * 0  # placeholder
    # scale from -1 to 3
    def Y(v): return yb - (v + 1) / 4.0 * (yb - ytop)
    fz = font("Inter-Medium.otf", 22)
    for v in [-1, 0, 1, 2, 3]:
        yy = Y(v)
        d.line((x0, yy, x1, yy), fill=LINE if v else MUTED, width=2 if v else 3)
        d.text((M - 40, yy - 14), f"{v:+d}" if v else "0", font=fz, fill=MUTED)
    n = len(SEASONS)
    slot = (x1 - x0) / n
    bw = slot * 0.62
    fy = font("Inter-Medium.otf", 21)
    fv = font("InterDisplay-Bold.otf", 22)
    for i, (s, v) in enumerate(zip(SEASONS, HM)):
        cx = x0 + slot * (i + 0.5)
        col = NEG if s == 2026 else (MUTED if s == 2020 else ACC)
        y0, y1 = sorted([Y(0), Y(v)])
        if y1 - y0 < 4: y0, y1 = Y(0) - 2, Y(0) + 4
        d.rounded_rectangle((cx - bw / 2, y0, cx + bw / 2, y1), radius=6, fill=col)
        lab = f"{v:+.1f}"
        ly = Y(v) - 34 if v >= 0 else Y(v) + 8
        if s in (2019, 2026): ly = Y(0) - 34
        d.text((cx - d.textlength(lab, font=fv) / 2, ly), lab, font=fv, fill=TXT)
        ys = f"'{str(s)[2:]}"
        d.text((cx - d.textlength(ys, font=fy) / 2, yb + 18), ys, font=fy, fill=MUTED)
    fn = font("Inter-Regular.otf", 28)
    y = para(d, (M, 1110), "2020 (gris): estadios casi sin aficionados por la pandemia, y la ventaja también se esfumó.",
             fn, MUTED, W - 2 * M, 40)
    footer(d, 2, TA)
    return im

def a3():
    im, d = base()
    kicker(d, 110, "La prueba")
    y = title(d, 160, ["¿Es real o", "es ruido?"], 96)
    y += 30
    blocks = [
        ("Hipótesis 1", "La ventaja de local es cero.", "p = 0.96", "No podemos rechazarla: no hay evidencia de ventaja de local en 2026.", ACC),
        ("Hipótesis 2", "La ventaja sigue en +1.8 puntos, como siempre.", "p = 0.15", "Tampoco podemos rechazarla: no hay evidencia de que haya desaparecido.", ACC),
    ]
    for tag, h0, p, concl, col in blocks:
        d.rounded_rectangle((M, y, W - M, y + 300), radius=24, fill=SURF)
        d.text((M + 36, y + 30), tag.upper(), font=font("Inter-SemiBold.otf", 24), fill=MUTED)
        d.text((M + 36, y + 66), h0, font=font("Inter-SemiBold.otf", 32), fill=TXT)
        d.text((M + 36, y + 120), p, font=font("InterDisplay-Black.otf", 72), fill=col)
        para(d, (M + 36, y + 210), concl, font("Inter-Regular.otf", 28), MUTED, W - 2 * M - 72, 38)
        y += 330
    para(d, (M, y + 10), "p = probabilidad de ver datos así si la hipótesis fuera cierta. Si es alta, no hay forma de descartarla.",
         font("Inter-Regular.otf", 26), MUTED, W - 2 * M, 36)
    footer(d, 3, TA)
    return im

def a4():
    im, d = base()
    kicker(d, 110, "Veredicto")
    y = title(d, 160, ["Inconcluso", "(y eso también", "es un dato)"], 88)
    y += 40
    pts = [
        "101 partidos: 51 ganó el local, 49 el visitante y 1 empate.",
        "El margen varía tanto entre partidos (±12.7 puntos) que el promedio todavía tiene un error de ±1.3 puntos.",
        "Rango plausible para 2026: de −2.5 a +2.4 puntos. Cabe tanto el cero como el histórico.",
        "Lo volvemos a medir en la semana 14, con el doble de partidos.",
    ]
    fp = font("Inter-Medium.otf", 32)
    for p in pts:
        d.ellipse((M, y + 14, M + 14, y + 28), fill=ACC)
        y = para(d, (M + 36, y), p, fp, TXT, W - 2 * M - 36, 44) + 26
    para(d, (M, 1130), "Datos: nflverse (CC-BY 4.0), temporadas regulares 2015–2026. Prueba t de una muestra sobre el margen del local.",
         font("Inter-Regular.otf", 24), MUTED, W - 2 * M, 34)
    footer(d, 4, TA)
    return im

# ======================= POST B =======================
TB = 3
LUCKY = ["CLE", "PIT", "DEN"]
UNLUCKY = ["LA", "JAX", "TB"]

def b1():
    im, d = base()
    kicker(d, 110, "NFL · Semanas 1–7")
    y = title(d, 160, ["Récord", "vs. realidad"], 112)
    y += 30
    para(d, (M, y), "El récord dice quién ganó. La EPA por jugada dice quién jugó mejor. Cuando no coinciden, casi siempre hay suerte de por medio.",
         font("Inter-Regular.otf", 38), MUTED, W - 2 * M, 52)
    y += 260
    fb = font("InterDisplay-Black.otf", 64)
    fl = font("Inter-Medium.otf", 30)
    d.text((M, y), "5-2", font=fb, fill=NEG)
    d.text((M + 170, y + 18), "Browns · 21° en EPA neta", font=fl, fill=TXT)
    y += 110
    d.text((M, y), "3-4", font=fb, fill=ACC)
    d.text((M + 170, y + 18), "Rams · 5° en EPA neta", font=fl, fill=TXT)
    footer(d, 1, TB)
    return im

def b2():
    im, d = base()
    kicker(d, 110, "Los 32 equipos")
    title(d, 160, ["¿Quién está", "fuera de lugar?"], 84)
    x0, x1, y0, y1 = M + 60, W - M - 10, 420, 1120
    xs, ys = t.net_epa, t.wpct
    xmin, xmax = -0.26, 0.26
    def X(v): return x0 + (v - xmin) / (xmax - xmin) * (x1 - x0)
    def Y(v): return y1 - v * (y1 - y0)
    fz = font("Inter-Medium.otf", 20)
    for v in [0, 0.25, 0.5, 0.75, 1.0]:
        d.line((x0, Y(v), x1, Y(v)), fill=LINE, width=2)
        d.text((M - 10, Y(v) - 12), f"{int(v*100)}%", font=fz, fill=MUTED)
    d.line((X(0), y0, X(0), y1), fill=LINE, width=2)
    # simple OLS line
    import numpy as np
    b, a = np.polyfit(xs, ys, 1)
    d.line((X(xmin), Y(a + b * xmin), X(xmax), Y(a + b * xmax)), fill=MUTED, width=3)
    fl = font("InterDisplay-Bold.otf", 22)
    for team, r in t.iterrows():
        cx, cy = X(r.net_epa), Y(r.wpct)
        col = NEG if team in LUCKY else (ACC if team in UNLUCKY else "#4A5566")
        rad = 12 if col != "#4A5566" else 8
        d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=col)
        if team in UNLUCKY:
            d.text((cx + 16, cy - 13), team, font=fl, fill=col)
    lx, ly = X(t.loc[LUCKY].net_epa.mean()), Y(t.loc[LUCKY].wpct.mean())
    d.text((lx - 250, ly - 50), "CLE · PIT · DEN", font=fl, fill=NEG)
    d.text((x0, y1 + 20), "← peor", font=fz, fill=MUTED)
    s = "mejor →"
    d.text((x1 - d.textlength(s, font=fz), y1 + 20), s, font=fz, fill=MUTED)
    s = "EPA neta por jugada"
    fa = font("Inter-SemiBold.otf", 24)
    d.text(((x0 + x1) / 2 - d.textlength(s, font=fa) / 2, y1 + 18), s, font=fa, fill=TXT)
    d.text((M - 10, y0 - 50), "% de victorias", font=fa, fill=TXT)
    fn = font("Inter-Regular.otf", 24)
    d.ellipse((M, 1200, M + 18, 1218), fill=NEG); d.text((M + 28, 1194), "Récord mejor que su juego", font=fn, fill=TXT)
    d.ellipse((M + 420, 1200, M + 438, 1218), fill=ACC); d.text((M + 448, 1194), "Juego mejor que su récord", font=fn, fill=TXT)
    footer(d, 2, TB)
    return im

def b3():
    im, d = base()
    kicker(d, 110, "Candidatos a regresar a la media")
    y = title(d, 160, ["La lista"], 96)
    y += 20
    def section(y, head, teams, col, names):
        d.text((M, y), head, font=font("Inter-SemiBold.otf", 30), fill=col)
        y += 56
        for tm in teams:
            r = t.loc[tm]
            d.line((M, y, W - M, y), fill=LINE, width=2)
            y += 22
            d.text((M, y), names[tm], font=font("InterDisplay-Bold.otf", 44), fill=TXT)
            s = f"{rec(tm)}  ·  {int(r.net_epa_rk)}° en EPA neta"
            fs = font("Inter-Medium.otf", 30)
            d.text((W - M - d.textlength(s, font=fs), y + 10), s, font=fs, fill=MUTED)
            y += 78
        return y + 30
    names = {"CLE": "Browns", "PIT": "Steelers", "DEN": "Broncos", "LA": "Rams", "JAX": "Jaguars", "TB": "Buccaneers"}
    y = section(y, "Récord inflado: cuidado", LUCKY, NEG, names)
    y = section(y, "Mejores de lo que dice su récord", UNLUCKY, ACC, names)
    para(d, (M, 1150), "El récord mezcla calidad con suerte (partidos cerrados, balones sueltos). La EPA mide jugada por jugada. Datos: nflverse (CC-BY 4.0).",
         font("Inter-Regular.otf", 24), MUTED, W - 2 * M, 34)
    footer(d, 3, TB)
    return im

# ======================= POST C =======================
TC = 2
NAMES = {"SF":"49ers","JAX":"Jaguars","KC":"Chiefs","CIN":"Bengals","LA":"Rams","MIN":"Vikings","SEA":"Seahawks",
"BUF":"Bills","BAL":"Ravens","GB":"Packers","CHI":"Bears","CAR":"Panthers","NE":"Patriots","TB":"Buccaneers",
"NYJ":"Jets","DEN":"Broncos","DET":"Lions","NYG":"Giants","PIT":"Steelers","HOU":"Texans","CLE":"Browns",
"ATL":"Falcons","DAL":"Cowboys","LV":"Raiders","WAS":"Commanders","NO":"Saints","IND":"Colts","ARI":"Cardinals",
"MIA":"Dolphins","LAC":"Chargers","TEN":"Titans","PHI":"Eagles"}
order = t.sort_values("net_epa", ascending=False).index.tolist()

def c1():
    im, d = base()
    kicker(d, 110, "NFL · Semana 8")
    title(d, 160, ["Power ranking", "xGol"], 96)
    para(d, (M, 390), "Ordenado por EPA neta por jugada (ataque menos defensa), semanas 1–7.",
         font("Inter-Regular.otf", 30), MUTED, W - 2 * M, 42)
    y = 485
    fr = font("InterDisplay-Black.otf", 44)
    fn = font("InterDisplay-Bold.otf", 42)
    fs = font("Inter-Medium.otf", 28)
    vmax = t.net_epa.max()
    for i, tm in enumerate(order[:10]):
        r = t.loc[tm]
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 14
        d.text((M, y), f"{i+1}", font=fr, fill=ACC)
        d.text((M + 80, y), NAMES[tm], font=fn, fill=TXT)
        s = f"{rec(tm)}   {fx(r.net_epa)}"
        d.text((W - M - d.textlength(s, font=fs), y + 10), s, font=fs, fill=MUTED)
        # mini bar
        bw = (W - 2 * M - 80) * r.net_epa / vmax * 0.35
        d.rounded_rectangle((M + 80, y + 54, M + 80 + bw, y + 60), radius=3, fill=ACC)
        y += 59
    footer(d, 1, TC)
    return im

def c2():
    im, d = base()
    kicker(d, 110, "Del 11 al 32")
    title(d, 160, ["El resto"], 96)
    y0 = 320
    fr = font("InterDisplay-Bold.otf", 30)
    fn = font("Inter-Medium.otf", 30)
    fs = font("Inter-Regular.otf", 24)
    colw = (W - 2 * M) / 2
    for k, tm in enumerate(order[10:]):
        col, row = divmod(k, 11)
        x = M + col * colw
        y = y0 + row * 78
        r = t.loc[tm]
        d.text((x, y), f"{k+11}", font=fr, fill=ACC if r.net_epa > 0 else NEG)
        d.text((x + 64, y), NAMES[tm], font=fn, fill=TXT)
        d.text((x + 64, y + 38), f"{rec(tm)} · {fx(r.net_epa)}", font=fs, fill=MUTED)
    para(d, (M, 1180), "EPA = puntos esperados que suma cada jugada. Datos: nflverse (CC-BY 4.0).",
         font("Inter-Regular.otf", 24), MUTED, W - 2 * M, 34)
    footer(d, 2, TC)
    return im

if __name__ == "__main__":
    for name, fns in {"a": [a1, a2, a3, a4], "b": [b1, b2, b3], "c": [c1, c2]}.items():
        for i, fn in enumerate(fns, 1):
            fn().save(f"{OUT}/xgol_{name}_{i}.png")
    print(sorted(os.listdir(OUT)))
