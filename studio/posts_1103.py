"""xGol — 3 nov: Champions League, jornada 4 (8 partidos del martes). Diseño v7.
Modelo xGol UCL v0 (studio/models/ucl_model_v0.py) ajustado con los 54 partidos J1–J3. Rangos 10–90% por bootstrap (150)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from matchup_1029 import Duel
from posts_1030 import three

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/1103")
UCL = ("Método: modelo de goles (Poisson) por equipo, ajustado con los 54 partidos de la fase liga 2026-27 y el coeficiente UEFA "
       "como punto de partida; ventaja de local estimada. Puntos «merecidos»: lo que el modelo esperaba en sus 3 partidos. "
       "Datos: UEFA.com. Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta.")
K = "Futbol · Champions League · Jornada 4 · Martes 3 de noviembre"


def cover(T, title, a, ra, b, rb, hora, take, size=78):
    return slide(1, T, K, title, [Matchup(a, ra, b, rb, sep=f"recibe a · hoy {hora} hora CDMX")], takeaway=take, style="cover", title_size=size)


def duel(T, n, title, a, b, rows, take):
    return slide(n, T, "El matchup", title, [Duel(a, b, rows)], takeaway=take, tag=f"DATO {n-1} DE {T-2}")


def pred(T, n, title, h, d, aw, la, lb, xg, o25, take):
    return slide(n, T, "La predicción", title, [three(h, d, aw, la, lb),
                 Stats([(f"{xg:.1f}", "goles esperados entre los dos", ACC), (f"{o25:.0%}", "probabilidad de 3 goles o más", GHOST)])],
                 takeaway=take, tag=f"DATO {n-1} DE {T-2}")


def end(T, title, bullets, q):
    return slide(T, T, "Conclusión", title, [Bullets(bullets)], takeaway=q, style="end", method=UCL)


def gpp(gf, ga):
    return [("Goles a favor por partido", f"{gf[0]/3:.2f}", f"{gf[1]/3:.2f}", "en esta Champions", gf[0] > gf[1] if gf[0] != gf[1] else None),
            ("Goles en contra por partido", f"{ga[0]/3:.2f}", f"{ga[1]/3:.2f}", "más bajo = mejor", ga[0] < ga[1] if ga[0] != ga[1] else None)]


def CONTEXTO():
    T = 4
    return [
        slide(1, T, "Futbol · Champions League · Antes de la jornada 4", "Esta Champions tiene goles como nunca",
              [Hero("4.1", "goles por partido en las primeras 3 jornadas (221 goles en 54 partidos).", ACC)],
              takeaway="Hoy se juegan 9 partidos. Antes de verlos, 2 datos que cambian cómo leer cualquier pronóstico.", style="cover"),
        slide(2, T, "Los goles", "Solo 6 empates en 54 partidos",
              [Stats([("6 de 54", "partidos terminaron empatados (11%)", AMBER), ("32", "victorias de local (59%)", ACC)])],
              takeaway="Con tantos goles, el empate casi desaparece. Por eso nuestro modelo da empates de ~20%, no de 27% como en una liga normal.", tag="DATO 1 DE 2"),
        slide(3, T, "Ser local", "Jugar en casa vale mucho en esta Champions",
              [Hero("×1.43", "goles anota un equipo de local respecto a lo que anotaría de visita, según nuestro modelo.", ACC)],
              takeaway="Es más que en las ligas (~×1.2–1.3). Puede ser porque son pocos partidos: lo tomamos con cautela, pero hoy lo usamos.", tag="DATO 2 DE 2"),
        slide(4, T, "Conclusión", "Hoy, espera goles y desconfía del empate",
              [Bullets(["4.1 goles por partido, de los promedios más altos.", "Solo 11% de empates.", "La localía pesa más de lo normal."])],
              takeaway="¿Sigue la lluvia de goles hoy? Te leemos.", style="end", method=UCL),
    ]


def SHA():
    T = 6; r = dict(p=(.494, .22, .286), xg=3.38, o=.657)
    return [
        cover(T, "Shakhtar vs. Sporting: la defensa que juega de «local» lejos de casa", "Shakhtar", "1-1-1 · 4 pts", "Sporting", "2-0-1 · 6 pts", "11:45",
              "Shakhtar defiende como un grande y ataca como un chico. 4 datos."),
        slide(2, T, "El contexto", "Shakhtar no juega en su estadio desde 2014",
              [Hero("0", "partidos europeos en Donetsk desde 2014, por la guerra: Shakhtar es «local» en estadios prestados.", AMBER)],
              takeaway="Nuestro modelo le da la ventaja de local completa. Siendo críticos: su «casa» no es su casa, así que probablemente lo sobreestima.", tag="DATO 1 DE 4"),
        duel(T, 3, "Shakhtar defiende; Sporting ataca", "Shakhtar", "Sporting", gpp((4, 7), (3, 4)) +
             [("Lugar en defensa (de 36)", "7°", "15°", "ajustado por rival", True), ("Lugar en ataque (de 36)", "24°", "14°", "ajustado por rival", False)],
             "Shakhtar recibe 1 gol por partido; Sporting anota 2.3. El partido se decide en si Sporting rompe ese bloque."),
        slide(4, T, "Lo probamos", "¿Alguno tiene más puntos de los que merece?",
              [Tests([(False, "«Sporting está inflado»", "Esperábamos 6.1 puntos; tiene 6.", "3 partidos"),
                      (False, "«Shakhtar está regalado»", "Esperábamos 4.2; tiene 4.", "3 partidos")])],
              takeaway="Los dos están justo donde sus goles dicen. Aquí no hay suerte que corregir.", tag="DATO 3 DE 4"),
        pred(T, 5, "Shakhtar, favorito por la localía", *r["p"], "Shakhtar", "Sporting", r["xg"], r["o"],
             "Sin la ventaja de local, el partido sería casi un volado. Por eso Sporting gana casi 3 de cada 10 aun de visita."),
        end(T, "Partido más parejo de lo que dice el modelo", ["Shakhtar: 7ª mejor defensa, 24° ataque.", "Su localía es prestada: ventaja menor.", "Shakhtar 49%, empate 22%, Sporting 29%."],
            "¿Sporting rompe el bloque ucraniano? Te leemos."),
    ]


def GAL():
    T = 6; r = dict(p=(.518, .205, .277), xg=3.77, o=.725)
    return [
        cover(T, "Galatasaray vs. Stuttgart: el «chico» con 7 puntos visita Estambul", "Galatasaray", "3 pts", "Stuttgart", "2-1-0 · 7 pts", "11:45",
              "Stuttgart llegó con uno de los coeficientes más bajos y sigue invicto. 4 datos."),
        slide(2, T, "La sorpresa", "Stuttgart suma más de lo que sus goles explican",
              [Stats([("7", "puntos reales", ACC), ("5.3", "puntos «merecidos» por sus partidos", GHOST)]),
               Stats([("2", "goles en contra en 3 partidos", ACC), ("29%", "de las veces sumaría 7 o más por azar", GHOST)])],
              takeaway="Le sobran 1.7 puntos, pero sumar 7 con su nivel pasa 3 de cada 10 veces. No es suerte comprobable: es un buen arranque.", tag="DATO 1 DE 4"),
        duel(T, 3, "El ataque de Galatasaray contra una defensa que casi no recibe", "Galatasaray", "Stuttgart", gpp((6, 7), (9, 2)) +
             [("Lugar en defensa (de 36)", "27°", "16°", "ajustado por rival", False)],
             "Galatasaray recibe 3 goles por partido; Stuttgart, 0.7. Pero ojo: Galatasaray recibió 4 de Barcelona, no de un rival cualquiera."),
        slide(4, T, "El estadio", "Estambul: la localía que el modelo sí ve",
              [Hero("×1.43", "goles de más anota un local en esta Champions, según nuestro modelo.", AMBER)],
              takeaway="Galatasaray perdió sus 2 partidos contra Barcelona y Sporting… y le ganó 4-2 a Lille de visita. Su nivel real está en medio.", tag="DATO 3 DE 4"),
        pred(T, 5, "Galatasaray, favorito en casa; se esperan goles", *r["p"], "Galatasaray", "Stuttgart", r["xg"], r["o"],
             "Stuttgart gana casi 3 de cada 10. Para el modelo, sus 7 puntos todavía no pesan más que su historia."),
        end(T, "Stuttgart llega invicto, pero Estambul pesa", ["Stuttgart: 7 puntos, 2 goles en contra.", "Galatasaray recibe 3 por partido.", "Galatasaray 52%, empate 20%, Stuttgart 28%."],
            "¿El invicto alemán sobrevive en Estambul? Te leemos."),
    ]


def ATL():
    T = 7; r = dict(p=(.479, .207, .314), xg=3.85, o=.74)
    return [
        cover(T, "Atlético vs. Bayern: la 2ª mejor defensa contra un ataque que no falla desde hace 24 partidos", "Atlético", "1-1-1 · 4 pts", "Bayern", "1-2-0 · 5 pts", "14:00",
              "Y Bayern llega sin Olise, Gnabry ni Neuer. 5 datos.", size=70),
        slide(2, T, "El Atlético", "4 victorias seguidas sin recibir gol",
              [Stats([("4", "victorias seguidas sin gol en contra (todas las competencias)", ACC), ("7", "victorias seguidas en LaLiga", ACC)]),
               Stats([("2°", "mejor defensa de esta Champions, ajustada por rival", ACC), ("3", "goles en contra en 3 partidos", GHOST)])],
              takeaway="Este Atlético está en su mejor momento del año, y su fuerza es la de siempre: no dejar anotar.", tag="DATO 1 DE 5"),
        slide(3, T, "El Bayern", "Bayern anota siempre… y también recibe",
              [Stats([("24", "partidos seguidos de Champions anotando", ACC), ("9", "partidos seguidos de visita en Champions con goles de los dos", AMBER)]),
               Stats([("3", "bajas importantes: Olise, Gnabry y Neuer", NEG), ("4 + 2", "goles y asistencias de Kane en 3 partidos", ACC)])],
              takeaway="Los últimos dos de Bayern en Champions: 3-3 y 2-2. Anota mucho, pero ya no cierra partidos. Y el modelo no ve las bajas.", tag="DATO 2 DE 5"),
        duel(T, 4, "El muro contra el ataque", "Atlético", "Bayern", gpp((4, 10), (3, 5)) +
             [("Lugar en defensa (de 36)", "2°", "12°", "ajustado por rival", True), ("Lugar en ataque (de 36)", "16°", "5°", "ajustado por rival", False)],
             "Bayern anota más del doble, pero el Atlético recibe 1 por partido. Clave: las bajas de Olise y Gnabry le quitan desequilibrio por fuera."),
        slide(5, T, "Lo probamos", "¿Bayern merece más que sus 5 puntos?",
              [Tests([(None, "«Bayern merecía más»", "Esperábamos 6.5 puntos; tiene 5.", "p = 0.25 · indicio, no prueba"),
                      (False, "«El Atlético está inflado»", "Esperábamos 4.4; tiene 4.", "en línea con sus goles")])],
              takeaway="A Bayern le faltan 1.5 puntos por los dos empates, pero con 3 partidos no se puede afirmar que sea mala suerte.", tag="DATO 4 DE 5"),
        pred(T, 6, "El Atlético, ligero favorito en casa", *r["p"], "Atlético", "Bayern", r["xg"], r["o"],
             "Rango del modelo: el Atlético gana entre 37% y 56%. Y si las bajas de Bayern pesan, aún más."),
        end(T, "Partido de goles, a pesar del muro", ["Atlético: 4 sin recibir gol; Bayern: 24 anotando.", "Bayern sin Olise, Gnabry ni Neuer.", "Atlético 48%, empate 21%, Bayern 31%."],
            "¿Se rompe la racha de 24 partidos de Bayern? Te leemos."),
    ]


def BAR():
    T = 6; r = dict(p=(.60, .169, .231), xg=4.76, o=.854)
    return [
        cover(T, "Barcelona vs. Aston Villa: el invicto perfecto visita a uno de los mejores ataques", "Barcelona", "2-0-1 · 6 pts", "Aston Villa", "9 pts", "14:00",
              "Villa ganó sus 3 partidos con 12 goles a favor. Barcelona anota casi 4 por partido. 4 datos."),
        slide(2, T, "Aston Villa", "Villa va perfecto: 9 de 9",
              [Stats([("12-3", "goles a favor y en contra", ACC), ("6.6", "puntos «merecidos» por sus partidos", GHOST)]),
               Stats([("6-0", "a Fenerbahçe", ACC), ("26%", "de las veces sumaría 9 por azar", GHOST)])],
              takeaway="Villa juega muy bien, pero 9 de 9 también tiene algo de fortuna: lo normal con su nivel era unos 6.6 puntos.", tag="DATO 1 DE 4"),
        duel(T, 3, "Dos de los 6 mejores ataques de la Champions", "Barcelona", "Villa", gpp((11, 12), (6, 3)) +
             [("Lugar en ataque (de 36)", "3°", "6°", "ajustado por rival", True), ("Lugar en defensa (de 36)", "6°", "5°", "ajustado por rival", None)],
             "Los dos atacan y defienden casi igual de bien. La diferencia la hace el estadio: el modelo le da a Barcelona ×1.43 goles de local."),
        slide(4, T, "Lo probamos", "¿Quién está inflado?",
              [Tests([(None, "«Villa está inflado»", "Esperábamos 6.6 puntos; tiene 9.", "p = 0.26 · indicio, no prueba"),
                      (False, "«Barcelona perdió por mala suerte»", "Esperábamos 5.1; tiene 6.", "en línea con sus goles")])],
              takeaway="Barcelona perdió 4-2 en París contra el mejor del torneo. Los otros dos los ganó 5-1 y 4-1.", tag="DATO 3 DE 4"),
        pred(T, 5, "Barcelona, favorito; casi seguro habrá goles", *r["p"], "Barcelona", "Aston Villa", r["xg"], r["o"],
             "85% de probabilidad de 3 goles o más y 80% de que anoten los dos. Uno de los más abiertos de la noche."),
        end(T, "Choque de ataques en Barcelona", ["Villa: 9 de 9, con algo de fortuna.", "Dos de los 6 mejores ataques.", "Barcelona 60%, empate 17%, Villa 23%."],
            "¿Villa sigue perfecto? Te leemos."),
    ]


def FEY():
    T = 6; r = dict(p=(.421, .214, .364), xg=3.74, o=.721)
    return [
        cover(T, "Feyenoord vs. Inter: el grande que suma solo 3 puntos", "Feyenoord", "3 pts", "Inter", "1-0-2 · 3 pts", "14:00",
              "Inter tiene uno de los coeficientes más altos y solo 3 puntos. ¿Mala racha o algo más? 4 datos."),
        slide(2, T, "El Inter", "Inter recibió 4 goles en casa de un equipo belga",
              [Stats([("3-4", "contra Brujas, en Milán", NEG), ("1-2", "en el Bernabéu", GHOST)]),
               Stats([("4.5", "puntos «merecidos» por sus partidos", AMBER), ("3", "puntos reales", NEG)])],
              takeaway="Perder en Madrid es normal. Recibir 4 en casa de Brujas, no: es el partido que le quitó los puntos.", tag="DATO 1 DE 4"),
        duel(T, 3, "Dos equipos que reciben más de lo que anotan", "Feyenoord", "Inter", gpp((4, 5), (8, 6)) +
             [("Lugar en ataque (de 36)", "21°", "12°", "ajustado por rival", False), ("Lugar en defensa (de 36)", "21°", "11°", "ajustado por rival", False)],
             "Ajustado por rivales, Inter es mejor en todo. Feyenoord recibió 5 de Barcelona, pero le ganó 3-2 a Como en casa."),
        slide(4, T, "Lo probamos", "¿Inter está peor de lo que es?",
              [Tests([(None, "«Inter merecía más puntos»", "Esperábamos 4.5; tiene 3.", "p = 0.35 · indicio débil"),
                      (False, "«Feyenoord está inflado»", "Esperábamos 3.1; tiene 3.", "justo donde debe")])],
              takeaway="Inter debería tener 1 o 2 puntos más. No alcanza para llamarlo mala suerte, pero sí para no darlo por muerto.", tag="DATO 3 DE 4"),
        pred(T, 5, "El partido más parejo del martes", *r["p"], "Feyenoord", "Inter", r["xg"], r["o"],
             "La localía de Feyenoord compensa casi toda la diferencia de nivel. Rango: Inter gana entre 29% y 44%."),
        end(T, "Inter es mejor, pero en Róterdam es un volado", ["Inter: 3 puntos, merecía ~4.5.", "La localía empareja el partido.", "Feyenoord 42%, empate 21%, Inter 36%."],
            "¿Inter despierta en Róterdam? Te leemos."),
    ]


def BOD():
    T = 6; r = dict(p=(.597, .179, .224), xg=4.27, o=.80)
    return [
        cover(T, "Bodø/Glimt vs. Lille: pasto sintético, frío ártico y un equipo con 0 puntos", "Bodø", "1-0-2 · 3 pts", "Lille", "0-0-3 · 0 pts", "14:00",
              "Bodø le ganó 1-0 a Dortmund en casa. Lille recibió 10 goles en 3 partidos. 4 datos."),
        slide(2, T, "La cancha", "Bodø juega arriba del Círculo Polar Ártico",
              [Stats([("Sintético", "pasto artificial: el balón corre distinto", AMBER), ("1-0", "a Dortmund en su estadio", ACC)])],
              takeaway="El modelo solo ve la ventaja de local promedio (×1.43). Siendo críticos: la cancha y el frío de Bodø probablemente pesan más que eso.", tag="DATO 1 DE 4"),
        duel(T, 3, "Lille recibe más de 3 goles por partido", "Bodø", "Lille", gpp((4, 4), (9, 10)),
             "Bodø recibió 5 de Bayern y 4 de Nápoles, de visita. En casa, solo jugó una vez: 1-0 a Dortmund."),
        slide(4, T, "Lo probamos", "¿Lille es tan malo como sus 0 puntos?",
              [Tests([(None, "«Lille merecía más»", "Esperábamos 3.3 puntos; tiene 0.", "p = 0.11 · indicio"),
                      (False, "«Bodø está inflado»", "Esperábamos 2.8; tiene 3.", "justo donde debe")])],
              takeaway="Lille perdió 2-3 y 2-4: partidos con goles a favor. Le faltan unos 3 puntos, aunque no se puede afirmar que sea mala suerte.", tag="DATO 3 DE 4"),
        pred(T, 5, "Bodø, favorito en su cancha", *r["p"], "Bodø/Glimt", "Lille", r["xg"], r["o"],
             "Seis de cada 10 veces gana Bodø. Y con dos defensas así, 80% de probabilidad de 3 goles o más."),
        end(T, "En el Ártico, Bodø es favorito", ["Pasto sintético y frío: ventajas que el modelo no ve.", "Lille: 0 puntos, merecía ~3.", "Bodø 60%, empate 18%, Lille 22%."],
            "¿Lille suma sus primeros puntos en el Ártico? Te leemos."),
    ]


def MUN():
    T = 6; r = dict(p=(.445, .207, .348), xg=3.95, o=.756)
    return [
        cover(T, "Manchester United vs. Roma: dos equipos con menos puntos de los que merecen", "United", "1-0-2 · 3 pts", "Roma", "1-1-1 · 4 pts", "14:00",
              "United empezó con 4-0 y luego perdió 0-2 y 1-4. Roma le ganó 4-0 a Slovan. 4 datos."),
        slide(2, T, "Las cuentas", "A los dos les faltan puntos",
              [Table(("Esperados", "Reales"), [("Manchester United", "4.4", "3"), ("Roma", "5.7", "4")], colors=[GHOST, NEG])],
              takeaway="Roma perdió 3-4 con el Real Madrid y empató en Estambul. United perdió 1-4 en el estadio de Como.", tag="DATO 1 DE 4"),
        duel(T, 3, "Roma ataca mejor; United necesita su estadio", "United", "Roma", gpp((5, 8), (6, 5)) +
             [("Lugar en ataque (de 36)", "19°", "9°", "ajustado por rival", False), ("Lugar en defensa (de 36)", "19°", "14°", "ajustado por rival", False)],
             "Ajustado por rivales, Roma es mejor en ataque y en defensa. La localía en Old Trafford es lo que pone a United arriba."),
        slide(4, T, "Lo probamos", "¿Mala suerte de los dos?",
              [Tests([(None, "«Roma merecía más»", "Esperábamos 5.7; tiene 4.", "p = 0.34 · indicio débil"),
                      (None, "«United merecía más»", "Esperábamos 4.4; tiene 3.", "p = 0.39 · indicio débil")])],
              takeaway="Con 3 partidos, ninguna diferencia es concluyente. Lo seguro: los dos están en la parte media-baja y necesitan ganar.", tag="DATO 3 DE 4"),
        pred(T, 5, "United, ligero favorito por jugar en casa", *r["p"], "Man. United", "Roma", r["xg"], r["o"],
             "Rango: United gana entre 34% y 54%. Sin la localía, Roma sería favorito."),
        end(T, "Partido de necesitados en Old Trafford", ["A los dos les faltan puntos.", "Roma es mejor; United tiene la localía.", "United 44%, empate 21%, Roma 35%."],
            "¿Quién sale de la zona baja? Te leemos."),
    ]


def VIL():
    T = 6; r = dict(p=(.323, .18, .497), xg=4.95, o=.871)
    return [
        cover(T, "Villarreal vs. PSG: el mejor ataque de la Champions visita una defensa que deja llegar", "Villarreal", "1-0-2 · 3 pts", "PSG", "3-0-0 · 9 pts", "14:00",
              "PSG: 14 goles en 3 partidos. Villarreal: 8 en contra. 4 datos."),
        slide(2, T, "El PSG", "14 goles en 3 partidos",
              [Stats([("6-1", "a Slovan", ACC), ("4-2", "a Barcelona y a City", ACC)]),
               Stats([("1°", "mejor ataque, ajustado por rival", ACC), ("6.2", "puntos «merecidos» (tiene 9)", AMBER)])],
              takeaway="Le ganó por 2 a Barcelona y a Manchester City. Merecía unos 6 puntos por sus partidos, pero es el mejor equipo de lo que va del torneo.", tag="DATO 1 DE 4"),
        duel(T, 3, "Villarreal anota bien, pero defiende mal", "Villarreal", "PSG", gpp((8, 14), (8, 5)) +
             [("Lugar en defensa (de 36)", "22°", "4°", "ajustado por rival", False), ("Lugar en ataque (de 36)", "10°", "1°", "ajustado por rival", False)],
             "Villarreal le metió 3 a Liverpool y 3 a Nápoles: sabe atacar. El problema es lo que recibe: 2.7 goles por partido."),
        slide(4, T, "Lo probamos", "¿El PSG está inflado?",
              [Tests([(None, "«PSG tiene más de lo que merece»", "Esperábamos 6.2; tiene 9.", "p = 0.22 · indicio, no prueba"),
                      (False, "«Villarreal está regalado»", "Esperábamos 3.6; tiene 3.", "en línea con sus goles")])],
              takeaway="Ganar sus 3 partidos con ese nivel pasa 2 de cada 10 veces. Es muy bueno… y también le salió todo.", tag="DATO 3 DE 4"),
        pred(T, 5, "PSG, favorito; el partido con más goles esperados", *r["p"], "Villarreal", "PSG", r["xg"], r["o"],
             "Casi 5 goles esperados y 87% de probabilidad de 3 o más. El PSG gana la mitad de las veces, aun de visita."),
        end(T, "Lluvia de goles esperada en Villarreal", ["PSG: el mejor ataque del torneo.", "Villarreal recibe 2.7 por partido.", "Villarreal 32%, empate 18%, PSG 50%."],
            "¿PSG llega a 12 de 12? Te leemos."),
    ]


if __name__ == "__main__":
    sets = {"SHA": SHA(), "GAL": GAL(), "ATL": ATL(), "BAR": BAR(), "FEY": FEY(), "BOD": BOD(), "MUN": MUN(), "VIL": VIL(), "CTX": CONTEXTO()}
    for k, ims in sets.items():
        o = f"{OUT}/{k}"; os.makedirs(o, exist_ok=True)
        for i, im in enumerate(ims, 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
