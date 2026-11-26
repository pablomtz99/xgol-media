"""xGol — Resumen del miércoles 25 nov: 12 partidos con probabilidad fijada ANTES (portadas_1124 ideas 2 y 3, commit 14fdb31; portadas_1125 ideas 2 y 4, commit 4384b92;
no publicadas). Cálculo: studio/models/resumen_1126.py. 4 de 12 (esperados 7.2; P(≤4) = 0.045). UCL 3 de 9 (esp 5.7): 6 sorpresas, P(≥6) = 0.053; publicamos P(≥3) = 71%.
Brier futbol 0.615 (uniforme 0.667; esperado 0.51; p = 0.19). Resultados: Yahoo Sports, Sporting Tribune, La Silla Rota, 365Scores, En Juego, ESPN (AP)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1126")
K = "Resumen · Champions, Liga MX y NBA · Miércoles 25 de noviembre"
METHOD = ("Método: probabilidades fijadas antes de cada partido. Champions: Modelo xGol UCL v0.1 (ataque y defensa por equipo con goles Poisson, 72 partidos de la fase de liga). "
          "Liga MX: Modelo xGol Liga MX v0 (diferencia de goles encogida + localía; Monte Carlo de la serie). NBA: Modelo NBA v1 (margen ajustado por rival; escenario con bajas). "
          "Error (Brier) en futbol = suma de (probabilidad − resultado)² en local/empate/visita; repartir 33% a cada uno da 0.67. p = probabilidad de una noche igual o peor "
          "por azar si nuestras probabilidades fueran correctas (200,000 noches simuladas). Resultados: Yahoo Sports, Sporting Tribune, La Silla Rota, 365Scores, ESPN (AP). "
          "Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta.")


def R():
    T = 5
    return [
        slide(1, T, K, "Miércoles de sorpresas: 4 de 12. Lo publicamos igual",
              [Results([(False, "Brujas 0 · Liverpool 3", "Brujas 47%"),
                        (False, "Lille 2 · Bayern 1", "Bayern 54%"),
                        (False, "Sporting 2 · Man Utd 2", "Sporting 56%"),
                        (False, "Thunder 106 · Wolves 113", "Oklahoma City 53%"),
                        (True, "Toluca 2 · Atlas 0", "Toluca 60%")]),
               Stats([("4 de 12", "aciertos; esperábamos 7.2", NEG),
                      ("1 de cada 22", "noches salen así o peor por azar", AMBER)])],
              takeaway="Porcentaje = lo que le dimos a nuestro favorito antes del partido. Ganemos o perdamos, aquí está.",
              style="cover", title_size=56),
        slide(2, T, "Champions · Jornada 5 · Los 9 partidos del miércoles", "Avisamos 3 sorpresas o más (71%). Hubo 6",
              [Results([(True, "Sabah 1 · Barcelona 4", "Barcelona 87%"),
                        (False, "Slavia 0 · Villarreal 1", "Slavia 42%"),
                        (True, "Atlético 2 · Viking 0", "Atlético 83%"),
                        (False, "Brujas 0 · Liverpool 3", "Brujas 47%"),
                        (True, "Inter 2 · Stuttgart 0", "Inter 73%"),
                        (False, "Lille 2 · Bayern 1", "Bayern 54%"),
                        (False, "PSG 2 · Roma 2", "PSG 76%"),
                        (False, "Shakhtar 0 · Fenerbahçe 1", "Shakhtar 56%"),
                        (False, "Sporting 2 · Man Utd 2", "Sporting 56%")]),
               Stats([("6 de 9", "sorpresas; esperábamos 3.3", NEG),
                      ("1 en 19", "jornadas salen así o peor", AMBER)])],
              takeaway="Bayern jugó sin Kane, Olise, Davies, Gnabry ni Neuer. United iba 2-1 con dos de Bruno y Sporting empató al 80'.",
              title_size=52),
        slide(3, T, "Las historias · Liga MX y NBA", "Toluca ya tiene un pie en semifinales: 85%",
              [Table(("Antes", "Ahora"),
                     [("Toluca avanza (ganó 2-0 la ida)", "61%", "85%"),
                      ("América avanza (0-0 en Monterrey)", "70%", "77%"),
                      ("Margen de Oklahoma City", "+1", "−7")], colors=[GHOST, ACC]),
               Stats([("2", "goles de Helinho en Toluca", ACC),
                      ("10", "jugadores de Monterrey desde la expulsión", AMBER),
                      ("32", "puntos de McDaniels; Minnesota remontó 10", NEG)])],
              takeaway="Atlas necesita ganar por 2 en el Jalisco. América aguantó el 0-0 con un hombre más y define en casa.",
              title_size=52),
        slide(4, T, "Lo que probamos · Calibración", "Noche rara, pero el error en futbol quedó bajo el de repartir parejo",
              [Tests([(False, "Los aciertos cupieron en lo normal",
                       "4 de 12 cuando esperábamos 7.2. Con nuestras probabilidades, sale así o peor 1 de cada 22 noches.",
                       "P(≤4 aciertos) = 0.045 · n = 12"),
                      (True, "En futbol fuimos mejores que repartir 33% a cada resultado",
                       "Error de 0.62 contra 0.67 de repartir parejo. Peor de lo esperado (0.51), pero cabe en el azar.",
                       "Brier 0.615 · esperado 0.51 · p = 0.19 · n = 11"),
                      (None, "Los resultados poco probables salieron un poco más de lo dicho",
                       "A lo que dimos 39% en promedio pasó 50% de las veces; a lo que dimos 66%, 44%. Con 35 resultados es solo un indicio.",
                       "tramos 0–25%: 16% vs 22% · 25–50%: 39% vs 50% · 50%+: 66% vs 44%")])],
              takeaway="Una noche no cambia el modelo; la seguimos sumando al registro y la revisamos cada semana.",
              title_size=46),
        slide(5, T, "Lo que aprendimos", "Cuando avisamos sorpresas, hay que creerle al aviso",
              [Bullets(["4 de 12; esperábamos 7.2. Pasa 1 de cada 22 noches.",
                        "Champions: 6 sorpresas cuando dijimos 3 o más.",
                        "En futbol, aun así, mejor que repartir parejo.",
                        "Toluca 85% y América 77% para semifinales."])],
              takeaway="¿Lille a Bayern fue la sorpresa de la jornada o lo fue Brujas 0-3?",
              style="end", method=METHOD, title_size=60),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
