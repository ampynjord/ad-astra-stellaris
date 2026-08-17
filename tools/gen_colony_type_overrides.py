#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - rend les designations de capitale accessibles a un empire confine.

CE QUI A ETE TROUVE (retour Sithiya, Workshop, 13/08)
    « cant do capital or colony designations pre-ftl ».

    Cause : cinq designations de capitale du jeu de base exigent
    « is_country_type = default », parfois sous une forme retournee :

        NAND = { FROM? = { OR = { NOT = { is_country_type = default }
                                  is_gestalt = yes } } }

    Un empire Ad Astra est du type adastra_grounded pendant tout le confinement.
    Aucune de ces designations ne lui est donc proposee, et comme sa seule
    planete est sa capitale, il n'a acces a aucune designation du tout.

LA METHODE
    La meme que pour les actions diplomatiques : on repart du bloc vanilla
    complet et on ELARGIT la condition au lieu de la remplacer. Chaque
    « is_country_type = default » devient

        OR = { is_country_type = default  is_country_type = adastra_grounded }

    Ce remplacement est correct dans les deux positions : en position positive
    il ajoute notre type, et sous un NOT il l'ajoute aussi, par De Morgan. Aucun
    autre empire de la galaxie ne voit de difference.

    python3 tools/gen_colony_type_overrides.py <fichier_vanilla> --out <fichier>
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402

# Designations a elargir. Les variantes ruche et machine sont volontairement
# absentes : l'origine est reservee aux empires reguliers.
A_ELARGIR = [
    "col_capital",
    "col_capital_foundry",
    "col_capital_factory",
    "col_capital_trade",
    "col_capital_extraction",
]

CIBLE = "is_country_type = default"
REMPLACEMENT = "OR = { is_country_type = default  is_country_type = adastra_grounded }"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_file")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    src = open(args.vanilla_file, encoding="utf-8-sig", errors="replace").read()
    out = ["# Ad Astra 1.2 - designations de capitale pour un empire confine.",
           "# FICHIER GENERE PAR tools/gen_colony_type_overrides.py - NE PAS EDITER A LA MAIN.",
           "#",
           "# Cinq designations de capitale exigent is_country_type = default. Un empire",
           "# Ad Astra est en adastra_grounded pendant tout le confinement : aucune ne lui",
           "# etait proposee, et comme sa seule planete est sa capitale, il n'avait acces a",
           "# aucune designation. Retour de Sithiya sur le Workshop.",
           "#",
           "# La condition est ELARGIE, jamais remplacee : les autres empires de la galaxie",
           "# ne voient aucune difference.",
           ""]
    vus, total = [], 0
    for name, s, e in top_level_blocks(src):
        if name not in A_ELARGIR:
            continue
        bloc = src[s:e]
        n = bloc.count(CIBLE)
        if not n:
            raise SystemExit("%s : plus de « %s » - le jeu de base a change" % (name, CIBLE))
        out.append("")
        out.append("### %s (%d condition%s elargie%s)" % (name, n, "s" if n > 1 else "",
                                                          "s" if n > 1 else ""))
        out.append(bloc.replace(CIBLE, REMPLACEMENT))
        vus.append(name)
        total += n

    manquants = [k for k in A_ELARGIR if k not in vus]
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")

    print("designations elargies : %d (%d conditions)" % (len(vus), total))
    for k in vus:
        print("   %s" % k)
    if manquants:
        print("INTROUVABLES DANS LE VANILLA : %s" % ", ".join(manquants))
    print("ecrit : %s" % args.out)


if __name__ == "__main__":
    main()
