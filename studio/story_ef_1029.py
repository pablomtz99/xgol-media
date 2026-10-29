"""xGol — 29 oct, estilo narrativo v3: E NBA (CLE @ ATL), F NBA (SAC @ NOP).
Números con datos hasta el 27 oct; se actualizan con los resultados del 28 antes de publicar."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font as F, base, para, wrap, BG, TXT, ACC, NEG, W, H, M
from story_lib import (MUTED, LINE, SURF, GHOST, AMBER, kicker, footer, headline, body, bridge, how,
                       steps_tag, mvm, verdict, flow)

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/story_ef")
T = 6
LEGAL = "Datos: BALLDONTLIE; mercado de predicción público al 28 oct. Análisis independiente, no afiliado a la NBA ni a sus equipos. No es recomendación de apuesta."


def interval(d, y, lo_v, hi_v, exp, team_a, team_h, mk=None):
    lo, hi = -18, 27
    x0, x1 = M + 10, W - M - 10
    sx = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
    ay = y + 80
    d.rounded_rectangle((sx(lo_v), ay - 26, sx(hi_v), ay + 26), radius=26, fill=SURF)
    d.line((sx(0), ay - 60, sx(0), ay + 60), fill=GHOST, width=3)
    d.text((sx(0) - 40, ay - 96), "empate", font=F("Inter-SemiBold.otf", 22), fill=GHOST)
    d.ellipse((sx(exp) - 18, ay - 18, sx(exp) + 18, ay + 18), fill=ACC)
    d.text((sx(exp) - 70, ay + 34), f"{team_h} +{exp:.0f} (modelo)", font=F("Inter-Bold.otf", 22), fill=ACC)
    d.text((sx(lo_v), ay + 76), f"← {team_a} por {abs(lo_v):.0f}", font=F("Inter-Medium.otf", 22), fill=MUTED)
    t = f"{team_h} por {hi_v:.0f} →"; ft = F("Inter-Medium.otf", 22)
    d.text((sx(hi_v) - d.textlength(t, font=ft), ay + 76), t, font=ft, fill=MUTED)
    d.text((M, ay + 120), "Rango donde cae el resultado 8 de cada 10 veces", font=F("Inter-SemiBold.otf", 24), fill=MUTED)
    return ay + 170


def bars2(d, y, rows, ta, th, scale=10):
    """Comparación lado a lado (ta a la izquierda, th a la derecha), valores en pts vs. promedio."""
    cx = W // 2 + 60
    d.text((cx - 160, y), ta, font=F("InterDisplay-Black.otf", 34), fill=GHOST)
    d.text((cx + 100, y), th, font=F("InterDisplay-Black.otf", 34), fill=ACC)
    y += 56
    for lab, a, h in rows:
        d.text((M, y + 8), lab, font=F("Inter-SemiBold.otf", 25), fill=TXT)
        for v, side in ((a, -1), (h, 1)):
            w = int(abs(v) * scale)
            x0, x1 = (cx - w, cx) if side < 0 else (cx, cx + w)
            col = (GHOST if side < 0 else ACC) if v >= 0 else NEG
            if w:
                d.rounded_rectangle((x0, y, x1, y + 44), radius=8, fill=col)
            t = f"{v:+.1f}"; ft = F("InterDisplay-Bold.otf", 30)
            tx = cx - w - 14 - d.textlength(t, font=ft) if side < 0 else cx + w + 14
            d.text((tx, y + 4), t, font=ft, fill=TXT)
        y += 68
    d.line((cx, y - 68 * len(rows) - 8, cx, y), fill=LINE, width=3)
    return y


# ============================================================ E · CLE @ ATL
def E():
    s = []
    im, d = base(); kicker(d, "NBA · Jueves 29 oct · 17:00 CDMX · CLE @ ATL")
    y = headline(d, "La mayor diferencia de la noche entre nosotros y el mercado", size=70)
    y = mvm(d, y + 40, "ATL", .62, .50, lk="Mercado de predicción")
    body(d, y + 10, "El mercado lo ve como un volado. Nuestro modelo le da a Atlanta 6 de cada 10. Alguien se está equivocando, y lo vamos a saber el jueves en la noche.")
    bridge(d, "Paso 1: qué ve nuestro modelo en Atlanta")
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "Paso 1 · El nivel de cada equipo"); steps_tag(d, 1)
    y = headline(d, "Ajustado por rival, Atlanta es 6° de la liga. Cleveland, 13°.")
    y += 40
    y = bars2(d, y, [("Nivel general", 1.5, 5.1), ("Ataque", 3.1, 4.3), ("Defensa", -1.6, 0.8)], "CLE", "ATL", scale=40)
    y += 20
    cw = (W - 2 * M) // 2
    for k, (v, l, col) in enumerate((("+9.2", "Atlanta gana por partido (incluye un 128-81)", ACC), ("-0.7", "Cleveland pierde por partido, en promedio", NEG))):
        x = M + k * cw
        d.text((x, y), v, font=F("InterDisplay-Black.otf", 56), fill=col)
        para(d, (x, y + 70), l, F("Inter-Medium.otf", 23), MUTED, cw - 30, 29)
    how(d, y + 160, "Nivel = puntos que le gana (o pierde) a un equipo promedio, corrigiendo por la calidad de cada rival y partiendo del 60% del nivel 2025-26. Defensa: positivo = permite menos que el promedio.")
    bridge(d, "Hay un detalle que suele mover partidos: el cansancio")
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Paso 2 · Cansancio y localía"); steps_tag(d, 2)
    y = headline(d, "Los dos juegan su segunda noche seguida: el cansancio se cancela.")
    y += 40
    items = [("−2.1", "CLE en back-to-back", NEG), ("−2.1", "ATL en back-to-back", NEG), ("+1", "ATL en casa", ACC), ("ATL +4.5", "margen esperado", ACC)]
    cw = (W - 2 * M) // 2
    for k, (v, l, col) in enumerate(items):
        x = M + (k % 2) * cw
        yy = y + (k // 2) * 170
        d.rounded_rectangle((x, yy, x + cw - 20, yy + 150), radius=18, fill=SURF)
        d.text((x + 24, yy + 18), v, font=F("InterDisplay-Black.otf", 56), fill=col)
        d.text((x + 24, yy + 94), l, font=F("Inter-Medium.otf", 24), fill=MUTED)
    y += 360
    how(d, y, "En 2025-26 medimos el efecto de jugar dos noches seguidas: −2.1 puntos (1,237 partidos, p = 0.011: es real). Como hoy lo sufren los dos, se anula. Queda la diferencia de nivel más la ventaja de casa.")
    bridge(d, "Entonces, ¿por qué el mercado lo ve 50/50?")
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Paso 3 · Modelo vs. mercado"); steps_tag(d, 3)
    y = headline(d, "El mercado le cree más al Cleveland del año pasado que nosotros.", size=62)
    y += 30
    y = interval(d, y, -14.4, 23.3, 4.5, "CLE", "ATL")
    rows = [("Probabilidad ATL", "62%", "50%"), ("Nivel de CLE en 2025-26", "+3.8", "")]
    d.line((M, y, W - M, y), fill=LINE, width=2); y += 12
    d.text((M, y + 6), "Probabilidad ATL", font=F("Inter-Medium.otf", 26), fill=TXT)
    d.text((620, y), "62%", font=F("InterDisplay-Bold.otf", 34), fill=ACC)
    d.text((830, y), "50%", font=F("InterDisplay-Bold.otf", 34), fill=GHOST)
    d.text((620, y + 46), "modelo", font=F("Inter-Medium.otf", 21), fill=MUTED)
    d.text((830, y + 46), "mercado", font=F("Inter-Medium.otf", 21), fill=MUTED)
    how(d, y + 100, "Posibles razones: el mercado pesa más el nivel previo de Cleveland (mejor que Atlanta el año pasado) y ve lesiones al minuto (ATL: Wiggins en duda; CLE: Tomlin fuera). Nuestro modelo solo ve marcadores.")
    bridge(d, "Lo que nos jugamos con este partido")
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "El veredicto")
    y = headline(d, "Atlanta es favorito para nosotros, y vamos a ponerlo a prueba en público.", size=62)
    y += 40
    verdict(d, y, [("1", "Atlanta es mejor hoy", "6° contra 13° en nuestro ranking, ajustado por rivales."),
                   ("2", "El cansancio no decide", "Los dos juegan dos noches seguidas: se anula."),
                   ("3", "Nos medimos", "Si gana Cleveland, el mercado tenía razón y lo diremos en el resumen del día.")])
    bridge(d, "¿Tú con quién vas: el modelo o el mercado?")
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "La lógica detrás")
    y = headline(d, "De los marcadores a la probabilidad", size=64)
    flow(d, y + 30, [("Marcadores 2025-26 y 2026-27", "todos los partidos de temporada regular"),
                     ("Ataque y defensa ajustados por rival", "partiendo de 60% del nivel del año pasado"),
                     ("Localía y cansancio", "+ casa; −2.1 pts por back-to-back (aquí, los dos)"),
                     ("Margen esperado ± 14.7 pts", "Atlanta por 4.5"),
                     ("Probabilidad", "ATL 62% · probado en 1,090 partidos: 69% de aciertos")], LEGAL)
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ F · SAC @ NOP
def F_():
    s = []
    im, d = base(); kicker(d, "NBA · Jueves 29 oct · 18:00 CDMX · SAC @ NOP")
    y = headline(d, "Alguien tiene que ganar su primer partido", size=78)
    y = mvm(d, y + 40, "NOP", .61, .69, lk="Mercado de predicción")
    body(d, y + 10, "Sacramento llega 0-4. Nueva Orleans, sin victorias. Uno de los dos se quita el cero el jueves. Probabilidad de que sea Nueva Orleans.")
    bridge(d, "Paso 1: ¿quién es peor de verdad?")
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "Paso 1 · ¿Quién es peor?"); steps_tag(d, 1)
    y = headline(d, "Sacramento no es mala suerte: es el último de la liga.")
    y += 40
    rows = [("Dif. por partido", -17.8, -3.3), ("Nivel ajustado", -8.8, -3.6)]
    y = bars2(d, y, rows, "SAC", "NOP", scale=9)
    y += 10
    cw = (W - 2 * M) // 2
    for k, (v, l, col) in enumerate((("30°", "Sacramento en nuestro ranking (de 30)", NEG), ("23°", "Nueva Orleans", AMBER))):
        x = M + k * cw
        d.text((x, y), v, font=F("InterDisplay-Black.otf", 60), fill=col)
        para(d, (x, y + 74), l, F("Inter-Medium.otf", 24), MUTED, cw - 30, 30)
    how(d, y + 150, "Sacramento perdió sus 4 partidos por 8, 11, 25 y 27 puntos, contra rivales por encima del promedio. Nueva Orleans perdió 3 por 1, 3 y 6: partidos cerrados.")
    bridge(d, "Nueva Orleans es mejor, pero llega con una desventaja")
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Paso 2 · Cansancio y localía"); steps_tag(d, 2)
    y = headline(d, "Nueva Orleans juega su segunda noche seguida. Sacramento descansó.")
    y += 40
    items = [("+5.2", "diferencia de nivel a favor de NOP", ACC), ("+1", "NOP en casa", ACC), ("−2.1", "NOP en back-to-back", NEG), ("NOP +4", "margen esperado", ACC)]
    cw = (W - 2 * M) // 2
    for k, (v, l, col) in enumerate(items):
        x = M + (k % 2) * cw
        yy = y + (k // 2) * 170
        d.rounded_rectangle((x, yy, x + cw - 20, yy + 150), radius=18, fill=SURF)
        d.text((x + 24, yy + 18), v, font=F("InterDisplay-Black.otf", 56), fill=col)
        para(d, (x + 24, yy + 92), l, F("Inter-Medium.otf", 23), MUTED, cw - 70, 28)
    y += 360
    how(d, y, "Jugar dos noches seguidas cuesta 2.1 puntos en promedio (medido en 1,237 partidos de 2025-26, p = 0.011). A Nueva Orleans le resta, pero no le alcanza para dejar de ser favorito.")
    bridge(d, "¿Y qué dice el mercado?")
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Paso 3 · Modelo vs. mercado"); steps_tag(d, 3)
    y = headline(d, "Nueva Orleans gana 6 de cada 10 veces. El mercado dice 7.", size=62)
    y += 30
    y = interval(d, y, -14.8, 22.9, 4.0, "SAC", "NOP")
    d.line((M, y, W - M, y), fill=LINE, width=2); y += 12
    d.text((M, y + 6), "Probabilidad NOP", font=F("Inter-Medium.otf", 26), fill=TXT)
    d.text((620, y), "61%", font=F("InterDisplay-Bold.otf", 34), fill=ACC)
    d.text((830, y), "69%", font=F("InterDisplay-Bold.otf", 34), fill=GHOST)
    d.text((620, y + 46), "modelo", font=F("Inter-Medium.otf", 21), fill=MUTED)
    d.text((830, y + 46), "mercado", font=F("Inter-Medium.otf", 21), fill=MUTED)
    how(d, y + 100, "Somos un poco más cautos: le restamos a Nueva Orleans el cansancio de jugar dos noches seguidas. El mercado parece pesar más lo mal que llega Sacramento.")
    bridge(d, "El veredicto")
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "El veredicto")
    y = headline(d, "Nueva Orleans debería quitarse el cero. Sacramento, seguir esperando.", size=62)
    y += 40
    verdict(d, y, [("1", "Sacramento es el peor", "30° de 30 en nuestro ranking: pierde por casi 18 de promedio."),
                   ("2", "NOP pierde cerrado", "Sus 3 derrotas fueron por 6 o menos: está más cerca de ganar."),
                   ("3", "Ojo con el cansancio", "Es la única carta de Sacramento: NOP juega dos noches seguidas.")])
    bridge(d, "¿Sacramento llega 0-5? Te leemos")
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "La lógica detrás")
    y = headline(d, "De los marcadores a la probabilidad", size=64)
    flow(d, y + 30, [("Marcadores 2025-26 y 2026-27", "todos los partidos de temporada regular"),
                     ("Ataque y defensa ajustados por rival", "partiendo de 60% del nivel del año pasado"),
                     ("Localía y cansancio", "+ casa; −2.1 pts a NOP por back-to-back"),
                     ("Margen esperado ± 14.7 pts", "Nueva Orleans por 4"),
                     ("Probabilidad", "NOP 61% · probado en 1,090 partidos: 69% de aciertos")], LEGAL)
    footer(d, 6, T); s.append(im)
    return s


if __name__ == "__main__":
    for k, fn in (("E", E), ("F", F_)):
        o = f"{OUT}/{k}"
        os.makedirs(o, exist_ok=True)
        for i, im in enumerate(fn(), 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
