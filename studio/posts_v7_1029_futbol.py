"""xGol — 29 oct · Fiorentina vs. Atalanta (Serie A), diseño v7. Estilos de juego + matchup + pruebas."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/fut")


def G():
    T = 7
    return [
        slide(1, T, "Futbol · Serie A (Italia) · Jueves 29 de octubre", "Fiorentina vs. Atalanta: la defensa más goleada de Italia contra el equipo de los partidos locos",
              [Matchup("Fiorentina", "18°", "Atalanta", "11°", sep="local · jueves 29 oct · 13:45 hora CDMX · visita")],
              takeaway="Sus partidos promedian 3.5 goles. ¿Lluvia de goles en Florencia? 4 datos.", style="cover", title_size=80),
        slide(2, T, "El cambio de estilo de Atalanta", "Atalanta cambió de estilo… y sus partidos se volvieron locos",
              [Hero("3.6", "goles por partido en los juegos de Atalanta esta temporada.", ACC),
               Stats([("2.3", "goles por partido en sus juegos de 2025-26", GHOST), ("15", "goles recibidos en 8 partidos", NEG)])],
              takeaway="Llegó Maurizio Sarri: posesión y defensa de 4, después de años con la defensa de 3 y la presión hombre a hombre de la era Gasperini (2016–2025). Todavía no se acomoda.", tag="DATO 1 DE 4"),
        slide(3, T, "La crisis de Fiorentina", "Fiorentina: la defensa más goleada de la Serie A",
              [Hero("19", "goles recibidos en 8 partidos, la peor marca de Italia.", NEG),
               Stats([("9", "partidos seguidos recibiendo gol", NEG), ("7", "partidos en casa sin ganar", NEG), ("1-1-6", "ganados, empatados y perdidos", GHOST)])],
              takeaway="Ya cambió de técnico (salió Grosso, volvió Vanoli) y contra el Inter perdió con dos goles en tiempo de compensación.", tag="DATO 2 DE 4"),
        slide(4, T, "El matchup", "Dos defensas en crisis frente a frente",
              [Stats([("4", "derrotas seguidas de Atalanta como visitante", NEG), ("8", "partidos seguidos de Atalanta recibiendo gol", NEG)]),
               Stats([("12 de 12", "partidos en casa contra Atalanta en los que Fiorentina anotó", ACC), ("3.5", "goles esperados entre los dos (nuestro cálculo)", ACC)])],
              takeaway="Atalanta sufre de visita y Fiorentina siempre le anota en casa. Ninguno defiende bien: esperamos goles en las dos porterías.", tag="DATO 3 DE 4"),
        slide(5, T, "¿Quién gana?", "La temporada dice Atalanta; el mercado, Fiorentina",
              [Table(("Temporada", "Mercado"), [("Gana Fiorentina", "33%", "41%"), ("Empate", "22%", "28%"), ("Gana Atalanta", "45%", "31%")], colors=[ACC, GHOST])],
              takeaway="Con lo que llevan este año, Atalanta es mejor. El mercado pesa la localía y la historia: Fiorentina perdió solo 2 de 25 partidos en casa contra Atalanta desde 1994.", tag="DATO 4 DE 4"),
        slide(6, T, "Lo que probamos", "Lo que se sostiene y lo que es mito",
              [Text("Si «p» es menor a 0.05, casi seguro no es casualidad. Corregimos por hacer varias pruebas a la vez.", 27, MUTED),
               Tests([(True, "«Los partidos de Atalanta ahora tienen más goles»", "29 goles en 8 partidos; con su ritmo de 2025-26 se esperaban 18.", "p = 0.013"),
                      (True, "«Fiorentina es fuerte en casa contra Atalanta»", "Real en la historia (2 derrotas en 25 desde 1994), pero son otros jugadores: no lo usamos para predecir.", "p = 0.02"),
                      (True, "«Atalanta está en mala racha de visita»", "4 derrotas seguidas fuera: real, pero con muestra chica. Es un indicio.", "p = 0.015 · indicio")])]),
        slide(7, T, "Conclusión", "Se esperan goles: dos defensas en crisis",
              [Bullets(["Unos 3.5 goles esperados entre los dos.", "Atalanta todavía se acomoda al estilo de Sarri; Fiorentina no deja de recibir goles.", "La temporada dice Atalanta; la historia y el mercado, Fiorentina."])],
              takeaway="¿Gana la historia o la temporada? Te leemos.", style="end",
              method="Método: modelo de goles (Poisson) con goles a favor y en contra de 2026-27 ajustados hacia el promedio de la liga por la muestra corta, + localía; pruebas de Poisson y binomial con corrección por pruebas múltiples; mercado: precios convertidos a probabilidad sin el margen de la casa. Datos públicos al 29 oct (The Stats Zone, Football Whispers). Análisis independiente, no afiliado a la Serie A ni a los clubes. No es recomendación de apuesta."),
    ]


if __name__ == "__main__":
    o = f"{OUT}/G"; os.makedirs(o, exist_ok=True)
    for i, im in enumerate(G(), 1):
        im.save(f"{o}/{i:02d}.png")
    print("ok")
