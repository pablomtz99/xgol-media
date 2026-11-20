"""xGol — Resumen del jueves 19 nov: las probabilidades que fijamos en las portadas del 19 nov (studio/portadas_1119.py, commit 3200c5c,
ANTES de los partidos; no se publicaron: sin aprobar).
1) IND@HOU (NFL v0, sem. 1–10): HOU 70.4% (59.7–79.3%), margen +7.2. Final: HOU 26-3 (nflverse games.csv; AP vía CBS Sports; Yahoo, ESPN).
   AP/CBS: Stroud 194 yd, 3 TD, 1 int (3er partido seguido con 3+ TD); Montgomery 26-107; IND 167 yd totales y 38 por tierra (mínimos del año),
   Jones 12/27 144 yd 1 int; safety de Will Anderson Jr. (líder NFL con 11.5 capturas); primera victoria de HOU en casa (0-4 antes). HOU 4-6, IND 3-8.
   Bajas IND: Gardner y Ward (CB titulares). Error de margen: +23 − 7.2 = 15.8 = 1.17σ (σ 13.5); rango 80% del margen: −10 a +24.5 → dentro.
2) POR@MIL (NBA v1 SRS): MIL 25.9% (16.5–37.5%), margen −9.5. Final: POR 124-114 (AP vía ESPN; WTMJ/AP: 12 derrotas seguidas).
   Lillard 33 (máximo de la temporada) en su regreso a Milwaukee; Henderson 27, Holiday 22, Camara 18; Herro 19, Ament 18 y 9 reb., Jakučionis 18.
   MIL 1-15 (peor arranque en 16 juegos de su historia; racha récord: 15 en 1996). POR 10-5. Sin Kuzma ni Turner (MIL), sin Avdija ni Morant (POR).
   MIL jugaba segunda noche seguida (perdió en Miami el 18); el modelo no ajusta descanso. Error de margen: 0.5 pts = 0.03σ.
Noche: 2 de 2; esperados 0.704 + 0.741 = 1.45; P(ambos) = 0.522. Brier = (0.296² + 0.259²)/2 = 0.077 (volado 0.25).
Acumulado NFL fuera de muestra (studio/models/nfl_1117.py con semanas 4–11, recalculado hoy con nflverse): 102 partidos, 67 aciertos vs 62.7 esperados;
Brier 0.227 (80%: 0.211–0.243); Spiegelhalter p = 0.78. Franjas: 50–60% 33/51 (dijo 55%, pasó 65%); 60–70% 20/33 (63% → 61%); 70%+ 14/18 (76% → 78%).
(En ese protocolo estricto IND@HOU daba 73.7%; en el resumen usamos el 70.4% publicado en la portada.)
Sin xgol-data (add_repo no disponible): no se actualiza el acumulado NBA."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
from resumen_1105 import Results

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1120")
K = "Resumen · NFL y NBA · Jueves 19 de noviembre"
METHOD = ("Método: NFL v0 = 0.5 × (puntos que suma por jugada el local − el visitante, restando lo que permite su defensa) × 61.6 jugadas "
          "+ 1.5 de localía; probabilidad = Φ(margen/13.5). NBA v1 = margen ajustado por rival (SRS) mezclado con 90% del nivel 2025-26 "
          "(peso 16 partidos) + 2 de localía; Φ(margen/14.7). Probabilidades fijadas antes de los partidos. Brier = error promedio, menos es mejor "
          "(volado: 0.25). Calibración: prueba de Spiegelhalter. Datos: nflverse, Basketball-Reference. Resultados: AP, ESPN, CBS Sports. "
          "Análisis independiente, no afiliado a la NFL, la NBA ni a los equipos. No es recomendación de apuesta.")


def R():
    T = 5
    return [
        slide(1, T, K, "Jueves: 2 de 2. Houston aplastó 26-3 y Milwaukee sumó su 12ª derrota seguida",
              [Results([(True, "Texans 26 · Colts 3", "Houston 70%"),
                        (True, "Trail Blazers 124 · Bucks 114", "Portland 74%")]),
               Stats([("2 de 2", "aciertos; esperábamos 1.45", ACC),
                      ("0.077", "error de la noche (Brier); volado = 0.25", ACC),
                      ("52%", "probabilidad de acertar ambos", GHOST)])],
              takeaway="Lo publicamos ganemos o perdamos. Ayer los dos números aguantaron; uno, casi al punto exacto.",
              style="cover", title_size=58),
        slide(2, T, "NFL · Semana 11 · Houston · Final", "Houston ganó por 23; esperábamos 7. La defensa dejó a Indianapolis en 167 yardas",
              [Matchup("Texans", "26 · ahora 4-6", "Colts", "3 · ahora 3-8", sep="ganaron en casa a · marcador · récord"),
               Table(("Estimado", "Real"),
                     [("Ventaja de Houston", "+7.2", "+23"),
                      ("Probabilidad / resultado", "70%", "Ganó"),
                      ("Yardas de Indianapolis", "—", "167"),
                      ("Yardas por tierra de Indy", "—", "38"),
                      ("Pases de TD de Stroud", "—", "3")], colors=[GHOST, ACC])],
              takeaway="Su 1-5 en partidos cerrados no se movió: no fue cerrado. Fue su primera victoria en casa del año.",
              title_size=54),
        slide(3, T, "NBA · Milwaukee · Final", "Le dimos 26% a Milwaukee y estimamos que perdía por 9.5. Perdió por 10",
              [Matchup("Blazers", "124 · ahora 10-5", "Bucks", "114 · ahora 1-15", sep="ganaron en casa de · marcador · récord"),
               Table(("Estimado", "Real"),
                     [("Margen de Milwaukee", "−9.5", "−10"),
                      ("Opciones de Milwaukee", "26%", "Perdió"),
                      ("Puntos de Lillard", "—", "33"),
                      ("Racha de derrotas (antes → ahora)", "11", "12")], colors=[GHOST, ACC])],
              takeaway="Lillard, en su regreso a Milwaukee, hizo su máximo del año. La racha récord de los Bucks es de 15 (1996).",
              title_size=56),
        slide(4, T, "Lo que probamos · Calibración", "Cuando decimos 7 de cada 10, pasa más o menos 7 de cada 10",
              [Tests([(True, "Los márgenes caben en nuestros rangos",
                       "Houston +23: dentro del rango de 80% (−10 a +25). Milwaukee: error de medio punto.",
                       "Error en desviaciones: 1.17σ y 0.03σ · σ = 13.5 (NFL), 14.7 (NBA)"),
                      (True, "Nuestro modelo NFL está calibrado",
                       "102 partidos fuera de muestra: 67 aciertos; esperábamos 63. Ningún desvío significativo.",
                       "Spiegelhalter p = 0.78 · Brier 0.227 (80%: 0.211–0.243)")]),
               HBars([("Dijo 55%", 64.7, AMBER), ("Dijo 63%", 60.6, ACC), ("Dijo 76%", 77.8, ACC)], 100, "{}%", 300)],
              takeaway="Barras = % de veces que ganó nuestro favorito, por franja (NFL, 51, 33 y 18 partidos).",
              title_size=56),
        slide(5, T, "Lo que aprendimos", "Un buen número no es el que acierta: es el que mide bien la duda",
              [Bullets(["Ayer: 2 de 2 y error de la noche de 0.077.",
                        "Milwaukee: estimamos −9.5 y perdió por 10.",
                        "Houston ganó por más de lo previsto, pero dentro del rango.",
                        "NFL acumulado: 67 de 102 y calibrado (p = 0.78)."])],
              takeaway="Milwaukee va 1-15. ¿Alcanza la racha récord de 15 derrotas?",
              style="end", method=METHOD),
    ]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{OUT}/{i:02d}.png")
    print("ok", OUT)
