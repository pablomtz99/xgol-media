"""xGol — motor de layout v7: cada slide se describe con bloques y el motor reparte TODO el espacio.
Bloques flexibles (gráficas, números grandes, tarjetas) crecen para llenar el lienzo; la idea clave va en un panel anclado abajo."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from render_car_gb import font as F, wrap, BG, TXT, ACC, NEG, W, H

MUTED = "#B3BDC9"; LINE = "#3B4757"; SURF = "#1A2330"; GHOST = "#D5DCE4"; AMBER = "#FFC24B"; TECH = "#8C98A8"
M = 72
TOP_LIMIT = 1215          # fin del área de contenido (encima del footer)


def tw(d, t, f):
    return d.textlength(t, font=f)


def para(d, x, y, text, f, fill, maxw, lh):
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill); y += lh
    return y


def para_h(d, text, f, maxw, lh):
    return len(wrap(d, text, f, maxw)) * lh


# ------------------------------------------------------------------ bloques
class Block:
    flex = 0          # peso para repartir el espacio sobrante
    maxgrow = 3.0     # crecimiento máximo respecto a su altura natural

    def natural(self, d): ...
    def draw(self, d, y, h): ...


class Chips(Block):
    def __init__(self, items): self.items = items
    def _f(self): return F("Inter-SemiBold.otf", 30)
    def natural(self, d):
        f = self._f(); return sum(26 + 42 * len(wrap(d, c, f, W - 2 * M - 52)) + 14 for c in self.items)
    def draw(self, d, y, h):
        f = self._f()
        for c in self.items:
            lines = wrap(d, c, f, W - 2 * M - 52)
            hh = 26 + 42 * len(lines)
            w = max(tw(d, l, f) for l in lines)
            d.rounded_rectangle((M, y, M + w + 52, y + hh), radius=hh // 2 if len(lines) == 1 else 26, fill=SURF)
            yy = y + 13
            for l in lines:
                d.text((M + 26, yy), l, font=f, fill=TXT); yy += 42
            y += hh + 14


class Hero(Block):
    """Número gigante + etiqueta. Crece hasta llenar el ancho y centra en su espacio."""
    flex = 2
    def __init__(self, value, label, col=ACC, maxsize=330): self.v, self.l, self.c, self.maxsize = value, label, col, maxsize
    def _size(self, d, hmax=None):
        s = self.maxsize
        while s > 90 and tw(d, self.v, F("InterDisplay-Black.otf", s)) > W - 2 * M:
            s -= 6
        if hmax:
            s = min(s, int(hmax))
        return s
    def natural(self, d):
        s = min(self._size(d), 220)
        return int(s * 0.95) + para_h(d, self.l, F("Inter-Medium.otf", 34), W - 2 * M, 46) + 24
    def draw(self, d, y, h):
        lab_h = para_h(d, self.l, F("Inter-Medium.otf", 34), W - 2 * M, 46)
        s = self._size(d, (h - lab_h - 24) / 0.95)
        block = int(s * 0.95) + 24 + lab_h
        y0 = y + max(0, (h - block) // 2)
        f = F("InterDisplay-Black.otf", s)
        d.text((M - int(s * 0.04), y0 - int(s * 0.17)), self.v, font=f, fill=self.c)
        para(d, M, y0 + int(s * 0.95) + 24 - int(s * 0.17) + 10, self.l, F("Inter-Medium.otf", 34), MUTED, W - 2 * M, 46)


class Stats(Block):
    """Fila de 2–3 cifras grandes en tarjetas que llenan el ancho."""
    flex = 1; maxgrow = 1.8
    def __init__(self, cells): self.cells = cells
    def natural(self, d): return 250
    def draw(self, d, y, h):
        n = len(self.cells); gap = 18
        cw = (W - 2 * M - gap * (n - 1)) / n
        for k, (v, l, col) in enumerate(self.cells):
            x = M + k * (cw + gap)
            d.rounded_rectangle((x, y, x + cw, y + h), radius=22, fill=SURF)
            s = 96
            while s > 40 and tw(d, v, F("InterDisplay-Black.otf", s)) > cw - 48:
                s -= 4
            d.text((x + 24, y + 22), v, font=F("InterDisplay-Black.otf", s), fill=col)
            para(d, x + 24, y + 30 + s, l, F("Inter-Medium.otf", 26), MUTED, cw - 48, 33)


class VBars(Block):
    """Barras verticales grandes; items = (etiqueta, real, esperado|None)."""
    flex = 3; maxgrow = 2.2
    def __init__(self, items, vmax, legend=False): self.items, self.vmax, self.legend = items, vmax, legend
    def natural(self, d): return 330 + (60 if self.legend else 0)
    def draw(self, d, y, h):
        if self.legend:
            d.rounded_rectangle((M, y + 6, M + 30, y + 36), radius=5, fill=ACC)
            d.text((M + 42, y + 2), "real", font=F("Inter-Bold.otf", 28), fill=ACC)
            d.rounded_rectangle((M + 150, y + 6, M + 180, y + 36), radius=5, outline=GHOST, width=3)
            d.text((M + 192, y + 2), "lo que esperaba el mercado", font=F("Inter-Bold.otf", 28), fill=GHOST)
            y += 60; h -= 60
        n = len(self.items)
        bw = (W - 2 * M) / n
        base_y = y + h - 46
        ch = h - 46 - 50
        for i, (lab, real, exp) in enumerate(self.items):
            cx = M + bw * i + bw / 2
            half = min(70, bw * 0.36)
            if exp is not None:
                te = base_y - ch * exp / self.vmax
                d.rounded_rectangle((cx - half, te, cx + half, base_y), radius=12, outline=GHOST, width=4)
                t = f"{exp:g}"; ft = F("Inter-Bold.otf", 26)
                d.text((cx - tw(d, t, ft) / 2, te - 38), t, font=ft, fill=GHOST)
            tr = base_y - ch * real / self.vmax
            col = (ACC if (exp is None or real < exp) else NEG)
            inner = half - (14 if exp is not None else 0)
            d.rounded_rectangle((cx - inner, tr, cx + inner, base_y), radius=10, fill=col)
            t = f"{real:g}"; ft = F("InterDisplay-Black.otf", 46 if bw > 200 else 38)
            inside = exp is not None
            d.text((cx - tw(d, t, ft) / 2, tr + 12 if inside else tr - 56), t, font=ft, fill=BG if inside else TXT)
            fl = F("Inter-SemiBold.otf", 25)
            d.text((cx - tw(d, lab, fl) / 2, base_y + 12), lab, font=fl, fill=MUTED)


class HBars(Block):
    flex = 1; maxgrow = 1.8
    def __init__(self, rows, vmax, fmt="{}", labw=300): self.rows, self.vmax, self.fmt, self.labw = rows, vmax, fmt, labw
    def natural(self, d): return 92 * len(self.rows)
    def draw(self, d, y, h):
        rh = h / len(self.rows); bh = min(84, rh * 0.62)
        bw = W - 2 * M - self.labw - 150
        for i, (lab, v, col) in enumerate(self.rows):
            yy = y + i * rh + (rh - bh) / 2
            d.text((M, yy + bh / 2 - 20), lab, font=F("InterDisplay-Bold.otf", 34), fill=TXT)
            w = max(10, int(bw * abs(v) / self.vmax))
            d.rounded_rectangle((M + self.labw, yy, M + self.labw + w, yy + bh), radius=14, fill=col)
            d.text((M + self.labw + w + 18, yy + bh / 2 - 28), self.fmt.format(v), font=F("InterDisplay-Black.otf", 50), fill=TXT)


class Table(Block):
    flex = 1; maxgrow = 1.6
    def __init__(self, head, rows, colors=None): self.head, self.rows, self.colors = head, rows, colors or [MUTED, ACC]
    def natural(self, d): return 60 + 100 * len(self.rows)
    def draw(self, d, y, h):
        cols = [W - M - 520, W - M - 250]
        fh = F("Inter-SemiBold.otf", 26)
        for cx, t in zip(cols, self.head):
            d.text((cx, y), t, font=fh, fill=GHOST)
        rh = (h - 60) / len(self.rows)
        y += 60
        for lab, *vals in self.rows:
            d.line((M, y, W - M, y), fill=LINE, width=2)
            para(d, M, y + rh / 2 - 20, lab, F("Inter-SemiBold.otf", 30), TXT, cols[0] - M - 30, 36)
            for cx, v, col in zip(cols, vals, self.colors):
                d.text((cx, y + rh / 2 - 34), v, font=F("InterDisplay-Black.otf", 60), fill=col)
            y += rh
        d.line((M, y, W - M, y), fill=LINE, width=2)


class MvM(Block):
    flex = 1; maxgrow = 1.7
    def __init__(self, label, model, market, lk="El mercado de predicción"): self.label, self.model, self.market, self.lk = label, model, market, lk
    def natural(self, d): return 300
    def draw(self, d, y, h):
        bh = min(110, (h - 120) / 2)
        for k, (lab, v, col) in enumerate((("Nuestro modelo", self.model, ACC), (self.lk, self.market, GHOST))):
            yy = y + k * (h / 2)
            d.text((M, yy), lab, font=F("Inter-SemiBold.otf", 30), fill=MUTED)
            d.rounded_rectangle((M, yy + 48, W - M, yy + 48 + bh), radius=18, fill=SURF)
            d.rounded_rectangle((M, yy + 48, M + int((W - 2 * M) * v), yy + 48 + bh), radius=18, fill=col)
            t = f"{self.label}: {round(v*100)}%"; ft = F("InterDisplay-Black.otf", 54)
            bw = int((W - 2 * M) * v)
            if tw(d, t, ft) + 56 <= bw:
                d.text((M + 28, yy + 48 + bh / 2 - 32), t, font=ft, fill=BG)
            else:
                pct = f"{round(v*100)}%"
                d.text((M + 28, yy + 48 + bh / 2 - 32), pct, font=ft, fill=BG)
                lt = F("InterDisplay-Bold.otf", 38)
                if M + bw + 24 + tw(d, self.label, lt) <= W - M - 16:
                    d.text((M + bw + 24, yy + 48 + bh / 2 - 22), self.label, font=lt, fill=TXT)
                else:
                    d.text((M + tw(d, lab, F("Inter-SemiBold.otf", 30)) + 16, yy), "· " + self.label, font=F("Inter-SemiBold.otf", 30), fill=TXT)


class Rank(Block):
    flex = 1; maxgrow = 1.8
    def __init__(self, rows): self.rows = rows
    def natural(self, d): return 130 * len(self.rows) + 60
    def draw(self, d, y, h):
        x0, x1 = M, W - M
        sx = lambda r: x0 + 40 + (x1 - x0 - 80) * (r - 1) / 29
        rh = (h - 60) / len(self.rows)
        for i, (lab, r, col) in enumerate(self.rows):
            yy = y + i * rh
            d.text((M, yy), lab, font=F("InterDisplay-Bold.otf", 36), fill=TXT)
            ly = yy + 80
            d.rounded_rectangle((x0, ly - 10, x1, ly + 10), radius=10, fill=LINE)
            d.ellipse((sx(r) - 40, ly - 40, sx(r) + 40, ly + 40), fill=col)
            t = f"{r}°"; ft = F("InterDisplay-Black.otf", 34)
            d.text((sx(r) - tw(d, t, ft) / 2, ly - 22), t, font=ft, fill=BG)
        fl = F("Inter-Medium.otf", 24)
        ly = y + h - 28
        d.text((x0, ly), "1° = mejor", font=fl, fill=MUTED)
        t = "30° = peor"; d.text((x1 - tw(d, t, fl), ly), t, font=fl, fill=MUTED)


class Stacked(Block):
    flex = 1; maxgrow = 1.8
    def __init__(self, title, vals, labels, cols): self.t, self.vals, self.labels, self.cols = title, vals, labels, cols
    def natural(self, d): return 200
    def draw(self, d, y, h):
        d.text((M, y), self.t, font=F("Inter-SemiBold.otf", 28), fill=MUTED)
        y += 46; bh = h - 46
        x = M; bw = W - 2 * M
        for v, l, c in zip(self.vals, self.labels, self.cols):
            w = int(bw * v)
            d.rectangle((x, y, x + w - 8, y + bh), fill=c)
            d.text((x + 20, y + 14), f"{round(v*100)}%", font=F("InterDisplay-Black.otf", 64 if bh > 160 else 48), fill=BG)
            d.text((x + 20, y + bh - 44), l, font=F("Inter-Bold.otf", 28), fill=BG)
            x += w


class Tests(Block):
    """Tarjetas de hipótesis ✓ / ✗."""
    flex = 2; maxgrow = 1.6
    def __init__(self, items): self.items = items
    def _card_h(self, d, it):
        ok, claim, res, tech = it
        return 36 + para_h(d, claim, F("InterDisplay-Bold.otf", 34), W - 2 * M - 130, 41) + 8 + para_h(d, res, F("Inter-Medium.otf", 27), W - 2 * M - 130, 35) + 34 + 26
    def natural(self, d): return sum(self._card_h(d, it) + 16 for it in self.items)
    def draw(self, d, y, h):
        nat = [self._card_h(d, it) for it in self.items]
        extra = max(0, (h - sum(nat) - 16 * len(nat)) / len(nat))
        for it, hh in zip(self.items, nat):
            ok, claim, res, tech = it
            hh += extra
            col = ACC if ok else NEG
            d.rounded_rectangle((M, y, W - M, y + hh), radius=20, fill=SURF)
            d.rounded_rectangle((M, y, M + 10, y + hh), radius=5, fill=col)
            cy = y + 36 + 28
            d.ellipse((M + 34, cy - 30, M + 94, cy + 30), fill=col)
            if ok:
                d.line((M + 49, cy, M + 60, cy + 13), fill=BG, width=7); d.line((M + 60, cy + 13, M + 80, cy - 13), fill=BG, width=7)
            else:
                d.line((M + 52, cy - 12, M + 76, cy + 12), fill=BG, width=7); d.line((M + 76, cy - 12, M + 52, cy + 12), fill=BG, width=7)
            ty = y + 30 + (extra / 2)
            ty = para(d, M + 120, ty, claim, F("InterDisplay-Bold.otf", 34), TXT, W - 2 * M - 130, 41)
            ty = para(d, M + 120, ty + 8, res, F("Inter-Medium.otf", 27), MUTED, W - 2 * M - 130, 35)
            d.text((M + 120, ty + 6), tech, font=F("Inter-Regular.otf", 21), fill=TECH)
            y += hh + 16


class Bullets(Block):
    flex = 1; maxgrow = 1.8
    def __init__(self, items): self.items = items
    def _f(self): return F("Inter-SemiBold.otf", 38)
    def natural(self, d): return sum(para_h(d, t, self._f(), W - 2 * M - 90, 50) + 34 for t in self.items)
    def draw(self, d, y, h):
        nat = [para_h(d, t, self._f(), W - 2 * M - 90, 50) for t in self.items]
        gap = max(34, (h - sum(nat)) / len(nat))
        for i, (t, hh) in enumerate(zip(self.items, nat)):
            d.ellipse((M, y + 2, M + 56, y + 58), fill=ACC)
            n = str(i + 1); fn = F("InterDisplay-Black.otf", 32)
            d.text((M + 28 - tw(d, n, fn) / 2, y + 8), n, font=fn, fill=BG)
            para(d, M + 86, y + 4, t, self._f(), TXT, W - 2 * M - 90, 50)
            y += hh + gap


class Text(Block):
    def __init__(self, text, size=34, col=TXT, font="Inter-Medium.otf"): self.t, self.s, self.c, self.f = text, size, col, font
    def natural(self, d): return para_h(d, self.t, F(self.f, self.s), W - 2 * M, int(self.s * 1.36))
    def draw(self, d, y, h): para(d, M, y, self.t, F(self.f, self.s), self.c, W - 2 * M, int(self.s * 1.36))


class Matchup(Block):
    """Duelo grande para portadas: dos equipos con su récord y un separador."""
    flex = 2; maxgrow = 1.7
    def __init__(self, a, a_sub, h, h_sub, sep="vs", a_col=TXT, h_col=TXT): self.a, self.as_, self.h, self.hs, self.sep, self.ac, self.hc = a, a_sub, h, h_sub, sep, a_col, h_col
    def natural(self, d): return 330
    def draw(self, d, y, h):
        rowh = (h - 70) / 2
        for k, (name, sub, col) in enumerate(((self.a, self.as_, self.ac), (self.h, self.hs, self.hc))):
            yy = y + k * (rowh + 70)
            s = 120
            while s > 50 and tw(d, name, F("InterDisplay-Black.otf", s)) > W - 2 * M - 230:
                s -= 4
            s = min(s, int(rowh * 0.9))
            d.rounded_rectangle((M, yy, W - M, yy + rowh), radius=24, fill=SURF)
            d.text((M + 32, yy + rowh / 2 - s * 0.62), name, font=F("InterDisplay-Black.otf", s), fill=col)
            fs = F("InterDisplay-Black.otf", 44); w = tw(d, sub, fs)
            d.text((W - M - 32 - w, yy + rowh / 2 - 30), sub, font=fs, fill=ACC)
        fsep = F("Inter-Bold.otf", 30); w = tw(d, self.sep, fsep)
        d.text((W / 2 - w / 2, y + rowh + 16), self.sep, font=fsep, fill=MUTED)


class Gap(Block):
    flex = 1; maxgrow = 99
    def natural(self, d): return 0
    def draw(self, d, y, h): pass


# ------------------------------------------------------------------ slide
def slide(page, total, kicker, title, blocks, takeaway=None, tag=None, style="normal", method=None, title_size=86):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    # cabecera
    d.rectangle((0, 0, W, 10), fill=ACC)
    d.text((M, 70), kicker.upper(), font=F("Inter-Bold.otf", 26), fill=ACC)
    if tag:
        f = F("Inter-Bold.otf", 24); t = tag; w = tw(d, t, f)
        d.rounded_rectangle((W - M - w - 36, 62, W - M, 106), radius=22, fill=ACC)
        d.text((W - M - w - 18, 70), t, font=f, fill=BG)
    s = title_size
    while True:
        ft = F("InterDisplay-Black.otf", s)
        lines = wrap(d, title, ft, W - 2 * M)
        if len(lines) <= 3 or s <= 56:
            break
        s -= 4
    y = 120
    for ln in lines:
        d.text((M, y), ln, font=ft, fill=TXT); y += int(s * 1.04)
    y += 36
    # pie: método y panel
    bottom = TOP_LIMIT
    if method:
        mh = para_h(d, method, F("Inter-Regular.otf", 19), W - 2 * M, 25)
        para(d, M, H - 118 - mh, method, F("Inter-Regular.otf", 19), TECH, W - 2 * M, 25)
        bottom = H - 118 - mh - 22
    if takeaway:
        lime = style in ("cover", "end")
        f = F("InterDisplay-Bold.otf" if lime else "Inter-SemiBold.otf", 40 if lime else 33)
        lh = 52 if lime else 44
        th = para_h(d, takeaway, f, W - 2 * M - 80, lh) + 64
        top = bottom - th
        if lime:
            d.rounded_rectangle((M - 20, top, W - M + 20, bottom), radius=26, fill=ACC)
            para(d, M + 20, top + 32, takeaway, f, BG, W - 2 * M - 40, lh)
        else:
            d.rounded_rectangle((M, top, W - M, bottom), radius=22, fill=SURF)
            d.rounded_rectangle((M, top, M + 10, bottom), radius=5, fill=ACC)
            para(d, M + 40, top + 32, takeaway, f, TXT, W - 2 * M - 80, lh)
        bottom = top - 34
    # reparto del espacio
    nat = [b.natural(d) for b in blocks]
    gaps = 30 * max(0, len(blocks) - 1)
    extra = bottom - y - sum(nat) - gaps
    wsum = sum(b.flex for b in blocks)
    alloc = []
    if extra < 0:
        flexnat = sum(n for b, n in zip(blocks, nat) if b.flex)
        k = max(0.55, 1 + extra / flexnat) if flexnat else 1
        alloc = [n * k if b.flex else n for b, n in zip(blocks, nat)]
    else:
        for b, n in zip(blocks, nat):
            add = extra * b.flex / wsum if wsum else 0
            add = min(add, n * (b.maxgrow - 1)) if b.flex else 0
            alloc.append(n + add)
    left = bottom - y - sum(alloc) - gaps
    gap = 30 + (left / max(1, len(blocks) - 1) if len(blocks) > 1 and left > 0 else 0)
    if len(blocks) == 1 and left > 0:
        y += left / 2
    for b, h in zip(blocks, alloc):
        b.draw(d, int(y), int(h))
        y += h + gap
    # footer
    fx = F("InterDisplay-Black.otf", 38)
    d.text((M, H - 92), "x", font=fx, fill=ACC)
    d.text((M + tw(d, "x", fx) + 2, H - 92), "Gol", font=fx, fill=TXT)
    fp = F("Inter-Medium.otf", 26); t = f"{page}/{total}"
    d.text((W - M - tw(d, t, fp), H - 84), t, font=fp, fill=MUTED)
    return im
