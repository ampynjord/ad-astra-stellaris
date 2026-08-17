#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - applique tools/vanilla_tech_age_map.py aux fichiers d'override.

Les deux fichiers d'override de technos vanilla sont generes ailleurs
(gen_tier1_overrides.py pour le gros, ecriture manuelle historique pour les
technos de depart). Ce script ne fait qu'une chose : remplacer la garde d'age
du bloc de chaque techno listee dans TECH_AGE.

Idempotent : relancable sans risque, il resout toujours vers l'age de la table.

    python3 tools/apply_vanilla_tech_ages.py [racine_du_mod]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vanilla_tech_age_map import GATED_AGES, TECH_AGE  # noqa: E402

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ad_astra")

FILES = ["zzz_adastra_tech_overrides.txt", "zzz_adastra_tier1_overrides.txt"]
ANY_GATE = re.compile(r"adastra_vanilla_open_(%s) = yes" % "|".join(GATED_AGES))


def block_span(src, key):
    """Retourne (debut, fin) du bloc de premier niveau `key = { ... }`."""
    m = re.search(r"^%s\s*=\s*\{" % re.escape(key), src, re.M)
    if not m:
        return None
    depth, j, n = 1, m.end(), len(src)
    while j < n and depth:
        c = src[j]
        if c == "#":
            j = src.find("\n", j)
            if j == -1:
                j = n
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        j += 1
    return m.start(), j


def main():
    done, missing, unchanged = [], [], []
    for name in FILES:
        path = os.path.join(ROOT, "common", "technology", name)
        src = open(path, encoding="utf-8").read()
        changed = False
        for tech, (age, _why) in TECH_AGE.items():
            span = block_span(src, tech)
            if not span:
                continue
            s, e = span
            block = src[s:e]
            if not ANY_GATE.search(block):
                missing.append((tech, name, "aucune garde d'age dans le bloc"))
                continue
            new = ANY_GATE.sub("adastra_vanilla_open_%s = yes" % age, block)
            if new == block:
                unchanged.append((tech, age))
            else:
                done.append((tech, age, name))
                src = src[:s] + new + src[e:]
                changed = True
        if changed:
            open(path, "w", encoding="utf-8", newline="\n").write(src)

    seen = {t for t, _a, _f in done} | {t for t, _a in unchanged}
    for tech in TECH_AGE:
        if tech not in seen and not any(tech == m[0] for m in missing):
            missing.append((tech, "-", "bloc introuvable dans les overrides"))

    print("technos redatees : %d" % len(done))
    for tech, age, fname in sorted(done):
        print("   %-34s -> %-12s (%s)" % (tech, age, fname))
    if unchanged:
        print("deja a l'age voulu : %d" % len(unchanged))
        for tech, age in sorted(unchanged):
            print("   %-34s    %s" % (tech, age))
    if missing:
        print("A TRAITER : %d" % len(missing))
        for tech, fname, why in sorted(missing):
            print("   %-34s %s (%s)" % (tech, why, fname))


if __name__ == "__main__":
    main()
