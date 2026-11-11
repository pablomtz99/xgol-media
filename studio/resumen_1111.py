"""xGol — Resumen del martes 10 nov: los 6 partidos NBA de la noche con el modelo NBA v1 (models/nba_ridge_1103.py).
Ninguna previa se publicó el 10 nov (las portadas del 10 nov no se aprobaron): jornada completa calculada con el mismo modelo y SOLO
los 154 partidos previos (al 9 nov), sin tocar parámetros ni elegir partidos. Rangos 10–90% por bootstrap (400).
Marcadores 2026-27: Land of Basketball (páginas de octubre y noviembre; 154 partidos, récords cuadran con los del 10 nov).
Resultados 10 nov: ESPN (NYK 117-85 MIL, BOS 123-101 PHI, MIA 115-109 UTA, POR 123-103 OKC), VAVEL y Sports Capitol (PHX 133-110 LAC),
Washington Post / AP (ORL 107-100 SAC), SI (POR-OKC; Lillard 25, Avdija 24; SGA 26).
Noche: 5 de 6 vs 3.81 esperados; Poisson-binomial P(5) = 0.224, P(≥5) = 0.29; Brier 0.180.
Margen esperado vs. final del favorito: NYK +12.3/+32, BOS +3.0/+22, PHX +1.1/+23, MIA +5.0/+6, ORL +5.4/+7, OKC +4.4/−20.
POR-OKC: desvío −24.4 = −1.66σ (σ 14.7) → P ≈ 0.048 (1 en 21).
Acumulado (validación día por día, M.validate): 144 partidos, 103 aciertos vs 95.0 esperados (P(≥103) = 0.088);
Brier 0.201 (80%: 0.185–0.217); Spiegelhalter z = −1.16, p = 0.25.
Franjas: 50–60%: 35 de 48 vs 26.9 (una cola 0.013; dos colas 0.025); 60–70%: 29 de 51 vs 33.4 (P(≤29) = 0.125);
70%+: 39 de 45 vs 34.6 (P(≥39) = 0.079). BH con 3 franjas y dos colas: 0.025×3 = 0.075 > 0.05 → indicio, no prueba."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1111")
K = "Resumen · NBA · Martes 10 de noviembre"
METHOD = ("Método: nuestro modelo NBA v1 (ataque y defensa ajustados por rival y localía, regresión ridge hacia la temporada pasada; "
          "no ve lesiones). Calculamos los 6 partidos con los mismos parámetros y solo con datos previos a la noche: jornada completa, "
          "sin elegir partidos. Brier = error promedio, menos es mejor (volado: 0.25). Aciertos esperados: Poisson-binomial; "
          "calibración: prueba de Spiegelhalter; franjas corregidas por Benjamini-Hochberg. Resultados: ESPN, AP, Land of Basketball. "
          "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 6
    return [
        slide(1, T, K, "Martes: 5 de 6. Esperábamos 3.8, y el único tropiezo fue de 20 puntos",
              [Hero("5 de 6", "favoritos de nuestro modelo ganaron el martes. La suma de sus probabilidades daba 3.8.", ACC),
               Stats([("0.18", "error de la noche (Brier). Un volado: 0.25", ACC),
                      ("−20", "Oklahoma City en Portland: la sorpresa", NEG),
                      ("103 de 144", "aciertos acumulados en la temporada", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Buena noche, pero no perfecta: aquí está cuánto fue mérito y cuánto suerte.",
              style="cover", title_size=68),
        slide(2, T, "Los 6 partidos", "Cinco favoritos ganaron. Cayó Oklahoma City en Portland",
              [Results([(True, "Bucks 85-117 Knicks", "Nueva York 80%"),
                        (True, "Magic 107-100 Kings", "Orlando 64%"),
                        (True, "Heat 115-109 Jazz", "Miami 63%"),
                        (False, "Thunder 103-123 Blazers", "Oklahoma City 62%"),
                        (True, "Celtics 123-101 76ers", "Boston 58%"),
                        (True, "Clippers 110-133 Suns", "Phoenix 53%")])],
              takeaway="Cinco de los seis favoritos estaban entre 53% y 64%: una noche así suele traer dos o tres tropiezos. Trajo uno.",
              title_size=66),
        slide(3, T, "Las sorpresas · margen esperado vs. final", "Boston y Phoenix arrasaron; Portland le dio la vuelta al pronóstico",
              [Table(("Esperado", "Final"),
                     [("Boston en Philadelphia", "+3.0", "+22"),
                      ("Phoenix vs. Clippers", "+1.1", "+23"),
                      ("Nueva York vs. Milwaukee", "+12.3", "+32"),
                      ("Thunder en Portland", "+4.4", "−20")], colors=[GHOST, ACC]),
               Stats([("1 en 21", "partidos se desvía tanto como Portland", AMBER),
                      ("±14.7", "puntos: desvío de un partido normal", GHOST),
                      ("+6.5", "puntos extra por favorito", ACC)])],
              takeaway="Philadelphia llegaba 9-2 ganando apretado; Boston, con mejor diferencia de puntos, ganó por 22. El récord engaña.",
              title_size=60),
        slide(4, T, "¿Noche normal? · Probabilidad compuesta", "Con estas 6 probabilidades, 5 aciertos sale 1 de cada 4 noches",
              [HBars([("6 de 6", 6.2, GHOST), ("5 de 6", 22.4, ACC), ("4 de 6", 33.0, GHOST),
                      ("3 de 6", 25.3, GHOST), ("2 de 6", 10.6, GHOST), ("1 o menos", 2.5, GHOST)], 36, "{}%", 230),
               Tests([(True, "Buena noche, sin ser rara",
                       "Lo más probable eran 4 aciertos. 5 o más pasa en 29 de cada 100 noches como esta.",
                       "Poisson-binomial · P(5) = 0.22 · P(≥5) = 0.29 · n = 6")])],
              takeaway="Lección: una buena noche no prueba nada por sí sola. Lo que importa es acertar lo que dices, a la larga.",
              title_size=62),
        slide(5, T, "Calibración · NBA · 144 partidos fuera de muestra", "Cuando decimos 70%, ¿gana 7 de cada 10? En conjunto, sí",
              [Table(("Esperábamos", "Ganaron"),
                     [("Favoritos 50–60% (48)", "26.9", "35"),
                      ("Favoritos 60–70% (51)", "33.4", "29"),
                      ("Favoritos 70%+ (45)", "34.6", "39")], colors=[GHOST, ACC]),
               Tests([(True, "Probabilidades bien calibradas", "103 aciertos contra 95.0 esperados; error 0.201 (un volado: 0.25).",
                       "Spiegelhalter z = −1.16, p = 0.25 · Brier 0.201 (80%: 0.185–0.217)"),
                      (None, "Los partidos parejos los resolvemos mejor de lo que decimos", "35 de 48 contra 26.9. Con corrección por 3 franjas, sigue siendo indicio, no prueba.",
                       "p dos colas = 0.025 · Benjamini-Hochberg: 0.075 > 0.05")])],
              takeaway=None, title_size=66),
        slide(6, T, "Lo que aprendimos", "Una buena noche, contada sin maquillaje",
              [Bullets(["5 de 6 favoritos ganaron; esperábamos 3.8.",
                        "Error de la noche: 0.18 (un volado: 0.25).",
                        "Cayó Oklahoma City (62%) en Portland, por 20.",
                        "Acumulado NBA: 103 de 144, calibrado (p = 0.25)."])],
              takeaway="Hoy se repite Oklahoma City en Portland. ¿Revancha o Portland otra vez? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
