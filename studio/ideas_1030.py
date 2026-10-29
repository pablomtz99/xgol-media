"""xGol — portadas de las 4 ideas del 29 oct (para vie 30 – dom 1 nov). Diseño v7."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas")
LEGAL = "Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta."


def covers():
    return {
        "1-nfl-bal-buf": slide(1, 7, "Futbol americano · NFL · Domingo 1 de noviembre · 12:00 CDMX",
            "Ravens vs. Bills: un regreso que voltea el partido",
            [Matchup("Ravens", "4-3", "Bills", "5-1", sep="visitan a · Buffalo viene de su semana de descanso"),
             Stats([("58%", "Bills, si Baltimore juega como sin Lamar", GHOST), ("48%", "Bills, con el Lamar de las semanas 1–3", ACC)])],
            takeaway="Lamar Jackson vuelve tras 3 partidos fuera. Con él, nuestro modelo NFL ve un volado.", style="cover", method=LEGAL),
        "2-nba-hou-dal": slide(1, 6, "Basquetbol · NBA · Viernes 30 de octubre · 18:00 CDMX",
            "El último invicto: ¿cuánto le dura el 5-0 a Houston?",
            [Matchup("Rockets", "5-0", "Mavericks", "3-2", sep="visitan a · Dallas viene de ganarle por 24 a Oklahoma City"),
             Stats([("7 de 10", "veces gana Houston en Dallas (nuestro modelo)", ACC), ("1 de 3", "llega 7-0 tras recibir a OKC el sábado", GHOST)])],
            takeaway="Gana por 14.2 puntos por partido. Lo que esperamos de aquí en adelante: la mitad.", style="cover", method=LEGAL),
        "3-futbol-liv-ars": slide(1, 6, "Futbol · Premier League · Domingo 1 de noviembre · 10:30 CDMX",
            "Liverpool vs. Arsenal: 0 victorias en 13 visitas a Anfield",
            [Matchup("Liverpool", "4°", "Arsenal", "2°", sep="recibe a · 15 vs. 21 puntos"),
             Stats([("39%", "gana Arsenal (rango 36–42%)", ACC), ("26%", "empate", GHOST), ("35%", "gana Liverpool", GHOST)])],
            takeaway="Arsenal no gana en Anfield desde 2012. Hoy es el mejor equipo por xG. ¿Pesa más la historia o los datos?", style="cover", method=LEGAL),
        "4-ligamx-ame-tol": slide(1, 6, "Futbol · Liga MX · Jornada 15 · Sábado 31 oct · 21:00 CDMX",
            "América vs. Toluca: la tabla dice 5 puntos; el xG dice empate",
            [Matchup("América", "1° · 28", "Toluca", "5° · 23", sep="recibe a · revancha de la final del Clausura 2025"),
             Stats([("24.7", "puntos «merecidos» por xG: América", GHOST), ("25.4", "puntos «merecidos» por xG: Toluca", ACC)])],
            takeaway="América califica si gana. Toluca suma 6 sin ganar. El modelo xGol: América 44%, empate 23%, Toluca 33%.", style="cover", method=LEGAL),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok")
