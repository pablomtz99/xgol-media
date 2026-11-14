"""xGol — portadas de las 4 ideas del 14 nov (NFL, semana 10). Diseño v7.
Datos: nflverse (CC-BY 4.0) games.csv + play_by_play_2026 (semanas 1–9, 16,864 jugadas de pase/carrera) y pbp 2016–2025 para pruebas.
Modelo NFL v0: margen = 0.5 × (EPA neta/jugada local − visitante) × 61.6 + 1.5; P = Φ(margen/13.5). Rangos 10–90%: bootstrap de partidos (400).
Validación fuera de muestra 2026 (semanas 4–9, solo datos previos): 87 partidos, 55 aciertos vs 55.0 esperados, Brier 0.230
(volado 0.25), Spiegelhalter z = −0.11, p = 0.91.
SIN NBA: xgol-data (modelo NBA v1) no accesible en esta corrida (add_repo no disponible). Futbol: fecha FIFA. Por eso 4 ideas NFL.
Horarios (ESPN/nflverse, ET; CDMX = ET − 1 h): dom 15 13:00 ET = 12:00; SNF 20:20 ET = 19:20; lun 16 MNF 20:15 ET = 19:15.
Lesiones: NFL.com reporte final semana 10; Ravens/Chargers: The Sports Leader (12 nov) y Russell Street Report.
1) MIN@GB (dom 12:00). GB 65.5% (50–80%), margen +5.4. MIN 6-2 con EPA neta −0.013 (19°): ataque −0.162 (31°), defensa −0.149 (2°);
   4-1 en partidos por ≤8 (P(≥4 de 5 | 50%) = 0.19); Pitágoras 5.1; balones +4 (12 recuperados, 8 perdidos). GB 6-3, 7°; pase +0.178.
   Prueba 2016–2025 (320 equipos tras 8 partidos): 2a mitad ~ récord + EPA neta → β estandarizados 0.045 (p = 0.027) vs 0.064 (p = 0.002);
   r récord 0.41, r EPA 0.43. Parecidos a MIN (6+ victorias, EPA neta < 0.03): n = 9, de 76% a 61% en la 2a mitad.
   Bajas: MIN sin Kyler Murray (abre Cousins), Jennings, Hockenson; Addison duda. GB sin Parsons y Jacobs.
2) PIT@CIN (dom 19:20). CIN 62.4% (52–73%), margen +4.3. Ambos 6-2. PIT viene de descanso (14 días vs 7). CIN 6°, PIT 12°.
   Pase CIN +0.253 vs pase permitido PIT −0.062; carrera PIT +0.122 vs carrera permitida CIN +0.032. Puntos: CIN 30.0/21.9, PIT 22.5/18.0.
   Rompemitos 2010–2025 (sin sedes neutrales): visitante tras descanso (n = 212) vs sin descanso (2,891): −1.1 pts, p = 0.26; local tras
   descanso (189): +0.4, p = 0.71; efecto combinado ≈ +0.7 pts → no significativo. Bajas: CIN sin Dugger; PIT Harmon duda.
3) LAC@BAL (lun 19:15). BAL 72.7% (59–82%), margen +8.2 — pero BAL abre con Jacoby Brissett (debut; Jackson y Huntley fuera): el modelo no
   ve el cambio de mariscal. LAC 0-8, EPA neta −0.248 (32°), −12.2 por partido, Pitágoras 1.6, 0-3 en cerrados, balones −7; Herbert 11 int.
   BAL 4-5, 4 derrotas seguidas (117-43). Monte Carlo (400 escenarios bootstrap × 100 temporadas, 9 partidos restantes): 2.5 victorias
   (10–90%: 1–4); P(0) = 5.7% (≈1 en 18); con el modelo puntual 5.2%. Historia 2016–2025: 6 equipos 0-8, solo 1 terminó sin ganar (CLE 2017).
4) Domingo: los 4 mejores en EPA neta juegan de visita: JAX@TEN 81.0% (69–89%), SF@DAL 67.5% (56–78%), KC@ATL 69.6% (50–82%),
   BUF@NYJ 62.3% (53–74%). Los 4 ganan: 23.7% (bootstrap 14–31%); 3 de 4: 41.7%; 2: 26.7%; esperado 2.8.
   Bajas: SF Trent Williams y 4 esquineros en duda; JAX sin Bates; NYJ Garrett Wilson duda; BUF Spencer Brown duda."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1114")
LEGAL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
SEP = "visitan a · récord · lugar en calidad real"


def covers():
    return {
        "1-nfl-min-gb": slide(1, 6, "NFL · Semana 10 · Domingo 15 nov · 12:00 CDMX · Green Bay",
            "Minnesota va 6-2 con la 31ª ofensiva de la liga. Nuestro modelo le da 1 de cada 3 en Green Bay",
            [Matchup("Vikings", "6-2 · 19°", "Packers", "6-3 · 7°", sep=SEP),
             Stats([("65%", "gana Green Bay (50–80%)", GHOST),
                    ("4-1", "en cerrados: pasa 1 de cada 5", AMBER),
                    ("76→61%", "equipos así en la 2a mitad (2016–2025)", ACC)])],
            takeaway="Minnesota abre con Cousins y sin Hockenson; Green Bay, sin Parsons ni Jacobs. ¿El récord miente o la defensa alcanza?",
            style="cover", method=LEGAL, title_size=60),
        "2-nfl-pit-cin": slide(1, 6, "NFL · Semana 10 · Domingo 15 nov · 19:20 CDMX · Cincinnati",
            "Pittsburgh llega con 2 semanas de descanso. En 401 partidos, eso no movió el marcador",
            [Matchup("Steelers", "6-2 · 12°", "Bengals", "6-2 · 6°", sep=SEP),
             Stats([("62%", "gana Cincinnati (52–73%)", GHOST),
                    ("+0.7", "puntos vale el descanso: no significativo", AMBER),
                    ("30.0", "puntos por partido de Cincinnati, 2° de la liga", ACC)])],
            takeaway="Rodgers contra Burrow por el primer lugar del Norte. ¿Pesa más el descanso o el mejor ataque aéreo?",
            style="cover", method=LEGAL, title_size=62),
        "3-nfl-lac-bal": slide(1, 6, "NFL · Semana 10 · Lunes 16 nov · 19:15 CDMX · Baltimore",
            "Los Chargers van 0-8. Simulamos su temporada 40,000 veces: terminan sin ganar 1 de cada 18",
            [Matchup("Chargers", "0-8 · 32°", "Ravens", "4-5 · 20°", sep=SEP),
             Stats([("73%", "gana Baltimore (59–82%)", GHOST),
                    ("1–4", "victorias de Los Ángeles (80% de simulaciones)", ACC),
                    ("1 de 6", "equipos 0-8 desde 2016 terminó sin ganar", AMBER)])],
            takeaway="Baltimore estrena a Brissett, sin Jackson ni Huntley, y nuestro modelo no ve ese cambio. ¿Hoy cae la primera victoria?",
            style="cover", method=LEGAL, title_size=60),
        "4-nfl-visitantes": slide(1, 6, "NFL · Semana 10 · Domingo 15 nov · 12:00 a 15:25 CDMX",
            "Los 4 mejores equipos de nuestro modelo juegan de visita. Que ganen todos sale 1 de cada 4",
            [HBars([("Jacksonville en Tennessee", 81, ACC), ("Kansas City en Atlanta", 70, ACC),
                    ("San Francisco en Dallas", 68, ACC), ("Buffalo en Nueva York", 62, ACC)], 100, "{}%", 470),
             Stats([("24%", "ganan los 4 (14–31%)", ACC),
                    ("3 de 4", "lo más probable (42%)", GHOST),
                    ("2.8", "victorias esperadas de los 4", GHOST)])],
            takeaway="San Francisco llega con Trent Williams y 4 esquineros en duda; los Jets, con Garrett Wilson en duda. ¿Cuál de los 4 cae?",
            style="cover", method=LEGAL, title_size=62),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
