"""xGol — Resumen del martes 3 nov: Champions League, jornada 4 (8 partidos con predicción). Diseño v7.
Predicciones: studio/posts_1103.py (commit 4922760, 3 nov 10:21 CDMX, antes del primer partido de las 11:45).
OJO: esas previas se renderizaron pero no se publicaron en Instagram (no hay queue/ ni published/ del 3 nov).
Resultados (2 fuentes): CBS Sports (calendario UCL) y Once Noticias; parciales en Yahoo y La Nación.
Cálculos: Brier de 3 resultados; distribución de aciertos = Poisson-binomial con la prob. del favorito;
goles: Poisson con λ = suma de goles esperados (32.7)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1104")
K = "Resumen · Champions League · Jornada 4 · Martes 3 nov"
METHOD = ("Método: probabilidades de nuestro modelo xGol UCL v0 (Poisson por equipo, 54 partidos J1–J3) calculadas antes de cada partido. "
          "Brier = suma de (probabilidad − resultado)² en local/empate/visita; 1/3 a cada uno da 0.67. Aciertos esperados = suma de la probabilidad "
          "de cada favorito; su distribución, Poisson-binomial. Goles: Poisson con 32.7 esperados. Resultados: CBS Sports, Once Noticias. "
          "Análisis independiente, no afiliado a la UEFA ni a los clubes. No es recomendación de apuesta.")


def R():
    T = 6
    return [
        slide(1, T, K, "Champions, martes: acertamos 4 de 8. Nuestras probabilidades esperaban 4",
              [Hero("4 de 8", "favoritos de nuestro modelo ganaron. La suma de sus probabilidades daba 4.05.", ACC),
               Stats([("0.59", "error promedio (Brier; menos es mejor). Al azar: 0.67", ACC),
                      ("22", "goles en 8 partidos; esperábamos 33", NEG),
                      ("1 de 8", "empates; le dábamos ~20% a cada uno", GHOST)])],
              takeaway="Lo publicamos igual cuando fallamos: qué salió, qué no y qué aprendimos.", style="cover"),
        slide(2, T, "Los aciertos", "4 favoritos cumplieron, uno remontando",
              [Tests([(True, "PSG 6-0 en Villarreal", "50% para el mejor ataque del torneo. La goleada de la noche.", "PSG: 50% · empate 18% · Villarreal 32%"),
                      (True, "Barcelona 3-0 Aston Villa", "Dijimos que el 9 de 9 de Villa tenía algo de fortuna. Se acabó el perfecto.", "Barcelona: 60%"),
                      (True, "Galatasaray 2-0 Stuttgart", "Estambul pesó: se acabó el invicto de Stuttgart.", "Galatasaray: 52%"),
                      (True, "Man. United 3-2 Roma", "Remontada dramática. Los dos tenían menos puntos de los que merecían.", "United: 45% · empate 21% · Roma 35%")])],
              title_size=72),
        slide(3, T, "Los fallos", "4 favoritos cayeron; en 3 avisamos el riesgo",
              [Tests([(False, "Atlético 0-2 Bayern", "Avisamos que el modelo no veía las bajas de Bayern. Ganó igual: 25 partidos seguidos anotando.", "Atlético: 48% · Bayern: 31%"),
                      (False, "Shakhtar 0-1 Sporting", "Avisamos que su localía «prestada» estaba sobreestimada.", "Shakhtar: 49% · Sporting: 29%"),
                      (False, "Bodø/Glimt 0-0 Lille", "El único empate de la noche: le dábamos 18%.", "Bodø: 60% · empate: 18%"),
                      (False, "Feyenoord 0-3 Inter", "Dijimos que Inter merecía más puntos y no había que darlo por muerto.", "Feyenoord: 42% · Inter: 36%")])],
              title_size=72),
        slide(4, T, "Calibración", "Cuando dijimos «1 de 2», salió 1 de 2",
              [Table(("Esperábamos", "Ganaron"),
                     [("Favoritos de 42% a 50% (5 partidos)", "2.3", "2"),
                      ("Favoritos de 52% a 60% (3 partidos)", "1.7", "2")], colors=[GHOST, ACC]),
               Tests([(True, "4 aciertos: justo lo normal", "Con estas probabilidades, acertar 4 o más pasa 65 de cada 100 noches. No fue suerte ni mala suerte.", "Poisson-binomial · P(aciertos ≥ 4) = 0.65 · n = 8")])],
              takeaway="Con 8 partidos la calibración es solo una pista. La medimos en el acumulado."),
        slide(5, T, "La falla de la noche", "La lluvia de goles paró: 22 de 33 esperados",
              [Stats([("2.75", "goles por partido el martes (8 partidos)", NEG),
                      ("4.1", "goles por partido en las jornadas 1–3", GHOST),
                      ("4 de 8", "partidos con 3 goles o más; esperábamos 6", AMBER)]),
               Tests([(False, "«El modelo calculó bien los goles»", "Con 33 esperados, ver 22 o menos pasa 3 de cada 100 veces. Le creímos demasiado a 54 partidos con muchos goles: regresión a la media.", "Poisson · P(X ≤ 22 | λ = 32.7) = 0.03"),
                      ])],
              takeaway="Y la localía: 4 victorias locales y 4 visitantes. Para la jornada 5, más peso al promedio histórico."),
        slide(6, T, "Lo que aprendimos", "Ganadores bien, goles de más",
              [Bullets(["4 de 8 favoritos ganaron: lo que nuestras probabilidades esperaban.",
                        "Error 0.59, mejor que el azar (0.67).",
                        "Fallamos en goles: 22 reales contra 33 esperados.",
                        "Bajas y localías prestadas: los riesgos que avisamos sí pesaron."])],
              takeaway="¿Qué resultado del martes te sorprendió más? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    o = f"{OUT}/R"; os.makedirs(o, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{o}/{i:02d}.png")
    print("ok")
