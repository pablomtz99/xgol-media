"""xGol — portadas de las 4 ideas del 27 nov. Diseño v7. Sin xgol-data ni nflverse (GitHub fuera de este repo bloqueado en esta corrida) → sin NFL nuevo.
1) Premier J12 dom 29 10:30 CDMX, Arsenal (1°, 28) vs Man City (3°, 22). Europa v0 (europa_v0_1127.py): ARS 46.7/24.7/28.6 (80% ARS 35–59). ARS 0.64 GC/p (liga 1.38).
   ARS 28 pts vs 22.4 esperados por goles (P(≥28) = 0.10; no sobrevive BH). xG FotMob ARS 17.6 (17 goles), City 21.9 (22). Bajas: Saka, Zubimendi fuera; Raya duda (Sports Mole).
2) Bundesliga J11 dom 29 12:30 CDMX, Dortmund (1°, 7-3-0, +10) vs Leverkusen (5°, +7). Europa v0: BVB 48.5/21.9/29.6 (80% 37–61). Fuerza por goles: BVB 4° (Bayern +20,
   Leipzig +18). P(invicto en 10 | sus goles) = 0.196. Leverkusen jugó jue 26 en Zagreb (3 días) vs BVB mar 24 (5): sens −8% → BVB 51%.
3) Liga MX vuelta dom 29 19:07, Chivas (1°, 33) vs Pachuca (8°, 25), ida 1-2. Liga MX v0 (ligamx_vuelta_dom_1127.py): Chivas avanza 46.8% (80% 36–58); sin Idrissi (supuesto −15%) 51%.
4) NBA sáb 28 19:30 CDMX, 76ers (15-4) en Rockets (14-5). NBA v1 (nba_phi_hou_1127.py): HOU 75% con back-to-back de PHI (80% 65–84). PHI Pitágoras 10.8 de 19; P(≥15) = 0.039."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/ideas1127")
LEGAL_EPL = "Análisis independiente, no afiliado a la Premier League ni a los clubes. No es recomendación de apuesta. Tabla: ESPN, NBC Sports; xG: FotMob; bajas: Sports Mole."
LEGAL_BL = "Análisis independiente, no afiliado a la Bundesliga ni a los clubes. No es recomendación de apuesta. Tabla: Sportschau; resultados: ESPN."
LEGAL_MX = "Análisis independiente, no afiliado a la Liga MX ni a los clubes. No es recomendación de apuesta. Tabla: Récord; horarios: ClaroSports; sanción: ESPN."
LEGAL_NBA = "Análisis independiente, no afiliado a la NBA ni a los equipos. No es recomendación de apuesta. Datos: ESPN, StatMuse, Basketball-Reference."


def covers():
    return {
        "1-epl-arsenal-city": slide(1, 6, "Premier League · Jornada 12 · Domingo 29 · 10:30 CDMX",
            "La mejor defensa de Inglaterra recibe al City: Arsenal gana 47 de cada 100",
            [Matchup("Arsenal", "1° · 28 pts", "Man City", "3° · 22 pts", sep="recibe a · lugar · puntos"),
             Stats([("47%", "gana Arsenal (80%: 35–59%); empate 25%", ACC),
                    ("0.64", "goles recibidos por partido (la liga: 1.38)", AMBER),
                    ("28 vs 22", "puntos de Arsenal vs los que dan sus goles", NEG)])],
            takeaway="Sin Saka ni Zubimendi y con Raya en duda. ¿Aguanta la defensa contra el ataque de 22 goles del City?",
            style="cover", method=LEGAL_EPL, title_size=52),
        "2-bundesliga-dortmund-leverkusen": slide(1, 6, "Bundesliga · Jornada 11 · Domingo 29 · 12:30 CDMX",
            "Dortmund es líder invicto, pero sus goles dicen que es el 4°",
            [Matchup("Dortmund", "1° · 24 pts", "Leverkusen", "5°", sep="recibe a · lugar · puntos (Leverkusen 19)"),
             Stats([("49%", "gana Dortmund (80%: 37–61%)", ACC),
                    ("1 en 5", "equipos con sus goles siguen invictos tras 10", AMBER),
                    ("3 vs 5", "días de descanso: Leverkusen jugó el jueves", NEG)])],
            takeaway="Bayern (+20) y Leipzig (+18) tienen el doble de diferencia de goles que Dortmund (+10). ¿Líder de verdad o de récord?",
            style="cover", method=LEGAL_BL, title_size=54),
        "3-ligamx-chivas-pachuca": slide(1, 6, "Liga MX · Cuartos de final, vuelta · Domingo 29 · 19:07 CDMX",
            "Al superlíder le basta ganar. Lo logra 47 de cada 100 veces",
            [Matchup("Chivas", "1° · 33 pts", "Pachuca", "8° · 25 pts", sep="recibe a · ida 1-2"),
             Stats([("47%", "avanza Chivas (80%: 36–58%)", ACC),
                    ("24%", "empate: Pachuca a semifinales", AMBER),
                    ("51%", "Chivas si pesa la baja de Idrissi (expulsado)", NEG)])],
            takeaway="Chivas fue invicto de visita; sus 2 derrotas fueron en el Akron. ¿Su casa lo salva o lo hunde?",
            style="cover", method=LEGAL_MX, title_size=54),
        "4-nba-phi-hou": slide(1, 6, "NBA · Sábado 28 · 19:30 CDMX · 76ers en Rockets",
            "Los 76ers van 15-4, pero sus puntos dicen 11-8",
            [Matchup("76ers", "15-4", "Rockets", "14-5", sep="visita a · récord"),
             Stats([("75%", "gana Houston (80%: 65–84%)", ACC),
                    ("1 en 26", "que un equipo con su diferencial vaya 15-4", AMBER),
                    ("−2.1", "puntos: Philadelphia juega 2 noches seguidas", NEG)])],
            takeaway="+2.2 puntos por partido alcanzan para 11 victorias, no para 15. Y Embiid está en duda. ¿Se acaba la racha?",
            style="cover", method=LEGAL_NBA, title_size=58),
    }


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, im in covers().items():
        im.save(f"{OUT}/{k}.png")
    print("ok", OUT)
