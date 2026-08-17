#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra - reecrit workshop_item.vdf en entier, jamais par substitution.

POURQUOI CET OUTIL EXISTE. Le 16/08, pour poser le changenote de la 1.3, j'ai
fait une substitution par expression reguliere sur le vdf :

    re.sub(r'("changenote"\s+")(.*)(")', ..., s, flags=re.S)

Le `.*` est gourmand et re.S lui fait traverser les sauts de ligne : il a donc
mange tout ce qui suivait, y compris la ligne

    "publishedfileid"  "3781408257"

SteamCMD, ne trouvant plus d'identifiant, n'a pas mis a jour le mod : il en a
publie un SECOND. Il a fallu supprimer le doublon a la main.

La lecon n'est pas « mieux ecrire la regex » : c'est qu'on ne modifie pas un
fichier structure par substitution textuelle. Cet outil reconstruit le vdf
champ par champ, et refuse d'ecrire si l'identifiant publie manque.

    python3 tools/maj_vdf.py --changenote-fichier kit/workshop_changenote_1_3.txt
"""
import argparse
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# L'identifiant du mod sur le Workshop. En dur, et c'est voulu : c'est la seule
# valeur dont la perte cree un doublon public.
PUBLISHED_FILE_ID = "3781408257"

CHAMPS = [
    ("appid", "281990"),
    ("contentfolder", r"C:\Users\Public\AdAstra\content"),
    ("previewfile", r"C:\Users\Public\AdAstra\thumbnail.png"),
    ("visibility", "0"),
    ("title", "Ad Astra - Origins (Pre-FTL / Pre-PRL) [BETA]"),
    ("description",
     "Start as a pre-FTL civilization, climb every age of history, run your own "
     "space program and emerge into the galaxy. / Commencez en civilisation pre-PRL, "
     "traversez tous les ages, menez votre programme spatial et emergez dans la "
     "galaxie. Full description: see below (updated after upload). No DLC required. "
     "Stellaris v4.4."),
]


def lit_changenote(chemin):
    s = open(chemin, encoding="utf-8").read()
    morceaux = s.split("-" * 72)
    corps = morceaux[1] if len(morceaux) > 1 else s
    corps = re.sub(r"\s+", " ", corps).strip()
    hors = sorted({c for c in corps if ord(c) > 126})
    if hors:
        sys.exit("changenote : caracteres non-ASCII %s" % hors)
    if '"' in corps:
        sys.exit("changenote : guillemet double interdit dans un vdf")
    return corps


def ecrit(chemin_sortie, changenote):
    lignes = ['"workshopitem"', "{"]
    for cle, val in CHAMPS:
        lignes.append('\t"%s"\t\t"%s"' % (cle, val))
    lignes.append('\t"changenote"\t\t"%s"' % changenote)
    lignes.append('\t"publishedfileid"\t\t"%s"' % PUBLISHED_FILE_ID)
    lignes.append("}")
    texte = "\n".join(lignes) + "\n"
    if PUBLISHED_FILE_ID not in texte:
        sys.exit("REFUS : identifiant publie absent - SteamCMD creerait un doublon")
    open(chemin_sortie, "w", encoding="utf-8").write(texte)
    return texte


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--changenote-fichier", required=True)
    ap.add_argument("--sortie", default=os.path.join(RACINE, "kit", "workshop_item.vdf"))
    a = ap.parse_args()
    note = lit_changenote(a.changenote_fichier)
    t = ecrit(a.sortie, note)
    print("vdf ecrit : %s" % a.sortie)
    print("  changenote : %d caracteres" % len(note))
    print("  publishedfileid : %s" % PUBLISHED_FILE_ID)
