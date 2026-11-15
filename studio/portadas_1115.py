"""xGol — portadas de las 4 ideas del 15 nov (NFL, semana 10). Diseño v7.
Datos: nflverse (CC-BY 4.0) schedules/games.csv + play_by_play_2026 (semanas 1–9, 16,864 jugadas de pase/carrera).
Modelo NFL v0: margen = 0.5 × (EPA neta/jugada local − visitante) × 61.6 + 1.5; P = Φ(margen/13.5). Rangos 10–90%: bootstrap de partidos (400).
Validación fuera de muestra 2026 (sem. 4–9, solo datos previos): 87 partidos, 55 aciertos vs 55.0 esperados, Brier 0.228, Spiegelhalter p = 0.78.
SIN NBA: xgol-data no accesible (add_repo no disponible). Futbol y Liga MX: fecha FIFA (Liga MX vuelve el 20 nov, J17).
Horarios ET; CDMX = ET − 1 h: 16:05 ET = 15:05 CDMX.
1) LA@ARI (dom 15:05). Rams 68.6% (51–82%), margen +6.5. Calidad: LA 4°, ARI 27°. Pase permitido ARI +0.215 (31°); defensa de pase LA 3°.
   ARI ganó 18-16 en LA (sem. 6). Rams 5-4, 3 seguidas; 2-3 en cerrados. ARI 3-6, Pitágoras 2.7.
   ARI: Carson Beck (novato) 1er inicio; Minshew a IR (codo, temporada). LA: Nacua fuera ≥1 mes; Adams en IR (therams.com, arizonasports.com).
   Debutantes titulares 2010–2025 (games.csv, 1er inicio por qb_id, temporada regular, n = 173): ganan 32% (55.5) vs 36% esperado
   antes del partido (mercado); margen real vs esperado +0.3 pts (IC95 −1.7 a +2.4), p = 0.76.
2) SEA@LV (dom 15:05). Seattle 60.3% (46–74%), margen +3.5. SEA 11°, LV 26°. Defensa SEA 5°; defensa LV 31°; carrera LV 32° (−0.232).
   LV: Fernando Mendoza 1er inicio (Cousins traspasado a MIN); Kubiak, coord. ofensivo de SEA en el título 2025 (raiders.com).
   SEA: Drew Lock por Darnold (costilla) (abc7). Récords 5-4 y 4-5. Puntos: LV 26.4/29.8, SEA 22.4/18.0.
3) Rompemitos divisional: 2010–2025, 4,099 partidos (sin neutrales/empates): el favorito gana 67.3% en divisionales (1,519) vs 65.9%;
   logit con margen esperado: coef. divisional +0.008, p = 0.91; margen real − esperado 0.07 vs 0.10, p = 0.93. 6 divisionales hoy.
4) Denver 7-2, 6-0 en partidos por ≤8 (P = 1/64 si 50/50); Pitágoras 4.8; calidad 16° (−0.006). Equipos 5-0+ en cerrados tras 9 juegos
   (n = 11): 26-17 (60%) después; r cerrados 1a vs 2a parte = 0.08 (p = 0.07). Monte Carlo 10,000 temporadas: playoffs 92%,
   división 43% (KC 56%), 11.4 victorias (10–13). Se recalcula el lunes con resultados del domingo (DEN descansa)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1115")
LEGAL = "Análisis independiente, no afiliado a la NFL ni a los equipos. No es recomendación de apuesta. Datos: nflverse."
SEP = "visitan a · récord · lugar en calidad real"


def covers():
    return {
        "1-nfl-la-ari": slide(1, 6, "NFL · Semana 10 · Domingo 15 nov · 15:05 CDMX · Arizona",
            "Arizona ya le ganó a los Rams. Hoy lo intenta con un novato en su primer partido",
            [Matchup("Rams", "5-4 · 4°", "Cardinals", "3-6 · 27°", sep=SEP),
             Stats([("69%", "gana Los Ángeles (51–82%)", GHOST),
                    ("1 de 3", "debutantes gana (173 casos, 2010–2025)", AMBER),
                    ("31°", "defensa de pase de Arizona", ACC)])],
            takeaway="Carson Beck debuta; los Rams, sin Nacua ni Adams. ¿Se repite el 18-16 o pesa la diferencia de calidad?",
            style="cover", method=LEGAL, title_size=62),
        "2-nfl-sea-lv": slide(1, 6, "NFL · Semana 10 · Domingo 15 nov · 15:05 CDMX · Las Vegas",
            "El campeón llega sin su mariscal y Las Vegas estrena novato. Seattle gana 3 de cada 5",
            [Matchup("Seahawks", "5-4 · 11°", "Raiders", "4-5 · 26°", sep=SEP),
             Stats([("60%", "gana Seattle (46–74%)", GHOST),
                    ("32°", "ataque por tierra de Las Vegas", AMBER),
                    ("5°", "defensa de Seattle en calidad", ACC)])],
            takeaway="Lock por Darnold; Mendoza debuta con Kubiak, el exestratega de Seattle. ¿Quién sabe más del otro?",
            style="cover", method=LEGAL, title_size=60),
        "3-nfl-divisionales": slide(1, 6, "NFL · Semana 10 · Rompemitos · 6 duelos de división hoy",
            "«En la división todo se empareja». Revisamos 4,099 partidos: es un mito",
            [HBars([("Divisionales", 67.3, ACC), ("No divisionales", 65.9, GHOST)], 100, "{}%", 330),
             Stats([("p = 0.91", "diferencia por ser divisional", AMBER),
                    ("1,519", "partidos divisionales (2010–2025)", GHOST),
                    ("3.9 de 6", "victorias esperadas de los favoritos de hoy", ACC)])],
            takeaway="El favorito gana 2 de cada 3 con o sin rivalidad. ¿Cuál de los 6 favoritos de hoy cae?",
            style="cover", method=LEGAL, title_size=62),
        "4-nfl-denver": slide(1, 6, "NFL · Semana 10 · Lunes 16 nov · Probabilidades de playoffs",
            "Denver va 6-0 en partidos cerrados. A puro volado, eso sale 1 de cada 64",
            [HBars([("Victorias reales", 7, ACC), ("Según sus puntos", 4.8, GHOST)], 9, "{}", 360),
             Stats([("92%", "llega a playoffs (10,000 temporadas)", GHOST),
                    ("60%", "cerrados que ganaron después los que iban invictos (n = 11)", AMBER),
                    ("10–13", "victorias finales de Denver (80%)", ACC)])],
            takeaway="Es el 16° de 32 en calidad, pero las victorias ya están en la bolsa. ¿Denver es candidato o espejismo?",
            style="cover", method=LEGAL, title_size=66),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
