"""xGol — Resumen del domingo 22 nov: 9 partidos con probabilidades fijadas ANTES (portadas_1121 ideas 1–3, commit ee90b02; portadas_1122 ideas 1, 3, 4,
commit ca3e0b7; no publicados: sin aprobar). Cálculo: studio/models/resumen_1123.py.
Noche: 4 de 9 (esperados 5.18; P(≤4) = 0.32). NFL 3 de 4 (esp 2.49); NBA 0 de 2 (esp 1.16; P = 0.18); futbol 1 de 3 (esp 1.54).
Brier binario 0.249 (esperado si calibrado 0.237, 80%: 0.18–0.30; p = 0.41; Spiegelhalter p = 0.79). Brier futbol 3 res 0.788 (esp 0.615; p = 0.14).
Futbol 21+22 nov (n = 6): Brier 0.796 vs 0.625 esperado, p = 0.047 (una sola prueba sin corregir → indicio); aciertos 1 vs 2.95 (P(≤1) = 0.12).
Thunder sin Gilgeous-Alexander (ESPN; 7 bajas ya señaladas en la portada del 22). Liderato: Cruz Azul 54% → Chivas superlíder (46%)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1123")
K = "Resumen · NFL, NBA y futbol · Domingo 22 de noviembre"
METHOD = ("Método: probabilidades fijadas antes de cada partido. NFL: Modelo NFL v0 (puntos que suma cada jugada, con localía). NBA: Modelo NBA v1 (calidad por "
          "margen ajustado por rival, encogida al nivel previo; no ve bajas). Futbol: Modelo xGol v0 (diferencia de goles encogida, Poisson, localía). "
          "Error (Brier) = promedio de (probabilidad − resultado)²; volado = 0.25; en futbol, 3 resultados con 1/3 c/u = 0.67. p = probabilidad de una noche "
          "igual o peor por azar si las probabilidades fueran correctas (simulación de 200,000 noches). Resultados: ESPN, CBS, NBA.com, Sky Sports, Claro Sports, "
          "LaPresse. Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta.")


def R():
    T = 5
    return [
        slide(1, T, K, "Domingo: 4 de 9. 3 de 4 en la NFL, 0 de 2 en la NBA",
              [Results([(True, "Bears 21 · Saints 13", "66%"), (True, "Broncos 38 · Raiders 24", "64%"),
                        (True, "Lions 31 · Buccaneers 21", "57%"), (False, "Eagles 19 · Steelers 16", "Pittsburgh 62%"),
                        (False, "Heat 123 · Thunder 113", "Oklahoma City 62%"), (False, "Warriors 88 · Celtics 87", "Boston 54%"),
                        (True, "Chivas 1 · Cruz Azul 0", "Chivas 46%"), (False, "Atalanta 4 · Inter 4", "Inter 53%"),
                        (False, "Hull 2 · Brighton 0", "Brighton 55%")]),
               Stats([("4 de 9", "aciertos; esperábamos 5.2", AMBER),
                      ("1 en 3", "noches salen así o peor por azar", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Porcentaje = lo que le dimos a nuestro favorito antes del partido.",
              style="cover", title_size=56),
        slide(2, T, "Lo que salió", "Chivas superlíder y 3 de 4 en la NFL",
              [Table(("Le dimos", "Así fue"),
                     [("Chivas gana en casa", "46%", "1-0"),
                      ("Chicago vs N. Orleans", "66%", "21-13"),
                      ("Denver vs Las Vegas", "64%", "38-24"),
                      ("Detroit vs Tampa Bay", "57%", "31-21")], colors=[ACC, ACC]),
               Stats([("46%", "le dábamos a Chivas; es superlíder por 1a vez desde 2011", ACC),
                      ("8-2", "Chicago, Denver y Detroit tras el domingo", GHOST)])],
              takeaway="Efraín Álvarez anotó al 21'. Chivas va contra Pachuca en cuartos; Cruz Azul, contra León.",
              title_size=58),
        slide(3, T, "Las 5 sorpresas", "Lo que pasó tenía entre 22% y 46% en nuestras cuentas",
              [Table(("Le dimos", "Así fue"),
                     [("Miami gana en casa", "38%", "123-113"),
                      ("Golden State gana", "46%", "88-87"),
                      ("Filadelfia gana", "38%", "19-16"),
                      ("Empate Atalanta–Inter", "22%", "4-4"),
                      ("Hull gana en casa", "22%", "2-0")], colors=[AMBER, NEG]),
               Stats([("0", "minutos de Gilgeous-Alexander", NEG),
                      ("2", "goles de Hull, ambos en el descuento", GHOST),
                      ("1", "punto decidió en San Francisco", GHOST)])],
              takeaway="Ya avisábamos 7 bajas del Thunder y a su figura en duda. Al final no jugó; Adebayo hizo triple-doble.",
              title_size=54),
        slide(4, T, "Lo que probamos · Calibración", "NFL y NBA, dentro de lo esperado. Futbol, una señal a vigilar",
              [Tests([(True, "NFL + NBA: probabilidades bien calibradas",
                       "Error de 0.249 en 6 partidos; si nuestras probabilidades son correctas, lo esperable es 0.24.",
                       "Brier 0.249 vs 0.237 (80%: 0.18–0.30) · p = 0.41 · n = 6"),
                      (True, "Un 4 de 9 cabe en lo normal",
                       "Con estas probabilidades, 4 o menos aciertos salen 1 de cada 3 noches.",
                       "Esperados 5.2 · P(≤4) = 0.32 · n = 9"),
                      (False, "Futbol: dos noches seguidas de error alto ya no parecen solo azar",
                       "Sábado y domingo: 1 de 6, con error de 0.80; por azar pasa 1 de cada 21 veces. Es un indicio, no prueba.",
                       "Brier 0.80 vs 0.63 · p = 0.047 · n = 6 · sin corregir por pruebas múltiples")])],
              takeaway="Revisamos el modelo de futbol: cuánto pesa la localía y cómo reparte el empate. Lo contamos aquí.",
              title_size=52),
        slide(5, T, "Lo que aprendimos", "Una mala noche se mide. No se esconde",
              [Bullets(["Domingo: 4 de 9; esperábamos 5.2. Pasa 1 de cada 3 noches.",
                        "NFL 3 de 4; Chivas superlíder con 46%: nuestro favorito sí ganó.",
                        "Oklahoma City perdió sin Gilgeous-Alexander: el modelo NBA no ve bajas.",
                        "Futbol, 1 de 6 en dos noches (p = 0.047): indicio que ya estamos revisando."])],
              takeaway="¿Quién pasa en cuartos: Chivas o Pachuca?",
              style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
