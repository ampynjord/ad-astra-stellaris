#!/usr/bin/env python3
"""Extrait les preuves d'une partie solo Ad Astra sans modifier la sauvegarde."""

import argparse
import json
import re
from pathlib import Path
from zipfile import BadZipFile, ZipFile


def bloc(texte, cle, profondeur):
    # Les sauvegardes texte de Stellaris alignent les accolades sur leur cle.
    indent = "\t" * profondeur
    motif = rf"^{indent}{re.escape(cle)}=[ \t]*\n{indent}\{{\n(.*?)^{indent}\}}[ \t]*$"
    match = re.search(motif, texte, re.M | re.S)
    return match.group(1) if match else ""


def valeur(texte, cle, profondeur=0):
    indent = "\t" * profondeur
    match = re.search(rf"^{indent}{re.escape(cle)}=([^\n]+)$", texte, re.M)
    return match.group(1).strip().strip('"') if match else None


def inspecter(sauvegarde):
    with ZipFile(sauvegarde) as archive:
        meta = archive.read("meta").decode("utf-8-sig")
        etat = archive.read("gamestate").decode("utf-8-sig")

    joueurs = re.findall(r"^\t\tcountry=(\d+)$", bloc(etat, "player", 0), re.M)
    if len(joueurs) != 1:
        raise ValueError("une sauvegarde solo avec un seul pays joueur est requise")
    joueur = joueurs[0]
    pays = bloc(bloc(etat, "country", 0), joueur, 1)
    if not pays:
        raise ValueError("pays joueur absent de la sauvegarde")
    flags = set(re.findall(r"^\t{3}(\w+)=", bloc(pays, "flags", 2), re.M))

    situations = bloc(bloc(etat, "situations", 0), "situations", 1)
    progression = None
    for identifiant in re.findall(r"^\t{2}(\d+)=", situations, re.M):
        situation = bloc(situations, identifiant, 2)
        if valeur(situation, "country", 3) == joueur and valeur(
            situation, "type", 3
        ) == "situation_adastra_ascension":
            progression = valeur(situation, "progress", 3)
            break

    return {
        "stellaris": valeur(meta, "version"),
        "date": valeur(meta, "date"),
        "pays_joueur": int(joueur),
        "mods": re.findall(r'^\t"([^"]+)"', bloc(meta, "mods", 0), re.M),
        "sauvegarde_marquee_triche": valeur(etat, "cheated_on_save"),
        "progression_ascension": progression,
        "lancement_suborbital": "core_suborbital_fait" in flags,
        "jalons": {
            nom: f"core_{nom}_fait" in flags
            for nom in (
                "suborbital",
                "satellite",
                "vol_habite",
                "premier_corps",
                "sonde_profonde",
            )
        },
        "etapes": sorted(f for f in flags if f.startswith("adastra_stage_")),
        "emergence": "adastra_completed" in flags,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sauvegarde", type=Path)
    args = parser.parse_args()
    try:
        preuves = inspecter(args.sauvegarde)
    except (OSError, BadZipFile, KeyError, ValueError) as erreur:
        parser.exit(2, f"Lecture impossible : {erreur}\n")
    print(json.dumps(preuves, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
