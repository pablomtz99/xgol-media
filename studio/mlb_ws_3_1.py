"""xGol — Serie Mundial 2026: ¿cuánto vale un 3-1? (MIL 3-1 TB)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, kicker, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ws")
os.makedirs(OUT, exist_ok=True)
T = 5

# --- modelo (calculado aquí para que el post sea reproducible)
E = 1.83
pyth = lambda r, a: r ** E / (r ** E + a ** E)
MIL, TB = pyth(832, 618), pyth(736, 650)          # carreras anotadas / permitidas temporada regular
pn = MIL * (1 - TB) / (MIL * (1 - TB) + TB * (1 - MIL))  # log5
HFA = 0.04
p_mil_away, p_mil_home = pn - HFA, pn + HFA
tb5, tb6, tb7 = 1 - p_mil_away, 1 - p_mil_home, 1 - p_mil_home
P_TB = tb5 * tb6 * tb7
P_MIL = 1 - P_TB
ONE_IN = round(1 / P_TB)


def cover():
    im, d = base()
    kicker(d, 110, "Serie Mundial · MIL 3–1 TB")
    d.text((M, 160), "¿Remontan", font=font("InterDisplay-Black.otf", 96), fill=TXT)
    d.text((M, 262), "los Rays?", font=font("InterDisplay-Black.otf", 96), fill=TXT)
    d.text((M - 8, 430), f"1 en {ONE_IN}", font=font("InterDisplay-Black.otf", 250), fill=ACC)
    para(d, (M, 740), f"Probabilidad de que Tampa Bay gane tres juegos seguidos —dos de ellos en Milwaukee— según nuestro modelo: {100*P_TB:.1f}%.",
         font("Inter-Medium.otf", 36), TXT, W - 2 * M, 50)
    para(d, (M, 930), "Desliza: por qué el 3-1 engaña un poco… y por qué igual pesa muchísimo.",
         font("Inter-Regular.otf", 32), MUTED, W - 2 * M, 44)
    footer(d, 1, T)
    return im


def path_slide():
    im, d = base()
    kicker(d, 110, "El camino de Tampa Bay")
    d.text((M, 160), "Tres monedas", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    d.text((M, 262), "cargadas", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    games = [("Juego 5", "en Tampa Bay", tb5), ("Juego 6", "en Milwaukee", tb6), ("Juego 7", "en Milwaukee", tb7)]
    y = 430
    for g, where, p in games:
        d.rounded_rectangle((M, y, W - M, y + 130), radius=18, fill=SURF)
        d.text((M + 30, y + 24), g, font=font("InterDisplay-Bold.otf", 44), fill=TXT)
        d.text((M + 30, y + 80), where, font=font("Inter-Medium.otf", 26), fill=MUTED)
        bw = 330
        bx = W - M - 30 - bw - 150
        d.rounded_rectangle((bx, y + 52, bx + bw, y + 78), radius=13, fill=LINE)
        d.rounded_rectangle((bx, y + 52, bx + int(bw * p), y + 78), radius=13, fill=ACC)
        s = f"{100*p:.0f}%"
        fs = font("InterDisplay-Black.otf", 56)
        d.text((W - M - 30 - d.textlength(s, font=fs), y + 32), s, font=fs, fill=TXT)
        y += 150
    d.text((M, y + 10), "×  ×  =", font=font("InterDisplay-Bold.otf", 40), fill=MUTED)
    s = f"{100*P_TB:.1f}%"
    d.text((M + 170, y - 6), s, font=font("InterDisplay-Black.otf", 80), fill=ACC)
    para(d, (M, y + 110), "Probabilidad de que TB gane cada juego. Ninguno es imposible por sí solo; lo difícil es encadenar los tres.",
         font("Inter-Regular.otf", 30), MUTED, W - 2 * M, 42)
    footer(d, 2, T)
    return im


def luck_slide():
    im, d = base()
    kicker(d, 110, "Victorias reales vs. merecidas")
    d.text((M, 160), "Los Rays viven", font=font("InterDisplay-Black.otf", 88), fill=TXT)
    d.text((M, 258), "de prestado", font=font("InterDisplay-Black.otf", 88), fill=TXT)
    rows = [("MIL", 103, MIL * 162, "832 anotadas · 618 permitidas"), ("TB", 98, TB * 162, "736 anotadas · 650 permitidas")]
    y = 440
    scale = 760 / 110
    for team, real, exp, sub in rows:
        d.text((M, y), team, font=font("InterDisplay-Black.otf", 60), fill=TXT)
        d.text((M + 150, y + 20), sub, font=font("Inter-Medium.otf", 26), fill=MUTED)
        y += 90
        for lab, v, col in (("Reales", real, TXT), ("Por carreras", exp, ACC)):
            d.text((M, y + 4), lab, font=font("Inter-Medium.otf", 26), fill=MUTED)
            bx = M + 200
            d.rounded_rectangle((bx, y, bx + int((v - 50) * scale * 1.0), y + 38), radius=10, fill=col)
            d.text((bx + int((v - 50) * scale) + 16, y - 2), f"{v:.0f}", font=font("InterDisplay-Bold.otf", 38), fill=TXT)
            y += 56
        y += 40
    diff = 98 - TB * 162
    para(d, (M, y + 10), f"Con sus carreras, TB «merecía» ~{TB*162:.0f} victorias y ganó 98: {diff:+.0f} de más, típico de ganar muchos juegos cerrados. MIL ganó justo lo que merecía.",
         font("Inter-Medium.otf", 32), TXT, W - 2 * M, 44)
    d.text((M, H - 190), "Escala recortada desde 50 victorias.", font=font("Inter-Regular.otf", 22), fill=MUTED)
    footer(d, 3, T)
    return im


def tight_slide():
    im, d = base()
    kicker(d, 110, "Pero ojo")
    d.text((M, 160), "Más pareja", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    d.text((M, 262), "de lo que parece", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    games = [("J1", "MIL 3–2 TB", True), ("J2", "MIL 5–4 TB", True), ("J3", "MIL 10–1 TB", False), ("J4", "TB 4–3 MIL · 12 entr.", True)]
    y = 430
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
    para(d, (M, y + 34), "3 de 4 juegos se decidieron por una carrera. Sin el 10-1, las carreras van MIL 11 – TB 10.",
         font("Inter-SemiBold.otf", 36), TXT, W - 2 * M, 48)
    para(d, (M, y + 190), "El marcador de la serie exagera la diferencia en el campo. Aun así, en una serie lo que cuenta son los juegos, no las carreras.",
         font("Inter-Regular.otf", 30), MUTED, W - 2 * M, 42)
    footer(d, 4, T)
    return im


def history_slide():
    im, d = base()
    kicker(d, 110, "La historia")
    d.text((M, 160), "Solo 6 lo han", font=font("InterDisplay-Black.otf", 88), fill=TXT)
    d.text((M, 258), "logrado", font=font("InterDisplay-Black.otf", 88), fill=TXT)
    para(d, (M, 380), "Remontadas de 3-1 en Serie Mundial (al mejor de 7):", font("Inter-Medium.otf", 28), MUTED, W - 2 * M, 38)
    teams = ["1925 Pirates", "1958 Yankees", "1968 Tigers", "1979 Pirates", "1985 Royals", "2016 Cubs"]
    y = 440
    cw = (W - 2 * M) // 2
    for i, t in enumerate(teams):
        x = M + (i % 2) * cw
        yy = y + (i // 2) * 70
        yr, nm = t.split(" ")
        d.text((x, yy), yr, font=font("InterDisplay-Bold.otf", 40), fill=ACC)
        d.text((x + 110, yy + 2), nm, font=font("InterDisplay-Bold.otf", 40), fill=TXT)
    y += 230
    d.line((M, y, W - M, y), fill=LINE, width=2)
    d.text((M, y + 26), "Cómo lo calculamos", font=font("Inter-Bold.otf", 24), fill=ACC)
    para(d, (M, y + 66),
         "1) Fuerza de cada equipo por carreras anotadas y permitidas en temporada regular (expectativa pitagórica). "
         "2) Duelo directo con log5: MIL gana 58% en campo neutral. 3) ±4 puntos por jugar en casa. "
         "4) Multiplicamos los tres juegos que TB necesita ganar.",
         font("Inter-Regular.otf", 27), TXT, W - 2 * M, 38)
    para(d, (M, H - 200), "No incluye abridores ni lesiones. Datos públicos de la temporada 2026 y de la serie al 27 oct. Análisis independiente, no afiliado a MLB ni a sus equipos. No es recomendación de apuesta.",
         font("Inter-Regular.otf", 19), MUTED, W - 2 * M, 26)
    footer(d, 5, T)
    return im


if __name__ == "__main__":
    print(f"MIL pyth {MIL:.3f} ({MIL*162:.1f} W) TB {TB:.3f} ({TB*162:.1f} W) neutral {pn:.3f} TB per game {tb5:.3f} {tb6:.3f} P_TB {P_TB:.4f} 1 en {ONE_IN}")
    for i, f in enumerate([cover, path_slide, luck_slide, tight_slide, history_slide], 1):
        f().save(f"{OUT}/{i:02d}.png")
