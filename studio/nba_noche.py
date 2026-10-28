"""xGol — NBA: la noche en números (3 partidos)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, kicker, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M

D = json.load(open(os.environ.get("NBA_JSON", "/tmp/nba_tonight.json")))
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/nba")
os.makedirs(OUT, exist_ok=True)
T = 5
GAMES = [
    ("SAS@UTA", "SAS", "UTA", "19:00", "Spurs", "Jazz",
     "Mismo guion que la temporada pasada: SAS sigue en positivo y UTA permite 121 puntos por partido."),
    ("OKC@DAL", "OKC", "DAL", "19:30", "Thunder", "Mavericks",
     "OKC no ha bajado el ritmo: +11.1 por partido el año pasado y +10.5 en su arranque 4-0."),
    ("LAL@LAC", "LAL", "LAC", "20:30", "Lakers", "Clippers",
     "Empate técnico. LAL arranca en +8.0, pero el año pasado fue +1.8: el modelo no se cree todavía el arranque."),
]


def pct(key):
    p_home = D["out"][key]["p_home"]
    return 100 - p_home, p_home


def bar(d, y, a, h, pa, ph):
    bw = W - 2 * M
    d.rounded_rectangle((M, y, M + bw, y + 70), radius=14, fill=SURF)
    fav_home = ph >= pa
    if pa == ph:
        d.rounded_rectangle((M, y, M + bw // 2, y + 70), radius=14, fill=MUTED)
    elif fav_home:
        d.rounded_rectangle((M + bw - int(bw * ph / 100), y, M + bw, y + 70), radius=14, fill=ACC)
    else:
        d.rounded_rectangle((M, y, M + int(bw * pa / 100), y + 70), radius=14, fill=ACC)
    fn = font("InterDisplay-Bold.otf", 40)
    d.text((M + 24, y + 12), f"{a} {pa}%", font=fn, fill=BG if (not fav_home and pa != ph) else TXT)
    s = f"{h} {ph}%"
    d.text((M + bw - 24 - d.textlength(s, font=fn), y + 12), s, font=fn, fill=BG if (fav_home and pa != ph) else TXT)


def cover():
    im, d = base()
    kicker(d, 110, "NBA · Miércoles 28 oct · Hora CDMX")
    f = font("InterDisplay-Black.otf", 104)
    d.text((M, 160), "La noche", font=f, fill=TXT)
    d.text((M, 274), "en números", font=f, fill=TXT)
    y = 470
    for key, a, h, hour, *_ in GAMES:
        pa, ph = pct(key)
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 30
        d.text((M, y), hour, font=font("Inter-SemiBold.otf", 30), fill=MUTED)
        d.text((M + 130, y - 10), f"{a} @ {h}", font=font("InterDisplay-Black.otf", 60), fill=TXT)
        fav = a if pa > ph else h
        s = "50 / 50" if pa == ph else f"{fav} {max(pa, ph)}%"
        fs = font("InterDisplay-Bold.otf", 44)
        d.text((W - M - d.textlength(s, font=fs), y - 2), s, font=fs, fill=ACC if pa != ph else TXT)
        y += 120
    d.line((M, y, W - M, y), fill=LINE, width=2)
    para(d, (M, y + 40), "Probabilidad de victoria según el modelo xGol. Desliza para ver los números de cada duelo.",
         font("Inter-Regular.otf", 32), MUTED, W - 2 * M, 44)
    footer(d, 1, T)
    return im


def game_slide(i, key, a, h, hour, na, nh, story):
    im, d = base()
    o = D["out"][key]
    pa, ph = pct(key)
    kicker(d, 110, f"{hour} CDMX · {na} @ {nh}")
    fb = font("InterDisplay-Black.otf", 150)
    d.text((M - 4, 160), a, font=fb, fill=TXT)
    wa = d.textlength(a, font=fb)
    d.text((M + wa + 24, 222), "@", font=font("InterDisplay-Medium.otf", 80), fill=MUTED)
    d.text((M + wa + 110, 160), h, font=fb, fill=TXT)
    d.text((M, 370), "Probabilidad de victoria · modelo xGol", font=font("Inter-Medium.otf", 28), fill=MUTED)
    bar(d, 420, a, h, pa, ph)
    rows = [
        ("Récord 2026-27", o["a"]["rec"], o["h"]["rec"], False),
        ("Dif. de puntos / partido, 2026-27", f"{o['a']['cur']:+.1f}", f"{o['h']['cur']:+.1f}", True),
        ("Dif. de puntos / partido, 2025-26", f"{o['a']['prev']:+.1f}", f"{o['h']['prev']:+.1f}", True),
        ("Puntos permitidos / partido, 2026-27", f"{o['a']['opp']:.1f}", f"{o['h']['opp']:.1f}", False),
    ]
    y = 560
    fh = font("Inter-SemiBold.otf", 26)
    cx1, cx2 = 690, 880
    d.text((cx1, y), a, font=fh, fill=MUTED); d.text((cx2, y), h, font=fh, fill=MUTED)
    y += 50
    fl = font("Inter-Medium.otf", 30)
    fv = font("InterDisplay-Bold.otf", 44)
    for lab, va, vh, signed in rows:
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 26
        para(d, (M, y + 6), lab, fl, TXT, 560, 38)
        for cx, v in ((cx1, va), (cx2, vh)):
            col = TXT
            if signed:
                col = ACC if v.startswith("+") else NEG
            d.text((cx, y), v, font=fv, fill=col)
        y += 96
    d.line((M, y, W - M, y), fill=LINE, width=2)
    para(d, (M, y + 34), story, font("Inter-Medium.otf", 32), TXT, W - 2 * M, 44)
    footer(d, i, T)
    return im


def method():
    im, d = base()
    kicker(d, 110, "Cómo lo calculamos")
    f = font("InterDisplay-Black.otf", 92)
    d.text((M, 160), "Modelo xGol", font=f, fill=TXT)
    d.text((M, 262), "NBA v0", font=f, fill=TXT)
    items = [
        ("1", "Fuerza de cada equipo = diferencia de puntos por partido."),
        ("2", "Mezclamos la temporada pasada (reducida a la mitad) con este arranque. El arranque pesa más con cada partido jugado."),
        ("3", "+1.8 puntos por jugar en casa (promedio 2025-26)."),
        ("4", "Error típico de ±14 puntos por partido → probabilidad."),
    ]
    y = 440
    for n, t in items:
        d.text((M, y - 6), n, font=font("InterDisplay-Black.otf", 54), fill=ACC)
        y = max(para(d, (M + 80, y), t, font("Inter-Medium.otf", 32), TXT, W - 2 * M - 80, 44), y + 44) + 36
    d.line((M, y, W - M, y), fill=LINE, width=2)
    fs = font("Inter-Regular.otf", 27)
    y = para(d, (M, y + 30), "Cada equipo lleva apenas 3 o 4 partidos: incertidumbre alta. Un 73% significa que el otro gana en más de 1 de cada 4 escenarios.",
             fs, MUTED, W - 2 * M, 38)
    para(d, (M, y + 20), "Datos: BALLDONTLIE, temporada regular 2025-26 y 2026-27. Análisis independiente, no afiliado a la NBA ni a ningún equipo. No es recomendación de apuesta.",
         fs, MUTED, W - 2 * M, 38)
    footer(d, 5, T)
    return im


if __name__ == "__main__":
    cover().save(f"{OUT}/01.png")
    for i, g in enumerate(GAMES, 2):
        game_slide(i, *g).save(f"{OUT}/{i:02d}.png")
    method().save(f"{OUT}/05.png")
    print(sorted(os.listdir(OUT)))
