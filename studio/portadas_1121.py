"""xGol — portadas de las 4 ideas del 21 nov. Diseño v7. Cálculos en studio/models/*_1121.py. SIN xgol-data (add_repo no disponible).
Sin MLB (fuera de temporada). Tenis: ATP Finals (semis hoy, final dom 11:00 CDMX) sin modelo propio validado → no se propone.
1) NFL semana 11 (dom 22): bye. Modelo NFL v0 con jugadas sem. 1–11 (nflverse). Descansados: CHI 66.3% (55–76) vs NO; DEN 63.6% (54–72) vs LV;
   TB 43.4% (34–53) en DET; PHI 37.8% (29–47) vs PIT. Prueba 2010–2025 (n = 3,349; 399 con bye vs rival sin bye): +0.75 pts (ee 0.63, p = 0.23), ajustado
   por diferencial previo; 2018+: +0.37 (p = 0.67). Equipo con bye gana 53.4%. Récords: CHI 7-2, NO 3-6, DEN 7-2, LV 4-6, PHI 2-7, PIT 6-3, TB 3-6, DET 7-2.
   PHI: Hurts en reserva de lesionados, Milton titular (philadelphiaeagles.com, theScore). Validación v0: 67 de 102 fuera de muestra, Spiegelhalter p = 0.78.
2) BOS@GSW (dom 22, 19:30 CDMX). NBA v1 SRS (B-Ref hasta 18 nov): BOS 11-4, MOV +10.47, SOS −2.94, SRS 7.53 (z = 1.98, p = 0.047), nivel encogido 6.22;
   GSW 0.66 (14°). Con −2.1 por back-to-back de BOS (sáb en SAC; calendario NBA): BOS 54.0% (40.8–66.6%), margen +1.5. Bajas GSW −3/−5: BOS 61.9/67.0%.
   Bajas (ESPN, 20 nov): Curry, Butler, Porziņģis, Moody fuera; Green día a día. Récord de GSW sin verificar (B-Ref 8-7 al 18; StatMuse 8-8) → no se muestra.
3) Atalanta–Inter (Serie A J12, dom 22, 13:45 CDMX). Tabla tras J11 (vavel 8 nov; puntos = TMW 9 nov y fantacalcio). Modelo xGol Europa v0:
   ATA 25.0 / E 22.3 / INT 52.7% (80%: 40–66%); sensibilidad INT 46–68%. Goles esp. 1.26–1.91. Puntos por goles: INT 24.0 vs 28 (P≥28 = 0.20), LAZ 25.1 vs 29
   (P = 0.19), ROM 26.9 vs 27; dif. de goles: ROM +21, LAZ +16, INT +15. Sin xG verificado; sin validación fuera de muestra (modelo nuevo).
4) Liga MX liderato (J17). Tras J16: CAZ 32 (+11), AME 30 (+15), CHV 30 (+11). MC 400,000: líder CAZ 41.9%, AME 35.9%, CHV 22.1% (sens. CAZ 38–48, AME 32–44,
   CHV 16–28). CAZ líder si gana 100%; AME si gana 69.4%; CHV si gana 48.4%. Tigres–América sáb 21:00, Chivas–Cruz Azul dom 17:07 (Récord, 18 nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1121")
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference, ESPN."
LEGAL_ITA = "Análisis independiente, no afiliado a la Serie A ni a los clubes. No es recomendación de apuesta. Tabla: vavel, TMW."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla: futboltotal, Claro Sports, Record."


def covers():
    return {
        "1-nfl-descanso": slide(1, 6, "NFL · Semana 11 · Domingo · 4 equipos vienen de su semana libre",
            "Dos semanas de descanso valen menos de 1 punto",
            [HBars([("Chicago vs Saints", 66, ACC), ("Denver vs Raiders", 64, ACC), ("Tampa en Detroit", 43, AMBER),
                    ("Filadelfia vs Steelers", 38, NEG)], 100, "{}%", 360),
             Stats([("+0.7", "puntos extra tras la semana libre (p = 0.23)", AMBER),
                    ("399", "partidos 2010–2025 con un equipo descansado", GHOST),
                    ("67 de 102", "aciertos de nuestro modelo NFL fuera de muestra", ACC)])],
            takeaway="Barras = probabilidad de ganar del equipo descansado. Filadelfia, 2-7 y sin Hurts: ¿le sirve el descanso?",
            style="cover", method=LEGAL_NFL, title_size=62),
        "2-nba-bos-gsw": slide(1, 6, "NBA · Domingo · 19:30 CDMX · Celtics en Warriors · San Francisco",
            "Boston gana por 10.5 en promedio. Ajustado por sus rivales, por 7.5",
            [Matchup("Celtics", "11-4 · 5°", "Warriors", "14° · sin Curry", sep="visitan a · récord · lugar en calidad real"),
             Stats([("54%", "gana Boston, según nuestro modelo (41–67%)", ACC),
                    ("−2.1", "puntos por jugar la 2ª noche seguida (p = 0.011)", AMBER),
                    ("62–67%", "Boston, si las bajas de Golden State valen 3 a 5 puntos", GHOST)])],
            takeaway="Boston juega el sábado en Sacramento. ¿Pesa más su cansancio o las bajas de Golden State?",
            style="cover", method=LEGAL_NBA, title_size=58),
        "3-seriea-atalanta-inter": slide(1, 6, "Serie A · Jornada 12 · Domingo · 13:45 CDMX · En Bérgamo",
            "La tabla dice Lazio e Inter. Los goles dicen Roma",
            [Matchup("Atalanta", "4-2-5 · 14 pts", "Inter", "9-1-1 · 28 pts", sep="recibe a · récord · puntos"),
             Stats([("53%", "gana Inter en Bérgamo (40–66%); empate 22%", ACC),
                    ("+4", "puntos de Inter sobre lo que dan sus goles (1 de cada 5)", AMBER),
                    ("+21", "Roma: la mejor diferencia de goles, y es 3ª", GHOST)])],
            takeaway="Inter mete 2.5 goles por partido y visita al 12°. ¿Sostiene su ritmo o los goles lo alcanzan?",
            style="cover", method=LEGAL_ITA, title_size=62),
        "4-ligamx-liderato": slide(1, 6, "Liga MX · Jornada 17 · Sábado y domingo · 400,000 simulaciones",
            "Chivas puede vencer a Cruz Azul y aun así no ser líder: pasa 1 de cada 2 veces",
            [HBars([("Cruz Azul · 32", 42, ACC), ("América · 30", 36, AMBER), ("Chivas · 30", 22, GHOST)], 100, "{}%", 300),
             Stats([("100%", "Cruz Azul es líder si gana en Guadalajara", ACC),
                    ("69%", "América es líder si gana en casa de Tigres", AMBER),
                    ("48%", "Chivas es líder aun ganando", GHOST)])],
            takeaway="Barras = veces que termina 1°. Tigres–América (sáb 21:00) y Chivas–Cruz Azul (dom 17:07). ¿Quién termina arriba?",
            style="cover", method=LEGAL_MX, title_size=54),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
