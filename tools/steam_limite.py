#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra - controle la limite de 1000 caracteres des commentaires Steam.

Steam a refuse un message de 986 caracteres. La limite ne compte donc pas les
caracteres au sens Python. Deux facteurs s'ajoutent :

  - les sauts de ligne sont envoyes en CRLF, soit deux caracteres chacun ;
  - les caracteres non ASCII (tiret cadratin, apostrophe typographique, accents)
    pesent plusieurs octets en UTF-8.

Le pire cas est donc « octets UTF-8 + un par saut de ligne ». Ce script mesure
les trois valeurs et signale le pire. Ecrire en ASCII pur supprime toute
ambiguite : le pire cas devient caracteres + sauts de ligne.

    python3 tools/steam_limite.py fichier.txt [autre.txt ...]
    python3 tools/steam_limite.py --limite 8000 workshop_description_FR.txt

DEUX LIMITES A CONNAITRE
  - commentaire Steam       : 1000 caracteres (defaut de ce script)
  - description d'un objet  : 8000 caracteres

Le 16/08, la description francaise a ete refusee par Steam avec un simple
« Un probleme est survenu lors de la sauvegarde du titre et de la
description » - aucune mention de longueur. Elle faisait 8666 caracteres.
L'anglaise, a 7799, est passee. Mesurer avant de coller.
"""
import sys

LIMITE = 1000
MARGE = 40          # on ne poste pas a 999


def mesure(chemin):
    s = open(chemin, encoding="utf-8").read()
    nl = s.count("\n")
    pire = len(s.encode("utf-8")) + nl
    non_ascii = sorted({c for c in s if ord(c) > 127})
    return len(s), pire, nl, non_ascii


def main():
    global LIMITE
    args = sys.argv[1:]
    if args and args[0] == "--limite":
        LIMITE = int(args[1])
        args = args[2:]
    mauvais = 0
    for chemin in args:
        n, pire, nl, non_ascii = mesure(chemin)
        etat = "OK" if pire <= LIMITE - MARGE else (
            "LIMITE" if pire <= LIMITE else "TROP LONG")
        if pire > LIMITE - MARGE:
            mauvais += 1
        print("%-42s %4d car. | pire cas %4d | %2d lignes | %s"
              % (chemin.split("/")[-1], n, pire, nl, etat))
        if non_ascii:
            print("      non-ASCII (chacun compte double ou triple) : %s"
                  % " ".join(non_ascii))
    return 1 if mauvais else 0


if __name__ == "__main__":
    sys.exit(main())
