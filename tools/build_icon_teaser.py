#!/usr/bin/env python3
"""Compose une planche de teaser depuis les icones reellement livrees."""
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artwork" / "teasers" / "icon-palette-1.4.png"
WIDTH, HEIGHT = 1920, 1080


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "bahnschrift.ttf" if not bold else "bahnschrift.ttf"
    return ImageFont.truetype(Path("C:/Windows/Fonts") / name, size)


def load_icons(folder: Path) -> list[Image.Image]:
    return [Image.open(path).convert("RGBA") for path in sorted(folder.glob("*.dds"))]


def paste_grid(canvas: Image.Image, icons: list[Image.Image], origin: tuple[int, int],
               columns: int, cell: int, size: int) -> None:
    for index, icon in enumerate(icons):
        x = origin[0] + (index % columns) * cell + (cell - size) // 2
        y = origin[1] + (index // columns) * cell + (cell - size) // 2
        image = icon.copy()
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas.alpha_composite(image, (x + (size - image.width) // 2,
                                      y + (size - image.height) // 2))


def main() -> None:
    random.seed(140)
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), (3, 10, 19, 255))
    draw = ImageDraw.Draw(canvas)

    for _ in range(440):
        x, y = random.randrange(WIDTH), random.randrange(HEIGHT)
        r = random.choice((1, 1, 1, 2))
        tone = random.choice(((44, 137, 180, 130), (111, 198, 236, 150),
                              (255, 255, 255, 110)))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=tone)

    title = font(72, bold=True)
    subtitle = font(25)
    label = font(24, bold=True)
    small = font(19)
    draw.text((72, 54), "AD ASTRA", font=title, fill=(208, 246, 255, 255))
    draw.text((76, 138), "ICON OVERHAUL  /  1.4", font=subtitle,
              fill=(73, 210, 226, 255))
    draw.line((72, 183, 1848, 183), fill=(53, 150, 171, 180), width=2)

    techs = load_icons(ROOT / "ad_astra/gfx/interface/icons/technologies")
    decisions = load_icons(ROOT / "ad_astra/gfx/interface/icons/decisions")
    buildings = load_icons(ROOT / "ad_astra/gfx/interface/icons/buildings")

    draw.text((72, 225), "250 TECHNOLOGIES", font=label, fill=(202, 233, 241, 255))
    draw.text((72, 258), "From stone tools to the first steps beyond the sky.",
              font=small, fill=(113, 166, 185, 255))
    paste_grid(canvas, techs, (72, 300), columns=25, cell=50, size=42)

    x = 1360
    draw.text((x, 225), "14 DECISIONS", font=label, fill=(202, 233, 241, 255))
    draw.text((x, 258), "Programs that turn a world upward.", font=small,
              fill=(113, 166, 185, 255))
    paste_grid(canvas, decisions, (x, 300), columns=7, cell=64, size=54)

    draw.text((x, 530), "21 BUILDINGS", font=label, fill=(202, 233, 241, 255))
    draw.text((x, 563), "A civilization made visible on the ground.", font=small,
              fill=(113, 166, 185, 255))
    paste_grid(canvas, buildings, (x, 605), columns=6, cell=78, size=72)

    draw.text((72, 864), "285 ORIGINAL ICONS", font=font(35, bold=True),
              fill=(207, 244, 252, 255))
    draw.text((72, 912), "Technologies  •  Decisions  •  Buildings", font=font(26),
              fill=(89, 194, 212, 255))
    draw.text((72, 1004), "AD ASTRA  —  PRE-FTL ORIGIN FOR STELLARIS",
              font=font(20), fill=(116, 150, 166, 255))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUT, optimize=True)
    print(f"ecrit : {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
