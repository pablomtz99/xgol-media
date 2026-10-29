"""xGol — MLB 29 oct: «De 9% a campeón». Estilo narrativo v3: tesis → pasos → veredicto → lógica.
Los títulos dicen la conclusión, las gráficas la muestran con anotaciones y una línea final conecta con el siguiente slide."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, wrap, kicker, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M

# Paleta de alto contraste (v3): grises más claros y superficies más separadas del fondo
MUTED = "#B3BDC9"   # texto secundario (antes #8A94A3)
LINE = "#3B4757"    # barras inactivas y divisores (antes #232C38)
SURF = "#1A2330"    # tarjetas (antes #141B24)
GHOST = "#D5DCE4"   # contorno de «esperado»
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/story_mlb")
T = 6
F = font


def headline(d, text, y=160, size=70, maxw=W - 2 * M, col=TXT):
    f = F("InterDisplay-Black.otf", size)
    for ln in wrap(d, text, f, maxw):
        d.text((M, y), ln, font=f, fill=col)
        y += int(size * 1.1)
    return y


def body(d, y, text, size=29, col=TXT):
    return para(d, (M, y), text, F("Inter-Regular.otf", size), col, W - 2 * M, int(size * 1.42))


def bridge(d, text):
    """Hilo conductor: lleva al siguiente slide."""
    f = F("Inter-SemiBold.otf", 29)
    lines = wrap(d, text, f, W - 2 * M - 60)
    y = H - 160 - len(lines) * 40
    d.line((M, y - 26, W - M, y - 26), fill=LINE, width=2)
    for i, ln in enumerate(lines):
        d.text((M, y), ln, font=f, fill=TXT)
        if i == len(lines) - 1:
            d.text((M + d.textlength(ln, font=f) + 14, y - 2), "→", font=F("InterDisplay-Black.otf", 32), fill=ACC)
        y += 40


def how(d, y, text):
    """Cómo se calculó, en una línea discreta pero visible."""
    d.text((M, y), "CÓMO SE CALCULA", font=F("Inter-Bold.otf", 21), fill=MUTED)
    return para(d, (M, y + 32), text, F("Inter-Regular.otf", 25), MUTED, W - 2 * M, 35)


def steps_tag(d, n):
    """Indicador de avance de la historia: ① ② ③."""
    x = W - M - 3 * 46
    for i in range(1, 4):
        on = i <= n
        d.ellipse((x, 104, x + 34, 138), fill=ACC if i == n else (LINE if not on else MUTED))
        t = str(i); fs = F("Inter-Bold.otf", 20)
        d.text((x + 17 - d.textlength(t, font=fs) / 2, 109), t, font=fs, fill=BG if on else MUTED)
        x += 46


# --------------------------------------------------------------------------- slides
def s1():
    im, d = base(); kicker(d, 110, "MLB · Serie Mundial · campeón el 28 oct")
    y = headline(d, "De 9% a campeón", size=104)
    # trayectoria del mercado
    xs = [("Agosto", 9), ("Inicio playoffs", 17), ("Semifinal", 24), ("Antes de la Serie", 62), ("Campeón", 100)]
    x0, y0, y1 = M, y + 70, y + 380
    bw = (W - 2 * M) / len(xs)
    for i, (l, v) in enumerate(xs):
        cx = x0 + bw * i + bw / 2
        top = y1 - (y1 - y0) * v / 100
        d.rounded_rectangle((cx - 58, top, cx + 58, y1), radius=12, fill=ACC if v == 100 else LINE)
        t = f"{v}%"; fs = F("InterDisplay-Bold.otf", 36)
        d.text((cx - d.textlength(t, font=fs) / 2, top - 48), t, font=fs, fill=TXT)
        fl = F("Inter-Medium.otf", 21)
        for j, ln in enumerate(wrap(d, l, fl, 150)):
            d.text((cx - d.textlength(ln, font=fl) / 2, y1 + 12 + j * 26), ln, font=fl, fill=MUTED)
    y = y1 + 90
    y = body(d, y, "Probabilidad de ser campeón según los mercados de predicción. En agosto, casi nadie apostaba por Milwaukee. Ayer ganó el primer título de su historia.", 28, MUTED)
    bridge(d, "¿Fue un milagro? Lo revisamos en 3 pasos, y la respuesta es no")
    footer(d, 1, T)
    return im


def s2():
    im, d = base(); kicker(d, 110, "Paso 1 · ¿Su récord era real?"); steps_tag(d, 1)
    y = headline(d, "Milwaukee ganó lo que merecía. Tampa, 8 de más.", size=66)
    y += 40
    # barras esperado (contorno) vs real (relleno), escala desde 80 victorias
    lo, hi = 80, 106
    bx0, bx1 = M + 120, W - M - 10
    sc = lambda v: bx0 + (bx1 - bx0) * (v - lo) / (hi - lo)
    for team, real, exp, tag, col in (("MIL", 103, 102.5, "justo lo esperado", ACC), ("TB", 98, 90.2, "+8 de más", NEG)):
        d.text((M, y + 30), team, font=F("InterDisplay-Black.otf", 52), fill=TXT)
        # esperado
        d.text((bx0, y - 2), f"Esperadas por sus carreras: {exp:.1f}".replace(".0:", ":"), font=F("Inter-Medium.otf", 23), fill=MUTED)
        d.rounded_rectangle((bx0, y + 30, sc(exp), y + 66), radius=10, outline=GHOST, width=3)
        # real
        d.rounded_rectangle((bx0, y + 78, sc(real), y + 114), radius=10, fill=col)
        d.text((bx0 + 14, y + 80), f"Reales: {real}", font=F("Inter-Bold.otf", 25), fill=BG)
        # anotación de la brecha
        if real - exp > 2:
            d.rectangle((sc(exp), y + 128, sc(real), y + 132), fill=NEG)
        ft = F("InterDisplay-Bold.otf", 30)
        d.text((bx0, y + 140), tag, font=ft, fill=col)
        y += 220
    d.text((bx0, y - 30), "escala desde 80 victorias", font=F("Inter-Regular.otf", 19), fill=MUTED)
    y = how(d, y + 10, "Con las carreras que un equipo anota y recibe se estima cuántos partidos «debió» ganar. Milwaukee anotó 832 y recibió 618 (+214, lo mejor de MLB): eso equivale a ~102 victorias, y ganó 103. Tampa (+86) equivalía a ~90 y ganó 98.")
    bridge(d, "El récord de Milwaukee era real. Entonces, ¿era favorito en la Serie?")
    footer(d, 2, T)
    return im


def s3():
    im, d = base(); kicker(d, 110, "Paso 2 · Antes del primer lanzamiento"); steps_tag(d, 2)
    y = headline(d, "Milwaukee ya era favorito: 7 de cada 10 Series eran suyas.", size=64)
    y += 34
    outs = [("en 4", .111, .031), ("en 5", .176, .080), ("en 6", .213, .099), ("en 7", .180, .111)]
    colw = (W - 2 * M - 30) // 2
    for side, (team, tot, col) in enumerate((("Gana MIL", .68, ACC), ("Gana TB", .32, MUTED))):
        x = M + side * (colw + 30)
        d.rounded_rectangle((x, y, x + colw, y + 360), radius=18, fill=SURF)
        d.text((x + 24, y + 18), team, font=F("Inter-SemiBold.otf", 26), fill=MUTED)
        d.text((x + 24, y + 50), f"{round(tot*100)}%", font=F("InterDisplay-Black.otf", 72), fill=col)
        yy = y + 150
        for lab, pm, pt in outs:
            p = pm if side == 0 else pt
            hit = side == 0 and lab == "en 5"
            d.text((x + 24, yy), lab, font=F("Inter-SemiBold.otf", 25), fill=ACC if hit else TXT)
            bw = colw - 220
            d.rounded_rectangle((x + 100, yy + 6, x + 100 + bw, yy + 30), radius=8, fill=LINE)
            d.rounded_rectangle((x + 100, yy + 6, x + 100 + int(bw * p / .22), yy + 30), radius=8, fill=ACC if hit else ("#7F8C9C" if side else TXT))
            d.text((x + colw - 100, yy), f"{100*p:.0f}%", font=F("Inter-Bold.otf", 25), fill=TXT)
            if hit:
                d.text((x + 100, yy + 34), "← así terminó (4-1)", font=F("Inter-Bold.otf", 21), fill=ACC)
                yy += 22
            yy += 46
        # nada
    y += 390
    y = how(d, y, "Con la fuerza de cada equipo, Milwaukee ganaba 58% de los juegos en campo neutral; ±4 puntos según quién jugara en casa. Con eso recorrimos los 8 finales posibles de la Serie. El mercado le daba 62%: nosotros, un poco más.")
    bridge(d, "Ser favorito no basta: en béisbol hay que ganar los juegos cerrados")
    footer(d, 3, T)
    return im


def s4():
    im, d = base(); kicker(d, 110, "Paso 3 · Dónde se decidió"); steps_tag(d, 3)
    y = headline(d, "La Serie fue pareja, y Milwaukee ganó los juegos cerrados.", size=64)
    y += 30
    rows = [("J1", "MIL 3–2 TB", "1 carrera", "MIL"), ("J2", "MIL 5–4 TB", "1 carrera", "MIL"), ("J3", "MIL 10–1 TB", "paliza", "MIL"),
            ("J4", "TB 4–3 MIL · 12 entradas", "1 carrera", "TB"), ("J5", "MIL 4–1 TB", "cierre", "MIL")]
    for g, sc, tag, win in rows:
        close = tag == "1 carrera"
        if close:
            d.rounded_rectangle((M - 12, y - 4, W - M + 12, y + 58), radius=12, fill=SURF)
        d.text((M, y + 8), g, font=F("Inter-SemiBold.otf", 25), fill=MUTED)
        d.text((M + 70, y), sc, font=F("InterDisplay-Bold.otf", 38), fill=TXT if close else MUTED)
        ft = F("Inter-Bold.otf", 22); tw = d.textlength(tag, font=ft)
        colr = ACC if close else (NEG if tag == "paliza" else LINE)
        d.rounded_rectangle((W - M - tw - 30, y + 8, W - M, y + 44), radius=18, fill=colr)
        d.text((W - M - tw - 15, y + 12), tag, font=ft, fill=BG if colr != LINE else TXT)
        y += 72
    y += 16
    cw = (W - 2 * M) // 2
    for k, (v, l) in enumerate((("2 de 3", "juegos de 1 carrera ganados por MIL"), ("15–11", "carreras de la Serie sin contar la paliza"))):
        x = M + k * cw
        d.text((x, y), v, font=F("InterDisplay-Black.otf", 64), fill=ACC if k == 0 else TXT)
        para(d, (x, y + 76), l, F("Inter-Medium.otf", 24), MUTED, cw - 30, 30)
    y += 150
    y = how(d, y, "Quitando el 10-1, la Serie fue 15-11: casi pareja. Tres de cinco juegos se decidieron por una carrera y Milwaukee ganó dos. Ahí estuvo la diferencia.")
    bridge(d, "Juntando las tres piezas, el veredicto")
    footer(d, 4, T)
    return im


def s5():
    im, d = base(); kicker(d, 110, "El veredicto")
    y = headline(d, "Un campeón que llegó exactamente donde sus números decían.", size=66)
    y += 40
    items = [("1", "Su récord era real", "103 victorias con números de 102.5. Tampa, en cambio, llegó con 8 victorias de más."),
             ("2", "Era el favorito", "68% antes de empezar. Terminó en uno de sus finales más probables."),
             ("3", "Ganó lo apretado", "2 de 3 juegos de una carrera, en una Serie que fue más pareja de lo que dice el 4-1.")]
    for n, t, s in items:
        d.ellipse((M, y, M + 56, y + 56), fill=ACC)
        d.text((M + 28 - d.textlength(n, font=F("InterDisplay-Black.otf", 34)) / 2, y + 6), n, font=F("InterDisplay-Black.otf", 34), fill=BG)
        d.text((M + 82, y + 4), t, font=F("InterDisplay-Bold.otf", 38), fill=TXT)
        y = para(d, (M + 82, y + 54), s, F("Inter-Regular.otf", 27), MUTED, W - 2 * M - 82, 37) + 34
    bridge(d, "No fue el 9% de agosto el que ganó: fue el mejor equipo del año. ¿Lo viste venir?")
    footer(d, 5, T)
    return im


def s6():
    im, d = base(); kicker(d, 110, "La lógica detrás")
    y = headline(d, "De las carreras a la probabilidad", size=66)
    y += 40
    flow = [("Carreras anotadas y recibidas", "832–618 MIL · 736–650 TB"),
            ("Fuerza de cada equipo", "fórmula pitagórica: .633 vs .556"),
            ("Probabilidad por juego", "MIL 58% neutral · ±4 en casa"),
            ("8 finales posibles", "calendario 2-3-2 de la Serie"),
            ("Probabilidad de título", "MIL 68% antes de empezar")]
    for i, (a, b) in enumerate(flow):
        last = i == len(flow) - 1
        d.rounded_rectangle((M, y, W - M, y + 104), radius=16, fill=ACC if last else SURF)
        d.text((M + 28, y + 16), a, font=F("InterDisplay-Bold.otf", 34), fill=BG if last else TXT)
        d.text((M + 28, y + 62), b, font=F("Inter-Medium.otf", 24), fill=BG if last else MUTED)
        y += 104
        if not last:
            d.text((W // 2 - 10, y), "↓", font=F("InterDisplay-Black.otf", 34), fill=MUTED)
            y += 44
    para(d, (M, H - 215), "Mercado: probabilidades publicadas por mercados de predicción. Datos públicos de la temporada 2026 y de la Serie Mundial. Análisis independiente, no afiliado a MLB ni a sus equipos. No es recomendación de apuesta.",
         F("Inter-Regular.otf", 18), MUTED, W - 2 * M, 24)
    footer(d, 6, T)
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate((s1, s2, s3, s4, s5, s6), 1):
        fn().save(f"{OUT}/{i:02d}.png")
    print("ok")
