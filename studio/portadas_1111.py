"""xGol — portadas de las 4 ideas del 11 nov. Diseño v7.
Datos NBA: marcadores 2026-27 (Land of Basketball oct–nov + ESPN/AP para el 10 nov; 160 partidos al 10 nov). Modelo NBA v1
(models/nba_ridge_1103.py), rangos 10–90% por bootstrap (400). Calibración fuera de muestra: 144 partidos, 103 aciertos vs 95.0
esperados, Brier 0.201, Spiegelhalter p = 0.25.
SIN NFL hoy: nflverse no fue accesible desde esta sesión (repos de GitHub fuera de alcance); futbol europeo y Liga MX en Fecha FIFA;
ATP Finals empieza el 15 nov.
1) NBA OKC@POR (mié 11, 22:00 ET = 21:00 CDMX; Land of Basketball). Revancha tras POR 123-103 OKC (10 nov; ESPN, SI: Lillard 25,
   Avdija 24; SGA 26). OKC 56% (45–68%), margen +2.3; antes del martes 62% (−6 pts). Rebote tras perder por 20+ (2026-27, residuo
   fuera de muestra del siguiente partido): n = 36, +2.6 pts, t = 1.19, p = 0.24 → no probado. Ambos en segunda noche seguida.
   Bajas (SI/OKC injury report): OKC fuera Holmgren, Jalen Williams, Wallace, Jaylin Williams, Sorber, Topic; POR fuera Sharpe, Morant, Krejci.
2) NBA GSW@HOU (mié 11, 21:30 ET = 20:30 CDMX; iHeart). Ambos 8-3; diferencial +9.2 (GSW) y +9.1 (HOU). HOU 64% (55–72%), margen +5.3
   = 1.6 localía + 3.6 calidad ajustada. Calidad de rivales (neto medio): HOU +2.2, GSW +0.8. GSW 7 de 11 en casa, HOU 6 de 11.
   Con solo datos 2026-27 (ridge λ≈0): GSW +11.0, HOU +12.3; el modelo conserva ~36% del arranque de GSW (prior 37 victorias).
   GSW: 16.5 triples por partido (1°), 40.3% (1°), Curry 30.6 pts. Bajas (iHeart): GSW fuera Butler, Porzingis, Moody, Payton II,
   B. Williams; Richard día a día. HOU fuera Adams, Capela.
3) NBA CLE@NYK (mié 11, 19:00 ET = 18:00 CDMX; Hoops Wire). NYK 60% sin ajuste (53–67%), margen +3.8. NYK en segunda noche seguida
   (ganó 117-85 a MIL el 10 nov); CLE descansó. Lab (xgol-data, 2025-26): back-to-back −2.1 al margen (p = 0.011) → NYK 55% (47–62%).
   Ajustados: CLE ataque 3°, defensa 16°; NYK ataque 16°, defensa 2°. Sábado 7 nov: NYK 109-97 en CLE. Bajas: NYK fuera Josh Hart;
   CLE fuera Merrill, Tomlin; Tyson duda; Allen regresa (Hoops Wire, iHeart).
4) NBA power ranking semana 4 (160 partidos). 1° Spurs 9-2 (rango bootstrap 1°–4°), 7° Lakers 10-2 (3°–10°), 14° 76ers 9-3 (11°–17°),
   21° Grizzlies 7-3 (15°–22°; 8° con solo datos de este año; calendario más fácil de la liga, rivales −2.95). Correlación récord–calidad
   r = 0.88. El modelo conserva ~1/3 del arranque (GSW 36%, MEM 32%), en línea con el laboratorio (arranque explica ~27% del margen
   futuro, r = 0.40). Jueves DAL@MIN (20:00 ET = 19:00 CDMX): MIN 73% (65–80%); DAL 7-4, 17°."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1111")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta."


def covers():
    return {
        "1-nba-okc-por-revancha": slide(1, 6, "NBA · Hoy miércoles 11 de noviembre · 21:00 CDMX · Portland",
            "Perdió por 20 y repite hoy en la misma cancha. Nuestro modelo aún ve arriba a Oklahoma City",
            [Matchup("Thunder", "8-3", "Trail Blazers", "7-3", sep="visitan a · Portland · segunda noche seguida"),
             Stats([("56%", "gana Oklahoma City (45–68%)", GHOST),
                    ("−6", "puntos le quitó la paliza (antes 62%)", AMBER),
                    ("p = 0.24", "el «rebote» tras perder por 20: no probado", ACC)])],
            takeaway="Lillard metió 25 y Avdija 24. Oklahoma City sigue sin Holmgren ni Jalen Williams. ¿Revancha o Portland otra vez?",
            style="cover", method=LEGAL_NBA, title_size=68),
        "2-nba-gsw-hou": slide(1, 6, "NBA · Hoy miércoles 11 de noviembre · 20:30 CDMX · Houston",
            "Mismo récord, misma diferencia de puntos. Aun así, Houston gana 64 de cada 100",
            [Matchup("Warriors", "8-3 · +9.2", "Rockets", "8-3 · +9.1", sep="visitan a · Houston · récord y puntos por partido"),
             Stats([("64%", "gana Houston (55–72%)", GHOST),
                    ("7 de 11", "partidos de Golden State fueron en casa", AMBER),
                    ("+2.2 / +0.8", "nivel de rivales: Houston los tuvo más duros", ACC)])],
            takeaway="Golden State mete más triples que nadie (16.5 por partido), pero llega sin Butler, Porzingis ni Moody. ¿Le alcanza a Curry?",
            style="cover", method=LEGAL_NBA, title_size=70),
        "3-nba-cle-nyk": slide(1, 6, "NBA · Hoy miércoles 11 de noviembre · 18:00 CDMX · Nueva York",
            "El 3er mejor ataque contra la 2a mejor defensa. Y Nueva York juega su segunda noche seguida",
            [Matchup("Cavaliers", "5-6", "Knicks", "6-4", sep="visitan a · Nueva York · revancha del sábado (NY 109-97)"),
             Stats([("55%", "gana NY, con ajuste por cansancio (47–62%)", GHOST),
                    ("−2.1", "puntos cuesta jugar dos noches seguidas (p = 0.011)", AMBER),
                    ("3° vs. 2°", "ataque de Cleveland vs. defensa de NY", ACC)])],
            takeaway="Cleveland viene de perder por 12 en Charlotte; Nueva York, de ganar por 32, y hoy no tiene a Josh Hart. ¿Gana el ataque o la defensa?",
            style="cover", method=LEGAL_NBA, title_size=66),
        "4-nba-ranking-s4": slide(1, 6, "NBA · Power ranking · Semana 4 · Ajustado por rival",
            "Los Lakers van 10-2 y son 7°. Memphis va 7-3 y es 21°. Así se ve la NBA sin el ruido del récord",
            [Matchup("Spurs", "9-2 · 1°", "Lakers", "10-2 · 7°", sep="récord · lugar en calidad real (ajustado por rival)"),
             Stats([("1 de 3", "del arranque cuenta; el resto es regresión a la media", AMBER),
                    ("21°", "Memphis: 7-3 con el calendario más fácil de la liga", NEG),
                    ("103 de 144", "aciertos fuera de muestra (calibrado)", ACC)])],
            takeaway="El jueves, Minnesota (6°) recibe a Dallas (7-4, pero 17°): 73% para Minnesota. ¿Quién es contendiente de verdad?",
            style="cover", method=LEGAL_NBA, title_size=64),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
