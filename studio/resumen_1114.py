"""xGol — Resumen del viernes 13 nov: los 3 partidos NBA que analizamos con el modelo NBA v1 (portadas del 13 nov, studio/portadas_1113.py).
Ninguna previa se publicó el 13 nov (portadas sin aprobar). Probabilidades fijadas ANTES del partido (commit b6d8470, 13 nov 15:30 UTC).
NO es jornada completa: xgol-data (modelo) no estuvo disponible en esta corrida, así que no recalculamos los otros 6 partidos ni el acumulado.
Resultados 13 nov (NBA.com "Top moments from Friday's Emirates NBA Cup" + segunda fuente cada uno):
  IND 106-104 NYK (ABC News/AP, CBS New York; Brunson 33, Towns falló el empate al final; Siakam 19, Nesmith 18).
  SAS 123-85 GSW (ABC7/AP, Pounding the Rock; 11 seguidas; Castle 32, récord personal; ventaja máx. 43; sin Curry).
  MIA 133-121 CLE (WSVN, Yahoo; Adebayo y Antetokounmpo 37 cada uno, 2a vez en la historia del Heat; CLE sin Mobley).
Favoritos: NYK 74% (perdió), SAS 68% (ganó), CLE 58% (perdió; MIA 42%). Aciertos 1 de 3 vs 2.00 esperados.
Poisson-binomial: P(3)=0.292, P(2)=0.451, P(1)=0.222, P(0)=0.035 → P(≤1) = 0.257. Brier (0.5476+0.1024+0.3364)/3 = 0.329.
Margen esperado vs final (σ 14.7): SAS +6.8/+38 (desvío +2.12σ, una cola 0.017 ≈ 1 en 60); NYK +9.5/−2 (−0.78σ, 0.22);
MIA −3.0/+12 (+1.02σ, 0.15). Racha SAS: producto de probabilidades previas de los 10 = 0.049; × 0.68 = 0.033 (1 en 30) para 11.
Acumulado (al jueves 12 nov, M.validate): 158 partidos, 114 aciertos vs 104.1 esperados; Brier 0.198; Spiegelhalter p = 0.15."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1114")
K = "Resumen · NBA · Viernes 13 de noviembre"
METHOD = ("Método: nuestro modelo NBA v1 (ataque y defensa ajustados por rival y localía, regresión ridge hacia la temporada pasada; "
          "no ve lesiones). Revisamos los 3 partidos del viernes que analizamos un día antes, con las probabilidades fijadas antes del salto inicial. "
          "Brier = error promedio, menos es mejor (volado: 0.25). Aciertos esperados: Poisson-binomial. Desvío: margen real menos esperado, "
          "en desviaciones típicas (14.7 puntos). Resultados: NBA.com, AP, ESPN. "
          "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 6
    return [
        slide(1, T, K, "Viernes: 1 de 3. Nueva York cayó por 2 y Miami sorprendió a Cleveland",
              [Hero("1 de 3", "favoritos de nuestro modelo ganaron el viernes. Esperábamos 2.", NEG),
               Stats([("0.33", "error de la noche (Brier). Un volado: 0.25", NEG),
                      ("1 de 4", "noches como esta terminan con 1 acierto o menos", AMBER),
                      ("+38", "San Antonio sobre Golden State: esperábamos +7", ACC)])],
              takeaway="Lo publicamos ganemos o perdamos. Fue una mala noche, de las que pasan 1 de cada 4 veces con estas probabilidades.",
              style="cover", title_size=64),
        slide(2, T, "Los 3 partidos", "Un acierto amplio y dos derrotas del favorito, una por solo 2 puntos",
              [Results([(False, "Knicks 104-106 Pacers", "Nueva York 74%"),
                        (True, "Warriors 85-123 Spurs", "San Antonio 68%"),
                        (False, "Cavaliers 121-133 Heat", "Cleveland 58%")]),
               Stats([("2", "puntos: Towns falló el tiro del empate al final", NEG),
                      ("37 y 37", "Adebayo y Antetokounmpo: 2a vez en la historia del Heat", AMBER),
                      ("11", "victorias seguidas de San Antonio", ACC)])],
              takeaway=None, title_size=60),
        slide(3, T, "Margen esperado vs. final", "San Antonio se pasó por 31 puntos; Miami, por 15",
              [Table(("Esperado", "Final"),
                     [("Spurs vs. Golden State", "+6.8", "+38"),
                      ("Knicks en Indiana", "+9.5", "−2"),
                      ("Heat vs. Cleveland", "−3.0", "+12")], colors=[GHOST, ACC]),
               Stats([("1 en 60", "partidos se desvía tanto como San Antonio", AMBER),
                      ("1 en 4.6", "partidos falla así un favorito como Nueva York", GHOST),
                      ("1 en 6.5", "partidos gana Miami por 12+ en este duelo", GHOST)])],
              takeaway="Golden State jugó sin Curry y nuestro modelo no ve lesiones: ahí está buena parte de los 31 puntos de diferencia.",
              title_size=60),
        slide(4, T, "¿Noche normal? · Probabilidad compuesta", "Con estas 3 probabilidades, 1 acierto o menos sale 1 de cada 4 noches",
              [HBars([("3 de 3", 29.2, GHOST), ("2 de 3", 45.1, GHOST), ("1 de 3", 22.2, NEG), ("0 de 3", 3.5, GHOST)], 50, "{}%", 230),
               Tests([(None, "Mala noche, pero dentro de lo posible",
                       "Lo más probable eran 2 aciertos. Uno o menos pasa en 26 de cada 100 noches como esta.",
                       "Poisson-binomial · P(≤1) = 0.26 · aciertos esperados 2.0 · n = 3")])],
              takeaway="Con 3 partidos, una noche dice poco. Por eso medimos el acumulado: 158 partidos al jueves, en el siguiente slide.",
              title_size=62),
        slide(5, T, "Calibración · NBA · 158 partidos fuera de muestra (al jueves)", "El acumulado sigue calibrado: 114 aciertos contra 104 esperados",
              [Stats([("114 de 158", "aciertos acumulados al jueves 12", ACC),
                      ("0.198", "error acumulado (Brier). Un volado: 0.25", ACC),
                      ("p = 0.15", "prueba de calibración: sin desvío significativo", GHOST)]),
               Tests([(True, "Las probabilidades siguen bien calibradas", "Cuando decimos 70%, el favorito gana cerca de 7 de cada 10 veces.",
                       "Spiegelhalter z = −1.45, p = 0.15 · Brier 0.198 (80%: 0.183–0.213)"),
                      (True, "San Antonio: 11 seguidas cuando salía 1 de cada 30", "Sumando sus probabilidades previas, esperábamos unas 8 victorias de 11.",
                       "Producto de 11 probabilidades previas = 0.033")])],
              takeaway=None, title_size=62),
        slide(6, T, "Lo que aprendimos", "Una mala noche, contada con la misma vara que las buenas",
              [Bullets(["1 de 3 favoritos ganó; esperábamos 2.",
                        "Error de la noche: 0.33 (un volado: 0.25).",
                        "Nueva York perdió por 2; Miami ganó con 37 y 37.",
                        "Acumulado NBA al jueves: 114 de 158, calibrado (p = 0.15)."])],
              takeaway="San Antonio ya suma 11 seguidas y no ha perdido en la Copa. ¿Hasta dónde llega la racha? Te leemos.", style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
