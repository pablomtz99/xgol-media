"""xGol — portadas de las 4 ideas del 4 nov. Diseño v7.
NFL: datos nflverse (games.csv, play_by_play_2026; semanas 1–8, 14,910 jugadas). Modelo NFL v0 (PLAYBOOK) con EPA neta;
   ajuste sin Lamar = EPA ofensiva de Baltimore en semanas 5–7 (Huntley). Rango 10–90% por bootstrap de jugadas (4,000).
   Lamar vs. resto: EPA por pase 0.36 (n=102) vs −0.11 (n=147), Welch p = 0.029. Locales con margen esperado del mercado
   ≤ −9.5 (temporada regular 1999–2025): 198 partidos, 37 victorias (19%).
   Ranking: ridge por rival (λ=3 partidos) sobre EPA por jugada de cada partido. Fuera de muestra (sem 1–5 → 6–8, n=42):
   Brier 0.245 ajustado vs 0.264 crudo. Victorias esperadas = Φ(EPA neta ajustada × 61.6 / 13.5) × partidos; binomial.
UCL: Modelo xGol UCL v0.1 (studio/models/ucl_model_v01_1104.py), 63 partidos. Puntos «merecidos» con el modelo ajustado
   sin los partidos del equipo; P(0 pts) por enumeración = 0.043. Contexto: The Hard Tackle, The Stats Zone, Yahoo Sports."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1104")
LEGAL_NFL = "Análisis independiente, no afiliado a la NFL ni a los equipos. Datos: nflverse. No es recomendación de apuesta."
LEGAL_UCL = "Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta."


def covers():
    return {
        "1-nfl-jax-bal": slide(1, 7, "NFL · Semana 9 · Jueves 5 de noviembre · 19:15 CDMX",
            "Baltimore, sin Lamar, recibe al nº1 en eficiencia. Jacksonville gana 3 de cada 4",
            [Matchup("Jaguars", "5-2", "Ravens", "4-4", sep="visitan a · Baltimore, sin Lamar Jackson y con Huntley en duda"),
             Stats([("73%", "gana Jacksonville, nuestro modelo (56–86%)", GHOST),
                    ("+0.46", "puntos por pase de Lamar sobre sus suplentes (p = 0.03)", ACC),
                    ("1 de 5", "locales así de relegados ganaron (198 desde 1999)", AMBER)])],
            takeaway="Con toda la temporada, nuestro modelo dice 68%; sin Lamar, 73%. Su 3er QB: −0.43 por pase en 24 jugadas. ¿Hay sorpresa?",
            style="cover", method=LEGAL_NFL, title_size=78),
        "2-nfl-ranking-s9": slide(1, 7, "NFL · Ranking de eficiencia · Antes de la semana 9",
            "Jacksonville es nº1 en nuestro ranking. Minnesota va 6-1… y es 11°",
            [Table(("Récord", "Lugar"), [("Jaguars", "5-2", "1°"), ("49ers", "6-1", "2°"), ("Vikings", "6-1", "11°")], colors=[GHOST, ACC]),
             Stats([("4.1", "victorias esperadas por su juego; tiene 6", AMBER),
                    ("0.245", "error fuera de muestra con ajuste (sin él: 0.264)", ACC),
                    ("p = 0.28", "¿le sobra suerte? Indicio, no prueba", GHOST)])],
            takeaway="Puntos por jugada ajustados por la calidad de cada rival, 32 equipos. ¿Quién está inflado y quién viene subiendo?",
            style="cover", method=LEGAL_NFL, title_size=80),
        "3-ucl-por-nap": slide(1, 7, "Champions · Jornada 4 · Miércoles 4 de noviembre · 14:00 CDMX",
            "Porto tiene 0 puntos. Por sus partidos merecía 4.5: eso pasa 4 de cada 100 veces",
            [Matchup("Napoli", "1-0-2", "Porto", "0-0-3", sep="visita al · Porto, 10 de 10 en la liga portuguesa"),
             Stats([("53%", "gana Porto, modelo xGol (46–60%)", GHOST),
                    ("4.5", "puntos «merecidos» por sus 3 partidos", ACC),
                    ("p = 0.04", "entre 36 clubes es indicio, no prueba", AMBER)])],
            takeaway="Regresión a la media: el líder de Portugal no es de 0 puntos. Y Napoli llega sin Lobotka ni Buongiorno. ¿Hoy empieza la corrección?",
            style="cover", method=LEGAL_UCL, title_size=78),
        "4-ucl-sla-ars": slide(1, 7, "Champions · Jornada 4 · Miércoles 4 de noviembre · 14:00 CDMX",
            "Arsenal tiene la mejor defensa de la Champions. Aun así, Praga le anota 3 de cada 4 veces",
            [Matchup("Arsenal", "2-1-0", "Slavia", "0-1-2", sep="visita al · Slavia Praga; Arsenal sin Saka"),
             Stats([("58%", "gana Arsenal, modelo xGol (49–67%)", GHOST),
                    ("1°", "defensa ajustada por rival (2 goles en 3 partidos)", ACC),
                    ("26%", "chance de que Arsenal no reciba gol", AMBER)])],
            takeaway="Slavia es 30° en ataque y en defensa, pero de local el modelo le da 1.3 goles. ¿Muro o volado?",
            style="cover", method=LEGAL_UCL, title_size=78),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok")
