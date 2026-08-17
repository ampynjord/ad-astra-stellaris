#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - applique tools/vanilla_zone_age_map.py.

Une zone se controle par DEUX blocs, tous deux en portee planete :
  potential : la zone est-elle proposee dans la liste des specialisations
  unlock    : peut-on la choisir maintenant
On garde les deux, sinon la zone reste visible et cliquable.

    python3 tools/gen_zone_age_overrides.py <dossier_vanilla_zones> --out <fichier>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402
from vanilla_zone_age_map import ZONE_AGE  # noqa: E402



INLINE_DIR = None   # rempli depuis la ligne de commande


def expand_inline(block):
    """Developpe les inline_script de zones qui definissent potential/unlock.

    Sans ca, la garde qu'on ajoute est ecrite AVANT le script partage, et c'est
    le potential du jeu de base qui gagne : le verrou ne s'applique pas. On
    remplace donc l'appel par son contenu, parametres substitues."""
    if not INLINE_DIR:
        return block

    def repl(m):
        body = m.group(1)
        name = re.search(r"script\s*=\s*zones/(\w+)", body)
        if not name:
            return m.group(0)
        path = os.path.join(INLINE_DIR, name.group(1) + ".txt")
        if not os.path.exists(path):
            return m.group(0)
        content = open(path, encoding="utf-8-sig", errors="replace").read()
        if not re.search(r"^(potential|unlock)\s*=\s*\{", content, re.M):
            return m.group(0)          # rien a fusionner, on laisse l'appel
        for pm in re.finditer(r"(\w+)\s*=\s*(\S+)", body):
            if pm.group(1) == "script":
                continue
            content = content.replace("$%s$" % pm.group(1), pm.group(2))
        return "\n" + "\n".join("\t" + l if l.strip() else l for l in content.splitlines())

    return re.sub(r"\n\tinline_script = \{(.*?)\n\t\}", repl, block, flags=re.S)


def guard(block_name, age, why):
    return (
        "\t%s = { # portee planete\n" % block_name +
        "\t\t# Ad Astra : %s\n" % why +
        "\t\tOR = {\n"
        "\t\t\tNOT = { exists = owner }\n"
        "\t\t\towner = {\n"
        "\t\t\t\tOR = {\n"
        "\t\t\t\t\tNOT = { has_origin = origin_adastra }\n"
        "\t\t\t\t\thas_country_flag = adastra_completed\n"
        "\t\t\t\t\thas_country_flag = adastra_reached_%s\n" % age +
        "\t\t\t\t}\n"
        "\t\t\t}\n"
        "\t\t}\n")


def inject(block, age, why):
    """Ajoute la garde dans potential et dans unlock, en les creant au besoin."""
    block = expand_inline(block)
    added = 0
    for name in ("potential", "unlock"):
        m = re.search(r"^\t%s = \{" % name, block, re.M)
        if m:
            block = block[:m.start()] + guard(name, age, why) + block[m.end():]
        else:
            head = block.index("{") + 1
            block = block[:head] + "\n" + guard(name, age, why) + "\t}\n" + block[head:]
        added += 1
    return block, added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_dir")
    ap.add_argument("--out", required=True)
    ap.add_argument("--inline", help="dossier common/inline_scripts/zones du jeu de base")
    args = ap.parse_args()
    global INLINE_DIR
    INLINE_DIR = args.inline

    todo = {k: v for k, v in ZONE_AGE.items() if v[0] not in ("na", "keep")}
    out = ["# Ad Astra 1.2 - age des specialisations de district (zones).",
           "# FICHIER GENERE PAR tools/gen_zone_age_overrides.py - NE PAS EDITER A LA MAIN.",
           "# Source de verite : tools/vanilla_zone_age_map.py",
           "#",
           "# Le jeu de base ne gate presque pas les zones : un empire a l'Age de pierre",
           "# pouvait specialiser son district en Industrie lourde. Chaque zone recoit",
           "# ici l'age de la techno d'epoque equivalente.",
           ""]
    seen = []
    files = args.vanilla_dir
    for fname in sorted(os.listdir(files)):
        if not fname.endswith(".txt"):
            continue
        src = open(os.path.join(files, fname), encoding="utf-8-sig", errors="replace").read()
        for name, s, e in top_level_blocks(src):
            if name not in todo:
                continue
            age, why = todo[name]
            block, _ = inject(src[s:e], age, why)
            out.append("")
            out.append("### %s -> %s" % (name, age))
            out.append(block)
            seen.append((name, age))

    missing = sorted(set(todo) - {n for n, _a in seen})
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    from collections import Counter
    print("zones recalees : %d" % len(seen))
    for a, n in sorted(Counter(a for _n, a in seen).items()):
        print("   %-12s %d" % (a, n))
    keep = [k for k, v in ZONE_AGE.items() if v[0] == "keep"]
    na = [k for k, v in ZONE_AGE.items() if v[0] == "na"]
    print("laissees libres : %d | non touchees : %d" % (len(keep), len(na)))
    if missing:
        print("INTROUVABLES : %s" % ", ".join(missing))
    print("ecrit : %s" % args.out)


if __name__ == "__main__":
    main()
