"""xGol — los 6 posts del 29 oct con el motor de layout v7 (contenido v6: ángulos + «Lo que probamos»)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *

N = json.load(open(os.environ["NBA_JSON"]))
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/v7")
NBA_M = ("Método: nivel de cada equipo ajustado por la calidad de sus rivales (parte de 90% del nivel 2025-26, recalibrado el 29 oct), localía y cansancio "
         "(−2.1 pts por jugar dos noches seguidas). Probado en 1,090 partidos: acertó 69%. Pruebas con la temporada 2025-26. Datos: BALLDONTLIE, "
         "Basketball-Reference, ESPN; mercado de predicción público. Análisis independiente, no afiliado a la NBA. No es recomendación de apuesta.")
SUB_NBA = "Hipótesis puestas a prueba con la temporada NBA 2025-26. Si «p» es menor a 0.05, casi seguro no es casualidad."


def A():
    T = 6
    return [
        slide(1, T, "Béisbol · Serie Mundial 2026 (la final de MLB)", "Los Brewers de Milwaukee son campeones por primera vez en su historia",
              [Matchup("Milwaukee", "4", "Tampa Bay", "1", sep="Serie Mundial · último juego: miércoles 28 oct", a_col=ACC)],
              takeaway="¿Fue suerte o lo merecían? Lo revisamos con 4 datos.", style="cover", title_size=96),
        slide(2, T, "La temporada", "Fueron el mejor equipo de todo el año",
              [Hero("103", "victorias en temporada regular, más que cualquiera de los 30 equipos de MLB."),
               HBars([("Milwaukee", 103, ACC), ("Tampa Bay", 98, GHOST)], 110, "{}", 280)],
              takeaway="Su rival en la final también fue el mejor de su liga, pero ganó 5 partidos menos.", tag="DATO 1 DE 4"),
        slide(3, T, "¿Fue suerte?", "Milwaukee ganó lo que merecía. Tampa Bay ganó de más.",
              [Text("Con las carreras que anotas y las que recibes se calcula cuántos partidos «deberías» ganar:", 30, MUTED),
               Table(("Debía ganar", "Ganó"), [("Milwaukee", "102.5", "103"), ("Tampa Bay", "90.2", "98")], colors=[GHOST, ACC]),
               Stats([("+0.5", "Milwaukee: justo lo esperado", ACC), ("+7.8", "Tampa Bay: victorias de más", NEG)])],
              takeaway="Milwaukee ganó justo lo esperado (103 vs. 102.5). Tampa Bay ganó 8 de más, algo que suele venir de ganar juegos cerrados (aunque con una temporada no se puede probar que fue suerte).", tag="DATO 2 DE 4"),
        slide(4, T, "Antes de empezar la final", "Ya eran favoritos antes del primer juego",
              [Hero("7 de 10", "veces ganaba Milwaukee la Serie, según nuestro modelo (68%). El mercado le daba 62%."),
               Stats([("68%", "nuestro modelo", ACC), ("62%", "el mercado", GHOST)])],
              takeaway="Comparamos la fuerza de los dos equipos y simulamos todos los resultados posibles de la serie, juego por juego.", tag="DATO 3 DE 4"),
        slide(5, T, "La final, juego por juego", "Ganaron los juegos apretados",
              [VBars([("J1", 3, None), ("J2", 5, None), ("J3", 10, None), ("J4", 3, None), ("J5", 4, None)], 11),
               Stats([("3 de 5", "juegos se definieron por una sola carrera", AMBER), ("2 de 3", "de esos los ganó Milwaukee", ACC)])],
              takeaway="Carreras de Milwaukee en cada juego. Ganó el 1, 2, 3 y 5; perdió el 4 por una carrera en 12 entradas.", tag="DATO 4 DE 4"),
        slide(6, T, "Conclusión", "Campeón merecido: ganó el mejor equipo del año",
              [Bullets(["El mejor récord de MLB: 103 victorias.", "Su récord iba de acuerdo con sus carreras.", "Era favorito: 7 de cada 10.", "Ganó los juegos de una carrera."])],
              takeaway="Y pensar que en agosto el mercado solo le daba 9%. ¿Lo viste venir?", style="end",
              method="Método: victorias esperadas con la fórmula pitagórica (carreras anotadas y recibidas); simulación de la serie con la fuerza de cada equipo y la ventaja de local. Datos públicos 2026. Análisis independiente, no afiliado a MLB. No es recomendación de apuesta."),
    ]


def B():
    T = 7
    return [
        slide(1, T, "Futbol americano · NFL · Jueves 29 de octubre", "Panthers vs. Packers: ¿la racha de pocos puntos de Green Bay significa algo?",
              [Matchup("Panthers", "3-3", "Packers", "4-3", sep="visitan a · jueves 29 oct · 18:15 hora CDMX"), Chips(["Carolina lidera su división; Green Bay es último de la suya"])],
              takeaway="Lo probamos con 15 años de datos de la NFL. Spoiler: la racha no dice nada. Pero hay algo que sí.", style="cover"),
        slide(2, T, "La racha", "Green Bay viene de 4 partidos con muy pocos puntos",
              [VBars([("Semana 4", 31, 38.5), ("Semana 5", 38, 46.5), ("Semana 6", 36, 53.5), ("Semana 7", 37, 55.5)], 60, legend=True)],
              takeaway="35.5 puntos por partido cuando se esperaban 48.5. Parece una tendencia clarísima… ¿lo es?", tag="DATO 1 DE 4"),
        slide(3, T, "Lo pusimos a prueba", "Después de una racha así, el siguiente partido es un volado",
              [Hero("50%", "de las veces, el siguiente partido también tuvo menos puntos de lo esperado. Revisamos los 392 casos de 2010 a 2025.", GHOST)],
              takeaway="Es lo mismo que lanzar una moneda: el mercado ya ajusta, así que una racha así no dice nada del próximo partido.", tag="DATO 2 DE 4"),
        slide(4, T, "Lo que sí es real", "Green Bay no sabe correr con el balón",
              [Hero("3.2", "yardas avanza Green Bay cada vez que corre: el peor de los 32 equipos.", NEG),
               HBars([("Green Bay", 3.2, NEG), ("Promedio liga", 4.3, LINE), ("Permite Carolina", 5.3, AMBER)], 6, "{}", 330)],
              takeaway="Lo de Green Bay no es mala suerte (casualidad: 6 en 1,000). Lo de Carolina todavía podría serlo (9 en 100).", tag="DATO 3 DE 4"),
        slide(5, T, "El duelo de mariscales", "Bryce Young lanza mucho… ¿pero lanza bien?",
              [Table(("B. Young", "J. Love"), [("Yardas por partido", "2°", "4°"), ("Eficiencia por jugada", "15°", "11°")], colors=[AMBER, GHOST]),
               Stats([("285", "yardas por partido de Young", AMBER), ("6°", "defensa contra el pase de Green Bay", ACC)])],
              takeaway="Young suma yardas porque lanza mucho, no porque cada pase rinda más. Y enfrente tiene a la 6ª mejor defensa contra el pase.", tag="DATO 4 DE 4"),
        slide(6, T, "Lo que probamos", "Lo que se sostiene y lo que es mito",
              [Text("Con datos de la NFL. Si «p» es menor a 0.05, casi seguro no es casualidad.", 27, MUTED),
               Tests([(False, "«Tras 4 partidos con pocos puntos, viene otro igual»", "392 casos (2010–2025): pasó 50% de las veces.", "p = 0.42"),
                      (False, "«Los jueves se anota menos»", "268 partidos en jueves: igual a lo esperado.", "p = 0.60"),
                      (False, "«Con frío se anota menos»", "670 partidos a 7 °C o menos: igual a lo esperado.", "p = 0.62"),
                      (True, "«Green Bay no sabe correr»", "137 acarreos en 2026: es real, no mala suerte.", "p = 0.006")])]),
        slide(7, T, "Conclusión", "Olvida la racha: el partido se decide corriendo",
              [Bullets(["Las rachas de pocos puntos no predicen nada: 392 casos.", "Lo real: el peor ataque por tierra; enfrente, una defensa que hasta ahora deja correr.", "Nuestro modelo: Green Bay gana 56 de cada 100."])],
              takeaway="¿Sabías que las rachas no significan nada? Te leemos.", style="end",
              method="Método: partidos de temporada regular NFL 2010–2025 comparando puntos reales con la expectativa del mercado; prueba t del ataque terrestre de Green Bay (2026); probabilidad con puntos esperados por jugada (EPA) + localía. Datos: nflverse (CC-BY 4.0). Análisis independiente, no afiliado a la NFL. No es recomendación de apuesta."),
    ]


def C():
    c = N["MEM@POR"]; T = 7
    return [
        slide(1, T, "Basquetbol · NBA · Jueves 29 de octubre", "Grizzlies vs. Trail Blazers: el reencuentro de Morant",
              [Matchup("Grizzlies", c['rec_a'], "Trail Blazers", c['rec_h'], sep="visitan a · jueves 29 oct · 20:00 hora CDMX"), Chips(["29 de junio: Memphis cambió a Ja Morant por Jerami Grant y Kris Murray"])],
              takeaway="Primer duelo desde el cambio, y los dos llegan invictos. ¿A quién le salió mejor?", style="cover"),
        slide(2, T, "Por qué Memphis lo cambió", "Memphis necesitaba pasar la página",
              [Hero("79 de 246", "partidos jugó Morant en sus últimas 3 temporadas con Memphis, entre lesiones y suspensiones.", AMBER),
               Stats([("2×", "All-Star", GHOST), ("2020", "Novato del Año", GHOST), ("32%", "de los partidos jugados", NEG)])],
              takeaway="Talento de sobra, pero casi no estuvo. Memphis apostó por empezar de nuevo.", tag="DATO 1 DE 4"),
        slide(3, T, "Morant en Portland", "En Portland juega menos… y tira mejor",
              [Table(("2025-26", "Hoy"), [("Puntos por partido", "19.5", "13.0"), ("% de tiros anotados", "41%", "52%")]),
               Stats([("24.5", "minutos por partido", GHOST), ("7.5", "asistencias por partido", ACC)])],
              takeaway="Ya no carga con todo: comparte la pelota con Lillard, Avdija y Holiday. Menos puntos, mucho más eficiente.", tag="DATO 2 DE 4"),
        slide(4, T, "¿Un 4-0 dice algo?", "Un arranque fuerte dice algo… pero poco",
              [Hero("3 de 10", "puntos de ventaja de los primeros partidos se mantienen el resto de la temporada (30 equipos, 2025-26).", AMBER),
               Rank([("Portland", c["rank_h"], ACC), ("Memphis", c["rank_a"], NEG)])],
              takeaway="Memphis gana por 9.8 con Ty Jerome (29.8 pts) y el novato Cam Boozer, pero contra rivales débiles. Ajustado por rivales, está en la mitad baja de la liga.", tag="DATO 3 DE 4"),
        slide(5, T, "¿Cómo será el partido?", "Ritmo lento, pero puntos normales",
              [Stats([("22°", "Memphis en ritmo de juego (de 30)", GHOST), ("20°", "Portland en ritmo", GHOST), (f"{c['total']:.0f}", f"puntos proyectados (liga: {N['league_total']:.0f})", ACC)]),
               MvM("Portland gana", c["p_home"] / 100, c["mkt"] / 100)],
              takeaway=f"Los dos juegan pausado, pero anotan bien. Portland gana {c['freq']} veces, por unos {c['margin']:.0f} puntos.", tag="DATO 4 DE 4"),
        slide(6, T, "Lo que probamos", "Lo que se sostiene y lo que es mito",
              [Text(SUB_NBA, 27, MUTED),
               Tests([(True, "«Un buen arranque predice algo»", "Sí, pero de cada 10 puntos de ventaja temprana solo se mantienen unos 3.", "30 equipos · correlación 0.40 · p = 0.03"),
                      (True, "«Ajustar por la calidad de los rivales ayuda»", "Con el ajuste, la relación con el resto de la temporada sube de 0.42 a 0.51.", "correlación 0.51 · p = 0.004"),
                      (False, "«Llegar con más días de descanso da ventaja»", "Un día extra no cambia nada. Solo pesa jugar dos noches seguidas.", "850 partidos · p = 0.74")])]),
        slide(7, T, "Conclusión", "El 4-0 de Memphis vale menos de lo que parece",
              [Bullets(["Morant: menos carga y más eficiencia en un Portland que gana.", "Los arranques fuertes exageran: solo 3 de cada 10 puntos de ventaja se mantienen.", f"Portland gana {c['freq']} veces; partido pausado, unos {c['total']:.0f} puntos."])],
              takeaway="¿Quién ganó el cambio? Te leemos.", style="end", method=NBA_M),
    ]


def E():
    e = N["CLE@ATL"]; T = 7
    return [
        slide(1, T, "Basquetbol · NBA · Jueves 29 de octubre", "Cavaliers vs. Hawks: el partido con más puntos esperados del jueves",
              [Matchup("Cavaliers", e['rec_a'], "Hawks", e['rec_h'], sep="visitan a · jueves 29 oct · 17:00 hora CDMX")],
              takeaway=f"Proyectamos unos {e['total']:.0f} puntos entre los dos, el más alto de la noche. 4 datos de por qué.", style="cover"),
        slide(2, T, "El estilo de Atlanta", "Atlanta juega rápido y lanza muchísimos triples",
              [Hero("42", "triples intenta Atlanta por partido.", ACC), Stats([("9°", "ritmo de juego (de 30)", ACC), ("120", "puntos por partido", ACC)])],
              takeaway="Más posesiones y más tiros de tres = más puntos, para los dos lados.", tag="DATO 1 DE 4"),
        slide(3, T, "El jugador a seguir", "Jalen Johnson hace de todo",
              [Stats([("21.5", "puntos por partido", ACC), ("9.8", "rebotes", ACC), ("8.5", "asistencias", ACC)]), Gap()],
              takeaway="Está a centímetros de promediar un triple-doble. Si Atlanta corre, todo pasa por sus manos.", tag="DATO 2 DE 4"),
        slide(4, T, "El estilo de Cleveland", "Cleveland anota… y también recibe",
              [VBars([(l, v, None) for l, v in e["cle_totals"]], 270)],
              takeaway=f"Puntos totales en cada partido de Cleveland. Anota {e['cle_pf']:.0f} y recibe {e['cle_pa']:.0f}: sus partidos casi nunca son lentos.", tag="DATO 3 DE 4"),
        slide(5, T, "La predicción", "Atlanta, ligero favorito en un partido de muchos puntos",
              [MvM("Atlanta gana", e["p_home"] / 100, e["mkt"] / 100), Rank([("Atlanta", e["rank_h"], ACC), ("Cleveland", e["rank_a"], GHOST)])],
              takeaway="Nosotros y el mercado lo vemos casi parejo; Atlanta tiene una ligera ventaja por jugar en casa y por cómo juega esta temporada.", tag="DATO 4 DE 4"),
        slide(6, T, "Lo que probamos", "Lo que se sostiene y lo que es mito",
              [Text(SUB_NBA, 27, MUTED),
               Tests([(True, "«Si proyectamos muchos puntos, hay muchos puntos»", "Los partidos que proyectamos más altos promediaron 239; los más bajos, 222.", "379 partidos · correlación 0.31 · p < 0.001"),
                      (False, "«Si los dos jugaron anoche, se anota menos»", "Unos 2 puntos menos, pero puede ser casualidad.", "70 partidos · p = 0.36"),
                      (True, "«Jugar dos noches seguidas afecta quién gana»", "El equipo cansado rinde 2.1 puntos menos. Hoy les pasa a los dos: se compensa.", "1,237 partidos · p = 0.011")])]),
        slide(7, T, "Conclusión", "Prepárate para muchos puntos en Atlanta",
              [Bullets([f"Unos {e['total']:.0f} puntos proyectados, lo más alto del jueves.", "Atlanta corre y tira de tres; Jalen Johnson lo mueve todo.", f"Ganador casi parejo: Atlanta {e['p_home']}% para nosotros."])],
              takeaway="¿Partido de 240 puntos? Te leemos.", style="end", method=NBA_M),
    ]


def F_():
    f = N["SAC@NOP"]; T = 7
    return [
        slide(1, T, "Basquetbol · NBA · Jueves 29 de octubre", "Kings vs. Pelicans: el duelo de los que no han ganado",
              [Matchup("Kings", f['rec_a'], "Pelicans", f['rec_h'], sep="visitan a · jueves 29 oct · 18:00 hora CDMX")],
              takeaway="Uno de los dos se quita el cero. ¿Quién? 5 datos.", style="cover"),
        slide(2, T, "La paradoja de Sacramento", "Sacramento tiene estrellas… y una de las peores defensas",
              [Stats([("29", "puntos por partido de Zach LaVine", ACC), ("17.3", "rebotes de Sabonis, líder de la liga", ACC)]),
               Stats([(f"{f['sac_pa']:.0f}", "puntos que recibe Sacramento por partido", NEG)])],
              takeaway="Los números individuales brillan, pero el equipo recibe más de lo que anota. Las estadísticas de un jugador no ganan partidos.", tag="DATO 1 DE 4"),
        slide(3, T, "Cómo pierde Sacramento", "Sacramento no pierde: lo golean",
              [Hero(f"{f['sac_diff']:+.1f}".replace("-", "−"), "puntos por partido en sus 4 derrotas.", NEG),
               VBars([("1", 25, None), ("2", 8, None), ("3", 11, None), ("4", 27, None)], 30)],
              takeaway="Perdió por 25, 8, 11 y 27 puntos. Es el último de los 30 equipos en nuestro ranking.", tag="DATO 2 DE 4"),
        slide(4, T, "Cómo pierde Nueva Orleans", "Nueva Orleans pierde, pero casi siempre cerca",
              [VBars([("1", 3, None), ("2", 1, None), ("3", 6, None), ("4", 13, None)], 30), Rank([("Nueva Orleans", f["rank_h"], AMBER), ("Sacramento", f["rank_a"], NEG)])],
              takeaway="Puntos por los que perdió: 3, 1 y 6; anoche, 13 contra Denver. Su desventaja hoy: jugó anoche.", tag="DATO 3 DE 4"),
        slide(5, T, "La predicción", "Nueva Orleans debería quitarse el cero",
              [MvM("Nueva Orleans gana", f["p_home"] / 100, f["mkt"] / 100),
               Stats([(f"+{f['margin']:.0f}", "diferencia esperada para Nueva Orleans", ACC), (f"{f['total']:.0f}", "puntos totales proyectados", GHOST)])],
              takeaway=f"Los dos coinciden. Somos un poco más cautos porque le restamos el cansancio. Diferencia esperada: Nueva Orleans por {f['margin']:.0f}.", tag="DATO 4 DE 4"),
        slide(6, T, "Lo que probamos", "Lo que se sostiene y lo que es mito",
              [Text(SUB_NBA, 27, MUTED),
               Tests([(True, "«Las palizas del arranque exageran»", "De cada 10 puntos de diferencia temprana se mantienen unos 3: el −17.8 de Sacramento vale como un −5.", "30 equipos · p = 0.03"),
                      (True, "«Un mal arranque dice algo, pero no todo»", "Los que arrancaron 1-3 o peor ganaron 42% del resto; los de buen arranque, 55%. La diferencia existe, pero no es enorme.", "11 y 9 equipos · indicio"),
                      (True, "«Jugar dos noches seguidas cuesta»", "Unos 2 puntos menos. Hoy le toca a Nueva Orleans.", "1,237 partidos · p = 0.011")])]),
        slide(7, T, "Conclusión", "Las palizas exageran, pero Sacramento sigue abajo",
              [Bullets(["Sacramento: grandes números individuales, pero recibe 126 puntos por partido.", "Las palizas del arranque exageran, pero Sacramento sigue siendo el peor de nuestro ranking.", f"Nueva Orleans gana {f['freq']} veces para nosotros."])],
              takeaway="¿Quién se quita el cero? Te leemos.", style="end", method=NBA_M),
    ]


def D():
    T = 6
    return [
        slide(1, T, "Futbol · Argentina · Domingo 1 de noviembre", "Boca vs. River: el clásico donde 1 de cada 3 partidos termina empatado",
              [Matchup("Boca Juniors", "local", "River Plate", "visita", sep="domingo 1 nov · 12:00 hora CDMX · La Bombonera"), Chips(["Torneo Clausura 2026"])],
              takeaway="¿Quién llega mejor y qué esperar? 4 datos.", style="cover"),
        slide(2, T, "La historia", "En más de 100 años, ninguno domina al otro",
              [Stacked("266 Superclásicos oficiales", (94 / 266, 84 / 266, 88 / 266), ("Boca 94", "Empate 84", "River 88"), (GHOST, ACC, MUTED)),
               Stats([("6", "victorias de diferencia en un siglo", GHOST), ("71%", "probabilidad de una diferencia así por pura casualidad", ACC)])],
              takeaway="Lo probamos: la ventaja de Boca cabe dentro del azar. Están parejos.", tag="DATO 1 DE 4"),
        slide(3, T, "Cómo llega Boca", "Boca casi no pierde",
              [Hero("1 de 14", "partidos perdió Boca en el Torneo Clausura.", ACC), Stats([("7", "ganados", ACC), ("6", "empatados", GHOST), ("1°", "tabla anual", ACC)])],
              takeaway="Difícil de vencer, aunque empata seguido.", tag="DATO 2 DE 4"),
        slide(4, T, "Cómo llega River", "River llega irregular, urgido… y con revancha",
              [Hero("5 de 14", "partidos perdió River en el Clausura (solo 2 empates).", NEG), Stats([("7°", "tabla anual", NEG), ("1-0", "perdió el último Superclásico (Apertura 2026)", AMBER)])],
              takeaway="Está 3 puntos debajo del último boleto a la Copa Libertadores. Necesita ganar.", tag="DATO 3 DE 4"),
        slide(5, T, "Lo que dice el mercado", "Boca es favorito; el empate, igual que siempre",
              [Stacked("Probabilidad para este domingo", (.422, .308, .270), ("Boca", "Empate", "River"), (GHOST, ACC, MUTED)),
               Text("Bajas: Boca sin Aranda, Belmonte, Bareiro ni Marchesín; River sin Fausto Vera.", 28, MUTED)],
              takeaway="Comparado con la historia, el mercado le suma a Boca por jugar en casa y llegar mejor. El empate no cambia: 1 de cada 3.", tag="DATO 4 DE 4"),
        slide(6, T, "Conclusión", "Boca es favorito, pero la mayoría de las veces no gana",
              [Bullets(["Boca gana 4 de cada 10 veces.", "Empate: 3 de cada 10, como siempre en este clásico.", "River: el menos probable, pero el que más lo necesita."])],
              takeaway="¿Se rompe la tendencia en La Bombonera?", style="end",
              method="Método: historial de 266 Superclásicos oficiales y prueba binomial de la ventaja de Boca (p = 0.71); forma en el Clausura 2026; mercado: precios convertidos a probabilidad sin el margen de la casa. Datos públicos al 28 oct. Análisis independiente, no afiliado a la LPF ni a los clubes. No es recomendación de apuesta."),
    ]


if __name__ == "__main__":
    which = sys.argv[1:] or ["A", "B", "C", "D", "E", "F"]
    fns = {"A": A, "B": B, "C": C, "D": D, "E": E, "F": F_}
    for k in which:
        o = f"{OUT}/{k}"
        os.makedirs(o, exist_ok=True)
        for i, im in enumerate(fns[k](), 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
