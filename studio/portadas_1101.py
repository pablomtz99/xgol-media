"""xGol — portadas de las 4 ideas del 1 nov (dom 1 – lun 2 nov). Diseño v7."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1101")
LEGAL = "Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta."


def covers():
    return {
        "1-nfl-phi-was": slide(1, 7, "NFL · Semana 8 · Domingo 1 de noviembre · 19:20 CDMX",
            ".269: el domingo por la noche más pobre en 20 años",
            [Matchup("Eagles", "2-5", "Commanders", "1-4-1", sep="visitan a · Washington, sin Jalen Hurts (lesionado)"),
             Stats([("67%", "nuestro modelo: gana Washington (rango 57–76%)", ACC),
                    ("+0.7", "puntos que da la semana de descanso (p = 0.28)", GHOST)])],
            takeaway="Washington viene de descansar 13 días. Lo probamos en 436 partidos: el descanso extra no se distingue del azar.",
            style="cover", method=LEGAL),
        "2-nfl-chi-sea": slide(1, 7, "NFL · Semana 8 · Lunes 2 de noviembre · 19:15 CDMX",
            "El «jugador 12» de Seattle valía 9 puntos. Hoy vale 3",
            [Matchup("Bears", "5-2", "Seahawks", "4-3", sep="visitan a · Seattle, el campeón vigente"),
             Stats([("+9.3", "ventaja en casa de Seattle 2010–14", ACC), ("+3.2", "desde 2020 (liga: +1.7)", AMBER),
                    ("58%", "gana Seattle (rango 42–73%)", GHOST)])],
            takeaway="Su ventaja en casa fue real (p = 0.006), pero regresó a la media: desde 2020 ya no se distingue de la liga.",
            style="cover", method=LEGAL),
        "3-nba-mem-nop": slide(1, 7, "NBA · Lunes 2 de noviembre · 19:00 CDMX",
            "Memphis 6-0: ¿equipo de verdad o calendario fácil?",
            [Matchup("Pelicans", "2-4", "Grizzlies", "6-0", sep="visitan a · Memphis, único invicto de la NBA"),
             Stats([("+15", "puntos de ventaja por partido", ACC), ("3°", "calendario más fácil de 30", AMBER),
                    ("71%", "gana Memphis (59–78%)", GHOST)])],
            takeaway="Un equipo promedio con ese calendario se va 6-0 1 de cada 47 veces. Memphis es bueno… pero no +15.",
            style="cover", method=LEGAL),
        "4-nba-b2b": slide(1, 7, "NBA · Lunes 2 de noviembre · 15 partidos",
            "8 equipos juegan dos noches seguidas. ¿Cuántos sobreviven?",
            [Stats([("8", "equipos repiten el lunes tras jugar el domingo", ACC),
                    ("−2.1", "puntos por cansancio (p = 0.011)", AMBER)]),
             Stats([("2.7", "victorias esperadas de 6 (Raptors y Clippers: los dos repiten)", GHOST), ("0.6%", "que ganen los 6", GHOST)])],
            takeaway="Celtics, Lakers, Warriors y compañía: simulamos 100,000 lunes. Lo más probable: 3 de 6 ganan.",
            style="cover", method=LEGAL),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok")
