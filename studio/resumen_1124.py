"""xGol — Resumen del lunes 23 nov: 2 partidos con probabilidad fijada ANTES (portadas_1123 ideas 1–2, commit 2620921; no publicadas: sin aprobar).
Cálculo: studio/models/resumen_1124.py. 1 de 2 (esperados 1.49; P(≤1) = 0.46). Brier 0.214 (esperado 0.177, 80%: 0.08–0.43; p = 0.46).
CIN 64% → Commanders 22-20 (FG de 26 yd de Drew Stevens en la última jugada; NFL.com, NBC). SAS 86% → Spurs 123-107 sin Wembanyama ni Fox (ESPN)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1124")
K = "Resumen · NFL y NBA · Lunes 23 de noviembre"
METHOD = ("Método: probabilidades fijadas antes de cada partido. NFL: Modelo NFL v0-b (diferencia de puntos por partido, encogida a la mitad, +1.5 de localía). "
          "NBA: Modelo NBA v1 (margen ajustado por rival, encogido al nivel previo; no ve bajas, por eso publicamos escenarios). Error (Brier) = promedio de "
          "(probabilidad − resultado)²; volado = 0.25. p = probabilidad de una noche igual o peor por azar si nuestras probabilidades fueran correctas "
          "(200,000 noches simuladas). Resultados: NFL.com, NBC Sports, ESPN, Sky Sports. Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta.")


def R():
    T = 4
    return [
        slide(1, T, K, "Lunes: 1 de 2. Washington lo ganó en la última jugada",
              [Results([(False, "Commanders 22 · Bengals 20", "Cincinnati 64%"),
                        (True, "Spurs 123 · Kings 107", "San Antonio 86%")]),
               Stats([("1 de 2", "aciertos; esperábamos 1.5", AMBER),
                      ("1 en 2", "noches salen así o peor por azar", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Porcentaje = lo que le dimos a nuestro favorito antes del partido.",
              style="cover", title_size=58),
        slide(2, T, "Las dos historias", "Un gol de campo nos tumbó. Los Spurs ganaron sin sus dos estrellas",
              [Table(("Le dimos", "Así fue"),
                     [("Cincinnati gana en Washington", "64%", "20-22"),
                      ("Margen de Cincinnati", "+4.7", "−2"),
                      ("San Antonio gana en Sacramento", "86%", "123-107"),
                      ("Margen de San Antonio", "+15.6", "+16")], colors=[ACC, GHOST]),
               Stats([("5 de 5", "goles de campo del novato Drew Stevens", NEG),
                      ("46 s", "quedaban cuando Cincinnati se puso arriba 20-19", GHOST),
                      ("0", "minutos de Wembanyama y Fox", ACC)])],
              takeaway="Sin Wembanyama ni Fox, San Antonio quedaba en 76%. Ganó por 16, casi el margen que esperábamos con ellos.",
              title_size=50),
        slide(3, T, "Lo que probamos · Calibración", "Una derrota por 2 puntos no dice que el modelo esté mal",
              [Tests([(True, "El error de la noche cabe en lo normal",
                       "0.21 de error en 2 partidos; con nuestras probabilidades, 1 de cada 2 noches sale igual o peor.",
                       "Brier 0.214 vs 0.177 esperado (80%: 0.08–0.43) · p = 0.46 · n = 2"),
                      (True, "Cincinnati: fallamos por 6.7 puntos de margen",
                       "Un partido de NFL se desvía 13.5 puntos en promedio; 6.7 es menos de la mitad de eso.",
                       "error −6.7 · z = −0.50 · P(error así o mayor) = 0.62"),
                      (True, "Los escenarios con bajas sirven",
                       "Avisamos que Wembanyama y Fox estaban en duda y calculamos 76% sin ellos. No jugaron y San Antonio ganó.",
                       "escenario −5 puntos · 76% · resultado +16")])],
              takeaway="Con 2 partidos no se concluye nada. Por eso sumamos noche tras noche y lo medimos aquí.",
              title_size=52),
        slide(4, T, "Lo que aprendimos", "Perder en la última jugada también se cuenta",
              [Bullets(["1 de 2; esperábamos 1.5. Pasa 1 de cada 2 noches.",
                        "Washington ganó con gol de campo en la última jugada.",
                        "San Antonio ganó por 16 sin Wembanyama ni Fox.",
                        "Error 0.21 (volado = 0.25): dentro de lo esperado."])],
              takeaway="¿Daniels ya es el QB que Washington esperaba?",
              style="end", method=METHOD, title_size=64),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
