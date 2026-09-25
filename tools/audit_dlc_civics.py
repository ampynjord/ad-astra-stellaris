#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit des civiques et origines du jeu de base face a l'economie pre-PRL.

Un empire Ad Astra n'a ni energie avant l'electricite, ni alliages avant le
bronze, ni biens de consommation avant la vapeur, ni vaisseaux ni base
stellaire avant l'Age spatial. Un civique qui paie ou produit ces ressources
des le premier jour peut rendre la partie impossible (Tankbound, signale le
25/09). Ce script liste, pour chaque civique et origine du jeu de base, les
indices d'un tel conflit, pour qu'on les tranche un par un.

Il ne decide rien et n'ecrit rien dans le mod : il produit un rapport.

    python tools/audit_dlc_civics.py "<Stellaris>/common" [--sortie rapport.md]
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Indice -> raison lisible. L'ordre compte peu : un civique cumule ses raisons.
INDICES = [
    (r"automated", "emplois automatises (entretien en energie)"),
    (r"\benergy\b|energy_", "energie"),
    (r"\balloys\b|alloys_", "alliages"),
    (r"consumer_goods", "biens de consommation"),
    (r"district_generator|energy_districts", "districts generateurs"),
    (r"(^|_)ship|starbase|fleet|naval", "vaisseaux, flotte ou base stellaire"),
    (r"robot|droid|synth", "robots"),
    (r"add_building", "batiments de depart"),
    (r"country_type", "type de pays"),
]


def lire(chemin):
    return open(chemin, encoding="utf-8-sig", errors="replace").read()


def exclusions_origine():
    """Civiques deja ecartes par le possible de l'origine Ad Astra."""
    chemin = os.path.join(RACINE, "ad_astra", "common", "governments", "civics",
                          "zzz_adastra_origins.txt")
    texte = lire(chemin)
    return set(re.findall(r"value = (civic_\w+)", texte))


def scripts_de_depart(common):
    """Scripts inline de debut de partie propres a un civique ou une origine."""
    out = {}
    for p in glob.glob(os.path.join(common, "inline_scripts", "game_start", "*.txt")):
        out[os.path.splitext(os.path.basename(p))[0]] = lire(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("common", help="dossier common/ du jeu de base")
    ap.add_argument("--sortie", help="fichier Markdown a ecrire (sinon stdout)")
    args = ap.parse_args()

    exclus = exclusions_origine()
    departs = scripts_de_depart(args.common)
    lignes = ["# Audit des civiques et origines face a l'economie pre-PRL", "",
              "Genere par tools/audit_dlc_civics.py. Un indice n'est pas un verdict : "
              "chaque ligne est a trancher (autoriser, adapter ou interdire).", "",
              "| Civique / origine | Jouable avec | Indices | Deja ecarte |",
              "|---|---|---|---|"]
    total = 0
    for p in sorted(glob.glob(os.path.join(args.common, "governments", "civics", "*.txt"))):
        texte = lire(p)
        for nom, s, e in top_level_blocks(texte):
            if nom.startswith("@"):
                continue
            bloc = texte[s:e]
            if "is_origin = yes" in bloc:
                # Ad Astra EST l'origine : les autres origines ne se cumulent pas.
                continue
            if nom.startswith(("civic_hive_", "civic_machine_")):
                # Ruche ou machine : l'origine Ad Astra exclut deja ces autorites.
                continue
            m = re.search(r"playable\s*=\s*\{([^}]*)\}", bloc)
            jouable = " ".join(m.group(1).split()) if m else "toujours"
            if "always = no" in jouable:
                continue
            corps = re.sub(r"#[^\n]*", "", bloc)
            # modifier = { ... } et effets de depart propres au civique
            zones = " ".join(re.findall(r"modifier\s*=\s*\{[^}]*\}", corps))
            zones += " " + departs.get(nom, "")
            raisons = [r for motif, r in INDICES if re.search(motif, zones)]
            if not raisons:
                continue
            total += 1
            lignes.append("| `%s` | %s | %s | %s |" % (
                nom, jouable.replace("|", "/"), ", ".join(raisons),
                "oui" if nom in exclus else ""))
    lignes += ["", "%d civiques a examiner." % total]
    rapport = "\n".join(lignes) + "\n"
    if args.sortie:
        open(args.sortie, "w", encoding="utf-8", newline="\n").write(rapport)
        print("ecrit : %s (%d civiques)" % (args.sortie, total))
    else:
        sys.stdout.write(rapport)


if __name__ == "__main__":
    main()
