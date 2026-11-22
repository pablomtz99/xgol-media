"""xGol — portadas de las 4 ideas del 22 nov. Diseño v7. Cálculos en studio/models/*_1122.py. SIN xgol-data ni nflverse (acceso no habilitado en esta ejecución)
→ sin NFL (no hay jugadas 2026 para el Modelo NFL v0). Sin MLB (fuera de temporada). Tenis: sin modelo propio validado.
Hull–Brighton (8:00 CDMX) descartado como previa: muy temprano.
1) Chivas–Cruz Azul (J17, hoy 17:07 CDMX, Estadio Akron). Tras Tigres 1-0 América: CHV 45.7 / E 23.8 / CAZ 30.5%; CAZ líder 54.3% (80%: 42–66%); CHV 45.7%; AME 0%.
   Goles esp 1.69–1.34. Sensibilidad localía 0–0.6: CAZ líder 48–62%. Puntos vs goles: CAZ 32 vs 28.7 esperados (P≥ = 0.31), CHV 30 vs 29.6. Sin validación fuera de muestra.
2) POR@PHI (lun 23, 19:00 ET = 18:00 CDMX). NBA v1 SRS (B-Ref hasta 18 nov): PHI 46.7% (34–60%) → POR 53.3% (41–66%); calidad PHI 12°, POR 8°.
   Récords hoy (Fox Sports y StatMuse 22 nov): PHI 14-3, POR 10-6. PHI al 18 nov: 13-3 con MOV +2.94 → victorias esperadas 9.3; P(≥13) = 0.047.
   Jaylen Brown día a día (FanDuel Research, 22 nov). Validación v1: 2025-26 fuera de muestra 69% aciertos, Brier 0.205 (n = 1,090).
3) Thunder doble jornada: dom 22 en MIA (18:00 ET = 17:00 CDMX; SI), lun 23 en IND (19:30 ET; IND juega dom en NYK → ambos en back-to-back, se cancela).
   OKC en MIA 61.6% (49–73%), en IND 76.9% (66–86%); ambas 47.1%; ninguna 9.6%. SRS 5.79 vs nivel previo 7.67: z = −0.5, p = 0.62.
   Bajas OKC (reporte oficial vía HEAVY/Yahoo, 21 nov): Holmgren, Jalen Williams, Wallace, Caruso, Sorber, Topić, Jaylin Williams fuera; Gilgeous-Alexander en duda.
   MIA: Antetokounmpo en duda; 9-6, 6 victorias seguidas; no jugó el sábado. El modelo no ve bajas.
4) Premier: Arsenal 28 pts (11 PJ, 17-7), Brighton 22 (10 PJ, 26-7) (ESPN UK tras Newcastle 2-2 Arsenal). Puntos esperados por goles: ARS 22.4 (80%: 17–27), P(≥28) = 0.10
   (BH: no sobrevive → indicio); BHA 24.9 vs 22. Hull–Brighton hoy 14:00 UK: BHA 55.4% (sens. 47–75%)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1122")
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla: futboltotal, Claro Sports, Record."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference, Fox Sports."
LEGAL_NBA2 = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: Basketball-Reference; bajas: reporte oficial NBA."
LEGAL_EPL = "Análisis independiente, no afiliado a la Premier League ni a los clubes. No es recomendación de apuesta. Tabla: Sky Sports, ESPN."


def covers():
    return {
        "1-ligamx-chivas-cruzazul": slide(1, 6, "Liga MX · Jornada 17 · Hoy 17:07 CDMX · Estadio Akron",
            "Chivas es favorito para ganar. Cruz Azul, para terminar líder",
            [Matchup("Chivas", "30 pts · +11", "Cruz Azul", "32 pts · +11", sep="recibe a · puntos · diferencia de goles"),
             Stats([("46%", "gana Chivas, según el modelo xGol; empate 24%", ACC),
                    ("54%", "Cruz Azul termina 1° (80%: 42–66%): le basta empatar", AMBER),
                    ("0%", "América: perdió con Tigres y ya no alcanza", GHOST)])],
            takeaway="Un solo partido decide el 1°, 2° y 3° lugar. ¿Le alcanza el empate a Cruz Azul?",
            style="cover", method=LEGAL_MX, title_size=58),
        "2-nba-por-phi": slide(1, 6, "NBA · Lunes 23 · 18:00 CDMX · Trail Blazers en 76ers · Filadelfia",
            "Filadelfia va 14-3, pero gana por márgenes de equipo promedio",
            [Matchup("Portland", "10-6 · 8°", "76ers", "14-3 · 12°", sep="visita a · récord · lugar en calidad real (nuestro ranking)"),
             Stats([("53%", "gana Portland en Filadelfia, según nuestro modelo (41–66%)", ACC),
                    ("1 en 21", "ganar 13 de 16 con un margen de +2.9 (p = 0.047)", AMBER),
                    ("9.3", "victorias que le daban sus márgenes en esos 16 juegos", GHOST)])],
            takeaway="Jaylen Brown, día a día. ¿Es Filadelfia de verdad el mejor del Este?",
            style="cover", method=LEGAL_NBA, title_size=58),
        "3-nba-thunder-doble": slide(1, 6, "NBA · Domingo en Miami (17:00 CDMX) y lunes en Indiana (18:30 CDMX)",
            "Oklahoma City gana las dos noches menos de la mitad de las veces",
            [HBars([("Domingo en Miami", 62, ACC), ("Lunes en Indiana", 77, ACC), ("Gana las dos", 47, AMBER)], 100, "{}%", 330),
             Stats([("7", "bajas del Thunder; Gilgeous-Alexander, en duda", NEG),
                    ("p = 0.62", "su caída frente a la temporada pasada aún no es significativa", GHOST),
                    ("6", "victorias seguidas de Miami", AMBER)])],
            takeaway="Barras = probabilidad del Thunder según nuestro modelo, que no ve bajas. ¿Aguanta Oklahoma City la doble jornada?",
            style="cover", method=LEGAL_NBA2, title_size=58),
        "4-premier-arsenal": slide(1, 6, "Premier League · Tras la jornada 11 · La tabla contra los goles",
            "Arsenal saca 6 puntos de ventaja. Sus goles valen 22",
            [Matchup("Arsenal", "28 pts · +10", "Brighton", "22 pts · +19", sep="puntos · diferencia de goles · Brighton con un partido menos"),
             Stats([("22.4", "puntos esperados de Arsenal por sus goles (80%: 17–27)", AMBER),
                    ("1 en 10", "sumar 28 con esos goles (p = 0.10: indicio, no prueba)", GHOST),
                    ("1.9", "goles de diferencia por partido de Brighton; Arsenal, 0.9", ACC)])],
            takeaway="Brighton visita a Hull hoy (le damos 55%). ¿Es real la ventaja de Arsenal o la alcanzan los goles?",
            style="cover", method=LEGAL_EPL, title_size=58),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
