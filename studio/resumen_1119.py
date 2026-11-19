"""xGol — Resumen del miércoles 18 nov (NBA): la estimación que fijamos en la portada del 18 nov (studio/portadas_1118.py,
commit 824e1d0, ANTES del partido; no se publicó: sin aprobar). Quentin Grimes: nivel estimado 37.4% (80%: 35.3–39.5%, Beta con prior
de 750 intentos al 36.6% de carrera + temporada ≈ 43/99); esperados 2.8 triples en ~7.6 intentos (80%: 1–5 en 8).
Final: Jazz 109, Lakers 97 (CBS Sports box score; AP vía FinChannel). Grimes 35 min, 20 pts, 8/20 de campo, 4/10 de triples (CBS);
NBC Sports: 20/7/4. Lakers 9/33 de triples (27.3%), Jazz 14/37 (37.8%). George 30 (UTA), Dončić 29 y 9 pérdidas. Fin de la racha de 9 de LAL (13-3);
UTA 3-13. Bajas: Reaves (LAL; talón), Markkanen, Jackson Jr., Nurkić (UTA).
Cálculos (scratch, numpy/scipy): con 10 intentos, esperados 3.74, 80% 2–6, P(=4) = 0.246. «Mano caliente» al 75%: P(≤4 de 10) = 0.0197 (≈1 en 51);
razón de verosimilitud modelo/mano caliente = 15. Temporada ahora 47/109 = 43.1%, p = 0.16 vs carrera. Nivel actualizado: 37.4% (35.3–39.5%).
Brier no aplica: ayer no fijamos probabilidad de ganador."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1119")
K = "Resumen · NBA · Miércoles 18 de noviembre"
METHOD = ("Método: nivel real de tiro = promedio Beta entre su carrera (36.6%, con peso de 750 intentos, supuesto) y su temporada. "
          "Rango 10–90% por simulación (400,000 escenarios). «Mano caliente» = suponer que sigue tirando 75%, como en sus 2 partidos previos; "
          "prueba binomial. Estimación fijada antes del partido. Datos: CBS Sports, NBC Sports, AP. "
          "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 4
    return [
        slide(1, T, K, "Grimes volvió a su nivel: 4 de 10 triples. Le estimábamos 37%; tiró 40%",
              [HBars([("2 previos", 75.0, GHOST), ("Ayer", 40.0, ACC), ("Estimado", 37.4, AMBER)], 100, "{}%", 300),
               Stats([("4", "triples; nuestro rango para 10 intentos: 2 a 6", ACC),
                      ("1 en 51", "veces pasa algo así si su mano siguiera «caliente»", AMBER),
                      ("97-109", "los Lakers cayeron ante Utah y cortaron racha de 9", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Esta vez el número aguantó: la racha no era su nuevo nivel.",
              style="cover", title_size=58),
        slide(2, T, "Lo que probamos · Una prueba nueva para una racha", "La «mano caliente» no pasó la prueba; su nivel de siempre, sí",
              [Tests([(False, "Grimes ya es un tirador de 75%",
                       "Si lo fuera, 4 de 10 o menos pasaría 2 de cada 100 noches. Ayer pasó.",
                       "Binomial · P(≤4 de 10 | 75%) = 0.020"),
                      (True, "Su nivel real ronda 37%",
                       "Con 10 intentos esperábamos 3.7 triples (rango 2–6). Metió 4.",
                       "P(exactamente 4) = 0.25 · nuestro modelo explica 15 veces mejor el resultado"),
                      (False, "Su temporada ya demuestra que mejoró",
                       "Va 47 de 109 (43%). Con esa muestra, aún podría ser su 37% de carrera con buena suerte.",
                       "Binomial · p = 0.16 vs. 36.6% de carrera · n = 109")])],
              title_size=58),
        slide(3, T, "El partido · Los Ángeles · Final", "Utah cortó la racha de 9 de los Lakers desde la línea de 3",
              [Matchup("Jazz", "109 · ahora 3-13", "Lakers", "97 · ahora 13-3", sep="ganaron en casa de · marcador · récord"),
               Table(("Jazz", "Lakers"),
                     [("Triples", "14 de 37", "9 de 33"),
                      ("% de triples", "37.8%", "27.3%"),
                      ("Puntos de su líder", "30", "29"),
                      ("Bajas clave", "3", "1")], colors=[GHOST, ACC]),
               ],
              takeaway="Utah jugó sin Markkanen, Jackson Jr. ni Nurkić; LA, sin Reaves. Dončić (29 y 9 balones perdidos) cortó su racha de 11 juegos con 30+.",
              title_size=56),
        slide(4, T, "Lo que aprendimos", "Tras una racha, el promedio pesa más que la emoción",
              [Bullets(["Grimes: 4 de 10 triples; esperábamos 37% y tiró 40%.",
                        "La «mano caliente» de 75% no pasó la prueba (p = 0.02).",
                        "Su nivel estimado sigue en 37% (35–40%).",
                        "Ayer no fijamos ganador: sin error de la noche (Brier)."])],
              takeaway="¿Grimes es un tirador de 37% o de 43%? Su temporada aún no lo dice. ¿Tú qué crees?",
              style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
