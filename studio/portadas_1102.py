"""xGol — portadas de las 4 ideas del 2 nov (Champions, jornada 4: mar 3 – mié 4 nov). Diseño v7.
Modelo xGol UCL v0: Poisson con ataque/defensa por equipo = β·log(coeficiente UEFA) + desviación ridge (λ=12),
ajustado con los 54 partidos de la fase liga 2026-27 (UEFA.com); localía estimada (×1.43). Validación fuera de
muestra: ajustado con J1-J2, predice J3 (n=18): Brier 0.475 vs 0.667 (1/3 a todo) y 0.576 (frecuencias L/E/V).
Rangos = percentiles 10–90 por bootstrap de partidos (400 réplicas). Cálculos en /tmp/claude-0/m (ucl3.py, calc*.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1102")
LEGAL = "Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta."


def covers():
    return {
        "1-ucl-kane-record": slide(1, 7, "Champions · Jornada 4 · Martes 3 de noviembre · 14:00 CDMX",
            "Kane, a un partido del récord de Ronaldo: lo logra 4 de cada 10 veces",
            [Matchup("Bayern", "1-2-0", "Atlético", "1-1-1", sep="visita al · Atlético, invicto en casa ante Bayern (2G 1E)"),
             Stats([("10", "seguidos anotando (récord: 11)", ACC),
                    ("43%", "Kane marca (35–52%)", GHOST),
                    ("1 en 182", "chance de 10 seguidos con su promedio en Bayern", AMBER)])],
            takeaway="Con 37 goles en 41 partidos, Kane anota en 6 de cada 10. Contra la defensa del Atlético, de visita, baja a 4 de cada 10.",
            style="cover", method=LEGAL),
        "2-ucl-liverpool-sin-empates": slide(1, 7, "Champions · Jornada 4 · Miércoles 4 de noviembre · 11:45 CDMX",
            "Liverpool: 46 partidos europeos sin un solo empate. Eso pasa 1 en 6,449",
            [Matchup("Liverpool", "3-0-0", "Fenerbahçe", "0-2-1", sep="visita al · Fenerbahçe, 10 partidos de Champions sin ganar"),
             Stats([("32-0-14", "últimos 46 en Europa (G-E-P)", ACC),
                    ("17%", "empate, nuestro modelo (15–21%)", GHOST),
                    ("7%", "que algún club de 36 la tenga", AMBER)])],
            takeaway="Prueba binomial con la tasa de empates de Champions (17%): p = 0.0002. Rarísimo… pero buscando entre 36 clubes, alguien podía tenerla.",
            style="cover", method=LEGAL),
        "3-ucl-haaland-leipzig": slide(1, 7, "Champions · Jornada 4 · Miércoles 4 de noviembre · 14:00 CDMX",
            "12 goles en 8 partidos a Leipzig. ¿Su víctima favorita? Los números dicen que no tanto",
            [Matchup("Man City", "2-0-1", "Leipzig", "1-0-2", sep="visita al · Leipzig, 5 derrotas seguidas ante ingleses en Europa"),
             Stats([("8.1", "goles esperados en 8 partidos con su promedio (61 en 60)", GHOST),
                    ("1 en 8", "chance de llegar a 12 o más solo por su nivel", ACC),
                    ("48%", "nuestro modelo: gana City (35–58%)", GHOST)])],
            takeaway="Regresión a la media: no es que Leipzig sea su «kryptonita». Haaland anota uno por partido contra casi todos.",
            style="cover", method=LEGAL),
        "4-ucl-betis-dortmund": slide(1, 7, "Champions · Jornada 4 · Miércoles 4 de noviembre · 14:00 CDMX",
            "Betis ganó sus 3 partidos, los 3 por un gol. Sus números daban 5.5 puntos, no 9",
            [Matchup("Betis", "3-0-0", "Dortmund", "2-0-1", sep="visita al · Dortmund, 4 de 4 en casa ante españoles en Europa"),
             Stats([("1 en 6", "chance de 9 de 9, nuestro modelo", AMBER),
                    ("+3.5", "puntos por encima de lo esperado", ACC),
                    ("53%", "gana Dortmund (46–59%)", GHOST)])],
            takeaway="3-2, 3-2 y 1-0: ganar siempre por la mínima rara vez dura. ¿Betis es candidato o viene la regresión?",
            style="cover", method=LEGAL),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok")
