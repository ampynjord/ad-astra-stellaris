#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - rendre la diplomatie possible pendant le confinement.

LE PROBLEME (rapporte par Sithiya, partie « rester pre-PRL pour toujours »)
    Quatorze actions diplomatiques du jeu de base testent `is_country_type =
    default` en dur. L'empire confine est de type `adastra_grounded` : il echoue
    au test et perd l'initiative diplomatique. Il peut accepter, jamais proposer.

LA CORRECTION
    On reprend les actions concernees telles quelles depuis le jeu de base et on
    elargit le test a notre type de pays, dans le bloc `potential` uniquement.
    L'elargissement vaut dans les deux sens : on peut proposer, et on peut se
    voir proposer. Le reste de l'action n'est pas touche.

    Seules les actions de NEGOCIATION sont reprises. L'espionnage et les actions
    d'un empire stellaire *envers* un pre-PRL (illumination, commerce pre-PRL)
    restent fermees : ce sont des choses qu'on nous fait, pas qu'on fait.

    python3 tools/gen_diplomacy_overrides.py <00_actions.txt> --out <fichier>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402

# Actions reprises, et pourquoi.
ACTIONS = {
    "action_improve_relation":       "ameliorer les relations : negocier, c'est la base",
    "action_harm_relation":          "degrader les relations : l'inverse doit exister aussi",
    "action_form_research_agreement": "accord de recherche : echanger du savoir sans quitter sa planete",
}

OLD = "is_country_type = default"
NEW = "OR = { is_country_type = default is_country_type = adastra_grounded }"


def widen_potential(block):
    """Elargit le test de type de pays, dans le bloc potential seulement."""
    m = re.search(r"^\tpotential = \{", block, re.M)
    if not m:
        return block, 0
    depth, i = 0, m.end() - 1
    while i < len(block):
        if block[i] == "{":
            depth += 1
        elif block[i] == "}":
            depth -= 1
            if depth == 0:
                i += 1
                break
        i += 1
    head, pot, tail = block[:m.start()], block[m.start():i], block[i:]
    n = pot.count(OLD)
    return head + pot.replace(OLD, NEW) + tail, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_file")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    src = open(args.vanilla_file, encoding="utf-8-sig", errors="replace").read()
    out = ["# Ad Astra 1.2 - diplomatie pendant le confinement.",
           "# FICHIER GENERE PAR tools/gen_diplomacy_overrides.py - NE PAS EDITER A LA MAIN.",
           "#",
           "# Les actions sont reprises telles quelles du jeu de base ; seul le test",
           "# `is_country_type = default` du bloc potential est elargi a notre type.",
           "# Aucun autre empire n'est affecte : le type default reste accepte.",
           ""]
    done, total = [], 0
    for name, s, e in top_level_blocks(src):
        if name not in ACTIONS:
            continue
        block, n = widen_potential(src[s:e])
        if not n:
            print("  ATTENTION : aucun test elargi dans %s" % name)
        out.append("")
        out.append("### %s - %s" % (name, ACTIONS[name]))
        out.append(block)
        done.append((name, n))
        total += n

    missing = sorted(set(ACTIONS) - {d[0] for d in done})
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    for name, n in done:
        print("  %-34s %d test(s) elargi(s)" % (name, n))
    if missing:
        print("  INTROUVABLES : %s" % ", ".join(missing))
    print("total : %d action(s), %d test(s)" % (len(done), total))
    print("ecrit : %s" % args.out)


if __name__ == "__main__":
    main()
