#!/usr/bin/env python3
"""Verifie que les sorties des generateurs internes sont a jour."""
import subprocess
import sys
from pathlib import Path


RACINE = Path(__file__).resolve().parent.parent
GENERATEURS = (
    "tools/gen_age_techs.py",
    "tools/gen_situation_progress.py",
    "tools/gen_age_buildings.py",
)
SORTIES = (
    "ad_astra/common/technology/adastra_age_techs.txt",
    "ad_astra/common/scripted_triggers/zz_adastra_age_gates.txt",
    "ad_astra/common/scripted_effects/zz_adastra_vagues.txt",
    "ad_astra/common/scripted_effects/zz_adastra_age_grants.txt",
    "ad_astra/common/situations/zzz_adastra_situations.txt",
    "ad_astra/common/buildings/adastra_age_buildings.txt",
    "ad_astra/common/buildings/zzz_adastra_capital.txt",
    "ad_astra/localisation/french/adastra_ages_l_french.yml",
    "ad_astra/localisation/english/adastra_ages_l_english.yml",
    "ad_astra/localisation/french/adastra_buildings_l_french.yml",
    "ad_astra/localisation/english/adastra_buildings_l_english.yml",
    "ad_astra/localisation/french/adastra_l_french.yml",
    "ad_astra/localisation/english/adastra_l_english.yml",
)


def lance(command):
    print("+", " ".join(command))
    subprocess.run(command, cwd=RACINE, check=True)


def main():
    # 18/08 : seuls ces generateurs n'ont pas besoin du vanilla local en CI.
    for generateur in GENERATEURS:
        lance([sys.executable, generateur])

    resultat = subprocess.run(
        ["git", "diff", "--exit-code", "--", *SORTIES], cwd=RACINE
    )
    if resultat.returncode:
        print("ERREUR : sorties generees desynchronisees ; regenerer puis versionner le diff.")
        return resultat.returncode

    print("sorties generees : a jour")
    return 0


if __name__ == "__main__":
    sys.exit(main())
