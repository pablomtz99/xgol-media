"""xGol — portadas de las 4 ideas del 12 nov. Diseño v7.
Datos NBA: marcadores 2026-27 (Land of Basketball oct–nov; 11 nov verificado con AP/ESPN/CBS/Yahoo, 2 marcadores corregidos;
170 partidos al 11 nov). Modelo NBA v1 (models/nba_ridge_1103.py), rangos 10–90% bootstrap (400). Calibración fuera de muestra:
154 partidos, 110 aciertos vs 101.4 esperados, Brier 0.201, Spiegelhalter p = 0.20.
SIN NFL (TNF Commanders–Giants hoy): nflverse no accesible (sin add_repo en esta sesión). Futbol: fecha FIFA (Nations League), sin
modelo/datos. Liga MX: pausa por fecha FIFA. ATP Finals desde el 15 nov.
1) NBA TOR@PHI (jue 12, 19:00 ET = 18:00 CDMX; Land of Basketball, Liberty Line). PHI 9-3 con +1.0 por partido; Pitágoras (exp. 14)
   6.4 victorias; partidos por ≤6 puntos 6-0 → P(6-0 | 50%) = 1/64 = 0.016; fuera de muestra esperábamos 6.1 de 11, ganó 8.
   Neto ajustado 14° (ataque 21°, defensa 8°; Liberty Line: ataque 20°, defensa 8°). Con solo datos 2026-27: −2.7.
   PHI 53% (44–61%), margen +1.0; TOR en 2a noche seguida (jugó 11 nov en casa vs BOS) → lab −2.1 → PHI 58% (50–66%, rango desplazado).
   Bajas: Embiid (pie) y LeBron James (espalda) dudas; PHI fuera Bona, Barlow, Hukporti; TOR fuera Kawhi Leonard (rodilla) (Liberty Line).
2) NBA DAL@MIN (jue 12, 20:00 ET = 19:00 CDMX). MIN 73% (65–79%), margen +8.8. Edwards fuera desde artroscopia (29 oct; ESPN: hasta 2 meses).
   MIN sin Edwards (desde 30 oct): 5-1, +9.8 por partido; residuo vs. modelo fuera de muestra +3.5 (con Edwards, 4 partidos: +15.9);
   Welch t = 1.49, p = 0.19 → inconcluso. DAL 7-4, +4.6 por partido, pero neto ajustado −1.3 (18°): solo datos 2026-27 +6.1;
   prior (26 victorias) −5.0. Lively fuera (Sports Mole). Ambos descansados.
3) NBA GSW@SAS (vie 13, 21:30 ET = 20:30 CDMX). SAS 67% (60–74%), margen +6.6. Racha de 8 de GSW (26 oct–9 nov; AP: la más larga desde 2022)
   con probabilidades previas fuera de muestra: producto 0.0027 (1 en 366), victorias esperadas 4.0 de 8. Neto GSW: prior −1.3 → hoy +3.0
   (solo 2026-27: +10.4). Curry salió con molestia abdominal derecha, resonancia sin resultado (AP/KRRO: "Concern is high" — Kerr).
   SAS 1° neto (+8.1), 10-2. El modelo no ve lesiones.
4) NBA OKC@LAC (vie 13, 22:30 ET = 21:30 CDMX; Copa NBA, fase de grupos; AP). OKC 69% (59–76%), margen +7.1. Dos derrotas en Portland
   (62% y 56% previos) → P(ambas) = 0.38 × 0.44 = 0.165 (1 en 6). Neto OKC antes del 10 nov +8.3 → hoy +7.0 (3°; defensa 1°).
   Calendario más duro de los 4 (rivales +1.70). Bajas OKC: Wallace, Holmgren, Jaylin y Jalen Williams fuera; Sorber y Mitchell día a día.
   LAC 2-8 sin Ingram ni Beal (AP)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1112")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta."


def covers():
    return {
        "1-nba-tor-phi": slide(1, 6, "NBA · Hoy jueves 12 de noviembre · 18:00 CDMX · Philadelphia",
            "Philadelphia va 9-3, pero sus puntos dicen 6-6. Ganó sus 6 partidos cerrados: eso sale 1 de cada 64",
            [Matchup("Raptors", "5-6 · 13°", "76ers", "9-3 · 14°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("58%", "gana Philadelphia (50–66%), ya con el cansancio", GHOST),
                    ("+1.0", "puntos por partido de diferencia: de media tabla", AMBER),
                    ("6-0", "en partidos por 6 o menos (p = 0.016)", ACC)])],
            takeaway="Toronto juega su segunda noche seguida y sin Kawhi; Embiid y LeBron, en duda. ¿Philadelphia es contendiente o ha tenido suerte?",
            style="cover", method=LEGAL_NBA, title_size=62),
        "2-nba-dal-min": slide(1, 6, "NBA · Hoy jueves 12 de noviembre · 19:00 CDMX · Minneapolis",
            "Sin Anthony Edwards, Minnesota va 5-1. Nuestro modelo le da 73% ante un Dallas que engaña",
            [Matchup("Mavericks", "7-4 · 18°", "Timberwolves", "8-3 · 6°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("73%", "gana Minnesota (65–79%)", GHOST),
                    ("p = 0.19", "¿bajó sin Edwards? Inconcluso (6 partidos)", ACC),
                    ("+6.1 vs. −1.3", "Dallas: nivel de este año vs. el que le damos", AMBER)])],
            takeaway="Dallas va 7-4 ganando por 4.6, pero viene de 26 victorias. ¿Le creemos a 11 partidos o a una temporada entera?",
            style="cover", method=LEGAL_NBA, title_size=62),
        "3-nba-gsw-sas": slide(1, 6, "NBA · Viernes 13 de noviembre · 20:30 CDMX · San Antonio",
            "Golden State ganó 8 seguidos cuando eso salía 1 de cada 366. Ahora visita al mejor equipo, quizá sin Curry",
            [Matchup("Warriors", "8-4 · 12°", "Spurs", "10-2 · 1°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("67%", "gana San Antonio (60–74%), antes de saber de Curry", GHOST),
                    ("4.0", "victorias esperábamos en esa racha de 8", AMBER),
                    ("−1.3 → +3.0", "cómo subió su nivel en nuestro modelo", ACC)])],
            takeaway="Curry salió en el primer cuarto con molestia abdominal y Kerr dijo «la preocupación es alta». ¿Cuánto vale él solo?",
            style="cover", method=LEGAL_NBA, title_size=62),
        "4-nba-okc-lac": slide(1, 6, "NBA · Copa NBA · Viernes 13 de noviembre · 21:30 CDMX · Los Ángeles",
            "Dos derrotas seguidas en Portland. ¿Crisis en Oklahoma City? Nuestro modelo aún le da 69%",
            [Matchup("Thunder", "8-4 · 3°", "Clippers", "2-8 · 20°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("69%", "gana Oklahoma City (59–76%)", GHOST),
                    ("1 en 6", "probabilidad previa de perder las dos en Portland", AMBER),
                    ("1°", "su defensa ajustada por rival", ACC)])],
            takeaway="Juega sin Holmgren ni los dos Williams; los Clippers, sin Ingram ni Beal. ¿Bache de dos noches o algo más?",
            style="cover", method=LEGAL_NBA, title_size=66),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
