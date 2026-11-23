"""xGol — portadas de las 4 ideas del 23 nov. Diseño v7. Cálculos en studio/models/*_1123.py. SIN xgol-data ni nflverse (add_repo no disponible; nflverse 403)
→ NFL con Modelo NFL v0-b (diferencial de puntos; sin EPA). Sin MLB (fuera de temporada). Tenis: Copa Davis Final 8 (mar 24, CZE–CAN) sin modelo propio → no.
No se repiten POR@PHI ni OKC@IND (ya propuestos el 22, sin elegir).
1) NFL MNF CIN (7-2) en WAS (3-5-1), lun 23, 19:15 CDMX. v0-b: CIN 63.8% (80%: 52–74%), margen +4.7; sens. factor 0.3–0.7: 57–70%. Pase CIN 298.8 yd (1°) vs WAS permite
   244.8 (31°). Puntos 30.9/21.4 vs 21.8/24.8. Pitágoras: CIN 6.3 esp vs 7 (p = 0.48) → el 7-2 se sostiene. Validación v0 (EPA): 67 de 102; v0-b sin validación propia.
2) NBA SAS (14-3) en SAC (2-14), lun 23, 21:00 CDMX. NBA v1 (SRS al 18 nov): SAS 85.5% (77–92%), margen +15.6; calidad 1° vs 28°; diferencia mayor que el 99.3% de los pares.
   Escenarios sin Wembanyama (−3) 80%; sin él y Fox (−5) 76% (ambos día a día, Sportbusy). P(por 10+) 65%. Validación v1: 69%, Brier 0.205 (n = 1,090).
3) UCL J5 martes 24, 14:00 CDMX. Modelo xGol UCL v0.1 + J4 completa (72 partidos): Arsenal–Dortmund 59.7/20.4/19.9 (80% L 54–64), Man City–Napoli 74.8/13.4/11.7 (66–80),
   Real Madrid–PSV 68.1/16.9/14.9 (61–74). Los 3 locales ganan: 30.4%. Validación fuera de muestra J4 (n = 18): Brier 0.501 vs 0.667 uniforme, 11 aciertos; P(mejora) = 99.7%.
   Bajas: ARS Saka, Zubimendi; MCI Nunes, Semenyo; NAP 7 + Marin suspendido; RMA Rodrygo, Mendy, Asencio (footballpredictions.com).
4) Liga MX Liguilla (cuartos 25–29 nov). Modelo xGol Liga MX v0 + Monte Carlo 200,000: campeón AME 23.1%, CHV 20.8%, CAZ 18.8%, TOL 15.3%, PAC 8.9%; sens. CHV 20–22%.
   Chivas pasa a semis 59.6% vs Pachuca (8° en tabla, +11 de diferencia: 4ª mejor). Histórico superlíder campeón 13 de 59 (22%; vs 1/8: p = 0.028), eliminado en cuartos 22 de 59 (37%)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1123")
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: ESPN, Fox Sports, commanders.com."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference, TeamRankings."
LEGAL_UCL = "Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta. Resultados: UEFA vía Sports Mole, NBC Sports."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla: El Imparcial, ESPN; histórico: Claro Sports, Excélsior."


def covers():
    return {
        "1-nfl-cin-was": slide(1, 6, "NFL · Lunes por la noche · Semana 11 · Hoy 19:15 CDMX · Washington",
            "El mejor ataque aéreo de la NFL visita a la 31ª defensa contra el pase",
            [Matchup("Cincinnati", "7-2 · +85", "Washington", "3-5-1 · −27", sep="visita a · récord · diferencia de puntos"),
             Stats([("64%", "gana Cincinnati (80%: 52–74%)", ACC),
                    ("299", "yardas por pase de Cincinnati: 1° de 32", AMBER),
                    ("245", "yardas por pase que permite Washington: 31°", NEG)])],
            takeaway="Su 7-2 no es suerte: sus puntos dicen 6.3 victorias (p = 0.48). ¿Burrow le gana a Daniels?",
            style="cover", method=LEGAL_NFL, title_size=56),
        "2-nba-sas-sac": slide(1, 6, "NBA · Lunes 23 · 21:00 CDMX · Spurs en Kings · Sacramento",
            "El 1° contra el 28°: Sacramento gana 1 de cada 7 veces",
            [Matchup("Spurs", "14-3 · 1°", "Kings", "2-14 · 28°", sep="visita a · récord · lugar en calidad real (nuestro ranking)"),
             Stats([("86%", "gana San Antonio (80%: 77–92%)", ACC),
                    ("+15.6", "puntos de margen esperado", AMBER),
                    ("76%", "sin Wembanyama ni Fox (día a día)", NEG)])],
            takeaway="¿Cuánto vale Wembanyama? Sin él ni Fox, la sorpresa pasa de 1 en 7 a 1 en 4.",
            style="cover", method=LEGAL_NBA, title_size=58),
        "3-ucl-martes": slide(1, 6, "Champions League · Jornada 5 · Martes 24 · 14:00 CDMX",
            "Arsenal, City y Madrid son favoritos. Que ganen los 3: 3 de cada 10",
            [HBars([("Arsenal vs Dortmund", 60, ACC), ("Man City vs Napoli", 75, ACC), ("Real Madrid vs PSV", 68, ACC), ("Ganan los 3", 30, AMBER)], 100, "{}%", 360),
             Stats([("0.50", "error fuera de muestra en la J4 (azar: 0.67)", ACC),
                    ("11 de 18", "favoritos acertados en esa jornada", GHOST),
                    ("8", "bajas de Napoli, 27° de 36", NEG)])],
            takeaway="Barras = probabilidad de que gane el local, según el modelo xGol. ¿Cuál de los tres se cae?",
            style="cover", method=LEGAL_UCL, title_size=56),
        "4-ligamx-liguilla": slide(1, 6, "Liga MX · Liguilla Apertura 2026 · Cuartos: 25 al 29 de noviembre",
            "Chivas es superlíder, pero América es el favorito al título",
            [HBars([("América (3°)", 23, ACC), ("Chivas (1°)", 21, ACC), ("Cruz Azul (2°)", 19, ACC), ("Toluca (5°)", 15, GHOST), ("Pachuca (8°)", 9, GHOST)], 30, "{}%", 380),
             Stats([("13 de 59", "superlíderes campeones en torneos cortos (22%)", AMBER),
                    ("40%", "Chivas cae ante Pachuca, 4° en goles", NEG)])],
            takeaway="Barras = probabilidad de ser campeón, según el modelo xGol (200,000 liguillas simuladas). ¿Rompe Chivas la maldición?",
            style="cover", method=LEGAL_MX, title_size=56),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
