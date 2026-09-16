#!/usr/bin/env python3
"""Genere les illustrations d'evenements Ad Astra depuis leurs sources PNG."""
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "artwork" / "event_pictures"
DESTINATION = ROOT / "ad_astra" / "gfx" / "event_pictures"
GFX_DESTINATION = ROOT / "ad_astra" / "interface" / "adastra_event_pictures.gfx"
TAILLE = (450, 150)

def main() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    sources = sorted(SOURCES.glob("adastra_*.png"))
    if not sources:
        raise FileNotFoundError(f"Aucune source dans : {SOURCES}")
    sprites = []
    for source in sources:
        nom = source.stem
        # Le cadrage est volontairement panoramique, comme les event pictures vanilla.
        image = Image.open(source).convert("RGB")
        image = ImageOps.fit(image, TAILLE, Image.Resampling.LANCZOS)
        cible = DESTINATION / f"{nom}.dds"
        image.save(cible, "DDS")
        print(f"ecrit : {cible.relative_to(ROOT)}")
        sprites.append(
            "\tspriteType = {\n"
            f"\t\tname = \"GFX_evt_{nom}\"\n"
            f"\t\ttexturefile = \"gfx/event_pictures/{nom}.dds\"\n"
            "\t\tmasking_texture = \"gfx/interface/situation_log/event_mask.dds\"\n"
            "\t\talwaystransparent = yes\n"
            "\t}\n"
        )
    GFX_DESTINATION.write_text("spriteTypes = {\n" + "".join(sprites) + "}\n", encoding="utf-8")
    print(f"ecrit : {GFX_DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
