"""xGol — Resumen del viernes 6 nov: los 9 partidos NBA de la noche con el modelo NBA v1 (nba_ridge_1103.py).
Predicción publicada en portada (portadas_1106.py): LAL 58% vs POR. Los otros 8 partidos NO estuvieron en portadas: se
calcularon con el mismo modelo y SOLO los 123 partidos previos (al 5 nov), sin tocar parámetros. Se incluye la noche completa
(no se eligieron partidos). Rangos 10–90% por bootstrap (400) del modelo.
Resultados: Land of Basketball (scores 2026-27, 8 partidos) y ESPN/Yahoo Sports (LAL 124-118 POR; Dončić 53 pts; LAL perdía 60-53 al medio).
Noche: 9 de 9 vs 6.12 esperados; Poisson-binomial P(9 de 9) = 0.029 (1 en 34); Brier 0.109. Exceso de margen del favorito +10.1 pts.
Acumulado (validación fuera de muestra día por día, M.validate): 116 partidos, 81 aciertos vs 76.2 esperados (P(≥81)=0.20);
Brier 0.208 (80%: 0.191–0.226); Spiegelhalter z=−0.63, p=0.53; exceso de margen del favorito −0.2 pts (DE 14.5, t p=0.87).
Franjas: 50–60%: 30 de 41 vs 23.0 (P(≥30)=0.018); 60–70%: 20 de 38 vs 24.9 (P(≤20)=0.068); 70%+: 31 de 37 vs 28.3.
BH con 3 franjas: 0.018×3 = 0.054 > 0.05 → indicio, no prueba. Código de cálculo: scratch res.py/cum.py (mismo modelo)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1107")
K = "Resumen · NBA · Viernes 6 de noviembre"
METHOD = ("Método: nuestro modelo NBA v1 (ataque y defensa ajustados por rival y localía, regresión ridge hacia la temporada pasada). "
          "Lakers–Portland fue nuestra portada; los otros 8 partidos los calculamos con los mismos parámetros y solo con datos previos "
          "a la noche: es la jornada completa, sin elegir partidos. Brier = error promedio, menos es mejor (volado: 0.25). "
          "Aciertos esperados: Poisson-binomial; calibración: prueba de Spiegelhalter; franjas corregidas por Benjamini-Hochberg. "
          "Resultados: Land of Basketball, ESPN. Análisis independiente, no afiliado a la NBA ni a los equipos. "
          "No es recomendación de apuesta.")


def R():
    T = 6
    return [
        slide(1, T, K, "Viernes perfecto: 9 de 9. Con nuestras probabilidades, eso pasa 1 noche de cada 34",
              [Hero("9 de 9", "favoritos de nuestro modelo ganaron en la NBA el viernes. La suma de sus probabilidades daba 6.1.", ACC),
               Stats([("0.11", "error de la noche (Brier). Un volado: 0.25", ACC),
                      ("53", "puntos de Dončić para salvar nuestra portada", AMBER),
                      ("81 de 116", "aciertos acumulados en la temporada", GHOST)])],
              takeaway="Lo publicamos igual cuando fallamos. Hoy salió perfecto: aquí está cuánto fue mérito y cuánto suerte.",
              style="cover", title_size=72),
        slide(2, T, "Los 9 partidos", "Nueve favoritos, nueve victorias. El más apretado: Lakers",
              [Results([(True, "Trail Blazers 118-124 Lakers", "Lakers 58%"),
                        (True, "76ers 95-119 Cavaliers", "Cleveland 55%"),
                        (True, "Jazz 100-112 Mavericks", "Dallas 67%"),
                        (True, "Thunder 128-97 Grizzlies", "Oklahoma City 67%"),
                        (True, "Celtics 119-80 Hornets", "Boston 68%"),
                        (True, "Raptors 121-107 Bucks", "Toronto 68%"),
                        (True, "Wolves 115-109 Pelicans", "Minnesota 72%"),
                        (True, "Wizards 132-139 Hawks", "Atlanta 74%"),
                        (True, "Spurs 124-109 Kings", "San Antonio 83%")])],
              takeaway="Cinco de los nueve favoritos jugaban de visitante y seis tenían menos de 70%: no era una noche fácil.",
              title_size=64),
        slide(3, T, "Nuestra portada · Lakers vs. Portland", "Le dimos 58% a Los Ángeles. Perdía al medio y Dončić metió 53",
              [Table(("Antes", "Final"),
                     [("Prob. de Lakers", "58%", "Ganó"),
                      ("Margen esperado", "+3.0", "+6"),
                      ("Puntos totales", "231", "242"),
                      ("Portland de visita", "5-0", "5-1")], colors=[GHOST, ACC]),
               Stats([("60-53", "perdía Los Ángeles al medio tiempo", NEG),
                      ("34-15", "el tercer cuarto de los Lakers", ACC),
                      ("3 de 23", "triples de los Lakers en todo el partido", AMBER)])],
              takeaway="La racha de 5-0 de visita de Portland (1 en 28 con sus probabilidades) se cortó justo donde el modelo la ponía en riesgo.",
              title_size=64),
        slide(4, T, "Regresión a la media", "¿Fue mérito o suerte? Un poco de ambos",
              [Stats([("+10", "puntos de más ganaron los favoritos el viernes", AMBER),
                      ("−0.2", "puntos vs. lo esperado en 116 partidos", ACC),
                      ("±14.5", "puntos: lo que se desvía un partido normal", GHOST)]),
               Tests([(True, "Las probabilidades no estaban infladas",
                       "Ganaron los nueve, pero ninguno por una diferencia imposible. En la temporada, los favoritos ganan por lo que decimos.",
                       "Exceso del favorito: −0.2 pts · DE 14.5 · t, p = 0.87 · n = 116"),
                      (True, "9 de 9 es buena suerte encima de un buen modelo",
                       "Esperábamos 6.1 aciertos. Un perfecto con estas probabilidades sale 1 noche de cada 34.",
                       "Poisson-binomial · P(9 de 9) = 0.029")])],
              takeaway="Lección: no esperar otro 9 de 9 mañana. Lo normal con estas probabilidades es 6 de 9.", title_size=70),
        slide(5, T, "Calibración · NBA · 116 partidos fuera de muestra", "Cuando decimos 70%, ¿gana 7 de cada 10? En conjunto, sí",
              [Table(("Esperábamos", "Ganaron"),
                     [("Favoritos 50–60% (41)", "23.0", "30"),
                      ("Favoritos 60–70% (38)", "24.9", "20"),
                      ("Favoritos 70%+ (37)", "28.3", "31")], colors=[GHOST, ACC]),
               Tests([(True, "Probabilidades bien calibradas", "81 aciertos contra 76.2 esperados; error 0.208 (un volado: 0.25).",
                       "Spiegelhalter z = −0.63, p = 0.53 · Brier 0.208 (80%: 0.191–0.226)"),
                      (None, "Las franjas se compensan", "Los de 50–60% ganan de más y los de 60–70% de menos. Con corrección, ninguna es prueba.",
                       "P = 0.018 y 0.068 · Benjamini-Hochberg con 3 franjas: no sobrevive")])],
              takeaway=None, title_size=66),
        slide(6, T, "Lo que aprendimos", "Noche perfecta, cabeza fría",
              [Bullets(["9 de 9 favoritos ganaron; esperábamos 6.1.",
                        "Error de la noche: 0.11 (un volado: 0.25).",
                        "Dončić (53) salvó la única portada del día.",
                        "Acumulado NBA: 81 de 116, calibrado (p = 0.53)."])],
              takeaway="¿Cuál de los nueve te parecía más arriesgado? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
