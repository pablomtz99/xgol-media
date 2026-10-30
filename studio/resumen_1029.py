"""xGol — Resumen del jueves 29 oct (diseño v7)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res1029")


def R():
    T = 6
    return [
        slide(1, T, "Resumen · jueves 29 de octubre", "Así nos fue ayer",
              [Hero("1 de 2", "ganadores acertados entre lo que publicamos: Packers sí, Portland no.", ACC),
               Stats([("27-19", "Packers a Panthers", ACC), ("124-103", "Memphis en Portland", NEG), ("227", "puntos en Portland (dijimos 231)", GHOST)])],
              takeaway="Lo que acertamos, lo que no y por qué. Lo publicamos siempre, también cuando fallamos.", style="cover"),
        slide(2, T, "Lo que acertamos · NFL", "Green Bay ganó… y no pudo correr, como dijimos",
              [Table(("Dijimos", "Resultado"), [("Packers ganan en casa", "56%", "27-19")], colors=[GHOST, ACC]),
               Stats([("1.9", "yardas por acarreo de Green Bay (48 en 25)", ACC), ("30/41", "pases completos de Jordan Love, 288 yardas", GHOST), ("3", "pases de anotación de Love", GHOST), ("6", "capturas a Bryce Young", GHOST)])],
              takeaway="El partido se decidió por aire: Green Bay sigue siendo el peor equipo por tierra y ganó igual con Love."),
        slide(3, T, "Lo que no · NBA", "Memphis llegó invicto sin Morant y se fue 5-0",
              [Table(("Dijimos", "Resultado"), [("Portland gana en casa", "67%", "103-124")], colors=[GHOST, NEG]),
               Stats([("18", "puntos de Cam Boozer, en triple-doble (19 años)", GHOST), ("8", "jugadores de Memphis con 10+ puntos", GHOST), ("14", "puntos de Morant ante su exequipo", GHOST), ("33-20", "4° cuarto para Memphis", GHOST)])],
              takeaway="Morant salió al inicio del último cuarto con molestia en el muslo (isquiotibial); Portland iba abajo por 8 y perdió ese cuarto por 13."),
        slide(4, T, "¿Qué tan lejos estuvimos?", "2 de 3 cayeron dentro de nuestro rango",
              [Tests([(True, "Green Bay ganó por 8", "Esperábamos Green Bay por 2. Rango del 80%: Carolina por 15 a Green Bay por 19.", "Modelo NFL v0 · margen ~ Normal(+2.0, 13.5)"),
                      (False, "Memphis ganó por 21", "Esperábamos Portland por 6. Rango: Memphis por 13 a Portland por 25. Pasa 3 de cada 100.", "Modelo NBA v1 · P(Memphis por 21 o más) = 0.03 · σ = 14.7"),
                      (True, "227 puntos en Portland", "Proyectamos 231: el ritmo lento sí se dio.", "error absoluto = 4 puntos")])],
              takeaway="Un rango del 80% falla 1 de cada 5 veces. Memphis fue de las grandes sorpresas."),
        slide(5, T, "Calibración", "Dos partidos: muestra muy chica para juzgar",
              [Stats([("0.321", "error de la noche (Brier: menos es mejor)", NEG), ("0.250", "lo que da decir 50/50 siempre", GHOST), ("0.205", "nuestro error en 1,090 partidos de prueba NBA 2025-26", ACC)]),
               Tests([(True, "¿1 acierto de 2 es mala señal?", "Esperábamos 1.2 aciertos. Sacar 1 o menos pasa 62 de cada 100 noches.", "Poisson-binomial · P(≤1 | p = 0.56, 0.67) = 0.62 · n = 2"),
                      (True, "¿Y lo acumulado (28 y 29 oct)?", "3 de 6 contra 3.8 esperados. Pasa 39 de cada 100 veces: dentro de lo normal.", "P(≤3 | n = 6) = 0.39 · Brier acumulado 0.297 · n = 6")])],
              takeaway="Con 6 partidos, el error se mueve mucho por un solo resultado. Lo medimos en el acumulado, en público."),
        slide(6, T, "Lo que aprendimos", "Memphis obliga a actualizar: el modelo aprende con cada partido",
              [Bullets(["Ganadores: 1 de 2. Rangos: 2 de 3 dentro. Error de la noche: 0.321.", "Acertamos cómo sería el Packers-Panthers: Green Bay no corrió y ganó por aire.", "Memphis ya va 5-0 sin Morant: cada victoria sube su nivel en el modelo.", "Pendiente: ajustar por lesiones (Morant, a revisión)."])],
              takeaway="¿Memphis es de verdad o es el calendario? Te leemos.", style="end",
              method="Método: probabilidades publicadas antes de cada partido (modelo NFL v0 y modelo NBA v1); rango del 80% del margen final. Brier = promedio de (probabilidad − resultado)². Resultados oficiales del 29 oct (Packers.com, ESPN). Datos: nflverse (CC-BY 4.0), BALLDONTLIE. Análisis independiente, no afiliado a ninguna liga. No es recomendación de apuesta."),
    ]


if __name__ == "__main__":
    o = f"{OUT}/R"; os.makedirs(o, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{o}/{i:02d}.png")
    print("ok")
