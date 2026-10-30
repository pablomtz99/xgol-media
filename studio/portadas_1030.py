"""xGol — portadas de las 4 ideas del 30 oct (vie 30 – sáb 31). Diseño v7."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1030")
LEGAL = "Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta."


def covers():
    return {
        "1-nba-nyk-phi": slide(1, 7, "Basquetbol · NBA Cup · Viernes 30 de octubre · 17:30 CDMX",
            "Knicks 2-3, 76ers 4-1… y nuestro modelo ve a Nueva York",
            [Matchup("Knicks", "2-3", "76ers", "4-1", sep="visitan a · revancha del 106-100 del día inaugural"),
             Stats([("55%", "ganan los Knicks (rango 40–70%)", ACC), ("p = 0.55", "¿el 2-3 es crisis? Sin evidencia", GHOST)])],
            takeaway="53-29 el año pasado. Cinco partidos no borran eso; Filadelfia, además, juega mañana otra vez.", style="cover", method=LEGAL),
        "2-nba-sac-mem": slide(1, 7, "Basquetbol · NBA · Sábado 31 de octubre · 18:00 CDMX",
            "5-0 contra 0-5: ¿cuánto de lo de Memphis es real?",
            [Matchup("Kings", "0-5", "Grizzlies", "5-0", sep="visitan a · Memphis ya les ganó 123-112 el 25 de octubre"),
             Stats([("77%", "gana Memphis (rango 63–87%)", ACC), ("~39", "victorias proyectadas para Memphis, no 82", GHOST)])],
            takeaway="Juega 8 puntos mejor de lo esperado: difícil que sea pura suerte (p = 0.04). Pero 5 partidos son pocos.", style="cover", method=LEGAL),
        "3-futbol-che-mun": slide(1, 7, "Futbol · Premier League · Sábado 31 de octubre · 6:30 CDMX",
            "La tabla dice Chelsea. El xG dice United.",
            [Matchup("Chelsea", "13 pts", "Man United", "7 pts", sep="recibe a · el United llega con 8 partidos sin ganar"),
             Stats([("42%", "gana Chelsea (33–52%)", ACC), ("25%", "empate", GHOST), ("33%", "gana el United (25–42%)", GHOST)])],
            takeaway="Chelsea metió 17 goles con ocasiones para 10: pasa 3 de cada 100 veces. ¿Talento o racha que se acaba?", style="cover", method=LEGAL),
        "4-ligamx-pac-tig": slide(1, 7, "Futbol · Liga MX · Jornada 15 · Sábado 31 de octubre · 17:00 CDMX",
            "Algo se rompe: 0 triunfos en casa contra 12 visitas sin ganar",
            [Matchup("Pachuca", "13° · 16 pts", "Tigres", "15° · 15 pts", sep="recibe a · a 4 y 5 puntos del 8° lugar"),
             Stats([("38%", "gana Pachuca", ACC), ("27%", "empate", GHOST), ("35%", "gana Tigres", GHOST)])],
            takeaway="Cada racha pasa menos de 3 de cada 100 veces por azar. El modelo xGol: casi un volado.", style="cover", method=LEGAL),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok")
