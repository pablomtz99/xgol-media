"""xGol — portadas de las 4 ideas del 10 nov. Diseño v7.
Datos NBA: marcadores 2026-27 (Land of Basketball, 154 partidos al 9 nov). Modelo NBA v1 (models/nba_ridge_1103.py), rangos 10–90%
por bootstrap (400). Calibración fuera de muestra: 138 partidos, 98 aciertos vs 91.2 esperados, Brier 0.202, Spiegelhalter p = 0.30.
1) NBA OKC@POR, dos partidos seguidos en Moda Center (mar 10, 23:00 ET = 22:00 CDMX; mié 11, 22:00 ET = 21:00 CDMX; sportbusy/LoB).
   OKC 62% por partido (50–73%), margen +4.4, total 225. Monte Carlo 200k con incertidumbre de bootstrap compartida:
   OKC 2-0 39%, 1-1 46%, POR 2-0 15%. Defensa ajustada OKC 1°; ataque ajustado POR 7°. POR 5-1 de visita, 1-2 en casa.
   Lesiones (iHeart/Rip City Radio, 10 nov): OKC fuera Jalen Williams, Cason Wallace, Chet Holmgren; POR fuera Sharpe, Krejci, Morant.
2) NBA BOS@PHI (mar 10, 20:00 ET = 19:00 CDMX). BOS 58% (50–66%), margen +3.0. PHI 9-2 con +3.1 por partido (BOS 8-2, +10.7).
   Poisson-binomial con probabilidades previas (fuera de muestra): PHI 6.09 victorias esperadas, P(≥9) = 0.058 (1 en 17).
   Pitágoras (exp. 14): 6.6. 7 de sus 9 triunfos por ≤8 pts. Ajustados: BOS defensa 3°, PHI ataque 21°. Lesiones: iHeart (Fox Sports 1300).
3) NBA LAL@MIL (mié 11, 20:00 ET = 19:00 CDMX). LAL 77% (71–82%), margen +10.9. LAL 10-2 vs 7.56 esperadas (P(≥10) = 0.114);
   ataque ajustado 1°, defensa 11°. MIL 1-9, −13.2 por partido (ataque 24°, defensa 27°). Reaves 43 pts sin Dončić (espalda) el 8 nov (Yahoo).
4) NFL power ranking S10 (nflverse pbp 2026, sem. 1–9; ridge λ=3 sobre EPA por jugada ajustada por rival). Validación rodante sem. 4–9:
   87 partidos, 63% aciertos, Brier 0.229. DEN 7-2, 12° (bootstrap por partido 10–90%: 7°–20°), 6-0 en partidos por ≤8; Pitágoras 4.8
   (P(≥7) = 0.13). TB 3-6, 9° (5°–17°), 1-6 en cerrados; Pitágoras 5.2 (P(≤3) = 0.13). Persistencia (games.csv 2010–2025, n = 392):
   r = 0.04, p = 0.42. TNF WAS@NYG (jue 12, 20:15 ET = 19:15 CDMX): NYG 57% (49–65%); NYG 5-2-1, 21° en calidad.
   Contexto: reporte Giants 9 nov — McCarthy (cadera) limitado; Daniels (WAS) práctica completa."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1110")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta."
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. Datos: nflverse. No es recomendación de apuesta."


def covers():
    return {
        "1-nba-okc-por-x2": slide(1, 6, "NBA · Mar 10 (22:00) y Mié 11 (21:00 CDMX) · Portland",
            "Dos noches seguidas, mismo duelo. Nuestro modelo: Oklahoma City barre 4 de cada 10 veces",
            [Matchup("Thunder", "8-2", "Trail Blazers", "6-3", sep="visitan a · Portland · dos partidos en 24 horas"),
             Stats([("62%", "gana Oklahoma City cada noche (50–73%)", GHOST),
                    ("46%", "se reparten uno y uno", AMBER),
                    ("15%", "Portland gana los dos", ACC)])],
            takeaway="La mejor defensa de la liga llega sin Holmgren, Jalen Williams ni Wallace; Portland, sin Sharpe ni Morant. ¿Quién aguanta dos noches?",
            style="cover", method=LEGAL_NBA, title_size=70),
        "2-nba-bos-phi": slide(1, 6, "NBA · Hoy martes 10 de noviembre · 19:00 CDMX · Philadelphia",
            "Philadelphia va 9-2; nuestras probabilidades esperaban 6-5. Un récord así sale 1 de cada 17 veces",
            [Matchup("Celtics", "8-2 · +10.7", "76ers", "9-2 · +3.1", sep="visitan a · Philadelphia · récord y puntos por partido"),
             Stats([("58%", "gana Boston (50–66%)", GHOST),
                    ("7 de 9", "triunfos de Philadelphia por 8 puntos o menos", AMBER),
                    ("3°", "defensa de Boston, ajustada por rival", ACC)])],
            takeaway="Philadelphia gana apretado; Boston gana por paliza. ¿Qué pesa más esta noche: el récord o la diferencia de puntos?",
            style="cover", method=LEGAL_NBA, title_size=70),
        "3-nba-lal-mil": slide(1, 6, "NBA · Mañana miércoles 11 de noviembre · 19:00 CDMX · Milwaukee",
            "El mejor ataque de la NBA con una defensa del montón. En Milwaukee, los Lakers ganan 3 de cada 4",
            [Matchup("Lakers", "10-2 · mejor récord", "Bucks", "1-9 · −13.2", sep="visitan a · Milwaukee"),
             Stats([("77%", "gana Los Ángeles (71–82%)", GHOST),
                    ("1° / 11°", "ataque / defensa de Lakers, ajustados", AMBER),
                    ("7.6", "victorias esperábamos de los Lakers; llevan 10", ACC)])],
            takeaway="Sin Dončić, Reaves metió 43 en Detroit. Un 10-2 así pasa 1 de cada 9 veces: ¿talento o calendario amable?",
            style="cover", method=LEGAL_NBA, title_size=70),
        "4-nfl-ranking-s10": slide(1, 6, "NFL · Power ranking · Semana 10 · Ajustado por rival",
            "Denver va 6-0 en partidos cerrados y Tampa 1-6. En 392 temporadas, eso no predijo nada",
            [Matchup("Broncos", "7-2 · 12°", "Buccaneers", "3-6 · 9°", sep="récord · lugar en calidad real (ajustado por rival)"),
             Stats([("1 en 64", "probabilidad de un 6-0 a puro volado", AMBER),
                    ("r = 0.04", "lo que predicen los cerrados (p = 0.42)", ACC),
                    ("57%", "Giants vs. Washington el jueves (49–65%)", GHOST)])],
            takeaway="Los Giants van 5-2-1 pero son 21° en calidad, y el jueves reciben a Washington. ¿Quién es contendiente de verdad?",
            style="cover", method=LEGAL_NFL, title_size=70),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
