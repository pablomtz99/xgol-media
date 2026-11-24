"""xGol — portadas de las 4 ideas del 24 nov. Diseño v7. Cálculos en studio/models/*_1124.py. Sin xgol-data (add_repo no disponible); nflverse SÍ accesible hoy.
1) NFL Thanksgiving jue 26 (CHI@DET 12:00, PHI@DAL 15:30, KC@BUF 19:20 CDMX). Modelo NFL v0 (EPA nflverse, sem 1-11): DET 56.1% (80%: 45–66), DAL 69.9% (61–77),
   KC 51.2% visitante (41–60). Los 3 favoritos: 20.1% (80%: 14–26%). Validación fuera de muestra sem 4-11: 77 de 114, Brier 0.223 vs 0.25; Spiegelhalter p = 0.64.
   Thanksgiving 2010-25: locales 20 de 47 (43%) vs 55.5% resto, p = 0.079 (indicio). DET 5-11, DAL 8-8 en ese día. BUF 9-1 vs 7.2 esperadas (Pitágoras; P(≥9) = 0.19).
2) UCL J5 mié 25 (14:00 CDMX): Club Brugge–Liverpool 46.5/19.4/34.1 (80% L 38–54). Modelo xGol UCL v0.1 (72 partidos). Defensa LIV 18ª de 36 (10 GC en 4).
   9 partidos del miércoles: ganan todos los favoritos 1.3% (1 en 77); sorpresas esperadas 3.3; P(≥3) 71%. Validación J4 n = 18: Brier 0.50 vs 0.67.
3) Liga MX cuartos ida mié 25: Toluca (5°, +12) vs Atlas (4°, −3) 19:00; Monterrey–América 21:10. Toluca avanza 61.2% (sens 57–70%); gana ida 59.5%;
   si Toluca gana por 2+ en la ida, avanza 91%. América avanza 70.4% (68–75%). Sin validación propia en Liguilla.
4) NBA Cup mar 24, DET (10-6) en ORL (7-9), 18:00 CDMX. NBA v1: DET 61.8% (49–74%); sin Cunningham ≈54%. Mercado sin margen 56%. ORL 1-5 casa / 6-4 visita: Fisher p = 0.15
   (azar); P(≤1 de 6 en casa | nivel) = 0.085. Bajas (Sportbusy): ORL Banchero, Isaac; DET Duren, D. Robinson; Cunningham día a día."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1124")
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
LEGAL_UCL = "Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta. Resultados: UEFA vía Sports Mole, NBC Sports."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla: El Imparcial, ESPN; horarios: Claro Sports."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference, Sportbusy."


def covers():
    return {
        "1-nfl-thanksgiving": slide(1, 6, "NFL · Thanksgiving · Jueves 26 · 12:00, 15:30 y 19:20 CDMX",
            "Tres favoritos en Thanksgiving. Que ganen los 3: 1 de cada 5",
            [HBars([("Lions vs Bears", 56, ACC), ("Cowboys vs Eagles", 70, ACC), ("Chiefs en Bills", 51, ACC), ("Ganan los 3", 20, AMBER)], 100, "{}%", 340),
             Stats([("20 de 47", "locales ganaron en Thanksgiving desde 2010", NEG),
                    ("5-11", "Detroit en casa ese día desde 2010", AMBER),
                    ("9-1", "Buffalo; sus puntos dicen 7.2 victorias", GHOST)])],
            takeaway="Barras = probabilidad del favorito según nuestro modelo (los 3 juntos, 80%: 14–26%). ¿Cuál se cae?",
            style="cover", method=LEGAL_NFL, title_size=56),
        "2-ucl-brujas-liverpool": slide(1, 6, "Champions League · Jornada 5 · Miércoles 25 · 14:00 CDMX",
            "El modelo xGol pone a Brujas por encima de Liverpool",
            [Matchup("Brujas", "9° · 9 pts", "Liverpool", "8° · 9 pts", sep="recibe a · lugar en la tabla · puntos"),
             Stats([("46%", "gana Brujas (80%: 38–54%)", ACC),
                    ("34%", "gana Liverpool", AMBER),
                    ("18°", "defensa de Liverpool de 36 (10 goles en 4)", NEG)])],
            takeaway="Los 9 favoritos del miércoles ganan solo 1 de cada 77 veces. ¿Liverpool es una de las sorpresas?",
            style="cover", method=LEGAL_UCL, title_size=58),
        "3-ligamx-toluca-atlas": slide(1, 6, "Liga MX · Cuartos de final, ida · Miércoles 25 · 19:00 CDMX · Toluca",
            "Atlas es 4° con más goles recibidos que anotados. Toluca lo elimina 6 de cada 10",
            [Matchup("Toluca", "5° · +12", "Atlas", "4° · −3", sep="recibe a · lugar · diferencia de goles"),
             Stats([("61%", "avanza Toluca (rango 57–70%)", ACC),
                    ("91%", "si Toluca gana la ida por 2 o más", AMBER),
                    ("70%", "avanza América ante Monterrey (21:10)", GHOST)])],
            takeaway="Probabilidades del modelo xGol con 200,000 series simuladas. ¿Atlas desmiente a los números?",
            style="cover", method=LEGAL_MX, title_size=54),
        "4-nba-det-orl": slide(1, 6, "NBA Cup · Hoy martes 24 · 18:00 CDMX · Pistons en Magic · Orlando",
            "Orlando: 1-5 en casa y 6-4 de visita. ¿Maldición? Los números dicen azar",
            [Matchup("Pistons", "10-6 · 6°", "Magic", "7-9 · 19°", sep="visita a · récord · lugar en calidad real (nuestro ranking)"),
             Stats([("62%", "gana Detroit (80%: 49–74%)", ACC),
                    ("p = 0.15", "casa vs visita de Orlando: cabe en el azar", GHOST),
                    ("54%", "si Cunningham no juega (día a día)", NEG)])],
            takeaway="Orlando juega sin Banchero ni Isaac; la probabilidad del mercado da 56% a Detroit. ¿Quién tiene razón?",
            style="cover", method=LEGAL_NBA, title_size=54),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
