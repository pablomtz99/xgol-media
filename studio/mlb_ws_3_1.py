"""xGol — Serie Mundial 2026: ¿remontan los Rays? v2 (Monte Carlo, sensibilidad, prueba pitagórica)."""
import os, sys
from math import erf, sqrt
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, kicker, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ws")
os.makedirs(OUT, exist_ok=True)
T = 6

# ---------------- modelo
E = 1.83
pyth = lambda r, a: r ** E / (r ** E + a ** E)
MIL, TB = pyth(832, 618), pyth(736, 650)
pn = MIL * (1 - TB) / (MIL * (1 - TB) + TB * (1 - MIL))
HFA = 0.04
tb5, tb6, tb7 = 1 - (pn - HFA), 1 - (pn + HFA), 1 - (pn + HFA)
rng = np.random.default_rng(1)
N = 100_000
g5, g6, g7 = rng.random(N) < 1 - tb5, rng.random(N) < 1 - tb6, rng.random(N) < 1 - tb7
OUTC = [("MIL en 5", g5.mean()), ("MIL en 6", (~g5 & g6).mean()), ("MIL en 7", (~g5 & ~g6 & g7).mean()), ("TB en 7", (~g5 & ~g6 & ~g7).mean())]
P_TB = OUTC[3][1]
ONE_IN = round(1 / P_TB)
SD_W = sqrt(162 * TB * (1 - TB))
Z = (98 - TB * 162) / SD_W
P_Z = 1 - 0.5 * (1 + erf(Z / sqrt(2)))


def title(d, l1, l2, size=88):
    f = font("InterDisplay-Black.otf", size)
    d.text((M, 160), l1, font=f, fill=TXT)
    d.text((M, 160 + int(size * 1.08)), l2, font=f, fill=TXT)


def cover():
    im, d = base()
    kicker(d, 110, "Serie Mundial · MIL 3–1 TB")
    title(d, "¿Remontan", "los Rays?", 96)
    d.text((M - 8, 430), f"1 en {ONE_IN}", font=font("InterDisplay-Black.otf", 250), fill=ACC)
    para(d, (M, 740), f"De 100,000 series simuladas desde el 3-1, Tampa Bay gana {100*P_TB:.1f}%. Necesita tres victorias seguidas, dos en Milwaukee.",
         font("Inter-Medium.otf", 36), TXT, W - 2 * M, 50)
    para(d, (M, 930), "Dentro: simulación, análisis de sensibilidad, una prueba de hipótesis y 101 años de historia.",
         font("Inter-Regular.otf", 30), MUTED, W - 2 * M, 42)
    footer(d, 1, T)
    return im


def sim_slide():
    im, d = base()
    kicker(d, 110, "Monte Carlo · 100,000 series")
    title(d, "Cómo termina", "la serie")
    y = 400
    games = [("J5 · en Tampa Bay", tb5), ("J6 · en Milwaukee", tb6), ("J7 · en Milwaukee", tb7)]
    d.text((M, y), "Probabilidad de que TB gane cada juego", font=font("Inter-Medium.otf", 26), fill=MUTED)
    y += 46
    for g, p in games:
        d.text((M, y + 4), g, font=font("Inter-SemiBold.otf", 28), fill=TXT)
        s = f"{100*p:.0f}%"
        fs = font("InterDisplay-Bold.otf", 40)
        d.text((W - M - d.textlength(s, font=fs), y - 4), s, font=fs, fill=TXT)
        y += 56
    y += 20
    d.line((M, y, W - M, y), fill=LINE, width=2)
    y += 30
    d.text((M, y), "Resultado final de la serie", font=font("Inter-Medium.otf", 26), fill=MUTED)
    y += 50
    bw = W - 2 * M - 330
    for lab, p in OUTC:
        tb = lab.startswith("TB")
        d.text((M, y + 6), lab, font=font("InterDisplay-Bold.otf", 34), fill=ACC if tb else TXT)
        bx = M + 210
        d.rounded_rectangle((bx, y + 10, bx + bw, y + 46), radius=10, fill=SURF)
        d.rounded_rectangle((bx, y + 10, bx + max(12, int(bw * p / 0.6)), y + 46), radius=10, fill=ACC if tb else MUTED)
        s = f"{100*p:.1f}%"
        fs = font("InterDisplay-Black.otf", 40)
        d.text((W - M - d.textlength(s, font=fs), y + 4), s, font=fs, fill=TXT)
        y += 72
    para(d, (M, y + 20), "Lo más probable no es solo que gane Milwaukee: es que lo cierre esta misma noche.",
         font("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    footer(d, 2, T)
    return im


def sens_slide():
    im, d = base()
    kicker(d, 110, "Análisis de sensibilidad")
    title(d, "Ni siendo", "un volado")
    para(d, (M, 390), "¿Y si nuestro modelo subestima a TB? Probabilidad de remontar según lo que valga TB en cada juego:",
         font("Inter-Medium.otf", 30), MUTED, W - 2 * M, 42)
    qs = [0.40, 0.45, 0.50, 0.55, 0.60]
    x0, y0, x1, y1 = M + 20, 560, W - M - 20, 1000
    vmax = 0.25
    d.line((x0, y1, x1, y1), fill=LINE, width=2)
    bwid = (x1 - x0) / len(qs)
    for k, q in enumerate(qs):
        v = q ** 3
        cx = x0 + bwid * (k + 0.5)
        top = y1 - (v / vmax) * (y1 - y0)
        hl = q == 0.50
        d.rounded_rectangle((cx - 60, top, cx + 60, y1), radius=12, fill=ACC if hl else SURF)
        s = f"{100*v:.1f}%"
        fs = font("InterDisplay-Bold.otf", 36)
        d.text((cx - d.textlength(s, font=fs) / 2, top - 50), s, font=fs, fill=TXT)
        l = f"{int(q*100)}%"
        fl = font("Inter-SemiBold.otf", 28)
        d.text((cx - d.textlength(l, font=fl) / 2, y1 + 16), l, font=fl, fill=ACC if hl else MUTED)
    d.text((M, y1 + 60), "Probabilidad de TB en cada juego", font=font("Inter-Medium.otf", 24), fill=MUTED)
    para(d, (M, y1 + 110), "Aunque cada juego fuera 50/50, TB remonta solo 12.5% (0.5³). Incluso con 60% por juego, no llega a 1 de 4.",
         font("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    footer(d, 3, T)
    return im


def luck_slide():
    im, d = base()
    kicker(d, 110, "Prueba de hipótesis · temporada regular")
    title(d, "¿Los Rays", "tuvieron suerte?")
    rows = [("MIL", 103, MIL * 162), ("TB", 98, TB * 162)]
    y = 400
    for team, real, exp in rows:
        d.text((M, y), team, font=font("InterDisplay-Black.otf", 52), fill=TXT)
        d.text((M + 150, y + 6), f"{real} reales", font=font("InterDisplay-Bold.otf", 40), fill=TXT)
        d.text((M + 450, y + 6), f"{exp:.1f} por carreras", font=font("InterDisplay-Bold.otf", 40), fill=ACC)
        y += 80
    d.line((M, y, W - M, y), fill=LINE, width=2)
    y += 30
    cells = [(f"+{98 - TB*162:.1f}", "victorias de más (TB)"), (f"±{SD_W:.1f}", "variación esperada por azar (1 DE)"), (f"{P_Z:.2f}", f"p-valor (z = {Z:.2f})")]
    cw = (W - 2 * M) // 3
    for k, (v, l) in enumerate(cells):
        x = M + k * cw
        d.text((x, y), v, font=font("InterDisplay-Black.otf", 60), fill=TXT)
        para(d, (x, y + 76), l, font("Inter-Medium.otf", 24), MUTED, cw - 20, 32)
    y += 190
    para(d, (M, y), "Veredicto: sospechoso, pero no concluyente. Ganar 8 de más pasa por puro azar ~1 de cada 9 temporadas. Puede ser suerte… o un bullpen que gana partidos cerrados.",
         font("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    para(d, (M, H - 210), "Victorias esperadas: expectativa pitagórica (exponente 1.83) con carreras anotadas y permitidas. DE binomial con 162 juegos.",
         font("Inter-Regular.otf", 22), MUTED, W - 2 * M, 30)
    footer(d, 4, T)
    return im


def tight_slide():
    im, d = base()
    kicker(d, 110, "Pero ojo")
    title(d, "Más pareja", "de lo que parece")
    games = [("J1", "MIL 3–2 TB", True), ("J2", "MIL 5–4 TB", True), ("J3", "MIL 10–1 TB", False), ("J4", "TB 4–3 MIL · 12 entr.", True)]
    y = 420
    for g, s, close in games:
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 24
        d.text((M, y + 6), g, font=font("Inter-SemiBold.otf", 30), fill=MUTED)
        d.text((M + 90, y), s, font=font("InterDisplay-Bold.otf", 46), fill=TXT)
        tag = "1 carrera" if close else "paliza"
        ft = font("Inter-Bold.otf", 26)
        tw = d.textlength(tag, font=ft)
        d.rounded_rectangle((W - M - tw - 32, y + 8, W - M, y + 50), radius=21, fill=ACC if close else NEG)
        d.text((W - M - tw - 16, y + 14), tag, font=ft, fill=BG)
        y += 86
    d.line((M, y, W - M, y), fill=LINE, width=2)
    para(d, (M, y + 34), "3 de 4 juegos por una carrera. Sin el 10-1, las carreras van MIL 11 – TB 10.",
         font("Inter-SemiBold.otf", 36), TXT, W - 2 * M, 48)
    para(d, (M, y + 190), "El 3-1 exagera la diferencia en el campo. Pero en una serie cuentan los juegos, no las carreras: por eso el 1 en 15 se sostiene.",
         font("Inter-Regular.otf", 30), MUTED, W - 2 * M, 42)
    footer(d, 5, T)
    return im


def history_slide():
    im, d = base()
    kicker(d, 110, "La historia")
    title(d, "Solo 6 lo han", "logrado")
    para(d, (M, 380), "Remontadas de 3-1 en Serie Mundial (al mejor de 7):", font("Inter-Medium.otf", 28), MUTED, W - 2 * M, 38)
    teams = ["1925 Pirates", "1958 Yankees", "1968 Tigers", "1979 Pirates", "1985 Royals", "2016 Cubs"]
    cw = (W - 2 * M) // 2
    for i, t in enumerate(teams):
        x = M + (i % 2) * cw
        yy = 440 + (i // 2) * 66
        yr, nm = t.split(" ")
        d.text((x, yy), yr, font=font("InterDisplay-Bold.otf", 38), fill=ACC)
        d.text((x + 106, yy + 2), nm, font=font("InterDisplay-Bold.otf", 38), fill=TXT)
    y = 660
    d.line((M, y, W - M, y), fill=LINE, width=2)
    d.text((M, y + 26), "Cómo lo calculamos", font=font("Inter-Bold.otf", 24), fill=ACC)
    para(d, (M, y + 66),
         f"1) Fuerza por carreras de temporada regular (expectativa pitagórica): MIL .{int(MIL*1000)}, TB .{int(TB*1000)}. "
         f"2) Duelo directo con log5: MIL {100*pn:.0f}% en campo neutral. 3) ±4 puntos por localía. "
         "4) 100,000 simulaciones de los juegos 5 a 7.",
         font("Inter-Regular.otf", 27), TXT, W - 2 * M, 38)
    para(d, (M, H - 200), "No incluye abridores, bullpen ni lesiones. Datos públicos de la temporada 2026 y de la serie al 27 oct. Análisis independiente, no afiliado a MLB ni a sus equipos. No es recomendación de apuesta.",
         font("Inter-Regular.otf", 19), MUTED, W - 2 * M, 26)
    footer(d, 6, T)
    return im


if __name__ == "__main__":
    print(OUTC, ONE_IN, Z, P_Z)
    for i, f in enumerate([cover, sim_slide, sens_slide, luck_slide, tight_slide, history_slide], 1):
        f().save(f"{OUT}/{i:02d}.png")
