"""xGol — 29 oct, estilo «para quien va scrolleando» (v4): B NFL, C NBA MEM@POR, D Superclásico, E NBA CLE@ATL, F NBA SAC@NOP.
Contexto primero · una idea por slide · nombres completos · un número grande · una frase clara."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font as F, base, para, wrap, BG, TXT, ACC, NEG, W, H, M
from story_lib import MUTED, LINE, SURF, GHOST, AMBER, kicker, footer

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/scroll_rest")
T = 6


def head(d, text, y=170, size=74, col=TXT):
    f = F("InterDisplay-Black.otf", size)
    for ln in wrap(d, text, f, W - 2 * M):
        d.text((M, y), ln, font=f, fill=col)
        y += int(size * 1.08)
    return y


def say(d, y, text, size=32, col=TXT, lh=1.4):
    return para(d, (M, y), text, F("Inter-Medium.otf", size), col, W - 2 * M, int(size * lh))


def tag(d, n, total=4):
    t = f"DATO {n} DE {total}"
    f = F("Inter-Bold.otf", 24)
    w = d.textlength(t, font=f)
    d.rounded_rectangle((W - M - w - 36, 100, W - M, 144), radius=22, fill=ACC)
    d.text((W - M - w - 18, 108), t, font=f, fill=BG)


def big(d, y, value, label, col=ACC, size=170):
    d.text((M - 6, y), value, font=F("InterDisplay-Black.otf", size), fill=col)
    return say(d, y + int(size * 1.15), label, 32, MUTED)


def chips(d, y, items):
    f = F("Inter-SemiBold.otf", 29)
    for c in items:
        lines = wrap(d, c, f, W - 2 * M - 48)
        h = 26 + 40 * len(lines)
        w = max(d.textlength(l, font=f) for l in lines)
        d.rounded_rectangle((M, y, M + w + 48, y + h), radius=28, fill=SURF)
        yy = y + 12
        for l in lines:
            d.text((M + 24, yy), l, font=f, fill=TXT); yy += 40
        y += h + 16
    return y


def bullets(d, y, items, size=34):
    for t in items:
        d.ellipse((M, y + 10, M + 26, y + 36), fill=ACC)
        y = para(d, (M + 50, y), t, F("Inter-Medium.otf", size), TXT, W - 2 * M - 50, int(size * 1.35)) + 22
    return y


def hbars(d, y, rows, vmax, fmt="{}", labw=260):
    bw = W - 2 * M - labw - 120
    for lab, v, col in rows:
        d.text((M, y + 6), lab, font=F("Inter-SemiBold.otf", 28), fill=TXT)
        w = int(bw * abs(v) / vmax)
        d.rounded_rectangle((M + labw, y, M + labw + max(w, 8), y + 50), radius=10, fill=col)
        d.text((M + labw + max(w, 8) + 16, y + 4), fmt.format(v), font=F("InterDisplay-Bold.otf", 36), fill=TXT)
        y += 72
    return y


def rankbar(d, y, rows):
    """Ranking de 30: posición marcada sobre una barra (1 = mejor, a la izquierda)."""
    x0, x1 = M + 240, W - M - 20
    sx = lambda r: x0 + (x1 - x0) * (r - 1) / 29
    for lab, r, col in rows:
        d.text((M, y + 8), lab, font=F("Inter-SemiBold.otf", 28), fill=TXT)
        d.rounded_rectangle((x0, y + 18, x1, y + 34), radius=8, fill=LINE)
        d.ellipse((sx(r) - 24, y + 2, sx(r) + 24, y + 50), fill=col)
        t = f"{r}°"; ft = F("InterDisplay-Black.otf", 24)
        d.text((sx(r) - d.textlength(t, font=ft) / 2, y + 10), t, font=ft, fill=BG)
        y += 80
    d.text((x0, y - 10), "1° mejor", font=F("Inter-Medium.otf", 22), fill=MUTED)
    t = "30° peor"; ft = F("Inter-Medium.otf", 22)
    d.text((x1 - d.textlength(t, font=ft), y - 10), t, font=ft, fill=MUTED)
    return y + 30


def stacked(d, y, vals, labels, cols):
    bw = W - 2 * M
    x = M
    for v, l, c in zip(vals, labels, cols):
        w = int(bw * v)
        d.rectangle((x, y, x + w - 6, y + 110), fill=c)
        d.text((x + 16, y + 10), f"{round(v*100)}%", font=F("InterDisplay-Black.otf", 46), fill=BG)
        d.text((x + 16, y + 68), l, font=F("Inter-Bold.otf", 24), fill=BG)
        x += w
    return y + 130


def mvm(d, y, team, model, market, lk="El mercado"):
    bw = W - 2 * M
    for lab, v, col in (("Nuestro modelo", model, ACC), (lk, market, GHOST)):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 28), fill=MUTED)
        d.rounded_rectangle((M, y + 42, M + bw, y + 104), radius=14, fill=SURF)
        d.rounded_rectangle((M, y + 42, M + int(bw * v), y + 104), radius=14, fill=col)
        d.text((M + 22, y + 50), f"{team}: {round(v*100)}%", font=F("InterDisplay-Black.otf", 40), fill=BG)
        y += 132
    return y


def method(d, text):
    para(d, (M, H - 230), text, F("Inter-Regular.otf", 19), MUTED, W - 2 * M, 25)


NBA_M = ("Método: nivel de cada equipo ajustado por la calidad de sus rivales (marcadores 2025-26 y 2026-27), ventaja de local y cansancio "
         "(−2.1 pts por jugar dos noches seguidas, medido en 1,237 partidos). Probado en 1,090 partidos: acertó 69%. Datos: BALLDONTLIE; "
         "mercado de predicción público. Análisis independiente, no afiliado a la NBA. No es recomendación de apuesta.")


# ============================================================ B · NFL
def B():
    s = []
    im, d = base(); kicker(d, "Futbol americano · NFL · Jueves 29 de octubre")
    y = head(d, "Panthers vs. Packers: el mercado confía más en Green Bay que nosotros", size=76)
    y = chips(d, y + 30, ["Carolina Panthers (3-3, líderes de su división) visitan a Green Bay Packers (4-3)",
                          "Jueves 29 oct · 18:15 hora CDMX"])
    say(d, y + 30, "Nosotros: Green Bay gana 56 de cada 100 veces. El mercado: 63. ¿Quién tiene razón? 4 datos.", 38, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "El punto débil de Green Bay"); tag(d, 1)
    y = head(d, "Green Bay no sabe correr con el balón")
    y = big(d, y + 30, "3.2", "yardas avanza Green Bay cada vez que corre. Es el peor de los 32 equipos (el promedio es 4.3).", NEG)
    say(d, y + 30, "Y no es una mala racha: con tantos intentos, la probabilidad de que sea casualidad es de 6 en 1,000.", 32, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "El punto débil de Carolina"); tag(d, 2)
    y = head(d, "Justo enfrente: una defensa que deja correr")
    y = big(d, y + 30, "5.3", "yardas permite Carolina cada vez que le corren, de las peores de la liga.", AMBER)
    say(d, y + 30, "El peor ataque por tierra contra una de las defensas que más permiten. Algo tiene que ceder, y ahí se decide el partido.", 32, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Todo lo demás"); tag(d, 3)
    y = head(d, "Fuera de eso, están casi iguales")
    y += 30
    say(d, y, "Medimos cuántos puntos gana o pierde cada equipo en promedio por jugada, sumando ataque y defensa:", 30, MUTED)
    y = hbars(d, y + 110, [("Carolina", .04, GHOST), ("Green Bay", .05, ACC)], .06, "{:+.2f}")
    say(d, y + 20, "Casi lo mismo. Green Bay es favorito sobre todo por jugar en casa y por su defensa (la 4ª mejor). Nuestro cálculo: Green Bay gana por unos 2 puntos.", 32, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "Por qué el mercado ve más"); tag(d, 4)
    y = head(d, "Esta temporada, el mercado ha acertado más que nosotros")
    y += 30
    say(d, y, "Error promedio de las predicciones en 75 partidos (menos es mejor):", 30, MUTED)
    y = hbars(d, y + 70, [("El mercado", .240, GHOST), ("Nuestro modelo", .258, NEG)], .27, "{:.3f}")
    say(d, y + 20, "Lo decimos claro: en NFL nuestro modelo todavía no le gana al mercado. Y el mercado ya toma en cuenta las bajas: Green Bay sin Micah Parsons y Carolina sin Taylor Moton.", 32, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Green Bay es favorito, y todo se define corriendo", size=78)
    y = bullets(d, y + 40, ["Favorito ligero: 56% para nosotros, 63% para el mercado.",
                            "Si Green Bay logra correr contra esta defensa, gana.",
                            "Si no, Carolina tiene muchas opciones: partido abierto."])
    say(d, y + 20, "¿A quién le crees: al mercado o a los números?", 34, ACC)
    method(d, "Método: ganancia promedio de puntos por jugada (EPA) de cada equipo en ataque y defensa, semanas 1–7, más ventaja de local. Mercado: precios convertidos a probabilidad sin el margen de la casa. Datos: nflverse (CC-BY 4.0). Análisis independiente, no afiliado a la NFL. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ C · NBA MEM @ POR
def C():
    s = []
    im, d = base(); kicker(d, "Basquetbol · NBA · Jueves 29 de octubre")
    y = head(d, "Grizzlies vs. Trail Blazers: dos invictos, pero solo uno es real", size=76)
    y = chips(d, y + 30, ["Memphis Grizzlies (4-0) visitan a Portland Trail Blazers (3-0)",
                          "Jueves 29 oct · 20:00 hora CDMX",
                          "Primer duelo de Ja Morant contra su exequipo"])
    say(d, y + 26, "Nosotros: Portland gana 2 de cada 3 veces. 4 datos de por qué.", 38, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "El 4-0 de Memphis"); tag(d, 1)
    y = head(d, "Memphis le ganó a equipos del fondo de la liga")
    y = big(d, y + 30, "3 de 4", "de sus victorias fueron contra dos de los peores equipos de la liga: Utah (dos veces) y Sacramento.", NEG, 160)
    say(d, y + 30, "Ganar mucho contra rivales débiles infla el récord.", 32, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "El 3-0 de Portland"); tag(d, 2)
    y = head(d, "Portland le ganó a mejores rivales, y por más")
    y = big(d, y + 30, "+18.7", "puntos de ventaja por partido, incluida una victoria de visita contra los Lakers.")
    say(d, y + 30, "Memphis gana por 9.8 en promedio: la mitad, y contra rivales más débiles.", 32, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Ajustando por rivales"); tag(d, 3)
    y = head(d, "Corrigiendo por la calidad de los rivales, Portland es mucho mejor")
    y += 30
    say(d, y, "Nuestro ranking de los 30 equipos, que toma en cuenta contra quién jugó cada uno:", 30, MUTED)
    y = rankbar(d, y + 110, [("Portland", 8, ACC), ("Memphis", 17, NEG)])
    say(d, y + 10, "Portland es mejor atacando y defendiendo. Memphis, en realidad, está a media tabla.", 32, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "La predicción"); tag(d, 4)
    y = head(d, "Todos ven ganar a Portland")
    y = mvm(d, y + 40, "Portland gana", .66, .73, lk="El mercado de predicción")
    say(d, y + 10, "Diferencia esperada: Portland por 6 puntos. Somos un poco más cautos porque nuestro modelo todavía toma en cuenta la temporada pasada, y estos equipos cambiaron mucho (empezando por Morant).", 30, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Portland es el invicto de verdad", size=80)
    y = bullets(d, y + 40, ["El 4-0 de Memphis fue contra rivales débiles.",
                            "Portland ganó contra mejores equipos y por más.",
                            "Portland gana 2 de cada 3 veces."])
    say(d, y + 20, "¿Morant le gana a su exequipo? Te leemos.", 34, ACC)
    method(d, NBA_M)
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ D · Superclásico
def D():
    s = []
    im, d = base(); kicker(d, "Futbol · Argentina · Domingo 1 de noviembre")
    y = head(d, "Boca vs. River: el clásico donde casi 1 de cada 3 partidos termina empatado", size=72)
    y = chips(d, y + 30, ["Superclásico en La Bombonera (casa de Boca)", "Domingo 1 nov · 12:00 hora CDMX", "Torneo Clausura 2026"])
    say(d, y + 26, "¿Quién llega mejor y qué esperar? 4 datos.", 38, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "La historia"); tag(d, 1)
    y = head(d, "En más de 100 años, ninguno domina al otro")
    y += 40
    say(d, y, "266 Superclásicos oficiales:", 30, MUTED)
    y = stacked(d, y + 50, (94 / 266, 84 / 266, 88 / 266), ("Boca 94", "Empate 84", "River 88"), (GHOST, ACC, MUTED))
    say(d, y + 20, "Boca le lleva solo 6 victorias de ventaja en un siglo. Revisamos si eso es una diferencia real: no lo es, es casualidad. Están parejos.", 32, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Cómo llega Boca"); tag(d, 2)
    y = head(d, "Boca casi no pierde")
    y = big(d, y + 30, "1 de 14", "partidos perdió Boca en el Torneo Clausura (7 ganados, 6 empatados).", ACC, 160)
    say(d, y + 30, "Además es líder de la tabla anual. Difícil de vencer, aunque empata seguido.", 32, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Cómo llega River"); tag(d, 3)
    y = head(d, "River llega irregular y con urgencia")
    y = big(d, y + 30, "5 de 14", "partidos perdió River en el Clausura (7 ganados, solo 2 empates).", NEG, 160)
    say(d, y + 30, "Es 7° en la tabla anual, 3 puntos debajo del último lugar que da boleto a la Copa Libertadores. Necesita ganar.", 32, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "Lo que dice el mercado"); tag(d, 4)
    y = head(d, "Boca es favorito; el empate, igual que siempre")
    y += 40
    say(d, y, "Probabilidad para este domingo:", 30, MUTED)
    y = stacked(d, y + 50, (.422, .308, .270), ("Boca", "Empate", "River"), (GHOST, ACC, MUTED))
    say(d, y + 20, "Comparado con la historia, el mercado le suma a Boca por jugar en casa y llegar mejor. Bajas: Boca sin Aranda, Belmonte, Bareiro ni Marchesín; River sin Fausto Vera.", 30, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Boca es favorito, pero la mayoría de las veces no gana", size=76)
    y = bullets(d, y + 40, ["Boca gana 4 de cada 10 veces.",
                            "Empate: 3 de cada 10, como siempre en este clásico.",
                            "River: el menos probable, pero el que más lo necesita."])
    say(d, y + 20, "¿Se rompe la tendencia en La Bombonera?", 34, ACC)
    method(d, "Método: historial de 266 Superclásicos oficiales y prueba estadística de si la ventaja de Boca es real (no lo es); forma en el Clausura 2026; mercado: precios convertidos a probabilidad sin el margen de la casa. Datos públicos de prensa al 28 oct. Análisis independiente, no afiliado a la LPF ni a los clubes. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ E · NBA CLE @ ATL
def E():
    s = []
    im, d = base(); kicker(d, "Basquetbol · NBA · Jueves 29 de octubre")
    y = head(d, "Cavaliers vs. Hawks: el partido donde más diferimos del mercado", size=76)
    y = chips(d, y + 30, ["Cleveland Cavaliers (2-1) visitan a Atlanta Hawks (2-2)", "Jueves 29 oct · 17:00 hora CDMX"])
    say(d, y + 26, "El mercado lo ve 50/50. Nosotros: Atlanta gana 6 de cada 10. ¿Por qué? 4 datos.", 38, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "Cómo vienen jugando"); tag(d, 1)
    y = head(d, "Atlanta viene ganando por mucho")
    y = big(d, y + 30, "+9.2", "puntos de ventaja por partido para Atlanta, incluida una paliza de 128-81 a Charlotte.")
    say(d, y + 30, "Cleveland, en cambio, pierde por 0.7 puntos en promedio.", 32, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Ajustando por rivales"); tag(d, 2)
    y = head(d, "Corrigiendo por la calidad de los rivales, Atlanta sigue arriba")
    y += 30
    say(d, y, "Nuestro ranking de los 30 equipos, que toma en cuenta contra quién jugó cada uno:", 30, MUTED)
    y = rankbar(d, y + 110, [("Atlanta", 6, ACC), ("Cleveland", 13, GHOST)])
    say(d, y + 10, "Atlanta es mejor atacando y defendiendo en lo que va de la temporada.", 32, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "El cansancio"); tag(d, 3)
    y = head(d, "Los dos jugaron la noche anterior: se compensa")
    y = big(d, y + 30, "−2", "puntos rinde en promedio un equipo que juega dos noches seguidas (lo medimos en más de 1,200 partidos).", NEG)
    say(d, y + 30, "Como les pasa a los dos, se cancela. Queda la diferencia de nivel y que Atlanta juega en casa: Atlanta por 4 a 5 puntos.", 32, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "¿Por qué el mercado lo ve parejo?"); tag(d, 4)
    y = head(d, "El mercado le cree más al Cleveland del año pasado")
    y = mvm(d, y + 40, "Atlanta gana", .62, .50, lk="El mercado de predicción")
    say(d, y + 10, "Cleveland fue mejor que Atlanta la temporada pasada; nosotros le damos más peso a cómo juegan ahora. Si gana Cleveland, el mercado tenía razón y lo diremos en el resumen del día.", 30, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Atlanta es favorito para nosotros, y lo vamos a poner a prueba", size=76)
    y = bullets(d, y + 40, ["Atlanta juega mejor esta temporada.",
                            "El cansancio afecta a los dos por igual.",
                            "Atlanta gana 6 de cada 10 veces; el mercado dice 5."])
    say(d, y + 20, "¿Tú con quién vas: con el modelo o con el mercado?", 34, ACC)
    method(d, NBA_M)
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ F · NBA SAC @ NOP
def F_():
    s = []
    im, d = base(); kicker(d, "Basquetbol · NBA · Jueves 29 de octubre")
    y = head(d, "Kings vs. Pelicans: uno de los dos por fin va a ganar", size=78)
    y = chips(d, y + 30, ["Sacramento Kings (0-4) visitan a New Orleans Pelicans (0-3)", "Jueves 29 oct · 18:00 hora CDMX"])
    say(d, y + 26, "Nosotros: Nueva Orleans gana 6 de cada 10 veces. 4 datos.", 38, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "Cómo llega Sacramento"); tag(d, 1)
    y = head(d, "Sacramento no pierde: lo golean")
    y = big(d, y + 30, "−17.8", "puntos por partido. Perdió por 25, 8, 11 y 27.", NEG)
    say(d, y + 30, "En nuestro ranking es el peor de los 30 equipos.", 32, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Cómo llega Nueva Orleans"); tag(d, 2)
    y = head(d, "Nueva Orleans pierde, pero cerrado")
    y = big(d, y + 30, "3, 1 y 6", "puntos: así de cerca estuvo en sus tres derrotas.", AMBER, 150)
    say(d, y + 30, "Está más cerca de ganar que Sacramento: es 23° de 30 en nuestro ranking.", 32, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "La única carta de Sacramento"); tag(d, 3)
    y = head(d, "Nueva Orleans jugó la noche anterior; Sacramento descansó")
    y = big(d, y + 30, "−2", "puntos rinde en promedio un equipo que juega dos noches seguidas (medido en más de 1,200 partidos).", NEG)
    say(d, y + 30, "Le resta a Nueva Orleans, pero no le alcanza a Sacramento: Nueva Orleans sigue arriba por unos 4 puntos.", 32, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "La predicción"); tag(d, 4)
    y = head(d, "Todos ven ganar a Nueva Orleans")
    y = mvm(d, y + 40, "Nueva Orleans gana", .61, .69, lk="El mercado de predicción")
    say(d, y + 10, "Somos un poco más cautos porque le restamos el cansancio. El mercado parece pesar más lo mal que llega Sacramento.", 30, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Nueva Orleans debería quitarse el cero", size=80)
    y = bullets(d, y + 40, ["Sacramento es el peor equipo de la liga ahora mismo.",
                            "Nueva Orleans pierde por poco: está cerca de ganar.",
                            "Nueva Orleans gana 6 de cada 10 veces."])
    say(d, y + 20, "¿Sacramento llega a 0-5? Te leemos.", 34, ACC)
    method(d, NBA_M)
    footer(d, 6, T); s.append(im)
    return s


if __name__ == "__main__":
    for k, fn in (("B", B), ("C", C), ("D", D), ("E", E), ("F", F_)):
        o = f"{OUT}/{k}"
        os.makedirs(o, exist_ok=True)
        for i, im in enumerate(fn(), 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
