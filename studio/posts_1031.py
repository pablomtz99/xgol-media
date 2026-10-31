"""xGol — 31 oct: Liga MX J15 sábado (Pachuca-Tigres, Chivas-Atlante, América-Toluca). Diseño v7."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from matchup_1029 import Duel
from posts_1030 import three, MX

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/1031")
K = "Futbol · Liga MX · Jornada 15 · Sábado 31 de octubre"


def PAC():
    T = 7
    return [
        slide(1, T, K, "Pachuca vs. Tigres: un 13° lugar que juega como equipo de play-in",
              [Matchup("Pachuca", "13° · 16 pts", "Tigres", "15° · 15 pts", sep="recibe a · hoy 17:00 hora CDMX · Estadio Hidalgo")],
              takeaway="Pachuca viene de ganarle 2-1 al líder en su casa. Tigres lleva 3 partidos sin ganar. 5 datos.", style="cover", title_size=80),
        slide(2, T, "La paradoja", "Pachuca mete más de los que recibe… y está 13°",
              [Hero("22-19", "goles a favor y en contra de Pachuca: diferencia de +3. 5 equipos que están arriba de él anotan menos.", ACC),
               Stats([("16", "puntos reales", GHOST), ("21.3", "puntos que «merecía» por sus goles", ACC)])],
              takeaway="Con esos goles, lo normal sería estar en zona de play-in o más arriba. Le faltan 5 puntos.", tag="DATO 1 DE 5"),
        slide(3, T, "Lo probamos", "¿Mala suerte? Puede ser, pero no se puede afirmar",
              [Hero("17%", "de las veces un equipo con esos goles sumaría 16 puntos o menos por pura casualidad.", GHOST),
               Stats([("p = 0.17", "no es concluyente", GHOST), ("−5.3", "puntos de menos", NEG)])],
              takeaway="Lo que sí dicen los números: Pachuca juega mejor de lo que dice su lugar en la tabla. Y le ganó al líder la semana pasada.", tag="DATO 2 DE 5"),
        slide(4, T, "El rival", "Tigres: el equipo que empata",
              [Stats([("6", "empates en 14 partidos, empatado como el que más", AMBER), ("1.07", "goles por partido: de los ataques más bajos", NEG)]),
               Stats([("15-19", "goles a favor y en contra", GHOST), ("16.2", "puntos «merecidos» (tiene 15)", GHOST)])],
              takeaway="¿Tigres es «equipo de empates»? Lo probamos: con su nivel, 6 empates pasa 15% de las veces (p = 0.15). No es un patrón, es un ataque que no remata los partidos.", tag="DATO 3 DE 5"),
        slide(5, T, "El matchup", "Pachuca ataca más; Tigres defiende igual de bien",
              [Duel("Pachuca", "Tigres", [
                  ("Goles a favor por partido", "1.57", "1.07", "promedio de la liga: 1.50", True),
                  ("Goles en contra por partido", "1.36", "1.36", "los dos, igual", None)]),
               Stats([("2,400 m", "altura de Pachuca", ACC), ("540 m", "altura de Monterrey, casa de Tigres", GHOST)])],
              takeaway="La altura de Pachuca es real, pero no la podemos medir con este torneo y no está en el modelo. Si pesa, Pachuca es aún más favorito.", tag="DATO 4 DE 5"),
        slide(6, T, "La predicción", "Pachuca, favorito en casa",
              [three(.47, .25, .28, "Pachuca", "Tigres"),
               Stats([("2.7", "goles esperados entre los dos", ACC), ("54%", "probabilidad de que anoten los dos", GHOST)])],
              takeaway="Tigres gana 28% de las veces: necesita que su ataque, de los más flojos del torneo, aparezca en la altura.", tag="DATO 5 DE 5"),
        slide(7, T, "Conclusión", "Pachuca juega mejor de lo que dice la tabla",
              [Bullets(["Debería tener unos 5 puntos más (no comprobado).", "Tigres empata mucho porque anota poco.", "Pachuca 47%, empate 25%, Tigres 28%."])],
              takeaway="¿Pachuca empieza a sumar lo que merece? Te leemos.", style="end", method=MX),
    ]


def CHI():
    T = 6
    return [
        slide(1, T, K, "Chivas vs. Atlante: la mejor defensa del torneo, por mucho",
              [Matchup("Chivas", "4° · 26 pts", "Atlante", "16° · 14 pts", sep="recibe a · hoy 19:07 hora CDMX · Estadio Akron")],
              takeaway="Chivas viene de ganar 1-0 en Monterrey. Solo ha perdido 2 partidos en 14. 4 datos.", style="cover", title_size=80),
        slide(2, T, "La defensa", "12 goles en contra en 14 partidos",
              [HBars([("Chivas", 0.86, ACC), ("León", 1.29, GHOST), ("Tijuana", 1.29, GHOST), ("Promedio liga", 1.50, MUTED)], 1.7, "{}", 330)],
              takeaway="Goles en contra por partido. La segunda mejor defensa recibe 50% más goles que Chivas.", tag="DATO 1 DE 4"),
        slide(3, T, "¿Es real?", "Chivas está justo donde sus goles dicen",
              [Stats([("26", "puntos reales", ACC), ("25.6", "puntos «merecidos» por sus goles", ACC)]),
               Stats([("7-5-2", "récord: solo 2 derrotas", GHOST), ("21", "goles a favor: ataque normal", GHOST)])],
              takeaway="No es racha ni suerte: Chivas gana porque casi no le anotan. Su ataque es del montón.", tag="DATO 2 DE 4"),
        slide(4, T, "El matchup", "El ataque de Atlante contra el muro de Chivas",
              [Duel("Chivas", "Atlante", [
                  ("Goles a favor por partido", "1.50", "1.00", "promedio de la liga: 1.50", True),
                  ("Goles en contra por partido", "0.86", "1.43", "más bajo = mejor", True)])],
              takeaway="Atlante anota un gol por partido, de los peores del torneo. Contra la mejor defensa, esperamos menos de uno: 0.9.", tag="DATO 3 DE 4"),
        slide(5, T, "La predicción", "Chivas, favorito… en un partido de pocos goles",
              [three(.53, .25, .22, "Chivas", "Atlante"),
               Stats([("2.5", "goles esperados entre los dos", GHOST), ("45%", "probabilidad de 3 goles o más", GHOST)])],
              takeaway="Es el partido del sábado con menos goles esperados. Ganar 1-0 es el estilo de Chivas.", tag="DATO 4 DE 4"),
        slide(6, T, "Conclusión", "Chivas gana con la defensa, no con el ataque",
              [Bullets(["0.86 goles en contra por partido: la mejor por mucho.", "Su lugar en la tabla es real.", "Chivas 53%, empate 25%, Atlante 22%."])],
              takeaway="¿Otro 1-0 en el Akron? Te leemos.", style="end", method=MX),
    ]


def AME():
    T = 7
    return [
        slide(1, T, K, "América vs. Toluca: el mejor ataque contra un equipo que lleva 6 sin ganar",
              [Matchup("América", "1° · 28 pts", "Toluca", "5° · 23 pts", sep="recibe a · hoy 21:10 hora CDMX · Estadio Banorte")],
              takeaway="América sumó 1 punto en sus últimos 2. Toluca, 6 partidos sin ganar. ¿Crisis o mala racha? 5 datos.", style="cover", title_size=76),
        slide(2, T, "Los ataques", "El 1° y el 3° ataque del torneo",
              [HBars([("América", 34, ACC), ("Cruz Azul", 32, GHOST), ("Toluca", 29, AMBER)], 38, "{} goles", 330)],
              takeaway="América 2.43 goles por partido; Toluca 2.07. El promedio de la liga es 1.50.", tag="DATO 1 DE 5"),
        slide(3, T, "La racha de Toluca", "6 partidos sin ganar… con números de equipo de arriba",
              [Hero("25.6", "puntos «merecía» Toluca por sus goles (29 a favor, 19 en contra). Tiene 23.", AMBER),
               Stats([("+10", "diferencia de goles: la 2ª mejor", ACC), ("6-5-3", "solo 3 derrotas en 14", GHOST)])],
              takeaway="Una racha así es rara para un equipo de su nivel (pasa ~1 de cada 20 temporadas), pero sus goles dicen que el equipo sigue siendo bueno.", tag="DATO 2 DE 5"),
        slide(4, T, "¿Equipo de empates?", "Toluca empata mucho. ¿Es un patrón?",
              [Stats([("5", "empates en 14", AMBER), ("p = 0.55", "normal para su nivel", GHOST)])],
              takeaway="Lo probamos: no. Con su nivel, 5 empates en 14 es lo esperable. Lo que le falta es cerrar partidos, no un «estilo de empatar».", tag="DATO 3 DE 5"),
        slide(5, T, "El matchup", "Dos ataques que anotan mucho y defienden igual",
              [Duel("América", "Toluca", [
                  ("Goles a favor por partido", "2.43", "2.07", "promedio de la liga: 1.50", True),
                  ("Goles en contra por partido", "1.36", "1.36", "los dos, igual", None)])],
              takeaway="Ninguno de los dos defiende especial (y en el último duelo ganó América 2-1). Cuando chocan dos ataques así, los goles son casi seguros. La altura no pesa: Toluca vive más arriba que la Ciudad de México.", tag="DATO 4 DE 5"),
        slide(6, T, "La predicción", "El partido con más goles esperados del sábado",
              [three(.48, .22, .31, "América", "Toluca"),
               Stats([("3.6", "goles esperados entre los dos", ACC), ("69%", "probabilidad de 3 goles o más", ACC)])],
              takeaway="7 de cada 10 veces habrá 3 goles o más, y en 7 de cada 10 anotan los dos. América es favorito, pero Toluca gana casi 1 de cada 3.", tag="DATO 5 DE 5"),
        slide(7, T, "Conclusión", "Toluca está en mala racha, no en crisis",
              [Bullets(["Toluca merece unos 2.6 puntos más de los que tiene.", "El 1° y el 3° ataque del torneo.", "América 48%, empate 22%, Toluca 31%. Se esperan goles."])],
              takeaway="¿Toluca rompe la racha en el Banorte? Te leemos.", style="end", method=MX),
    ]


if __name__ == "__main__":
    for k, ims in {"PAC": PAC(), "CHI": CHI(), "AME": AME()}.items():
        o = f"{OUT}/{k}"; os.makedirs(o, exist_ok=True)
        for i, im in enumerate(ims, 1):
            im.save(f"{o}/{i:02d}.png")
    print("ok")
