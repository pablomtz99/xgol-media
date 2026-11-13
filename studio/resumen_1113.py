"""xGol — Resumen del jueves 12 nov: los 4 partidos NBA de la noche con el modelo NBA v1 (models/nba_ridge_1103.py).
Ninguna previa se publicó el 12 nov (portadas del 12 nov sin aprobar; dos de ellas eran TOR@PHI y DAL@MIN): jornada completa con el
mismo modelo y SOLO los 170 partidos previos (al 11 nov), sin tocar parámetros ni elegir partidos. Rangos 10–90% por bootstrap (400).
Resultados 12 nov: Land of Basketball (resumen diario), verificados uno por uno: PHI 123-112 TOR (ESPN, Washington Post/AP, CBS;
sin LeBron James), MIN 133-94 DAL (ESPN, ABC/AP: "most lopsided win of the season"), PHX 101-96 CHA (ESPN, Yahoo; Booker 30),
DET 144-140 WAS 2OT (NBA.com, Yahoo/AP; Cunningham 52, récord personal).
Noche: 4 de 4 vs 2.71 esperados; Poisson-binomial P(4) = 0.20; Brier 0.115.
Margen esperado vs final del favorito: PHX +5.8/+5, MIN +8.8/+39, DET +12.6/+4 (2OT), PHI +1.0/+11.
MIN-DAL: desvío +30.2 = +2.06σ (σ 14.7) → una cola P ≈ 0.020 (1 en 50). Total DET-WAS 284 vs 221.7 proyectado (dos prórrogas).
Acumulado (M.validate): 158 partidos, 114 aciertos vs 104.1 esperados (P(≥114) = 0.052); Brier 0.198 (80%: 0.183–0.213);
Spiegelhalter z = −1.45, p = 0.15. Franjas: 50–60%: 39 de 54 vs 30.4 (una cola 0.011; dos colas 0.023); 60–70%: 32 de 55 vs 35.9
(P(≤32) = 0.16); 70%+: 43 de 49 vs 37.8 (P(≥43) = 0.047). BH 3 franjas: 0.023×3 = 0.069 > 0.05 → indicio, no prueba."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1113")
K = "Resumen · NBA · Jueves 12 de noviembre"
METHOD = ("Método: nuestro modelo NBA v1 (ataque y defensa ajustados por rival y localía, regresión ridge hacia la temporada pasada; "
          "no ve lesiones). Calculamos los 4 partidos con los mismos parámetros y solo con datos previos a la noche: jornada completa, "
          "sin elegir partidos. Brier = error promedio, menos es mejor (volado: 0.25). Aciertos esperados: Poisson-binomial; "
          "calibración: prueba de Spiegelhalter; franjas corregidas por Benjamini-Hochberg. Resultados: AP, ESPN, NBA.com, Land of Basketball. "
          "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 6
    return [
        slide(1, T, K, "Jueves: 4 de 4. Hasta el partido más parejo de la noche cayó del lado del modelo",
              [Hero("4 de 4", "favoritos de nuestro modelo ganaron el jueves. La suma de sus probabilidades daba 2.7.", ACC),
               Stats([("0.11", "error de la noche (Brier). Un volado: 0.25", ACC),
                      ("+39", "Minnesota sobre Dallas: esperábamos +9", AMBER),
                      ("114 de 158", "aciertos acumulados en la temporada", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Una noche perfecta pasa 1 de cada 5 veces con estas probabilidades: buena, no milagrosa.",
              style="cover", title_size=64),
        slide(2, T, "Los 4 partidos", "Cuatro favoritos, cuatro victorias. Detroit necesitó dos prórrogas",
              [Results([(True, "Raptors 112-123 76ers", "Philadelphia 53%"),
                        (True, "Mavericks 94-133 Wolves", "Minnesota 73%"),
                        (True, "Hornets 96-101 Suns", "Phoenix 65%"),
                        (True, "Pistons 144-140 Wizards (2 pr.)", "Detroit 80%")]),
               Stats([("53%", "Philadelphia: el más parejo, y aun sin LeBron James", GHOST),
                      ("52", "puntos de Cunningham en Washington, su récord", ACC),
                      ("30", "puntos de Booker para Phoenix", GHOST)])],
              takeaway=None, title_size=60),
        slide(3, T, "Margen esperado vs. final", "Phoenix, clavado. Minnesota se pasó por 30 puntos",
              [Table(("Esperado", "Final"),
                     [("Suns vs. Charlotte", "+5.8", "+5"),
                      ("Wolves vs. Dallas", "+8.8", "+39"),
                      ("Pistons en Washington", "+12.6", "+4"),
                      ("76ers vs. Toronto", "+1.0", "+11")], colors=[GHOST, ACC]),
               Stats([("1 en 50", "partidos se desvía tanto como Minnesota", AMBER),
                      ("284", "puntos en Washington; proyectábamos 222 en 48 minutos", GHOST),
                      ("2 pr.", "le costó a Detroit ganar como favorito de 80%", NEG)])],
              takeaway="Acertar quién gana no es acertar por cuánto: Detroit ganó por 4 cuando esperábamos 13; Minnesota, por 39 cuando esperábamos 9.",
              title_size=60),
        slide(4, T, "¿Noche normal? · Probabilidad compuesta", "Con estas 4 probabilidades, el 4 de 4 sale 1 de cada 5 noches",
              [HBars([("4 de 4", 20.1, ACC), ("3 de 4", 41.2, GHOST), ("2 de 4", 29.3, GHOST),
                      ("1 de 4", 8.6, GHOST), ("0 de 4", 0.9, GHOST)], 45, "{}%", 230),
               Tests([(True, "Buena noche, dentro de lo esperado",
                       "Lo más probable eran 3 aciertos. El pleno pasa en 20 de cada 100 noches como esta.",
                       "Poisson-binomial · P(4) = 0.20 · aciertos esperados 2.7 · n = 4")])],
              takeaway="Con 4 partidos, una noche dice poco. Lo que importa es el acumulado: 158 partidos, en el siguiente slide.",
              title_size=62),
        slide(5, T, "Calibración · NBA · 158 partidos fuera de muestra", "Cuando decimos 70%, ¿gana 7 de cada 10? En conjunto, sí",
              [Table(("Esperábamos", "Ganaron"),
                     [("Favoritos 50–60% (54)", "30.4", "39"),
                      ("Favoritos 60–70% (55)", "35.9", "32"),
                      ("Favoritos 70%+ (49)", "37.8", "43")], colors=[GHOST, ACC]),
               Tests([(True, "Probabilidades bien calibradas", "114 aciertos contra 104.1 esperados; error 0.198 (un volado: 0.25).",
                       "Spiegelhalter z = −1.45, p = 0.15 · Brier 0.198 (80%: 0.183–0.213)"),
                      (None, "Los partidos parejos los resolvemos mejor de lo que decimos", "39 de 54 contra 30.4. Con corrección por 3 franjas, sigue siendo indicio, no prueba.",
                       "p dos colas = 0.023 · Benjamini-Hochberg: 0.069 > 0.05")])],
              takeaway=None, title_size=66),
        slide(6, T, "Lo que aprendimos", "Una noche perfecta, contada con la misma vara que las malas",
              [Bullets(["4 de 4 favoritos ganaron; esperábamos 2.7.",
                        "Error de la noche: 0.11 (un volado: 0.25).",
                        "Minnesota ganó por 39: 1 en 50. Detroit sufrió 2 prórrogas.",
                        "Acumulado NBA: 114 de 158, calibrado (p = 0.15)."])],
              takeaway="Esta noche San Antonio, el 1° de nuestra tabla, recibe a Golden State sin Curry. ¿Se sostiene su racha de 10? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
