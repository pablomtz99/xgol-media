"""xGol — portadas de las 4 ideas del 18 nov. Diseño v7. Cálculos: studio/models/*_1118.py. Datos NFL: nflverse (CC-BY 4.0), pbp 2019–2026 y games.csv.
SIN xgol-data (add_repo no disponible). SIN tenis ni futbol: ATP Finals sin fuente de datos para modelar; fecha FIFA; Liga MX regresa el 20 nov.
1) Mariscal nuevo (QB principal distinto al del partido anterior y con <25% de los pases previos del equipo), v0 fuera de muestra, sem. 4+, 2019–2025:
   1er partido n=249, error −4.63 pts (80%: −5.77 a −3.54), p=2.7e-7; 2° n=134, −3.12 (−4.62 a −1.60), p=0.010; 3° n=97, −1.94, p=0.16; 4°+ n=248, −0.47, p=0.57.
   Robustez con titular oficial de games.csv: n=186, −4.50, p=1.1e-5. Corrección fuera de muestra 2020–2026 (efecto estimado solo con años previos): Brier 0.2281→0.2233, 1,425 partidos.
   Semana 11, 2° partido: MIN (Cousins), BAL (Brissett), ARI (Beck), LV (Mendoza), MIA (McCord). SF vs MIN: 66.4% (58.0–75.4) → 74.4% (66.8–82.1). Cousins debutó 30-10 vs GB.
2) Regresión a la media, corte a 9 partidos, 2002–2025, n=768: récord ≥15 puntos de % arriba de lo que implica su diferencial, n=66: 69.4%→52.4%, bajan 75.8% (80%: 69.7–83.3), p=5e-8.
   Sensibilidad: umbral 10: 73%; 20: 86%. R² fuera de muestra (dejando una temporada fuera): diferencial 0.244, récord 0.204. DEN 7-2, +1.33, 17° en calidad; resto esperado 54.9% (28.3–81.5). TB 3-6, +2.67.
3) IND@HOU (jue 19, 20:15 ET = 19:15 CDMX). HOU 70.4% (59.1–80.1). Jueves vs domingo 2012–2025: local +1.32 (n=235) vs +2.15 (n=3,020), p=0.39; vs mercado p=0.50. Pase HOU 8° vs defensa de pase IND 19°;
   carrera HOU 24° vs defensa de carrera IND 32°. No entrenaron el martes 17 (SI): Hunter, Harrison Jr., Marks (HOU); Gardner, Ward, Raimann (IND).
4) Grimes: 10 de 14 vs CHA (CBS) y 5 de 6 vs PHX (NBC) = 15 de 20. Carrera 36.6% (Wikipedia; statz 37.1%). P(≥15 de 20 | 36.6%) = 0.00054 = 1 en 1,841. Temporada 43.4% en 7.6 intentos × 13 partidos (statz) ≈ 43/99,
   p=0.17 vs carrera. Nivel estimado Beta (prior 750 intentos, supuesto): 37.4% (35.3–39.5). Esperados: 7.6 × 0.374 = 2.8 triples. UTA@LAL 22:00 ET = 21:00 CDMX."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1118")
LEGAL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: CBS Sports, NBC Sports, Statz."


def covers():
    return {
        "1-nfl-mariscal-nuevo": slide(1, 6, "NFL · Semana 11 · Lo que probamos · 2019–2025",
            "Estrenar mariscal cuesta 4.6 puntos. Esta semana, 5 equipos van por su segundo partido",
            [HBars([("1er partido", 4.6, NEG), ("2° partido", 3.1, AMBER), ("3° (solo indicio)", 1.9, GHOST), ("4° en adelante", 0.5, GHOST)], 6, "−{} pts", 300),
             Stats([("249", "debuts · p < 0.001", ACC),
                    ("74%", "San Francisco, ya ajustado (67–82%)", AMBER),
                    ("0.223", "error con ajuste; sin él, 0.228", GHOST)])],
            takeaway="Sin ajuste, San Francisco tenía 66%. Cousins debutó ganando por 20: ¿Minnesota rompe la regla en la Ciudad de México?",
            style="cover", method=LEGAL, title_size=58),
        "2-nfl-denver-regresion": slide(1, 6, "NFL · Regresión a la media · 768 equipos · 2002–2025",
            "Denver va 7-2 con solo +1.3 puntos por partido. 3 de cada 4 equipos así bajaron después",
            [HBars([("Primeros 9", 69.4, GHOST), ("Resto del año", 52.4, ACC)], 100, "{}%", 300),
             Stats([("76%", "de 66 equipos así ganaron menos (70–83%)", ACC),
                    ("p < 0.001", "la caída no es casualidad", GHOST),
                    ("55%", "esperamos que gane Denver de aquí al final (28–82%)", AMBER)])],
            takeaway="El caso contrario: Tampa Bay va 3-6 y supera a sus rivales por 2.7 puntos. ¿A cuál le crees?",
            style="cover", method=LEGAL, title_size=60),
        "3-nfl-ind-hou-jueves": slide(1, 6, "NFL · Semana 11 · Jueves 19 nov · 19:15 CDMX · Houston",
            "¿La semana corta le quita la localía a Houston? En 235 jueves, no. Nuestro modelo le da 70%",
            [Matchup("Colts", "3-7 · 28°", "Texans", "3-6 · 11°", sep="visitan a · récord · lugar en calidad real"),
             Stats([("70%", "gana Houston (59–80%)", GHOST),
                    ("p = 0.39", "local en jueves +1.3 vs. domingo +2.2 puntos", AMBER),
                    ("8° vs 19°", "pase de Houston contra defensa de pase de Indianapolis", ACC)])],
            takeaway="Hunter, de Houston, y Gardner y Ward, de Indianapolis, no entrenaron el martes. ¿Quién llega completo?",
            style="cover", method=LEGAL, title_size=58),
        "4-nba-grimes": slide(1, 6, "NBA · Hoy · 21:00 CDMX · Jazz en Lakers · Los Ángeles",
            "Quentin Grimes metió 15 de 20 triples en dos partidos: a su nivel, pasa 1 de cada 1,800 veces",
            [HBars([("Últimos 2 partidos", 75.0, ACC), ("Esta temporada", 43.4, AMBER), ("Nivel estimado", 37.4, GHOST), ("Carrera", 36.6, GHOST)], 100, "{}%", 300),
             Stats([("37%", "su nivel real estimado (35–40%)", ACC),
                    ("2.8", "triples esperados hoy en unos 8 intentos", AMBER),
                    ("p = 0.17", "su temporada aún no se distingue de su carrera", GHOST)])],
            takeaway="¿Mano caliente o racha normal? Hoy, ante Utah, hay una nueva prueba. ¿Cuántos mete?",
            style="cover", method=LEGAL_NBA, title_size=58),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
