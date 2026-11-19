"""xGol — portadas de las 4 ideas del 19 nov. Diseño v7. Cálculos en studio/models/*_1119.py.
SIN xgol-data (add_repo no disponible). SIN tenis ni futbol europeo (sin fuente verificable de tablas/datos hoy; Europa regresa el 20-21 nov).
1) Liga MX J17 (vie 20 – dom 22). Tabla tras J16 + pendiente QRO 0-1 MTY (14 nov): futboltotal (PJ/GF/GC) cruzada con Claro Sports y Record (MTY 24, LEO 23 +2,
   PAC 22 +9, TIJ 22 +3, PUM 21 −2). Top 8 a Liguilla, sin Play-In (Claro Sports). Modelo xGol Liga MX v0: fuerza = dif. de goles/(16+8) (encogida),
   Poisson con 3.0 goles/partido y localía +0.35 (supuesto). Monte Carlo 200,000: top 8 SAN 84.0%, MTY 69.5%, TIJ 52.2%, PAC 43.8%, LEO 42.3%, PUM 8.2%;
   líder CAZ 42.0%, AME 35.8%, CHV 22.2%. Sensibilidad (encogimiento 0/16, localía 0/0.6): SAN 82–86, MTY 63–78, TIJ 46–58, PAC 37–49, LEO 35–52, PUM 7–9; CAZ líder 38–48.
   Sin validación fuera de muestra (modelo nuevo). León GF sin dato: desempate por goles a favor aleatorio para León.
2) IND@HOU (hoy 19:15 CDMX). HOU 70.4% (59.7–79.3%), margen +7.2 (v0, sem. 1–10). HOU 3-6, cerrados (≤8) 1-5; IND 3-7. Regresión: 2002–2025, equipos con ≥4 cerrados
   en sus primeros 9 y ≥3 después (n = 463): r = 0.13 (p = 0.006); con ≤25% en cerrados (n = 87): 18.3% → 48.7% después, p = 0.66 vs 50%; su % total 32% → 47%.
   Lesiones (Yahoo, 18 nov): IND fuera Raimann, Travis (tacles), Ward, Tillery, Mallory; Gardner duda. HOU fuera Hunter, Harrison Jr., Marks, Jordan.
   HOU capturas defensivas 2° (9.2%); IND carrera 11°, pase 30°; HOU defensa vs carrera 16°.
3) 76ers 13-3, margen +2.94, SOS −2.10, SRS 0.83 (Basketball-Reference, 19 nov). Victorias esperadas por margen: 16 × Φ(2.94/14.7) = 9.3; P(≥13) = 0.047 (1 en 21).
   Cerrados (≤8): 9-0 (ESPN, marcadores). Si fueran 50/50: 1 en 512. Ranking nuestro (SRS encogido hacia 90% de 2025-26, peso 16 partidos): PHI 12°, POR 8° (SOS 2.84, 3° más duro).
   r récord–SRS = 0.89. Próximo: sáb 21 vs MIL.
4) POR@MIL (hoy 20:00 ET = 19:00 CDMX). MIL 1-14, 11 seguidas, 1-7 casa / 0-7 visita (ESPN, Sportbusy). P(MIL) = 25.9% (16.5–37.5%), margen −9.5 (Q MIL −7.20, POR +4.30, local +2).
   Por margen (−13.1) esperaríamos 2.8 victorias; P(≤1) = 0.20. Monte Carlo resto de temporada (67 juegos, rival promedio, mitad en casa): 22 victorias (80%: 15–30).
   Lesiones de POR sin segunda fuente: no se usan."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1119")
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla: futboltotal, Claro Sports, Record."
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference, ESPN."


def covers():
    return {
        "1-ligamx-j17-montecarlo": slide(1, 6, "Liga MX · Jornada 17 · 20 al 22 nov · 200,000 simulaciones",
            "3 boletos a la Liguilla en juego: Tijuana 52%, Pachuca 44%, León 42%",
            [HBars([("Santos · 25 pts", 84.0, ACC), ("Monterrey · 24", 69.5, ACC), ("Tijuana · 22", 52.2, AMBER),
                    ("Pachuca · 22", 43.8, AMBER), ("León · 23", 42.3, AMBER)], 100, "{}%", 300),
             Stats([("42%", "Cruz Azul termina líder (38–48%)", ACC),
                    ("+9", "Pachuca: 5ª mejor diferencia", AMBER),
                    ("8", "clasifican; sin repechaje", GHOST)])],
            takeaway="Pumas, con 21, solo entra 8 de cada 100 veces. ¿Quién se queda fuera?",
            style="cover", method=LEGAL_MX, title_size=56),
        "2-nfl-hou-cerrados": slide(1, 6, "NFL · Semana 11 · Hoy · 19:15 CDMX · Colts en Texans · Houston",
            "Houston va 1-5 en partidos cerrados. De 87 equipos así, después ganaron la mitad",
            [Matchup("Colts", "3-7 · 28°", "Texans", "3-6 · 11°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("70%", "gana Houston, según nuestro modelo (60–79%)", GHOST),
                    ("18% → 49%", "cerrados ganados por esos 87 equipos, antes y después", ACC),
                    ("p = 0.66", "su segunda mitad no se distingue de un volado", AMBER)])],
            takeaway="Indianapolis juega sin sus 2 tacles titulares ante la 2ª defensa que más captura. Houston, sin Hunter. ¿Quién lo resiente?",
            style="cover", method=LEGAL_NFL, title_size=58),
        "3-nba-76ers-regresion": slide(1, 6, "NBA · Regresión a la media · 2026-27 · Sábado: Bucks en Filadelfia",
            "Filadelfia va 13-3, pero su diferencia de puntos es de un 9-7. Ganó sus 9 partidos cerrados",
            [HBars([("Real", 13, ACC), ("Por margen", 9.3, AMBER), ("Cerrados 50/50", 8.5, GHOST)], 16, "{}", 300),
             Stats([("1 en 21", "veces gana 13 o más con su margen (+2.9 por partido)", AMBER),
                    ("12°", "en nuestro ranking ajustado por rival (récord: 2°)", GHOST),
                    ("9-0", "en partidos decididos por 8 puntos o menos", ACC)])],
            takeaway="Portland va 9-5 con el 3er calendario más duro y es 8°. ¿Filadelfia es candidato o espejismo?",
            style="cover", method=LEGAL_NBA, title_size=56),
        "4-nba-bucks-racha": slide(1, 6, "NBA · Hoy · 19:00 CDMX · Trail Blazers en Bucks · Milwaukee",
            "Milwaukee va 1-14 y suma 11 derrotas seguidas. Hoy le damos 26% de cortar la racha",
            [Matchup("Trail Blazers", "9-5 · 8°", "Bucks", "1-14 · 27°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("26%", "gana Milwaukee (17–38%)", AMBER),
                    ("2.8", "victorias que «merecía» por su margen; tiene 1", ACC),
                    ("22", "victorias esperadas al final de la temporada (15–30)", GHOST)])],
            takeaway="Pierde por 13 puntos en promedio, pero ante el 7° calendario más duro. ¿Hoy se acaba la racha?",
            style="cover", method=LEGAL_NBA, title_size=58),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
