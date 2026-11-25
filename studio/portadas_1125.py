"""xGol — portadas de las 4 ideas del 25 nov. Diseño v7. Cálculos en studio/models/*_1125.py (+ ucl_j5_mie_1124.py). Sin xgol-data (repo no adjunto en esta corrida); nflverse SÍ.
1) NFL Black Friday vie 27, DEN (8-2) en PIT (6-4), 14:00 CDMX. NFL v0: PIT 54.7% (80%: 45–64). DEN 6-0 en partidos por ≤8 pts; Pitágoras 5.7 victorias (P(≥8) = 0.12).
   Regresión a la media nflverse 2010-25: 18 equipos con ≥2 victorias sobre Pitágoras tras 10 juegos: 80.6% → 56.6% el resto (t = −3.98, p = 0.0004); el récord no añade
   nada sobre los puntos (t = 0.9 vs 5.3). Mercado (diferencial DEN −3, SI) ≈ DEN 59%. Validación v0 sem 4-11: 77 de 114, Brier 0.223.
2) NBA mié 25, MIN (13-5) en OKC (10-8), 18:30 CDMX. NBA v1 (SRS al 19 nov): OKC 55.6% (43–68); con bajas (OKC sin Holmgren, J. Williams, Wallace; MIN sin Edwards) ≈ 53%.
   OKC 10-8 vs nivel de 64 victorias: P(≤10 de 18) = 0.14 → cabe en el azar.
3) Liga MX cuartos ida jue 26, Pachuca (8°) vs Chivas (1°) 19:00. Liga MX v0: Chivas avanza 59.3% (sens 59–60%); Pachuca gana la ida 44.9%; si Pachuca gana por 2+, Chivas avanza 17%.
   Superlíder eliminado en cuartos 22 de 59 (37%); vs modelo 41%: binomial p = 0.69 (consistente).
4) UCL J5 mié 25 14:00 CDMX: Sporting–Man Utd 55.6/20.7/23.8 (80% L 48–63). Goles esp. 2.14–1.35. United: 15 goles recibidos en sus últimos 5 (Goal); P(recibe 2+) 63%.
   Opta: Sporting 39.5%. Validación UCL v0.1 J4 n = 18: Brier 0.50 vs 0.67."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1125")
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference, KFAN, Sportsmole."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla y horarios: ESPN; histórico: Claro Sports, Excélsior."
LEGAL_UCL = "Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta. Resultados: UEFA vía Sports Mole, NBC Sports; forma: Goal."


def covers():
    return {
        "1-nfl-den-pit": slide(1, 6, "NFL · Black Friday · Viernes 27 · 14:00 CDMX · Broncos en Steelers",
            "Denver es 8-2, pero sus puntos dicen 5.7. Nuestro modelo va con Pittsburgh",
            [Matchup("Broncos", "8-2", "Steelers", "6-4 · 4-0 en casa", sep="visita a · récord"),
             Stats([("55%", "gana Pittsburgh (80%: 45–64%)", ACC),
                    ("6-0", "Denver en partidos decididos por 8 o menos", AMBER),
                    ("81% → 57%", "así cayeron 18 equipos con récord inflado (2010-25)", NEG)])],
            takeaway="Ganar 6 de 6 cerrados con una moneda pasa 1 de cada 64 veces. ¿Talento o suerte?",
            style="cover", method=LEGAL_NFL, title_size=54),
        "2-nba-min-okc": slide(1, 6, "NBA · Hoy miércoles 25 · 18:30 CDMX · Wolves en Thunder",
            "El campeón va 10-8 y llega sin Holmgren ni Jalen Williams. ¿Crisis o azar?",
            [Matchup("Timberwolves", "13-5", "Thunder", "10-8", sep="visita a · récord"),
             Stats([("53%", "gana Oklahoma City con las bajas de hoy (sin ellas, 56%)", ACC),
                    ("p = 0.14", "10-8 con nivel de campeón: cabe en el azar", GHOST),
                    ("Fuera", "Anthony Edwards: Minnesota también llega incompleto", NEG)])],
            takeaway="Oklahoma City ganó 64 el año pasado. Nuestro modelo dice que sigue siendo top 3. ¿Le crees?",
            style="cover", method=LEGAL_NBA, title_size=54),
        "3-ligamx-pachuca-chivas": slide(1, 6, "Liga MX · Cuartos de final, ida · Jueves 26 · 19:00 CDMX",
            "Chivas terminó 1°, pero pierde la ida en Pachuca 45 de cada 100 veces",
            [Matchup("Pachuca", "8° · +11", "Chivas", "1° · +12", sep="recibe a · lugar · diferencia de goles"),
             Stats([("59%", "avanza Chivas (rango 59–60%)", ACC),
                    ("17%", "si Pachuca gana la ida por 2 o más", NEG),
                    ("22 de 59", "superlíderes eliminados en cuartos", AMBER)])],
            takeaway="Pachuca fue 8° con la cuarta mejor diferencia de goles. ¿El octavo más peligroso de la Liguilla?",
            style="cover", method=LEGAL_MX, title_size=54),
        "4-ucl-sporting-united": slide(1, 6, "Champions League · Jornada 5 · Hoy miércoles 25 · 14:00 CDMX",
            "United recibió 15 goles en 5 partidos. Sporting gana más del doble de veces",
            [Matchup("Sporting", "10° · 9 pts", "Man Utd", "17° · 6 pts", sep="recibe a · lugar en la tabla · puntos"),
             Stats([("56%", "gana Sporting (80%: 48–63%)", ACC),
                    ("24%", "gana United", AMBER),
                    ("63%", "que United reciba 2 o más goles", NEG)])],
            takeaway="Primer partido de Champions de Pochettino con United, sin Cunha ni Šeško. ¿Reacción o goleada?",
            style="cover", method=LEGAL_UCL, title_size=56),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
