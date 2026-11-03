"""xGol — portadas de las 4 ideas del 3 nov (para mié 4 nov). Diseño v7.
NBA: Modelo NBA v1 reconstruido (studio/models/nba_ridge_1103.py): ridge λ=16 sobre puntos 2026-27 (107 partidos,
Land of Basketball, al 2 nov) con prior = 90% del nivel 2025-26 por récord; σ=14.7. Validación fuera de muestra
(día a día, n=91): 67% aciertos, Brier 0.218 vs 0.25 (moneda). Rangos 10–90% por bootstrap (400).
UCL: Modelo xGol UCL v0 (studio/models/ucl_model_v0.py). Como: ajustado sin sus 3 partidos → 3.74 goles esperados;
P(≥10 | Poisson) = 0.0052. Cálculos en el scratchpad de la sesión (calc_1103.py, como.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1103")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta."
LEGAL_UCL = "Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta."


def covers():
    return {
        "1-nba-phi-det": slide(1, 7, "NBA · Miércoles 4 de noviembre · 18:00 CDMX",
            "Philadelphia va 7-1, aunque por sus partidos esperaba 4.6. Detroit gana 2 de cada 3",
            [Matchup("76ers", "7-1", "Pistons", "6-1", sep="visitan a los · Pistons, que ganaron el 1.er duelo 106-93"),
             Stats([("68%", "gana Detroit, nuestro modelo (62–74%)", GHOST),
                    ("+11.6", "diferencia por partido de Detroit (Phila.: +5.8)", ACC),
                    ("1 en 13", "chance de ir 7-1 con la de cada partido", AMBER)])],
            takeaway="Los dos mejores récords del Este. Uno gana cerrado, el otro aplasta. ¿Cuál récord es real?",
            style="cover", method=LEGAL_NBA),
        "2-nba-por-phx": slide(1, 7, "NBA · Miércoles 4 de noviembre · 20:00 CDMX",
            "Portland va 5-1 y gana por 10.8. Nuestro modelo le cree 1 de cada 4 de esos puntos",
            [Matchup("Trail Blazers", "5-1", "Suns", "1-4", sep="visitan a los · Suns; Portland va 4-0 de visita"),
             Stats([("56%", "gana Portland, nuestro modelo (44–67%)", GHOST),
                    ("p = 0.09", "¿mejor que el año pasado? Indicio, no prueba", AMBER),
                    ("49", "victorias proyectadas (41–56)", ACC)])],
            takeaway="Regresión a la media: tras 6 partidos, el arranque pesa ~27%. ¿Portland es candidato o viene la regresión?",
            style="cover", method=LEGAL_NBA),
        "3-nba-noche": slide(1, 7, "NBA · Miércoles 4 de noviembre · desde las 18:00 CDMX",
            "Noche de 14 partidos: ¿cuántos favoritos van a caer?",
            [Hero("1 en 413", "chance de que ganen los 14 favoritos de nuestro modelo", ACC, maxsize=260),
             Stats([("9.2", "favoritos ganan en promedio (7–11)", GHOST),
                    ("67%", "aciertos fuera de muestra (91 partidos)", ACC),
                    ("3", "volados: 52%, 54% y 56%", AMBER)])],
            takeaway="Probabilidad compuesta: 14 chances multiplicadas. Ojo: Oklahoma City sin Holmgren ni J. Williams; el modelo no ve bajas.",
            style="cover", method=LEGAL_NBA),
        "4-ucl-lens-como": slide(1, 7, "Champions · Jornada 4 · Miércoles 4 de noviembre · 14:00 CDMX",
            "Como, debutante: 10 goles en 3 partidos. Con su nivel previo, eso pasa 1 vez en 190",
            [Matchup("Como", "2-0-1", "Lens", "1-0-2", sep="visita al · Lens: 16 partidos de Champions recibiendo gol"),
             Stats([("43%", "gana Como, modelo xGol (31–51%)", GHOST),
                    ("3.7", "goles esperados en esos 3 partidos", ACC),
                    ("15%", "chance de que Lens no reciba gol", AMBER)])],
            takeaway="Prueba de Poisson: p = 0.005. Pero entre 36 clubes, alguno así sale 17% de las veces. Y sin Kean. ¿Real o racha?",
            style="cover", method=LEGAL_UCL),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok")
