"""xGol — portadas de las 4 ideas del 17 nov (NFL semana 11). Diseño v7. Cálculos: studio/models/nfl_1117.py y nfl_ideas_1117.py.
Datos: nflverse (CC-BY 4.0) games.csv + play_by_play_2026 (semanas 1–10 completas, incl. LAC@BAL del lunes). Modelo NFL v0; rangos 10–90% bootstrap (400).
Validación fuera de muestra (sem. 4–10): 101 partidos, 66 aciertos vs 62.0; Brier 0.228 (80%: 0.213–0.244); Spiegelhalter p = 0.86.
SIN NBA (xgol-data sin acceso: add_repo no disponible; Land of Basketball bloqueado por el proxy y WebFetch pidió permiso sin respuesta).
SIN tenis (ATP Finals en curso, sin fuente de datos verificable). Futbol: fecha FIFA; Liga MX regresa el 20 nov.
1) MIN vs SF en CDMX (dom 22, 20:20 ET = 19:20 CDMX, Estadio Banorte, neutral; SF local designado). SF 66.4% (57.5–74.4%), margen +5.7; solo
   semanas 7–10: 70.4%. SF 8-1, 2° (ataque 1°, pase 1°, carrera 2°; defensa 9°, contra carrera 1°; capturas defensivas 31°). MIN 7-2, 13° (ataque 29°,
   defensa 1°, contra pase 1°, capturas 1° 12.0%). MIN cerrados 4-1, Pitágoras 6.2. Mariscales MIN (pbp): Wentz sem. 1–2 y 9, Murray 3–8, Cousins 10
   (EPA/jugada sem. 10 +0.064, su mejor semana). Murray (isquiotibial grado 2) quizá (Yahoo, 16 nov). SF entrena en Colorado Springs por la altura;
   Mike Evans (tendinitis de Aquiles) incierto (Yardbarker, 16 nov). Azteca 2005–2022: favorito del mercado 5 de 5 (esperados 3.4).
   Altitud Denver 2002–2025: split local−visita DEN +5.24 vs resto +4.40 (n = 24 vs 744), p = 0.53; vs mercado −0.01, p = 0.99.
2) IND@HOU (jue 19, 20:15 ET = 19:15 CDMX). HOU 70.4% (59.0–80.7%), margen +7.2; sem. 7–10: 75.5%. HOU 3-6, 11°, Pitágoras 4.8,
   cerrados (≤8) 1-5: P(≤1 de 6 | 50%) = 0.109. IND 3-7, 28°, contra carrera 32°; HOU capturas defensivas 2° (9.2%). Jones vs Stroud (SI, 17 nov):
   IND en duda Gardner, Ward, Raimann; HOU Marks duda; Montgomery, Teller, Hunter, Harrison Jr., Al-Shaair en duda.
3) Rompemitos rachas (2002–2025, vs probabilidad del mercado): tras cortar 5+ derrotas (n = 158): ganó 32.9% vs 37.9% esperado; residuo −1.07, p = 0.31;
   tras cortar 8+ (31): p = 0.87; con 5+ derrotas seguidas, siguiente (564): 31.7% vs 34.3%, p = 0.55; 10+ (50): p = 0.14. BH: ninguna q < 0.55.
   NYJ@LAC dom 22: LAC 44.5% (34.7–53.0%). BAL (5 seguidas) en CAR: 41.6%.
4) Sorpresas semana 11 (13 partidos): favoritos esperados 8.52; sorpresas 4.48 (bootstrap 4.06–4.78); P(13 de 13) = 0.0038 (1 en 263).
   Distribución: 0–2: 11.8%, 3: 17.1%, 4: 22.7%, 5: 21.6%, 6+: 26.8%. Fuera de muestra sem. 4–10: 35 sorpresas vs 39.0 esperadas; dispersión χ² = 6.54,
   gl = 7, p = 0.48. Mercado 2010–2025: 5.0 sorpresas/semana; 1 de 277 semanas sin sorpresas. Más claro: KC 81.9% vs ARI; más parejos TB@DET 56.6%, BAL@CAR 58.4%."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1117")
LEGAL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
SEP = "vs. · récord · lugar en calidad real"


def covers():
    return {
        "1-nfl-min-sf-cdmx": slide(1, 6, "NFL · Semana 11 · Domingo 22 nov · 19:20 CDMX · Estadio Banorte",
            "Mejor defensa vs. mejor ataque, a 2,240 metros: nuestro modelo da 2 de cada 3 a San Francisco",
            [Matchup("Vikings", "7-2 · 13°", "49ers", "8-1 · 2°", sep=SEP),
             Stats([("66%", "gana San Francisco (58–74%)", GHOST),
                    ("3", "mariscales titulares de Minnesota", AMBER),
                    ("5 de 5", "favoritos ganaron en la CDMX (2005–2022)", ACC)])],
            takeaway="¿Pesa la altura? En Denver no vimos ventaja extra medible (p = 0.53). San Francisco igual entrena en Colorado.",
            style="cover", method=LEGAL, title_size=58),
        "2-nfl-ind-hou": slide(1, 6, "NFL · Semana 11 · Jueves 19 nov · 19:15 CDMX · Houston",
            "Houston va 3-6, pero perdió 5 de sus 6 partidos cerrados. Nuestro modelo le da 70%",
            [Matchup("Colts", "3-7 · 28°", "Texans", "3-6 · 11°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("70%", "gana Houston (59–81%)", GHOST),
                    ("1 de 9", "a volado: ganar 1 de 6 cerrados o menos", AMBER),
                    ("4.8", "victorias que merecen sus puntos. Tiene 3", ACC)])],
            takeaway="La defensa contra la carrera de Indianapolis es la peor de la liga. ¿Houston por fin cierra uno?",
            style="cover", method=LEGAL, title_size=62),
        "3-nfl-rachas": slide(1, 6, "NFL · Rompemitos · 2002–2025",
            "¿Cortar una mala racha despierta a un equipo? En 158 casos, no",
            [HBars([("Ganaron el siguiente", 32.9, ACC), ("Se esperaba antes", 37.9, GHOST)], 100, "{}%", 380),
             Stats([("p = 0.31", "tras cortar 5 o más derrotas seguidas: sin efecto", GHOST),
                    ("564", "partidos con racha de 5+: lo esperado", AMBER),
                    ("44%", "Chargers ante los Jets, tras cortar 11 seguidas", ACC)])],
            takeaway="Los Chargers cortaron su racha el lunes y Baltimore ya suma 5 derrotas. ¿Pesa la racha o la calidad?",
            style="cover", method=LEGAL, title_size=62),
        "4-nfl-sorpresas": slide(1, 6, "NFL · Semana 11 · 13 partidos · Probabilidad compuesta",
            "Que ganen los 13 favoritos de la semana sale 1 de cada 263 veces",
            [HBars([("0 a 2 sorpresas", 11.8, GHOST), ("3", 17.1, GHOST), ("4", 22.7, ACC), ("5", 21.6, ACC), ("6 o más", 26.8, GHOST)], 30, "{}%", 300),
             Stats([("4.5", "sorpresas esperadas", ACC),
                    ("35 vs 39", "reales vs. esperadas (sem. 4–10)", GHOST),
                    ("82%", "Kansas City, el favorito más claro", AMBER)])],
            takeaway="Los más parejos: Detroit 57% ante Tampa Bay y Carolina 58% ante Baltimore. ¿Dónde cae la sorpresa?",
            style="cover", method=LEGAL, title_size=56),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
