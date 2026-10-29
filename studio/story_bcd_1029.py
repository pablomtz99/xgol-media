"""xGol — 29 oct, estilo narrativo v3: B NFL (CAR@GB), C NBA (MEM@POR), D Superclásico."""
import os, sys
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font as F, base, para, wrap, BG, TXT, ACC, NEG, W, H, M
from story_lib import (MUTED, LINE, SURF, GHOST, AMBER, kicker, footer, headline, body, bridge, how,
                       steps_tag, mvm, verdict, flow)

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/story_bcd")
T = 6


# ============================================================ B · NFL
def B():
    s = []
    # 1
    im, d = base(); kicker(d, "NFL · Jueves 29 oct · 18:15 CDMX · CAR @ GB")
    y = headline(d, "El mercado cree más en Green Bay que nosotros", size=76)
    y = mvm(d, y + 40, "GB", .56, .63)
    body(d, y + 10, "El líder del NFC Sur (CAR, 3-3) visita al último del NFC Norte (GB, 4-3)… y no es el favorito. Revisamos en 3 pasos quién tiene razón.")
    bridge(d, "Empecemos por lo que define este partido: correr con el balón")
    footer(d, 1, T); s.append(im)

    # 2
    im, d = base(); kicker(d, "Paso 1 · El duelo por tierra"); steps_tag(d, 1)
    y = headline(d, "Green Bay no sabe correr, y no es mala racha.")
    y += 60
    lo, hi = 2.5, 6.0
    x0, x1 = M + 20, W - M - 20
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    ay = y + 130
    d.line((x0, ay, x1, ay), fill=LINE, width=6)
    for v in (3, 4, 5, 6):
        d.text((sx(v) - 8, ay + 20), str(v), font=F("Inter-Medium.otf", 22), fill=MUTED)
    d.line((sx(4.34), ay - 70, sx(4.34), ay + 12), fill=GHOST, width=3)
    d.text((sx(4.34) - 70, ay - 104), "Promedio liga 4.3", font=F("Inter-SemiBold.otf", 22), fill=GHOST)
    for v, lab, col, up in ((3.18, "GB ataque: 3.2", NEG, False), (5.31, "CAR permite: 5.3", AMBER, False)):
        d.ellipse((sx(v) - 20, ay - 20, sx(v) + 20, ay + 20), fill=col)
        fl = F("InterDisplay-Bold.otf", 30)
        d.text((sx(v) - d.textlength(lab, font=fl) / 2, ay + 60), lab, font=fl, fill=col)
    y = ay + 120
    d.text((M, y), "yardas por acarreo", font=F("Inter-Medium.otf", 22), fill=MUTED)
    y += 50
    cw = (W - 2 * M) // 2
    for k, (v, l, col) in enumerate((("6 en 1,000", "probabilidad de que lo de GB sea casualidad (p = 0.006)", NEG),
                                     ("9 en 100", "probabilidad de que lo de CAR sea casualidad (p = 0.09)", AMBER))):
        x = M + k * cw
        d.text((x, y), v, font=F("InterDisplay-Black.otf", 52), fill=col)
        para(d, (x, y + 66), l, F("Inter-Medium.otf", 23), MUTED, cw - 30, 29)
    how(d, y + 160, "Comparamos los 137 acarreos de Green Bay y los 174 que ha permitido Carolina contra el promedio de la liga (prueba t). Lo de Green Bay es real; lo de Carolina todavía podría ser ruido.")
    bridge(d, "Debilidad contra debilidad. Entonces, ¿qué inclina el partido?")
    footer(d, 2, T); s.append(im)

    # 3
    im, d = base(); kicker(d, "Paso 2 · Jugada por jugada"); steps_tag(d, 2)
    y = headline(d, "Por jugada están empatados; la casa y la defensa inclinan a GB.", size=60)
    y += 40
    rows = [("Ataque (EPA por jugada)", .06, .00), ("Defensa (EPA que evita)", -.02, .06), ("Balance", .04, .05)]
    cx = W // 2
    sc = 2600
    d.text((cx - 150, y), "CAR", font=F("InterDisplay-Black.otf", 34), fill=GHOST)
    d.text((cx + 90, y), "GB", font=F("InterDisplay-Black.otf", 34), fill=ACC)
    y += 56
    for lab, c, g in rows:
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 25), fill=MUTED)
        y += 38
        d.line((cx, y - 6, cx, y + 46), fill=LINE, width=3)
        for v, sign, col in ((c, -1, GHOST), (g, 1, ACC)):
            w = int(abs(v) * sc)
            if v >= 0:
                x0, x1 = (cx - w, cx) if sign < 0 else (cx, cx + w)
            else:
                x0, x1 = (cx, cx + w) if sign < 0 else (cx - w, cx)
            if w:
                d.rounded_rectangle((x0, y, x1, y + 40), radius=8, fill=col if v >= 0 else NEG)
            t = f"{v:+.2f}" if v else "0.00"
            ft = F("InterDisplay-Bold.otf", 30)
            tx = cx - w - 20 - d.textlength(t, font=ft) if sign < 0 else cx + w + 20
            if sign < 0 and v < 0:
                tx = cx - 20 - d.textlength(t, font=ft)
            d.text((tx, y + 2), t, font=ft, fill=TXT)
        y += 66
    y += 4
    chips = [("+0.01", "diferencia en balance"), ("+1.5", "puntos por jugar en casa"), ("GB +2", "margen esperado")]
    cw = (W - 2 * M) // 3
    d.rounded_rectangle((M, y, W - M, y + 130), radius=18, fill=SURF)
    for k, (v, l) in enumerate(chips):
        x = M + 28 + k * cw
        d.text((x, y + 16), v, font=F("InterDisplay-Black.otf", 46), fill=ACC if k == 2 else TXT)
        d.text((x, y + 80), l, font=F("Inter-Medium.otf", 21), fill=MUTED)
    how(d, y + 152, "EPA = puntos que suma cada jugada. La diferencia de balance × ~62 jugadas por partido, reducida a la mitad porque van pocas semanas, + 1.5 de localía = Green Bay por 2 → 56%.")
    bridge(d, "Entonces, ¿por qué el mercado ve 63%?")
    footer(d, 3, T); s.append(im)

    # 4
    im, d = base(); kicker(d, "Paso 3 · ¿A quién creerle?"); steps_tag(d, 3)
    y = headline(d, "Esta temporada, el mercado ha predicho mejor que nuestro modelo.", size=62)
    y += 50
    bw = W - 2 * M - 230
    for lab, v, col in (("Mercado", .240, GHOST), ("Referencia simple", .249, LINE), ("Nuestro modelo NFL", .258, NEG)):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 28), fill=TXT)
        d.rounded_rectangle((M, y + 42, M + int(bw * v / .27), y + 92), radius=12, fill=col)
        d.text((M + int(bw * v / .27) + 20, y + 46), f"{v:.3f}", font=F("InterDisplay-Black.otf", 40), fill=TXT)
        y += 122
    d.text((M, y), "menos es mejor ←", font=F("Inter-SemiBold.otf", 23), fill=ACC)
    how(d, y + 50, "Brier = error promedio de las probabilidades en 75 partidos (semanas 3 a 7), prediciendo cada semana solo con datos previos. El mercado además ve lesiones (GB sin Parsons, CAR sin Moton) y nuestro modelo no.")
    bridge(d, "Con eso claro, qué esperar el jueves")
    footer(d, 4, T); s.append(im)

    # 5
    im, d = base(); kicker(d, "El veredicto")
    y = headline(d, "Green Bay es favorito, y el partido se decide en el suelo.", size=64)
    y += 40
    verdict(d, y, [("1", "Favorito ligero", "Nosotros 56%, el mercado 63%. Esta temporada, la referencia más confiable es el mercado."),
                   ("2", "La llave: correr", "El peor ataque por tierra contra una de las defensas que más permite. Si Green Bay logra correr, se lo lleva."),
                   ("3", "Partido abierto", "8 de cada 10 veces el resultado cae entre «Carolina por 15» y «Green Bay por 19».")])
    bridge(d, "¿Le crees al mercado o a los números de la temporada?")
    footer(d, 5, T); s.append(im)

    # 6
    im, d = base(); kicker(d, "La lógica detrás")
    y = headline(d, "De cada jugada a la probabilidad", size=64)
    flow(d, y + 30, [("Todas las jugadas, semanas 1–7", "nflverse · ataque y defensa de cada equipo"),
                     ("EPA por jugada", "puntos que suma o evita cada jugada"),
                     ("Diferencia × 62 jugadas × 0.5", "+1.5 por jugar en casa = GB por 2"),
                     ("Error típico ±13.5 puntos", "cuánto se desvía un partido normal"),
                     ("Probabilidad", "GB 56% · mercado 63%")],
         "Datos: nflverse (CC-BY 4.0), semanas 1–7; mercado: precios convertidos a probabilidad sin el margen de la casa. Análisis independiente, no afiliado a la NFL ni a sus equipos. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ C · NBA
def C():
    s = []
    im, d = base(); kicker(d, "NBA · Jueves 29 oct · 20:00 CDMX · MEM @ POR")
    y = headline(d, "Dos invictos. Solo uno es real.", size=84)
    y = mvm(d, y + 40, "POR", .66, .73, lk="Mercado de predicción")
    body(d, y + 10, "Ja Morant enfrenta por primera vez a los Grizzlies, su exequipo. Memphis llega 4-0; Portland, 3-0. Probabilidad de que gane Portland.")
    bridge(d, "Paso 1: ¿contra quién ganó Memphis?")
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "Paso 1 · El calendario"); steps_tag(d, 1)
    y = headline(d, "El 4-0 de Memphis fue contra el fondo de la liga.")
    y += 40
    lo, hi = -10, 5
    x0, x1 = M + 200, W - M - 20
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    for team, opps, avg, col in (("MEM", [("UTA", -6.3), ("GSW", -1.1), ("SAC", -8.8), ("UTA", -6.3)], -5.6, NEG),
                                 ("POR", [("PHX", -2.0), ("SAC", -8.8), ("LAL", 3.1)], -2.6, ACC)):
        d.text((M, y + 40), team, font=F("InterDisplay-Black.otf", 46), fill=TXT)
        ay = y + 66
        d.line((x0, ay, x1, ay), fill=LINE, width=4)
        d.line((sx(0), ay - 40, sx(0), ay + 40), fill=GHOST, width=2)
        seen = {}
        for o, v in opps:
            k = seen.get(o, 0); seen[o] = k + 1
            d.ellipse((sx(v) - 13, ay - 13, sx(v) + 13, ay + 13), fill=MUTED)
            fo = F("Inter-SemiBold.otf", 20)
            if k == 0:
                d.text((sx(v) - d.textlength(o, font=fo) / 2, ay - 44), o + (" ×2" if o == "UTA" and team == "MEM" else ""), font=fo, fill=MUTED)
        d.rectangle((sx(avg) - 3, ay - 28, sx(avg) + 3, ay + 28), fill=col)
        d.text((sx(avg) - 60, ay + 30), f"promedio {avg:+.1f}", font=F("Inter-Bold.otf", 22), fill=col)
        y += 190
    d.text((sx(0) - 70, y - 20), "equipo promedio = 0", font=F("Inter-Medium.otf", 20), fill=GHOST)
    how(d, y + 30, "Cada equipo tiene un nivel: cuántos puntos le gana (o pierde) a un equipo promedio. Memphis le ganó a rivales que pierden por casi 6 contra cualquiera. Portland ya le ganó a los Lakers de visita.")
    bridge(d, "Si quitamos el efecto del calendario, ¿qué tan buenos son?")
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Paso 2 · Ajuste por rival"); steps_tag(d, 2)
    y = headline(d, "Ajustado, Portland es 8° de la liga. Memphis, 17°.")
    y += 50
    lo, hi = -4, 20
    x0, x1 = M + 140, W - M - 30
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    for team, raw, adj, col in (("MEM", 9.8, -0.8, NEG), ("POR", 18.7, 4.4, ACC)):
        d.text((M, y + 14), team, font=F("InterDisplay-Black.otf", 46), fill=TXT)
        ay = y + 40
        d.line((sx(raw), ay, sx(adj) + 18, ay), fill=MUTED, width=4)
        d.polygon([(sx(adj) + 4, ay), (sx(adj) + 26, ay - 12), (sx(adj) + 26, ay + 12)], fill=MUTED)
        d.ellipse((sx(raw) - 14, ay - 14, sx(raw) + 14, ay + 14), outline=GHOST, width=4)
        d.ellipse((sx(adj) - 16, ay - 16, sx(adj) + 16, ay + 16), fill=col)
        d.text((sx(raw) - 30, ay - 58), f"{raw:+.1f}", font=F("InterDisplay-Bold.otf", 28), fill=GHOST)
        d.text((sx(adj) - 30, ay + 24), f"{adj:+.1f}", font=F("InterDisplay-Bold.otf", 30), fill=col)
        y += 150
    d.line((sx(0), y - 300, sx(0), y - 40), fill=LINE, width=2)
    d.text((M, y - 20), "○ ganan por partido (sin ajustar)   ● nivel ajustado", font=F("Inter-Medium.otf", 23), fill=MUTED)
    y += 30
    rows = [("Ataque vs. promedio", "-1.2", "+3.3"), ("Defensa vs. promedio", "+0.4", "+1.1"), ("Días de descanso", "2", "1")]
    for lab, a, b in rows:
        d.line((M, y, W - M, y), fill=LINE, width=2); y += 12
        d.text((M, y + 6), lab, font=F("Inter-Medium.otf", 26), fill=TXT)
        for cx, v in ((660, a), (860, b)):
            col = TXT if not v[0] in "+-" else (ACC if v.startswith("+") else NEG)
            d.text((cx, y), v, font=F("InterDisplay-Bold.otf", 34), fill=col)
        y += 56
    how(d, y + 14, "Corregimos cada marcador por la calidad del rival y partimos del 60% del nivel de la temporada pasada, porque 3 o 4 partidos son muy pocos.")
    bridge(d, "Con esos niveles, el modelo calcula el partido de hoy")
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Paso 3 · El partido"); steps_tag(d, 3)
    y = headline(d, "Portland gana 2 de cada 3 veces. El mercado dice 3 de cada 4.", size=62)
    y += 50
    lo, hi = -15, 27
    x0, x1 = M + 10, W - M - 10
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    ay = y + 80
    d.rounded_rectangle((sx(-12.8), ay - 26, sx(24.9), ay + 26), radius=26, fill=SURF)
    d.line((sx(0), ay - 60, sx(0), ay + 60), fill=GHOST, width=3)
    d.text((sx(0) - 50, ay - 96), "empate", font=F("Inter-SemiBold.otf", 22), fill=GHOST)
    d.ellipse((sx(6.1) - 18, ay - 18, sx(6.1) + 18, ay + 18), fill=ACC)
    d.ellipse((sx(7.5) - 12, ay - 12, sx(7.5) + 12, ay + 12), outline=GHOST, width=4)
    d.text((sx(6.1) - 60, ay + 34), "POR +6 (modelo)", font=F("Inter-Bold.otf", 22), fill=ACC)
    d.text((sx(7.5) - 10, ay - 64), "+7.5 (mercado)", font=F("Inter-Bold.otf", 22), fill=GHOST)
    d.text((sx(-12.8), ay + 70), "← MEM por 13", font=F("Inter-Medium.otf", 22), fill=MUTED)
    t = "POR por 25 →"; ft = F("Inter-Medium.otf", 22)
    d.text((sx(24.9) - d.textlength(t, font=ft), ay + 70), t, font=ft, fill=MUTED)
    y = ay + 130
    d.text((M, y), "Rango donde cae el resultado 8 de cada 10 veces", font=F("Inter-SemiBold.otf", 24), fill=MUTED)
    y += 56
    for lab, a, b in (("Probabilidad POR", "66%", "73%"), ("Puntos totales", "230.5", "233.5")):
        d.line((M, y, W - M, y), fill=LINE, width=2); y += 12
        d.text((M, y + 6), lab, font=F("Inter-Medium.otf", 26), fill=TXT)
        d.text((620, y), a, font=F("InterDisplay-Bold.otf", 34), fill=ACC)
        d.text((830, y), b, font=F("InterDisplay-Bold.otf", 34), fill=GHOST)
        y += 56
    d.text((620, y + 6), "modelo", font=F("Inter-Medium.otf", 21), fill=MUTED)
    d.text((830, y + 6), "mercado", font=F("Inter-Medium.otf", 21), fill=MUTED)
    how(d, y + 50, "Un partido de NBA se desvía ±14.7 puntos de lo esperado. Somos más cautos que el mercado porque el modelo aún pesa la temporada pasada, y estas plantillas cambiaron (Morant).")
    bridge(d, "Juntando las tres piezas, el veredicto")
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "El veredicto")
    y = headline(d, "Portland es el invicto real. Memphis necesita su mejor noche.", size=64)
    y += 40
    verdict(d, y, [("1", "El récord engaña", "Memphis ganó contra el fondo de la liga; Portland, contra mejores rivales."),
                   ("2", "Portland es mejor", "Ataca y defiende mejor incluso después de ajustar por calendario: 8° contra 17°."),
                   ("3", "Todos coinciden", "Modelo (66%) y mercado (73%) ven a Portland; solo difieren en cuánto.")])
    bridge(d, "¿Morant le gana a su exequipo? Te leemos")
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "La lógica detrás")
    y = headline(d, "De los marcadores a la probabilidad", size=64)
    flow(d, y + 30, [("Marcadores 2025-26 y 2026-27", "todos los partidos de temporada regular"),
                     ("Ataque y defensa ajustados por rival", "partiendo de 60% del nivel del año pasado"),
                     ("Localía y cansancio", "+ casa; −2.1 pts si juega dos noches seguidas"),
                     ("Margen esperado ± 14.7 pts", "Portland por 6"),
                     ("Probabilidad", "POR 66% · probado en 1,090 partidos: 69% de aciertos")],
         "Datos: BALLDONTLIE; mercado de predicción público al 28 oct. Análisis independiente, no afiliado a la NBA ni a sus equipos. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ D · Superclásico
def D():
    s = []
    im, d = base(); kicker(d, "Futbol · Domingo 1 nov · 12:00 CDMX · Boca vs River")
    y = headline(d, "El clásico del empate", size=96)
    y += 40
    bw = W - 2 * M
    for lab, vals in (("Historia · 266 partidos", (94 / 266, 84 / 266, 88 / 266)), ("Mercado · este domingo", (.422, .308, .270))):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 26), fill=MUTED); y += 40
        x = M
        for v, col, t in zip(vals, (GHOST, ACC, MUTED), ("Boca", "Empate", "River")):
            w = int(bw * v)
            d.rectangle((x, y, x + w - 6, y + 90), fill=col)
            d.text((x + 16, y + 8), f"{round(v*100)}%", font=F("InterDisplay-Black.otf", 40), fill=BG)
            d.text((x + 16, y + 56), t, font=F("Inter-SemiBold.otf", 22), fill=BG)
            x += w
        y += 126
    body(d, y + 4, "Casi 1 de cada 3 Superclásicos termina empatado, y el mercado del domingo vuelve a decir lo mismo. Lo que cambia es quién gana.")
    bridge(d, "Paso 1: ¿alguien domina de verdad la historia?")
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "Paso 1 · La historia"); steps_tag(d, 1)
    y = headline(d, "En más de 100 años, ninguno domina: 94 contra 88.")
    y += 50
    n = 182
    pmf = {k: comb(n, k) / 2 ** n for k in range(72, 111)}
    pmax = max(pmf.values())
    x0, x1, base_y, top = M, W - M, y + 300, y + 20
    bw = (x1 - x0) / len(pmf)
    for i, (k, p) in enumerate(pmf.items()):
        h = (base_y - top) * p / pmax
        col = ACC if k == 94 else (LINE if abs(k - 91) >= 3 else MUTED)
        d.rectangle((x0 + i * bw + 2, base_y - h, x0 + (i + 1) * bw - 2, base_y), fill=col)
    xi = x0 + (94 - 72 + 0.5) * bw
    d.text((xi - 20, top - 40), "Boca 94 ↓", font=F("Inter-Bold.otf", 24), fill=ACC)
    d.line((x0, base_y, x1, base_y), fill=LINE, width=2)
    for k in (75, 91, 107):
        xx = x0 + (k - 72 + 0.5) * bw
        d.text((xx - 14, base_y + 10), str(k), font=F("Inter-Medium.otf", 21), fill=MUTED)
    d.text((M, base_y + 44), "Victorias de Boca esperables si ambos fueran iguales (182 partidos con ganador)", font=F("Inter-Medium.otf", 22), fill=MUTED)
    y = base_y + 100
    d.text((M, y), "71%", font=F("InterDisplay-Black.otf", 64), fill=ACC)
    para(d, (M + 170, y + 8), "de las veces aparece una diferencia así o mayor por pura casualidad (p = 0.71).", F("Inter-Medium.otf", 27), TXT, W - 2 * M - 170, 36)
    how(d, y + 110, "Si Boca y River fueran exactamente iguales, como una moneda, lo normal sería 91-91. Lo que pasó (94-88) cae en el centro de lo esperable: no hay dominio.")
    bridge(d, "Si la historia está pareja, ¿por qué el mercado favorece a Boca?")
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Paso 2 · Cómo llegan"); steps_tag(d, 2)
    y = headline(d, "Boca casi no pierde. River gana o pierde.")
    y += 50
    bw = W - 2 * M - 160
    for team, (g, e, p), extra in (("Boca", (7, 6, 1), "1° tabla anual · 27 pts (3° de su grupo)"), ("River", (7, 2, 5), "7° tabla anual · 23 pts (4° de su grupo)")):
        d.text((M, y + 18), team, font=F("InterDisplay-Black.otf", 42), fill=TXT)
        x = M + 160
        for v, col, lab in ((g, ACC, "G"), (e, GHOST, "E"), (p, NEG, "P")):
            w = int(bw * v / 14)
            d.rectangle((x, y, x + w - 4, y + 80), fill=col)
            d.text((x + 12, y + 18), f"{v}{lab}", font=F("InterDisplay-Black.otf", 36), fill=BG)
            x += w
        d.text((M + 160, y + 92), extra, font=F("Inter-Medium.otf", 23), fill=MUTED)
        y += 170
    d.text((M, y), "Torneo Clausura 2026: ganados, empatados y perdidos (14 partidos)", font=F("Inter-Medium.otf", 22), fill=MUTED)
    how(d, y + 60, "Boca perdió 1 de 14 y empató 6: es difícil de vencer. River perdió 5 y empató solo 2: todo o nada. Y River llega urgido, 3 puntos debajo del último lugar a Libertadores.")
    bridge(d, "¿Cuánto le suma eso a Boca según el mercado?")
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Paso 3 · Historia vs. mercado"); steps_tag(d, 3)
    y = headline(d, "El mercado le suma 7 puntos a Boca y deja el empate igual.", size=62)
    y += 60
    lo, hi = 20, 46
    x0, x1 = M + 210, W - M - 20
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    for lab, h, m in (("Gana Boca", 35, 42), ("Empate", 32, 31), ("Gana River", 33, 27)):
        d.text((M, y + 2), lab, font=F("InterDisplay-Bold.otf", 32), fill=TXT)
        ay = y + 22
        d.line((sx(h), ay, sx(m), ay), fill=MUTED, width=6)
        d.ellipse((sx(h) - 14, ay - 14, sx(h) + 14, ay + 14), outline=GHOST, width=4)
        col = ACC if m > h + 1 else (NEG if m < h - 1 else GHOST)
        d.ellipse((sx(m) - 16, ay - 16, sx(m) + 16, ay + 16), fill=col)
        diff = m - h
        d.text((sx(m) + (24 if diff >= 0 else -90), ay - 18), f"{diff:+d}", font=F("InterDisplay-Black.otf", 32), fill=col)
        off = 22 if abs(sx(h) - sx(m)) > 60 else 0
        d.text((sx(h) - 18 + (off if h > m else -off) * 0 + (20 if abs(sx(h) - sx(m)) <= 60 else 0), ay + 22), f"{h}%", font=F("Inter-Medium.otf", 21), fill=MUTED)
        d.text((sx(m) - 18 - (34 if abs(sx(h) - sx(m)) <= 60 else 0), ay + 22), f"{m}%", font=F("Inter-Bold.otf", 21), fill=col)
        y += 120
    d.text((M, y), "○ historia   ● mercado del domingo", font=F("Inter-Medium.otf", 23), fill=MUTED)
    how(d, y + 54, "Probabilidad del mercado: precios convertidos a probabilidad, quitando el margen de la casa. La ventaja de Boca sale de jugar en La Bombonera y de su forma. Bajas: Boca sin Aranda, Belmonte, Bareiro ni Marchesín; River sin Fausto Vera.")
    bridge(d, "Con todo junto, qué esperar el domingo")
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "El veredicto")
    y = headline(d, "Boca es favorito, pero 58% de las veces no gana.", size=66)
    y += 40
    verdict(d, y, [("1", "Historia pareja", "94 contra 88 en más de un siglo: no hay dominio, y el empate es 1 de cada 3."),
                   ("2", "Boca llega mejor", "1 derrota en 14 y en casa. River llega irregular y urgido."),
                   ("3", "Nada escrito", "Boca 42%, empate 31%, River 27%: el favorito gana menos de la mitad de las veces.")])
    bridge(d, "¿Se rompe la tendencia en La Bombonera? Te leemos")
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "La lógica detrás")
    y = headline(d, "De 266 partidos a tres probabilidades", size=64)
    flow(d, y + 30, [("266 Superclásicos oficiales", "94 Boca · 84 empates · 88 River"),
                     ("Prueba binomial", "¿la ventaja de Boca es real? p = 0.71: no"),
                     ("Forma actual", "Clausura 2026 y tabla anual"),
                     ("Precios del mercado", "convertidos a probabilidad, sin el margen de la casa"),
                     ("Probabilidades del domingo", "Boca 42 · Empate 31 · River 27")],
         "Datos públicos de prensa al 28 oct. Análisis independiente, no afiliado a la LPF ni a los clubes. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


if __name__ == "__main__":
    for k, fn in (("B", B), ("C", C), ("D", D)):
        o = f"{OUT}/{k}"
        os.makedirs(o, exist_ok=True)
        for i, im in enumerate(fn(), 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
