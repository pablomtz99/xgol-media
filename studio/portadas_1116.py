"""xGol — portadas de las 4 ideas del 16 nov (NFL tras la semana 10). Diseño v7. Cálculos: studio/models/nfl_1116.py.
Datos: nflverse (CC-BY 4.0) games.csv 2002–2026 + play_by_play_2026 (semanas 1–10, 18,328 jugadas de pase/carrera).
Modelo NFL v0: margen = 0.5 × (EPA neta/jugada local − visitante) × 61.6 + 1.5; P = Φ(margen/13.5). Rangos 10–90%: bootstrap de partidos (400).
Validación fuera de muestra 2026 (semanas 4–10, solo datos previos): 100 partidos, 65 aciertos vs 63.2, Brier 0.224 (80%: 0.207–0.242), Spiegelhalter p = 0.98.
SIN NBA (xgol-data no accesible: add_repo no disponible; ESPN pidió permiso y no hubo respuesta) y SIN tenis (ATP Finals en curso, pero sin fuente
verificable de datos punto a punto: el repo de Sackmann bloqueado por el proxy y Tennis Abstract pidió permiso). Futbol: fecha FIFA; Liga MX vuelve el 20 nov.
1) LAC@BAL (lun 16, 20:15 ET = 19:15 CDMX). BAL 72.7% (58–85%), margen +8.2. Solo semanas 6–10: 64.4% (margen +5.0).
   Calidad: LAC 32° (EPA neta −0.248; pase 32°, carrera 30°, éxito 32°); BAL 19° (−0.032). Ataque BAL: +0.186 sem. 1–4 (Jackson) vs −0.172 sem. 5–9 (29° desde sem. 5).
   BAL: Brissett 1er inicio con BAL (traspaso desde ARI, WMAR 11 nov); 4° titular distinto en 4 partidos (Huntley sem. 7, Jackson sem. 8 —se lesionó—,
   Fagnano sem. 9; pbp nflverse); Jackson (pulgar) y Huntley (dedo del pie) en IR. LAC: Herbert juega (dedo, rayos X negativos); McConkey fuera (Yahoo, Covers).
   BAL 4-5, 4 derrotas seguidas (43-117). Equipos 0-8+ 2002–2025: 15; solo 2 terminaron sin ganar; en sus partidos con 0-8+ ganaron 13 de 59 vs 16.9
   esperados por el mercado antes del partido; margen −1.5 vs esperado, p = 0.36. Monte Carlo (400 escenarios × 25): LAC 0-17 = 5.2% (≈1 en 19); 2.6 victorias (1–4).
2) Playoffs tras semana 10 (Monte Carlo, 10,000 temporadas, modelo v0 bootstrap; desempate aleatorio): DEN 94.6% (7-2, 16°, 11.5 V, 10–13),
   MIN 82.9% (7-2, 15°), LA 59.7% (6-4, 4°), SEA 41.9% (6-4, 8°), TB 34.9% (3-6, 11°). Regresión 2002–2025 (768 equipos, 9 partidos → resto):
   β estandarizado diferencia de puntos 0.099 (p < 0.001) vs récord 0.022 (p = 0.14). DEN 6-0 en partidos por ≤8: 0.5^6 = 1/64.
3) Rompemitos (2002–2025, siguiente partido vs. probabilidad del mercado): tras ganar por 20+ (n = 1,162): gana 58.2% vs 58.2% esperado; margen +0.06, p = 0.87.
   Tras perder por 20+ (1,162): +0.52, p = 0.16. Tras 4+ victorias seguidas (926): +0.24, p = 0.58. Tras golear sin ser favorito (213): 44.1% vs 52.6%,
   −1.89 pts, p = 0.031 → BH (4 pruebas) q = 0.12: indicio, no prueba. MIN ganó 30-10 en GB sin ser favorito; dom 22 visita a SF.
4) Ranking de calidad semana 11 (EPA neta/jugada): 1 JAX (7-2), 2 SF (8-1), 3 KC, 4 LA, 5 BUF (8-1). TB 3-6, 11°, Pitágoras 5.2, 1-6 en partidos por ≤8:
   P(≤1 de 7 | 50%) = 0.0625 (1 en 16). Cerrados 1a vs 2a parte de temporada (577 equipos con 4+ cerrados): r = 0.08 (p = 0.053); los que ganaron ≤20%
   de 5+ cerrados (n = 49) ganaron 50% de los cerrados después. TB playoffs 34.9% (división: CAR 4-5 al frente)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1116")
LEGAL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
SEP = "visitan a · récord · lugar en calidad real"


def covers():
    return {
        "1-nfl-lac-bal": slide(1, 6, "NFL · Semana 10 · Hoy lunes 16 nov · 19:15 CDMX · Baltimore",
            "Los Chargers van 0-8. Desde 2002, de 15 equipos así, solo 2 terminaron sin ganar",
            [Matchup("Chargers", "0-8 · 32°", "Ravens", "4-5 · 19°", sep=SEP),
             Stats([("73%", "gana Baltimore (58–85%)", GHOST),
                    ("4", "titulares de Baltimore en 4 partidos", AMBER),
                    ("1 de 19", "temporadas simuladas: Chargers 0-17", ACC)])],
            takeaway="Brissett debuta con Baltimore y el modelo no ve el cambio: con solo el último mes, baja a 64%. ¿Quién rompe su racha?",
            style="cover", method=LEGAL, title_size=62),
        "2-nfl-playoffs": slide(1, 6, "NFL · Tras la semana 10 · 10,000 temporadas simuladas",
            "Denver es 16° en calidad y tiene 95% de llegar a playoffs. Los Rams son 4° y tienen 60%",
            [HBars([("Denver 7-2 · 16°", 94.6, ACC), ("Minnesota 7-2 · 15°", 82.9, ACC), ("Rams 6-4 · 4°", 59.7, GHOST),
                    ("Seattle 6-4 · 8°", 41.9, GHOST)], 100, "{}%", 380),
             Stats([("4.5 a 1", "diferencia de puntos vs. récord al anticipar", GHOST),
                    ("1 de 64", "a volado, el 6-0 de Denver en partidos cerrados", AMBER),
                    ("10–13", "victorias finales de Denver (80%)", ACC)])],
            takeaway="Las victorias ya en la bolsa pesan más que la calidad… por ahora. ¿Quién llega mejor a enero?",
            style="cover", method=LEGAL, title_size=60),
        "3-nfl-palizas": slide(1, 6, "NFL · Rompemitos · 2002–2025",
            "¿Una paliza anuncia otra victoria? Revisamos 1,162 casos: no cambia nada",
            [HBars([("Ganaron el siguiente", 58.2, ACC), ("Se esperaba antes", 58.2, GHOST)], 100, "{}%", 380),
             Stats([("p = 0.87", "efecto de ganar por 20+ en el partido siguiente", GHOST),
                    ("44% vs 53%", "no favoritos que golearon: ganaron después vs. lo esperado", AMBER),
                    ("Indicio", "no prueba: no sobrevive a la corrección por 4 pruebas", ACC)])],
            takeaway="Minnesota ganó por 20 en Green Bay sin ser favorito y el domingo visita a San Francisco. ¿Le pasa factura?",
            style="cover", method=LEGAL, title_size=62),
        "4-nfl-ranking": slide(1, 6, "NFL · Ranking de calidad · Semana 11",
            "Tampa Bay va 3-6, pero es 11° en calidad: perdió 6 de sus 7 partidos cerrados",
            [HBars([("Victorias reales", 3, NEG), ("Según sus puntos", 5.2, GHOST)], 9, "{}", 360),
             Stats([("1 de 16", "a volado, perder 6 de 7 cerrados", AMBER),
                    ("r = 0.08", "lo que anticipan los cerrados de la 1a mitad (577 equipos)", GHOST),
                    ("35%", "de llegar a playoffs: su división la lidera Carolina 4-5", ACC)])],
            takeaway="Y el 1° en calidad no es ninguno de los 8-1: es Jacksonville. ¿Tu equipo está arriba o abajo de su récord?",
            style="cover", method=LEGAL, title_size=62),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
