"""xGol — portadas de las 4 ideas del 6 nov. Diseño v7.
NBA: modelo NBA v1 (studio/models/nba_ridge_1103.py) con 123 partidos 2026-27 al 5 nov (Land of Basketball oct/nov + ESPN 5 nov).
   Fuera de muestra (107): 67% aciertos, Brier 0.216, calibración Spiegelhalter p = 0.94. Rangos 10–90% por bootstrap (400).
   POR@LAL (vie 6, 21:00 CDMX, Copa NBA): LAL 58% (51–67%), margen +3.0, total 231. Portland 5-0 de visita: probabilidades previas
   .62/.42/.68/.43/.56 → P(5 de 5) = 0.036 (1 en 28); global 6-1 vs 3.94 esperadas, P(≥6) = 0.109. Ranking ajustado: POR 11°, LAL 6°.
   Contexto: iHeart/Fox Sports 990 (POR sin Morant, Sharpe, Krejci; Doncic 38.5 pts), SI.com (Copa NBA; Mamukelashvili en duda).
   NYK@CLE (sáb 7, hora por confirmar): CLE juega el vie 6 vs PHI → −2.1 (lab xgol-data, p = 0.011). Sin ajuste 52%; con ajuste CLE 47% (40–53%).
   Ataque CLE 2° / defensa NYK 3° (ajustados). Cavs en duda: Allen, Watson, Proctor (DK Network, 6 nov).
NFL: modelo NFL v0 con EPA por jugada de nflverse (sem. 1–9). CIN 66% (62–71% con regresión 0.35–0.65), mercado 60% sin margen.
   Sede neutral (nflverse games.csv, temporada regular 2003–2025, n = 66): favoritos ganaron 46 (esperado 41.6 por la línea; binomial
   p = 0.31); total real − esperado = −1.4 pts (p = 0.36); 'local' nominal 45% vs 46% esperado.
Liga MX: modelo xGol Liga MX v0 — Poisson por equipo con GF y GC por partido (tabla tras J15, vivoelfutbol.com.mx / futmx.com),
   encogido 50% a la media; localía supuesta ×1.15; desempate por diferencia de goles y goles a favor. 200,000 simulaciones.
   Partidos: SI.com (calendario de América, Chivas, Cruz Azul), sinembargo.mx (J16), playersoflife (Atlas J17 en Juárez).
   P(líder): América 41% (34–50%), Chivas 33% (26–40%), Cruz Azul 21% (17–25%), Atlas 5%; rango variando encogimiento 0.3–0.7 y localía 1.05–1.25."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1106")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta."
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. Datos: nflverse. No es recomendación de apuesta."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta."


def covers():
    return {
        "1-nba-por-lal": slide(1, 6, "NBA · Copa NBA · Hoy viernes 6 de noviembre · 21:00 CDMX",
            "Portland va 5-0 de visitante. Con sus probabilidades, eso pasa 1 de cada 28 veces",
            [Matchup("Trail Blazers", "6-1", "Lakers", "7-2", sep="visitan a · Los Ángeles · revancha del 27 oct (136-129)"),
             Stats([("58%", "gana Los Ángeles (51–67%)", GHOST),
                    ("38.5", "puntos por partido de Dončić", AMBER),
                    ("11°", "Portland en nuestro ranking ajustado", ACC)])],
            takeaway="Portland llega sin Morant ni Sharpe y su récord vale más que su nivel. Pero ya ganó en ese mismo piso. ¿Racha real o regresión?",
            style="cover", method=LEGAL_NBA, title_size=76),
        "2-nba-nyk-cle": slide(1, 6, "NBA · Sábado 7 de noviembre · Cleveland",
            "Una noche sin descanso le quita el favoritismo a Cleveland: de 52% a 47%",
            [Matchup("Knicks", "4-4", "Cavaliers", "4-4", sep="visitan a · Cleveland · 2ª noche seguida para los Cavaliers"),
             Stats([("53%", "gana Nueva York (47–60%)", GHOST),
                    ("−2.1", "puntos por 2 noches seguidas", AMBER),
                    ("2° vs 3°", "ataque Cavs vs. defensa Knicks", ACC)])],
            takeaway="El mejor ataque ajustado contra una de las mejores defensas, con Allen en duda. ¿Pesa más el cansancio o la localía?",
            style="cover", method=LEGAL_NBA, title_size=76),
        "3-nfl-cin-atl": slide(1, 6, "NFL · Semana 9 · Domingo 8 de noviembre · 8:30 CDMX · Madrid",
            "66 partidos de NFL en sede neutral: el viaje no cambió nada (p = 0.31)",
            [Matchup("Bengals", "5-2", "Falcons", "3-5", sep="vs. · Estadio Santiago Bernabéu · sin localía"),
             Stats([("66%", "gana Cincinnati (62–71%)", GHOST),
                    ("60%", "le da el mercado de predicción", MUTED),
                    ("5° vs 28°", "ataques en puntos por jugada (de 32)", ACC)])],
            takeaway="Rompemitos: fuera de casa los favoritos ganan lo esperado y no hay menos puntos. Entonces, ¿qué decide en Madrid?",
            style="cover", method=LEGAL_NFL, title_size=74),
        "4-mx-lider": slide(1, 6, "Futbol · Liga MX · Apertura 2026 · Jornada 16 · 7 y 8 de noviembre",
            "Tres empatados en 29 a dos fechas. América termina líder 4 de cada 10 veces",
            [Table(("Pts", "Líder"), [("América", "29", "41%"),
                                       ("Chivas", "29", "33%"),
                                       ("Cruz Azul", "29", "21%"),
                                       ("Atlas", "27", "5%")], colors=[GHOST, ACC]),
             Stats([("200 mil", "simulaciones, modelo xGol", GHOST),
                    ("34–50%", "rango de América", AMBER)])],
            takeaway="América tiene el mejor ataque (36 goles), pero cierra de visita en CU y Monterrey. Chivas y Cruz Azul se enfrentan en la última. ¿Quién te late?",
            style="cover", method=LEGAL_MX, title_size=76),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
