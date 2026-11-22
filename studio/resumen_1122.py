"""xGol — Resumen del sábado 21 nov: 3 partidos de futbol con probabilidades fijadas ANTES (portadas_1120 ideas 3 y 4, commit 9a28c51; portadas_1121 idea 4,
commit ee90b02; no publicados: sin aprobar). Cálculo: studio/models/resumen_1122.py.
Resultados: Pumas 0-2 Monterrey en CU (Bolavip; Noticias MXM: Orellano 74' y 90+1'); Newcastle 2-2 Arsenal (ESPN UK: Eze 33', Barnes 49', Thiaw 62', Madueke 78';
titulares Arseblog y arsenal.com); Tigres 1-0 América (Noticias MXM: Brunetta 90'; titulares Heraldo de México y SDP Noticias).
Noche: 0 de 3; esperados 1.41; P(0 de 3) = 0.147. Brier 3 resultados 0.805 (uniforme 0.667; esperado si calibrado 0.634, 80%: 0.425–0.805; P(≥obs) = 0.10).
Prob. media dada al resultado real 0.281. Cumplido: MTY a Liguilla (69.5%; 100% si ganaba), Pumas fuera (8.4%). América líder: 35.9% → 0.
Sin xgol-data ni nflverse (acceso a esos repos no habilitado en esta ejecución): sin acumulados."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1122")
K = "Resumen · Futbol · Sábado 21 de noviembre"
METHOD = ("Método: Modelo xGol Liga MX v0 y Europa v0 = fuerza por diferencia de goles (encogida), goles con Poisson y localía; probabilidades fijadas antes "
          "de los partidos. Brier de 3 resultados = suma de (probabilidad − resultado)²; repartir 1/3 a cada resultado da 0.67. Aciertos esperados = suma de las "
          "probabilidades de cada favorito. Resultados: ESPN, Bolavip, Noticias MXM, Heraldo de México. Análisis independiente, no afiliado a ninguna liga. "
          "No es recomendación de apuesta.")


def R():
    T = 5
    return [
        slide(1, T, K, "Sábado: 0 de 3. Ningún favorito nuestro ganó",
              [Results([(False, "Pumas 0 · Monterrey 2", "Pumas 42%"), (False, "Newcastle 2 · Arsenal 2", "Arsenal 47%"),
                        (False, "Tigres 1 · América 0", "América 52%")]),
               Stats([("0 de 3", "aciertos; esperábamos 1.4", NEG),
                      ("1 en 7", "veces que pasa un 0 de 3 con estas probabilidades", AMBER)])],
              takeaway="Lo publicamos ganemos o perdamos. En futbol, un favorito de 45% pierde o empata más de la mitad de las veces.",
              style="cover", title_size=62),
        slide(2, T, "Las 3 sorpresas", "Lo que pasó tenía entre 25% y 34% en nuestras cuentas",
              [Table(("Le dimos", "Así fue"),
                     [("Monterrey gana en CU", "34%", "0-2"),
                      ("Empate en Newcastle", "25%", "2-2"),
                      ("Tigres le gana a América", "25%", "1-0")], colors=[AMBER, NEG]),
               Stats([("28%", "probabilidad promedio que le dimos a lo que pasó", AMBER),
                      ("2 de 3", "se decidieron del minuto 78 en adelante", GHOST)])],
              takeaway="Orellano anotó al 74' y al 90+1'; Madueke empató al 78'; Brunetta le dio el 1-0 a Tigres al 90'.",
              title_size=56),
        slide(3, T, "Lo que sí se cumplió", "Las cuentas de la tabla sí salieron",
              [Table(("Le dimos", "Así fue"),
                     [("Monterrey a Liguilla", "70%", "Sí"),
                      ("Pumas a Liguilla", "8%", "Fuera"),
                      ("América termina líder", "36%", "Ya no")], colors=[ACC, GHOST]),
               Stats([("54%", "Cruz Azul termina 1° tras la derrota de América (hoy vs Chivas)", ACC),
                      ("+6", "Arsenal sigue líder de la Premier tras el 2-2", GHOST)])],
              takeaway="Hoy en Guadalajara se decide el 1°: a Cruz Azul le basta el empate; Chivas necesita ganar.",
              title_size=58),
        slide(4, T, "Lo que probamos · Calibración", "Mala noche, pero no prueba que las probabilidades estén mal",
              [Tests([(True, "Un 0 de 3 cabe en lo esperable",
                       "Con 42%, 47% y 52%, el 0 de 3 sale 1 de cada 7 noches; el 1 de 3 es lo más común.",
                       "P(0) = 15% · P(1) = 40% · P(2) = 36% · P(3) = 10%"),
                      (False, "Nuestras probabilidades están descalibradas",
                       "El error de la noche (0.81) es alto, pero 1 de cada 10 noches así sale por azar.",
                       "Brier 0.81 vs 0.63 esperado (80%: 0.43–0.81) · p = 0.10 · n = 3"),
                      (True, "En futbol, el favorito suele no ganar",
                       "Nuestros tres favoritos tenían menos de 53%: era más probable que fallara al menos uno.",
                       "P(al menos una sorpresa) = 90%")])],
              takeaway="Con 3 partidos, una noche es una pista, no un veredicto. Seguimos midiendo.",
              title_size=54),
        slide(5, T, "Lo que aprendimos", "Una probabilidad de 45% también avisa que vas a fallar seguido",
              [Bullets(["Sábado: 0 de 3; esperábamos 1.4.",
                        "Lo que pasó tenía entre 25% y 34%; dos se definieron del 78' en adelante.",
                        "Las cuentas de tabla sí salieron: Monterrey a Liguilla, Pumas fuera.",
                        "Error de la noche: 0.81, alto, pero sin evidencia de descalibración (p = 0.10)."])],
              takeaway="Cruz Azul o Chivas: ¿quién termina primero hoy?",
              style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
