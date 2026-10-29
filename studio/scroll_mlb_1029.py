"""xGol — MLB 29 oct, estilo «para quien va scrolleando» (v4):
contexto primero, una idea por slide, nombres completos, un número grande, una frase clara."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font as F, base, para, wrap, BG, TXT, ACC, NEG, W, H, M
from story_lib import MUTED, LINE, SURF, GHOST, kicker, footer

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/scroll_mlb")
T = 6


def head(d, text, y=170, size=74, col=TXT):
    f = F("InterDisplay-Black.otf", size)
    for ln in wrap(d, text, f, W - 2 * M):
        d.text((M, y), ln, font=f, fill=col)
        y += int(size * 1.08)
    return y


def say(d, y, text, size=34, col=TXT, lh=1.4):
    return para(d, (M, y), text, F("Inter-Medium.otf", size), col, W - 2 * M, int(size * lh))


def tag(d, n, total=4):
    t = f"DATO {n} DE {total}"
    f = F("Inter-Bold.otf", 24)
    w = d.textlength(t, font=f)
    d.rounded_rectangle((W - M - w - 36, 100, W - M, 144), radius=22, fill=ACC)
    d.text((W - M - w - 18, 108), t, font=f, fill=BG)


def big(d, y, value, label, col=ACC):
    d.text((M - 6, y), value, font=F("InterDisplay-Black.otf", 170), fill=col)
    return say(d, y + 200, label, 32, MUTED)


def s1():
    im, d = base(); kicker(d, "Béisbol · Serie Mundial 2026 (la final de MLB)")
    y = head(d, "Los Brewers de Milwaukee son campeones por primera vez en su historia", size=84)
    y += 40
    chips = ["Le ganaron 4-1 a los Rays de Tampa Bay", "Último juego: miércoles 28 de octubre"]
    for c in chips:
        f = F("Inter-SemiBold.otf", 30)
        w = d.textlength(c, font=f)
        d.rounded_rectangle((M, y, M + w + 48, y + 62), radius=31, fill=SURF)
        d.text((M + 24, y + 13), c, font=f, fill=TXT)
        y += 80
    y += 40
    say(d, y, "¿Fue suerte o lo merecían? Lo revisamos con 4 datos.", 40, ACC)
    footer(d, 1, T)
    return im


def s2():
    im, d = base(); kicker(d, "La temporada"); tag(d, 1)
    y = head(d, "Fueron el mejor equipo de todo el año")
    y = big(d, y + 30, "103", "victorias en temporada regular, más que cualquiera de los 30 equipos de MLB.")
    # comparación simple
    y += 40
    bw = W - 2 * M - 200
    for team, v, col in (("Milwaukee", 103, ACC), ("Tampa Bay", 98, GHOST)):
        d.text((M, y + 6), team, font=F("Inter-SemiBold.otf", 28), fill=TXT)
        d.rounded_rectangle((M + 200, y, M + 200 + int(bw * v / 110), y + 50), radius=10, fill=col)
        d.text((M + 216 + int(bw * v / 110), y + 4), str(v), font=F("InterDisplay-Bold.otf", 36), fill=TXT)
        y += 72
    say(d, y + 30, "Su rival en la final también fue el mejor de su liga, pero ganó 5 partidos menos.", 30, MUTED)
    footer(d, 2, T)
    return im


def s3():
    im, d = base(); kicker(d, "¿Fue suerte?"); tag(d, 2)
    y = head(d, "Milwaukee ganó lo que merecía. Tampa Bay ganó de más.")
    y += 40
    say(d, y, "Con las carreras que anotas y las que recibes se puede calcular cuántos partidos «deberías» ganar:", 30, MUTED)
    y += 140
    lo, hi = 80, 106
    x0, x1 = M + 230, W - M - 60
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    for team, exp, real, note, col in (("Milwaukee", 102.5, 103, "justo lo esperado", ACC), ("Tampa Bay", 90.2, 98, "8 victorias de más", NEG)):
        d.text((M, y + 28), team, font=F("InterDisplay-Bold.otf", 36), fill=TXT)
        d.text((x0, y - 6), f"debía ganar {exp:.0f}", font=F("Inter-Medium.otf", 24), fill=MUTED)
        d.rounded_rectangle((x0, y + 26, sx(exp), y + 60), radius=10, outline=GHOST, width=3)
        d.rounded_rectangle((x0, y + 70, sx(real), y + 112), radius=10, fill=col)
        d.text((x0 + 14, y + 74), f"ganó {real}", font=F("Inter-Bold.otf", 28), fill=BG)
        d.text((x0, y + 124), note, font=F("InterDisplay-Bold.otf", 32), fill=col)
        y += 230
    say(d, y + 10, "Ganar muchos más partidos de lo esperado suele ser suerte en juegos cerrados. Milwaukee no la necesitó.", 30, TXT)
    footer(d, 3, T)
    return im


def s4():
    im, d = base(); kicker(d, "Antes de empezar la final"); tag(d, 3)
    y = head(d, "Ya eran favoritos antes del primer juego")
    y = big(d, y + 30, "7 de 10", "veces ganaba Milwaukee la Serie, según nuestro modelo (68%). El mercado le daba 62%.")
    y += 40
    say(d, y, "Nuestro modelo compara la fuerza de los dos equipos y simula todos los resultados posibles de la serie, juego por juego.", 30, MUTED)
    footer(d, 4, T)
    return im


def s5():
    im, d = base(); kicker(d, "La final, juego por juego"); tag(d, 4)
    y = head(d, "Ganaron los juegos apretados")
    y += 40
    rows = [("Juego 1", "Milwaukee 3 – 2 Tampa Bay", True), ("Juego 2", "Milwaukee 5 – 4 Tampa Bay", True), ("Juego 3", "Milwaukee 10 – 1 Tampa Bay", False),
            ("Juego 4", "Tampa Bay 4 – 3 Milwaukee", True), ("Juego 5", "Milwaukee 4 – 1 Tampa Bay", False)]
    for g, sc, close in rows:
        if close:
            d.rounded_rectangle((M - 14, y - 6, W - M + 14, y + 66), radius=14, fill=SURF)
        d.text((M, y + 10), g, font=F("Inter-SemiBold.otf", 26), fill=MUTED)
        d.text((M + 150, y + 4), sc, font=F("InterDisplay-Bold.otf", 36), fill=TXT if close else MUTED)
        if close:
            t = "por 1 carrera"; ft = F("Inter-Bold.otf", 22)
            d.text((W - M - d.textlength(t, font=ft), y + 16), t, font=ft, fill=ACC)
        y += 84
    y += 20
    say(d, y, "3 de los 5 juegos se definieron por una sola carrera, y Milwaukee ganó 2 de esos 3. Ahí se decidió el título.", 32, TXT)
    footer(d, 5, T)
    return im


def s6():
    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Campeón merecido: ganó el mejor equipo del año", size=80)
    y += 50
    for t in ("El mejor récord de MLB: 103 victorias.", "Su récord era real, no suerte.", "Era favorito: 7 de cada 10.", "Ganó los juegos de una carrera."):
        d.ellipse((M, y + 10, M + 26, y + 36), fill=ACC)
        para(d, (M + 50, y), t, F("Inter-Medium.otf", 36), TXT, W - 2 * M - 50, 48)
        y += 76
    y += 30
    say(d, y, "Y pensar que en agosto, el mercado solo le daba 9% de ser campeón.", 32, ACC)
    para(d, (M, H - 230), "Método: victorias esperadas con la fórmula pitagórica (carreras anotadas y recibidas); simulación de la serie con la fuerza de cada equipo y la ventaja de local. Datos públicos 2026. Análisis independiente, no afiliado a MLB. No es recomendación de apuesta.",
         F("Inter-Regular.otf", 19), MUTED, W - 2 * M, 25)
    footer(d, 6, T)
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate((s1, s2, s3, s4, s5, s6), 1):
        fn().save(f"{OUT}/{i:02d}.png")
    print("ok")
