#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controles des invariants de la ligne de hotfix 1.3.x."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).parents[1]
TECHS = ROOT / "ad_astra" / "common" / "technology" / "adastra_age_techs.txt"
EVENTS = ROOT / "ad_astra" / "events" / "adastra_events.txt"
DESCRIPTOR = ROOT / "ad_astra" / "descriptor.mod"
SCRIPT_VALUES = ROOT / "ad_astra" / "common" / "script_values" / "adastra_script_values.txt"
COUNTRY_TYPES = ROOT / "ad_astra" / "common" / "country_types" / "adastra_country_types.txt"
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
    country_types = COUNTRY_TYPES.read_text(encoding="utf-8-sig")
    declared = re.search(r'^version="([^"]+)"$', descriptor, re.MULTILINE)
    if not declared:
        fail("le descripteur doit annoncer une version")
    argument = sys.argv[1] if len(sys.argv) > 1 else ""
    expected = argument.removeprefix("v") if argument else declared.group(1)
    if declared.group(1) != expected:
        fail(f"le descripteur annonce {declared.group(1)} au lieu de {expected}")
    if len(re.findall(r"^tech_adastra_[a-z0-9_]+ = \{", techs, re.MULTILINE)) != 250:
        fail("le hotfix doit conserver les 250 technologies d'epoque de la 1.3")
    if "NOT = { has_country_flag = adastra_reached_" in techs:
        fail("une exclusion d'age est encore dans potential")
    if techs.count("# 1.3.1 : hors tirage apres l'age") != 225:
        fail("les 225 exclusions d'age attendues ne sont pas toutes des weight_modifier")
    if "pop_growth_speed" in techs:
        fail("une technologie utilise encore pop_growth_speed, ignore par Stellaris 4.4")
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
        lines = localisation.read_text(encoding="utf-8-sig").splitlines()
        line = next((line for line in lines
                     if line.lstrip().startswith("origin_adastra_effects:0 ")), "")
        if not line or "\\n" not in line or not line.endswith('"'):
            fail(f"localisation origin_adastra_effects invalide : {localisation.name}")
        for number, content in enumerate(lines[1:], start=2):
            if content and not content.startswith((" ", "#")):
                fail(f"localisation non indentee : {localisation.name}:{number}")
    grounded = country_types.split("adastra_grounded = {", 1)[1].split("resources =", 1)[0]
    if "standard_diplomacy_module = { contact_rule = on_action_only }" not in grounded:
        fail("le pays confine doit eviter les sites de premier contact bloques")
    print("0 erreur : invariants 1.3.1 valides.")


if __name__ == "__main__":
    main()
