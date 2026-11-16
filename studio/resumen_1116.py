"""xGol — Resumen del domingo 15 nov (NFL, semana 10): las 8 probabilidades que fijamos en las portadas del 14 y 15 nov
(studio/portadas_1114.py y portadas_1115.py; commits 0c175b1 y 95b4ff5, ANTES de los partidos). Ninguna se publicó (sin aprobar).
Modelo NFL v0 (EPA neta/jugada, semanas 1–9). Favoritos: GB 65.5% (perdió 10-30), CIN 62.4% (38-18), JAX 81.0% (40-23 en TEN),
SF 67.5% (46-40 en DAL), KC 69.6% (35-13 en ATL), BUF 62.3% (31-12 en NYJ), LA 68.6% (34-6 en ARI), SEA 60.3% (21-13 en LV).
Aciertos 7 de 8 vs 5.37 esperados; Poisson-binomial P(≥7) = 0.20. Brier 0.150. Los 4 visitantes (idea 4 del 14 nov): 0.237 → ganaron los 4.
Jornada completa del domingo con el mismo modelo (12 partidos, sin elegir): 10 de 12 vs 7.53; P(≥10) = 0.11; Brier 0.182.
Acumulado fuera de muestra 2026 (semanas 4–10, solo datos previos a cada semana): 100 partidos, 65 aciertos vs 63.2; Brier 0.224
(80%: 0.207–0.242; volado 0.25); Spiegelhalter p = 0.98. Franjas: 50–60% 27/42 vs 23.2; 60–70% 23/38 vs 24.3; 70%+ 15/20 vs 15.6.
Rompemitos divisional (idea 3 del 15 nov): favoritos del mercado 4 de 6 vs 3.9 esperados.
Resultados: DAZN (todos los marcadores de la semana 10), AP/ABC15 (LA 34-6 ARI: Beck 11/18, 108 yd, 2 int; Rams 4 seguidas, 6-4; ARI 11
derrotas seguidas en casa), AP/ABC News (SEA 21-13 LV: Lock 2 TD, 6 capturas a Mendoza; SEA 6-4), ESPN. Coinciden con nflverse games.csv."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1116")
K = "Resumen · NFL · Domingo 15 de noviembre"
METHOD = ("Método: nuestro modelo NFL v0. Margen esperado = 0.5 × (puntos que suma por jugada el local − el visitante, ya restando lo que "
          "permite su defensa) × 61.6 jugadas + 1.5 de localía; probabilidad = Φ(margen / 13.5). Probabilidades fijadas antes de cada partido "
          "con datos de las semanas 1–9. Brier = error promedio, menos es mejor (volado: 0.25). Aciertos esperados: Poisson-binomial; "
          "calibración: prueba de Spiegelhalter. Datos: nflverse. Resultados: AP, ESPN, DAZN. "
          "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 6
    return [
        slide(1, T, K, "Domingo: 7 de 8. Y los 4 favoritos de visita ganaron, algo que salía 1 de cada 4",
              [Hero("7 de 8", "favoritos de nuestro modelo ganaron el domingo. La suma de sus probabilidades daba 5.4.", ACC),
               Stats([("0.15", "error de la noche (Brier). Un volado: 0.25", ACC),
                      ("1 de 5", "domingos como este terminan con 7 aciertos o más", AMBER),
                      ("4 de 4", "visitantes: Jacksonville, San Francisco, Kansas City y Buffalo", ACC)])],
              takeaway="Lo publicamos ganemos o perdamos. Este domingo salió mejor de lo esperado; el único tropiezo fue Green Bay.",
              style="cover", title_size=62),
        slide(2, T, "Los 8 partidos que analizamos", "Siete aciertos, cinco de ellos por 17 puntos o más",
              [Results([(True, "Rams 34-6 en Arizona", "Los Ángeles 69%"),
                        (True, "Seahawks 21-13 en Las Vegas", "Seattle 60%"),
                        (True, "Jaguars 40-23 en Tennessee", "Jacksonville 81%"),
                        (True, "49ers 46-40 en Dallas", "San Francisco 68%"),
                        (True, "Chiefs 35-13 en Atlanta", "Kansas City 70%"),
                        (True, "Bills 31-12 en Nueva York", "Buffalo 62%"),
                        (True, "Bengals 38-18 vs. Pittsburgh", "Cincinnati 62%"),
                        (False, "Packers 10-30 vs. Minnesota", "Green Bay 66%")])],
              takeaway=None, title_size=58),
        slide(3, T, "Margen esperado vs. final", "Los favoritos ganaron por más de lo esperado; Minnesota rompió el guion",
              [Table(("Esperado", "Final"),
                     [("Rams en Arizona", "+6.5", "+28"),
                      ("Chiefs en Atlanta", "+6.9", "+22"),
                      ("Bengals vs. Pittsburgh", "+4.3", "+20"),
                      ("Seahawks en Las Vegas", "+3.5", "+8"),
                      ("Packers vs. Minnesota", "+5.4", "−20")], colors=[GHOST, ACC]),
               Stats([("11 de 18", "pases completos de Carson Beck en su debut, con 2 intercepciones", GHOST),
                      ("6", "capturas de Seattle a Fernando Mendoza, también debutante", AMBER),
                      ("11", "derrotas seguidas de Arizona en casa", NEG)])],
              takeaway="Los dos mariscales novatos sufrieron como sugería la historia: los debutantes ganan 1 de cada 3.",
              title_size=58),
        slide(4, T, "¿Domingo normal? · Probabilidad compuesta", "Con estas 8 probabilidades, 7 aciertos o más salía 1 de cada 5 domingos",
              [HBars([("8 de 8", 4.0, GHOST), ("7 de 8", 16.0, ACC), ("6 de 8", 27.9, GHOST), ("5 de 8", 27.4, GHOST),
                      ("4 o menos", 24.7, GHOST)], 32, "{}%", 230),
               Tests([(True, "Mejor que lo esperado, sin salirse de lo posible",
                       "Lo más probable eran 5 o 6 aciertos. Siete o más pasa en 20 de cada 100 domingos como este.",
                       "Poisson-binomial · P(≥7) = 0.20 · aciertos esperados 5.4 · n = 8"),
                      (True, "Los 4 visitantes: lo calculamos el sábado en 24%",
                       "Multiplicamos sus 4 probabilidades: 0.81 × 0.68 × 0.70 × 0.62. Ganaron los cuatro.",
                       "Probabilidad compuesta = 0.237 (bootstrap 14–31%)")])],
              takeaway=None, title_size=60),
        slide(5, T, "Calibración · NFL · 100 partidos fuera de muestra (semanas 4–10)", "Cuando decimos 2 de cada 3, gana cerca de 2 de cada 3",
              [Table(("Dijimos", "Pasó"),
                     [("Favorito 50–60% · 42 partidos", "55%", "64%"),
                      ("Favorito 60–70% · 38 partidos", "64%", "61%"),
                      ("Favorito 70% o más · 20 partidos", "78%", "75%")], colors=[GHOST, ACC]),
               Stats([("65 de 100", "aciertos; esperábamos 63", ACC),
                      ("0.224", "error acumulado (80%: 0.207–0.242)", ACC),
                      ("p = 0.98", "prueba de calibración: sin desvío", GHOST)]),
               Tests([(True, "Jornada completa del domingo: 10 de 12",
                       "Mismo modelo, todos los partidos, sin elegir. Esperábamos 7.5; 10 o más salía 11 de cada 100.",
                       "P(≥10) = 0.11 · Brier 0.182 · n = 12")])],
              takeaway=None, title_size=58),
        slide(6, T, "Lo que aprendimos", "Una buena noche, contada con la misma vara que las malas",
              [Bullets(["7 de 8 favoritos ganaron; esperábamos 5.4.",
                        "Error de la noche: 0.15 (un volado: 0.25).",
                        "Los 4 visitantes ganaron (salía 24%) y los debutantes sufrieron.",
                        "Acumulado NFL: 65 de 100 y calibrado (p = 0.98)."])],
              takeaway="Minnesota ganó en Green Bay por 20 siendo el 19° en calidad. ¿Ya cambió o fue un domingo raro? Te leemos.",
              style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
