#!/usr/bin/env python3
"""Genere les icones Ad Astra depuis les sources artistiques conservees.

Les PNG haute definition vivent hors du dossier du mod afin que les DDS livres
soient reproductibles. Les cadres de decisions sont appliques ici : ils restent
identiques, sans dupliquer un asset vanilla.
"""
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artwork" / "icon_sources" / "decisions"
DESTINATION = ROOT / "ad_astra" / "gfx" / "interface" / "icons" / "decisions"
BUILDING_SOURCE = ROOT / "artwork" / "icon_sources" / "buildings"
BUILDING_DESTINATION = ROOT / "ad_astra" / "gfx" / "interface" / "icons" / "buildings"
TECHNOLOGY_SOURCE = ROOT / "artwork" / "icon_sources" / "technologies"
TECHNOLOGY_DESTINATION = ROOT / "ad_astra" / "gfx" / "interface" / "icons" / "technologies"

# Nom de fichier source, nom d'icone employe dans common/decisions.
DECISIONS = {
    "decision_adastra_explore": "explore.png",
    "decision_adastra_starbase": "starbase.png",
    "decision_adastra_hyperdrive": "hyperdrive.png",
    "decision_adastra_navy": "navy.png",
    "decision_adastra_campaign_harvest": "campaign_harvest.png",
    "decision_adastra_campaign_mining": "campaign_mining.png",
    "decision_adastra_campaign_fuel": "campaign_fuel.png",
    "decision_adastra_campaign_industry": "campaign_industry.png",
    "decision_adastra_colony": "colony.png",
}

DECISION_SIZE = 45
BUILDING_SIZE = 78
TECHNOLOGY_SIZE = 52
FRAME = (48, 91, 80, 255)
CORNER = (117, 240, 214, 255)


def build_decision(source: Path) -> Image.Image:
    """Reduit une source et pose le liseret commun des decisions."""
    image = Image.open(source).convert("RGBA")
    image = image.resize((DECISION_SIZE, DECISION_SIZE), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, DECISION_SIZE - 1, DECISION_SIZE - 1), outline=FRAME)
    for point in ((0, 0), (DECISION_SIZE - 1, 0), (0, DECISION_SIZE - 1),
                  (DECISION_SIZE - 1, DECISION_SIZE - 1)):
        draw.point(point, fill=CORNER)
    return image


BUILDINGS = {
    "building_adastra_cave": "cave.png",
    "building_adastra_granary": "granary.png",
    "building_adastra_foundry": "foundry.png",
    "building_adastra_tablet_house": "tablet_house.png",
    "building_adastra_courthouse": "courthouse.png",
    "building_adastra_mill": "mill.png",
    "building_adastra_citadel": "citadel.png",
    "building_adastra_university": "university.png",
    "building_adastra_manufactory": "manufactory.png",
    "building_adastra_radio": "radio.png",
    "building_adastra_school": "school.png",
}


def build_building(source: Path) -> Image.Image:
    """Cadre un batiment transparent sans lui imposer une vue isometrique."""
    image = Image.open(source).convert("RGBA")
    box = image.getchannel("A").getbbox()
    if not box:
        raise ValueError(f"Alpha vide : {source}")
    image = image.crop(box)
    image.thumbnail((BUILDING_SIZE - 4, BUILDING_SIZE - 4), Image.Resampling.LANCZOS)
    result = Image.new("RGBA", (BUILDING_SIZE, BUILDING_SIZE), (0, 0, 0, 0))
    result.alpha_composite(image, ((BUILDING_SIZE - image.width) // 2,
                                   BUILDING_SIZE - image.height - 1))
    return result


def build_technology(source: Path) -> Image.Image:
    """Reduit une technologie opaque en conservant sa vignette sombre."""
    image = Image.open(source).convert("RGB")
    return image.resize((TECHNOLOGY_SIZE, TECHNOLOGY_SIZE), Image.Resampling.LANCZOS)


def main() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for icon, filename in DECISIONS.items():
        source = SOURCE / filename
        if not source.is_file():
            raise FileNotFoundError(f"Source manquante : {source}")
        target = DESTINATION / f"{icon}.dds"
        build_decision(source).save(target, "DDS")
        print(f"ecrit : {target.relative_to(ROOT)}")
    BUILDING_DESTINATION.mkdir(parents=True, exist_ok=True)
    for icon, filename in BUILDINGS.items():
        source = BUILDING_SOURCE / filename
        if not source.is_file():
            raise FileNotFoundError(f"Source manquante : {source}")
        target = BUILDING_DESTINATION / f"{icon}.dds"
        build_building(source).save(target, "DDS")
        print(f"ecrit : {target.relative_to(ROOT)}")
    if TECHNOLOGY_SOURCE.is_dir():
        TECHNOLOGY_DESTINATION.mkdir(parents=True, exist_ok=True)
        for source in sorted(TECHNOLOGY_SOURCE.glob("*.png")):
            target = TECHNOLOGY_DESTINATION / f"tech_adastra_{source.stem}.dds"
            build_technology(source).save(target, "DDS")
            print(f"ecrit : {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
