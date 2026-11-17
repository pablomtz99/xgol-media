"""xGol — Resumen del lunes 16 nov (NFL, semana 10, Monday Night): la probabilidad que fijamos en la portada del 16 nov
(studio/portadas_1116.py, commit d7a25e4, ANTES del partido; no se publicó: sin aprobar). Modelo NFL v0 con semanas 1–10 (sin el lunes):
BAL 72.7% (58–85%), margen +8.2. Final: LAC 23-20 BAL (nflverse games.csv; ESPN y AP/ABC News). Brier de la noche = 0.727² = 0.529.
Datos del partido: AP/ABC News y ESPN (Herbert 129 yd por aire, 0 int, 7 carreras 51 yd y TD de 22; Brissett 340 yd y 1 int en su debut;
carrera 160-16; Henry 10 carreras 10 yd 2 TD; balón suelto de Flowers a 2:03; LAC 1-8 cortó 11 derrotas seguidas; BAL 4-6, 5 seguidas, 7 de sus
últimos 8 en casa perdidos). EPA/jugada del partido (pbp nflverse): LAC −0.005, BAL −0.029; éxito 42.6% vs 41.5%.
Acumulado fuera de muestra (studio/models/nfl_1117.py, semanas 4–10, solo datos previos a cada semana, recalculado hoy con pbp actualizado):
101 partidos, 66 aciertos vs 62.0 esperados; Brier 0.228 (80%: 0.213–0.244); Spiegelhalter p = 0.86. Franjas: 50–60% 33/51 (dijo 55%, 65%);
60–70% 20/33 (63% → 61%); 70%+ 13/17 (76% → 76.5%). En ese protocolo estricto (sem. 1–9) este partido daba BAL 70.5%; con sem. 6–9: 63.6%.
Histórico (portadas_1116): equipos 0-8+ 2002–2025: 15; solo 2 terminaron sin ganar. Monte Carlo 16 nov: LAC 0-17 = 5.2%."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1117")
K = "Resumen · NFL · Lunes 16 de noviembre"
METHOD = ("Método: nuestro modelo NFL v0. Margen esperado = 0.5 × (puntos que suma por jugada el local − el visitante, ya restando lo que "
          "permite su defensa) × 61.6 jugadas + 1.5 de localía; probabilidad = Φ(margen / 13.5). Probabilidad fijada antes del partido "
          "con datos de las semanas 1–10; rango 10–90% por remuestreo de partidos. Brier = error promedio, menos es mejor (volado: 0.25). "
          "Calibración: prueba de Spiegelhalter. Datos: nflverse. Resultados: AP, ESPN. "
          "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 5
    return [
        slide(1, T, K, "Fallamos: los Chargers ganaron su primer partido, 23-20 en Baltimore",
              [Matchup("Chargers", "23 · ahora 1-8", "Ravens", "20 · ahora 4-6", sep="ganaron en casa de · marcador · récord"),
               Stats([("27%", "le dábamos a los Chargers: pasa 1 de cada 4 veces", NEG),
                      ("0.53", "error de la noche (Brier). Un volado: 0.25", NEG),
                      ("160 a 16", "yardas por tierra: ahí se decidió", AMBER)])],
              takeaway="Lo publicamos ganemos o perdamos. Nuestro favorito era Baltimore con 73% y perdió.",
              style="cover", title_size=62),
        slide(2, T, "El partido · Lunes por la noche · Baltimore", "Esperábamos Baltimore por 8. Perdió por 3 porque no pudo correr",
              [Table(("Chargers", "Ravens"),
                     [("Yardas por tierra", "160", "16"),
                      ("Puntos por jugada", "−0.01", "−0.03"),
                      ("Jugadas con éxito", "43%", "42%"),
                      ("Yardas por aire", "129", "340"),
                      ("Intercepciones", "0", "1")], colors=[ACC, GHOST]),
               Stats([("10 en 10", "Derrick Henry: 10 acarreos, 10 yardas", NEG),
                      ("51", "yardas corriendo de Justin Herbert", ACC),
                      ("2:03", "restaban: balón suelto de Baltimore", AMBER)])],
              takeaway="Brissett lanzó 340 yardas en su debut, pero sin carrera Baltimore no pudo cerrar.",
              title_size=58),
        slide(3, T, "¿Sorpresa? · Lo que probamos", "Un 27% no es un cero: estas cosas pasan 1 de cada 4 veces",
              [HBars([("Dijimos", 76, GHOST), ("Pasó: 13 de 17", 76.5, ACC)], 100, "{}%", 330),
               Tests([(True, "Nuestros favoritos fuertes ganan lo que decimos",
                       "En 17 partidos con 70% o más, esperábamos 13 victorias. Fueron 13. Este fue una de las 4 derrotas.",
                       "Fuera de muestra, semanas 4–10 · n = 17 · dijo 76%, pasó 76.5%"),
                      (True, "Lo anotamos antes del partido: el modelo no veía a Brissett",
                       "Con solo el último mes, Baltimore bajaba de 73% a 64%. Era su 4° mariscal titular en 4 partidos.",
                       "Semanas 6–9 · P = 0.64 · el modelo no ve cambios de mariscal"),
                      (True, "Los 0-8 casi siempre ganan alguno",
                       "Desde 2002, 13 de 15 equipos que llegaron 0-8 ganaron después. Los Chargers se suman.",
                       "nflverse 2002–2025 · simulación del 16 nov: 0-17 en 5% de temporadas")])],
              takeaway=None, title_size=58),
        slide(4, T, "Calibración · NFL · 101 partidos fuera de muestra (semanas 4–10)", "Con este tropiezo, cuando decimos 3 de cada 4, siguen ganando 3 de cada 4",
              [Table(("Dijimos", "Pasó"),
                     [("Favorito 50–60% · 51 partidos", "55%", "65%"),
                      ("Favorito 60–70% · 33 partidos", "63%", "61%"),
                      ("Favorito 70% o más · 17 partidos", "76%", "76%")], colors=[GHOST, ACC]),
               Stats([("66 de 101", "aciertos; esperábamos 62", ACC),
                      ("0.228", "error acumulado (80%: 0.213–0.244)", ACC),
                      ("p = 0.86", "prueba de calibración: sin desvío", GHOST)])],
              takeaway="Una noche mala pesa, pero se mide contra 101 partidos. La vara es la misma que en las buenas.",
              title_size=56),
        slide(5, T, "Lo que aprendimos", "El modelo mide calidad; los cambios de mariscal todavía no",
              [Bullets(["Baltimore 73% y ganaron los Chargers 23-20.",
                        "Error de la noche: 0.53 (un volado: 0.25).",
                        "Se decidió por tierra: 160 contra 16 yardas.",
                        "Acumulado NFL: 66 de 101 y calibrado (p = 0.86).",
                        "Pendiente: ajustar por mariscal titular."])],
              takeaway="¿Los Chargers ya despertaron o fue un lunes raro? El domingo reciben a los Jets. Te leemos.",
              style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
