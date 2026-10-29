"""xGol — propuestas del 29 oct 2026, v2: misma historia, conclusión en palabras simples en cada slide.
A MLB · B NFL · C NBA · D Superclásico (6 slides c/u)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font, base, footer, para, wrap, kicker, BG, SURF, LINE, TXT, MUTED, ACC, NEG, W, H, M

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/p1029v2")
T = 6
F = font
BOTTOM = 1205


def title(d, l1, l2=None, size=88, y=160):
    f = F("InterDisplay-Black.otf", size)
    d.text((M, y), l1, font=f, fill=TXT)
    if l2:
        d.text((M, y + int(size * 1.08)), l2, font=f, fill=TXT)


def note(d, y, text, size=26):
    return para(d, (M, y), text, F("Inter-Regular.otf", size), MUTED, W - 2 * M, int(size * 1.4))


def simple(d, text, label="EN SIMPLE", bottom=BOTTOM):
    """Caja de conclusión en palabras simples, anclada abajo."""
    f = F("Inter-SemiBold.otf", 31)
    lines = wrap(d, text, f, W - 2 * M - 70)
    h = 28 + 34 + len(lines) * 43 + 24
    top = bottom - h
    d.rounded_rectangle((M, top, W - M, bottom), radius=20, fill=SURF)
    d.rounded_rectangle((M, top, M + 10, bottom), radius=5, fill=ACC)
    d.text((M + 38, top + 24), label, font=F("Inter-Bold.otf", 22), fill=ACC)
    y = top + 62
    for ln in lines:
        d.text((M + 38, y), ln, font=f, fill=TXT)
        y += 43
    return top


def small(d, text):
    para(d, (M, H - 182), text, F("Inter-Regular.otf", 18), MUTED, W - 2 * M, 24)


def mvm(d, y, team, model, market, lm="Nuestro modelo", lk="Mercado"):
    bw = W - 2 * M
    for lab, v, col in ((lm, model, ACC), (lk, market, MUTED)):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 26), fill=MUTED)
        d.rounded_rectangle((M, y + 40, M + bw, y + 96), radius=14, fill=SURF)
        d.rounded_rectangle((M, y + 40, M + int(bw * v), y + 96), radius=14, fill=col)
        d.text((M + 22, y + 46), f"{team} {round(v*100)}%", font=F("InterDisplay-Black.otf", 40), fill=BG)
        y += 124
    return y


def table(d, y, head, rows, cols=(650, 860), signed=(), rowh=62, lab_size=26):
    fh = F("Inter-SemiBold.otf", 24)
    for cx, h in zip(cols, head):
        d.text((cx, y), h, font=fh, fill=MUTED)
    y += 38
    for i, (lab, *vals) in enumerate(rows):
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 14
        para(d, (M, y + 6), lab, F("Inter-Medium.otf", lab_size), TXT, cols[0] - M - 20, 32)
        for cx, v in zip(cols, vals):
            col = TXT
            if i in signed:
                col = ACC if str(v).startswith("+") else NEG
            d.text((cx, y), str(v), font=F("InterDisplay-Bold.otf", 38), fill=col)
        y += rowh
    d.line((M, y, W - M, y), fill=LINE, width=2)
    return y


def stat3(d, y, cells, h=150):
    cw = (W - 2 * M) // 3
    d.rounded_rectangle((M, y, W - M, y + h), radius=18, fill=SURF)
    for k, (v, l) in enumerate(cells):
        x = M + 30 + k * cw
        d.text((x, y + 20), v, font=F("InterDisplay-Black.otf", 50), fill=TXT)
        para(d, (x, y + 86), l, F("Inter-Medium.otf", 22), MUTED, cw - 40, 28)
    return y + h


def checks(d, y, items):
    for ok, t in items:
        d.text((M, y - 4), "✓" if ok else "✗", font=F("InterDisplay-Black.otf", 44), fill=ACC if ok else NEG)
        y = max(para(d, (M + 70, y), t, F("Inter-Medium.otf", 31), TXT, W - 2 * M - 70, 42), y + 42) + 26
    return y


def glossary(d, y, items):
    for term, expl in items:
        d.text((M, y), term, font=F("Inter-Bold.otf", 27), fill=ACC)
        y = para(d, (M, y + 36), expl, F("Inter-Regular.otf", 27), TXT, W - 2 * M, 37) + 22
    return y


# ======================================================== A · MLB
def A():
    s = []
    im, d = base(); kicker(d, 110, "MLB · Brewers campeones · 4-1 en el J5")
    title(d, "De 9%", "a campeón", 110)
    xs = [("Agosto", 9), ("Inicio playoffs", 17), ("Semifinal", 24), ("Pre-Serie", 62), ("Campeón", 100)]
    x0, y0, y1 = M, 450, 800
    bw = (W - 2 * M) / len(xs)
    for i, (l, v) in enumerate(xs):
        cx = x0 + bw * i + bw / 2
        top = y1 - (y1 - y0) * v / 100
        d.rounded_rectangle((cx - 62, top, cx + 62, y1), radius=12, fill=ACC if v == 100 else LINE)
        t = f"{v}%"; fs = F("InterDisplay-Bold.otf", 38)
        d.text((cx - d.textlength(t, font=fs) / 2, top - 50), t, font=fs, fill=TXT)
        fl = F("Inter-Medium.otf", 22)
        for j, ln in enumerate(l.split(" ")):
            d.text((cx - d.textlength(ln, font=fl) / 2, y1 + 14 + j * 28), ln, font=fl, fill=MUTED)
    note(d, 880, "Probabilidad de ser campeón según los mercados de predicción, en cada etapa.")
    simple(d, "En agosto, casi nadie creía en Milwaukee: 9 de cada 100. Hoy ganaron el primer título de su historia. ¿Suerte o lo merecían? Desliza.")
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, 110, "La temporada regular")
    title(d, "El mejor equipo", "del año", 84)
    table(d, 380, ("MIL", "TB"), [
        ("Récord", "103-59", "98-64"),
        ("Carreras anotadas", "832", "736"),
        ("Carreras recibidas", "618", "650"),
        ("Diferencia", "+214", "+86"),
        ("Victorias que «merecían» por sus carreras", "102.5", "90.2"),
    ], signed=(3,))
    simple(d, "Milwaukee anotó 214 carreras más de las que recibió, la mayor diferencia de MLB. Con eso se espera ganar unos 102 partidos… y ganó 103. Su récord no fue suerte: fue nivel.")
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, 110, "Antes de la Serie · nuestro modelo")
    title(d, "Los 8 finales", "posibles", 84)
    outs = [("MIL en 4", .111), ("MIL en 5", .176), ("MIL en 6", .213), ("MIL en 7", .180),
            ("TB en 4", .031), ("TB en 5", .080), ("TB en 6", .099), ("TB en 7", .111)]
    y = 370
    bwid = W - 2 * M - 330
    for lab, p in outs:
        hit = lab == "MIL en 5"
        d.text((M, y + 2), lab, font=F("InterDisplay-Bold.otf", 30), fill=ACC if hit else TXT)
        d.rounded_rectangle((M + 190, y + 8, M + 190 + bwid, y + 38), radius=10, fill=SURF)
        d.rounded_rectangle((M + 190, y + 8, M + 190 + int(bwid * p / .25), y + 38), radius=10, fill=ACC if hit else MUTED)
        t = f"{100*p:.1f}%"; fs = F("InterDisplay-Bold.otf", 30)
        d.text((W - M - d.textlength(t, font=fs), y + 2), t, font=fs, fill=TXT)
        y += 52
    note(d, y + 10, "Sumando los cuatro finales de MIL: 68%. El mercado le daba 62%.")
    simple(d, "Antes de empezar, nuestro modelo decía: Milwaukee gana la Serie 7 de cada 10 veces. Ganó en 5 juegos, uno de los finales más probables. No fue una sorpresa: era el favorito.")
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, 110, "La Serie, juego por juego")
    title(d, "Ganó los", "partidos cerrados", 84)
    rows = [("J1", "MIL 3–2 TB", "1 carrera"), ("J2", "MIL 5–4 TB", "1 carrera"), ("J3", "MIL 10–1 TB", "paliza"),
            ("J4", "TB 4–3 MIL · 12 entr.", "1 carrera"), ("J5", "MIL 4–1 TB", "campeón")]
    y = 370
    for g, sc, tag in rows:
        d.line((M, y, W - M, y), fill=LINE, width=2); y += 16
        d.text((M, y + 6), g, font=F("Inter-SemiBold.otf", 26), fill=MUTED)
        d.text((M + 80, y), sc, font=F("InterDisplay-Bold.otf", 40), fill=TXT)
        ft = F("Inter-Bold.otf", 23); tw = d.textlength(tag, font=ft)
        col = ACC if tag == "1 carrera" else (NEG if tag == "paliza" else TXT)
        d.rounded_rectangle((W - M - tw - 32, y + 6, W - M, y + 44), radius=19, fill=col)
        d.text((W - M - tw - 16, y + 11), tag, font=ft, fill=BG)
        y += 70
    d.line((M, y, W - M, y), fill=LINE, width=2)
    stat3(d, y + 24, [("25–12", "carreras en la Serie"), ("2 de 3", "juegos de 1 carrera para MIL"), ("4–1", "la Serie")])
    simple(d, "Fue más pareja de lo que dice el 4-1: tres juegos se decidieron por una sola carrera. La diferencia: Milwaukee ganó dos de esos tres momentos apretados.")
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, 110, "El veredicto")
    title(d, "¿Título", "merecido?", 100)
    checks(d, 420, [(True, "Mejor récord de todo MLB (103-59)."),
                    (True, "Mayor diferencia de carreras (+214): su récord era real."),
                    (True, "Favorito de nuestro modelo antes de la Serie (68%)."),
                    (True, "Ganó los juegos cerrados cuando importaba.")])
    simple(d, "Sí. El mejor equipo de la temporada fue el campeón, y en béisbol de playoffs eso no está garantizado. Los números respaldan este título.", label="CONCLUSIÓN")
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo lo calculamos")
    title(d, "Método", None, 88)
    glossary(d, 290, [
        ("Victorias «merecidas»", "Con las carreras anotadas y recibidas se estima cuántos partidos debió ganar un equipo (fórmula pitagórica). Si gana muchos más, suele ser suerte."),
        ("Nuestro modelo", "Compara la fuerza de los dos equipos, suma la ventaja de jugar en casa y calcula los 8 finales posibles de la Serie."),
        ("Mercado de predicción", "Lo que pagan las personas por cada resultado, convertido en probabilidad."),
    ])
    small(d, "Datos públicos de la temporada 2026 y de la Serie Mundial. Análisis independiente, no afiliado a MLB ni a sus equipos. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


# ======================================================== B · NFL
def B():
    s = []
    im, d = base(); kicker(d, 110, "NFL · Jueves 18:15 CDMX · CAR @ GB")
    title(d, "El mercado", "cree más que nosotros", 82)
    y = mvm(d, 390, "GB", 0.56, 0.63)
    note(d, y + 6, "Probabilidad de que gane Green Bay.")
    simple(d, "Los dos vemos ganar a Green Bay, pero no con la misma seguridad. Nosotros: 56 de cada 100 veces. El mercado: 63. ¿Por qué la diferencia? Desliza.")
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, 110, "Prueba de hipótesis · semanas 1–7")
    title(d, "Algo tiene", "que ceder", 88)
    y = 380
    for team, lab, v, p, col in (("GB", "ataque por tierra", "3.2", "p = 0.006", NEG),
                                 ("CAR", "defensa por tierra", "5.3", "p = 0.09", ACC)):
        d.rounded_rectangle((M, y, W - M, y + 150), radius=20, fill=SURF)
        d.text((M + 30, y + 18), f"{team} · {lab}", font=F("Inter-SemiBold.otf", 26), fill=MUTED)
        d.text((M + 30, y + 52), v, font=F("InterDisplay-Black.otf", 80), fill=col)
        d.text((M + 220, y + 62), "yardas por acarreo (liga: 4.3)", font=F("Inter-Medium.otf", 26), fill=TXT)
        d.text((M + 220, y + 98), p, font=F("Inter-Bold.otf", 26), fill=ACC)
        y += 170
    note(d, y, "p = probabilidad de ver números así de extremos por pura casualidad. Menos de 0.05 = casi seguro que es real.", 25)
    simple(d, "Green Bay no sabe correr con el balón, y no es mala racha (solo 6 en 1,000 de que sea casualidad). Carolina defiende mal la carrera, pero eso todavía podría ser suerte. Uno de los dos va a ceder.")
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, 110, "Los números del duelo")
    title(d, "CAR @ GB", None, 100)
    table(d, 300, ("CAR", "GB"), [
        ("Récord", "3-3", "4-3"),
        ("Ataque: puntos que suma cada jugada (EPA)", "+0.06", "0.00"),
        ("Defensa: puntos que permite por jugada", "+0.02", "-0.06"),
        ("Balance por jugada", "+0.04", "+0.05"),
        ("Lugar en carrera (ataque)", "11°", "32°"),
    ], lab_size=25)
    simple(d, "Jugada por jugada, los dos rinden casi igual. Lo que inclina el partido hacia Green Bay: juega en casa y tiene la 4ª mejor defensa de la liga. Pero ojo: no tiene a Parsons.")
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, 110, "Transparencia · 75 partidos de 2026")
    title(d, "¿Quién le ha", "atinado más?", 88)
    y = 400
    bw = W - 2 * M - 260
    for lab, v, col in (("Mercado", .240, MUTED), ("Referencia simple", .249, LINE), ("Nuestro modelo NFL", .258, NEG)):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 28), fill=TXT)
        d.rounded_rectangle((M, y + 42, M + int(bw * v / .27), y + 90), radius=12, fill=col)
        d.text((M + int(bw * v / .27) + 20, y + 44), f"{v:.3f}", font=F("InterDisplay-Black.otf", 40), fill=TXT)
        y += 120
    note(d, y, "Error promedio de las probabilidades (Brier). Menos es mejor.", 25)
    simple(d, "Te lo decimos claro: en NFL, esta temporada el mercado ha predicho mejor que nuestro modelo. Por eso hoy le damos más peso al 63% del mercado que a nuestro 56%. Ya estamos mejorando el modelo.")
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, 110, "Qué esperar")
    title(d, "Favorito ligero,", "partido abierto", 82)
    stat3(d, 380, [("GB +2", "margen esperado (modelo)"), ("GB +3.5", "margen esperado (mercado)"), ("47.5", "puntos totales (mercado)")])
    note(d, 560, "8 de cada 10 veces, el resultado debería caer entre «Carolina gana por 15» y «Green Bay gana por 19».", 28)
    simple(d, "Green Bay es favorito, pero por poco: una o dos anotaciones deciden. Si Green Bay logra correr contra la defensa débil de Carolina, se lo lleva. Si no, Carolina tiene muchas opciones.", label="CONCLUSIÓN")
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo lo calculamos")
    title(d, "Método", None, 88)
    glossary(d, 290, [
        ("EPA", "Puntos que una jugada suma o resta, en promedio. Es la mejor forma de medir qué tan bueno es un ataque o una defensa."),
        ("Nuestro modelo", "Diferencia de EPA entre equipos × jugadas por partido, reducida a la mitad por la muestra corta, + 1.5 pts de localía."),
        ("Mercado", "Lo que implican los precios del mercado, convertido a probabilidad y sin el margen de la casa."),
    ])
    small(d, "Datos: nflverse (CC-BY 4.0), semanas 1–7; reportes de lesiones públicos. Análisis independiente, no afiliado a la NFL ni a sus equipos. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


# ======================================================== C · NBA
def C():
    s = []
    im, d = base(); kicker(d, 110, "NBA · Jueves 20:00 CDMX · MEM @ POR")
    title(d, "Morant contra", "su pasado", 92)
    y = mvm(d, 400, "POR", 0.66, 0.73, lk="Mercado de predicción")
    note(d, y + 6, "Probabilidad de que gane Portland.")
    simple(d, "Ja Morant enfrenta por primera vez a los Grizzlies, su exequipo. Los dos están invictos: Memphis 4-0 y Portland 3-0. Spoiler: solo un invicto es real.")
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, 110, "¿Contra quién ganó Memphis?")
    title(d, "¿Un 4-0", "de verdad?", 92)
    y = 390
    d.text((M, y), "Rivales de Memphis y su nivel (puntos vs. un equipo promedio)", font=F("Inter-Medium.otf", 25), fill=MUTED)
    y += 46
    for t, v in (("Utah", "-6.3"), ("Golden State", "-1.1"), ("Sacramento", "-8.8"), ("Utah", "-6.3")):
        d.text((M, y), t, font=F("InterDisplay-Bold.otf", 36), fill=TXT)
        d.text((M + 360, y), v, font=F("InterDisplay-Bold.otf", 36), fill=NEG)
        y += 52
    stat3(d, y + 16, [("+9.8", "gana por partido"), ("−5.6", "nivel de sus rivales"), ("17°", "en nuestro ranking")])
    simple(d, "Ganarle a los peores infla el récord. Tres de las cuatro victorias de Memphis fueron contra equipos del fondo. Portland ya le ganó a los Lakers de visita: su invicto vale más.")
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, 110, "Los números del duelo")
    title(d, "MEM @ POR", None, 100)
    table(d, 300, ("MEM", "POR"), [
        ("Nivel general (ajustado por rival)", "-0.8", "+4.4"),
        ("Ataque vs. un equipo promedio", "-1.2", "+3.3"),
        ("Defensa vs. un equipo promedio", "+0.4", "+1.1"),
        ("Ganan por partido (sin ajustar)", "+9.8", "+18.7"),
        ("Días de descanso", "2", "1"),
    ], signed=(0, 1, 2, 3), lab_size=25)
    simple(d, "Portland es mejor atacando y defendiendo, incluso después de ajustar por rivales. Memphis llega con un día más de descanso, pero no alcanza a compensar.")
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, 110, "Nuestro modelo vs. el mercado")
    title(d, "Mismo favorito,", "distinta confianza", 82)
    table(d, 390, ("Modelo", "Mercado"), [
        ("Probabilidad de que gane POR", "66%", "73%"),
        ("Portland gana por…", "6", "7.5"),
        ("Puntos totales", "230.5", "233.5"),
    ])
    simple(d, "Todos vemos ganar a Portland. Nosotros con un poco menos de confianza porque nuestro modelo todavía «recuerda» cómo eran estos equipos el año pasado, y cambiaron mucho (empezando por Morant).")
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, 110, "Qué esperar")
    title(d, "Portland,", "pero con margen", 88)
    stat3(d, 380, [("POR +6", "margen esperado"), ("66%", "gana Portland"), ("230", "puntos totales")])
    note(d, 560, "8 de cada 10 veces, el resultado debería caer entre «Memphis gana por 13» y «Portland gana por 25».", 28)
    simple(d, "Portland gana 2 de cada 3 veces. Para que Memphis siga invicto necesita su mejor partido del año… justo el día que Morant quiere demostrar algo contra ellos.", label="CONCLUSIÓN")
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo lo calculamos")
    title(d, "Modelo NBA v1", None, 88)
    glossary(d, 290, [
        ("Ajuste por rival", "No es lo mismo ganarle a Utah que a los Lakers. Cada marcador se corrige según la calidad del rival."),
        ("Temporada pasada", "En octubre hay pocos partidos, así que empezamos con 60% del nivel de 2025-26 y cada juego nuevo pesa más."),
        ("¿Qué tan bueno es?", "Probado en 1,090 partidos de 2025-26 sin ver el resultado: acertó al ganador 69% de las veces."),
    ])
    small(d, "Datos: BALLDONTLIE; mercado de predicción público al 28 oct. Análisis independiente, no afiliado a la NBA ni a sus equipos. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


# ======================================================== D · Superclásico
def D():
    s = []
    im, d = base(); kicker(d, 110, "Futbol · Domingo 12:00 CDMX · Boca vs River")
    title(d, "El clásico", "del empate", 100)
    y = 420
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
        y += 126
    simple(d, "Casi 1 de cada 3 Superclásicos termina empatado, y el mercado de este domingo dice exactamente eso. Pero le da más chances a Boca que la historia. ¿Por qué? Desliza.")
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, 110, "Prueba de hipótesis · 266 partidos")
    title(d, "¿Quién domina", "la historia?", 88)
    stat3(d, 380, [("94", "victorias de Boca"), ("84", "empates"), ("88", "victorias de River")])
    d.text((M - 4, 560), "p = 0.71", font=F("InterDisplay-Black.otf", 130), fill=ACC)
    note(d, 720, "p = qué tan probable es ver una diferencia así si los dos fueran exactamente iguales. 0.71 = muy probable.", 27)
    simple(d, "En más de 100 años, Boca le ha ganado solo 6 partidos más a River. Eso es nada: si lanzas una moneda 182 veces, una diferencia así sale todo el tiempo. Están empatados.")
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo llegan")
    title(d, "Boca no pierde,", "River sí", 88)
    table(d, 390, ("Boca", "River"), [
        ("Clausura: ganados-empatados-perdidos", "7-6-1", "7-2-5"),
        ("Puntos en su grupo", "27 (3°)", "23 (4°)"),
        ("Tabla anual", "1°", "7°"),
        ("Último partido", "G 1-0", "G 1-0"),
    ], lab_size=25)
    simple(d, "Boca casi no pierde (1 de 14), pero empata mucho. River es todo o nada: gana o pierde, casi nunca empata. Y River llega urgido: se juega su lugar en la Libertadores.")
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, 110, "Historia vs. mercado")
    title(d, "Lo que el mercado", "le suma a Boca", 82)
    table(d, 390, ("Historia", "Mercado"), [
        ("Gana Boca", "35%", "42%"),
        ("Empate", "32%", "31%"),
        ("Gana River", "33%", "27%"),
    ])
    note(d, 700, "Bajas: Boca sin Aranda, Belmonte, Bareiro ni Marchesín. River sin Fausto Vera.", 26)
    simple(d, "El empate casi no cambia: ronda 1 de cada 3. Lo que cambia es el ganador: el mercado le da 7 puntos más a Boca por jugar en La Bombonera y por llegar en mejor momento.")
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, 110, "Qué esperar")
    title(d, "Tres escenarios", None, 88)
    y = 320
    for lab, p, txt in (("Gana Boca", "42%", "El más probable: localía y forma."),
                        ("Empate", "31%", "Lo de siempre en este clásico: 1 de cada 3."),
                        ("Gana River", "27%", "El que más lo necesita, el menos probable.")):
        d.rounded_rectangle((M, y, W - M, y + 130), radius=18, fill=SURF)
        d.text((M + 30, y + 20), lab, font=F("InterDisplay-Bold.otf", 40), fill=TXT)
        d.text((W - M - 30 - d.textlength(p, font=F("InterDisplay-Black.otf", 56)), y + 30), p, font=F("InterDisplay-Black.otf", 56), fill=ACC)
        d.text((M + 30, y + 78), txt, font=F("Inter-Medium.otf", 25), fill=MUTED)
        y += 150
    simple(d, "Boca es favorito, pero no por mucho: más de la mitad de las veces (58%) Boca NO gana. En el clásico más parejo del mundo, nada está escrito.", label="CONCLUSIÓN")
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, 110, "Cómo lo calculamos")
    title(d, "Método", None, 88)
    glossary(d, 290, [
        ("Historia", "266 Superclásicos oficiales: 94 victorias de Boca, 84 empates y 88 de River."),
        ("Prueba binomial", "Revisa si la ventaja de Boca en victorias es real o cabe dentro del azar. Resultado: cabe dentro del azar."),
        ("Mercado", "Lo que implican los precios del mercado, convertido a probabilidad y sin el margen de la casa."),
    ])
    small(d, "Datos públicos de prensa al 28 oct. Análisis independiente, no afiliado a la LPF ni a los clubes. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


if __name__ == "__main__":
    for k, fn in (("A", A), ("B", B), ("C", C), ("D", D)):
        o = f"{OUT}/{k}"
        os.makedirs(o, exist_ok=True)
        for i, im in enumerate(fn(), 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
