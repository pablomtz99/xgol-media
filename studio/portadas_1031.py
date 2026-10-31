"""xGol — portadas de las 4 ideas del 31 oct (sáb 31 – dom 1 nov). Diseño v7."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1031")
LEGAL = "Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta."


def covers():
    return {
        "1-nfl-kc-den": slide(1, 7, "NFL · Semana 8 · Domingo 1 de noviembre · 15:25 CDMX",
            "1,609 metros de altura… ¿y cuánto pesan en el marcador?",
            [Matchup("Chiefs", "5-1", "Broncos", "5-2", sep="visitan a · Denver, la ciudad más alta de la NFL"),
             Stats([("+0.9", "puntos extra por jugar en Denver (p = 0.41)", ACC),
                    ("50%", "nuestro modelo: un volado (rango 31–72%)", GHOST)])],
            takeaway="Probamos 16 temporadas: la «ventaja de la altura» no se distingue del azar. Y Mahomes va 6-2 en Denver.",
            style="cover", method=LEGAL),
        "2-nfl-min-det": slide(1, 7, "NFL · Semana 8 · Domingo 1 de noviembre · 12:00 CDMX",
            "6-0 con el ataque 29° de la liga: ¿quién sostiene a Minnesota?",
            [Matchup("Vikings", "6-0", "Lions", "4-2", sep="visitan a · la mejor defensa contra la defensa 29°"),
             Stats([("33", "puntos por juego de Minnesota", ACC), ("58", "puntos por juego de Detroit", AMBER),
                    ("53%", "gana Minnesota (rango 42–65%)", GHOST)])],
            takeaway="Por sus puntos, Minnesota «merecía» 4.7 victorias, no 6. Algo de eso es racha… pero no todo.",
            style="cover", method=LEGAL),
        "3-futbol-liv-ars": slide(1, 7, "Premier League · Jornada 9 · Domingo 1 nov · 10:30 CDMX",
            "Arsenal: 7 victorias con solo 13 goles. ¿Eficiencia o racha?",
            [Matchup("Liverpool", "4° · 15 pts", "Arsenal", "2° · 21 pts", sep="recibe a · en Anfield"),
             Stats([("33%", "gana Liverpool", GHOST), ("29%", "empate", GHOST), ("38%", "gana Arsenal", ACC)])],
            takeaway="Por sus goles, Arsenal «merecía» 16.7 puntos. Lleva 21. Eso pasa 1 de cada 8 veces: indicio, no prueba.",
            style="cover", method=LEGAL),
        "4-ligamx-ame-tol": slide(1, 7, "Liga MX · Jornada 15 · Sábado 31 de octubre · 21:10 CDMX",
            "El mejor ataque contra el 3° mejor: 3 de cada 4 veces habrá 3 goles o más",
            [Matchup("América", "1° · 28 pts", "Toluca", "5° · 23 pts", sep="recibe a · 34 y 29 goles a favor"),
             Stats([("53%", "gana América (36–69%)", ACC), ("20%", "empate", GHOST), ("27%", "gana Toluca", GHOST)])],
            takeaway="Toluca lleva 5 empates en 14. ¿Equipo de empates? Lo probamos: no (p = 0.55). Por sus goles, merecía 2.6 puntos más.",
            style="cover", method=LEGAL),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok")
