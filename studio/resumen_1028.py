"""xGol — Resumen del miércoles 28 oct (diseño v7)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/res")


def R():
    T = 5
    return [
        slide(1, T, "Resumen · miércoles 28 de octubre", "Así nos fue ayer",
              [Hero("2 de 4", "ganadores acertados entre lo que publicamos de NBA y la Serie Mundial.", ACC),
               Stats([("3", "partidos NBA", GHOST), ("1", "Serie Mundial", GHOST), ("1°", "título de los Brewers", ACC)])],
              takeaway="Lo que acertamos, lo que no y por qué. Lo publicamos siempre.", style="cover"),
        slide(2, T, "Lo que acertamos", "Spurs y Brewers, como se esperaba",
              [Table(("Dijimos", "Resultado"), [("Spurs en Utah", "73%", "117-111"), ("Brewers, Juego 5", "54%", "4-1")], colors=[GHOST, ACC])],
              takeaway="Los Brewers cerraron la Serie Mundial en 5, uno de los finales más probables que habíamos calculado."),
        slide(3, T, "Lo que no", "Dos sorpresas con nombre y apellido: las bajas",
              [Table(("Dijimos", "Resultado"), [("Thunder gana en Dallas", "75%", "96-120"), ("Clippers ganan a Lakers", "54%", "103-87")], colors=[GHOST, NEG])],
              takeaway="Oklahoma jugó sin Holmgren, Caruso, Jalen Williams ni Wallace. Y los Lakers ganaron por 16 aun sin Dončić. Las lesiones pesaron más de lo que el modelo puede ver."),
        slide(4, T, "¿Qué tan lejos estuvimos?", "2 de 3 resultados cayeron dentro del rango que dimos",
              [Tests([(True, "Spurs ganaron por 6", "Nuestro rango: de Utah por 28 a Spurs por 10.", "dentro"),
                      (False, "Dallas ganó por 24", "Fuera del rango que dimos.", "fuera"),
                      (True, "Lakers ganaron por 16", "Nuestro rango: de Clippers por 20 a Lakers por 17.", "dentro")])],
              takeaway="Es lo esperado: un rango del 80% debe fallar 1 de cada 5 veces. Una noche no dice mucho; lo que cuenta es el acumulado."),
        slide(5, T, "Lo que aprendimos", "Las bajas importan: ya trabajamos en meterlas al modelo",
              [Bullets(["Ganadores: 2 de 4. Rangos: 2 de 3 dentro.", "Las dos fallas tuvieron lesiones importantes de por medio.", "Seguimos midiendo todo, en público, todos los días."])],
              takeaway="Hoy: Panthers-Packers, Fiorentina-Atalanta y tres de NBA. ¿Cuál quieres que revisemos mañana?", style="end",
              method="Método: probabilidades publicadas antes de cada partido (modelo NBA v1 y modelo de la Serie Mundial); rango del 80% del margen final. Resultados oficiales del 28 oct. Análisis independiente. No es recomendación de apuesta."),
    ]


if __name__ == "__main__":
    o = f"{OUT}/R"; os.makedirs(o, exist_ok=True)
    for i, im in enumerate(R(), 1):
        im.save(f"{o}/{i:02d}.png")
    print("ok")
