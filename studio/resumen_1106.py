"""xGol — Resumen del jueves 5 nov: NFL (JAX@BAL, modelo NFL v0) + NBA (MIA@GSW y ORL@PHX, modelo NBA v1).
Predicciones: JAX 73% (portadas_1104.py / models/nfl_jax_bal_1104.py, commit 95ee0d2 del 4 nov); GSW 63% con ajuste por
2ª noche seguida de Miami (portadas_1105.py, 5 nov). ORL@PHX no estuvo en las portadas: se calculó con nba_ridge_1103.py y
solo los 121 partidos previos (al 4 nov) → PHX 53%. Margen esperado NFL: 8.3 (reproducido con pbp semanas 1–8).
Resultados: JAX 33-10 BAL (nflverse games.csv); GSW 120-100 MIA y PHX 117-104 ORL (ESPN y The Sports Encounter, 5 nov).
Acumulado NBA: validación fuera de muestra día por día (M.validate) con 123 partidos → 107 evaluados: 72 aciertos vs 70.1 esperados
(Poisson-binomial P(≥72) = 0.39); Brier 0.216 (80%: 0.198–0.235); Spiegelhalter z = −0.08, p = 0.94; exceso de margen de los
favoritos −1.1 pts (DE 14.3, p = 0.43). Franja 60–70%: 16 de 34 vs 22.2 esperados (P(≤16) = 0.021; no sobrevive a BH con 3 franjas
al nivel de 'prueba' → indicio)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1106")
K = "Resumen · Jueves 5 de noviembre"
METHOD = ("Método: probabilidades calculadas antes de cada partido. NBA: nuestro modelo NBA v1 (ataque y defensa ajustados por rival y "
          "localía; −2.1 pts por jugar 2 noches seguidas). NFL: modelo NFL v0 (puntos por jugada, regresión a la media 50%). "
          "Phoenix–Orlando no estuvo en nuestras portadas: lo calculamos con los datos previos al partido. Brier = error promedio, "
          "menos es mejor (volado: 0.25). Calibración: prueba de Spiegelhalter; aciertos esperados: Poisson-binomial. "
          "Resultados: nflverse, ESPN, The Sports Encounter. Datos NFL: nflverse. "
          "Análisis independiente, no afiliado a la NFL, la NBA ni los equipos. No es recomendación de apuesta.")


def R():
    T = 5
    return [
        slide(1, T, K, "Jueves: ganaron los 3 favoritos. Y por mucho más de lo esperado",
              [Hero("3 de 3", "favoritos de nuestros modelos ganaron (NFL y NBA). La suma de sus probabilidades daba 1.9.", ACC),
               Stats([("0.14", "error de la noche (Brier). Un volado: 0.25", ACC),
                      ("+14", "puntos promedio por encima del margen esperado", AMBER),
                      ("1 de 4", "noches salen 3 de 3 con esas probabilidades", GHOST)])],
              takeaway="Lo publicamos igual cuando fallamos. Hoy salió bien: aquí está cuánto fue mérito y cuánto ruido.", style="cover",
              title_size=76),
        slide(2, T, "Los 3 partidos", "Jacksonville, Golden State y Phoenix: los tres cumplieron",
              [Results([(True, "Jaguars 33-10 Ravens", "Jacksonville 73%"),
                        (True, "Heat 100-120 Warriors", "Golden State 63%"),
                        (True, "Magic 104-117 Suns", "Phoenix 53%")]),
               Table(("Esperado", "Real"),
                     [("Jacksonville (NFL)", "+8.3", "+23"),
                      ("Golden State (NBA)", "+4.9", "+20"),
                      ("Phoenix (NBA)", "+1.2", "+13")], colors=[GHOST, ACC])],
              takeaway="Miami jugaba su 2ª noche seguida: el ajuste por cansancio subió a Golden State de 58% a 63%. Ganó por 20.",
              title_size=70),
        slide(3, T, "Regresión a la media", "¿Nos quedamos cortos con los favoritos? En 107 partidos, no",
              [Stats([("+14", "puntos de más, en promedio, el jueves (3 partidos)", AMBER),
                      ("−1.1", "puntos vs. lo esperado en 107 partidos NBA", ACC),
                      ("±14", "puntos: lo que se desvía un partido normal", GHOST)]),
               Tests([(True, "Un jueves no cambia el modelo",
                       "Cada margen quedó a una desviación típica de lo esperado: algo normal en un solo partido. En el acumulado, los favoritos ganan por lo que dijimos.",
                       "Exceso del favorito: −1.1 pts · DE 14.3 · p = 0.43 · n = 107")])],
              takeaway="Lección: no inflar a los favoritos por una noche de palizas.", title_size=70),
        slide(4, T, "Calibración · NBA · 107 partidos fuera de muestra", "Cuando decimos 70%, ¿gana 7 de cada 10? En conjunto, sí",
              [Table(("Esperábamos", "Ganaron"),
                     [("Favoritos 50–60% (39)", "21.8", "28"),
                      ("Favoritos 60–70% (34)", "22.2", "16"),
                      ("Favoritos 70%+ (34)", "26.1", "28")], colors=[GHOST, ACC]),
               Tests([(True, "Probabilidades bien calibradas", "72 aciertos contra 70.1 esperados; error 0.216 (un volado: 0.25).",
                       "Spiegelhalter z = −0.08, p = 0.94 · Brier 0.216 (80%: 0.198–0.235)"),
                      (None, "La franja de 60–70%, floja", "Ganaron 16 de 34. Con n tan chico es un indicio, no una prueba.",
                       "Poisson-binomial P(≤ 16) = 0.021 · sin corrección por pruebas múltiples")])],
              takeaway=None, title_size=66),
        slide(5, T, "Lo que aprendimos", "Buena noche, con los pies en la tierra",
              [Bullets(["3 de 3 favoritos ganaron; esperábamos 1.9.",
                        "Error de la noche: 0.14 (un volado: 0.25).",
                        "Las palizas fueron ruido: en 107 partidos, los márgenes cuadran.",
                        "Acumulado NBA: 72 de 107, calibrado (p = 0.94)."])],
              takeaway="¿Cuál de los tres te sorprendió más? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
