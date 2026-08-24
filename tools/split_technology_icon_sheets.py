#!/usr/bin/env python3
"""Decoupe les planches source en icones de technologies independantes.

Les planches sont des sources artistiques. Les PNG individuels obtenus ici sont
ensuite convertis en DDS par build_custom_icons.py. Ne jamais modifier les DDS
a la main.
"""
from pathlib import Path
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from age_techs_data import TECHS  # noqa: E402

SHEETS = ROOT / "artwork" / "icon_sources" / "sheets"
OUTPUT = ROOT / "artwork" / "icon_sources" / "technologies"
EXISTING = {
    "fire", "stone_tools", "hunting", "cave_art", "language",
    "agriculture", "pottery", "bronze", "writing", "first_city",
}
GRID = 4


def missing_keys():
    """Rend les cles qui etaient historiquement des copies vanilla."""
    return [
        tech["key"].removeprefix("tech_adastra_")
        for technologies in TECHS.values()
        for tech in technologies
        if tech["key"].removeprefix("tech_adastra_") not in EXISTING
    ]


def main():
    keys = missing_keys()
    if len(keys) % (GRID * GRID):
        raise ValueError("Le nombre de technologies doit remplir les planches")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for sheet_index in range(len(keys) // (GRID * GRID)):
        source = SHEETS / ("tech_%02d.png" % (sheet_index + 1))
        if not source.is_file():
            raise FileNotFoundError("Planche manquante : %s" % source)
        image = Image.open(source).convert("RGB")
        if image.width != image.height:
            raise ValueError("Planche non carree : %s : %s" % (source, image.size))
        # Le moteur d'image peut rendre 1024 ou 1254 pixels. On normalise ici
        # avant le decoupage pour conserver quatre cellules strictement egales.
        if image.size != (1024, 1024):
            image = image.resize((1024, 1024), Image.Resampling.LANCZOS)
        cell = image.width // GRID
        batch = keys[sheet_index * GRID * GRID:(sheet_index + 1) * GRID * GRID]
        for index, key in enumerate(batch):
            x, y = (index % GRID) * cell, (index // GRID) * cell
            image.crop((x, y, x + cell, y + cell)).save(OUTPUT / (key + ".png"))
            print("ecrit : artwork/icon_sources/technologies/%s.png" % key)


if __name__ == "__main__":
    main()
