"""xGol — 29 oct, formato v4 con ÁNGULOS v5 (no solo quién gana):
B NFL «¿partido de pocos puntos?», C NBA «Morant por Grant», E NBA «el partido de más puntos», F NBA «duelo de 0-4».
Los números NBA se leen de NBA_JSON (datos hasta el 28 oct)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font as F, base, para, wrap, BG, TXT, ACC, NEG, W, H, M
from story_lib import MUTED, LINE, SURF, GHOST, AMBER, kicker, footer
from scroll_rest_1029 import head, say, tag, big, chips, bullets, hbars, rankbar, mvm, method, NBA_M

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/v5")
N = json.load(open(os.environ["NBA_JSON"]))
T = 6


def vbars(d, y, items, vmax, h=300, ref=None):
    """Barras verticales: items = (etiqueta, real, esperado|None)."""
    n = len(items)
    bw = (W - 2 * M) / n
    base_y = y + h
    for i, (lab, real, exp) in enumerate(items):
        cx = M + bw * i + bw / 2
        if exp is not None:
            te = base_y - h * exp / vmax
            d.rounded_rectangle((cx - 48, te, cx + 48, base_y), radius=10, outline=GHOST, width=3)
            d.text((cx - 48, te - 34), f"{exp:g}", font=F("Inter-Medium.otf", 22), fill=GHOST)
        tr = base_y - h * real / vmax
        col = ACC if (exp is None or real < exp) else NEG
        d.rounded_rectangle((cx - 32, tr, cx + 32, base_y), radius=8, fill=col)
        t = f"{real:g}"; ft = F("InterDisplay-Black.otf", 34)
        d.text((cx - d.textlength(t, font=ft) / 2, tr + 8 if exp is not None and tr - te < 60 else tr - 44), t, font=ft, fill=BG if exp is not None and tr - te < 60 else TXT)
        fl = F("Inter-SemiBold.otf", 22)
        d.text((cx - d.textlength(lab, font=fl) / 2, base_y + 12), lab, font=fl, fill=MUTED)
    return base_y + 50


def statrow(d, y, cells):
    cw = (W - 2 * M) // len(cells)
    for k, (v, l, col) in enumerate(cells):
        x = M + k * cw
        d.text((x, y), v, font=F("InterDisplay-Black.otf", 64), fill=col)
        para(d, (x, y + 78), l, F("Inter-Medium.otf", 24), MUTED, cw - 24, 30)
    return y + 170


# ============================================================ B · NFL
def B():
    s = []
    im, d = base(); kicker(d, "Futbol americano · NFL · Jueves 29 de octubre")
    y = head(d, "Panthers vs. Packers: ¿un partido de pocos puntos?", size=80)
    y = chips(d, y + 30, ["Carolina Panthers (3-3, líderes de su división) visitan a Green Bay Packers (4-3)", "Jueves 29 oct · 18:15 hora CDMX"])
    say(d, y + 26, "El mercado espera unos 47 puntos entre los dos equipos. Los últimos partidos de Green Bay dicen otra cosa. 4 datos.", 36, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "La racha de Green Bay"); tag(d, 1)
    y = head(d, "Green Bay viene de 4 partidos con muy pocos puntos")
    y += 40
    d.text((M, y), "Puntos totales de cada partido:", font=F("Inter-Medium.otf", 25), fill=MUTED)
    d.rounded_rectangle((M, y + 44, M + 26, y + 70), radius=4, fill=ACC)
    d.text((M + 38, y + 40), "real", font=F("Inter-Bold.otf", 25), fill=ACC)
    d.rounded_rectangle((M + 140, y + 44, M + 166, y + 70), radius=4, outline=GHOST, width=3)
    d.text((M + 178, y + 40), "lo que esperaba el mercado", font=F("Inter-Bold.otf", 25), fill=GHOST)
    y += 40
    y = vbars(d, y + 70, [("Semana 4", 31, 38.5), ("Semana 5", 38, 46.5), ("Semana 6", 36, 53.5), ("Semana 7", 37, 55.5)], 60, 330)
    say(d, y + 10, "Promedio: 35.5 puntos por partido, cuando el mercado esperaba 48.5. En los cuatro hubo menos puntos de lo esperado.", 30, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "¿Por qué tan pocos puntos?"); tag(d, 2)
    y = head(d, "Una defensa de élite y un ataque que no puede correr")
    y = statrow(d, y + 40, [("4°", "mejor defensa de la liga (de 32)", ACC), ("6°", "mejor defensa contra el pase", ACC), ("32°", "ataque por tierra: el peor", NEG)])
    say(d, y + 10, "Green Bay frena a sus rivales, pero tampoco acelera: avanza solo 3.2 yardas cada vez que corre (promedio de la liga: 4.3). Partidos lentos y cerrados.", 30, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "El riesgo"); tag(d, 3)
    y = head(d, "Pero Carolina es una montaña rusa")
    y += 40
    d.text((M, y), "Puntos totales en cada partido de Carolina:", font=F("Inter-Medium.otf", 25), fill=MUTED)
    y = vbars(d, y + 60, [("S1", 96, None), ("S2", 37, None), ("S3", 39, None), ("S4", 58, None), ("S6", 39, None), ("S7", 56, None)], 100, 300)
    say(d, y + 10, "De 37 a 96 puntos. Y siendo críticos: 7 partidos son pocos; la racha de Green Bay todavía no es una tendencia comprobada (puede ser casualidad).", 30, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "El duelo de mariscales"); tag(d, 4)
    y = head(d, "Bryce Young lanza mucho… ¿pero lanza bien?")
    y += 40
    rows = [("", "Bryce Young", "Jordan Love"), ("Yardas por partido", "285 (2°)", "280 (4°)"), ("Eficiencia por jugada", "15°", "11°")]
    for i, (a, b, c) in enumerate(rows):
        f = F("Inter-SemiBold.otf", 26) if i == 0 else F("InterDisplay-Bold.otf", 38)
        d.text((M, y + 6), a, font=F("Inter-Medium.otf", 26), fill=TXT)
        d.text((560, y), b, font=f, fill=GHOST if i == 0 else TXT)
        d.text((820, y), c, font=f, fill=GHOST if i == 0 else TXT)
        y += 70 if i == 0 else 84
        if i:
            d.line((M, y - 14, W - M, y - 14), fill=LINE, width=2)
    say(d, y + 20, "Young (Carolina) es de los que más yardas suman, pero no de los más eficientes: necesita muchas jugadas para avanzar. Enfrente tiene a la 6ª mejor defensa contra el pase.", 30, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Todo apunta a un partido cerrado y de pocos puntos", size=78)
    y = bullets(d, y + 40, ["Green Bay: 4 partidos seguidos con menos puntos de lo esperado.",
                            "Su defensa frena y su ataque no acelera.",
                            "El riesgo: Carolina es capaz de partidos de 96 puntos.",
                            "Nuestro modelo: Green Bay gana 56 de cada 100."], 32)
    say(d, y + 10, "¿Partido cerrado o lluvia de puntos? Te leemos.", 34, ACC)
    method(d, "Método: puntos esperados por jugada (EPA) de ataque y defensa de cada equipo, semanas 1–7; ranking de defensas por EPA permitida; prueba t de los puntos totales de Green Bay contra el promedio de la liga (no significativa). Datos: nflverse (CC-BY 4.0); referencia del mercado pública. Análisis independiente, no afiliado a la NFL. No es recomendación de apuesta.")
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ C · NBA MEM @ POR
def C():
    c = N["MEM@POR"]
    s = []
    im, d = base(); kicker(d, "Basquetbol · NBA · Jueves 29 de octubre")
    y = head(d, "Grizzlies vs. Trail Blazers: el reencuentro de Morant", size=80)
    y = chips(d, y + 30, [f"Memphis Grizzlies ({c['rec_a']}) visitan a Portland Trail Blazers ({c['rec_h']})", "Jueves 29 oct · 20:00 hora CDMX",
                          "29 de junio: Memphis cambió a Ja Morant por Jerami Grant y Kris Murray"])
    say(d, y + 26, "Primer duelo desde el cambio, y los dos llegan invictos. ¿A quién le salió mejor? 4 datos.", 36, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "Por qué Memphis lo cambió"); tag(d, 1)
    y = head(d, "Memphis necesitaba pasar la página")
    y = big(d, y + 30, "79 de 246", "partidos jugó Morant en sus últimas 3 temporadas con Memphis, entre lesiones y suspensiones.", AMBER, 140)
    say(d, y + 30, "Dos veces All-Star y Novato del Año, pero en los últimos años casi no estuvo. Memphis apostó por empezar de nuevo.", 30, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Morant en Portland"); tag(d, 2)
    y = head(d, "En Portland juega menos… y tira mejor")
    y += 40
    rows = [("", "2025-26 (Memphis)", "Hoy (Portland)"), ("Puntos por partido", "19.5", "13.0"), ("% de tiros anotados", "41%", "52%")]
    for i, (a, b, cc) in enumerate(rows):
        f = F("Inter-SemiBold.otf", 24) if i == 0 else F("InterDisplay-Bold.otf", 40)
        d.text((M, y + 6), a, font=F("Inter-Medium.otf", 26), fill=TXT)
        d.text((520, y), b, font=f, fill=GHOST if i == 0 else MUTED)
        d.text((800, y), cc, font=f, fill=GHOST if i == 0 else ACC)
        y += 64 if i == 0 else 84
        if i:
            d.line((M, y - 14, W - M, y - 14), fill=LINE, width=2)
    say(d, y + 20, "Ya no tiene que cargar con todo: comparte la pelota con Lillard, Avdija y Holiday. Menos puntos, pero mucho más eficiente, en 24 minutos por partido.", 30, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Memphis sin Morant"); tag(d, 3)
    y = head(d, "Memphis va invicto… pero contra rivales débiles")
    y = statrow(d, y + 40, [("29.8", "puntos por partido de Ty Jerome, su nuevo líder", ACC), ("15.3 · 10.5", "puntos y rebotes del novato Cam Boozer", GHOST)])
    say(d, y, f"Ojo: 3 de sus 4 victorias fueron contra Utah (dos veces) y Sacramento, de los peores de la liga. Ajustado por rivales, Memphis es {c['rank_a']}° de 30 y Portland {c['rank_h']}°.", 30, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "¿Cómo será el partido?"); tag(d, 4)
    y = head(d, "Ritmo lento, pero puntos normales")
    y = statrow(d, y + 40, [("22°", "Memphis en ritmo de juego (de 30)", GHOST), ("20°", "Portland en ritmo de juego", GHOST), (f"{c['total']:.0f}", f"puntos totales proyectados (promedio de la liga: {N['league_total']:.0f})", ACC)])
    say(d, y, f"Los dos juegan pausado, pero anotan bien cuando atacan: por eso proyectamos puntos en el promedio. Nuestro modelo: Portland gana {c['freq']} veces ({c['p_home']}%), por unos {c['margin']:.0f} puntos. El mercado lo ve igual, con un poco más de confianza ({c['mkt']}%).", 30, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Por ahora, el cambio le sale bien a los dos", size=80)
    y = bullets(d, y + 40, ["Morant: menos carga, más eficiencia, en un equipo que gana.",
                            "Memphis: invicto con caras nuevas, pero aún sin probarse contra los buenos.",
                            f"Portland es favorito: gana {c['freq']} veces.",
                            "Esperamos un partido pausado, con puntos en el promedio."], 32)
    say(d, y + 10, "¿Quién ganó el cambio? Te leemos.", 34, ACC)
    method(d, NBA_M + " Ritmo y estadísticas individuales: Basketball-Reference y ESPN.")
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ E · NBA CLE @ ATL
def E():
    e = N["CLE@ATL"]
    s = []
    im, d = base(); kicker(d, "Basquetbol · NBA · Jueves 29 de octubre")
    y = head(d, "Cavaliers vs. Hawks: el partido con más puntos esperados del jueves", size=74)
    y = chips(d, y + 30, [f"Cleveland Cavaliers ({e['rec_a']}) visitan a Atlanta Hawks ({e['rec_h']})", "Jueves 29 oct · 17:00 hora CDMX"])
    say(d, y + 26, f"Proyectamos unos {e['total']:.0f} puntos entre los dos, el más alto de la noche. 4 datos de por qué.", 36, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "El estilo de Atlanta"); tag(d, 1)
    y = head(d, "Atlanta juega rápido y lanza muchísimos triples")
    y = big(d, y + 30, "42", "triples intenta Atlanta por partido, y juega a uno de los ritmos más altos de la liga (9° de 30).")
    say(d, y + 30, "Más posesiones y más tiros de tres = más puntos, para los dos lados.", 30, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "El jugador a seguir"); tag(d, 2)
    y = head(d, "Jalen Johnson hace de todo")
    y = statrow(d, y + 40, [("21.5", "puntos por partido", ACC), ("9.8", "rebotes", ACC), ("8.5", "asistencias", ACC)])
    say(d, y, "Está a centímetros de promediar un triple-doble. Si Atlanta corre, todo pasa por sus manos.", 32, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "El estilo de Cleveland"); tag(d, 3)
    y = head(d, "Cleveland anota… y también recibe")
    y += 40
    d.text((M, y), "Puntos totales en cada partido de Cleveland:", font=F("Inter-Medium.otf", 25), fill=MUTED)
    y = vbars(d, y + 60, [(l, v, None) for l, v in e["cle_totals"]], 270, 300)
    say(d, y + 10, f"Cleveland anota {e['cle_pf']:.0f} y recibe {e['cle_pa']:.0f} por partido: sus partidos casi nunca son lentos. Y Atlanta acaba de recibir 129 de Miami.", 30, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "La predicción"); tag(d, 4)
    y = head(d, "Atlanta, favorito en un partido de muchos puntos")
    y = mvm(d, y + 40, "Atlanta gana", e["p_home"] / 100, e["mkt"] / 100, lk="El mercado de predicción")
    say(d, y + 10, f"Nosotros vemos a Atlanta más fuerte por cómo juega esta temporada (es {e['rank_h']}° de 30 en nuestro ranking; Cleveland, {e['rank_a']}°). El mercado le da más peso al Cleveland del año pasado. Los dos jugaron la noche anterior, así que el cansancio no inclina la balanza.", 28, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Prepárate para muchos puntos en Atlanta", size=80)
    y = bullets(d, y + 40, [f"Unos {e['total']:.0f} puntos proyectados: lo más alto del jueves.",
                            "Atlanta corre y tira de tres; Jalen Johnson lo mueve todo.",
                            f"Atlanta gana {e['freq']} veces para nosotros."], 32)
    say(d, y + 10, "¿Partido de 240 puntos? Te leemos.", 34, ACC)
    method(d, NBA_M + " Ritmo, triples y estadísticas individuales: Basketball-Reference (primeros partidos de la temporada).")
    footer(d, 6, T); s.append(im)
    return s


# ============================================================ F · NBA SAC @ NOP
def F_():
    f = N["SAC@NOP"]
    s = []
    im, d = base(); kicker(d, "Basquetbol · NBA · Jueves 29 de octubre")
    y = head(d, "Kings vs. Pelicans: el duelo de los que no han ganado", size=80)
    y = chips(d, y + 30, [f"Sacramento Kings ({f['rec_a']}) visitan a New Orleans Pelicans ({f['rec_h']})", "Jueves 29 oct · 18:00 hora CDMX"])
    say(d, y + 26, "Uno de los dos se quita el cero. ¿Quién? 4 datos.", 38, ACC)
    footer(d, 1, T); s.append(im)

    im, d = base(); kicker(d, "La paradoja de Sacramento"); tag(d, 1)
    y = head(d, "Sacramento tiene estrellas… y una de las peores defensas")
    y = statrow(d, y + 40, [("29", "puntos por partido de Zach LaVine", ACC), ("17.3", "rebotes de Sabonis: líder de la liga", ACC), (f"{f['sac_pa']:.0f}", "puntos que recibe Sacramento por partido", NEG)])
    say(d, y, "Los números individuales brillan, pero el equipo recibe más de lo que anota. Las estadísticas de un jugador no ganan partidos.", 30, TXT)
    footer(d, 2, T); s.append(im)

    im, d = base(); kicker(d, "Cómo pierde Sacramento"); tag(d, 2)
    y = head(d, "Sacramento no pierde: lo golean")
    y = big(d, y + 30, f"{f['sac_diff']:+.1f}".replace("-", "−"), "puntos por partido. Perdió por " + f["sac_margins"] + ".", NEG)
    say(d, y + 30, "Es el último de los 30 equipos en nuestro ranking.", 30, TXT)
    footer(d, 3, T); s.append(im)

    im, d = base(); kicker(d, "Cómo pierde Nueva Orleans"); tag(d, 3)
    y = head(d, "Nueva Orleans pierde, pero casi siempre cerca")
    y = big(d, y + 30, f["nop_margins_short"], "puntos: así de cerca estuvo en 3 de sus 4 derrotas. Anoche sí perdió por 13 contra Denver.", AMBER, 130)
    say(d, y + 30, f"Es {f['rank_h']}° de 30 en nuestro ranking, lejos del último lugar de Sacramento. Su desventaja: jugó anoche, y eso resta unos 2 puntos en promedio.", 30, TXT)
    footer(d, 4, T); s.append(im)

    im, d = base(); kicker(d, "La predicción"); tag(d, 4)
    y = head(d, "Nueva Orleans debería quitarse el cero")
    y = mvm(d, y + 40, "Nueva Orleans gana", f["p_home"] / 100, f["mkt"] / 100, lk="El mercado de predicción")
    say(d, y + 10, f"Los dos coinciden. Nosotros somos un poco más cautos porque le restamos a Nueva Orleans el cansancio. Diferencia esperada: Nueva Orleans por {f['margin']:.0f}.", 30, TXT)
    footer(d, 5, T); s.append(im)

    im, d = base(); kicker(d, "Conclusión")
    y = head(d, "Estrellas sin defensa contra derrotas por poco", size=80)
    y = bullets(d, y + 40, ["Sacramento: grandes números individuales, peor equipo de la liga.",
                            "Nueva Orleans: pierde cerrado, está cerca de ganar.",
                            f"Nueva Orleans gana {f['freq']} veces para nosotros."], 32)
    say(d, y + 10, "¿Sacramento llega a 0-5? Te leemos.", 34, ACC)
    method(d, NBA_M + " Estadísticas individuales: Basketball-Reference.")
    footer(d, 6, T); s.append(im)
    return s


if __name__ == "__main__":
    for k, fn in (("B", B), ("C", C), ("E", E), ("F", F_)):
        o = f"{OUT}/{k}"
        os.makedirs(o, exist_ok=True)
        for i, im in enumerate(fn(), 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
