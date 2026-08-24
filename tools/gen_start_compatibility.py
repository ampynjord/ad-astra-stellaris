#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le nettoyage des infrastructures de depart anachroniques.

La table de datation vanilla est l'unique source. Le moteur peut poser les
batiments apres le premier evenement de l'origine selon l'ethique, le civisme
ou un contenu DLC. Cette sortie est appelee au demarrage et au jour 4.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vanilla_building_age_map import CIVIC_BUILDING_UNLOCKS, STARTUP_BUILDING_AGE  # noqa: E402


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ad_astra" / "common" / "scripted_effects" / "zz_adastra_start_compatibility.txt"


def condition(age):
    if age == "ftl":
        return "NOT = { has_country_flag = adastra_completed }"
    return "NOT = { has_country_flag = adastra_reached_%s }" % age


def render():
    out = [
        "# Ad Astra - compatibilite des infrastructures de depart.",
        "# FICHIER GENERE PAR tools/gen_start_compatibility.py - NE PAS EDITER A LA MAIN.",
        "# Source de verite : tools/vanilla_building_age_map.py (STARTUP_BUILDING_AGE).",
        "#",
        "# L'effet est execute sur la capitale pendant l'initialisation et au jour 4.",
        "# Il neutralise les structures posees par les scripts vanilla avant leur epoque,",
        "# quelle que soit l'ethique, le civisme ou le DLC qui les a declenchees.",
        "",
        "adastra_cleanup_start_infrastructure = {",
    ]
    for key, age in sorted(STARTUP_BUILDING_AGE.items()):
        out.extend((
            "\tif = {",
            "\t\tlimit = { owner = { %s } }" % condition(age),
            "\t\tremove_building = %s" % key,
            "\t}",
        ))
    out.append("}")
    out.extend((
        "",
        "# Les batiments explicitement fournis par un civisme reviennent des que leur",
        "# economie est capable d'assurer leur entretien. L'effet est appele sur la",
        "# capitale et ne remplace jamais un batiment existant.",
        "adastra_grant_civic_infrastructure = {",
    ))
    for civic, data in sorted(CIVIC_BUILDING_UNLOCKS.items()):
        building = data["building"]
        out.extend((
            "\tif = {",
            "\t\tlimit = {",
            "\t\t\towner = { has_civic = %s }" % civic,
            "\t\t\towner = { has_country_flag = adastra_reached_%s }" % data["age"],
            *["\t\t\towner = { %s = yes }" % trigger for trigger in data["triggers"]],
            "\t\t\tfree_building_slots > 0",
            "\t\t\tNOT = { has_building = %s }" % building,
            "\t\t}",
            "\t\tadd_building = %s" % building,
            "\t}",
        ))
    out.append("}")
    return "\n".join(out) + "\n"


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8", newline="\n")
    print("ecrit : %s (%d batiments)" % (OUT.relative_to(ROOT), len(STARTUP_BUILDING_AGE)))


if __name__ == "__main__":
    main()
