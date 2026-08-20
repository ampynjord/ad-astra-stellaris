#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genere les gardes technologiques des specialisations de district.

Une zone utilise potential pour etre affichee et unlock pour etre choisie.
Les deux doivent donc tester la technologie fondatrice.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402
from vanilla_zone_age_map import ZONE_AGE  # noqa: E402


INLINE_DIR = None


def expand_inline(block):
    """Developpe les inline scripts qui definissent potential ou unlock."""
    if not INLINE_DIR:
        return block

    def replace_inline(match):
        body = match.group(1)
        name = re.search(r"script\s*=\s*zones/(\w+)", body)
        if not name:
            return match.group(0)
        path = os.path.join(INLINE_DIR, name.group(1) + ".txt")
        if not os.path.exists(path):
            return match.group(0)
        content = open(path, encoding="utf-8-sig", errors="replace").read()
        if not re.search(r"^(potential|unlock)\s*=\s*\{", content, re.M):
            return match.group(0)
        for parameter in re.finditer(r"(\w+)\s*=\s*(\S+)", body):
            if parameter.group(1) != "script":
                content = content.replace("$%s$" % parameter.group(1), parameter.group(2))
        return "\n" + "\n".join("\t" + line if line.strip() else line for line in content.splitlines())

    return re.sub(r"\n\tinline_script = \{(.*?)\n\t\}", replace_inline, block, flags=re.S)


def guard(block_name, tech, why):
    return (
        "\t%s = { # portee planete\n" % block_name
        + "\t\t# Ad Astra : %s\n" % why
        + "\t\tOR = {\n"
        + "\t\t\tNOT = { exists = owner }\n"
        + "\t\t\towner = {\n"
        + "\t\t\t\tOR = {\n"
        + "\t\t\t\t\tNOT = { has_origin = origin_adastra }\n"
        + "\t\t\t\t\thas_country_flag = adastra_completed\n"
        + "\t\t\t\t\thas_technology = %s\n" % tech
        + "\t\t\t\t}\n"
        + "\t\t\t}\n"
        + "\t\t}\n"
    )


def inject(block, tech, why):
    """Ajoute une garde dans potential et unlock sans ecraser le vanilla."""
    block = expand_inline(block)
    for name in ("potential", "unlock"):
        match = re.search(r"^\t%s = \{" % name, block, re.M)
        if match:
            block = block[:match.start()] + guard(name, tech, why) + block[match.end():]
        else:
            head = block.index("{") + 1
            block = block[:head] + "\n" + guard(name, tech, why) + "\t}\n" + block[head:]
    return block


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vanilla_dir")
    parser.add_argument("--out", required=True)
    parser.add_argument("--inline", help="dossier common/inline_scripts/zones du jeu de base")
    args = parser.parse_args()
    global INLINE_DIR
    INLINE_DIR = args.inline

    todo = {name: value for name, value in ZONE_AGE.items() if value[0] not in ("na", "keep")}
    output = [
        "# Ad Astra 1.4 - technologies des specialisations de district (zones).",
        "# FICHIER GENERE PAR tools/gen_zone_age_overrides.py - NE PAS EDITER A LA MAIN.",
        "# Source de verite : tools/vanilla_zone_age_map.py",
        "#",
        "# Chaque specialisation depend de sa technologie fondatrice, pas seulement d'un age.",
        "",
    ]
    seen = []
    for filename in sorted(os.listdir(args.vanilla_dir)):
        if not filename.endswith(".txt"):
            continue
        source = open(os.path.join(args.vanilla_dir, filename), encoding="utf-8-sig", errors="replace").read()
        for name, start, end in top_level_blocks(source):
            if name not in todo:
                continue
            _age, tech, why = todo[name]
            output.extend(["", "### %s -> %s" % (name, tech), inject(source[start:end], tech, why)])
            seen.append(name)

    missing = sorted(set(todo) - set(seen))
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(output) + "\n")
    if missing:
        raise SystemExit("zones introuvables : %s" % ", ".join(missing))
    print("zones regenerees : %d" % len(seen))


if __name__ == "__main__":
    main()
