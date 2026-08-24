#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere les gardes technologiques des emplacements de zones urbaines.

    python tools/gen_zone_slot_age_overrides.py <zone_slots_vanilla> --out <fichier>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402
from vanilla_zone_slot_age_map import CITY_ZONE_SLOT_TECH  # noqa: E402


def fin_bloc(text, opening):
    """Retourne l'indice apres le bloc dont l'accolade ouvrante est opening."""
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index + 1
    raise ValueError("bloc non ferme")


def guard(tech, fail_text, why):
    """Garde planete, transparente pour les empires non Ad Astra."""
    return (
        "\n\t\t# Ad Astra : %s\n" % why
        + "\t\tcustom_tooltip = {\n"
        + "\t\t\tfail_text = %s\n" % fail_text
        + "\t\t\tOR = {\n"
        + "\t\t\t\tNOT = { exists = owner }\n"
        + "\t\t\t\towner = {\n"
        + "\t\t\t\t\tOR = {\n"
        + "\t\t\t\t\t\tNOT = { has_origin = origin_adastra }\n"
        + "\t\t\t\t\t\thas_country_flag = adastra_completed\n"
        + "\t\t\t\t\t\thas_technology = %s\n" % tech
        + "\t\t\t\t\t}\n"
        + "\t\t\t\t}\n"
        + "\t\t\t}\n"
        + "\t\t}\n"
    )


def inject(block, tech, fail_text, why):
    """Ajoute la garde dans unlock sans ecraser les conditions vanilla."""
    match = re.search(r"^\tunlock\s*=\s*\{", block, re.M)
    if not match:
        raise ValueError("unlock absent")
    opening = block.index("{", match.start())
    closing = fin_bloc(block, opening) - 1
    closing_line = block.rfind("\n", 0, closing) + 1
    return block[:closing_line] + guard(tech, fail_text, why) + block[closing_line:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vanilla_file")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    source = open(args.vanilla_file, encoding="utf-8-sig", errors="replace").read()
    output = [
        "# Ad Astra 1.4 - emplacements de zones urbaines progressifs.",
        "# FICHIER GENERE PAR tools/gen_zone_slot_age_overrides.py - NE PAS EDITER A LA MAIN.",
        "# Source de verite : tools/vanilla_zone_slot_age_map.py",
        "#",
        "# Le jeu de base ouvre ces deux emplacements aux primitifs. Ad Astra les",
        "# lie aux technologies qui rendent possible une ville specialisee.",
        "",
    ]
    seen = set()
    for name, start, end in top_level_blocks(source):
        if name not in CITY_ZONE_SLOT_TECH:
            continue
        tech, fail_text, why = CITY_ZONE_SLOT_TECH[name]
        output += ["", "### %s -> %s" % (name, tech), inject(source[start:end], tech, fail_text, why)]
        seen.add(name)

    missing = sorted(set(CITY_ZONE_SLOT_TECH) - seen)
    if missing:
        raise SystemExit("emplacements introuvables : %s" % ", ".join(missing))
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(output) + "\n")
    print("emplacements urbains regeneres : %d" % len(seen))


if __name__ == "__main__":
    main()
