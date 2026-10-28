"""xGol — render profile picture and CAR @ GB carousel (provisional brand style)."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.environ.get("XGOL_OUT", "/tmp/xgol-out")
os.makedirs(OUT, exist_ok=True)
F = "/usr/share/fonts/opentype/inter/"

def font(name, size):
    return ImageFont.truetype(F + name, size)

BG = "#0A0E13"
SURF = "#141B24"
LINE = "#232C38"
TXT = "#F2F4F7"
MUTED = "#8A94A3"
ACC = "#C6FF3D"   # lime
NEG = "#FF6B5B"   # coral for weak spots
W, H = 1080, 1350
M = 80

def base():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    return im, d

def wordmark(d, x, y, size=44):
    fx = font("InterDisplay-Black.otf", size)
    d.text((x, y), "x", font=fx, fill=ACC)
    wx = d.textlength("x", font=fx)
    d.text((x + wx + 2, y), "Gol", font=fx, fill=TXT)

def footer(d, page, total):
    wordmark(d, M, H - 100, 36)
    f = font("Inter-Medium.otf", 26)
    s = f"{page}/{total}"
    d.text((W - M - d.textlength(s, font=f), H - 92), s, font=f, fill=MUTED)

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def para(d, xy, text, f, fill, maxw, lh):
    x, y = xy
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=fill); y += lh
    return y

def kicker(d, y, text):
    f = font("Inter-SemiBold.otf", 26)
    d.text((M, y), text.upper(), font=f, fill=ACC)

TOTAL = 5

# ---------- Profile picture ----------
def profile():
    S = 1080
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    fx = font("InterDisplay-Black.otf", 470)
    tw = d.textlength("xG", font=fx)
    wx = d.textlength("x", font=fx)
    bbox = d.textbbox((0, 0), "xG", font=fx)
    h = bbox[3] - bbox[1]
    x0 = (S - tw) / 2
    y0 = (S - h) / 2 - bbox[1] - 10
    d.text((x0, y0), "x", font=fx, fill=ACC)
    d.text((x0 + wx, y0), "G", font=fx, fill=TXT)
    im.save(f"{OUT}/xgol_perfil.png")

# ---------- Slide 1: cover ----------
def s1():
    im, d = base()
    kicker(d, 110, "NFL · Semana 8 · Jueves 29 oct · 18:15 CDMX")
    fb = font("InterDisplay-Black.otf", 190)
    d.text((M - 6, 170), "CAR", font=fb, fill=TXT)
    fa = font("InterDisplay-Medium.otf", 90)
    d.text((M, 395), "@", font=fa, fill=MUTED)
    d.text((M + 95, 350), "GB", font=fb, fill=TXT)

    # probability block
    y = 700
    d.text((M, y), "Probabilidad de victoria · modelo xGol", font=font("Inter-Medium.otf", 30), fill=MUTED)
    y += 60
    pg, pc = 56, 44
    bw = W - 2 * M
    wg = int(bw * pg / 100)
    d.rounded_rectangle((M, y, M + bw, y + 70), radius=14, fill=SURF)
    d.rounded_rectangle((M + bw - wg, y, M + bw, y + 70), radius=14, fill=ACC)
    fn = font("InterDisplay-Bold.otf", 40)
    d.text((M + 24, y + 12), f"CAR {pc}%", font=fn, fill=TXT)
    s = f"GB {pg}%"
    d.text((M + bw - 24 - d.textlength(s, font=fn), y + 12), s, font=fn, fill=BG)

    y += 140
    fh = font("InterDisplay-Bold.otf", 54)
    y = para(d, (M, y), "Duelo de debilidades:", fh, TXT, W - 2 * M, 66)
    fbody = font("Inter-Regular.otf", 40)
    para(d, (M, y + 10), "el peor ataque terrestre de la NFL contra una de las defensas que más deja correr.",
         fbody, MUTED, W - 2 * M, 54)
    footer(d, 1, TOTAL)
    im.save(f"{OUT}/xgol_car_gb_1.png")

# ---------- Slide 2: table ----------
def s2():
    im, d = base()
    kicker(d, 110, "Así llegan · Semanas 1–7")
    d.text((M, 160), "Los números", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    rows = [
        ("Récord", "3-3", "", "4-3", ""),
        ("Dif. de puntos / partido", "-1.2", "21°", "-0.1", "18°"),
        ("EPA / jugada, ataque", "+0.06", "9°", "0.00", "16°"),
        ("EPA / jugada, defensa", "+0.02", "20°", "-0.06", "4°"),
        ("EPA neta / jugada", "+0.04", "12°", "+0.05", "10°"),
        ("Tasa de éxito, ataque", "43.6%", "15°", "39.2%", "28°"),
    ]
    y = 300
    fh = font("Inter-SemiBold.otf", 28)
    cx1, cx2 = 640, 870
    d.text((cx1, y), "CAR", font=fh, fill=MUTED)
    d.text((cx2, y), "GB", font=fh, fill=MUTED)
    y += 60
    fl = font("Inter-Medium.otf", 32)
    fv = font("InterDisplay-Bold.otf", 46)
    fr = font("Inter-Medium.otf", 24)
    for lab, a, ar, b, br in rows:
        d.line((M, y, W - M, y), fill=LINE, width=2)
        y += 26
        d.text((M, y + 8), lab, font=fl, fill=TXT)
        for cx, v, r in ((cx1, a, ar), (cx2, b, br)):
            d.text((cx, y), v, font=fv, fill=TXT)
            if r:
                d.text((cx, y + 56), r + " de 32", font=fr, fill=MUTED)
        y += 100
    d.line((M, y, W - M, y), fill=LINE, width=2)
    fn = font("Inter-Regular.otf", 30)
    para(d, (M, y + 34), "EPA = puntos esperados que suma cada jugada. En ataque, más alto es mejor; en defensa, más bajo es mejor.",
         fn, MUTED, W - 2 * M, 42)
    footer(d, 2, TOTAL)
    im.save(f"{OUT}/xgol_car_gb_2.png")

# ---------- strip helper (rank 1..32) ----------
def strip(d, y, rank, label, color):
    x0, x1 = M, W - M
    d.text((M, y), label, font=font("Inter-Medium.otf", 30), fill=TXT)
    y += 56
    d.rounded_rectangle((x0, y, x1, y + 14), radius=7, fill=SURF)
    px = x0 + (x1 - x0) * (rank - 1) / 31
    d.ellipse((px - 22, y - 15, px + 22, y + 29), fill=color)
    fr = font("Inter-Medium.otf", 22)
    d.text((x0, y + 36), "1° mejor", font=fr, fill=MUTED)
    s = "32° peor"
    d.text((x1 - d.textlength(s, font=fr), y + 36), s, font=fr, fill=MUTED)
    s = f"{rank}°"
    fb = font("InterDisplay-Bold.otf", 34)
    d.text((px - d.textlength(s, font=fb) / 2, y - 64 + 6), "", font=fb, fill=color)
    return y + 90

# ---------- Slide 3: key stat ----------
def s3():
    im, d = base()
    kicker(d, 110, "El dato clave")
    d.text((M, 160), "Algo tiene", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    d.text((M, 262), "que ceder", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    fb = font("InterDisplay-Black.otf", 150)
    y = 430
    d.text((M, y), "3.0", font=fb, fill=NEG)
    para(d, (M + 300, y + 30), "yardas por acarreo de Green Bay: último lugar en EPA por carrera (32 de 32).",
         font("Inter-Medium.otf", 34), TXT, W - 2 * M - 300, 46)
    y += 230
    d.text((M, y), "4.8", font=fb, fill=NEG)
    para(d, (M + 300, y + 30), "yardas por acarreo que permite Carolina: 30° de 32 en EPA contra la carrera.",
         font("Inter-Medium.otf", 34), TXT, W - 2 * M - 300, 46)
    y += 270
    y = strip(d, y, 32, "GB · ataque terrestre (EPA)", NEG)
    strip(d, y + 30, 30, "CAR · defensa contra la carrera (EPA)", NEG)
    footer(d, 3, TOTAL)
    im.save(f"{OUT}/xgol_car_gb_3.png")

# ---------- Slide 4: strength vs strength ----------
def s4():
    im, d = base()
    kicker(d, 110, "Fuerza contra fuerza")
    d.text((M, 160), "El otro duelo", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    y = 330
    para(d, (M, y), "Carolina ataca mejor de lo que dice su récord. Enfrente tendrá una de las defensas más eficientes de la liga.",
         font("Inter-Regular.otf", 36), MUTED, W - 2 * M, 50)
    y = 560
    y = strip(d, y, 9, "CAR · ataque (EPA por jugada)", ACC)
    y = strip(d, y + 50, 4, "GB · defensa (EPA permitida por jugada)", ACC)
    y = strip(d, y + 50, 5, "GB · defensa contra el pase", ACC)
    footer(d, 4, TOTAL)
    im.save(f"{OUT}/xgol_car_gb_4.png")

# ---------- Slide 5: method ----------
def s5():
    im, d = base()
    kicker(d, 110, "Cómo lo calculamos")
    d.text((M, 160), "Modelo xGol v0", font=font("InterDisplay-Black.otf", 92), fill=TXT)
    items = [
        ("1", "Diferencia de EPA neta por jugada entre ambos equipos."),
        ("2", "× 61.6 jugadas por partido (promedio de la liga)."),
        ("3", "× 0.5 por regresión a la media: 6–7 partidos son poca muestra."),
        ("4", "+ 1.5 puntos por jugar en casa."),
        ("=", "GB por +2.0 puntos → 56% de probabilidad."),
    ]
    y = 340
    fnum = font("InterDisplay-Black.otf", 54)
    ft = font("Inter-Medium.otf", 34)
    for n, t in items:
        d.text((M, y - 6), n, font=fnum, fill=ACC)
        yy = para(d, (M + 80, y), t, ft, TXT, W - 2 * M - 80, 46)
        y = max(yy, y + 46) + 40
    y += 20
    d.line((M, y, W - M, y), fill=LINE, width=2)
    fs = font("Inter-Regular.otf", 28)
    y = para(d, (M, y + 30), "Muestra corta = incertidumbre alta. Un 56% significa que Green Bay pierde en más de 4 de cada 10 escenarios.",
             fs, MUTED, W - 2 * M, 40)
    y = para(d, (M, y + 20), "Datos: nflverse (CC-BY 4.0), temporada 2026, semanas 1–7. Análisis independiente, no afiliado a la NFL ni a ningún equipo. No es recomendación de apuesta.",
             fs, MUTED, W - 2 * M, 40)
    footer(d, 5, TOTAL)
    im.save(f"{OUT}/xgol_car_gb_5.png")

if __name__ == "__main__":
    profile(); s1(); s2(); s3(); s4(); s5()
    print(sorted(os.listdir(OUT)))
