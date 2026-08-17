#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - applique tools/vanilla_district_age_map.py.

Un district se controle par son bloc `potential` (portee planete). Comme pour
les batiments, on repart du bloc vanilla complet et on insere la garde : un bloc
redeclare remplace le precedent, on ne peut pas surcharger un seul champ.

    python3 tools/gen_district_age_overrides.py <dossier_vanilla_districts> --out <fichier>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402
from vanilla_district_age_map import DISTRICT_TECH, UPKEEP_SWAP  # noqa: E402



def inline_vars(block, at_vars):
    """Les @variables sont locales au fichier vanilla. Un bloc recopie sans
    elles donne « Malformed token: @base_cost » au chargement : on inline."""
    for k in sorted(at_vars, key=len, reverse=True):
        block = block.replace(k, at_vars[k])
    return block


def _fin_du_bloc(texte, i):
    """Rend l'indice APRES l'accolade fermante du bloc ouvert a partir de i."""
    d = 0
    j = texte.index("{", i)
    while j < len(texte):
        c = texte[j]
        if c == "{":
            d += 1
        elif c == "}":
            d -= 1
            if d == 0:
                return j + 1
        j += 1
    raise SystemExit("bloc non ferme")


def swap_upkeep(block, name):
    """Reecrit l'entretien en energie en deux blocs mutuellement exclusifs.

    Avant l'electricite, le district se paie en minerais et en nourriture : de
    la matiere qui s'use, et des bras qu'il faut nourrir. La garde passe par
    adastra_pays_energy_upkeep, vrai pour tous les empires SAUF un empire
    Ad Astra encore prive d'energie.

    DEUX PIEGES, tous deux rencontres sur district_city, tous deux visibles
    seulement dans error.log :

    1. Le point d'insertion. Chercher la prochaine occurrence de « \t\t} »
       apres la ligne d'energie ne marche pas : c'est une SOUS-CHAINE de
       « \t\t\t} ». Sur un bloc upkeep contenant un trigger vanilla
       multiligne, l'insertion tombait dedans - « Unexpected token: upkeep ».
       On compte les accolades.

    2. Le trigger deja present. district_city porte
       « trigger = { NOT = { has_modifier = wooden_planet } } » : ajouter un
       second trigger a cote laisse le moteur n'en garder qu'un, et c'est le
       notre qui saute. La condition vanilla est donc RECOPIEE dans les deux
       blocs, et la notre s'y ajoute.
    """
    for old, amount in UPKEEP_SWAP.get(name, []):
        marker = "\t\t\t%s\n" % old
        if marker not in block:
            raise SystemExit(
                "%s : bloc d'entretien « %s » introuvable - le jeu de base a "
                "change, relire la table UPKEEP_SWAP" % (name, old))

        # bornes du bloc upkeep qui contient la ligne
        pos = block.index(marker)
        debut = block.rindex("\t\tupkeep = {", 0, pos)
        d, k = 0, block.index("{", debut)
        while True:
            if block[k] == "{":
                d += 1
            elif block[k] == "}":
                d -= 1
                if d == 0:
                    break
            k += 1
        fin = k + 1
        corps = block[debut:fin]

        # conditions vanilla deja presentes dans ce bloc, recopiees telles quelles
        vanilla_cond = ""
        m = re.search(r"trigger\s*=\s*\{", corps)
        if m:
            d2, k2 = 0, m.end() - 1
            while True:
                if corps[k2] == "{":
                    d2 += 1
                elif corps[k2] == "}":
                    d2 -= 1
                    if d2 == 0:
                        break
                k2 += 1
            vanilla_cond = "\n".join(
                l for l in corps[m.end():k2].split("\n") if l.strip())

        def bloc(lignes, garde):
            out = ["\t\tupkeep = {"] + lignes + ["\t\t\ttrigger = {"]
            if vanilla_cond:
                out.append(vanilla_cond)
            out.append("\t\t\t\t%s" % garde)
            out += ["\t\t\t}", "\t\t}"]
            return "\n".join(out)

        minerals, food = amount
        pre = ["\t\t\t# Ad Astra : avant l'electricite, on entretient ses carrieres",
               "\t\t\t# et ses champs avec du materiau et du travail, pas avec du",
               "\t\t\t# courant.",
               "\t\t\tminerals = %d" % minerals]
        if food:
            pre.append("\t\t\tfood = %d" % food)

        neuf = (bloc(["\t\t\t%s" % old], "owner = { adastra_pays_energy_upkeep = yes }")
                + "\n"
                + bloc(pre, "owner = { NOT = { adastra_pays_energy_upkeep = yes } }"))
        block = block[:debut] + neuf + block[fin:]
    return block


def guard(tech, why):
    """Portee PLANETE : les triggers de pays passent par owner."""
    return (
        "\tpotential = {\n"
        "\t\t# Ad Astra : %s\n" % why +
        "\t\tOR = {\n"
        "\t\t\tNOT = { exists = owner }\n"
        "\t\t\towner = {\n"
        "\t\t\t\tOR = {\n"
        "\t\t\t\t\tNOT = { has_origin = origin_adastra }\n"
        "\t\t\t\t\thas_country_flag = adastra_completed\n"
        "\t\t\t\t\thas_technology = %s\n" % tech +
        "\t\t\t\t}\n"
        "\t\t\t}\n"
        "\t\t}\n")


def inject(block, tech, why):
    m = re.search(r"^\tpotential = \{", block, re.M)
    if m:
        return block[:m.start()] + guard(tech, why) + block[m.end():]
    head = block.index("{") + 1
    return block[:head] + "\n" + guard(tech, why) + "\t}\n" + block[head:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_dir")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    todo = {k: v for k, v in DISTRICT_TECH.items() if v[0] not in ("na", "keep")}
    todo_upkeep = set(UPKEEP_SWAP)
    out = ["# Ad Astra 1.2 - technologie requise par district.",
           "# FICHIER GENERE PAR tools/gen_district_age_overrides.py - NE PAS EDITER A LA MAIN.",
           "# Source de verite : tools/vanilla_district_age_map.py",
           "#",
           "# Un district cree ses emplois tout seul, sans batiment ni zone. C'est le",
           "# troisieme etage du systeme de 4.4, et celui qui nous avait echappe :",
           "# la planete de depart portait deux districts generateurs, donc de",
           "# l'electricite a l'Age de pierre.",
           ""]
    seen, done = set(), []
    seen_upkeep, done_upkeep = set(), []
    for fname in sorted(os.listdir(args.vanilla_dir)):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(args.vanilla_dir, fname),
                  encoding="utf-8-sig", errors="replace") as f:
            src = f.read()
        at_vars = dict(re.findall(r"^(@[A-Za-z0-9_]+)\s*=\s*(\S+)", src, re.M))
        for name, s, e in top_level_blocks(src):
            if name not in todo and name not in todo_upkeep:
                continue
            block = inline_vars(src[s:e], at_vars)
            if name in todo_upkeep:
                block = swap_upkeep(block, name)
                seen_upkeep.add(name)
            if name in todo:
                tech, why = todo[name]
                block = inject(block, tech, why)
                seen.add(name)
                done.append((name, tech))
            else:
                done_upkeep.append(name)
            out.append("")
            out.append("### %s%s" % (name, " -> " + todo[name][0] if name in todo else " : entretien d'epoque"))
            out.append(block)

    missing = sorted((set(todo) - seen) | (todo_upkeep - seen_upkeep))
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")

    print("districts surcharges : %d" % len(done))
    for name, tech in done:
        print("   %-24s <- %s" % (name, tech))
    keep = [k for k, v in DISTRICT_TECH.items() if v[0] == "keep"]
    na = [k for k, v in DISTRICT_TECH.items() if v[0] == "na"]
    print("entretien d'epoque : %s" % ", ".join(sorted(done_upkeep)))
    print("laisses disponibles : %d | non touches : %d" % (len(keep), len(na)))
    if missing:
        print("INTROUVABLES DANS LE VANILLA : %s" % ", ".join(missing))
    print("ecrit : %s" % args.out)


if __name__ == "__main__":
    main()
