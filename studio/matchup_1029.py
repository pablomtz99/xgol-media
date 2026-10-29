"""xGol — slide de matchup (cómo ataca uno vs. cómo defiende el otro) para F (SAC@NOP) y C (MEM@POR). Inserta antes del slide de predicción."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout_v7 import *
import posts_v7_1029 as P


class Duel(Block):
    """Filas: (métrica, equipo A valor, equipo B valor, nota corta, a_mejor:bool|None)."""
    flex = 2; maxgrow = 1.4
    def __init__(self, ta, tb, rows): self.ta, self.tb, self.rows = ta, tb, rows
    def natural(self, d): return 60 + 118 * len(self.rows)
    def draw(self, d, y, h):
        cA, cB = W - M - 400, W - M - 180
        fh = F("Inter-Bold.otf", 26)
        d.text((cA, y), self.ta, font=fh, fill=GHOST); d.text((cB, y), self.tb, font=fh, fill=ACC)
        rh = (h - 50) / len(self.rows); y += 50
        for lab, a, b, note, amejor in self.rows:
            d.line((M, y, W - M, y), fill=LINE, width=2)
            d.text((M, y + 16), lab, font=F("Inter-SemiBold.otf", 29), fill=TXT)
            d.text((M, y + 56), note, font=F("Inter-Regular.otf", 22), fill=MUTED)
            for cx, v, good in ((cA, a, amejor is True), (cB, b, amejor is False)):
                d.text((cx, y + 18), v, font=F("InterDisplay-Black.otf", 52), fill=ACC if good else TXT)
            y += rh
        d.line((M, y, W - M, y), fill=LINE, width=2)


def F_slide(T):
    return slide(5, T, "El matchup", "Dos defensas que dejan tirar, y Nueva Orleans provoca más faltas",
                 [Duel("SAC", "NOP", [
                     ("Tiro efectivo atacando", "50.0%", "51.5%", "liga: 53.1%", False),
                     ("Tiro efectivo que permite", "57.8%", "56.0%", "más alto = peor defensa", False),
                     ("Rebote defensivo", "74.1%", "75.1%", "rebotes propios que atrapa", None),
                     ("Tiros libres por tiro", ".257", ".325", "qué tanto provoca faltas", False),
                     ("% de tiros que son de 3", "36%", "35%", "liga: 42%", None)])],
                 takeaway="Ninguno defiende el tiro, ninguno tira mucho de 3 y los dos cierran bien su rebote. Ventaja de Nueva Orleans: provoca más faltas. Ojo: son solo 4 partidos por equipo.",
                 tag="DATO 4 DE 5")


def C_slide(T):
    return slide(5, T, "El matchup", "El mejor ataque contra una de las mejores defensas… y una guerra por el rebote",
                 [Duel("MEM", "POR", [
                     ("Tiro efectivo atacando", "53.7%", "60.7%", "Portland: el mejor de la liga", False),
                     ("Tiro efectivo que permite", "50.5%", "51.9%", "más bajo = mejor defensa", True),
                     ("% de tiros que son de 3", "42%", "49%", "Portland vive del triple", None),
                     ("Rebote ofensivo", "32.4%", "30.2%", "segundas oportunidades", True),
                     ("Pérdidas de balón", "14.4%", "11.8%", "más bajo = mejor", False)])],
                 takeaway="Casi la mitad de los tiros de Portland son de 3, contra una defensa que limita el tiro. La carta de Memphis: el rebote ofensivo, porque Portland deja escapar 30 de cada 100. Ojo: 3 y 4 partidos de muestra.",
                 tag="DATO 4 DE 5")


def renum(ims_builder, insert_fn, after_index):
    pass


if __name__ == "__main__":
    OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out/v9")
    for k, fn, ins in (("F", P.F_, F_slide), ("C", P.C, C_slide)):
        T = 8
        # re-render with new total: patch slide() page/total by rebuilding via monkeypatch
        import layout_v7 as L
        orig = L.slide
        calls = []
        def rec(page, total, *a, **kw):
            calls.append((page, a, kw)); return None
        P.slide = rec
        fn()
        P.slide = orig
        ims = []
        for page, a, kw in calls:
            newp = page if page < 5 else page + 1
            if kw.get("tag"):
                kw["tag"] = "DATO 5 DE 5" if kw["tag"] == "DATO 4 DE 4" else kw["tag"].replace("DE 4", "DE 5")
            ims.append((newp, orig(newp, T, *a, **kw)))
            if page == 4:
                ims.append((5, ins(T)))
        o = f"{OUT}/{k}"; os.makedirs(o, exist_ok=True)
        for p, im in sorted(ims, key=lambda x: x[0]):
            im.save(f"{o}/{p:02d}.png")
    print("ok")
