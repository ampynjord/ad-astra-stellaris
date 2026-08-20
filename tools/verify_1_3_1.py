#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controles specifiques aux hotfixes 1.3.x."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).parents[1]
TECHS = ROOT / "ad_astra" / "common" / "technology" / "adastra_age_techs.txt"
EVENTS = ROOT / "ad_astra" / "events" / "adastra_events.txt"
DESCRIPTOR = ROOT / "ad_astra" / "descriptor.mod"
LAUNCHER_DESCRIPTOR = ROOT / "ad_astra.mod"
SCRIPT_VALUES = ROOT / "ad_astra" / "common" / "script_values" / "adastra_script_values.txt"
COUNTRY_TYPES = ROOT / "ad_astra" / "common" / "country_types" / "adastra_country_types.txt"
ORIGIN = ROOT / "ad_astra" / "common" / "governments" / "civics" / "zzz_adastra_origins.txt"
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
    launcher_descriptor = LAUNCHER_DESCRIPTOR.read_text(encoding="utf-8-sig")
    script_values = SCRIPT_VALUES.read_text(encoding="utf-8-sig")
    country_types = COUNTRY_TYPES.read_text(encoding="utf-8-sig")
    origin = ORIGIN.read_text(encoding="utf-8-sig")
    if 'version="1.3.2"' not in descriptor:
        fail("le descripteur doit annoncer 1.3.2")
    if 'version="1.3.2"' not in launcher_descriptor:
        fail("le descripteur launcher doit annoncer 1.3.2")
    if len(re.findall(r"^tech_adastra_[a-z0-9_]+ = \{", techs, re.MULTILINE)) != 250:
        fail("le hotfix doit conserver les 250 technologies d'epoque de la 1.3")
    if "NOT = { has_country_flag = adastra_reached_" in techs:
        fail("une exclusion d'age est encore dans potential")
    if "has_country_flag = adastra_vague_" in techs:
        fail("une garde de vague peut encore invalider une recherche entre deux ages")
    if "# 1.3.1 : hors tirage apres l'age" in techs:
        fail("un weight_modifier 1.3.1 retire encore les technologies precedentes du tirage")
    if "pop_growth_speed" in techs:
        fail("une technologie utilise encore pop_growth_speed, ignore par Stellaris 4.4")
    if "NOR = {\n\t\t\t\tvalue = auth_hive_mind" in origin:
        fail("l origine utilise une forme NOR d autorite non validee par les origines vanilla")
    for authority in ("auth_hive_mind", "auth_machine_intelligence"):
        if f"NOT = {{ value = {authority} }}" not in origin:
            fail(f"l origine doit exclure explicitement {authority}")
    buildings = (ROOT / "ad_astra" / "common" / "buildings" /
                 "adastra_age_buildings.txt").read_text(encoding="utf-8-sig")
    if buildings.count("building_sets = {\n\t\turban\n\t}") != 11:
        fail("les onze batiments d'epoque doivent viser le set urban des zones de ville")
    if re.search(r"building_sets = \{\n\t\t(?:urban_automation|farming|mining|research|unity|industrial|factory|fortress|entertainment)", buildings):
        fail("un batiment d'epoque vise un set exclu par les zones urbaines de base")
    modifiers = (ROOT / "ad_astra" / "common" / "static_modifiers" /
                 "adastra_modifiers.txt").read_text(encoding="utf-8-sig")
    pre_manu = re.search(r"adastra_pre_manufacture = \{(.*?)^\}", modifiers,
                         re.MULTILINE | re.DOTALL)
    if not pre_manu or "consumer_goods_upkeep_mult" in pre_manu.group(1):
        fail("les multiplicateurs de biens de consommation plafonnes sont encore utilises")
    for key in ("planet_politicians_consumer_goods_upkeep_add",
                "planet_bureaucrats_consumer_goods_upkeep_add",
                "planet_entertainers_consumer_goods_upkeep_add"):
        if key not in pre_manu.group(1):
            fail(f"annulation forfaitaire manquante : {key}")
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
