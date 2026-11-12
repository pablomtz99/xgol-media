"""xGol — Resumen del miércoles 11 nov: los 10 partidos NBA de la noche con el modelo NBA v1 (models/nba_ridge_1103.py).
Ninguna previa se publicó el 11 nov (portadas del 11 nov sin aprobar): jornada completa con el mismo modelo y SOLO los 160 partidos
previos (al 10 nov), sin tocar parámetros ni elegir partidos. Rangos 10–90% por bootstrap (400).
Resultados 11 nov: Land of Basketball (resumen diario) + CBS Sports (7 marcadores) ; GSW-HOU 108-115 (ESPN, AP/ABC, Yahoo; Land of
Basketball decía 105, corregido); ORL-UTA 123-108 (AP/KJZZ, Yahoo, CBS; Land of Basketball decía 106, corregido); POR 118-108 OKC (AP/KRMG, ESPN).
Contexto: Curry salió en el 1er cuarto con molestia abdominal derecha (AP); Avdija 28, SGA 31 (AP); Wagner 38 (AP).
Noche: 7 de 10 vs 6.36 esperados; Poisson-binomial P(7) = 0.247, P(≥7) = 0.47; Brier 0.193.
Margen esperado vs final del favorito: LAL +11.3/+11, SAS +14.2/+5, HOU +5.3/+7, ORL +4.6/+15, IND +1.6/+13, BOS +3.4/+5, DEN +3.4/+5,
NOP +3.6/−34, NYK +3.8/−8, OKC +2.3/−10. NOP-BKN: desvío −37.6 = −2.56σ (σ 14.7) → P ≈ 0.005 (1 en 190).
Acumulado (M.validate): 154 partidos, 110 aciertos vs 101.4 esperados (P(≥110) = 0.078); Brier 0.201 (80%: 0.185–0.216);
Spiegelhalter z = −1.28, p = 0.20. Franjas: 50–60%: 38 de 53 vs 29.8 (una cola 0.015; dos colas 0.031); 60–70%: 31 de 54 vs 35.3
(P(≤31) = 0.14); 70%+: 41 de 47 vs 36.3 (P(≥41) = 0.063). BH 3 franjas: 0.031×3 = 0.092 > 0.05 → indicio, no prueba."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1112")
K = "Resumen · NBA · Miércoles 11 de noviembre"
METHOD = ("Método: nuestro modelo NBA v1 (ataque y defensa ajustados por rival y localía, regresión ridge hacia la temporada pasada; "
          "no ve lesiones). Calculamos los 10 partidos con los mismos parámetros y solo con datos previos a la noche: jornada completa, "
          "sin elegir partidos. Brier = error promedio, menos es mejor (volado: 0.25). Aciertos esperados: Poisson-binomial; "
          "calibración: prueba de Spiegelhalter; franjas corregidas por Benjamini-Hochberg. Resultados: AP, ESPN, CBS Sports, Land of Basketball. "
          "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 6
    return [
        slide(1, T, K, "Miércoles: 7 de 10. Esperábamos 6.4, y Brooklyn dio el golpe de la noche",
              [Hero("7 de 10", "favoritos de nuestro modelo ganaron el miércoles. La suma de sus probabilidades daba 6.4.", ACC),
               Stats([("0.19", "error de la noche (Brier). Un volado: 0.25", ACC),
                      ("+34", "Brooklyn (2-8) en Nueva Orleans: la sorpresa", NEG),
                      ("110 de 154", "aciertos acumulados en la temporada", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Noche normal, con una sorpresa de las que salen 1 vez cada 190 partidos.",
              style="cover", title_size=68),
        slide(2, T, "Los 10 partidos", "Siete favoritos ganaron. Fallaron Nueva Orleans, Nueva York y Oklahoma City",
              [Results([(True, "Spurs 124-119 Bulls", "San Antonio 83%"),
                        (True, "Lakers 123-112 Bucks", "Lakers 78%"),
                        (True, "Warriors 108-115 Rockets", "Houston 64%"),
                        (True, "Magic 123-108 Jazz", "Orlando 62%"),
                        (True, "Celtics 98-93 Raptors", "Boston 59%"),
                        (True, "Nuggets 123-118 Grizzlies", "Denver 59%"),
                        (True, "Wizards 101-114 Pacers", "Indiana 54%"),
                        (False, "Cavaliers 115-107 Knicks", "Nueva York 60%"),
                        (False, "Nets 145-111 Pelicans", "N. Orleans 60%"),
                        (False, "Thunder 108-118 Blazers", "Oklahoma 56%")])],
              takeaway=None, title_size=58),
        slide(3, T, "Las sorpresas · margen esperado vs. final", "Los Lakers, clavados. Brooklyn, a 38 puntos del pronóstico",
              [Table(("Esperado", "Final"),
                     [("Lakers en Milwaukee", "+11.3", "+11"),
                      ("Pelicans vs. Brooklyn", "+3.6", "−34"),
                      ("Thunder en Portland", "+2.3", "−10"),
                      ("Knicks vs. Cleveland", "+3.8", "−8")], colors=[GHOST, ACC]),
               Stats([("1 en 190", "partidos se desvía tanto como Brooklyn", AMBER),
                      ("2 de 2", "Portland barrió a Oklahoma City", NEG),
                      ("1er cuarto", "salió Curry (abdomen) y Houston cortó su racha de 8", GHOST)])],
              takeaway="Brooklyn llegaba 2-8 y anotó 145. Una noche así no cambia mucho al modelo: un partido pesa poco contra 160.",
              title_size=60),
        slide(4, T, "¿Noche normal? · Probabilidad compuesta", "Con estas 10 probabilidades, 7 aciertos sale 1 de cada 4 noches",
              [HBars([("9 o 10", 7.0, GHOST), ("8 de 10", 15.9, GHOST), ("7 de 10", 24.7, ACC),
                      ("6 de 10", 24.9, GHOST), ("5 de 10", 16.9, GHOST), ("4 o menos", 10.8, GHOST)], 30, "{}%", 230),
               Tests([(True, "Noche dentro de lo esperado",
                       "Lo más probable eran 6 o 7 aciertos. 7 o más pasa en 47 de cada 100 noches como esta.",
                       "Poisson-binomial · P(7) = 0.25 · P(≥7) = 0.47 · n = 10")])],
              takeaway="Siete favoritos estaban entre 54% y 64%: con tantos partidos parejos, tres tropiezos es lo normal.",
              title_size=62),
        slide(5, T, "Calibración · NBA · 154 partidos fuera de muestra", "Cuando decimos 70%, ¿gana 7 de cada 10? En conjunto, sí",
              [Table(("Esperábamos", "Ganaron"),
                     [("Favoritos 50–60% (53)", "29.8", "38"),
                      ("Favoritos 60–70% (54)", "35.3", "31"),
                      ("Favoritos 70%+ (47)", "36.3", "41")], colors=[GHOST, ACC]),
               Tests([(True, "Probabilidades bien calibradas", "110 aciertos contra 101.4 esperados; error 0.201 (un volado: 0.25).",
                       "Spiegelhalter z = −1.28, p = 0.20 · Brier 0.201 (80%: 0.185–0.216)"),
                      (None, "Los partidos parejos los resolvemos mejor de lo que decimos", "38 de 53 contra 29.8. Con corrección por 3 franjas, sigue siendo indicio, no prueba.",
                       "p dos colas = 0.031 · Benjamini-Hochberg: 0.092 > 0.05")])],
              takeaway=None, title_size=66),
        slide(6, T, "Lo que aprendimos", "Una noche normal, contada sin maquillaje",
              [Bullets(["7 de 10 favoritos ganaron; esperábamos 6.4.",
                        "Error de la noche: 0.19 (un volado: 0.25).",
                        "Brooklyn ganó por 34 en Nueva Orleans: 1 en 190.",
                        "Acumulado NBA: 110 de 154, calibrado (p = 0.20)."])],
              takeaway="Golden State visita el viernes a San Antonio, quizá sin Curry. ¿Cuánto vale él solo? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
