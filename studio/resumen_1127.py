"""xGol — Resumen del jueves 26 nov (Thanksgiving + Liga MX cuartos ida): 5 partidos con probabilidad fijada ANTES (portadas_1124 idea 1; portadas_1125 idea 3;
portadas_1126 idea 2; no publicadas). Cálculo: studio/models/resumen_1127.py. 1 de 5 (esperados 2.6; P(≤1) = 0.15). NFL: perdieron los 3 favoritos (P = 0.065).
Brier NFL 0.355 (moneda 0.25; p = 0.064); futbol 0.54 (parejo 0.667). Resultados: ClickOnDetroit, CBS Texas (AP), Audacy WGR, La Silla Rota, EFE/Infobae; xG León–Cruz Azul: ESPN."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1127")
K = "Resumen · NFL Thanksgiving y Liga MX · Jueves 26 de noviembre"
METHOD = ("Método: probabilidades fijadas antes de cada partido. NFL: Modelo NFL v0 (diferencia de puntos por jugada ofensiva y defensiva, datos nflverse, + localía; "
          "probabilidad = Φ(margen/13.5)). Liga MX: Modelo xGol Liga MX v0 (diferencia de goles encogida + localía; Monte Carlo de la serie, 400,000 vueltas). "
          "Error (Brier): NFL = (probabilidad − resultado)²; una moneda da 0.25. Futbol = suma en local/empate/visita; repartir 33% da 0.67. p = probabilidad de una noche igual "
          "o peor por azar si nuestras probabilidades fueran correctas. Resultados: ClickOnDetroit, CBS Texas (AP), Audacy, La Silla Rota, EFE; xG: ESPN. Datos: nflverse. "
          "Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta.")


def R():
    T = 5
    return [
        slide(1, T, K, "Jueves de remontadas: 1 de 5. Lo publicamos igual",
              [Results([(False, "Bears 39 · Lions 35", "Detroit 56%"),
                        (False, "Eagles 39 · Cowboys 38", "Dallas 70%"),
                        (False, "Chiefs 10 · Bills 13", "Kansas City 51%"),
                        (True, "Pachuca 2 · Chivas 1", "Pachuca 45%"),
                        (False, "León 0 · Cruz Azul 4", "León 39%")]),
               Stats([("1 de 5", "aciertos; esperábamos 2.6", NEG),
                      ("1 de cada 7", "noches salen así o peor por azar", AMBER)])],
              takeaway="Porcentaje = lo que le dimos a nuestro favorito antes del partido. Ganemos o perdamos, aquí está.",
              style="cover", title_size=58),
        slide(2, T, "NFL · Thanksgiving · Los 3 partidos", "Los 3 favoritos cayeron en los últimos 3 segundos",
              [Table(("Dimos", "Final"),
                     [("Detroit vs Chicago · TD de Chicago a 3 s", "56%", "35-39"),
                      ("Dallas vs Philadelphia · gol de campo a 2 s", "70%", "38-39"),
                      ("Kansas City en Buffalo · gol de 57 yd al final", "51%", "10-13")], colors=[GHOST, NEG]),
               Stats([("1 en 16", "jueves en que pierden los 3 favoritos", NEG),
                      ("21", "puntos de ventaja que perdió Dallas", AMBER),
                      ("8", "puntos sumados entre las 3 derrotas", ACC)])],
              takeaway="Philadelphia remontó con Joe Milton de QB (Hurts no jugó). Las 3 derrotas fueron por 4, 1 y 3 puntos.",
              title_size=52),
        slide(3, T, "Las historias · Liga MX, cuartos de final", "Cruz Azul ya casi está en semis: 99.8%",
              [Table(("Antes", "Ahora"),
                     [("Cruz Azul avanza (ganó 4-0 en León)", "67%", "99.8%"),
                      ("Chivas avanza (perdió 2-1 en Pachuca)", "59%", "47%"),
                      ("León necesita ganar por 5 o más", "—", "0.2%")], colors=[GHOST, ACC]),
               Stats([("1.2 vs 1.4", "goles esperados León–Cruz Azul: el 4-0 fue más amplio que el juego", AMBER),
                      ("2", "goles de Idrissi; expulsado, no juega la vuelta", NEG),
                      ("1-0", "le basta a Chivas en el Akron (avanza por ser 1°)", ACC)])],
              takeaway="León tuvo el balón (59%) y 17 tiros, pero solo 1 a puerta. Cruz Azul: 9 a puerta, 4 goles.",
              title_size=52),
        slide(4, T, "Lo que probamos · Calibración", "Noche mala en NFL; en futbol, mejor que repartir parejo",
              [Tests([(True, "1 de 5 cabe en el azar",
                       "Una noche así o peor pasa 1 de cada 7.",
                       "P(≤1 acierto) = 0.15 · n = 5"),
                      (False, "En NFL, peor que lanzar una moneda",
                       "Error 0.36 vs 0.25 de una moneda; pasa 1 de cada 16.",
                       "Brier 0.355 · esperado 0.235 · p = 0.064 · n = 3"),
                      (True, "En futbol, mejor que repartir 33% a cada resultado",
                       "Error 0.54 vs 0.67. En las 4 idas de cuartos: 0.55.",
                       "Brier 0.538 · n = 2 (idas: 0.545, n = 4)"),
                      (None, "Thanksgiving vuelve a castigar al local",
                       "Desde 2010 gana 21 de 50 (42%) vs 55% el resto. Indicio.",
                       "binomial p = 0.064 · 2010–2026")])],
              takeaway="Una noche no cambia el modelo: la sumamos al registro.",
              title_size=44),
        slide(5, T, "Lo que aprendimos", "Tres finales de fotografía y un 4-0 más amplio que el juego",
              [Bullets(["1 de 5; esperábamos 2.6. Pasa 1 de cada 7 noches.",
                        "NFL: los 3 favoritos perdieron en los últimos 3 segundos.",
                        "Cruz Azul 99.8% para semis; Chivas, 47%.",
                        "Thanksgiving: el local gana 42% desde 2010."])],
              takeaway="¿Qué fue más improbable: la remontada de 21 puntos de Philadelphia o el 4-0 en León?",
              style="end", method=METHOD, title_size=58),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
