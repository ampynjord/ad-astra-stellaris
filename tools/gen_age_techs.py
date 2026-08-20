#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere les correctifs 1.3.x des technologies d'age.

La source du generateur 1.3.0 n'avait pas ete versionnee avec la sortie.
Ce generateur conservatif maintient donc exactement ses donnees generees et
ne transforme que les gardes de tirage qui peuvent invalider une recherche.
"""

from pathlib import Path
import re
import sys


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "ad_astra"
TARGET = ROOT / "common" / "technology" / "adastra_age_techs.txt"
ENGLISH = ROOT / "localisation" / "english" / "adastra_ages_l_english.yml"
NEXT_AGE = re.compile(r"^\s*NOT = \{ has_country_flag = (adastra_reached_[a-z]+) \}\s*$")
INVALID_GROWTH = re.compile(r"^(\s*)pop_growth_speed\s*=\s*([0-9.]+)\s*$")
WAVE_GATE = re.compile(r"^\s*has_country_flag = adastra_vague_[2-5]\s*$")
POST_AGE_WEIGHT = "# 1.3.1 : hors tirage apres l'age"
BUILDINGS_EN = {
    "Monument des ancêtres": "Ancestral Monument",
    "Grenier": "Granary",
    "Fonderie": "Foundry",
    "Maison des tablettes": "House of Tablets",
    "Tribunal": "Courthouse",
    "Moulin": "Mill",
    "Citadelle": "Citadel",
    "Université": "University",
    "Manufacture": "Manufactory",
    "Station de radiodiffusion": "Broadcasting Station",
    "École publique": "Public School",
}


def transform(lines):
    """Retire les gardes qui peuvent invalider une recherche en cours."""
    output = []
    in_potential = False
    potential_depth = 0
    next_age = None
    changed = 0
    growth_fixed = 0
    wave_removed = 0
    post_age_removed = 0
    skip_post_age_weight = False
    post_age_depth = 0

    for line in lines:
        if line.strip().startswith(POST_AGE_WEIGHT):
            skip_post_age_weight = True
            post_age_removed += 1
            continue

        if skip_post_age_weight:
            if line.strip() == "weight_modifier = {":
                post_age_depth = line.count("{") - line.count("}")
                continue
            if post_age_depth:
                post_age_depth += line.count("{") - line.count("}")
                if post_age_depth == 0:
                    skip_post_age_weight = False
                continue
            raise SystemExit("weight_modifier 1.3.1 incomplet apres son commentaire")

        growth = INVALID_GROWTH.match(line)
        if growth:
            output.append(f"{growth.group(1)}logistic_growth_mult = {growth.group(2)}\n")
            growth_fixed += 1
            continue

        if line.strip() == "potential = {":
            in_potential = True
            potential_depth = line.count("{") - line.count("}")
            next_age = None
            output.append(line)
            continue

        if in_potential:
            if WAVE_GATE.match(line):
                wave_removed += 1
                continue
            match = NEXT_AGE.match(line)
            if match:
                next_age = match.group(1)
                changed += 1
                continue

            potential_depth += line.count("{") - line.count("}")
            output.append(line)
            if potential_depth == 0:
                if next_age:
                    output.extend([
                        "\n",
                        "\t# 1.3.1 : hors tirage apres l'age, mais toujours valide pour give_technology.\n",
                        "\tweight_modifier = {\n",
                        "\t\tfactor = 1\n",
                        "\t\tmodifier = {\n",
                        "\t\t\tfactor = 0\n",
                        f"\t\t\thas_country_flag = {next_age}\n",
                        "\t\t}\n",
                        "\t}\n",
                    ])
                in_potential = False
            continue

        output.append(line)

    return output, changed, growth_fixed, wave_removed, post_age_removed


def main():
    lines = TARGET.read_text(encoding="utf-8-sig").splitlines(keepends=True)
    transformed, changed, growth_fixed, wave_removed, post_age_removed = transform(lines)
    transformed = [
        line.replace(
            "# Source de verite : tools/age_techs_data.py\n",
            "# Source de verite : 1.3.0, correctif applique par tools/gen_age_techs.py\n",
        )
        for line in transformed
    ]
    if changed:
        raise SystemExit("une exclusion d'age 1.3.0 est reapparue dans potential")
    if wave_removed not in (0, 200):
        raise SystemExit(f"{wave_removed} gardes de vague retirees au lieu de 200 attendues.")
    if post_age_removed not in (0, 225):
        raise SystemExit(f"{post_age_removed} weight_modifier 1.3.1 retires au lieu de 225 attendus.")
    if wave_removed:
        print("200 gardes de vague retirees : une recherche reste valide entre deux ages.")
    if post_age_removed:
        print("225 exclusions de tirage apres l'age retirees.")

    if growth_fixed not in (0, 8):
        raise SystemExit(f"{growth_fixed} modificateurs de croissance corriges au lieu des 8 attendus.")
    if growth_fixed:
        print(f"{growth_fixed} modificateurs pop_growth_speed remplaces.")

    TARGET.write_text("".join(transformed), encoding="utf-8", newline="\n")

    english = ENGLISH.read_text(encoding="utf-8-sig")
    for french, english_name in BUILDINGS_EN.items():
        english = english.replace(
            f"Unlocks the building: {french}",
            f"Unlocks the building: {english_name}",
        )
    ENGLISH.write_text(english, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
