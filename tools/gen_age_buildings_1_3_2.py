#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le correctif 1.3.2 des sets de batiments d'epoque."""

from pathlib import Path
import re
import sys


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "ad_astra"
TARGET = ROOT / "common" / "buildings" / "adastra_age_buildings.txt"
GOVERNMENT_SET = re.compile(r"(building_sets = \{\s*\t\t)government\b")


def main():
    source = TARGET.read_text(encoding="utf-8-sig")
    fixed, count = GOVERNMENT_SET.subn(r"\1urban_automation", source)
    if count not in (0, 11):
        raise SystemExit(f"{count} sets government remplaces au lieu de 11 attendus.")
    if "building_sets = {\n\t\tgovernment" in fixed:
        raise SystemExit("un batiment d'epoque conserve le set government")
    if fixed.count("urban_automation") != 11:
        raise SystemExit("les onze batiments d'epoque doivent viser les zones urbaines")
    TARGET.write_text(fixed, encoding="utf-8", newline="\n")
    print("11 sets de batiments d'epoque diriges vers les zones urbaines.")


if __name__ == "__main__":
    main()
