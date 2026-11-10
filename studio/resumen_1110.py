"""xGol — Resumen del lunes 9 nov: los 8 partidos NBA de la noche con el modelo NBA v1 (models/nba_ridge_1103.py).
Ninguna previa se publicó el 9 nov: es la jornada completa calculada con el mismo modelo y SOLO los 146 partidos previos
(al 8 nov), sin tocar parámetros ni elegir partidos. Rangos 10–90% por bootstrap (400).
Resultados: Land of Basketball (resumen diario 9 nov y marcadores de oct–nov) y ESPN (recaps LAL 124-114 ATL, CHA 124-112 CLE).
Noche: 6 de 8 vs 5.44 esperados; Poisson-binomial P(6) = 0.286 (el resultado más probable), P(≥6) = 0.50; Brier 0.200.
Exceso de margen del favorito +3.3 pts (GSW +51 vs +6.9; MEM ganó por 16 en TOR con TOR 67%; CHA ganó por 12 con CLE 70%).
Acumulado (validación día por día, M.validate): 138 partidos, 98 aciertos vs 91.2 esperados (P(≥98) = 0.12);
Brier 0.202 (80%: 0.185–0.218); Spiegelhalter z = −1.03, p = 0.30.
Franjas: 50–60%: 33 de 46 vs 25.8 (P(≥33) = 0.022); 60–70%: 27 de 48 vs 31.5 (P(≤27) = 0.11); 70%+: 38 de 44 vs 33.8 (P(≥38) = 0.089).
BH con 3 franjas: 0.022×3 = 0.066 > 0.05 → indicio, no prueba. Cálculo: scratch res.py (mismo modelo)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1110")
K = "Resumen · NBA · Lunes 9 de noviembre"
METHOD = ("Método: nuestro modelo NBA v1 (ataque y defensa ajustados por rival y localía, regresión ridge hacia la temporada pasada; "
          "no ve lesiones). Calculamos los 8 partidos con los mismos parámetros y solo con datos previos a la noche: jornada completa, "
          "sin elegir partidos. Brier = error promedio, menos es mejor (volado: 0.25). Aciertos esperados: Poisson-binomial; "
          "calibración: prueba de Spiegelhalter; franjas corregidas por Benjamini-Hochberg. Resultados: Land of Basketball, ESPN. "
          "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 6
    return [
        slide(1, T, K, "Lunes: 6 de 8. Con nuestras probabilidades, era justo el resultado más probable",
              [Hero("6 de 8", "favoritos de nuestro modelo ganaron el lunes. La suma de sus probabilidades daba 5.4.", ACC),
               Stats([("0.20", "error de la noche (Brier). Un volado: 0.25", ACC),
                      ("+51", "Golden State: la paliza de la noche", AMBER),
                      ("98 de 138", "aciertos acumulados en la temporada", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Dos favoritos cayeron; aquí está si fue mala suerte o un error del modelo.",
              style="cover", title_size=70),
        slide(2, T, "Los 8 partidos", "Seis favoritos ganaron. Cayeron Cleveland y Toronto",
              [Results([(True, "Wizards 111-122 Pistons", "Detroit 85%"),
                        (False, "Cavaliers 112-124 Hornets", "Cleveland 70%"),
                        (True, "Pacers 122-125 Mavericks", "Dallas 69%"),
                        (True, "Pelicans 87-138 Warriors", "Golden State 68%"),
                        (True, "Spurs 122-96 Suns", "San Antonio 68%"),
                        (False, "Grizzlies 118-102 Raptors", "Toronto 67%"),
                        (True, "Nuggets 100-110 Rockets", "Houston 62%"),
                        (True, "Lakers 124-114 Hawks", "Lakers 57%")])],
              takeaway="Siete de los ocho favoritos estaban entre 57% y 70%: en ese rango, perder 2 o 3 es lo normal.",
              title_size=66),
        slide(3, T, "Las sorpresas · margen esperado vs. final", "Charlotte y Memphis sorprendieron; Golden State se pasó por 44",
              [Table(("Esperado", "Final"),
                     [("Cleveland en Charlotte", "+7.5", "−12"),
                      ("Toronto vs. Memphis", "+6.6", "−16"),
                      ("Warriors vs. Pelicans", "+6.9", "+51"),
                      ("Detroit vs. Washington", "+15.2", "+11")], colors=[GHOST, ACC]),
               Stats([("3 de 10", "veces pierde un favorito de 70%", AMBER),
                      ("±14.7", "puntos: lo que se desvía un partido normal", GHOST),
                      ("+3.3", "puntos de más ganaron los favoritos en promedio", ACC)])],
              takeaway="Desvíos como los de Cleveland y Toronto se ven 1 de cada 5 a 8 partidos. Lo raro fue Golden State: 3 de cada 1,000.",
              title_size=62),
        slide(4, T, "¿Noche normal? · Probabilidad compuesta", "Con estas 8 probabilidades, 6 aciertos era lo más probable",
              [HBars([("8 de 8", 4.4, GHOST), ("7 de 8", 17.1, GHOST), ("6 de 8", 28.6, ACC),
                      ("5 de 8", 27.1, GHOST), ("4 de 8", 15.7, GHOST), ("3 o menos", 7.2, GHOST)], 32, "{}%", 230),
               Tests([(True, "No fue una mala noche: fue una noche típica",
                       "La mitad de las noches con estas probabilidades terminan con 6 aciertos o más.",
                       "Poisson-binomial · P(6) = 0.29 · P(≥6) = 0.50 · n = 8")])],
              takeaway="Lección: con favoritos de 60–70%, nadie acierta todo. Lo que importa es acertar lo que dices, a la larga.",
              title_size=64),
        slide(5, T, "Calibración · NBA · 138 partidos fuera de muestra", "Cuando decimos 70%, ¿gana 7 de cada 10? En conjunto, sí",
              [Table(("Esperábamos", "Ganaron"),
                     [("Favoritos 50–60% (46)", "25.8", "33"),
                      ("Favoritos 60–70% (48)", "31.5", "27"),
                      ("Favoritos 70%+ (44)", "33.8", "38")], colors=[GHOST, ACC]),
               Tests([(True, "Probabilidades bien calibradas", "98 aciertos contra 91.2 esperados; error 0.202 (un volado: 0.25).",
                       "Spiegelhalter z = −1.03, p = 0.30 · Brier 0.202 (80%: 0.185–0.218)"),
                      (None, "La franja de 60–70% sigue un poco abajo", "27 de 48 contra 31.5. Con corrección por 3 franjas, es indicio, no prueba.",
                       "P = 0.022, 0.089 y 0.11 · Benjamini-Hochberg: ninguna sobrevive")])],
              takeaway=None, title_size=66),
        slide(6, T, "Lo que aprendimos", "Una noche normal, contada sin maquillaje",
              [Bullets(["6 de 8 favoritos ganaron; esperábamos 5.4.",
                        "Error de la noche: 0.20 (un volado: 0.25).",
                        "Cayeron Cleveland (70%) y Toronto (67%).",
                        "Acumulado NBA: 98 de 138, calibrado (p = 0.30)."])],
              takeaway="¿Te sorprendió más Charlotte o Memphis? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
