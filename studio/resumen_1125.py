"""xGol — Resumen del martes 24 nov: 4 partidos con probabilidad fijada ANTES (portadas_1123 idea 3, commit 2620921; portadas_1124 idea 4, commit 14fdb31; no publicadas).
Cálculo: studio/models/resumen_1125.py. 2 de 4 (esperados 2.64; P(≤2) = 0.42). Futbol: Brier 3 resultados 0.84 (uniforme 0.67; esperado 0.49, 80%: 0.16–0.85; p = 0.15).
NBA: DET 62% → 104-86 sin Cunningham (margen esperado +4.4, real +18). Resultados: ESPN, ParisFans, AfricaSoccer, Washington Post (AP), Yahoo Sports."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1125")
K = "Resumen · Champions y NBA · Martes 24 de noviembre"
METHOD = ("Método: probabilidades fijadas antes de cada partido. Champions: Modelo xGol UCL v0.1 (ataque y defensa por equipo con goles Poisson, 72 partidos de la fase de liga). "
          "NBA: Modelo NBA v1 (margen ajustado por rival, encogido al nivel previo; no ve bajas, por eso publicamos escenarios). Error (Brier) en futbol = suma de "
          "(probabilidad − resultado)² en local/empate/visita; repartir 33% a cada uno da 0.67. p = probabilidad de una noche igual o peor por azar si nuestras probabilidades "
          "fueran correctas (200,000 noches simuladas). Resultados: ESPN, AP, Yahoo Sports. Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta.")


def R():
    T = 4
    return [
        slide(1, T, K, "Martes: 2 de 4. Dos empates en Inglaterra nos costaron la noche",
              [Results([(False, "Arsenal 1 · Dortmund 1", "Arsenal 60%"),
                        (False, "Man City 2 · Napoli 2", "Man City 75%"),
                        (True, "Real Madrid 5 · PSV 1", "Real Madrid 68%"),
                        (True, "Pistons 104 · Magic 86", "Detroit 62%")]),
               Stats([("2 de 4", "aciertos; esperábamos 2.6", AMBER),
                      ("4 de 10", "noches salen así o peor por azar", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Porcentaje = lo que le dimos a nuestro favorito antes del partido.",
              style="cover", title_size=56),
        slide(2, T, "Las historias", "Detroit ganó por 18 sin Cunningham. Madrid remontó y goleó",
              [Table(("Le dimos", "Así fue"),
                     [("Arsenal gana a Dortmund", "60%", "1-1"),
                      ("Man City gana a Napoli", "75%", "2-2"),
                      ("Real Madrid gana a PSV", "68%", "5-1"),
                      ("Detroit gana en Orlando", "62%", "104-86"),
                      ("Margen de Detroit", "+4.4", "+18")], colors=[ACC, GHOST]),
               Stats([("54%", "Detroit sin Cunningham (no jugó)", ACC),
                      ("1 en 37", "que Arsenal y City empataran los dos", NEG),
                      ("30%", "que ganaran los 3 locales de Champions", GHOST)])],
              takeaway="PSV anotó primero en Madrid y terminó perdiendo 5-1. Orlando, que ya era 1-5 en casa, ahora es 1-6.",
              title_size=50),
        slide(3, T, "Lo que probamos · Calibración", "Mala noche en futbol, pero todavía dentro de lo que el azar explica",
              [Tests([(True, "Los aciertos caben en lo normal",
                       "2 de 4 cuando esperábamos 2.6: con nuestras probabilidades, 4 de cada 10 noches salen igual o peor.",
                       "P(≤2 aciertos) = 0.42 · n = 4"),
                      (False, "En futbol erramos más que repartir a partes iguales",
                       "Los dos empates pesan mucho: el error fue 0.84 cuando 33% a cada resultado da 0.67.",
                       "Brier 0.84 vs 0.49 esperado (80%: 0.16–0.85) · p = 0.15 · n = 3"),
                      (True, "El escenario sin Cunningham sirvió",
                       "Avisamos que estaba en duda y calculamos 54% sin él. Fue baja de último momento y Detroit ganó por 18.",
                       "escenario −3 puntos · 54% · resultado +18")])],
              takeaway="Una noche así pasa 15 de cada 100 veces en futbol. Por eso sumamos noche tras noche y lo medimos aquí.",
              title_size=48),
        slide(4, T, "Lo que aprendimos", "Los empates también se cuentan",
              [Bullets(["2 de 4; esperábamos 2.6. Pasa 4 de cada 10 noches.",
                        "Arsenal y City empataron en casa: 1 en 37.",
                        "Real Madrid remontó y le metió 5 al PSV.",
                        "Detroit ganó por 18 sin Cunningham."])],
              takeaway="¿El empate en casa ya es tendencia para Arsenal y City o fue una noche rara?",
              style="end", method=METHOD, title_size=64),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
