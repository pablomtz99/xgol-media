"""xGol — portadas de las 4 ideas del 13 nov. Diseño v7.
Datos NBA: marcadores 2026-27 (Land of Basketball oct–nov; 12 nov verificado con ESPN/AP/NBA.com/Yahoo; 174 partidos al 12 nov).
Modelo NBA v1 (models/nba_ridge_1103.py), rangos 10–90% bootstrap (400). Calibración fuera de muestra: 158 partidos, 114 aciertos
vs 104.1 esperados, Brier 0.198, Spiegelhalter p = 0.15.
SIN NFL: nflverse no accesible (sin add_repo; xgol-data tampoco). Futbol europeo y Liga MX: fecha FIFA (Liga MX regresa J17 tras la pausa).
ATP Finals arrancan el domingo 15. Por eso las 4 ideas son NBA, con 4 técnicas distintas.
Horarios: basketbols.com (Copa NBA, 13 nov, ET) y NBA.com (14 nov, 8:00 PM ET). CDMX = ET − 1 h.
1) GSW@SAS (vie 13, 21:30 ET = 20:30 CDMX; Copa NBA, Oeste C). SAS 68% (60–75%), margen +6.8. Racha de 10 de SAS (23 oct perdió;
   24 oct–11 nov ganó 10): probabilidades previas fuera de muestra .73 .84 .82 .55 .86 .79 .83 .57 .68 .83 → producto 0.049 (1 en 20),
   victorias esperadas 7.5 de 10. Copa: GSW +17, SAS +15 en diferencial (airalamo/basketbols). P(SAS por 3+) = 62%; por 10+ = 43%.
   Bajas: Curry fuera (desgarro oblicuo; ESPN/Charania: cerca de un mes), Butler, Moody, B. Williams fuera, Porzingis no viaja;
   SAS: Fox y Vassell duda, T. Harris y Quaintance fuera (airalamo). El modelo no ve lesiones.
2) NYK@IND (vie 13, 19:00 ET = 18:00 CDMX; Copa NBA, Este B). NYK 74% (68–80%), margen +9.5. NYK 6-5, +6.8 por partido; Pitágoras
   (exp. 14) 7.8 victorias; 5 victorias por 10+ y 0 derrotas por 10+; partidos por ≤6: 1-3 → P(≤1 de 4 | 50%) = 0.31 (azar compatible).
   Residuo vs. modelo fuera de muestra +4.0 por partido. Neto ajustado 8° (defensa 3°). IND 4-8, 24°. Bajas IND: Haliburton (isquiotibial),
   Sheppard, Furphy fuera; Nesmith día a día. NYK sin bajas (iHeart, reporte del 13 nov).
3) MIA doble jornada: CLE@MIA (vie 13, 20:00 ET = 19:00 CDMX; Copa, Este B: ambos 1-0) y DET@MIA (sáb 14, 20:00 ET = 19:00 CDMX).
   MIA vs CLE 42% (34–49%), margen −3.0. MIA vs DET 33% → con 2a noche seguida (lab: −2.1, p = 0.011) 28% (22–35%).
   Ambas: 0.418 × 0.284 = 0.119 (bootstrap 8–16%); ninguna 42%; exactamente una 46%. DET descansa el viernes (jugó 2OT el jueves).
   Giannis Antetokounmpo probable (muñeca); Klay Thompson y Larsson duda; CLE sin Mobley, Merrill, Tomlin (ClutchPoints, 13 nov).
   Ranking: CLE 10°, MIA 18°, DET 6°.
4) CHI@MIN (sáb 14, 20:00 ET = 19:00 CDMX). MIN 86% (79–90%), margen +15.8. CHI 1-9, −15.5 por partido (peor de la liga), 0-4 en
   partidos por ≤6; neto ajustado −7.0 (27°; bootstrap −9.2 a −4.9). Monte Carlo (400 escenarios del modelo × 72 partidos restantes vs
   rival promedio, mitad en casa): 24 victorias (18–31); P(≤20) = 24%; P(≥30) = 14%. MIN sin Edwards (artroscopia 29 oct; ESPN):
   6-1, +14.0 por partido vs +12.6 con él (5 partidos); Welch p = 0.88; residuos vs. modelo p = 0.97 → no se nota la baja."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1113")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta."
SEP = "visitan a · récord · lugar en calidad real"


def covers():
    return {
        "1-nba-gsw-sas": slide(1, 6, "NBA · Copa · Hoy viernes 13 nov · 20:30 CDMX · San Antonio",
            "San Antonio ganó 10 seguidos cuando eso salía 1 de cada 20. Esta noche recibe a Golden State sin Curry",
            [Matchup("Warriors", "8-4 · 12°", "Spurs", "10-2 · 1°", sep=SEP),
             Stats([("68%", "gana San Antonio (60–75%)", GHOST),
                    ("7.5 de 10", "victorias esperábamos en esa racha", AMBER),
                    ("62%", "gana por 3 o más: lo que pide la Copa", ACC)])],
            takeaway="Curry, fuera cerca de un mes, y nuestro modelo no ve lesiones; Fox y Vassell, en duda. ¿San Antonio ya es el mejor del Oeste?",
            style="cover", method=LEGAL_NBA, title_size=62),
        "2-nba-nyk-ind": slide(1, 6, "NBA · Copa · Hoy viernes 13 nov · 18:00 CDMX · Indianápolis",
            "Nueva York va 6-5, pero sus puntos dicen 8-3. Ganó 5 veces por 10 o más y no ha perdido así ni una",
            [Matchup("Knicks", "6-5 · 8°", "Pacers", "4-8 · 24°", sep=SEP),
             Stats([("74%", "gana Nueva York (68–80%)", GHOST),
                    ("7.8", "victorias que dan sus puntos (fórmula de Pitágoras)", ACC),
                    ("1-3", "en partidos por 6 o menos (p = 0.31: puede ser azar)", AMBER)])],
            takeaway="Indiana juega sin Haliburton; Nueva York, completo. ¿Los Knicks son mejores que su récord o les falta algo en los finales?",
            style="cover", method=LEGAL_NBA, title_size=62),
        "3-nba-mia-doble": slide(1, 6, "NBA · Viernes 13 y sábado 14 · 19:00 CDMX · Miami",
            "Miami recibe a Cleveland y a Detroit en 24 horas. Ganar las dos sale 1 de cada 8",
            [Matchup("Cavaliers", "6-6 · 10°", "Heat", "5-6 · 18°", sep=SEP),
             Stats([("42%", "gana Miami ante Cleveland (34–49%)", GHOST),
                    ("28%", "ante Detroit, en 2a noche seguida (22–35%)", AMBER),
                    ("12%", "gana las dos (8–16%); ninguna: 42%", ACC)])],
            takeaway="Giannis, probable pese a la muñeca; Cleveland sin Mobley; Detroit llega descansado. ¿Miami salva el fin de semana?",
            style="cover", method=LEGAL_NBA, title_size=64),
        "4-nba-chi-min": slide(1, 6, "NBA · Sábado 14 de noviembre · 19:00 CDMX · Minneapolis",
            "Chicago va 1-9 y pierde por 15.5 puntos. Simulamos su temporada: le da para 24 victorias",
            [Matchup("Bulls", "1-9 · 27°", "Timberwolves", "9-3 · 3°", sep=SEP),
             Stats([("86%", "gana Minnesota (79–90%)", GHOST),
                    ("18–31", "victorias de Chicago (80% de simulaciones)", ACC),
                    ("p = 0.88", "Minnesota sin Edwards: no se nota la baja", AMBER)])],
            takeaway="Minnesota va 6-1 sin Edwards y ganando por 14. Chicago, 0-4 en finales cerrados. ¿Cuántas gana Chicago este año?",
            style="cover", method=LEGAL_NBA, title_size=64),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
