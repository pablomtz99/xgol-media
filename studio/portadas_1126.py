"""xGol — portadas de las 4 ideas del 26 nov. Diseño v7. Sin xgol-data (add_repo no disponible en esta corrida); nflverse no recalculado hoy (pbp no descargado):
las cifras NFL vienen de nfl_thanksgiving_1124.py (fijadas 24 nov).
1) NFL Thanksgiving noche jue 26, KC (8-2) en BUF (9-1), 19:20 CDMX. NFL v0: KC 51.2% (80%: 41–60). BUF 9-1 vs 7.2 Pitágoras (P(≥9) = 0.19). Allen 5-1 vs KC en
   temporada regular, 0-4 en playoffs (Heavy/Yahoo). Clima: ~3 °C, lluvia 75%, viento ~30 km/h (Heavy citando Yahoo Weather). KC sin Kenneth Walker III.
2) Liga MX cuartos ida jue 26, León (7°, 26 pts) vs Cruz Azul (2°, 32 pts), 21:10, Estadio León (Nación Fútbol, Vamos Azul). Liga MX v0: L/E/V 39/24/36;
   Cruz Azul avanza 66.7% (sens 65–71); si León gana por 2+, 22%. Cruz Azul campeón vigente, nunca ha sido bicampeón en torneos cortos (Nación Fútbol).
3) NBA Cup vie 27, LAL (15-3) en SAS (15-4), 20:30 CDMX. NBA v1 (SRS 19 nov): SAS 68% (56–79); sin Wembanyama ≈58%, sin él ni Fox ≈54%.
   LAL 15-3 con diferencial +3.4 → Pitágoras 10.9 de 18; P(≥15) = 0.037 (nba_lal_sas_1126.py).
4) Liga MX vuelta sáb 28: Atlas–Toluca 19:00 (Toluca 85% tras 2-0), América–Monterrey 21:10 (América 77% tras 0-0). Ambos avanzan 66%. Monte Carlo
   400,000 vueltas (resumen_1126.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1126")
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse; contexto: Heavy, Yahoo Sports."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference, Sportsmole."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla y bajas: Nación Fútbol, Vamos Azul."
LEGAL_MX2 = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Resultados: La Silla Rota, 365Scores; horarios: Excélsior."


def covers():
    return {
        "1-nfl-kc-buf": slide(1, 6, "NFL · Thanksgiving · Hoy jueves 26 · 19:20 CDMX · Chiefs en Bills",
            "Buffalo es 9-1, pero nuestro modelo ve una moneda al aire",
            [Matchup("Chiefs", "8-2", "Bills", "9-1", sep="visita a · récord"),
             Stats([("51%", "gana Kansas City (80%: 41–60%)", ACC),
                    ("7.2", "victorias que dicen los puntos de Buffalo (tiene 9)", AMBER),
                    ("5-1 · 0-4", "Allen ante Kansas City: temporada regular · playoffs", NEG)])],
            takeaway="Lluvia, 3 °C y viento de 30 km/h. Quien gane se queda con el liderato de la Conferencia Americana. ¿Mahomes o Allen?",
            style="cover", method=LEGAL_NFL, title_size=56),
        "2-ligamx-leon-cruzazul": slide(1, 6, "Liga MX · Cuartos de final, ida · Hoy jueves 26 · 21:10 CDMX",
            "El campeón visita León: Cruz Azul avanza 2 de cada 3 veces",
            [Matchup("León", "7° · 26 pts", "Cruz Azul", "2° · 32 pts", sep="recibe a · lugar · puntos"),
             Stats([("67%", "avanza Cruz Azul (rango 65–71%)", ACC),
                    ("39%", "gana León la ida; empate 24%", AMBER),
                    ("22%", "Cruz Azul avanza si pierde por 2 o más", NEG)])],
            takeaway="Cruz Azul nunca ha sido bicampeón en torneos cortos. ¿Esta ida lo acerca o lo complica?",
            style="cover", method=LEGAL_MX, title_size=56),
        "3-nba-lal-sas": slide(1, 6, "NBA Cup · Mañana viernes 27 · 20:30 CDMX · Lakers en Spurs",
            "Los Lakers van 15-3, pero sus puntos dicen 11-7",
            [Matchup("Lakers", "15-3", "Spurs", "15-4", sep="visita a · récord"),
             Stats([("68%", "gana San Antonio (80%: 56–79%)", ACC),
                    ("1 en 27", "que un equipo con su diferencial vaya 15-3", AMBER),
                    ("58%", "San Antonio si Wembanyama no juega (duda)", NEG)])],
            takeaway="+3.4 puntos por partido alcanzan para 11 victorias, no para 15. ¿Suerte en los cierres o equipo de élite?",
            style="cover", method=LEGAL_NBA, title_size=58),
        "4-ligamx-vuelta": slide(1, 6, "Liga MX · Cuartos de final, vuelta · Sábado 28 · 19:00 y 21:10 CDMX",
            "Atlas necesita ganar por 2. Le pasa 15 de cada 100 veces",
            [HBars([("Toluca (ganó 2-0)", 85, ACC), ("América (0-0)", 77, ACC),
                    ("Avanzan los dos", 66, AMBER), ("Atlas remonta", 15, NEG)], 100, "{}%", 340)],
            takeaway="Monterrey solo necesita ganar en casa del América, y le pasa 23 de cada 100. ¿Quién da la sorpresa?",
            style="cover", method=LEGAL_MX2, title_size=56),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
