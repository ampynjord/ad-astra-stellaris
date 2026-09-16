#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra - surcharge des designations de colonie vanilla.

DEUX PROBLEMES, UN SEUL FICHIER DE SORTIE
    1. Retour Sithiya (Workshop, 13/08) : cinq designations de capitale
       exigent « is_country_type = default » ; un empire confine
       (adastra_grounded) n'y avait acces a aucune. On ELARGIT la
       condition, on ne la remplace jamais.
    2. Retour ampynjord (31/08) : avant l'emergence, TOUTES les
       designations vanilla restaient selectionnables a la main alors que
       seule la designation d'epoque (col_pre_ftl_*) a un sens. On
       VERROUILLE : chaque designation vanilla recoit dans son potential
       une garde qui l'ecarte tant que l'empire est confine
       (drapeau adastra_locked). A l'emergence le drapeau tombe et le
       nuancier vanilla revient de lui-meme.

    Les 10 col_pre_ftl_* sont EXCLUES d'ici : elles sont surchargees par
    zzz_adastra_preftl_colony_types.txt (elargies a notre type), et ce
    fichier-ci se charge apres lui - le re-emettre ici l'ecraserait.

    Une designation vanilla sans bloc potential en recoit un, reduit a la
    garde : sans cela elle resterait toujours valide.

    python3 tools/gen_colony_type_overrides.py <fichier_vanilla> --out <fichier>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402

# Designations a elargir (probleme 1). Les variantes ruche et machine sont
# volontairement absentes : l'origine est reservee aux empires reguliers.
A_ELARGIR = [
    "col_capital",
    "col_capital_foundry",
    "col_capital_factory",
    "col_capital_trade",
    "col_capital_extraction",
]

CIBLE = "is_country_type = default"
REMPLACEMENT = "OR = { is_country_type = default  is_country_type = adastra_grounded }"

# Garde du verrou (probleme 2). owner? : un monde sans proprietaire ne
# matche pas, la garde passe.
GARDE = ("NOT = { owner? = { is_country_type = adastra_grounded "
         "has_country_flag = adastra_locked } }")


def poser_garde(nom, bloc):
    """Insere la garde en tete du potential (cree le potential s'il manque)."""
    m = re.search(r"(\n\tpotential\s*=\s*\{)", bloc)
    if m:
        return bloc[:m.end()] + "\n\t\t" + GARDE + bloc[m.end():]
    # pas de potential : la designation etait valide partout - on en pose un
    m = re.search(r"\A\s*" + re.escape(nom) + r"\s*=\s*\{", bloc)
    if not m:
        raise SystemExit("%s : tete de bloc introuvable" % nom)
    return (bloc[:m.end()] + "\n\tpotential = {\n\t\t" + GARDE + "\n\t}"
            + bloc[m.end():])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_file")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    src = open(args.vanilla_file, encoding="utf-8-sig", errors="replace").read()
    out = ["# Ad Astra - designations de colonie : elargissement et verrou.",
           "# FICHIER GENERE PAR tools/gen_colony_type_overrides.py - NE PAS EDITER A LA MAIN.",
           "#",
           "# 1. Les cinq designations de capitale sont ELARGIES a adastra_grounded",
           "#    (retour Sithiya) - condition elargie, jamais remplacee.",
           "# 2. Toute designation vanilla est VERROUILLEE tant que l'empire est",
           "#    confine (drapeau adastra_locked) : avant l'emergence seule la",
           "#    designation d'epoque col_pre_ftl_* s'applique (retour ampynjord,",
           "#    31/08). A l'emergence le drapeau tombe, le nuancier revient.",
           "#",
           "# Les col_pre_ftl_* sont surchargees ailleurs et absentes d'ici.",
           ""]
    # Les @ declares en tete du fichier vanilla sont locaux au fichier :
    # les blocs recopies en ont besoin ici aussi. (Ceux de
    # common/scripted_variables/ sont globaux et n'ont pas a etre recopies.)
    locales = re.findall(r"^@\w+\s*=\s*\S+", src, re.M)
    if locales:
        out.append("# Variables locales recopiees du fichier vanilla :")
        out.extend(locales)
        out.append("")
    vus_elargis, total_elargis, verrouillees = [], 0, 0
    for name, s, e in top_level_blocks(src):
        if name.startswith("col_pre_ftl"):
            continue
        bloc = src[s:e]
        n = bloc.count(CIBLE)
        if name in A_ELARGIR:
            if not n:
                raise SystemExit("%s : plus de « %s » - le jeu de base a change"
                                 % (name, CIBLE))
            bloc = bloc.replace(CIBLE, REMPLACEMENT)
            vus_elargis.append(name)
            total_elargis += n
            etiquette = "elargie et verrouillee"
        else:
            etiquette = "verrouillee avant emergence"
        bloc = poser_garde(name, bloc)
        out.append("")
        out.append("### %s (%s)" % (name, etiquette))
        out.append(bloc)
        verrouillees += 1

    manquants = [k for k in A_ELARGIR if k not in vus_elargis]
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")

    print("designations verrouillees : %d, dont %d elargies (%d conditions)"
          % (verrouillees, len(vus_elargis), total_elargis))
    if manquants:
        print("INTROUVABLES DANS LE VANILLA : %s" % ", ".join(manquants))
    print("ecrit : %s" % args.out)


if __name__ == "__main__":
    main()
