"""xGol — portadas de las 4 ideas del 20 nov. Diseño v7. Cálculos en studio/models/*_1120.py.
SIN xgol-data (add_repo no disponible). Sin NFL (semana 11 sigue el domingo 22, fuera de hoy/mañana), sin MLB (fuera de temporada), sin tenis (sin torneo grande verificable).
1) NBA viernes (9 juegos, Copa NBA; Fox Sports, horarios UTC → primer juego 18:00 CDMX). Modelo NBA v1 (SRS de Basketball-Reference, hasta mié 18; ningún equipo
   del viernes jugó el jueves → sin back-to-back). Favoritos: ATL 69.2, DET 68.0, ORL 64.4, CLE 76.4, CHI 63.7, OKC 84.5, PHX 59.8, LAL 84.1, HOU 53.7.
   P(todos) = 0.0337 (1 en 30); sorpresas esperadas 2.76 (80%: 1–5); P(≥2) = 82%. Validación v1: 2025-26 fuera de muestra 69% aciertos, Brier 0.205 (n = 1,090).
2) HOU@DEN (hoy, 21:00 CDMX, Copa NBA). DEN 46.3% (33.7–59.3%), margen −1.4. Ranking nuestro: HOU 4°, DEN 10°. Rebote ofensivo HOU 33.2% (1° de 30; liga 27.3%;
   z = 3.5, p < 0.001 con ~44 oportunidades/partido, supuesto); DEN rebote defensivo 69.8% (25°; p = 0.12 → indicio). Cruce esperado: HOU 36.4% → +4 rebotes ofensivos.
   Bajas (CBS Sports, 20 nov): Şengün en duda (golpe en ambos ojos), Adams en duda (cuádriceps), Capela fuera (tobillo). Nuggets: sin reporte verificado hoy.
3) Pumas–Monterrey (sáb 21, 19:00 CDMX; TV Azteca). Modelo xGol Liga MX v0 + Monte Carlo 200,000 (tabla tras J16: futboltotal, Claro Sports, Record).
   PUM 42.1% / E 24.0% / MTY 33.9%; goles esperados 1.60–1.42. MTY a Liguilla: 69.5%; si gana 100%, si empata 76.1%, si pierde 41.2%. PUM: 8.4%; si gana 20.0%.
   Sensibilidad (encogimiento 0/16, localía 0/0.6): PUM gana 34–48%; MTY top 8 63–78%. Sin validación fuera de muestra (modelo nuevo).
4) Newcastle–Arsenal (sáb 21, 17:30 UK = 11:30 CDMX; Sky Sports). Tabla tras J10 (Sky Sports, act. 8 nov; coincide nigfooty 20 nov; Sports Mole: Arsenal 5 pts sobre Brighton).
   Modelo xGol Europa v0 (dif. de goles encogida, Poisson, localía +0.30 supuesto): NEW 27.8 / E 24.9 / ARS 47.3% (80%: 35–59%); sensibilidad ARS 42–61%.
   Puntos esperados por goles (Poisson con sus tasas): ARS 21.2 (80%: 16–26) vs 27 reales, P(≥27) = 0.06 → indicio (no significativo al 5%); BHA 24.8 vs 22.
   Bajas (Sports Mole, 18 nov): Saka fuera (cuádriceps), Dowman suspendido, Zubimendi en duda. Newcastle: sin fuente verificada."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1120")
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla: futboltotal, Claro Sports, Record."
LEGAL_EPL = "Análisis independiente, no afiliado a la Premier League ni a los clubes. No es recomendación de apuesta. Tabla: Sky Sports."


def covers():
    return {
        "1-nba-viernes-compuesta": slide(1, 6, "NBA · Copa NBA · Hoy · 9 partidos desde las 18:00 CDMX",
            "9 partidos y 9 favoritos. Que ganen todos pasa 1 de cada 30 noches",
            [Hero("1 en 30", "noches ganan los 9 favoritos de nuestro modelo. Lo normal: 2 o 3 sorpresas.", AMBER, maxsize=260),
             Stats([("2.8", "sorpresas esperadas hoy (80%: 1 a 5)", ACC),
                    ("84%", "Thunder y Lakers: nuestros favoritos más claros", GHOST),
                    ("54%", "Houston en Denver: el más parejo", AMBER)])],
            takeaway="En 1,090 partidos de la temporada pasada nuestro modelo acertó 69%. ¿Dónde cae la sorpresa?",
            style="cover", method=LEGAL_NBA, title_size=60),
        "2-nba-hou-den-rebote": slide(1, 6, "NBA · Hoy · 21:00 CDMX · Rockets en Nuggets · Denver",
            "El mejor rebote ofensivo de la NBA visita Denver con sus 3 centros en duda o fuera",
            [Matchup("Rockets", "12-4 · 4°", "Nuggets", "8-5 · 10°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("46%", "gana Denver, según nuestro modelo (34–59%)", GHOST),
                    ("33%", "de sus fallos recupera Houston: 1° de 30 (p < 0.001)", ACC),
                    ("+4", "rebotes ofensivos extra ante Denver (25° defendiendo el rebote)", AMBER)])],
            takeaway="Şengün y Adams, en duda; Capela, fuera. Sin centros, ¿se queda Houston sin su arma?",
            style="cover", method=LEGAL_NBA, title_size=56),
        "3-ligamx-pumas-monterrey": slide(1, 6, "Liga MX · J17 · Sábado 19:00 CDMX · 200,000 simulaciones",
            "Monterrey se juega la Liguilla en CU: si gana entra 100 de 100 veces; si pierde, 41",
            [HBars([("Si gana", 100, ACC), ("Si empata", 76, AMBER), ("Si pierde", 41, NEG)], 100, "{}%", 260),
             Stats([("42%", "gana Pumas en casa (34–48% según supuestos)", AMBER),
                    ("20%", "llega Pumas a la Liguilla aun ganando", GHOST),
                    ("70%", "llega Monterrey hoy, antes de jugar", ACC)])],
            takeaway="Pumas necesita ganar y que pierdan otros. ¿Monterrey sale vivo de Ciudad Universitaria?",
            style="cover", method=LEGAL_MX, title_size=56),
        "4-epl-newcastle-arsenal": slide(1, 6, "Premier League · J11 · Sábado · 11:30 CDMX · En Newcastle",
            "Arsenal lleva 27 puntos con goles de 21. Visita Newcastle sin Saka",
            [HBars([("Puntos reales", 27, ACC), ("Por sus goles", 21.2, AMBER), ("Brighton real", 22, GHOST)], 30, "{}", 320),
             Stats([("47%", "gana Arsenal en Newcastle (35–59%)", ACC),
                    ("1 en 17", "equipos con sus goles suman 27 o más", AMBER),
                    ("+19", "diferencia de Brighton, 2°: la mejor de la liga", GHOST)])],
            takeaway="15 goles a favor y 5 en contra en 10 partidos, y solo una derrota. ¿Es dominio o buena racha?",
            style="cover", method=LEGAL_EPL, title_size=60),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
