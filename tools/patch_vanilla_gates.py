#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - bascule les gardes des overrides de techs vanilla depuis le
drapeau brut d'age vers le declencheur adastra_vanilla_open_<age>, qui exige en
plus que les 5 techs custom de l'age soient terminees.

Idempotent : relancable sans risque.
Ne touche PAS adastra_unlock_ftl (pose par la decision de phase 3, pas par un age).

ATTENTION, 16/08 : les technos de PALIER 2 de zzz_adastra_tier1_overrides.txt ne
doivent PAS recevoir adastra_vanilla_open_space. Ce declencheur accepte le
drapeau adastra_vanilla_gift_space, pose des l'arrivee a l'Age spatial pour
livrer le paquet de seize technos de vaisseau - et il ouvrait du meme coup les
161 technos de palier 2. Six d'entre elles suffisaient a ouvrir le palier 3, ou
se trouvent la terraformation et les cuirassiers. Retour de cooldude808.

Elles portent desormais « has_country_flag = adastra_completed » : le palier 2
attend l'emergence, et le palier 3 - qui exige six technos de palier 2 deja
cherchees - ne s'ouvre jamais pendant le confinement.

Si ce script est relance apres une regeneration, il faut REAPPLIQUER cette
distinction : voir la fonction de garde par palier dans gen_tier1_overrides.py.
"""
import os
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ad_astra")

AGES = ["renaissance", "steam", "industrial", "machine", "atomic", "space"]
FILES = ["zzz_adastra_tech_overrides.txt", "zzz_adastra_tier1_overrides.txt"]

total = 0
for name in FILES:
    path = os.path.join(ROOT, "common", "technology", name)
    with open(path, encoding="utf-8") as f:
        src = f.read()
    n = 0
    for age in AGES:
        old = "has_country_flag = adastra_unlock_%s\n" % age
        new = "adastra_vanilla_open_%s = yes\n" % age
        n += src.count(old)
        src = src.replace(old, new)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    print("  %-38s %3d garde(s) basculee(s)" % (name, n))
    total += n

leftovers = []
for name in FILES:
    with open(os.path.join(ROOT, "common", "technology", name), encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if "has_country_flag = adastra_unlock_" in line and "ftl" not in line:
                leftovers.append("%s:%d %s" % (name, i, line.strip()))
print("total : %d" % total)
if leftovers:
    print("RESTES A TRAITER :")
    for l in leftovers:
        print("   " + l)
else:
    print("aucun drapeau d'age brut restant (hors adastra_unlock_ftl, normal)")
