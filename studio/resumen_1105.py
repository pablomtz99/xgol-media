"""xGol — Resumen del miércoles 4 nov: Champions J4 (9 partidos, modelo xGol UCL v0.1) + NBA (14 partidos, modelo NBA v1).
Predicciones: studio/posts_1104.py y studio/models/ucl_model_v01_1104.py (commit 70768d1, 4 nov 10:55 CDMX, antes del primer partido 11:45).
NBA: reproducidas el 5 nov con nba_ridge_1103.py y los 107 partidos al 2 nov (coinciden con los 9 % publicados en los slides del 4 nov).
OJO: esas previas se renderizaron pero no se publicaron en Instagram.
Resultados Champions (2 fuentes): Blueprint (blueprint.ng) y The Sports Encounter. NBA: Land of Basketball (resumen diario 4 nov);
Celtics 109-102 Bucks y Knicks 135-105 Bulls confirmados en ESPN.
Cálculos: Brier 3 vías (futbol) y 2 vías (NBA); aciertos = Poisson-binomial; goles = Poisson."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1105")
K = "Resumen · Miércoles 4 de noviembre"
METHOD = ("Método: probabilidades calculadas antes de cada partido. Champions: modelo xGol UCL v0.1 (goles Poisson por equipo, 63 partidos). "
          "NBA: nuestro modelo NBA v1 (ataque y defensa ajustados por rival, 107 partidos). Brier = error promedio, menos es mejor "
          "(volado: 0.25 en NBA; 1/3 a cada resultado: 0.67 en futbol). Aciertos esperados = suma de las probabilidades de cada favorito "
          "(Poisson-binomial). Resultados: Land of Basketball, ESPN, Blueprint, The Sports Encounter. "
          "Análisis independiente, no afiliado a la UEFA, la NBA ni los clubes. No es recomendación de apuesta.")


class Results(Block):
    """Lista compacta: ✓/✗ · marcador · probabilidad que le dimos al favorito."""
    flex = 1; maxgrow = 1.5

    def __init__(self, rows): self.rows = rows

    def natural(self, d): return 92 * len(self.rows)

    def draw(self, d, y, h):
        rh = h / len(self.rows)
        for ok, game, fav in self.rows:
            col = ACC if ok else NEG
            cy = y + rh / 2
            d.ellipse((M, cy - 22, M + 44, cy + 22), fill=col)
            if ok:
                d.line((M + 11, cy, M + 19, cy + 9), fill=BG, width=6); d.line((M + 19, cy + 9, M + 33, cy - 9), fill=BG, width=6)
            else:
                d.line((M + 13, cy - 9, M + 31, cy + 9), fill=BG, width=6); d.line((M + 31, cy - 9, M + 13, cy + 9), fill=BG, width=6)
            d.text((M + 70, cy - 22), game, font=F("InterDisplay-Bold.otf", 36), fill=TXT)
            f = F("Inter-SemiBold.otf", 28)
            d.text((W - M - tw(d, fav, f), cy - 16), fav, font=f, fill=col if not ok else MUTED)
            d.line((M, y + rh, W - M, y + rh), fill=LINE, width=1)
            y += rh


def R():
    T = 6
    return [
        slide(1, T, K, "Miércoles: ganaron 16 de nuestros 23 favoritos. Esperábamos 14",
              [Hero("16 de 23", "favoritos de nuestros modelos ganaron entre Champions y NBA. La suma de sus probabilidades daba 14.", ACC),
               Stats([("7 de 9", "en Champions (esperábamos 4.8)", ACC),
                      ("9 de 14", "en NBA: justo los «unos 9» que dijimos", ACC),
                      ("44", "goles en 9 partidos de Champions; esperábamos 33", AMBER)])],
              takeaway="Lo publicamos igual cuando fallamos. Hoy tocó una buena noche: aquí está cuánto fue mérito y cuánto suerte.", style="cover"),
        slide(2, T, "Champions · 9 partidos", "7 de 9 favoritos ganaron. Fallaron Liverpool y PSV",
              [Results([(True, "AEK 2-3 Real Madrid", "Madrid 69%"),
                        (True, "Leipzig 2-3 Man. City", "City 49%"),
                        (True, "Slavia 1-2 Arsenal", "Arsenal 58%"),
                        (True, "Lens 1-9 Como", "Como 40%"),
                        (True, "Dortmund 2-1 Betis", "Dortmund 52%"),
                        (True, "Porto 4-1 Napoli", "Porto 53%"),
                        (True, "Viking 4-1 Sabah", "Viking 55%"),
                        (False, "Fenerbahçe 3-2 Liverpool", "Liverpool 55%"),
                        (False, "PSV 1-2 Brujas", "PSV 47%")])],
              takeaway="Error 0.44 (Brier; menos es mejor). Al azar: 0.67. Repartiendo como la historia de la Champions: 0.62.",
              title_size=66),
        slide(3, T, "NBA · 14 partidos", "Dijimos «unos 9 de 14». Fueron 9",
              [Stats([("9.2", "favoritos que esperábamos", GHOST), ("9", "los que ganaron", ACC), ("0.207", "error (Brier). Un volado: 0.25", ACC)]),
               Results([(True, "Celtics 109-102 Bucks", "Boston 80%"),
                        (True, "Spurs 112-111 Mavericks", "San Antonio 79%"),
                        (False, "76ers 112-106 Pistons", "Detroit 68%"),
                        (False, "Timberwolves 117-107 Rockets", "Houston 58%"),
                        (False, "Pacers 107-103 Grizzlies", "Memphis 70%"),
                        (False, "Hornets 104-114 Nets", "Charlotte 57%"),
                        (False, "Heat 117-116 Clippers (TE)", "Clippers 54%")])],
              takeaway="Los 4 favoritos más claros (78% a 81%) ganaron. Los 5 fallos fueron favoritos de 54% a 70%: ahí el modelo casi no sabe.",
              title_size=76),
        slide(4, T, "Calibración", "Mientras más seguros, más acertamos",
              [Table(("Esperábamos", "Ganaron"),
                     [("Favoritos de 40% a 60% (13 partidos)", "6.9", "8"),
                      ("Favoritos de 61% a 70% (6 partidos)", "4.0", "4"),
                      ("Favoritos de 78% a 81% (4 partidos NBA)", "3.2", "4")], colors=[GHOST, ACC]),
               Tests([(None, "¿Fue habilidad o suerte?", "Con estas probabilidades, acertar 16 o más de 23 pasa 26 de cada 100 noches. Buena noche, no milagro.", "Poisson-binomial · P(aciertos ≥ 16) = 0.26 · n = 23")])],
              takeaway="Con 23 partidos la calibración es una pista, no una prueba. La medimos en el acumulado."),
        slide(5, T, "La lluvia de goles", "Martes faltaron 11 goles; miércoles sobraron 11",
              [Stats([("22 de 33", "goles el martes (8 partidos)", NEG), ("44 de 33", "goles el miércoles (9 partidos)", AMBER)]),
               Hero("66 de 65.5", "goles en los 17 partidos que pronosticamos de la jornada 4. Se emparejó.", ACC, maxsize=170),
               Tests([(True, "Regresión a la media", "44 o más en un día pasa 4 de cada 100 veces; en la jornada completa, la diferencia es medio gol. ¿Los 9 de Como en Lens? 1 en 12,800.", "Poisson · P(X ≥ 44 | λ = 32.8) = 0.036")])],
              takeaway="Lección: no corregir el modelo por un solo día.", title_size=70),
        slide(6, T, "Lo que aprendimos", "Buena noche, sin sacar el pecho",
              [Bullets(["16 de 23 favoritos ganaron; esperábamos 14.",
                        "NBA: dijimos unos 9 de 14 y fueron 9.",
                        "Champions: 7 de 9, error 0.44 (azar: 0.67).",
                        "Goles: la jornada completa cuadró (66 vs 65.5)."])],
              takeaway="¿Qué resultado del miércoles no viste venir? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
