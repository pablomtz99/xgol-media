"""xGol — portadas de las 4 ideas del 5 nov. Diseño v7.
NBA: modelo NBA v1 (studio/models/nba_ridge_1103.py) con 121 partidos 2026-27 al 4 nov (Land of Basketball; local/visita
   verificados contra el calendario oficial NBA). Fuera de muestra (105 partidos): 67% aciertos, Brier 0.217.
   Rangos 10–90% por bootstrap (300). Cansancio: −2.1 pts al margen por 2ª noche seguida (lab xgol-data, 2025-26, p = 0.011).
   76ers 8-1: Poisson-binomial con la prob. previa a cada partido (modelo ajustado solo con partidos anteriores) → P(≥8) = 0.030.
   Grizzlies: margen +10.8 vs −0.5 esperado por el punto de partida (25 victorias 2025-26): z = 2.16, p = 0.015 (una cola);
   con 30 equipos, P(al menos uno así) ≈ 37%. Calendario: rivales con nivel promedio −4.85 (el más fácil de 30).
   Contexto: hoopsnightly.com/injuries (4 nov), Yahoo Sports, Eric Nehm (Giannis, muñeca), Land of Basketball (Heat–Clippers TE).
NFL: modelo NFL v0 (PLAYBOOK) con EPA por jugada de SumerSports (actualizado 4 nov): CIN ataque 0.07 / defensa −0.04;
   ATL ataque −0.13 / defensa −0.08. Sede neutral (Madrid): sin localía. Margen = 0.5 × 0.16 × 61.6 = 4.9 → Φ(4.9/13.5) = 64%;
   rango 60–68% con factor de regresión 0.35–0.65. Mercado: 62% sin margen de la casa. Contexto: SI.com (récords, Burrow, lesiones)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1105")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta."
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. Datos: SumerSports. No es recomendación de apuesta."


def covers():
    return {
        "1-nba-mia-gsw": slide(1, 6, "Basquetbol · NBA · Hoy jueves 5 de noviembre · 21:00 CDMX",
            "Miami jugó tiempo extra anoche en Los Ángeles. Hoy repite en San Francisco",
            [Matchup("Heat", "3-5", "Warriors", "5-3", sep="visita a · 2ª noche seguida para Miami"),
             Stats([("63%", "gana Golden State con el ajuste (55–70%)", GHOST),
                    ("−2.1", "puntos por 2 noches seguidas (p = 0.011)", AMBER),
                    ("25°", "defensa de Miami, ajustada (de 30)", ACC)])],
            takeaway="Sin cansancio, el modelo dice 58%; con él, 63%. Pero Golden State juega sin Butler ni Porziņģis y Giannis está en duda. ¿Qué pesa más?",
            style="cover", method=LEGAL_NBA, title_size=78),
        "2-nba-phi-cle": slide(1, 6, "Basquetbol · NBA · Viernes 6 de noviembre · 18:30 CDMX",
            "Filadelfia va 8-1. Con sus probabilidades, eso pasa 1 de cada 34 veces",
            [Matchup("76ers", "8-1", "Cavaliers", "4-4", sep="visitan a · Cleveland"),
             Stats([("55%", "gana Cleveland (50–60%)", GHOST),
                    ("4.9", "victorias esperadas en 9; tiene 8", AMBER),
                    ("+5.8", "puntos por partido: cerrado (p = 0.13)", ACC)])],
            takeaway="Regresión a la media: su diferencia de puntos es de equipo bueno, no de 8-1. Pero el miércoles le ganaron al n.º 1 del modelo. ¿Son reales?",
            style="cover", method=LEGAL_NBA, title_size=80),
        "3-nba-okc-mem": slide(1, 6, "Basquetbol · NBA · Viernes 6 de noviembre · 19:00 CDMX",
            "Memphis va 6-2 y gana por 10.8. Tuvo el calendario más fácil de la NBA",
            [Matchup("Thunder", "6-2", "Grizzlies", "6-2", sep="visita a · Memphis"),
             Stats([("67%", "gana Oklahoma City (59–76%)", GHOST),
                    ("p = 0.015", "su +10.8 vs. lo esperado: indicio, no prueba", AMBER),
                    ("20°", "Memphis en nuestro ranking ajustado", ACC)])],
            takeaway="Ojo: OKC juega sin Holmgren, Jalen Williams ni Wallace, y el modelo no ve bajas. ¿Memphis es real o fue el calendario?",
            style="cover", method=LEGAL_NBA, title_size=80),
        "4-nfl-cin-atl": slide(1, 6, "NFL · Semana 9 · Domingo 8 de noviembre · 8:30 CDMX",
            "La NFL en el Bernabéu: Burrow y sus 20 pases de touchdown contra un ataque que no anotó la semana pasada",
            [Matchup("Bengals", "5-2", "Falcons", "3-5", sep="vs. · Estadio Santiago Bernabéu, Madrid · sin localía"),
             Stats([("64%", "gana Cincinnati, nuestro modelo NFL (60–68%)", GHOST),
                    ("62%", "le da el mercado de predicción", MUTED),
                    ("6° vs 26°", "ataques en puntos por jugada (de 32)", ACC)])],
            takeaway="Atlanta perdió 16-0 con 8 pases completos, pero su defensa es 9ª. ¿Burrow conquista Madrid?",
            style="cover", method=LEGAL_NFL, title_size=70),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
