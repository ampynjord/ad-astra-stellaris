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


def fail(message):
    print(f"ERREUR : {message}")
    raise SystemExit(1)


def main():
    techs = TECHS.read_text(encoding="utf-8-sig")
    events = EVENTS.read_text(encoding="utf-8-sig")
    descriptor = DESCRIPTOR.read_text(encoding="utf-8-sig")
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
    print("0 erreur : invariants 1.3.1 valides.")


if __name__ == "__main__":
    main()
