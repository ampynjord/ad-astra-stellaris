#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere le correctif 1.3.2 des sets de batiments d'epoque."""

from pathlib import Path
import re
import sys


ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "ad_astra"
TARGET = ROOT / "common" / "buildings" / "adastra_age_buildings.txt"
BUILDING_SETS = re.compile(
    r"(building_adastra_[a-z_]+ = \{.*?\n\tbuilding_sets = \{)\n"
    r"(?:\t\t[^\n]+\n)+(\t\})",
    re.DOTALL,
)


def main():
    source = TARGET.read_text(encoding="utf-8-sig")
    fixed, count = BUILDING_SETS.subn(r"\1\n\t\turban\n\2", source)
    if count != 11:
        raise SystemExit(f"{count} ensembles remplaces au lieu de 11 attendus.")
    if fixed.count("building_sets = {\n\t\turban\n\t}") != 11:
        raise SystemExit("les onze batiments d'epoque doivent viser le set urban")
    TARGET.write_text(fixed, encoding="utf-8", newline="\n")
    print("11 sets de batiments d'epoque diriges vers les zones urbaines.")


if __name__ == "__main__":
    main()
