"""xGol — NBA: la noche en números (v2, modelo ataque/defensa ajustado por rival)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, kicker, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M

D = json.load(open(os.environ["NBA_JSON"]))
O, BT = D["out"], D["bt"]
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/nba")
os.makedirs(OUT, exist_ok=True)
T = 5
GAMES = [
    ("SAS@UTA", "SAS", "UTA", "19:00", "Spurs", "Jazz",
     "Bajas: UTA sin Jackson Jr. y con Markkanen en duda. SAS juega su segundo partido en dos noches; aun así, la mayor brecha defensiva de la noche (8.9 pts) es a su favor."),
    ("OKC@DAL", "OKC", "DAL", "19:30", "Thunder", "Mavericks",
     "La defensa de OKC es la mejor de la noche: permite 7.9 pts menos que el promedio. Bajas: OKC sin Holmgren ni Caruso; DAL sin Lively e Irving en duda."),
    ("LAL@LAC", "LAL", "LAC", "20:30", "Lakers", "Clippers",
     "Ojo: el modelo no ve lesiones. Sin Dončić (espalda), el 52% de LAL probablemente está inflado. LAC sin Ingram, Beal ni Hachimura; LAL en segunda noche seguida."),
]


def pct(key):
    p_home = O[key]["p_home"]
    return 100 - p_home, p_home


def bar(d, y, a, h, pa, ph):
    bw = W - 2 * M
    d.rounded_rectangle((M, y, M + bw, y + 64), radius=14, fill=SURF)
    fav_home = ph > pa
    if fav_home:
        d.rounded_rectangle((M + bw - int(bw * ph / 100), y, M + bw, y + 64), radius=14, fill=ACC)
    else:
        d.rounded_rectangle((M, y, M + int(bw * pa / 100), y + 64), radius=14, fill=ACC)
    fn = font("InterDisplay-Bold.otf", 38)
    d.text((M + 24, y + 10), f"{a} {pa}%", font=fn, fill=TXT if fav_home else BG)
    s = f"{h} {ph}%"
    d.text((M + bw - 24 - d.textlength(s, font=fn), y + 10), s, font=fn, fill=BG if fav_home else TXT)


def cover():
    im, d = base()
    kicker(d, 110, "NBA · Miércoles 28 oct · Hora CDMX")
    f = font("InterDisplay-Black.otf", 104)
    d.text((M, 160), "La noche", font=f, fill=TXT)
    d.text((M, 274), "en números", font=f, fill=TXT)
    y = 470
    for key, a, h, hour, *_ in GAMES:
        pa, ph = pct(key)
        o = O[key]
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 26
        d.text((M, y + 8), hour, font=font("Inter-SemiBold.otf", 30), fill=MUTED)
        d.text((M + 130, y - 4), f"{a} @ {h}", font=font("InterDisplay-Black.otf", 58), fill=TXT)
        fav = a if pa > ph else h
        s = f"{fav} {max(pa, ph)}%"
        fs = font("InterDisplay-Bold.otf", 44)
        d.text((W - M - d.textlength(s, font=fs), y + 2), s, font=fs, fill=ACC)
        proj = f"Proyección {a} {o['pa']:.0f} – {o['ph']:.0f} {h}"
        d.text((M + 130, y + 70), proj, font=font("Inter-Medium.otf", 28), fill=MUTED)
        y += 128
    d.line((M, y, W - M, y), fill=LINE, width=2)
    para(d, (M, y + 36), "Probabilidad de victoria y marcador proyectado con nuestro modelo de ataque y defensa ajustados por rival. Desliza.",
         font("Inter-Regular.otf", 30), MUTED, W - 2 * M, 42)
    footer(d, 1, T)
    return im


def game_slide(i, key, a, h, hour, na, nh, story):
    im, d = base()
    o = O[key]
    pa, ph = pct(key)
    kicker(d, 110, f"{hour} CDMX · {na} @ {nh}")
    fb = font("InterDisplay-Black.otf", 140)
    d.text((M - 4, 150), a, font=fb, fill=TXT)
    wa = d.textlength(a, font=fb)
    d.text((M + wa + 24, 206), "@", font=font("InterDisplay-Medium.otf", 76), fill=MUTED)
    d.text((M + wa + 106, 150), h, font=fb, fill=TXT)
    d.text((M, 340), "Probabilidad de victoria · nuestro modelo", font=font("Inter-Medium.otf", 26), fill=MUTED)
    bar(d, 382, a, h, pa, ph)
    rows = [
        ("Rating neto ajustado por rival", o["net_a"], o["net_h"], True),
        ("Ataque vs. promedio (pts)", o["off_a"], o["off_h"], True),
        ("Defensa vs. promedio (pts)", -o["def_a"], -o["def_h"], True),
        ("Días de descanso", o["rest"][a], o["rest"][h], False),
    ]
    y = 482
    fh = font("Inter-SemiBold.otf", 24)
    cx1, cx2 = 700, 880
    d.text((cx1, y), a, font=fh, fill=MUTED); d.text((cx2, y), h, font=fh, fill=MUTED)
    y += 40
    fl = font("Inter-Medium.otf", 28)
    fv = font("InterDisplay-Bold.otf", 40)
    for lab, va, vh, signed in rows:
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 18
        d.text((M, y + 8), lab, font=fl, fill=TXT)
        for cx, v in ((cx1, va), (cx2, vh)):
            if signed:
                s, col = f"{v:+.1f}", (ACC if v > 0 else NEG)
            else:
                s, col = (f"{v}" if v else "0 (B2B)"), (TXT if v else NEG)
            d.text((cx, y), s, font=fv if signed or v else font("InterDisplay-Bold.otf", 32), fill=col)
        y += 66
    d.line((M, y, W - M, y), fill=LINE, width=2)
    y += 22
    fav, m = (h, o["margin"]) if o["margin"] > 0 else (a, -o["margin"])
    d.text((M, y), "Marcador proyectado", font=font("Inter-Medium.otf", 26), fill=MUTED)
    s = f"{a} {o['pa']:.0f} – {o['ph']:.0f} {h}"
    d.text((M, y + 36), s, font=font("InterDisplay-Black.otf", 54), fill=TXT)
    lo, hi = o["lo"], o["hi"]
    rng = f"Margen {h}: {lo:+.0f} a {hi:+.0f} (80%)"
    d.text((W - M - d.textlength(rng, font=font("Inter-Medium.otf", 26)), y + 56), rng, font=font("Inter-Medium.otf", 26), fill=MUTED)
    y += 116
    d.line((M, y, W - M, y), fill=LINE, width=2)
    para(d, (M, y + 26), story, font("Inter-Medium.otf", 29), TXT, W - 2 * M, 40)
    footer(d, i, T)
    return im


def method():
    im, d = base()
    kicker(d, 110, "Cómo lo calculamos")
    f = font("InterDisplay-Black.otf", 88)
    d.text((M, 160), "Modelo NBA v1", font=f, fill=TXT)
    items = [
        ("1", "Cada marcador se descompone en ataque de un equipo + defensa del rival + localía (regresión ridge)."),
        ("2", "Punto de partida: 60% del nivel 2025-26. Cada partido nuevo pesa más que el anterior."),
        ("3", f"Error típico ±{BT['sd']:.1f} pts por partido → probabilidad e intervalo del 80%."),
    ]
    y = 300
    for n, t in items:
        d.text((M, y - 6), n, font=font("InterDisplay-Black.otf", 50), fill=ACC)
        y = max(para(d, (M + 70, y), t, font("Inter-Medium.otf", 30), TXT, W - 2 * M - 70, 41), y + 41) + 28
    # backtest box
    y += 6
    d.rounded_rectangle((M, y, W - M, y + 330), radius=20, fill=SURF)
    d.text((M + 32, y + 26), "PRUEBA FUERA DE MUESTRA · 2025-26", font=font("Inter-Bold.otf", 22), fill=ACC)
    para(d, (M + 32, y + 62), f"{BT['n']:,} partidos predichos solo con datos previos a cada día.",
         font("Inter-Regular.otf", 26), MUTED, W - 2 * M - 64, 34)
    cols = [(f"{100*BT['acc']:.0f}%", "aciertos"), (f"{BT['brier']:.3f}", f"Brier (ref. {BT['base']:.3f})"), ("81%", "ganó cuando dijo 70-80%")]
    cw = (W - 2 * M - 64) // 3
    for k, (v, l) in enumerate(cols):
        x = M + 32 + k * cw
        d.text((x, y + 136), v, font=font("InterDisplay-Black.otf", 64), fill=TXT)
        para(d, (x, y + 220), l, font("Inter-Medium.otf", 24), MUTED, cw - 20, 32)
    y += 360
    para(d, (M, y), "Límites: no ve lesiones ni rotaciones, y en octubre hay pocos partidos. Menor Brier = mejor.",
         font("Inter-Regular.otf", 26), MUTED, W - 2 * M, 36)
    para(d, (M, H - 175), "Datos: BALLDONTLIE y reportes de lesiones públicos al 28 oct, 18:00 CDMX. Análisis independiente, no afiliado a la NBA ni a sus equipos. No es recomendación de apuesta.",
         font("Inter-Regular.otf", 19), MUTED, W - 2 * M, 26)
    footer(d, 5, T)
    return im


if __name__ == "__main__":
    cover().save(f"{OUT}/01.png")
    for i, g in enumerate(GAMES, 2):
        game_slide(i, *g).save(f"{OUT}/{i:02d}.png")
    method().save(f"{OUT}/05.png")
    print(sorted(os.listdir(OUT)))
