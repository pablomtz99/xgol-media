"""xGol — 30 oct: 5 previas (Liga MX ×3, NBA ×2) + 3 posts de datos que siempre conviene considerar. Diseño v7."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from matchup_1029 import Duel

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/1030")
MX = ("Método: modelo de goles (Poisson) con goles a favor y en contra del Apertura 2026, ajustados hacia el promedio de la liga "
      "por muestra corta, + ventaja de local. Puntos «esperados»: simulamos cada partido del equipo con su promedio de goles. "
      "Datos: ESPN, FutbolTotal (tablas al 30 oct). Análisis independiente, no afiliado a la Liga MX. No es recomendación de apuesta.")
NBA = ("Método: nivel de cada equipo ajustado por rival (parte de 90% del nivel 2025-26), localía y cansancio. Probado en 1,090 partidos: "
       "acertó 69%. Matchup: Basketball-Reference (4 a 6 partidos). Mercado de predicción público al 30 oct. Análisis independiente, "
       "no afiliado a la NBA. No es recomendación de apuesta.")
LAB = ("Método: pruebas sobre la temporada NBA 2025-26 (1,237 partidos) y temporadas regulares recientes de la NFL (nflverse), "
       "con corrección por pruebas múltiples. Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta.")


def three(h, d, a, lh, la):
    cols = (ACC, GHOST, MUTED) if h >= a else (MUTED, GHOST, ACC)
    return Stacked("Nuestro modelo", (h, d, a), (lh, "Empate", la), cols)


# ---------------------------------------------------------------- Liga MX
def QRO():
    T = 7
    return [
        slide(1, T, "Futbol · Liga MX · Jornada 15 · Viernes 30 de octubre", "Juárez vs. Querétaro: un equipo que rinde de visita contra el peor del torneo",
              [Matchup("Juárez", "18° · 5 pts", "Querétaro", "9° · 20 pts", sep="recibe a · hoy 19:00 hora CDMX · Estadio Olímpico Benito Juárez")],
              takeaway="Querétaro está en zona de play-in (7° a 10°) y no puede fallar. Pero llega con 3 derrotas seguidas. 5 datos.", style="cover", title_size=80),
        slide(2, T, "De visita", "Querétaro rinde más fuera que en casa",
              [Table(("En casa", "De visita"), [("Récord (G-E-P)", "2-1-3", "4-1-2"), ("Puntos por partido", "1.17", "1.86")], colors=[GHOST, ACC]),
               Stats([("13", "de sus 20 puntos los ganó de visita", ACC), ("7", "en casa, en casi los mismos partidos", GHOST)])],
              takeaway="Lo probamos: con 13 partidos, esa diferencia entre casa y visita puede ser casualidad (p = 0.30). Es un indicio, no una regla.", tag="DATO 1 DE 5"),
        slide(3, T, "El rival", "Juárez: 1 victoria en 14 partidos",
              [Hero("−24", "de diferencia de goles: 9 a favor y 33 en contra. El peor de la liga, ya eliminado.", NEG),
               Stats([("1-1-5", "en casa", NEG), ("0.71", "goles por partido en casa", NEG)])],
              takeaway="Juárez ganó un solo partido en todo el torneo y ya no tiene nada en juego. Querétaro sí: está empatado en puntos con el 8° lugar.", tag="DATO 2 DE 5"),
        slide(4, T, "La racha", "3 derrotas seguidas: ¿crisis o mala racha?",
              [Hero("17.1", "puntos «merecía» Querétaro por sus goles (17 a favor, 18 en contra). Tiene 20.", AMBER),
               Stats([("+2.9", "puntos de más", AMBER), ("p = 0.31", "puede ser casualidad", GHOST)])],
              takeaway="Sus goles dicen que Querétaro es de media tabla, y ahí está. No es una crisis: incluso tiene un poco más de lo que sus goles explican.", tag="DATO 3 DE 5"),
        slide(5, T, "La altura", "¿Pesa la altura? Hoy no",
              [Hero("680 m", "más arriba vive Querétaro que Juárez. Bajar no cansa: el efecto de la altura es al subir.", ACC),
               Stats([("1,140 m", "Ciudad Juárez", GHOST), ("1,820 m", "Querétaro", ACC)])],
              takeaway="La altura no juega en contra de Querétaro. Y el calor de Juárez tampoco: el partido es de noche y a fin de octubre.", tag="DATO 4 DE 5"),
        slide(6, T, "La predicción", "Querétaro es favorito, pero no tanto como parece",
              [three(.29, .25, .46, "Juárez", "Querétaro"),
               Stats([("2.7", "goles esperados entre los dos", ACC), ("52%", "probabilidad de 3 goles o más", GHOST)])],
              takeaway="El modelo frena los extremos porque 14 partidos son pocos: aun el peor equipo le gana a uno de media tabla 3 de cada 10 veces.", tag="DATO 5 DE 5"),
        slide(7, T, "Conclusión", "Querétaro tiene que ganar, y es favorito",
              [Bullets(["Rinde más de visita (indicio, no regla).", "Juárez: el peor del torneo y sin nada en juego.", "Querétaro gana 46%; empate 25%; Juárez 29%."])],
              takeaway="¿Los Gallos rompen la racha en Juárez? Te leemos.", style="end", method=MX),
    ]


def ATL():
    T = 7
    return [
        slide(1, T, "Futbol · Liga MX · Jornada 15 · Viernes 30 de octubre", "San Luis vs. Atlas: el 4° lugar con más goles en contra que a favor",
              [Matchup("San Luis", "11° · 19 pts", "Atlas", "4° · 24 pts", sep="recibe a · hoy 19:00 hora CDMX · Estadio Alfonso Lastras")],
              takeaway="Atlas está en zona de Liguilla directa (top 6). Pero sus goles cuentan otra historia. 5 datos.", style="cover", title_size=80),
        slide(2, T, "La paradoja", "Atlas es 4° con más goles en contra que a favor",
              [Hero("25-26", "goles a favor y en contra de Atlas en 14 partidos: diferencia de −1.", AMBER),
               Stats([("24", "puntos reales", ACC), ("18.9", "puntos que «merecía» por sus goles", GHOST)])],
              takeaway="Con esos goles, lo normal sería tener unos 19 puntos. Atlas tiene 24: cinco más de lo que sus goles explican.", tag="DATO 1 DE 5"),
        slide(3, T, "Lo probamos", "¿Suerte? No se puede afirmar",
              [Hero("18%", "de las veces un equipo con esos goles sumaría 24 puntos o más por pura casualidad.", GHOST),
               Stats([("p = 0.18", "no es concluyente", GHOST), ("+5", "puntos de más", AMBER)])],
              takeaway="No podemos decir que sea pura suerte, pero sí que su posición exagera su nivel real: más de media tabla que de top 4.", tag="DATO 2 DE 5"),
        slide(4, T, "El patrón raro", "Atlas juega mejor de visita que en casa",
              [Table(("En casa", "De visita"), [("Récord (G-E-P)", "2-3-3", "5-0-1"), ("Goles a favor-en contra", "12-17", "13-9")], colors=[NEG, ACC])],
              takeaway="Hoy juega de visita, donde es fuerte. ¿Es real? Lo probamos: p = 0.055, justo en el límite. Un indicio fuerte, no una certeza.", tag="DATO 3 DE 5"),
        slide(5, T, "El matchup", "Dos defensas que dejan llegar",
              [Table(("San Luis", "Atlas"), [("Goles a favor por partido", "1.36", "1.79"), ("Goles en contra por partido", "1.57", "1.86")], colors=[GHOST, ACC]),
               Stats([("1,860 m", "altura de San Luis (Guadalajara: 1,560 m)", GHOST), ("3-2-2", "San Luis en casa", GHOST)])],
              takeaway="Atlas anota más que San Luis, pero también recibe más. La altura apenas cambia: 300 metros de diferencia.", tag="DATO 4 DE 5"),
        slide(6, T, "La predicción", "Partido de goles; San Luis, ligero favorito",
              [three(.47, .23, .31, "San Luis", "Atlas"),
               Stats([("3.3", "goles esperados entre los dos", ACC), ("64%", "probabilidad de 3 goles o más", ACC)])],
              takeaway="Nuestro modelo no ve a Atlas como un 4° lugar, sino como un equipo de media tabla que defiende mal. Si su patrón de visita es real, el partido está más parejo.", tag="DATO 5 DE 5"),
        slide(7, T, "Conclusión", "Atlas está arriba, pero sus goles no lo respaldan",
              [Bullets(["4° lugar con más goles en contra que a favor.", "Fuerte de visita, frágil en casa (indicio).", "Se esperan goles: 2 de cada 3 veces habrá 3 o más."])],
              takeaway="¿Atlas sostiene su lugar o lo alcanzan los números? Te leemos.", style="end", method=MX),
    ]


def PUE():
    T = 6
    return [
        slide(1, T, "Futbol · Liga MX · Jornada 15 · Viernes 30 de octubre", "Puebla vs. Pumas: el que pierde casi se despide del play-in",
              [Matchup("Puebla", "14° · 16 pts", "Pumas", "12° · 17 pts", sep="recibe a · hoy 21:00 hora CDMX · Estadio Cuauhtémoc")],
              takeaway="El 10° lugar (último del play-in) tiene 19 puntos. Quedan 3 jornadas. 4 datos.", style="cover", title_size=80),
        slide(2, T, "Las cuentas", "A los dos les faltan 2 o 3 puntos, y quedan 9 en juego",
              [HBars([("10° Santos", 19, GHOST), ("12° Pumas", 17, ACC), ("14° Puebla", 16, AMBER)], 22, "{} pts", 330)],
              takeaway="Del 9° al 14° hay solo 4 puntos de diferencia. Un empate no le sirve casi a ninguno de los dos.", tag="DATO 1 DE 4"),
        slide(3, T, "Cómo llegan", "Puebla no gana desde hace 5 partidos",
              [Stats([("0 de 5", "victorias de Puebla en sus últimos 5 (3 derrotas, 2 empates)", NEG), ("4-5-5", "récord de Pumas en el torneo: empata más de lo que gana", AMBER)]),
               Table(("Puebla", "Pumas"), [("En casa / de visita", "1-3-2", "3-1-3")], colors=[GHOST, ACC])],
              takeaway="Pumas gana más fuera (3) que en casa (1). Puebla casi no gana en su estadio.", tag="DATO 2 DE 4"),
        slide(4, T, "La altura y los números", "Ni la altura ni la tabla separan a estos dos",
              [Stats([("2,135 m", "Puebla", GHOST), ("2,240 m", "Ciudad de México", GHOST)]),
               Stats([("15.7", "puntos «merecidos» de Puebla (tiene 16)", GHOST), ("17.4", "puntos «merecidos» de Pumas (tiene 17)", GHOST)])],
              takeaway="Los dos están justo donde sus goles dicen. Y ninguno sufre la altura: Pumas vive incluso más arriba.", tag="DATO 3 DE 4"),
        slide(5, T, "La predicción", "Casi parejo, con ventaja de casa para Puebla",
              [three(.45, .25, .31, "Puebla", "Pumas"),
               Stats([("2.9", "goles esperados", ACC), ("57%", "probabilidad de que anoten los dos", GHOST)])],
              takeaway="La ventaja de Puebla es casi solo la localía. Si Pumas repite lo que hace de visita, el partido se empareja.", tag="DATO 4 DE 4"),
        slide(6, T, "Conclusión", "Partido de eliminación adelantada",
              [Bullets(["El que pierde queda a 2 o más puntos del play-in, con 2 jornadas por jugar.", "Puebla lleva 5 partidos sin ganar.", "Puebla 45%, empate 25%, Pumas 31%."])],
              takeaway="¿Quién sigue vivo el sábado? Te leemos.", style="end", method=MX),
    ]


# ---------------------------------------------------------------- NBA
def NYK(N):
    c = N["NYK@PHI"]; T = 6
    return [
        slide(1, T, "Basquetbol · NBA · Viernes 30 de octubre", "Knicks vs. 76ers: 2-3 contra 4-1… y vemos a Nueva York",
              [Matchup("Knicks", c["rec_a"], "76ers", c["rec_h"], sep="visitan a · hoy 17:30 hora CDMX")],
              takeaway="El récord dice Filadelfia. Ajustado por rivales, Nueva York es 7° de la liga y Filadelfia 15°. 4 datos.", style="cover"),
        slide(2, T, "El récord engaña", "Ajustado por rivales, los Knicks son mejores",
              [Rank([("Knicks", c["rank_a"], ACC), ("76ers", c["rank_h"], GHOST)])],
              takeaway="El modelo parte del nivel del año pasado y lo corrige con cada partido, según la calidad del rival. Cinco partidos todavía pesan poco.", tag="DATO 1 DE 4"),
        slide(3, T, "El matchup", "Filadelfia cuida el balón; Nueva York domina el rebote",
              [Duel("NYK", "PHI", [
                  ("Pérdidas de balón", "15.4%", "12.4%", "más bajo = mejor", False),
                  ("Triples por tiro", ".424", ".384", "Nueva York tira más de 3", None),
                  ("Rebote ofensivo", "30.5%", "18.9%", "segundas oportunidades", True),
                  ("Rebote defensivo", "77.4%", "70.6%", "rebotes propios", True),
                  ("Tiro efectivo atacando", "49.8%", "49.0%", "liga: 53.1%", None)])],
              takeaway="Los dos tiran mal. Filadelfia además obliga a perder el balón en 17% de las jugadas rivales. Clave: que Nueva York lo cuide y aproveche su rebote.", tag="DATO 2 DE 4"),
        slide(4, T, "¿Cómo será?", "Partido lento y de pocos puntos",
              [Stats([(f"{c['total']:.0f}", f"puntos proyectados (liga: {N['league_total']:.0f})", ACC), ("49–50%", "tiro efectivo de los dos, de los peores", NEG)])],
              takeaway="Dos equipos que fallan mucho, y Filadelfia permite poco (48.5% de tiro efectivo rival). Esperamos menos puntos de lo normal.", tag="DATO 3 DE 4"),
        slide(5, T, "La predicción", "Nuestro modelo ve a Nueva York; el mercado, un volado",
              [MvM("Knicks ganan", (100 - c["p_home"]) / 100, .53)],
              takeaway="Nosotros le damos más peso a lo que los Knicks hicieron el año pasado y a la calidad de sus rivales; el mercado, a su 2-3.", tag="DATO 4 DE 4"),
        slide(6, T, "Conclusión", "El 2-3 de los Knicks no es una crisis",
              [Bullets(["Ajustado por rivales, son 7° de la liga.", "Clave: cuidar el balón y ganar el rebote.", f"Nueva York gana {100 - c['p_home']}% para nosotros, en un partido de pocos puntos."])],
              takeaway="¿Crisis en Nueva York o falsa alarma? Te leemos.", style="end", method=NBA),
    ]


def HOU(N):
    c = N["HOU@DAL"]; T = 6
    return [
        slide(1, T, "Basquetbol · NBA · Viernes 30 de octubre", "Rockets vs. Mavericks: uno de los dos invictos pone a prueba su 5-0",
              [Matchup("Rockets", c["rec_a"], "Mavericks", c["rec_h"], sep="visitan a · hoy 18:00 hora CDMX")],
              takeaway="Houston gana por 14 puntos por partido. Dallas viene de ganarle por 24 a Oklahoma City. 4 datos.", style="cover"),
        slide(2, T, "Houston", "Houston tira muy por encima del promedio",
              [Hero("59.4%", "de tiro efectivo de Houston: muy arriba del 53.1% de la liga.", ACC),
               Stats([("31%", "rebote ofensivo", ACC), (".326", "tiros libres por tiro", ACC)])],
              takeaway="Tira bien, rebota sus fallas y provoca faltas. Lo de los arranques: de cada 10 puntos de ventaja temprana se mantienen unos 3.", tag="DATO 1 DE 4"),
        slide(3, T, "El matchup", "Houston provoca faltas; Dallas casi no va a la línea",
              [Duel("HOU", "DAL", [
                  ("Tiro efectivo atacando", "59.4%", "56.5%", "liga: 53.1%", True),
                  ("Tiros libres por tiro", ".326", ".193", "Dallas, de los que menos", True),
                  ("Rebote ofensivo", "31.0%", "27.5%", "segundas oportunidades", True),
                  ("Pérdidas de balón", "16.6%", "16.5%", "los dos la pierden mucho", None)])],
              takeaway="Dallas también tira bien, pero casi no saca faltas. Houston suma puntos «gratis» desde la línea y con rebotes ofensivos.", tag="DATO 2 DE 4"),
        slide(4, T, "Ajustado por rivales", "Houston es 4° de la liga; Dallas, 22°",
              [Rank([("Houston", c["rank_a"], ACC), ("Dallas", c["rank_h"], NEG)])],
              takeaway="Ajustado por la calidad de los rivales, el 3-2 de Dallas vale menos que el 5-0 de Houston. Una gran victoria no cambia eso.", tag="DATO 3 DE 4"),
        slide(5, T, "La predicción", "Los dos vemos a Houston; nosotros, con más confianza",
              [MvM("Rockets ganan", (100 - c["p_home"]) / 100, .62)],
              takeaway=f"Diferencia esperada: Houston por {abs(c['margin']):.0f}. Unos {c['total']:.0f} puntos entre los dos.", tag="DATO 4 DE 4"),
        slide(6, T, "Conclusión", "El 5-0 de Houston tiene base, pero no es de 14 puntos",
              [Bullets(["Tira, rebota y provoca faltas mejor que Dallas.", "Los arranques exageran: esperamos que gane por 9, no por 14.", f"Houston gana {100 - c['p_home']}% para nosotros."])],
              takeaway="¿Houston llega 6-0? Te leemos.", style="end", method=NBA),
    ]


# ---------------------------------------------------------------- Siempre considerar
def REST():
    T = 5
    return [
        slide(1, T, "Datos que siempre hay que considerar · NBA", "Cansancio sí, descanso no",
              [Hero("−2.1", "puntos rinde un equipo que jugó la noche anterior.", NEG)],
              takeaway="Lo probamos con 1,237 partidos. Pero tener un día extra de descanso no da ninguna ventaja. 3 datos.", style="cover"),
        slide(2, T, "Lo que sí pesa", "Jugar dos noches seguidas cuesta 2 puntos",
              [Stats([("−2.1", "puntos al margen final", NEG), ("p = 0.011", "casi seguro no es casualidad", ACC)]),
               Stats([("1,237", "partidos de la temporada 2025-26", GHOST)])],
              takeaway="Dos puntos parecen poco, pero mueven un partido parejo de 50% a ~45%.", tag="DATO 1 DE 3"),
        slide(3, T, "Lo que no pesa", "Un día extra de descanso no cambia nada",
              [Hero("0", "ventaja medible por llegar con 2 o 3 días de descanso en vez de 1.", GHOST)],
              takeaway="El efecto es prácticamente cero (p = 0.74). Lo que importa es no jugar la noche anterior, no descansar de más.", tag="DATO 2 DE 3"),
        slide(4, T, "Lo que la gente cree", "Si los dos están cansados, ¿hay menos puntos?",
              [Stats([("−2.4", "puntos totales cuando los dos jugaron anoche", AMBER), ("p = 0.36", "puede ser casualidad", GHOST)])],
              takeaway="Solo 70 partidos así: hay un indicio, pero no alcanza para afirmarlo. Por eso no lo usamos para proyectar puntos.", tag="DATO 3 DE 3"),
        slide(5, T, "Lo que probamos", "Lo que se sostiene y lo que es mito",
              [Tests([(True, "«Jugar dos noches seguidas cuesta»", "−2.1 puntos al margen.", "1,237 partidos · p = 0.011"),
                      (False, "«Más días de descanso dan ventaja»", "Un día extra no cambia nada.", "p = 0.74"),
                      (False, "«Si los dos están cansados hay menos puntos»", "Indicio, no comprobado.", "70 partidos · p = 0.36")])],
              takeaway="Antes de ver un partido de NBA, revisa quién jugó anoche. ¿Lo tomabas en cuenta?", style="end", method=LAB),
    ]


def START():
    T = 4
    return [
        slide(1, T, "Datos que siempre hay que considerar · NBA", "Los arranques engañan",
              [Hero("3 de 10", "puntos de ventaja de los primeros partidos se mantienen el resto de la temporada.", AMBER)],
              takeaway="¿Tu equipo arrancó invicto? ¿O 0-4? Antes de emocionarte (o de asustarte), 2 datos.", style="cover"),
        slide(2, T, "Lo que medimos", "Los primeros partidos dicen algo, pero poco",
              [Stats([("0.40", "relación entre los 4 primeros partidos y el resto de la temporada", AMBER), ("p = 0.03", "la relación es real, pero débil", ACC)])],
              takeaway="Si un equipo gana por 10 en sus primeros juegos, lo esperable es que el resto del año gane por unos 3. No por 10.", tag="DATO 1 DE 2"),
        slide(3, T, "La corrección", "Ver contra quién ganaste predice mejor",
              [HBars([("Sin ajustar", 0.42, GHOST), ("Ajustado por rivales", 0.51, ACC)], 0.6, "{}", 360)],
              takeaway="Relación con el resto de la temporada (30 equipos). Ganarle a los peores infla el récord; corregir por la calidad del rival mejora la predicción (p = 0.004).", tag="DATO 2 DE 2"),
        slide(4, T, "Conclusión", "Regla para octubre: divide la emoción entre tres",
              [Bullets(["Una ventaja temprana se mantiene solo en ~30%.", "Fíjate contra quién ganó.", "Un 0-4 no condena; un 4-0 no consagra."])],
              takeaway="¿Qué arranque de este año crees que es real? Te leemos.", style="end", method=LAB),
    ]


def STREAK():
    T = 5
    return [
        slide(1, T, "Datos que siempre hay que considerar · NFL", "Las rachas de puntos no predicen nada",
              [Hero("50%", "de las veces, tras 4 partidos con pocos puntos, el siguiente también tuvo pocos. Un volado.", GHOST)],
              takeaway="Lo probamos con temporadas recientes de la NFL. Y otros dos mitos de los que todo mundo habla. 3 datos.", style="cover"),
        slide(2, T, "Las rachas", "Después de 4 partidos con pocos puntos, viene… un volado",
              [Stats([("392", "casos en temporadas recientes de la NFL", GHOST), ("50%", "el siguiente también tuvo pocos puntos", GHOST)]),
               Stats([("−0.02", "relación entre lo que un equipo venía anotando y su siguiente partido, comparado con lo esperado (6,814 casos)", GHOST)])],
              takeaway="El mercado ya ajusta sus expectativas a las rachas. Por eso, una vez ajustadas, no queda nada que predecir.", tag="DATO 1 DE 3"),
        slide(3, T, "Los jueves", "¿Los partidos de jueves tienen menos puntos?",
              [Stats([("268", "partidos en jueves", GHOST), ("p = 0.60", "igual a lo esperado", GHOST)])],
              takeaway="Se dice que con menos días de preparación se anota menos. Los números no lo muestran.", tag="DATO 2 DE 3"),
        slide(4, T, "El frío", "¿Con frío se anota menos?",
              [Stats([("670", "partidos a 7 °C o menos", GHOST), ("p = 0.62", "igual a lo esperado", GHOST)])],
              takeaway="Comparado con lo que el mercado esperaba para cada partido, el frío no cambia nada: ya está descontado.", tag="DATO 3 DE 3"),
        slide(5, T, "Lo que probamos", "Tres mitos de la NFL",
              [Tests([(False, "«Las rachas de pocos puntos siguen»", "Es un volado.", "392 casos · p = 0.42"),
                      (False, "«Los jueves se anota menos»", "Igual a lo esperado.", "268 partidos · p = 0.60"),
                      (False, "«Con frío se anota menos»", "El mercado ya lo descuenta.", "670 partidos · p = 0.62")])],
              takeaway="¿Cuál de estos creías? Te leemos.", style="end", method=LAB),
    ]


if __name__ == "__main__":
    N = json.load(open(os.environ["NBA_JSON"]))
    sets = {"QRO": QRO(), "ATL": ATL(), "PUE": PUE(), "NYK": NYK(N), "HOU": HOU(N), "REST": REST(), "START": START(), "STREAK": STREAK()}
    for k, ims in sets.items():
        o = f"{OUT}/{k}"; os.makedirs(o, exist_ok=True)
        for i, im in enumerate(ims, 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
