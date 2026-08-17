#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - masquage des batiments vanilla anachroniques.

A LANCER AVEC LE PC EN LIGNE : ce script a besoin du dossier common/buildings du
jeu de base, impossible a atteindre hors ligne. Meme principe que
gen_tier1_overrides.py pour les technos.

    python3 tools/gen_building_overrides.py \
        "C:/Program Files (x86)/Steam/steamapps/common/Stellaris/common/buildings" \
        --out ad_astra/common/buildings/zzz_adastra_building_overrides.txt

Quels batiments sont concernes ?
    Un batiment vanilla dont la construction depend d'une techno est deja
    verrouille : la 1.1 a gate les technos, donc le batiment suit. Le probleme
    signale par argroww vient des batiments SANS prerequis technologique, qui
    restent constructibles a l'Age de pierre. Ce sont ceux-la que le script
    cible, plus ceux dont le seul prerequis est une techno de depart.

Rien n'est masque pour les autres empires : la garde commence toujours par
`NOT = { has_origin = origin_adastra }`.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402

# Batiments a NE JAMAIS masquer : sans eux la planete de depart ne fonctionne
# plus. A completer au premier test si un batiment essentiel disparait.
ALLOWLIST = {
    "building_capital",
    "building_capital_1", "building_capital_2", "building_capital_3",
    "building_colony_shelter",
    "building_primitive_capital",
}

# Batiments vanilla que l'on veut disponibles AVANT l'emergence, a partir d'un
# age precis. Cle = batiment vanilla, valeur = drapeau d'age.
# Exemple : "building_foundry_1": "adastra_reached_industrial".
HISTORICAL = {}

GUARD_HEAD = "\t\tNOT = { has_origin = origin_adastra }"


def guard_for(name):
    lines = ["\tpotential = {", "\t\tOR = {", GUARD_HEAD,
             "\t\t\thas_country_flag = adastra_completed"]
    if name in HISTORICAL:
        lines.append("\t\t\thas_country_flag = %s" % HISTORICAL[name])
    lines += ["\t\t}", "\t}"]
    return "\n".join(lines)


def inline_vars(text, path):
    """Remplace les @variables definies dans le meme fichier."""
    for m in re.finditer(r"^(@\w+)\s*=\s*(\S+)", text, re.M):
        text = text.replace(m.group(1), m.group(2))
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_dir")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.vanilla_dir):
        sys.exit("dossier vanilla introuvable : %s" % args.vanilla_dir)

    targets, skipped_tech, skipped_allow = [], [], []
    for fname in sorted(os.listdir(args.vanilla_dir)):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(args.vanilla_dir, fname)
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            src = inline_vars(f.read(), path)
        for name, s, e in top_level_blocks(src):
            if not name.startswith("building_"):
                continue
            block = src[s:e]
            if name in ALLOWLIST:
                skipped_allow.append(name)
                continue
            if re.search(r"\bprerequisites\s*=\s*\{\s*\"", block):
                # deja verrouille par une techno, elle-meme gatee par la 1.1
                skipped_tech.append(name)
                continue
            targets.append(name)

    header = [
        "# Ad Astra 1.2 - masquage des batiments vanilla anachroniques.",
        "# FICHIER GENERE PAR tools/gen_building_overrides.py - NE PAS EDITER A LA MAIN.",
        "#",
        "# Ne concerne QUE les batiments sans prerequis technologique : les autres",
        "# sont deja verrouilles par le gating des technos. Aucun autre empire",
        "# n'est affecte (la garde teste has_origin en premier).",
        "#",
        "# %d batiment(s) masque(s), %d deja couvert(s) par une techno," % (
            len(targets), len(skipped_tech)),
        "# %d en liste blanche." % len(skipped_allow),
        "",
    ]
    body = []
    for name in targets:
        body.append("%s = {\n%s\n}\n" % (name, guard_for(name)))

    out = "\n".join(header) + "\n".join(body)

    print("batiments sans prerequis techno (seront masques) : %d" % len(targets))
    for n in targets:
        print("   " + n)
    print("deja couverts par une techno : %d" % len(skipped_tech))
    print("liste blanche : %s" % ", ".join(sorted(skipped_allow)) or "-")

    if args.dry_run:
        print("\n--dry-run : rien n'a ete ecrit")
        return
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("\necrit : %s" % args.out)


if __name__ == "__main__":
    main()
