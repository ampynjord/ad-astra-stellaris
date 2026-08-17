#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra - copie l'icone vanilla de chaque techno d'age sous notre nom.

Une technologie Stellaris n'a PAS de champ icon : le moteur cherche
    gfx/interface/icons/technologies/<cle_de_la_techno>.dds
Nos technos doivent donc embarquer un .dds portant leur propre nom. La table
ICONS de tools/age_techs_data.py dit de quelle icone du jeu de base on part.

    python3 tools/copy_tech_icons.py <dossier_icones_vanilla> [--out <dossier>]

Idempotent : recopie tout a chaque passage, ce qui rattrape aussi une icone
changee par une mise a jour du jeu.
"""
import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from age_techs_data import ICONS  # noqa: E402

DEFAULT_OUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "ad_astra", "gfx", "interface", "icons", "technologies")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_icons")
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    done, missing = 0, []
    for suffix, src_name in ICONS.items():
        src = os.path.join(args.vanilla_icons, "tech_%s.dds" % src_name)
        dst = os.path.join(args.out, "tech_adastra_%s.dds" % suffix)
        if not os.path.exists(src):
            missing.append((suffix, src_name))
            continue
        shutil.copyfile(src, dst)
        done += 1

    print("icones copiees : %d / %d" % (done, len(ICONS)))
    if missing:
        print("SOURCES INTROUVABLES :")
        for suffix, src in missing:
            print("   tech_adastra_%-28s <- tech_%s.dds" % (suffix, src))
    extra = [f for f in os.listdir(args.out)
             if f.endswith(".dds")
             and f[len("tech_adastra_"):-4] not in ICONS]
    if extra:
        print("ORPHELINES (techno supprimee ?) : %s" % ", ".join(sorted(extra)))


if __name__ == "__main__":
    main()
