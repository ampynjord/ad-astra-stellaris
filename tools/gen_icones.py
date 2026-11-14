#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra - fabrique des icônes de technologie dans la direction du jeu.

Constat, après avoir ouvert les fichiers du jeu de base : les icônes sont des
DDS **52x52**, non compressés (BGRA 32 bits), sans mipmap. Deux sous-styles
coexistent :

  1. des objets peints en 3D, avec spéculaire et matière — irreproductible ici ;
  2. des **glyphes filaires lumineux** posés sur un fond sombre teinté et
     quadrillé — celui-là est géométrique, donc reproductible.

Ce module fabrique le second. Il ne cherche pas à imiter la peinture : il joue
la carte du plan technique, qui existe déjà dans le jeu et qui a l'avantage
d'être *cohérent* sur 250 entrées là où un mélange d'icônes vanilla empruntées
ne l'est jamais.

Le fond est teinté par domaine de recherche, comme dans le jeu :
    physique    -> bleu nuit / cyan
    société     -> vert profond / turquoise
    ingénierie  -> rouille / ambre

    python3 tools/gen_icones.py --apercu     # planche de comparaison
    python3 tools/gen_icones.py --tout       # les 250 .dds
"""
import argparse
import math
import os
import struct
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from age_techs_data import AGES, TECHS  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "ad_astra", "gfx", "interface", "icons", "technologies")

COTE = 52
ECHELLE = 8          # on dessine en grand puis on réduit : c'est ce qui donne
                     # des bords propres sans antialiasing maison

# Fond et trait par domaine, relevés à la pipette sur les icônes du jeu.
PALETTE = {
    "physics":     ((14, 26, 48), (28, 52, 92), (120, 205, 255)),
    "society":     ((12, 34, 32), (24, 66, 60), (120, 245, 205)),
    "engineering": ((44, 22, 18), (86, 42, 30), (255, 186, 110)),
}


def fond(domaine):
    """Dégradé radial sombre + quadrillage, comme les icônes filaires du jeu."""
    sombre, clair, _trait = PALETTE[domaine]
    n = COTE * ECHELLE
    img = Image.new("RGBA", (n, n), sombre + (255,))
    d = ImageDraw.Draw(img)
    centre = n / 2.0
    # dégradé : on empile des ellipses de plus en plus sombres
    for i in range(24, 0, -1):
        r = n * 0.75 * i / 24.0
        f = i / 24.0
        c = tuple(int(clair[k] * (1 - f) + sombre[k] * f) for k in range(3))
        d.ellipse([centre - r, centre - r, centre + r, centre + r], fill=c + (255,))
    # quadrillage
    pas = n // 7
    grille = tuple(int(clair[k] * 1.25) for k in range(3))
    for i in range(1, 7):
        d.line([(i * pas, 0), (i * pas, n)], fill=grille + (26,), width=max(1, ECHELLE // 3))
        d.line([(0, i * pas), (n, i * pas)], fill=grille + (26,), width=max(1, ECHELLE // 3))
    return img


def cadre(img, domaine):
    """Vignette sombre sur les bords : les icônes du jeu ne sont jamais à vif."""
    n = img.size[0]
    voile = Image.new("L", (n, n), 0)
    ImageDraw.Draw(voile).ellipse([n * 0.02, n * 0.02, n * 0.98, n * 0.98], fill=255)
    voile = voile.filter(ImageFilter.GaussianBlur(n * 0.16))
    noir = Image.new("RGBA", (n, n), (0, 0, 0, 255))
    return Image.composite(img, noir, voile)


def halo(calque, couleur, force=1.0):
    """Le glyphe est dessiné deux fois : flou coloré dessous, trait net dessus."""
    n = calque.size[0]
    flou = calque.filter(ImageFilter.GaussianBlur(n * 0.035))
    flou = Image.eval(flou, lambda v: int(v * 0.85 * force))
    return flou


# --------------------------------------------------------------- les glyphes
# Chaque glyphe est une fonction (dessin, taille) -> None, en coordonnées
# relatives : 0 à 1. On reste sur des formes simples et lisibles à 52 pixels.

def _l(d, n, pts, w=0.055):
    d.line([(x * n, y * n) for x, y in pts], fill=255, width=max(1, int(w * n)),
           joint="curve")


def _c(d, n, cx, cy, r, w=0.055):
    d.ellipse([(cx - r) * n, (cy - r) * n, (cx + r) * n, (cy + r) * n],
              outline=255, width=max(1, int(w * n)))


def g_flamme(d, n):
    _l(d, n, [(0.5, 0.15), (0.68, 0.42), (0.62, 0.58), (0.72, 0.72),
              (0.5, 0.85), (0.28, 0.72), (0.38, 0.58), (0.32, 0.42), (0.5, 0.15)])
    _l(d, n, [(0.5, 0.45), (0.58, 0.63), (0.5, 0.75), (0.42, 0.63), (0.5, 0.45)], 0.04)


def g_roue(d, n):
    _c(d, n, 0.5, 0.5, 0.34)
    _c(d, n, 0.5, 0.5, 0.10)
    for k in range(8):
        a = k * math.pi / 4
        _l(d, n, [(0.5 + 0.10 * math.cos(a), 0.5 + 0.10 * math.sin(a)),
                  (0.5 + 0.34 * math.cos(a), 0.5 + 0.34 * math.sin(a))], 0.035)


def g_lunette(d, n):
    _l(d, n, [(0.20, 0.70), (0.74, 0.28)], 0.10)
    _l(d, n, [(0.66, 0.20), (0.82, 0.36)], 0.05)
    _l(d, n, [(0.30, 0.78), (0.30, 0.88)], 0.05)
    _l(d, n, [(0.18, 0.88), (0.44, 0.88)], 0.05)


def g_puce(d, n):
    d.rectangle([0.30 * n, 0.30 * n, 0.70 * n, 0.70 * n], outline=255,
                width=max(1, int(0.05 * n)))
    d.rectangle([0.42 * n, 0.42 * n, 0.58 * n, 0.58 * n], outline=255,
                width=max(1, int(0.04 * n)))
    for k in range(3):
        y = 0.38 + k * 0.12
        _l(d, n, [(0.14, y), (0.30, y)], 0.035)
        _l(d, n, [(0.70, y), (0.86, y)], 0.035)
        _l(d, n, [(0.38 + k * 0.12, 0.14), (0.38 + k * 0.12, 0.30)], 0.035)
        _l(d, n, [(0.38 + k * 0.12, 0.70), (0.38 + k * 0.12, 0.86)], 0.035)


def g_epi(d, n):
    _l(d, n, [(0.5, 0.88), (0.5, 0.22)], 0.05)
    for k in range(4):
        y = 0.30 + k * 0.14
        _l(d, n, [(0.5, y + 0.08), (0.30, y)], 0.04)
        _l(d, n, [(0.5, y + 0.08), (0.70, y)], 0.04)


def g_fusee(d, n):
    _l(d, n, [(0.5, 0.12), (0.64, 0.42), (0.64, 0.70), (0.36, 0.70), (0.36, 0.42), (0.5, 0.12)])
    _l(d, n, [(0.36, 0.62), (0.22, 0.80), (0.36, 0.74)], 0.04)
    _l(d, n, [(0.64, 0.62), (0.78, 0.80), (0.64, 0.74)], 0.04)
    _c(d, n, 0.5, 0.42, 0.07, 0.04)


GLYPHES = {
    "fire": g_flamme, "wheel": g_roue, "telescope": g_lunette,
    "transistor": g_puce, "agriculture": g_epi, "rocketry": g_fusee,
}


def icone(domaine, glyphe):
    n = COTE * ECHELLE
    img = cadre(fond(domaine), domaine)
    calque = Image.new("L", (n, n), 0)
    glyphe(ImageDraw.Draw(calque), n)
    _s, _c2, trait = PALETTE[domaine]
    lueur = Image.new("RGBA", (n, n), trait + (0,))
    lueur.putalpha(halo(calque, trait))
    img = Image.alpha_composite(img, lueur)
    net = Image.new("RGBA", (n, n), tuple(min(255, int(v * 1.25)) for v in trait) + (0,))
    net.putalpha(calque)
    img = Image.alpha_composite(img, net)
    return img.resize((COTE, COTE), Image.LANCZOS)


def ecrit_dds(img, chemin):
    """DDS 52x52 BGRA non compresse, sans mipmap - le format du jeu."""
    l, h = img.size
    px = img.convert("RGBA").tobytes()
    bgra = bytearray(len(px))
    for i in range(0, len(px), 4):
        bgra[i] = px[i + 2]; bgra[i + 1] = px[i + 1]
        bgra[i + 2] = px[i]; bgra[i + 3] = px[i + 3]
    entete = bytearray(128)
    entete[0:4] = b"DDS "
    struct.pack_into("<I", entete, 4, 124)
    struct.pack_into("<I", entete, 8, 0x1 | 0x2 | 0x4 | 0x1000 | 0x8)
    struct.pack_into("<I", entete, 12, h)
    struct.pack_into("<I", entete, 16, l)
    struct.pack_into("<I", entete, 20, l * 4)
    struct.pack_into("<I", entete, 76, 32)
    struct.pack_into("<I", entete, 80, 0x41)          # RGBA non compresse
    struct.pack_into("<I", entete, 88, 32)
    struct.pack_into("<I", entete, 92, 0x00FF0000)
    struct.pack_into("<I", entete, 96, 0x0000FF00)
    struct.pack_into("<I", entete, 100, 0x000000FF)
    struct.pack_into("<I", entete, 104, 0xFF000000)
    struct.pack_into("<I", entete, 108, 0x1000)
    open(chemin, "wb").write(bytes(entete) + bytes(bgra))


def apercu():
    """Planche de comparaison : nos glyphes au-dessus, le jeu de base dessous."""
    exemples = [("fire", "physics"), ("wheel", "engineering"),
                ("telescope", "physics"), ("transistor", "physics"),
                ("agriculture", "society"), ("rocketry", "engineering")]
    n = len(exemples)
    planche = Image.new("RGBA", (COTE * n, COTE * 2 + 4), (18, 20, 26, 255))
    for i, (cle, dom) in enumerate(exemples):
        planche.paste(icone(dom, GLYPHES[cle]), (i * COTE, 0))
        van = os.path.join(SORTIE, "tech_adastra_%s.dds" % cle)
        if os.path.exists(van):
            planche.paste(Image.open(van).convert("RGBA"), (i * COTE, COTE + 4))
    planche = planche.resize((planche.size[0] * 4, planche.size[1] * 4), Image.NEAREST)
    chemin = os.path.join(RACINE, "kit", "apercu_icones.png")
    planche.save(chemin)
    print("planche ecrite :", chemin)
    print("ligne du haut : fabriquees | ligne du bas : jeu de base actuellement en place")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apercu", action="store_true")
    a = ap.parse_args()
    if a.apercu:
        apercu()
    else:
        ap.print_help()
