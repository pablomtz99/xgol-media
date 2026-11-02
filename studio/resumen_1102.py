"""xGol — Resumen del fin de semana de clásicos (sáb 31 oct – dom 1 nov). Diseño v7.
Lo publicado: post «fin de semana de los clásicos» (29 oct) y «Boca-River» (31 oct). No hubo posts el 1 nov.
Fuentes de resultados: FC Bayern (2-2), The Analyst/Opta (Milan 3-1), Claro Sports (América 2-2),
Sky Sports / Football365 (Liverpool 0-1), El Intransigente / Perfil (Boca 1-0)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1102")


def R():
    T = 6
    return [
        slide(1, T, "Resumen · fin de semana de clásicos", "Dijimos que en los clásicos se empata más. Hubo 2 de 5",
              [Hero("2 de 5", "clásicos terminaron empatados: Bayern-Dortmund y América-Toluca.", ACC),
               Stats([("31.5%", "empates en 514 clásicos (lo que publicamos)", GHOST),
                      ("40%", "empates este fin de semana (n = 5)", ACC),
                      ("1 de 1", "favorito acertado: Boca", ACC)])],
              takeaway="Lo publicamos siempre: lo que salió, lo que no y qué tan lejos estuvimos.", style="cover"),
        slide(2, T, "Superclásico · domingo", "Boca 1-0 River: el favorito que mostramos ganó",
              [Table(("Dijimos", "Resultado"), [("Boca gana en la Bombonera", "42%", "1-0")], colors=[GHOST, ACC]),
               Stats([("27'", "gol de Di Lollo, de cabeza tras córner", ACC),
                      ("9", "jugadores terminó River: 2 expulsados", GHOST),
                      ("3", "Superclásicos seguidos para Boca (no pasaba desde 1991)", GHOST)])],
              takeaway="La revancha del 1-0 del Apertura no llegó: otro 1-0. River jugó con 10 desde el minuto 10."),
        slide(3, T, "Los otros 4 clásicos", "Lo que esperábamos vs. lo que pasó",
              [Tests([(False, "Bayern 2-2 Dortmund", "Historial de goles 231 a 141 para Bayern… y Dortmund empató en el 89'. Siguen igualados arriba e invictos.", "Laimer 38', Guirassy 60', Upamecano 66', Fábio Silva 89'"),
                      (True, "Milan 3-1 Inter", "Dijimos que la ventaja histórica de Inter cabía en el azar. Milan ya suma 3 victorias seguidas en liga contra Inter.", "Pulisic, Rabiot, Moreira (tiro libre) · Bastoni"),
                      (True, "América 2-2 Toluca", "Empate de clásico: dos goles en los últimos 3 minutos y dos expulsados.", "Henry Martín 62' y 89' (penal) · Viñas 42' y gol de Toluca al 87'"),
                      (True, "Liverpool 0-1 Arsenal", "Dijimos que ganar en Anfield lo dejaba líder solo: ya está 3 puntos arriba del City.", "Havertz 16' · Liverpool: 0 tiros a puerta en casa")])],
              takeaway="La «excepción alemana» no se sostuvo esta vez: Dortmund rescató el empate en el 89'."),
        slide(4, T, "¿Qué tan lejos estuvimos?", "Superclásico: la probabilidad que mostramos le ganó al azar",
              [Stats([("0.51", "error de la probabilidad que mostramos (Brier: menos es mejor)", ACC),
                      ("0.67", "lo que da poner 1/3 a cada resultado", GHOST),
                      ("0.63", "lo que daba usar solo el historial (94-84-88)", GHOST)]),
               Tests([(True, "Boca era favorito y ganó", "Mostramos 42% (mercado sin margen): gana algo más de 2 de cada 5 veces. Pasó.", "Brier = (1−0.42)² + 0.31² + 0.27² = 0.51 · n = 1")])],
              takeaway="Un solo partido no califica a nadie: lo medimos en el acumulado, en público."),
        slide(5, T, "Calibración", "¿2 empates de 5 confirma o desmiente lo de los clásicos?",
              [Stats([("1.6", "empates esperados (tasa de clásicos)", GHOST),
                      ("2", "empates reales", ACC),
                      ("50%", "de los fines de semana: 2 o más", GHOST)]),
               Tests([(True, "Coincide con lo esperado", "Con 31.5% de empates, ver 2 o más en 5 partidos pasa 1 de cada 2 veces.", "Binomial · P(X ≥ 2 | n = 5, p = 0.315) = 0.50")])],
              takeaway="Pero 5 partidos no prueban nada: con la tasa normal (26%) pasa 39 de cada 100. La prueba válida sigue siendo la de 514 clásicos (p = 0.003)."),

        slide(6, T, "Lo que aprendimos", "Los clásicos cumplieron con su fama",
              [Bullets(["Empates: 2 de 5 (40%), dentro de lo esperado para clásicos.",
                        "Boca, el favorito que mostramos, ganó 1-0 con River en 9.",
                        "Arsenal ganó en Anfield y quedó líder solo, como planteamos.",
                        "La falla: Bayern no impuso su historial; Dortmund empató en el 89'."])],
              takeaway="¿Cuál clásico te sorprendió más? Te leemos.", style="end",
              method="Método: tasas y probabilidades publicadas antes de cada partido (posts del 29 y 31 oct). Brier de 3 resultados = suma de (probabilidad − resultado)². Binomial con n = 5. Resultados: FC Bayern, Opta/The Analyst, Claro Sports, Sky Sports, El Intransigente. Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta."),
    ]


if __name__ == "__main__":
    o = f"{OUT}/R"; os.makedirs(o, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{o}/{i:02d}.png")
    print("ok")
