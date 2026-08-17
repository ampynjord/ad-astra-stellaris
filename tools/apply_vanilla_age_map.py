#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - applique tools/vanilla_age_map.py au mod.

1. Recale la garde de chaque techno vanilla de depart sur l'age de sa decouverte
   reelle (adastra_vanilla_open_<age> = yes).
2. Recale les octrois automatiques (give_technology) des events d'age sur la
   politique GRANT de la carte : plus rien d'offert avant l'Age spatial, pour que
   les technos d'epoque passent bien AVANT le vanilla du meme age.

Idempotent : relancable sans risque.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vanilla_age_map import VANILLA_AGE_MAP, AGE_EVENTS  # noqa: E402
from clausewitz import top_level_blocks  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ad_astra")
OVERRIDES = os.path.join(ROOT, "common", "technology", "zzz_adastra_tech_overrides.txt")
EVENTS = os.path.join(ROOT, "events", "adastra_events.txt")



# ------------------------------------------------------------ 1) les gardes
src = open(OVERRIDES, encoding="utf-8").read()
changes, unknown = [], []
for key, start, end in reversed(top_level_blocks(src)):
    if key not in VANILLA_AGE_MAP:
        unknown.append(key)
        continue
    age, _grant = VANILLA_AGE_MAP[key]
    block = src[start:end]
    if age == "ftl":
        continue
    want = "adastra_vanilla_open_%s = yes" % age
    cur = re.search(r"adastra_vanilla_open_(\w+) = yes", block)
    if not cur:
        continue
    if cur.group(1) != age:
        changes.append("%s : %s -> %s" % (key, cur.group(1), age))
        block = block.replace(cur.group(0), want)
        src = src[:start] + block + src[end:]
open(OVERRIDES, "w", encoding="utf-8", newline="\n").write(src)

print("== gardes des technos vanilla de depart ==")
for c in changes:
    print("  deplace  " + c)
if not changes:
    print("  aucune modification (deja aligne)")
if unknown:
    print("  ABSENTES DE LA CARTE : %s" % ", ".join(unknown))

# ------------------------------------------------- 2) les octrois d'age
lines = open(EVENTS, encoding="utf-8").read().split("\n")
grants_by_age = {}
for tech, (age, grant) in VANILLA_AGE_MAP.items():
    if grant:
        grants_by_age.setdefault(age, []).append(tech)
# ordre stable : celui de la carte
order = list(VANILLA_AGE_MAP)
for age in grants_by_age:
    grants_by_age[age].sort(key=order.index)

# On ne vise que les DEFINITIONS d'event : une ligne dont l'id est le seul
# contenu. Les appels (country_event = { id = adastra.4X }) portent l'id sur une
# ligne qui contient aussi country_event, et doivent etre ignores.
targets = []
for i, line in enumerate(lines):
    m = re.match(r"\s*id = adastra\.(4\d)\s*$", line)
    if m:
        targets.append((i, AGE_EVENTS[int(m.group(1))]))
if len(targets) != len(AGE_EVENTS):
    sys.exit("ERREUR : %d definitions d'event d'age trouvees, %d attendues"
             % (len(targets), len(AGE_EVENTS)))

print("\n== octrois automatiques par age ==")
report = []
for idx, age in reversed(targets):
    start = idx
    while start >= 0 and "country_event = {" not in lines[start]:
        start -= 1
    depth, end = 0, start
    for j in range(start, len(lines)):
        body = lines[j].split("#", 1)[0]
        depth += body.count("{") - body.count("}")
        if depth == 0 and j > start:
            end = j
            break
    before = sum(1 for j in range(start, end + 1) if "give_technology" in lines[j])
    block = [l for l in lines[start:end + 1] if "give_technology" not in l]
    wanted = grants_by_age.get(age, [])
    if wanted:
        anchor = next((k for k, l in enumerate(block)
                       if "set_country_flag = adastra_reached_%s" % age in l), None)
        if anchor is None:
            print("  ANCRE INTROUVABLE pour l'age %s" % age)
        else:
            indent = re.match(r"\s*", block[anchor]).group(0)
            ins = ["%sgive_technology = { tech = %s message = no }" % (indent, t)
                   for t in wanted]
            block = block[:anchor + 1] + ins + block[anchor + 1:]
    lines[start:end + 1] = block
    report.append((age, before, len(wanted)))

open(EVENTS, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
for age, before, after in reversed(report):
    flag = "" if before == after else "   <-- change"
    print("  %-12s %2d -> %2d octroi(s)%s" % (age, before, after, flag))
print("\nOK")
