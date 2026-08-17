#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - applique tools/vanilla_building_age_map.py.

Produit les surcharges qui rendent chaque batiment vanilla constructible a
partir de son age, et pas avant. Aucun autre empire n'est affecte : la garde
commence toujours par NOT has_origin.

On ne surcharge QUE le bloc potential, sans recopier le reste du batiment : en
Clausewitz, un bloc redeclare remplace le precedent, donc il faut au contraire
repartir du fichier vanilla. C'est pour ca que le script a besoin du dossier du
jeu de base.

    python3 tools/gen_building_age_overrides.py <dossier_vanilla_buildings> --out <fichier>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402
from vanilla_building_age_map import BUILDING_AGE  # noqa: E402


def guard(age, why):
    """Le potential d'un batiment est evalue en portee PLANETE : les triggers de
    pays doivent passer par owner, sinon le moteur rejette la garde entiere."""
    return (
        "\tpotential = {\n"
        "\t\t# Ad Astra : %s\n" % why +
        "\t\tOR = {\n"
        "\t\t\tNOT = { exists = owner }\n"
        "\t\t\towner = {\n"
        "\t\t\t\tOR = {\n"
        "\t\t\t\t\tNOT = { has_origin = origin_adastra }\n"
        "\t\t\t\t\thas_country_flag = adastra_completed\n"
        "\t\t\t\t\thas_country_flag = adastra_reached_%s\n" % age +
        "\t\t\t\t}\n"
        "\t\t\t}\n"
        "\t\t}\n")


def inject(block, age, why):
    m = re.search(r"^\tpotential = \{", block, re.M)
    if m:
        return block[:m.start()] + guard(age, why) + block[m.end():]
    head = block.index("{") + 1
    return block[:head] + "\n" + guard(age, why) + "\t}\n" + block[head:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_dir")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    # 1.2 : "tech" rejoint "na" et "keep" - ces batiments sont dates par leur
    # techno prerequise (tools/vanilla_tech_age_map.py), on ne les surcharge plus.
    todo = {k: v for k, v in BUILDING_AGE.items() if v[0] not in ("na", "keep", "tech")}
    out = ["# Ad Astra 1.2 - age de disponibilite des batiments vanilla.",
           "# FICHIER GENERE PAR tools/gen_building_age_overrides.py - NE PAS EDITER A LA MAIN.",
           "# Source de verite : tools/vanilla_building_age_map.py",
           "#",
           "# En 4.4 un batiment est debloque par une zone, pas par une techno, et les",
           "# zones ne sont pas gatees par techno : rien dans le jeu de base n'empeche",
           "# une fonderie d'alliage a l'Age de pierre. Chaque batiment recoit donc",
           "# l'age de la techno d'epoque equivalente de notre arbre.",
           ""]
    seen, done = set(), []
    for fname in sorted(os.listdir(args.vanilla_dir)):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(args.vanilla_dir, fname),
                  encoding="utf-8-sig", errors="replace") as f:
            src = f.read()
        for name, s, e in top_level_blocks(src):
            if name not in todo:
                continue
            age, why = todo[name]
            seen.add(name)
            out.append("")
            out.append("### %s -> %s" % (name, age))
            out.append(inject(src[s:e], age, why))
            done.append((name, age))

    missing = sorted(set(todo) - seen)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")

    from collections import Counter
    print("surcharges ecrites : %d" % len(done))
    for age, n in Counter(a for _k, a in done).most_common():
        print("   %-12s %2d" % (age, n))
    keep = [k for k, v in BUILDING_AGE.items() if v[0] == "keep"]
    na = [k for k, v in BUILDING_AGE.items() if v[0] == "na"]
    bytech = [k for k, v in BUILDING_AGE.items() if v[0] == "tech"]
    print("laisses disponibles : %d  |  inatteignables, non touches : %d"
          "  |  dates par leur techno : %d" % (len(keep), len(na), len(bytech)))
    if missing:
        print("INTROUVABLES DANS LE VANILLA : %s" % ", ".join(missing))
    print("ecrit : %s" % args.out)


if __name__ == "__main__":
    main()
