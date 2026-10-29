"""xGol — helpers del estilo narrativo v3 (tesis → pasos → veredicto → lógica), paleta de alto contraste."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_car_gb import font as F, base, para, wrap, BG, TXT, ACC, NEG, W, H, M

MUTED = "#B3BDC9"
LINE = "#3B4757"
SURF = "#1A2330"
GHOST = "#D5DCE4"
AMBER = "#FFC24B"


def kicker(d, text):
    d.text((M, 110), text.upper(), font=F("Inter-SemiBold.otf", 26), fill=ACC)


def footer(d, page, total):
    fx = F("InterDisplay-Black.otf", 36)
    d.text((M, H - 100), "x", font=fx, fill=ACC)
    d.text((M + d.textlength("x", font=fx) + 2, H - 100), "Gol", font=fx, fill=TXT)
    f = F("Inter-Medium.otf", 26)
    s = f"{page}/{total}"
    d.text((W - M - d.textlength(s, font=f), H - 92), s, font=f, fill=MUTED)


def headline(d, text, y=160, size=66, col=TXT):
    f = F("InterDisplay-Black.otf", size)
    for ln in wrap(d, text, f, W - 2 * M):
        d.text((M, y), ln, font=f, fill=col)
        y += int(size * 1.1)
    return y


def body(d, y, text, size=28, col=MUTED):
    return para(d, (M, y), text, F("Inter-Regular.otf", size), col, W - 2 * M, int(size * 1.42))


def bridge(d, text):
    f = F("Inter-SemiBold.otf", 29)
    lines = wrap(d, text, f, W - 2 * M - 60)
    y = H - 160 - len(lines) * 40
    d.line((M, y - 26, W - M, y - 26), fill=LINE, width=2)
    for i, ln in enumerate(lines):
        d.text((M, y), ln, font=f, fill=TXT)
        if i == len(lines) - 1:
            d.text((M + d.textlength(ln, font=f) + 14, y - 2), "→", font=F("InterDisplay-Black.otf", 32), fill=ACC)
        y += 40
    return H - 160 - len(lines) * 40 - 26


def how(d, y, text):
    d.text((M, y), "CÓMO SE CALCULA", font=F("Inter-Bold.otf", 21), fill=MUTED)
    return para(d, (M, y + 32), text, F("Inter-Regular.otf", 25), MUTED, W - 2 * M, 35)


def steps_tag(d, n):
    x = W - M - 3 * 46
    for i in range(1, 4):
        on = i <= n
        d.ellipse((x, 104, x + 34, 138), fill=ACC if i == n else (MUTED if on else LINE))
        t = str(i); fs = F("Inter-Bold.otf", 20)
        d.text((x + 17 - d.textlength(t, font=fs) / 2, 109), t, font=fs, fill=BG if on else MUTED)
        x += 46


def mvm(d, y, team, model, market, lk="Mercado"):
    bw = W - 2 * M
    for lab, v, col in (("Nuestro modelo", model, ACC), (lk, market, GHOST)):
        d.text((M, y), lab, font=F("Inter-SemiBold.otf", 26), fill=MUTED)
        d.rounded_rectangle((M, y + 40, M + bw, y + 96), radius=14, fill=SURF)
        d.rounded_rectangle((M, y + 40, M + int(bw * v), y + 96), radius=14, fill=col)
        d.text((M + 22, y + 46), f"{team} {round(v*100)}%", font=F("InterDisplay-Black.otf", 40), fill=BG)
        y += 124
    return y


def verdict(d, y, items):
    for n, t, s in items:
        d.ellipse((M, y, M + 56, y + 56), fill=ACC)
        fn = F("InterDisplay-Black.otf", 34)
        d.text((M + 28 - d.textlength(n, font=fn) / 2, y + 6), n, font=fn, fill=BG)
        d.text((M + 82, y + 4), t, font=F("InterDisplay-Bold.otf", 36), fill=TXT)
        y = para(d, (M + 82, y + 52), s, F("Inter-Regular.otf", 27), MUTED, W - 2 * M - 82, 37) + 32
    return y


def flow(d, y, steps, legal):
    for i, (a, b) in enumerate(steps):
        last = i == len(steps) - 1
        d.rounded_rectangle((M, y, W - M, y + 100), radius=16, fill=ACC if last else SURF)
        d.text((M + 28, y + 14), a, font=F("InterDisplay-Bold.otf", 32), fill=BG if last else TXT)
        d.text((M + 28, y + 58), b, font=F("Inter-Medium.otf", 23), fill=BG if last else MUTED)
        y += 100
        if not last:
            d.text((W // 2 - 10, y), "↓", font=F("InterDisplay-Black.otf", 32), fill=MUTED)
            y += 40
    para(d, (M, H - 215), legal, F("Inter-Regular.otf", 18), MUTED, W - 2 * M, 24)
