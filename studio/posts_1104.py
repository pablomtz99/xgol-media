"""xGol — 4 nov: Champions J4 (miércoles) con modelo xGol UCL v0.1 (63 partidos) + NBA (modelo v1, 107 partidos al 2 nov)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from matchup_1029 import Duel
from posts_1030 import three

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/1104")
UCL = ("Método: modelo de goles (Poisson) por equipo con los 63 partidos de la fase liga 2026-27, el coeficiente UEFA como punto de partida "
       "y el promedio de goles de la temporada pasada para no exagerar. Puntos «merecidos»: lo que el modelo esperaba en sus partidos. "
       "Datos: UEFA.com. Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta.")
NBA = ("Método: nivel de cada equipo ajustado por rival (parte de 90% del nivel 2025-26), con localía. 107 partidos al 2 nov; "
       "fuera de muestra acertó 67% (91 partidos). Rangos 10–90% por remuestreo. Datos: BALLDONTLIE. "
       "Análisis independiente, no afiliado a la NBA. No es recomendación de apuesta.")
KU = "Futbol · Champions League · Jornada 4 · Miércoles 4 de noviembre"
KN = "Basquetbol · NBA · Miércoles 4 de noviembre"


def cov(T, k, title, a, ra, b, rb, sep, take, size=76):
    return slide(1, T, k, title, [Matchup(a, ra, b, rb, sep=sep)], takeaway=take, style="cover", title_size=size)


def tag(n, T): return f"DATO {n-1} DE {T-2}"


def predu(T, n, title, p, la, lb, xg, o25, take):
    return slide(n, T, "La predicción", title, [three(*p, la, lb),
                 Stats([(f"{xg:.1f}", "goles esperados entre los dos", ACC), (f"{o25:.0%}", "probabilidad de 3 goles o más", GHOST)])],
                 takeaway=take, tag=tag(n, T))


def endu(T, title, bullets, q, m=UCL):
    return slide(T, T, "Conclusión", title, [Bullets(bullets)], takeaway=q, style="end", method=m)


def g3(a, b, gfa, gaa, gfb, gab, ra, rb):
    return [("Goles a favor por partido", f"{gfa/3:.2f}", f"{gfb/3:.2f}", "en esta Champions", gfa > gfb if gfa != gfb else None),
            ("Goles en contra por partido", f"{gaa/3:.2f}", f"{gab/3:.2f}", "más bajo = mejor", gaa < gab if gaa != gab else None),
            ("Lugar en ataque (de 36)", f"{ra[0]}°", f"{rb[0]}°", "ajustado por rival", ra[0] < rb[0]),
            ("Lugar en defensa (de 36)", f"{ra[1]}°", f"{rb[1]}°", "ajustado por rival", ra[1] < rb[1])]


# ------------------------------------------------------------------ Champions
def FEN():
    T = 6
    return [
        cov(T, KU, "Liverpool: 46 partidos europeos seguidos sin un solo empate", "Fenerbahçe", "2 pts", "Liverpool", "9 pts",
            "recibe a · hoy 11:45 hora CDMX · Estambul", "Liverpool ganó sus 3 partidos, pero recibió 7 goles. Fenerbahçe lleva 10 partidos de Champions sin ganar. 4 datos."),
        slide(2, T, "La racha rara", "32 victorias, 0 empates, 14 derrotas",
              [Hero("1 en 6,449", "probabilidad de 46 partidos sin empatar si empatara como un equipo típico de Champions (17%).", AMBER),
               Stats([("p = 0.0002", "prueba binomial", GHOST), ("7%", "chance de que alguno de 36 clubes tenga una racha así", GHOST)])],
              takeaway="Rarísimo para un equipo… pero buscando entre 36 clubes, a alguno le podía tocar. Es una curiosidad, no un «estilo».", tag=tag(2, T)),
        slide(3, T, "El matchup", "Liverpool anota mucho, pero también recibe",
              [Duel("Fenerbahçe", "Liverpool", g3("F", "L", 3, 9, 12, 7, (27, 27), (2, 16)))],
              takeaway="Liverpool tiene el 2° mejor ataque, pero su defensa es 16°: ganó 6-3 y 4-3. Fenerbahçe recibió 6 de Aston Villa.", tag=tag(3, T)),
        slide(4, T, "Lo probamos", "¿Liverpool está inflado?",
              [Tests([(None, "«Liverpool tiene más de lo que merece»", "Esperábamos 6.4 puntos; tiene 9.", "p = 0.28 · indicio débil"),
                      (None, "«Fenerbahçe merecía más»", "Esperábamos 3.6; tiene 2.", "p = 0.26 · indicio débil")])],
              takeaway="Con 3 partidos nada es concluyente. Lo que sí: los dos dejan llegar, así que se esperan goles.", tag=tag(4, T)),
        predu(T, 5, "Liverpool, favorito aun en Estambul", (.262, .185, .553), "Fenerbahçe", "Liverpool", 4.4, .81,
              "El empate tiene 18% en nuestro modelo, no 0%. La racha no entra en el cálculo: el modelo no cree en rachas de empates."),
        endu(T, "Si Liverpool no gana, probablemente pierde", ["46 partidos europeos sin empatar: curiosidad, no patrón.", "2° mejor ataque, defensa 16°.", "Fenerbahçe 26%, empate 18%, Liverpool 55%."],
             "¿Hoy se rompe la racha sin empates? Te leemos."),
    ]


def AEK():
    T = 6
    return [
        cov(T, KU, "Real Madrid, 9 de 9, visita a uno de los ataques más flojos de la Champions", "AEK", "3 pts", "Real Madrid", "9 pts",
            "recibe al · hoy 11:45 hora CDMX · Atenas", "Madrid le ganó a Inter, Roma y Leipzig. AEK es 32° de 36 en ataque. 4 datos."),
        slide(2, T, "El Madrid", "9 de 9, pero ganando cerrado",
              [Stats([("2-1", "a Inter", ACC), ("4-3", "en Roma", ACC)]),
               Stats([("5.8", "puntos «merecidos» por sus partidos (tiene 9)", AMBER), ("18%", "de las veces sumaría 9 con ese nivel", GHOST)])],
              takeaway="Dos de sus tres victorias fueron por un gol. Es muy bueno, y además le salió todo.", tag=tag(2, T)),
        slide(3, T, "El matchup", "Uno de los peores ataques contra uno de los mejores",
              [Duel("AEK", "Madrid", g3("A", "M", 3, 8, 10, 5, (32, 31), (4, 7)))],
              takeaway="AEK es 32° en ataque y 31° en defensa. Recibió 5 de Manchester City. Madrid anota 3.3 por partido.", tag=tag(3, T)),
        slide(4, T, "Lo probamos", "¿Alguien está fuera de lugar?",
              [Tests([(None, "«Madrid tiene más de lo que merece»", "Esperábamos 5.8; tiene 9.", "p = 0.18 · indicio, no prueba"),
                      (False, "«AEK está regalado»", "Esperábamos 2.5; tiene 3.", "justo donde debe")])],
              takeaway="AEK está donde sus goles dicen: es de los más débiles del torneo. Madrid gana mucho, pero no tanto como su 9 de 9.", tag=tag(4, T)),
        predu(T, 5, "Madrid gana 7 de cada 10", (.152, .161, .687), "AEK", "Real Madrid", 4.0, .77,
              "AEK necesita su estadio: aun así, solo gana 15% de las veces. Rango del modelo para Madrid: 56% a 81%."),
        endu(T, "Madrid, claro favorito en Atenas", ["Madrid: 9 de 9, con algo de fortuna.", "AEK: 32° en ataque, 31° en defensa.", "AEK 15%, empate 16%, Madrid 69%."],
             "¿Madrid llega a 12 de 12? Te leemos."),
    ]


def LEI():
    T = 6
    return [
        cov(T, KU, "Leipzig vs. City: Haaland le metió 12 goles en 8 partidos. ¿Su víctima favorita?", "Leipzig", "3 pts", "Man. City", "6 pts",
            "recibe al · hoy 14:00 hora CDMX", "Leipzig perdió 5 seguidos contra ingleses en Europa. ¿Kryptonita o casualidad? 4 datos."),
        slide(2, T, "Lo probamos", "¿Haaland tiene algo especial contra Leipzig?",
              [Hero("1 en 8", "probabilidad de que Haaland le meta 12 o más en 8 partidos a cualquier rival, solo por su promedio.", AMBER),
               Stats([("8.1", "goles esperados con su promedio en Champions (61 en 60)", GHOST), ("12", "goles reales", ACC)])],
              takeaway="Es mucho, pero pasa 1 de cada 8 veces. No es que Leipzig sea su «kryptonita»: Haaland anota uno por partido contra casi todos.", tag=tag(2, T)),
        slide(3, T, "El matchup", "City ataca mejor; Leipzig recibe mucho",
              [Duel("Leipzig", "City", g3("L", "C", 3, 8, 9, 5, (22, 24), (6, 9)))],
              takeaway="Leipzig recibió 4 de Como y 4 de Real Madrid, de visita. En casa le ganó 1-0 a PSV.", tag=tag(3, T)),
        slide(4, T, "Los números", "Los dos están donde deben",
              [Table(("Esperados", "Reales"), [("Leipzig", "3.1", "3"), ("Manchester City", "5.5", "6")], colors=[GHOST, ACC])],
              takeaway="Aquí no hay suerte que corregir: City es mejor, y la localía de Leipzig empareja un poco.", tag=tag(4, T)),
        predu(T, 5, "City, favorito, pero Leipzig gana 3 de cada 10", (.302, .205, .493), "Leipzig", "Man. City", 3.9, .74,
              "Rango del modelo para City: 39% a 57%. De visita, en Alemania, no es un trámite."),
        endu(T, "City es mejor; la «kryptonita» es un mito", ["12 goles en 8: pasa 1 de cada 8 veces.", "City 6° en ataque; Leipzig 24° en defensa.", "Leipzig 30%, empate 21%, City 49%."],
             "¿Haaland llega a 13? Te leemos."),
    ]


def BVB():
    T = 6
    return [
        cov(T, KU, "Dortmund vs. Betis: 9 de 9 ganando siempre por un gol", "Dortmund", "6 pts", "Betis", "9 pts",
            "recibe al · hoy 14:00 hora CDMX", "3-2, 3-2 y 1-0. Ganar siempre por la mínima rara vez dura. 4 datos."),
        slide(2, T, "Betis", "Tres victorias, tres por un gol",
              [Stats([("3-2", "en Lille", ACC), ("3-2", "a Porto", ACC)]),
               Stats([("5.3", "puntos «merecidos» por sus partidos", AMBER), ("14%", "de las veces sumaría 9 con ese nivel", GHOST)])],
              takeaway="7 goles a favor y 4 en contra: diferencia de +3 en 3 partidos. Con eso, lo normal era unos 5 puntos, no 9.", tag=tag(2, T)),
        slide(3, T, "El matchup", "Dos equipos casi idénticos",
              [Duel("Dortmund", "Betis", g3("D", "B", 5, 4, 7, 4, (13, 13), (12, 14)))],
              takeaway="Mismo nivel en ataque y defensa. La diferencia es el estadio: Dortmund ganó sus 4 partidos en casa contra españoles en Europa.", tag=tag(3, T)),
        slide(4, T, "Lo probamos", "¿Betis es candidato o viene la regresión?",
              [Tests([(None, "«Betis tiene más de lo que merece»", "Esperábamos 5.3; tiene 9.", "p = 0.14 · indicio"),
                      (False, "«Dortmund está mal»", "Esperábamos 5.7; tiene 6.", "justo donde debe")])],
              takeaway="Es el indicio más fuerte del día, pero con 3 partidos sigue sin ser prueba. Betis juega bien; ganar siempre por uno es lo difícil de repetir.", tag=tag(4, T)),
        predu(T, 5, "Dortmund, favorito en casa", (.519, .209, .273), "Dortmund", "Betis", 3.6, .70,
              "Rango del modelo para Dortmund: 47% a 57%. Betis gana 27%: no es poco para un equipo que va perfecto."),
        endu(T, "Betis va perfecto, pero sus números no tanto", ["3 victorias por un gol.", "Merecía ~5 puntos, no 9 (indicio).", "Dortmund 52%, empate 21%, Betis 27%."],
             "¿Betis sigue perfecto en Dortmund? Te leemos."),
    ]


def LEN():
    T = 6
    return [
        cov(T, KU, "Lens vs. Como: el debutante con 10 goles en 3 partidos", "Lens", "3 pts", "Como", "6 pts",
            "recibe al · hoy 14:00 hora CDMX", "Como le metió 4 a Leipzig y 4 a Manchester United. Lens lleva 16 partidos de Champions recibiendo gol. 4 datos."),
        slide(2, T, "Como", "10 goles en 3 partidos… con un ataque de nivel bajo",
              [Stats([("4-1", "a Leipzig", ACC), ("4-1", "a Manchester United", ACC)]),
               Stats([("26°", "en ataque ajustado por rival: el modelo aún no le cree", AMBER), ("6", "puntos (esperábamos 3.8)", GHOST)])],
              takeaway="El modelo parte de su coeficiente, que es de los más bajos porque es debutante. Con 3 partidos, todavía pesa más el historial que los goles.", tag=tag(2, T)),
        slide(3, T, "El matchup", "Lens, de los más débiles; Como anota y recibe",
              [Duel("Lens", "Como", g3("L", "C", 3, 7, 10, 5, (34, 33), (26, 29)))],
              takeaway="Lens es 34° en ataque y 33° en defensa: de los más débiles. Como anota mucho pero también recibe.", tag=tag(3, T)),
        slide(4, T, "Lo probamos", "¿Como es real?",
              [Tests([(None, "«Como tiene más de lo que merece»", "Esperábamos 3.8 puntos; tiene 6.", "p = 0.29 · indicio débil"),
                      (None, "«Sus 10 goles son suerte»", "Con su nivel previo, 10 en 3 pasa 1 vez en 190.", "p = 0.005, pero entre 36 clubes: 17%")])],
              takeaway="Que un debutante meta tanto es raro. Que a alguno de los 36 le pase, no tanto. Puede ser un equipo mejor de lo que dice su historial.", tag=tag(4, T)),
        predu(T, 5, "El partido más parejo del miércoles", (.37, .228, .402), "Lens", "Como", 3.4, .65,
              "Si Como es tan bueno como sus goles, es favorito claro. Si no, es un volado. El modelo está en medio."),
        endu(T, "Un volado con un debutante que no deja de anotar", ["Como: 10 goles en 3, raro pero posible.", "Lens: de los más débiles del torneo.", "Lens 37%, empate 23%, Como 40%."],
             "¿Como sigue sorprendiendo? Te leemos."),
    ]


def SLA():
    T = 6
    return [
        cov(T, KU, "Slavia vs. Arsenal: la mejor defensa de la Champions, sin Saka", "Slavia", "1 pt", "Arsenal", "7 pts",
            "recibe al · hoy 14:00 hora CDMX · Praga", "Arsenal recibió solo 2 goles en 3 partidos, los dos en Múnich. 4 datos."),
        slide(2, T, "Arsenal", "La defensa n.° 1 del torneo",
              [Stats([("2", "goles en contra en 3 partidos", ACC), ("1°", "defensa ajustada por rival", ACC)]),
               Stats([("1-0", "en Nápoles", GHOST), ("2-2", "en Múnich", GHOST)])],
              takeaway="Ganó en Nápoles y empató en el estadio de Bayern. Su fuerza es no recibir, no golear.", tag=tag(2, T)),
        slide(3, T, "El matchup", "El 30° ataque contra la mejor defensa",
              [Duel("Slavia", "Arsenal", g3("S", "A", 4, 7, 6, 2, (30, 30), (8, 1)))],
              takeaway="Slavia es 30° en ataque y en defensa. Su único punto fue un 2-2 en Estambul. Sin Saka, Arsenal pierde a su mejor generador.", tag=tag(3, T)),
        slide(4, T, "Lo probamos", "¿Slavia es tan malo como su 1 punto?",
              [Tests([(None, "«Slavia merecía más»", "Esperábamos 4.8 puntos; tiene 1.", "p = 0.09 · indicio"),
                      (None, "«Arsenal tiene de más»", "Esperábamos 4.9; tiene 7.", "p = 0.21 · indicio débil")])],
              takeaway="A Slavia le faltan casi 4 puntos: perdió 2-3 en casa con Lens. No es tan malo como su lugar, pero tampoco bueno.", tag=tag(4, T)),
        predu(T, 5, "Arsenal, favorito; Slavia anota 3 de cada 4 veces", (.22, .199, .581), "Slavia", "Arsenal", 3.6, .69,
              "Aun contra la mejor defensa, de local Slavia anota en 74% de las simulaciones."),
        endu(T, "Muro contra el ataque 30°", ["Arsenal: 2 goles en contra en 3.", "Sin Saka.", "Slavia 22%, empate 20%, Arsenal 58%."],
             "¿Arsenal mantiene el muro en Praga? Te leemos."),
    ]


# ------------------------------------------------------------------ NBA
def PHI():
    T = 6
    return [
        cov(T, KN, "76ers vs. Pistons: los dos mejores récords del Este, uno gana por 6 y el otro por 12", "76ers", "7-1", "Pistons", "6-1",
            "visitan a los · hoy 18:00 hora CDMX", "Filadelfia gana por 5.8 puntos; Detroit, por 11.6. ¿Cuál récord es real? 4 datos.", size=70),
        slide(2, T, "Filadelfia", "7-1, aunque por sus partidos esperaba 4.7",
              [Hero("1 en 12", "probabilidad de ir 7-1 o mejor con la probabilidad que tenía en cada partido.", AMBER),
               Stats([("+5.8", "diferencia por partido", GHOST), ("18°", "ataque de la liga, ajustado por rival", NEG)])],
              takeaway="Filadelfia ganó más de lo que su diferencia de puntos explica. Eso suele no durar: sus números son de equipo bueno, no de 7-1.", tag=tag(2, T)),
        slide(3, T, "El matchup", "La mejor defensa de la NBA contra un ataque del montón",
              [Duel("76ers", "Pistons", [
                  ("Puntos por partido", "110.9", "111.9", "liga: 113.4", None),
                  ("Puntos que permite", "105.1", "100.3", "más bajo = mejor", False),
                  ("Lugar en ataque (de 30)", "18°", "8°", "ajustado por rival", False),
                  ("Lugar en defensa (de 30)", "8°", "1°", "ajustado por rival", False)])],
              takeaway="Detroit permite 100 puntos por partido, la mejor defensa ajustada. A Filadelfia le va a costar: su ataque es 18°.", tag=tag(3, T)),
        slide(4, T, "Lo probamos", "¿El 7-1 de Filadelfia es real?",
              [Tests([(None, "«Filadelfia tiene más victorias de las que merece»", "Esperábamos 4.7; tiene 7.", "p = 0.085 · indicio"),
                      (False, "«Detroit está inflado»", "Esperábamos 4.9; tiene 6.", "p = 0.32 · normal")])],
              takeaway="Hoy, el cansancio no cuenta: ayer no hubo partidos, así que nadie juega con la noche anterior encima.", tag=tag(4, T)),
        slide(5, T, "La predicción", "Detroit gana 2 de cada 3",
              [MvM("Pistons ganan", .68, None) if False else Stats([("68%", "gana Detroit (rango 62–75%)", ACC), ("+6.9", "diferencia esperada para Detroit", GHOST)]),
               Stats([("220", "puntos esperados entre los dos (liga: 227)", GHOST)])],
              takeaway="Dos buenas defensas: menos puntos de lo normal. El récord dice parejo; los números dicen Detroit.", tag=tag(5, T)),
        endu(T, "El récord dice parejo; los números, Detroit", ["Filadelfia gana más de lo que sus puntos explican (indicio).", "Detroit: mejor defensa de la liga.", "Detroit 68%, por unos 7 puntos."],
             "¿Filadelfia rompe la lógica en Detroit? Te leemos.", m=NBA),
    ]


def HOU():
    T = 6
    return [
        cov(T, KN, "Timberwolves vs. Rockets: dos de los 5 mejores equipos de la NBA", "Timberwolves", "5-3", "Rockets", "7-1",
            "visitan a los · hoy 19:30 hora CDMX", "Houston: 3° en nuestro ranking. Minnesota: 5°. El récord engaña: 4 datos."),
        slide(2, T, "El récord engaña", "Minnesota va 5-3, pero juega como 5°",
              [Stats([("+11.4", "diferencia por partido de Minnesota", ACC), ("+12.9", "de Houston", ACC)]),
               Stats([("5.0", "victorias esperadas de Minnesota (tiene 5)", GHOST), ("5.2", "de Houston (tiene 7)", AMBER)])],
              takeaway="Casi la misma diferencia de puntos, pero 2 victorias de distancia. Houston ha convertido mejor su ventaja en victorias.", tag=tag(2, T)),
        slide(3, T, "El matchup", "Dos ataques y dos defensas de élite",
              [Duel("Wolves", "Rockets", [
                  ("Puntos por partido", "119.0", "119.2", "liga: 113.4", None),
                  ("Puntos que permite", "107.6", "106.4", "más bajo = mejor", False),
                  ("Lugar en ataque (de 30)", "5°", "3°", "ajustado por rival", False),
                  ("Lugar en defensa (de 30)", "6°", "4°", "ajustado por rival", False)])],
              takeaway="Casi idénticos. Houston es ligeramente mejor en todo… y juega en casa, donde va 4-0.", tag=tag(3, T)),
        slide(4, T, "Lo probamos", "¿Houston tiene más victorias de las que merece?",
              [Tests([(None, "«Houston está inflado»", "Esperábamos 5.2; tiene 7.", "p = 0.16 · indicio débil"),
                      (False, "«Minnesota está mal»", "Esperábamos 5.0; tiene 5.", "justo donde debe")])],
              takeaway="Houston es muy bueno: 3° del ranking. Pero 7-1 es un poco más de lo que sus puntos explican.", tag=tag(4, T)),
        slide(5, T, "La predicción", "Houston, ligero favorito por la localía",
              [Stats([("58%", "gana Houston (rango 49–65%)", ACC), ("+2.8", "diferencia esperada", GHOST)]),
               Stats([("226", "puntos esperados entre los dos", GHOST)])],
              takeaway="Sin la localía, sería casi un volado. El partido de la noche entre equipos de arriba.", tag=tag(5, T)),
        endu(T, "El mejor partido de la noche", ["Dos de los 5 mejores equipos.", "Houston: 2 victorias más con casi la misma diferencia.", "Houston 58%, por unos 3 puntos."],
             "¿Minnesota frena a Houston? Te leemos.", m=NBA),
    ]


def POR():
    T = 6
    return [
        cov(T, KN, "Trail Blazers vs. Suns: Portland va 5-1 y gana por 10.8. ¿Es real?", "Trail Blazers", "5-1", "Suns", "1-4",
            "visitan a los · hoy 20:00 hora CDMX", "Portland va 4-0 de visita. Phoenix pierde por 10.6. 4 datos."),
        slide(2, T, "Portland", "Un arranque que nadie esperaba",
              [Stats([("+10.8", "diferencia por partido", ACC), ("4-0", "de visita", ACC)]),
               Stats([("3.6", "victorias esperadas por sus partidos (tiene 5)", AMBER), ("42", "victorias el año pasado: equipo promedio", GHOST)])],
              takeaway="Portland llegó como equipo de media tabla. Lo de los arranques: de cada 10 puntos de ventaja temprana, se mantienen unos 3.", tag=tag(2, T)),
        slide(3, T, "El matchup", "Portland ataca; Phoenix no defiende",
              [Duel("Portland", "Phoenix", [
                  ("Puntos por partido", "120.2", "112.2", "liga: 113.4", True),
                  ("Puntos que permite", "109.3", "122.8", "más bajo = mejor", True),
                  ("Lugar en ataque (de 30)", "10°", "15°", "ajustado por rival", True),
                  ("Lugar en defensa (de 30)", "10°", "22°", "ajustado por rival", True)])],
              takeaway="Phoenix permite casi 123 puntos por partido. Ajustado por rivales la diferencia se achica: Portland 10° y Phoenix 15° en ataque.", tag=tag(3, T)),
        slide(4, T, "Lo probamos", "¿Portland es candidato?",
              [Tests([(None, "«Portland es mejor que el año pasado»", "Indicio, no prueba.", "p = 0.09"),
                      (None, "«Phoenix es tan malo como su 1-4»", "Esperábamos 2.0 victorias; tiene 1.", "p = 0.33 · normal")])],
              takeaway="Portland pinta para mejor que el año pasado, pero 6 partidos no alcanzan para afirmarlo. Proyección: unas 49 victorias.", tag=tag(4, T)),
        slide(5, T, "La predicción", "Portland, favorito aun de visita",
              [Stats([("56%", "gana Portland (rango 45–67%)", ACC), ("+2.2", "diferencia esperada para Portland", GHOST)]),
               Stats([("229", "puntos esperados entre los dos", GHOST)])],
              takeaway="No por 10.8 puntos, sino por unos 2. Esa es la regresión a la media: el modelo le cree poco a 6 partidos.", tag=tag(5, T)),
        endu(T, "Portland es bueno; no tan bueno como su 5-1", ["Gana por 10.8; esperamos ~2 hoy.", "Phoenix permite casi 123 por partido.", "Portland 56%."],
             "¿Portland sigue invicto de visita? Te leemos.", m=NBA),
    ]


def NOCHE():
    T = 5
    return [
        slide(1, T, KN, "Noche de 14 partidos: ¿cuántos favoritos van a caer?",
              [Hero("1 en 413", "probabilidad de que ganen los 14 favoritos de nuestro modelo.", ACC)],
              takeaway="Probabilidad compuesta: 14 chances multiplicadas. 3 datos.", style="cover"),
        slide(2, T, "Lo esperable", "Ganarán unos 9 de 14 favoritos",
              [Stats([("9.2", "favoritos ganan en promedio", ACC), ("7 a 11", "rango normal (80% de las noches)", GHOST)]),
               Stats([("67%", "acierto del modelo fuera de muestra (91 partidos)", ACC), ("0", "equipos cansados: ayer no hubo partidos", GHOST)])],
              takeaway="Si mañana ves que «solo» acertamos 9, es exactamente lo esperado. Acertar 14 sería rarísimo.", tag="DATO 1 DE 3"),
        slide(3, T, "Los más claros", "Los 3 favoritos más fuertes",
              [HBars([("Celtics vs. Bucks", 80, ACC), ("Spurs vs. Mavericks", 79, ACC), ("Knicks vs. Bulls", 78, ACC)], 100, "{}%", 360)],
              takeaway="Aun así, cada uno pierde 1 de cada 5 veces. Y los Lakers ganan 79% en Sacramento: el favorito de visita más claro.", tag="DATO 2 DE 3"),
        slide(4, T, "Los volados", "Los 3 partidos más parejos",
              [HBars([("Nuggets vs. Raptors", 52, AMBER), ("Clippers vs. Heat", 54, AMBER), ("Trail Blazers en Suns", 56, AMBER)], 100, "{}%", 360)],
              takeaway="Aquí el modelo casi no sabe. Ojo: Oklahoma City juega sin Holmgren ni J. Williams y el modelo no ve bajas.", tag="DATO 3 DE 3"),
        slide(5, T, "Conclusión", "Unos 9 de 14, y 3 volados",
              [Bullets(["Que ganen los 14 favoritos: 1 en 413.", "Lo normal: entre 7 y 11.", "3 partidos casi parejos."])],
              takeaway="¿Cuántos favoritos crees que caen hoy? Te leemos.", style="end", method=NBA),
    ]


if __name__ == "__main__":
    sets = {"FEN": FEN(), "AEK": AEK(), "LEI": LEI(), "BVB": BVB(), "LEN": LEN(), "SLA": SLA(), "PHI": PHI(), "HOU": HOU(), "POR": POR(), "NOCHE": NOCHE()}
    only = os.environ.get("ONLY")
    for k, ims in sets.items():
        if only and k not in only.split(","): continue
        o = f"{OUT}/{k}"; os.makedirs(o, exist_ok=True)
        for i, im in enumerate(ims, 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
