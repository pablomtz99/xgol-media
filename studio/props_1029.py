"""xGol — propuestas del 29 oct 2026: A MLB, B NFL, C NBA, D Superclásico (5 slides c/u)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, kicker, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/p1029")
T = 5
F = lambda n, s: font(n, s)


def title(d, l1, l2=None, size=92, y=160):
    f = F("InterDisplay-Black.otf", size)
    d.text((M, y), l1, font=f, fill=TXT)
    if l2:
        d.text((M, y + int(size * 1.08)), l2, font=f, fill=TXT)


def small(d, text, y=H - 200):
    para(d, (M, y), text, F("Inter-Regular.otf", 19), MUTED, W - 2 * M, 26)


def mvm(d, y, team, model, market, lm="Nuestro modelo", lk="Mercado"):
    bw = W - 2 * M
    for lab, v, col in ((lm, model, ACC), (lk, market, MUTED)):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 26), fill=MUTED)
        d.rounded_rectangle((M, y + 40, M + bw, y + 96), radius=14, fill=SURF)
        d.rounded_rectangle((M, y + 40, M + int(bw * v), y + 96), radius=14, fill=col)
        d.text((M + 22, y + 46), f"{team} {round(v*100)}%", font=F("InterDisplay-Black.otf", 40), fill=BG)
        y += 128
    return y


def table(d, y, head, rows, cols=(640, 860), signed=()):
    fh = F("Inter-SemiBold.otf", 24)
    for cx, h in zip(cols, head):
        d.text((cx, y), h, font=fh, fill=MUTED)
    y += 40
    for i, (lab, *vals) in enumerate(rows):
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 18
        para(d, (M, y + 8), lab, F("Inter-Medium.otf", 27), TXT, cols[0] - M - 20, 34)
        for cx, v in zip(cols, vals):
            col = TXT
            if i in signed:
                col = ACC if str(v).startswith("+") else NEG
            d.text((cx, y), str(v), font=F("InterDisplay-Bold.otf", 40), fill=col)
        y += 70
    d.line((M, y, W - M, y), fill=LINE, width=2)
    return y


def stat3(d, y, cells, h=170):
    cw = (W - 2 * M) // 3
    d.rounded_rectangle((M, y, W - M, y + h), radius=18, fill=SURF)
    for k, (v, l) in enumerate(cells):
        x = M + 30 + k * cw
        d.text((x, y + 24), v, font=F("InterDisplay-Black.otf", 54), fill=TXT)
        para(d, (x, y + 96), l, F("Inter-Medium.otf", 22), MUTED, cw - 40, 28)
    return y + h


# ======================================================== A · MLB
def A():
    s = []
    im, d = base(); kicker(d, 110, "MLB · Brewers campeones · 4-1 en el J5")
    title(d, "De 9%", "a campeón", 110)
    xs = [("Agosto", 9), ("Inicio playoffs", 17), ("Semifinal", 24), ("Pre-Serie", 62), ("Campeón", 100)]
    x0, y0, y1 = M, 470, 860
    bw = (W - 2 * M) / len(xs)
    for i, (l, v) in enumerate(xs):
        cx = x0 + bw * i + bw / 2
        top = y1 - (y1 - y0) * v / 100
        d.rounded_rectangle((cx - 62, top, cx + 62, y1), radius=12, fill=ACC if v == 100 else SURF)
        t = f"{v}%"; fs = F("InterDisplay-Bold.otf", 38)
        d.text((cx - d.textlength(t, font=fs) / 2, top - 50), t, font=fs, fill=TXT)
        fl = F("Inter-Medium.otf", 22)
        for j, ln in enumerate(l.split(" ")):
            d.text((cx - d.textlength(ln, font=fl) / 2, y1 + 14 + j * 28), ln, font=fl, fill=MUTED)
    para(d, (M, 960), "Probabilidad de título según los mercados de predicción. El primer título en la historia de los Brewers. ¿Fue el título más merecido de la década?",
         F("Inter-Medium.otf", 31), TXT, W - 2 * M, 43)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, 110, "La temporada regular")
    title(d, "El mejor equipo", "no fue suerte", 84)
    y = table(d, 400, ("MIL", "TB"), [
        ("Récord", "103-59", "98-64"),
        ("Carreras anotadas", "832", "736"),
        ("Carreras permitidas", "618", "650"),
        ("Diferencial", "+214", "+86"),
        ("Victorias «merecidas» por carreras", "102.5", "90.2"),
    ], signed=(3,))
    para(d, (M, y + 30), "MIL ganó lo que merecía: su diferencial de +214 explica sus 103 victorias casi exacto (expectativa pitagórica). TB ganó ~8 de más.",
         F("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, 110, "Antes de la Serie · nuestro modelo")
    title(d, "68% vs. 62%", None, 120)
    para(d, (M, 310), "Nuestro modelo veía a Milwaukee más favorito que el mercado. Así repartía los 8 finales posibles:",
         F("Inter-Medium.otf", 30), MUTED, W - 2 * M, 42)
    outs = [("MIL en 4", .111), ("MIL en 5", .176), ("MIL en 6", .213), ("MIL en 7", .180),
            ("TB en 4", .031), ("TB en 5", .080), ("TB en 6", .099), ("TB en 7", .111)]
    y = 440
    bwid = W - 2 * M - 330
    for lab, p in outs:
        hit = lab == "MIL en 5"
        d.text((M, y + 2), lab, font=F("InterDisplay-Bold.otf", 32), fill=ACC if hit else TXT)
        d.rounded_rectangle((M + 190, y + 8, M + 190 + bwid, y + 40), radius=10, fill=SURF)
        d.rounded_rectangle((M + 190, y + 8, M + 190 + int(bwid * p / .25), y + 40), radius=10, fill=ACC if hit else MUTED)
        t = f"{100*p:.1f}%"; fs = F("InterDisplay-Bold.otf", 32)
        d.text((W - M - d.textlength(t, font=fs), y + 2), t, font=fs, fill=TXT)
        y += 58
    para(d, (M, y + 20), "Pasó «MIL en 5» (17.6%): el tercer final más probable de los ocho. Un título favorito, no una sorpresa.",
         F("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, 110, "La Serie en números")
    title(d, "Ganó apretando", "y una vez aplastando", 80)
    rows = [("J1", "MIL 3–2 TB", "1 carrera"), ("J2", "MIL 5–4 TB", "1 carrera"), ("J3", "MIL 10–1 TB", "paliza"),
            ("J4", "TB 4–3 MIL · 12 entr.", "1 carrera"), ("J5", "MIL 4–1 TB", "campeón")]
    y = 390
    for g, sc, tag in rows:
        d.line((M, y, W - M, y), fill=LINE, width=2); y += 20
        d.text((M, y + 6), g, font=F("Inter-SemiBold.otf", 28), fill=MUTED)
        d.text((M + 80, y), sc, font=F("InterDisplay-Bold.otf", 42), fill=TXT)
        ft = F("Inter-Bold.otf", 24); tw = d.textlength(tag, font=ft)
        col = ACC if tag == "1 carrera" else (NEG if tag == "paliza" else TXT)
        d.rounded_rectangle((W - M - tw - 32, y + 6, W - M, y + 46), radius=20, fill=col)
        d.text((W - M - tw - 16, y + 12), tag, font=ft, fill=BG)
        y += 76
    d.line((M, y, W - M, y), fill=LINE, width=2)
    y = stat3(d, y + 30, [("25–12", "carreras en la serie"), ("2–1", "MIL en juegos de 1 carrera"), ("4–1", "serie")])
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo lo calculamos")
    title(d, "Método", None, 92)
    y = 300
    for n, t in [("1", "Fuerza de cada equipo por carreras anotadas y permitidas (expectativa pitagórica, exponente 1.83)."),
                 ("2", "Duelo directo con log5: MIL 58% en campo neutral, ±4 puntos por localía."),
                 ("3", "Árbol de los 8 finales posibles de la Serie con el calendario 2-3-2."),
                 ("4", "Mercado: probabilidades publicadas por mercados de predicción en cada etapa.")]:
        d.text((M, y - 6), n, font=F("InterDisplay-Black.otf", 50), fill=ACC)
        y = max(para(d, (M + 70, y), t, F("Inter-Medium.otf", 30), TXT, W - 2 * M - 70, 41), y + 41) + 30
    para(d, (M, y + 20), "¿El título más merecido de la década? Mejor récord, mejor diferencial y favorito del modelo. Los números dicen que sí.",
         F("InterDisplay-Bold.otf", 34), TXT, W - 2 * M, 46)
    small(d, "Datos públicos de la temporada 2026 y de la Serie Mundial. Análisis independiente, no afiliado a MLB ni a sus equipos. No es recomendación de apuesta.")
    footer(d, 5, T); s.append(im)
    return s


# ======================================================== B · NFL
def B():
    s = []
    im, d = base(); kicker(d, 110, "NFL · Jueves 18:15 CDMX · CAR @ GB")
    title(d, "El mercado", "cree más que nosotros", 84)
    y = mvm(d, 400, "GB", 0.56, 0.63)
    para(d, (M, y + 20), "El líder del NFC Sur visita al último del NFC Norte… y no es el favorito. Y ojo: esta temporada el mercado le ha atinado más que nuestro modelo. ¿A quién le crees?",
         F("Inter-Medium.otf", 31), TXT, W - 2 * M, 43)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, 110, "Prueba de hipótesis · semanas 1–7")
    title(d, "Algo tiene", "que ceder", 92)
    y = 410
    for team, lab, v, p, verdict, col in (("GB", "ataque terrestre", "3.2", "p = 0.006", "No es mala suerte: es malo de verdad.", NEG),
                                          ("CAR", "defensa terrestre", "5.3", "p = 0.09", "Mala, pero aún podría ser ruido.", ACC)):
        d.rounded_rectangle((M, y, W - M, y + 210), radius=20, fill=SURF)
        d.text((M + 30, y + 22), f"{team} · {lab}", font=F("Inter-SemiBold.otf", 28), fill=MUTED)
        d.text((M + 30, y + 62), v, font=F("InterDisplay-Black.otf", 96), fill=col)
        d.text((M + 250, y + 78), "yardas/acarreo · liga 4.3", font=F("Inter-Medium.otf", 28), fill=TXT)
        d.text((M + 250, y + 118), p, font=F("Inter-Bold.otf", 28), fill=ACC)
        d.text((M + 30, y + 166), verdict, font=F("Inter-Medium.otf", 26), fill=MUTED)
        y += 235
    para(d, (M, y + 10), "Prueba t contra el promedio de la liga (137 y 174 acarreos). El peor ataque por tierra contra una de las peores defensas por tierra.",
         F("Inter-Regular.otf", 27), MUTED, W - 2 * M, 38)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, 110, "Los números del duelo")
    title(d, "CAR @ GB", None, 110)
    y = table(d, 320, ("CAR", "GB"), [
        ("Récord", "3-3", "4-3"),
        ("EPA por jugada, ataque", "+0.06", "0.00"),
        ("EPA permitida (menos = mejor)", "+0.02", "-0.06"),
        ("EPA neta por jugada", "+0.04", "+0.05"),
        ("Rango en EPA por carrera (ataque)", "11°", "32°"),
    ])
    para(d, (M, y + 26), "Casi idénticos en EPA neta. La localía y la defensa de GB (4ª de la liga) le dan la ventaja. Bajas: GB sin Parsons; CAR sin Moton.",
         F("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, 110, "Transparencia · 75 partidos de 2026")
    title(d, "¿Quién le ha", "atinado más?", 92)
    y = 420
    bw = W - 2 * M - 300
    for lab, v, col in (("Mercado", .240, MUTED), ("Referencia: % histórico del local", .249, SURF), ("Nuestro modelo NFL v0", .258, NEG)):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 28), fill=TXT)
        d.rounded_rectangle((M, y + 44, M + int(bw * v / .27), y + 96), radius=12, fill=col if col != SURF else LINE)
        d.text((M + int(bw * v / .27) + 20, y + 48), f"{v:.3f}", font=F("InterDisplay-Black.otf", 44), fill=TXT)
        y += 130
    para(d, (M, y + 10), "Brier score (menos es mejor), semanas 3 a 7. Nuestro modelo NFL todavía no le gana ni a la referencia simple. Lo decimos aunque no nos guste: por eso lo estamos recalibrando.",
         F("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo lo calculamos")
    title(d, "Método", None, 92)
    y = 300
    for n, t in [("1", "Margen = 0.5 × (EPA neta por jugada GB − CAR) × 61.6 jugadas + 1.5 de localía = GB por 2.0."),
                 ("2", "Error típico ±13.5 pts → GB 56%. Intervalo del 80%: de CAR por 15 a GB por 19."),
                 ("3", "Mercado: probabilidad implícita sin el margen de la casa (GB 63%, equivale a ~3.5 pts)."),
                 ("4", "Prueba de modelo: predicciones semana a semana solo con datos previos.")]:
        d.text((M, y - 6), n, font=F("InterDisplay-Black.otf", 50), fill=ACC)
        y = max(para(d, (M + 70, y), t, F("Inter-Medium.otf", 30), TXT, W - 2 * M - 70, 41), y + 41) + 30
    small(d, "Datos: nflverse (CC-BY 4.0), semanas 1–7; reportes de lesiones públicos. Análisis independiente, no afiliado a la NFL ni a sus equipos. No es recomendación de apuesta.")
    footer(d, 5, T); s.append(im)
    return s


# ======================================================== C · NBA
def C():
    s = []
    im, d = base(); kicker(d, 110, "NBA · Jueves 20:00 CDMX · MEM @ POR")
    title(d, "Morant contra", "su pasado", 92)
    y = mvm(d, 400, "POR", 0.66, 0.73, lk="Mercado de predicción")
    para(d, (M, y + 20), "Primer duelo de Ja Morant contra los Grizzlies. Choque de invictos: MEM 4-0, POR 3-0. Pero solo uno de los dos invictos es real.",
         F("Inter-Medium.otf", 31), TXT, W - 2 * M, 43)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, 110, "Ajuste por calendario")
    title(d, "¿Un 4-0", "de verdad?", 92)
    rows = [("UTA", "-6.3"), ("GSW", "-1.1"), ("SAC", "-8.8"), ("UTA", "-6.3")]
    y = 400
    d.text((M, y), "Rivales de MEM y su rating (pts vs. promedio)", font=F("Inter-Medium.otf", 26), fill=MUTED)
    y += 50
    for t, v in rows:
        d.text((M, y), t, font=F("InterDisplay-Bold.otf", 40), fill=TXT)
        d.text((M + 200, y), v, font=F("InterDisplay-Bold.otf", 40), fill=NEG)
        y += 58
    y = stat3(d, y + 20, [("+9.8", "dif. de puntos real"), ("−5.6", "nivel medio de sus rivales"), ("17°", "MEM en nuestro rating")])
    para(d, (M, y + 26), "3 de sus 4 victorias fueron contra equipos del fondo (UTA dos veces, SAC). Portland, en cambio, ya le ganó a LAL de visita.",
         F("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, 110, "Los números del duelo")
    title(d, "MEM @ POR", None, 110)
    y = table(d, 320, ("MEM", "POR"), [
        ("Rating neto ajustado", "-0.8", "+4.4"),
        ("Ataque vs. promedio", "-1.2", "+3.3"),
        ("Defensa vs. promedio", "+0.4", "+1.1"),
        ("Dif. de puntos real", "+9.8", "+18.7"),
        ("Días de descanso", "2", "1"),
    ], signed=(0, 1, 2, 3))
    para(d, (M, y + 26), "Defensa: positivo = permite menos que el promedio. POR es 8° en nuestro rating; MEM, 17°.",
         F("Inter-Regular.otf", 27), MUTED, W - 2 * M, 38)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, 110, "Modelo vs. mercado")
    title(d, "Mismo favorito,", "distinta confianza", 84)
    y = table(d, 420, ("Modelo", "Mercado"), [
        ("Probabilidad POR", "66%", "73%"),
        ("Margen esperado POR", "+6.1", "+7.5"),
        ("Puntos totales", "230.5", "233.5"),
    ])
    para(d, (M, y + 30), "Los dos ven a Portland, pero el mercado le cree más. Posible razón: nuestro modelo todavía pesa la temporada pasada, y estas plantillas cambiaron mucho (empezando por Morant).",
         F("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    para(d, (M, y + 230), "Intervalo del 80% del margen: de MEM por 13 a POR por 25.", F("Inter-Regular.otf", 27), MUTED, W - 2 * M, 38)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo lo calculamos")
    title(d, "Modelo NBA v1", None, 88)
    y = 300
    for n, t in [("1", "Ataque y defensa de cada equipo ajustados por rival (regresión ridge), partiendo de 60% del nivel 2025-26."),
                 ("2", "Ajuste por cansancio (back-to-back): −2.1 pts, p = 0.011."),
                 ("3", "Error típico ±14.7 pts → probabilidad e intervalo."),
                 ("4", "Prueba fuera de muestra 2025-26: 69% de aciertos, Brier 0.205 vs. 0.248.")]:
        d.text((M, y - 6), n, font=F("InterDisplay-Black.otf", 50), fill=ACC)
        y = max(para(d, (M + 70, y), t, F("Inter-Medium.otf", 30), TXT, W - 2 * M - 70, 41), y + 41) + 30
    small(d, "Datos: BALLDONTLIE; mercado de predicción público al 28 oct. Análisis independiente, no afiliado a la NBA ni a sus equipos. No es recomendación de apuesta.")
    footer(d, 5, T); s.append(im)
    return s


# ======================================================== D · Superclásico
def D():
    s = []
    im, d = base(); kicker(d, 110, "Futbol · Domingo 12:00 CDMX · Boca vs River")
    title(d, "El clásico", "del empate", 100)
    y = 430
    bw = W - 2 * M
    for lab, vals in (("Historia · 266 partidos", (94 / 266, 84 / 266, 88 / 266)), ("Mercado · este domingo", (.422, .308, .270))):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 26), fill=MUTED); y += 40
        x = M
        for v, col, t in zip(vals, (TXT, ACC, MUTED), ("Boca", "Empate", "River")):
            w = int(bw * v)
            d.rectangle((x, y, x + w - 6, y + 90), fill=col)
            d.text((x + 16, y + 8), f"{round(v*100)}%", font=F("InterDisplay-Black.otf", 40), fill=BG)
            d.text((x + 16, y + 56), t, font=F("Inter-SemiBold.otf", 22), fill=BG)
            x += w
        y += 130
    para(d, (M, y + 20), "Casi 1 de cada 3 Superclásicos termina empatado, y el mercado le da exactamente eso. ¿Se rompe la tendencia en La Bombonera?",
         F("Inter-Medium.otf", 31), TXT, W - 2 * M, 43)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, 110, "Prueba de hipótesis · 266 partidos")
    title(d, "Empate técnico", "histórico", 88)
    d.text((M - 6, 400), "p = 0.71", font=F("InterDisplay-Black.otf", 170), fill=ACC)
    para(d, (M, 610), "Boca 94 victorias, River 88. ¿Es una ventaja real o puro azar? Si fueran exactamente iguales, una diferencia así o mayor aparecería 71% de las veces.",
         F("Inter-Medium.otf", 32), TXT, W - 2 * M, 44)
    y = stat3(d, 830, [("94", "victorias de Boca"), ("84", "empates (31.6%)"), ("88", "victorias de River")])
    para(d, (M, y + 26), "Veredicto: en 100+ años, ninguno domina al otro. Prueba binomial sobre los 182 partidos con ganador.",
         F("Inter-Regular.otf", 27), MUTED, W - 2 * M, 38)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo llegan")
    title(d, "Boca no pierde,", "River sí", 88)
    y = table(d, 400, ("Boca", "River"), [
        ("Clausura: G-E-P", "7-6-1", "7-2-5"),
        ("Puntos en su zona", "27 (3°)", "23 (4°)"),
        ("Tabla anual", "1° · 57", "7° · 52"),
        ("Último partido", "G 1-0", "G 1-0"),
    ])
    para(d, (M, y + 26), "Boca empata mucho (6 de 14) y casi no pierde. River gana o pierde: solo 2 empates. Choque de estilos… y River se juega la Libertadores.",
         F("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, 110, "Historia vs. mercado")
    title(d, "Lo que el mercado", "le suma a Boca", 84)
    y = table(d, 420, ("Historia", "Mercado"), [
        ("Gana Boca", "35%", "42%"),
        ("Empate", "32%", "31%"),
        ("Gana River", "33%", "27%"),
    ])
    para(d, (M, y + 30), "El empate coincide casi exacto. La diferencia está en el ganador: el mercado le suma 7 puntos a Boca por jugar en La Bombonera y por su forma (1 derrota en 14).",
         F("Inter-Medium.otf", 30), TXT, W - 2 * M, 42)
    para(d, (M, y + 230), "Bajas: Boca sin Aranda, Belmonte, Bareiro ni Marchesín. River sin Fausto Vera.", F("Inter-Regular.otf", 27), MUTED, W - 2 * M, 38)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo lo calculamos")
    title(d, "Método", None, 92)
    y = 300
    for n, t in [("1", "Historia: 266 Superclásicos oficiales (94 Boca, 84 empates, 88 River)."),
                 ("2", "Prueba binomial: ¿la ventaja de Boca en victorias es distinta de 50/50? p = 0.71, no."),
                 ("3", "Mercado: probabilidades implícitas sin el margen de la casa (Boca 42, empate 31, River 27)."),
                 ("4", "Forma: Torneo Clausura 2026 y tabla anual al 28 oct.")]:
        d.text((M, y - 6), n, font=F("InterDisplay-Black.otf", 50), fill=ACC)
        y = max(para(d, (M + 70, y), t, F("Inter-Medium.otf", 30), TXT, W - 2 * M - 70, 41), y + 41) + 30
    small(d, "Datos públicos de prensa al 28 oct. Análisis independiente, no afiliado a la LPF ni a los clubes. No es recomendación de apuesta.")
    footer(d, 5, T); s.append(im)
    return s


if __name__ == "__main__":
    for k, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        o = f"{OUT}/{k}"
        os.makedirs(o, exist_ok=True)
        for i, im in enumerate(fn(), 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
