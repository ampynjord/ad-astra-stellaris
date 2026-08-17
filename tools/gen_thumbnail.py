#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra - generateur de vignettes de la collection.

Une seule direction artistique pour tous les mods : meme fond, meme typo, meme
composition. Seuls changent le nom du module, le sous-titre et le motif.
Ajouter un mod = ajouter une entree dans MODULES et une fonction de motif.

    python3 tools/gen_thumbnail.py            # tous les modules publies
    python3 tools/gen_thumbnail.py origins    # un seul
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "art")
FONTS = "/usr/share/fonts/truetype/google-fonts"
SERIF = os.path.join(FONTS, "Lora-Variable.ttf")
SANS = os.path.join(FONTS, "Poppins-Medium.ttf")
SANS_L = os.path.join(FONTS, "Poppins-Light.ttf")

S = 4          # supersampling
SIZE = 512     # taille finale

# ----------------------------------------------------------------- palette
DEEP = (5, 8, 22)
HORIZON = (22, 32, 74)
PLANET = (3, 5, 12)
GOLD = (232, 180, 81)
GOLD_HI = (248, 224, 168)
WHITE = (234, 240, 255)
MUTED = (141, 160, 200)

MODULES = {
    "origins": dict(
        module="ORIGINS",
        subtitle="PRÉ-PRL  ·  PRE-FTL",
        motif="rocket",
        tag="BETA",
        file="thumbnail_origins",
    ),
    # Modules a venir : meme fond, meme typo, motif different.
    "nations":  dict(module="NATIONS",  subtitle="GÉOPOLITIQUE  ·  STATECRAFT",
                     motif="crown", tag="", file="thumbnail_nations"),
    "frontier": dict(module="FRONTIER", subtitle="EXPLORATION  ·  CONTACT",
                     motif="probe", tag="", file="thumbnail_frontier"),
}


def font(path, px):
    return ImageFont.truetype(path, px)


def tracked_text(draw, xy, text, fnt, fill, tracking, anchor_center=True):
    """Texte avec interlettrage, centre horizontalement sur xy[0] si demande."""
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_center else xy[0]
    for c, w in zip(text, widths):
        draw.text((x, xy[1]), c, font=fnt, fill=fill)
        x += w + tracking
    return total


def glow(layer, radius, strength=1.0):
    g = layer.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        a = g.split()[3].point(lambda v: int(min(255, v * strength)))
        g.putalpha(a)
    return g


# ------------------------------------------------------------------ fond
def background(w, h):
    base = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(base)
    # degrade vertical vers l'horizon
    for y in range(h):
        t = (y / h) ** 1.6
        c = tuple(int(DEEP[i] + (HORIZON[i] - DEEP[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    base = base.convert("RGBA")

    # deux nebuleuses tres douces
    neb = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    nd = ImageDraw.Draw(neb)
    nd.ellipse([-w * 0.25, h * 0.05, w * 0.55, h * 0.62], fill=(70, 60, 150, 60))
    nd.ellipse([w * 0.55, -h * 0.05, w * 1.3, h * 0.5], fill=(30, 90, 130, 45))
    neb = neb.filter(ImageFilter.GaussianBlur(w * 0.10))
    return Image.alpha_composite(base, neb)


def stars(w, h, seed=7):
    rnd = random.Random(seed)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for _ in range(520):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h * 0.80)
        # plus rare et plus faible pres de l'horizon
        if rnd.random() < (y / (h * 0.80)) * 0.55:
            continue
        r = rnd.choice([1, 1, 1, 1.5, 1.5, 2, 2.6, 3.4]) * (S / 4) * 1.6
        a = int(rnd.uniform(70, 235))
        tint = rnd.choice([WHITE, WHITE, (200, 214, 255), (255, 236, 205)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=tint + (a,))
    lay = Image.alpha_composite(lay, glow(lay, w * 0.004, 0.7))

    # quelques eclats en croix
    bright = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bright)
    for _ in range(7):
        x, y = rnd.uniform(w * 0.05, w * 0.95), rnd.uniform(h * 0.04, h * 0.55)
        L = rnd.uniform(w * 0.018, w * 0.036)
        bd.line([(x - L, y), (x + L, y)], fill=WHITE + (150,), width=max(1, int(S * 0.6)))
        bd.line([(x, y - L), (x, y + L)], fill=WHITE + (150,), width=max(1, int(S * 0.6)))
    return Image.alpha_composite(lay, glow(bright, w * 0.006, 1.2))


def planet(w, h):
    """Limbe planetaire en bas de cadre, avec halo atmospherique."""
    cy = h * 1.40
    r = h * 0.86
    box = [w / 2 - r, cy - r, w / 2 + r, cy + r]

    halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse(box, outline=(120, 170, 255, 190), width=int(h * 0.020))
    halo = glow(halo, h * 0.045, 1.5)

    rim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(rim).ellipse(box, outline=GOLD_HI + (235,), width=int(h * 0.0055))
    rim = Image.alpha_composite(rim, glow(rim, h * 0.012, 1.3))

    body = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(body).ellipse(box, fill=PLANET + (255,))

    # lueur d'atmosphere juste au-dessus du limbe
    band = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(band).ellipse([box[0] - h * 0.03, box[1] - h * 0.03,
                                  box[2] + h * 0.03, box[3] + h * 0.03],
                                 outline=(150, 190, 255, 90), width=int(h * 0.045))
    band = glow(band, h * 0.055, 1.2)

    # quelques lumieres de villes, groupees en agglomerations et serrees contre
    # le limbe : la civilisation est deja la, elle attend de lever les yeux.
    rnd = random.Random(23)
    lights = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lights)
    for _ in range(7):
        ca = rnd.uniform(-0.95, 0.95)
        for _ in range(rnd.randint(4, 8)):
            a = ca + rnd.gauss(0, 0.055)
            dist = r - abs(rnd.gauss(0, h * 0.010)) - h * 0.003
            x = w / 2 + math.sin(a) * dist * 0.82
            y = cy - math.cos(a) * dist
            if not (h * 0.56 < y < h * 0.99):
                continue
            rr = h * rnd.uniform(0.0012, 0.0022)
            ld.ellipse([x - rr, y - rr, x + rr, y + rr],
                       fill=(255, 202, 132, int(rnd.uniform(55, 135))))
    lights = Image.alpha_composite(lights, glow(lights, h * 0.005, 1.1))

    out = Image.alpha_composite(halo, band)
    out = Image.alpha_composite(out, body)
    out = Image.alpha_composite(out, lights)
    return Image.alpha_composite(out, rim)


# ---------------------------------------------------------------- motifs
def motif_rocket(w, h):
    """Fusee montante + arc de trajectoire pointille vers une etoile.
    Tout le motif vit sous la zone de texte (qui s'arrete vers 0.33 h)."""
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    lw = max(1, int(h * 0.0050))

    x0, y0 = w * 0.225, h * 0.660
    x1, y1 = w * 0.775, h * 0.415
    cx, cy = w * 0.30, h * 0.395
    pts = []
    for i in range(121):
        t = i / 120
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t ** 2 * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t ** 2 * y1
        pts.append((x, y))
    for i in range(0, 118, 6):
        seg = pts[i:i + 4]
        if len(seg) > 1:
            d.line(seg, fill=GOLD + (int(45 + 160 * (i / 118)),), width=lw)

    # etoile d'arrivee
    sx, sy = x1, y1
    R = h * 0.026
    d.line([(sx - R, sy), (sx + R, sy)], fill=GOLD_HI + (255,), width=lw)
    d.line([(sx, sy - R), (sx, sy + R)], fill=GOLD_HI + (255,), width=lw)
    d.line([(sx - R * 0.42, sy - R * 0.42), (sx + R * 0.42, sy + R * 0.42)],
           fill=GOLD_HI + (150,), width=max(1, int(lw * 0.7)))
    d.line([(sx - R * 0.42, sy + R * 0.42), (sx + R * 0.42, sy - R * 0.42)],
           fill=GOLD_HI + (150,), width=max(1, int(lw * 0.7)))
    d.ellipse([sx - R * 0.22, sy - R * 0.22, sx + R * 0.22, sy + R * 0.22],
              fill=GOLD_HI + (255,))

    # fusee alignee sur la tangente de depart
    tang = math.atan2(pts[3][1] - pts[0][1], pts[3][0] - pts[0][0])
    L, W = h * 0.132, h * 0.043
    # on recule la fusee le long de la tangente : son nez tombe sur le depart de l'arc
    rx = x0 - math.cos(tang) * L * 0.60
    ry = y0 - math.sin(tang) * L * 0.60

    def rot(px, py):
        return (rx + px * math.cos(tang) - py * math.sin(tang),
                ry + px * math.sin(tang) + py * math.cos(tang))

    d.polygon([rot(L * 0.60, 0), rot(L * 0.30, -W * 0.36), rot(L * 0.10, -W * 0.50),
               rot(-L * 0.36, -W * 0.50), rot(-L * 0.36, W * 0.50),
               rot(L * 0.10, W * 0.50), rot(L * 0.30, W * 0.36)],
              fill=(10, 14, 32, 255), outline=GOLD_HI + (255,), width=lw)
    for k in (-1, 1):
        d.polygon([rot(-L * 0.14, k * W * 0.50), rot(-L * 0.52, k * W * 1.06),
                   rot(-L * 0.36, k * W * 0.50)], fill=GOLD + (240,))
    hx, hy = rot(L * 0.20, 0)
    hr = W * 0.19
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=GOLD_HI + (255,))

    flame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flame)
    fd.polygon([rot(-L * 0.38, -W * 0.32), rot(-L * 0.38, W * 0.32),
                rot(-L * 1.20, 0)], fill=(255, 186, 104, 215))
    lay = Image.alpha_composite(lay, glow(flame, h * 0.014, 1.6))
    return Image.alpha_composite(lay, glow(lay, h * 0.010, 0.5))


def motif_crown(w, h):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    lw = max(1, int(h * 0.0050))
    cx, cy, R = w * 0.5, h * 0.44, h * 0.085
    pts = [(cx - R, cy + R * 0.62), (cx - R, cy - R * 0.55), (cx - R * 0.5, cy),
           (cx, cy - R * 0.85), (cx + R * 0.5, cy), (cx + R, cy - R * 0.55),
           (cx + R, cy + R * 0.62)]
    d.line(pts + [pts[0]], fill=GOLD_HI + (255,), width=lw, joint="curve")
    return Image.alpha_composite(lay, glow(lay, h * 0.012, 0.8))


def motif_probe(w, h):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    lw = max(1, int(h * 0.0050))
    cx, cy, R = w * 0.5, h * 0.42, h * 0.075
    d.ellipse([cx - R * 0.3, cy - R * 0.3, cx + R * 0.3, cy + R * 0.3],
              outline=GOLD_HI + (255,), width=lw)
    for k in (-1, 1):
        d.line([(cx + k * R * 0.35, cy), (cx + k * R * 1.15, cy)],
               fill=GOLD + (235,), width=lw)
        d.line([(cx + k * R * 1.15, cy - R * 0.42), (cx + k * R * 1.15, cy + R * 0.42)],
               fill=GOLD + (235,), width=lw)
    return Image.alpha_composite(lay, glow(lay, h * 0.012, 0.8))


MOTIFS = {"rocket": motif_rocket, "crown": motif_crown, "probe": motif_probe}


# ------------------------------------------------------------------ texte
def typography(w, h, cfg):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)

    f_title = font(SERIF, int(h * 0.108))
    f_mod = font(SANS, int(h * 0.040))
    f_sub = font(SANS_L, int(h * 0.0245))
    f_tag = font(SANS, int(h * 0.0225))

    tracked_text(d, (w / 2, h * 0.093), "AD ASTRA", f_title, GOLD_HI + (255,), h * 0.020)

    # filet + nom du module
    y = h * 0.238
    tw = tracked_text(d, (w / 2, y), cfg["module"], f_mod, WHITE + (240,), h * 0.030)
    rule = tw / 2 + h * 0.035
    for k in (-1, 1):
        x = w / 2 + k * rule
        d.line([(x, y + h * 0.030), (x + k * h * 0.075, y + h * 0.030)],
               fill=GOLD + (150,), width=max(1, int(h * 0.0028)))

    tracked_text(d, (w / 2, h * 0.303), cfg["subtitle"], f_sub, (176, 194, 232) + (255,), h * 0.014)

    if cfg["tag"]:
        ty = h * 0.885
        tw = tracked_text(d, (w / 2, ty), cfg["tag"], f_tag, GOLD + (255,), h * 0.020)
        for k in (-1, 1):
            x = w / 2 + k * (tw / 2 + h * 0.028)
            d.line([(x, ty + h * 0.017), (x + k * h * 0.055, ty + h * 0.017)],
                   fill=GOLD + (120,), width=max(1, int(h * 0.0022)))

    return Image.alpha_composite(lay, glow(lay, h * 0.012, 0.45))


def vignette(w, h):
    v = Image.new("L", (w, h), 0)
    ImageDraw.Draw(v).ellipse([-w * 0.30, -h * 0.30, w * 1.30, h * 1.30], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(w * 0.10))
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    lay.putalpha(v.point(lambda p: int((255 - p) * 0.70)))
    return lay


def render(key, cfg):
    w = h = SIZE * S
    img = background(w, h)
    img = Image.alpha_composite(img, stars(w, h))
    img = Image.alpha_composite(img, planet(w, h))
    img = Image.alpha_composite(img, MOTIFS[cfg["motif"]](w, h))
    img = Image.alpha_composite(img, vignette(w, h))
    img = Image.alpha_composite(img, typography(w, h, cfg))

    os.makedirs(OUT, exist_ok=True)
    big = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
    small = img.convert("RGB").resize((SIZE, SIZE), Image.LANCZOS)
    p1 = os.path.join(OUT, cfg["file"] + "_1024.png")
    p2 = os.path.join(OUT, cfg["file"] + "_512.png")
    big.save(p1)
    small.save(p2)
    print("  %s -> %s / %s" % (key, os.path.basename(p1), os.path.basename(p2)))


if __name__ == "__main__":
    want = sys.argv[1:] or ["origins"]
    print("Ad Astra - vignettes")
    for k in want:
        render(k, MODULES[k])
