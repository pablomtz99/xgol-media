"""xGol — «El fin de semana de los clásicos» (post temático, diseño v7)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/clas")


class Agenda(Block):
    flex = 2; maxgrow = 1.5
    def __init__(self, rows): self.rows = rows
    def natural(self, d): return 112 * len(self.rows)
    def draw(self, d, y, h):
        rh = h / len(self.rows)
        for i, (day, hour, match, comp) in enumerate(self.rows):
            yy = y + i * rh
            d.rounded_rectangle((M, yy, W - M, yy + rh - 14), radius=18, fill=SURF)
            d.text((M + 24, yy + (rh - 14) / 2 - 34), day, font=F("Inter-Bold.otf", 24), fill=ACC)
            d.text((M + 24, yy + (rh - 14) / 2 - 4), hour, font=F("InterDisplay-Black.otf", 34), fill=TXT)
            d.text((M + 200, yy + (rh - 14) / 2 - 36), match, font=F("InterDisplay-Bold.otf", 38), fill=TXT)
            d.text((M + 200, yy + (rh - 14) / 2 + 10), comp, font=F("Inter-Medium.otf", 24), fill=MUTED)


def P():
    T = 7
    return [
        slide(1, T, "Futbol · 31 de octubre y 1 de noviembre", "El fin de semana de los clásicos",
              [Hero("5", "clásicos en menos de 48 horas: Alemania, Italia, México, Inglaterra y Argentina.", ACC, maxsize=380)],
              takeaway="Lo que dicen los números de cada uno, y un dato que se repite en casi todos.", style="cover", title_size=100),
        slide(2, T, "La agenda · hora CDMX", "Guarda las fechas",
              [Agenda([("SÁB 31", "11:30", "Bayern vs. Dortmund", "Bundesliga · «Der Klassiker»"),
                       ("SÁB 31", "13:45", "Milan vs. Inter", "Serie A · Derbi de Milán"),
                       ("SÁB 31", "21:10", "América vs. Toluca", "Liga MX · revancha de la final del Clausura 2025"),
                       ("DOM 1", "10:30", "Liverpool vs. Arsenal", "Premier League · en Anfield"),
                       ("DOM 1", "12:00", "Boca vs. River", "Argentina · Superclásico en La Bombonera")])],
              takeaway="Desliza: qué tienen en común y qué tiene de especial cada uno."),
        slide(3, T, "Lo que se repite", "En los clásicos hay más empates de lo normal",
              [Hero("32%", "de los clásicos terminaron empatados: casi 1 de cada 3.", ACC),
               HBars([("Clásicos", 31.5, ACC), ("Partido típico", 26, GHOST)], 35, "{}%", 300)],
              takeaway="Sumando 514 partidos de Boca-River, Milan-Inter (Serie A) y Liverpool-Arsenal (Premier). En una liga, alrededor de 1 de cada 4 partidos termina empatado.", tag="DATO 1 DE 3"),
        slide(4, T, "La excepción", "El único clásico desequilibrado: Bayern vs. Dortmund",
              [Stats([("231", "goles de Bayern en 113 clásicos de Bundesliga", ACC), ("141", "goles de Dortmund", GHOST)]),
               Stats([("2.0", "goles por partido de Bayern en el clásico", ACC), ("1.2", "de Dortmund", GHOST)])],
              takeaway="En los otros clásicos nadie domina (Boca 94 vs. River 88; Inter 70 vs. Milan 57 en Serie A). En Alemania, Bayern sí.", tag="DATO 2 DE 3"),
        slide(5, T, "Lo que está en juego", "Tres clásicos con algo extra",
              [Bullets(["Liverpool vs. Arsenal: Arsenal llega empatado en la cima con el City (21 puntos); con una victoria puede quedar líder solo.",
                        "América vs. Toluca: el líder contra uno de los de arriba, y Toluca le ganó la final del Clausura 2025.",
                        "Milan vs. Inter: los dos jugaron el miércoles; el cansancio y las rotaciones pueden pesar."])],
              tag="DATO 3 DE 3"),
        slide(6, T, "Lo que probamos", "¿Es casualidad?",
              [Tests([(True, "«En los clásicos hay más empates»", "162 empates en 514 partidos (31.5%) contra ~26% de un partido típico. Muy difícil que sea casualidad.", "p = 0.003"),
                      (False, "«Inter domina el derbi de Milán»", "Inter lleva 13 victorias más en Serie A, pero con tantos partidos eso todavía cabe en el azar.", "184 partidos · p = 0.29"),
                      (True, "«Bayern domina a Dortmund»", "231 goles contra 141: la diferencia es enorme y constante.", "113 partidos")])],
              takeaway="Si un clásico te parece parejo, probablemente lo es: casi 1 de cada 3 termina empatado."),
        slide(7, T, "Conclusión", "Lo que hay que saber antes del fin de semana",
              [Bullets(["Los clásicos se empatan más que un partido normal: casi 1 de cada 3.", "La excepción es Alemania: Bayern domina a Dortmund.", "Liverpool-Arsenal puede cambiar al líder de la Premier."])],
              takeaway="¿Cuál de los cinco no te pierdes? Te leemos.", style="end",
              method="Método: historiales oficiales de liga (Boca-River 266 partidos; Milan-Inter 184 en Serie A, al 8 mar 2026; Liverpool-Arsenal 64 en Premier League, al feb 2024; Bayern-Dortmund 113 en Bundesliga). Prueba binomial contra una tasa de empate de ~26%, aproximada para ligas de primera división. Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta."),
    ]


if __name__ == "__main__":
    o = f"{OUT}/P"; os.makedirs(o, exist_ok=True)
    for i, im in enumerate(P(), 1):
        im.save(f"{o}/{i:02d}.png")
    print("ok")
