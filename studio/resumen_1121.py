"""xGol — Resumen del viernes 20 nov: los 9 juegos NBA de la portada del 20 nov (studio/portadas_1120.py, idea 1, y HOU@DEN, idea 2; commit 9a28c51,
ANTES de los partidos; no se publicaron: sin aprobar). Probabilidades: studio/models/nba_viernes_1120.py. Cálculo: studio/models/resumen_1121.py.
Resultados (coinciden NBA.com, recap Copa NBA 20 nov, y SI scoreboard): ATL 111-97 CHA; TOR 105-102 DET; ORL 113-111 BKN; CLE 128-119 IND; WAS 98-94 CHI;
OKC 126-120 NOP; PHX 111-101 UTA; LAL 106-104 SAC; DEN 133-124 HOU. Ambas fuentes: Harden 51 (CLE), SGA 40, Davis 36 (WAS), Wagner 35 (ORL), Barnes 29 (TOR).
Récords previos (Basketball-Reference, hasta 19 nov) +1: SAC 1-14, LAL 14-3, DEN 9-5, HOU 12-5, TOR 6-10, DET 10-5, WAS 6-11, CHI 4-11.
No usamos: línea final de Şengün (solo parcial en vivo), línea de Mara (fuentes discrepan), rebotes ofensivos del HOU@DEN (sin box score verificado).
Noche: 6 de 9; esperados 6.24; sorpresas 3 vs 2.76 (80%: 1–5). P(6 exactos) 0.277. Brier 0.183 (esperado si calibrado 0.203, 80%: 0.134–0.283; volado 0.25).
Spiegelhalter (noche) z = −0.34, p = 0.73. Márgenes: 9 de 9 dentro del rango 80% (±18.8). Favoritos ≥70%: 3 de 3 (esp. 2.45); <70%: 3 de 6 (esp. 3.79).
Sin xgol-data (add_repo no disponible): no se actualiza el acumulado NBA (último: 114 de 158, p = 0.15)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1121")
K = "Resumen · NBA · Viernes 20 de noviembre"
METHOD = ("Método: Modelo NBA v1 = margen ajustado por rival (SRS) mezclado con 90% del nivel 2025-26 (peso 16 partidos) + 2 pts de localía; "
          "probabilidad = Φ(margen/14.7); rango 80% del margen = ±18.8. Probabilidades fijadas antes de los partidos. Brier = error promedio, menos es mejor "
          "(volado: 0.25). Calibración: prueba de Spiegelhalter. Datos: Basketball-Reference. Resultados: NBA.com, SI. "
          "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 5
    return [
        slide(1, T, K, "Dijimos 2 o 3 sorpresas en 9 partidos. Hubo 3",
              [Results([(True, "Hawks 111 · Hornets 97", "69%"), (False, "Raptors 105 · Pistons 102", "Detroit 68%"),
                        (True, "Magic 113 · Nets 111", "64%"), (True, "Cavaliers 128 · Pacers 119", "76%"),
                        (False, "Wizards 98 · Bulls 94", "Chicago 64%"), (True, "Thunder 126 · Pelicans 120", "84%"),
                        (True, "Suns 111 · Jazz 101", "60%"), (True, "Lakers 106 · Kings 104", "84%"),
                        (False, "Nuggets 133 · Rockets 124", "Houston 54%")]),
               Stats([("6 de 9", "aciertos; esperábamos 6.2", ACC),
                      ("0.183", "error de la noche (volado: 0.25)", ACC)])],
              takeaway="Lo publicamos ganemos o perdamos. El número que importaba era el de sorpresas: 2.8 estimadas, 3 reales.",
              style="cover", title_size=58),
        slide(2, T, "Las 3 sorpresas", "Las tres cayeron donde dábamos menos de 7 de cada 10",
              [Table(("Le dimos", "Margen real"),
                     [("Detroit (estimado +6.9)", "68%", "−3"),
                      ("Chicago (estimado +5.2)", "64%", "−4"),
                      ("Houston (estimado +1.4)", "54%", "−9")], colors=[AMBER, NEG]),
               Stats([("3 de 6", "ganaron nuestros favoritos por debajo de 70% (esperábamos 3.8)", AMBER),
                      ("−0.7σ", "el mayor de estos errores: dentro de lo normal", GHOST)])],
              takeaway="Toronto ganó sin Leonard ni Barrett; Davis metió 36 para Washington; Denver le hizo 133 a Houston.",
              title_size=56),
        slide(3, T, "Los favoritos claros", "Los 3 favoritos de 75% o más ganaron. Dos se salvaron por poco",
              [Table(("Le dimos", "Margen real"),
                     [("Cleveland (estimado +10.6)", "76%", "+9"),
                      ("Oklahoma City (est. +14.9)", "84%", "+6"),
                      ("Lakers (estimado +14.7)", "84%", "+2")], colors=[GHOST, ACC]),
               Stats([("51", "puntos de Harden para Cleveland, con 7 triples", ACC),
                      ("1-14", "Sacramento: perdió por 2 ante los Lakers (14-3)", AMBER),
                      ("40", "puntos de Gilgeous-Alexander", GHOST)])],
              takeaway="Cleveland quedó a 1.6 puntos de lo estimado. Lakers y Thunder ganaron, pero por menos de lo esperado.",
              title_size=56),
        slide(4, T, "Lo que probamos · Calibración", "La noche cuadra con nuestras probabilidades",
              [Tests([(True, "El número de sorpresas cabe en lo estimado",
                       "Estimamos 2.8 (80%: 1 a 5). Hubo 3. Acertar 6 de 9 era el resultado más probable.",
                       "P(6 aciertos) = 28% · suma de probabilidades = 6.24"),
                      (True, "Los 9 márgenes, dentro de nuestros rangos",
                       "Ningún resultado se salió del rango de 80%. Error medio: 7.7 puntos.",
                       "Mayor error 0.86σ (Lakers) · σ = 14.7"),
                      (True, "Las probabilidades están calibradas esta noche",
                       "El error de la noche (0.183) es menor que el esperado si todo cuadra (0.203).",
                       "Spiegelhalter z = −0.34, p = 0.73 · n = 9: una noche es una pista, no una prueba")]),],
              takeaway="Favoritos de 70% o más: 3 de 3 (esperábamos 2.5). De menos de 70%: 3 de 6 (esperábamos 3.8).",
              title_size=56),
        slide(5, T, "Lo que aprendimos", "Una buena probabilidad también dice cuántas veces vas a fallar",
              [Bullets(["Ayer: 6 de 9; esperábamos 6.2.",
                        "Anticipamos 2 o 3 sorpresas: hubo 3, todas en favoritos de menos de 70%.",
                        "Los 9 márgenes cayeron dentro de nuestros rangos.",
                        "Error de la noche: 0.183 (un volado da 0.25)."])],
              takeaway="Sacramento va 1-14 y casi tumba a los Lakers. ¿Cuándo llega su segunda victoria?",
              style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
