"""xGol — NBA: la noche en números (v2: ataque/defensa ridge + ajuste back-to-back + Monte Carlo)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, kicker, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M

D = json.load(open(os.environ["NBA_JSON"]))
O, BT, BB = D["out"], D["bt"], D["b2b"]
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/nba")
os.makedirs(OUT, exist_ok=True)
T = 6
GAMES = [
    ("SAS@UTA", "SAS", "UTA", "19:00", "Spurs", "Jazz",
     "SAS llega en back-to-back y aun así es el favorito más claro. UTA sin Jackson Jr.; Markkanen en duda."),
    ("OKC@DAL", "OKC", "DAL", "19:30", "Thunder", "Mavericks",
     "La mejor defensa de la noche (-7.9 pts vs. promedio). OKC sin Holmgren ni Caruso; DAL sin Lively, Irving en duda."),
    ("LAL@LAC", "LAL", "LAC", "20:30", "Lakers", "Clippers",
     "El cansancio voltea el pronóstico: sin ajuste, LAL 52%. Además LAL juega sin Dončić, algo que el modelo no ve."),
]


def pct(key):
    p_home = O[key]["p_home2"]
    return 100 - p_home, p_home


def bar(d, y, a, h, pa, ph):
    bw = W - 2 * M
    d.rounded_rectangle((M, y, M + bw, y + 60), radius=14, fill=SURF)
    fav_home = ph > pa
    if fav_home:
        d.rounded_rectangle((M + bw - int(bw * ph / 100), y, M + bw, y + 60), radius=14, fill=ACC)
    else:
        d.rounded_rectangle((M, y, M + int(bw * pa / 100), y + 60), radius=14, fill=ACC)
    fn = font("InterDisplay-Bold.otf", 36)
    d.text((M + 24, y + 10), f"{a} {pa}%", font=fn, fill=TXT if fav_home else BG)
    s = f"{h} {ph}%"
    d.text((M + bw - 24 - d.textlength(s, font=fn), y + 10), s, font=fn, fill=BG if fav_home else TXT)


def cover():
    im, d = base()
    kicker(d, 110, "NBA · Miércoles 28 oct · Hora CDMX")
    f = font("InterDisplay-Black.otf", 92)
    d.text((M, 160), "El cansancio", font=f, fill=TXT)
    d.text((M, 260), "voltea un partido", font=f, fill=TXT)
    para(d, (M, 390), f"Jugar dos noches seguidas cuesta {abs(BB['eff']):.1f} puntos (p = {BB['p']:.3f}). Dos equipos lo sufren hoy.",
         font("Inter-Medium.otf", 32), MUTED, W - 2 * M, 44)
    y = 520
    for key, a, h, hour, *_ in GAMES:
        pa, ph = pct(key)
        o = O[key]
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 24
        d.text((M, y + 8), hour, font=font("Inter-SemiBold.otf", 30), fill=MUTED)
        d.text((M + 130, y - 4), f"{a} @ {h}", font=font("InterDisplay-Black.otf", 56), fill=TXT)
        fav = a if pa > ph else h
        s = f"{fav} {max(pa, ph)}%"
        fs = font("InterDisplay-Bold.otf", 44)
        d.text((W - M - d.textlength(s, font=fs), y + 2), s, font=fs, fill=ACC)
        tag = []
        if o["rest"][a] == 0: tag.append(f"{a} back-to-back")
        if o["rest"][h] == 0: tag.append(f"{h} back-to-back")
        sub = f"Proyección {a} {o['pa2']} – {o['ph2']} {h}" + ("  ·  " + ", ".join(tag) if tag else "")
        d.text((M + 130, y + 66), sub, font=font("Inter-Medium.otf", 26), fill=MUTED)
        y += 120
    d.line((M, y, W - M, y), fill=LINE, width=2)
    para(d, (M, y + 30), "100,000 simulaciones por partido. Desliza para la prueba y los números.",
         font("Inter-Regular.otf", 28), MUTED, W - 2 * M, 40)
    footer(d, 1, T)
    return im


def b2b_slide():
    im, d = base()
    kicker(d, 110, "Prueba de hipótesis · NBA 2025-26")
    f = font("InterDisplay-Black.otf", 84)
    d.text((M, 160), "¿Pesa jugar dos", font=f, fill=TXT)
    d.text((M, 252), "noches seguidas?", font=f, fill=TXT)
    eff, se = BB["eff"], BB["se"]
    lo, hi = eff - 1.96 * se, eff + 1.96 * se
    d.text((M - 6, 380), f"{eff:+.1f}", font=font("InterDisplay-Black.otf", 200), fill=ACC)
    d.text((M + 400, 440), "puntos de margen", font=font("Inter-SemiBold.otf", 34), fill=TXT)
    d.text((M + 400, 486), "vs. lo esperado por el modelo", font=font("Inter-Medium.otf", 28), fill=MUTED)
    # CI plot
    y = 660
    x0, x1 = M, W - M
    vmin, vmax = -5.0, 2.0
    X = lambda v: x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    d.line((x0, y + 40, x1, y + 40), fill=LINE, width=3)
    for v in range(-5, 3):
        d.line((X(v), y + 32, X(v), y + 48), fill=LINE, width=2)
        s = f"{v:+d}" if v else "0"
        d.text((X(v) - d.textlength(s, font=font("Inter-Medium.otf", 22)) / 2, y + 56), s, font=font("Inter-Medium.otf", 22), fill=MUTED)
    d.line((X(0), y - 10, X(0), y + 90), fill=MUTED, width=2)
    d.rounded_rectangle((X(lo), y + 28, X(hi), y + 52), radius=12, fill=ACC)
    d.ellipse((X(eff) - 16, y + 24, X(eff) + 16, y + 56), fill=TXT)
    d.text((X(lo), y - 26), f"IC 95%: {lo:.1f} a {hi:.1f}", font=font("Inter-SemiBold.otf", 26), fill=TXT)
    y += 130
    stats = [(f"{BB['n']}", "partidos en B2B (rival descansado)"), (f"{BB['p']:.3f}", "p-valor (prueba z)"), (f"{BB['eff']/ (BB['se']*BB['n']**0.5):.2f}", "tamaño del efecto (d)")]
    cw = (W - 2 * M) // 3
    for k, (v, l) in enumerate(stats):
        x = M + k * cw
        d.text((x, y), v, font=font("InterDisplay-Black.otf", 56), fill=TXT)
        para(d, (x, y + 70), l, font("Inter-Medium.otf", 24), MUTED, cw - 20, 32)
    para(d, (M, y + 170), "Veredicto: el efecto es real (p < 0.05) pero pequeño. Suficiente para mover un partido parejo, no para tumbar a un favorito claro.",
         font("Inter-Medium.otf", 29), TXT, W - 2 * M, 40)
    footer(d, 2, T)
    return im


def game_slide(i, key, a, h, hour, na, nh, story):
    im, d = base()
    o = O[key]
    pa, ph = pct(key)
    kicker(d, 110, f"{hour} CDMX · {na} @ {nh}")
    fb = font("InterDisplay-Black.otf", 120)
    d.text((M - 4, 145), a, font=fb, fill=TXT)
    wa = d.textlength(a, font=fb)
    d.text((M + wa + 20, 192), "@", font=font("InterDisplay-Medium.otf", 64), fill=MUTED)
    d.text((M + wa + 92, 145), h, font=fb, fill=TXT)
    d.text((M, 300), "Probabilidad de victoria · nuestro modelo", font=font("Inter-Medium.otf", 24), fill=MUTED)
    bar(d, 336, a, h, pa, ph)
    rest = lambda t: o["rest"][t]
    rows = [
        ("Rating neto ajustado por rival", o["net_a"], o["net_h"], "s"),
        ("Ataque vs. promedio (pts)", o["off_a"], o["off_h"], "s"),
        ("Defensa vs. promedio (pts)", -o["def_a"], -o["def_h"], "s"),
        ("Días de descanso", rest(a), rest(h), "r"),
    ]
    y = 420
    fh = font("Inter-SemiBold.otf", 22)
    cx1, cx2 = 700, 880
    d.text((cx1, y), a, font=fh, fill=MUTED); d.text((cx2, y), h, font=fh, fill=MUTED)
    y += 34
    fl = font("Inter-Medium.otf", 26)
    fv = font("InterDisplay-Bold.otf", 36)
    for lab, va, vh, kind in rows:
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 14
        d.text((M, y + 6), lab, font=fl, fill=TXT)
        for cx, v in ((cx1, va), (cx2, vh)):
            if kind == "s":
                s, col, ff = f"{v:+.1f}", (ACC if v > 0 else NEG), fv
            else:
                s, col, ff = (f"{v}" if v else "0 · B2B"), (TXT if v else NEG), (fv if v else font("InterDisplay-Bold.otf", 28))
            d.text((cx, y), s, font=ff, fill=col)
        y += 56
    d.line((M, y, W - M, y), fill=LINE, width=2)
    # simulation block
    y += 20
    d.rounded_rectangle((M, y, W - M, y + 250), radius=18, fill=SURF)
    d.text((M + 28, y + 20), "100,000 SIMULACIONES", font=font("Inter-Bold.otf", 21), fill=ACC)
    d.text((M + 28, y + 52), f"{a} {o['pa2']} – {o['ph2']} {h}", font=font("InterDisplay-Black.otf", 50), fill=TXT)
    adj = o["b2b_adj"]
    if adj:
        s = f"ajuste B2B: {adj:+.1f} para {h}"
        d.text((W - M - 28 - d.textlength(s, font=font("Inter-Medium.otf", 22)), y + 72), s, font=font("Inter-Medium.otf", 22), fill=MUTED)
    cells = [(f"{o['mlo']:+d} a {o['mhi']:+d}", f"margen {h} (80%)"), (f"{o['tlo']}–{o['thi']}", "puntos totales (80%)"),
             (f"{o['close']}%", "final por ≤5 pts"), (f"{o['blow']}%", "paliza (≥15 pts)")]
    cw = (W - 2 * M - 56) // 4
    for k, (v, l) in enumerate(cells):
        x = M + 28 + k * cw
        d.text((x, y + 138), v, font=font("InterDisplay-Bold.otf", 32), fill=TXT)
        para(d, (x, y + 182), l, font("Inter-Medium.otf", 20), MUTED, cw - 12, 26)
    y += 276
    para(d, (M, y), story, font("Inter-Medium.otf", 27), TXT, W - 2 * M, 38)
    footer(d, i, T)
    return im


def method():
    im, d = base()
    kicker(d, 110, "Cómo lo calculamos")
    d.text((M, 160), "Modelo NBA v2", font=font("InterDisplay-Black.otf", 84), fill=TXT)
    items = [
        "Cada marcador = ataque propio + defensa rival + localía (regresión ridge). Punto de partida: 60% del nivel 2025-26.",
        f"Ajuste por back-to-back: {BB['eff']:+.1f} pts, estimado con {BB['n']} partidos de 2025-26.",
        f"Margen ~ Normal(proyección, σ = {BT['sd']:.1f}); total ~ Normal(proyección, σ = {BB['totsd']:.1f}). 100,000 simulaciones.",
    ]
    y = 290
    for n, t in enumerate(items, 1):
        d.text((M, y - 6), str(n), font=font("InterDisplay-Black.otf", 48), fill=ACC)
        y = max(para(d, (M + 66, y), t, font("Inter-Medium.otf", 28), TXT, W - 2 * M - 66, 38), y + 38) + 24
    y += 6
    d.rounded_rectangle((M, y, W - M, y + 300), radius=20, fill=SURF)
    d.text((M + 32, y + 24), "PRUEBA FUERA DE MUESTRA · 2025-26", font=font("Inter-Bold.otf", 22), fill=ACC)
    para(d, (M + 32, y + 58), f"{BT['n']:,} partidos predichos solo con datos previos a cada día.",
         font("Inter-Regular.otf", 25), MUTED, W - 2 * M - 64, 32)
    cols = [(f"{100*BT['acc']:.0f}%", "aciertos"), (f"{BT['brier']:.3f}", f"Brier (ref. {BT['base']:.3f})"), ("81%", "ganó cuando dijo 70-80%")]
    cw = (W - 2 * M - 64) // 3
    for k, (v, l) in enumerate(cols):
        x = M + 32 + k * cw
        d.text((x, y + 120), v, font=font("InterDisplay-Black.otf", 60), fill=TXT)
        para(d, (x, y + 198), l, font("Inter-Medium.otf", 23), MUTED, cw - 20, 30)
    y += 326
    para(d, (M, y), "Límites: no ve lesiones ni rotaciones; en octubre hay pocos partidos por equipo. Menor Brier = mejor.",
         font("Inter-Regular.otf", 25), MUTED, W - 2 * M, 34)
    para(d, (M, H - 175), "Datos: BALLDONTLIE y reportes de lesiones públicos al 28 oct. Análisis independiente, no afiliado a la NBA ni a sus equipos. No es recomendación de apuesta.",
         font("Inter-Regular.otf", 19), MUTED, W - 2 * M, 26)
    footer(d, 6, T)
    return im


if __name__ == "__main__":
    cover().save(f"{OUT}/01.png")
    b2b_slide().save(f"{OUT}/02.png")
    for i, g in enumerate(GAMES, 3):
        game_slide(i, *g).save(f"{OUT}/{i:02d}.png")
    method().save(f"{OUT}/06.png")
    print(sorted(os.listdir(OUT)))
