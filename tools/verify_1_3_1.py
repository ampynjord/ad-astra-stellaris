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
ORIGIN = ROOT / "ad_astra" / "common" / "governments" / "civics" / "zzz_adastra_origins.txt"
ZONES = ROOT / "ad_astra" / "common" / "zones" / "zzz_adastra_zone_ages.txt"
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
    origin = ORIGIN.read_text(encoding="utf-8-sig")
    zones = ZONES.read_text(encoding="utf-8-sig")
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
    starting_state = events.index("# 1.3.2 : un country_event ne s'execute pas dans cette pile.")
    if not grants < starting_state < capital:
        fail("l etat de l age choisi doit etre pose avant la capitale")
    if "else_if = { limit = { has_country_flag = adastra_choice_bronze } country_event = { id = adastra.41 } }" in events:
        fail("le demarrage ne doit plus mettre l age choisi en file d evenement")
    for fragment in (
        "add_zone = { district = district_city zone = zone_industrial zone_slot = 1 }",
        "building = building_factory_1",
        "add_zone = { district = district_city zone = zone_research_unity zone_slot = 2 }",
        "building = building_research_lab_1",
        "while = { count = 2 add_district = district_generator }",
    ):
        if fragment not in events:
            fail(f"reconstruction economique absente : {fragment}")
    early_archives = re.compile(
        r"else_if = \{\s*limit = \{ owner = \{ OR = \{ has_country_flag = adastra_choice_bronze.*?"
        r"add_zone = \{ district = district_city zone = zone_research_unity zone_slot = 2 \}",
        re.DOTALL,
    )
    if early_archives.search(events):
        fail("les depart Bronze a Renaissance ne doivent pas recevoir d Archives gratuitement")
    if re.search(r"\b(if|limit)\s*=", script_values):
        fail("script_values contient une syntaxe CK3 invalide")
    zone_techs = {
        "zone_research_unity": "tech_adastra_writing",
        "zone_research": "tech_adastra_scholasticism",
        "zone_research_physics": "tech_adastra_experimental_method",
        "zone_research_society": "tech_adastra_experimental_method",
        "zone_research_engineering": "tech_adastra_experimental_method",
        "zone_unity": "tech_adastra_law",
        "zone_unity_spiritualist": "tech_adastra_priesthood",
        "zone_fortress": "tech_adastra_standing_army",
        "zone_trade": "tech_adastra_coinage",
        "zone_industrial": "tech_adastra_steam_engine",
        "zone_factory": "tech_adastra_assembly_line",
        "zone_foundry": "tech_adastra_bessemer",
    }
    if "has_country_flag = adastra_reached_" in zones:
        fail("une specialisation depend encore directement d un age au lieu de sa technologie")
    for zone, tech in zone_techs.items():
        header = f"### {zone} -> {tech}"
        if header not in zones:
            fail(f"specialisation sans technologie fondatrice : {zone}")
        block = re.search(rf"{re.escape(header)}\n({re.escape(zone)} = \{{.*?\n\}})", zones, re.DOTALL)
        if not block or block.group(1).count(f"has_technology = {tech}") != 2:
            fail(f"garde potential/unlock invalide pour : {zone}")
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
