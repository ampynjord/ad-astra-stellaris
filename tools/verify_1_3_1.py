#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controles specifiques au hotfix 1.3.1."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).parents[1]
TECHS = ROOT / "ad_astra" / "common" / "technology" / "adastra_age_techs.txt"
EVENTS = ROOT / "ad_astra" / "events" / "adastra_events.txt"
DESCRIPTOR = ROOT / "ad_astra" / "descriptor.mod"
SCRIPT_VALUES = ROOT / "ad_astra" / "common" / "script_values" / "adastra_script_values.txt"
LOCALISATIONS = (
    ROOT / "ad_astra" / "localisation" / "english" / "adastra_l_english.yml",
    ROOT / "ad_astra" / "localisation" / "french" / "adastra_l_french.yml",
)


def fail(message):
    print(f"ERREUR : {message}")
    raise SystemExit(1)


def main():
    techs = TECHS.read_text(encoding="utf-8-sig")
    events = EVENTS.read_text(encoding="utf-8-sig")
    descriptor = DESCRIPTOR.read_text(encoding="utf-8-sig")
    script_values = SCRIPT_VALUES.read_text(encoding="utf-8-sig")
    if 'version="1.3.1"' not in descriptor:
        fail("le descripteur doit annoncer 1.3.1")
    if len(re.findall(r"^tech_adastra_[a-z0-9_]+ = \{", techs, re.MULTILINE)) != 250:
        fail("le hotfix doit conserver les 250 technologies d'epoque de la 1.3")
    if "NOT = { has_country_flag = adastra_reached_" in techs:
        fail("une exclusion d'age est encore dans potential")
    if techs.count("# 1.3.1 : hors tirage apres l'age") != 225:
        fail("les 225 exclusions d'age attendues ne sont pas toutes des weight_modifier")
    grants = events.index("adastra_grant_starting_ages_1_3_1 = yes")
    capital = events.index("# 1.2 : la capitale demarre specialisee")
    if grants > capital:
        fail("les octrois d'age doivent preceder la preparation de la capitale")
    for fragment in (
        "add_zone = { district = district_city zone = zone_industrial zone_slot = 1 }",
        "building = building_factory_1",
        "add_zone = { district = district_city zone = zone_research_unity zone_slot = 2 }",
        "building = building_research_lab_1",
        "while = { count = 2 add_district = district_generator }",
    ):
        if fragment not in events:
            fail(f"reconstruction economique absente : {fragment}")
    if re.search(r"\b(if|limit)\s*=", script_values):
        fail("script_values contient une syntaxe CK3 invalide")
    for name, multiplier in (("adastra_cout_relance_explore", "mult = 0.35"),
                             ("adastra_cout_relance_navy", "mult = 0.25")):
        block = re.search(rf"{name} = \{{(.*?)^\}}", script_values, re.MULTILINE | re.DOTALL)
        if not block or multiplier not in block.group(1):
            fail(f"surcout de relance invalide : {name}")
    for localisation in LOCALISATIONS:
        line = next((line for line in localisation.read_text(encoding="utf-8-sig").splitlines()
                     if line.startswith("origin_adastra_effects:0 ")), "")
        if not line or "\\n" not in line or not line.endswith('"'):
            fail(f"localisation origin_adastra_effects invalide : {localisation.name}")
    print("0 erreur : invariants 1.3.1 valides.")


if __name__ == "__main__":
    main()
