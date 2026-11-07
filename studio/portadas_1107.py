"""xGol — portadas de las 4 ideas del 7 nov. Diseño v7.
NBA LAL@DET (dom 8, 18:00 ET = 17:00 CDMX): modelo NBA v1 (models/nba_ridge_1103.py) con 132 partidos 2026-27 al 6 nov
   (Land of Basketball + ESPN/Yahoo para LAL 124-118 POR). DET 59.5% (52–67% bootstrap 400), margen +3.5, total 227.
   Ataque ajustado: LAL 1° (+4.1); defensa ajustada: DET 1° (+5.4). LAL 8-2 vs 6.54 esperadas con probabilidades previas
   (Poisson-binomial P(≥8) = 0.27); calendario 9° más fácil. DET 6-2 vs 5.33 (P = 0.47). Monte Carlo 200k: P(|margen| ≤ 5) = 26%.
   Contexto: Duren (DET) fuera desde el 23 oct por isquiotibial (Detroit Sports Nation, 6 nov); Dončić 53 pts el 6 nov (Yahoo/ESPN).
NFL TB@CHI (dom 8, 20:20 ET = 19:20 CDMX): modelo NFL v0 con EPA por jugada (nflverse pbp 2026, sem. 1–9). CHI 56.5% (41–70%
   bootstrap por jugada; 56–57% con regresión 0.35–0.65). TB: pase ofensivo 31°, defensa 2° (EPA por jugada permitida), neto 10°.
   TB 3-5 con +27 de diferencia; Pitágoras (exp. 2.37) 4.77 victorias esperadas (binomial P(≤3) = 0.18); 1-5 en partidos por ≤8 pts.
   Persistencia (nflverse games.csv 2010–2025, n = 392 equipo-temporada): % de victorias en partidos cerrados en los 8 primeros vs
   el resto r = 0.04, p = 0.42; equipos con ≤25% en los primeros (n = 81) ganaron 52% de los cerrados después.
   Contexto: reporte oficial Bucs 6 nov — Diaby fuera, Egbuka en duda, Mayfield entrenó completo (pulgar).
Liga MX PUM–AME (sáb 7, 21:10 CDMX, CU): modelo xGol Liga MX v0 (Poisson, GF/GC tras J15 encogidos 50%, localía ×1.15):
   Pumas 37%, empate 23%, América 41%; rango (encogimiento 0.3–0.7, localía 1.05–1.25): América 30–52%. Goles esperados 1.65 + 1.75.
   Monte Carlo 200k con Tigres–Cruz Azul y León–Chivas: líder tras J16 América 54%; si gana 99.8%, si empata 38%, si pierde 14%.
   Tabla J15: news.jointly.mx; contexto: TUDN (América 3 sin ganar; un triunfo podría eliminar a Pumas).
Premier CRY–LIV (dom 8, 14:00 GMT = 8:00 CDMX): Poisson con GF/GC tras 9 jornadas (BeSoccer), encogimiento 50%, localía ×1.12:
   Palace 28%, empate 25%, Liverpool 47% (34–61%). Liverpool: 10 de 12 pts de visita, 5 de 15 en casa; prueba de permutación
   exacta de puntos por partido casa vs. visita: p = 0.21 (dos colas). Palace: 21 goles recibidos (más de la liga), Mateta suspendido
   (FPL vía footballdream.in, 4 nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1107")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta."
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. Datos: nflverse. No es recomendación de apuesta."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta."
LEGAL_PL = "Análisis independiente, no afiliado a la Premier League ni a los clubes. No es recomendación de apuesta."


def covers():
    return {
        "1-nba-lal-det": slide(1, 6, "NBA · Domingo 8 de noviembre · 17:00 CDMX · Detroit",
            "El mejor ataque de la NBA contra la mejor defensa. Nuestro modelo: Detroit, 6 de cada 10",
            [Matchup("Lakers", "8-2", "Pistons", "6-2", sep="visitan a · Detroit · ataque 1° vs. defensa 1° (ajustados por rival)"),
             Stats([("60%", "gana Detroit (52–67%)", GHOST),
                    ("53", "puntos de Dončić el viernes", AMBER),
                    ("6.5", "victorias esperábamos de los Lakers; llevan 8", ACC)])],
            takeaway="Los Lakers anotan como nadie; Detroit, aun sin su pívot Duren, es quien menos permite. ¿Qué pesa más el domingo?",
            style="cover", method=LEGAL_NBA, title_size=72),
        "2-nfl-tb-chi": slide(1, 6, "NFL · Semana 9 · Domingo 8 de noviembre · 19:20 CDMX · Chicago",
            "Tampa perdió 5 partidos por 8 puntos o menos. En 392 casos, esa mala racha no se repitió",
            [Matchup("Buccaneers", "3-5", "Bears", "6-2", sep="visitan a · Chicago · domingo por la noche"),
             Stats([("56%", "gana Chicago (41–70%)", GHOST),
                    ("1-5", "Tampa en partidos cerrados", NEG),
                    ("2°", "defensa de Tampa en puntos por jugada", ACC)])],
            takeaway="Tampa anotó 27 puntos más de los que recibió y aun así va 3-5. ¿Es un equipo malo o un equipo con mala suerte?",
            style="cover", method=LEGAL_NFL, title_size=72),
        "3-mx-pumas-america": slide(1, 6, "Futbol · Liga MX · Jornada 16 · Hoy sábado 7 nov · 21:10 CDMX",
            "El liderato se decide en CU: si América gana, es líder 998 de cada 1,000 veces. Si pierde, 14%",
            [Matchup("Pumas", "10° · 20 pts", "América", "1° · 29 pts", sep="reciben a · Estadio Olímpico Universitario · Clásico Capitalino"),
             Stats([("41%", "gana América (30–52%)", GHOST),
                    ("23%", "empate", MUTED),
                    ("3.4", "goles esperados, modelo xGol", ACC)])],
            takeaway="América llega con 3 partidos sin ganar y Pumas se juega la Liguilla. ¿Se cae el líder en el clásico?",
            style="cover", method=LEGAL_MX, title_size=70),
        "4-pl-palace-liverpool": slide(1, 6, "Futbol · Premier League · Jornada 10 · Dom 8 nov · 8:00 CDMX",
            "Liverpool suma 2.5 veces más puntos de visita que en casa. ¿Ventaja real? Probablemente casualidad",
            [Matchup("Crystal Palace", "18°", "Liverpool", "5°", sep="recibe a · Selhurst Park · 7 vs. 15 puntos"),
             Stats([("47%", "gana Liverpool (34–61%)", GHOST),
                    ("10 de 12", "puntos de Liverpool de visita", AMBER),
                    ("p = 0.21", "prueba casa vs. visita: no concluyente", ACC)])],
            takeaway="Palace es el que más goles recibe (21) y no tiene a Mateta. ¿Sigue la magia de Liverpool lejos de casa?",
            style="cover", method=LEGAL_PL, title_size=70),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
