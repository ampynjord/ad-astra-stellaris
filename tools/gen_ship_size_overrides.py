#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - rend les vaisseaux civils constructibles par un empire confine.

CE QUI A ETE TROUVE (16/08, apres trois fausses pistes)
    Le chantier orbital ne proposait ni vaisseau scientifique, ni vaisseau de
    construction, ni colonisateur. Les plans etaient pourtant bien dans la
    liste de designs de l'empire - verifie dans la sauvegarde - et les
    vaisseaux naissaient sans probleme quand un evenement les creait.

    Deux fausses pistes avant la bonne :

      1. is_special_buildable = yes sur les designs globaux. Necessaire, sans
         doute, mais pas suffisant : rien n'a change.
      2. required_component = EMPTY_DRIVE, la cale vide du jeu de base, pour
         remplir le jeu ftl_components qu'un design valide doit couvrir. Juste
         aussi, et toujours rien.

    La vraie cause est un cran plus haut. Les tailles science, constructor et
    colonizer declarent chacune :

        potential_country = {
            ...
            OR = {
                has_technology = tech_hyper_drive_1
                has_technology = tech_hyper_drive_2
                has_technology = tech_hyper_drive_3
                has_technology = tech_jump_drive_1
                has_technology = tech_psi_jump_drive_1
            }
        }

    Sans l'une de ces cinq technologies, la TAILLE elle-meme n'existe pas pour
    l'empire. Aucun design, si valide soit-il, ne peut alors etre propose. La
    corvette, elle, n'a aucun potential_country : c'est exactement pour ca
    qu'elle apparaissait, seule, dans le chantier.

    C'est cohérent du point de vue du jeu de base - un vaisseau civil sert a
    voyager entre les etoiles - et c'est precisement l'hypothese que ce mod
    casse : nos coques ne quittent pas leur systeme, et n'ont rien a y faire.

LA METHODE
    La meme que partout ailleurs dans ce mod : on repart du bloc vanilla
    COMPLET et on ELARGIT la condition, on ne la remplace jamais. Une ligne
    s'ajoute au OR :

        AND = { has_origin = origin_adastra
                NOT = { has_country_flag = adastra_completed } }

    Un empire Ad Astra encore confine peut donc batir ses trois coques
    sous-luminiques. Apres l'emergence il a l'hyperpropulsion, la condition du
    jeu de base suffit, et la notre s'efface d'elle-meme. Aucun autre empire de
    la galaxie ne voit la moindre difference.

RESERVE DE COMPATIBILITE
    Surcharger des tailles de vaisseau est plus expose que le reste du mod :
    c'est un fichier que les mods d'equilibrage naval touchent volontiers. Trois
    tailles seulement sont reprises, et rien d'autre n'est modifie dans les
    blocs copies.

    python3 tools/gen_ship_size_overrides.py <00_ship_sizes.txt> --out <fichier>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

A_ELARGIR = ["science", "constructor", "colonizer"]

CIBLE = "has_technology = tech_psi_jump_drive_1"
AJOUT = ("has_technology = tech_psi_jump_drive_1\n"
         "\t\t\t# Ad Astra : une coque sous-luminique n'a pas besoin de savoir\n"
         "\t\t\t# plier l'espace pour traverser son propre systeme.\n"
         "\t\t\tAND = {\n"
         "\t\t\t\thas_origin = origin_adastra\n"
         "\t\t\t\tNOT = { has_country_flag = adastra_completed }\n"
         "\t\t\t}")

ENTETE = """# Ad Astra 1.2 - tailles de vaisseaux civils, elargies a un empire confine.
# FICHIER GENERE PAR tools/gen_ship_size_overrides.py - NE PAS EDITER A LA MAIN.
#
# science, constructor et colonizer exigent l'une des cinq technologies de
# voyage supraluminique dans leur potential_country. Sans elle la TAILLE
# n'existe pas pour l'empire, et aucun design - si valide soit-il - ne peut
# etre propose au chantier. La corvette n'a pas cette clause : c'est pour ca
# qu'elle etait la seule a s'afficher.
#
# La condition est ELARGIE, jamais remplacee. Apres l'emergence, l'empire a
# l'hyperpropulsion et la clause du jeu de base suffit ; la notre s'efface.
"""


def blocs(texte):
    i, n = 0, len(texte)
    motif = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{", re.M)
    while i < n:
        m = motif.search(texte, i)
        if not m:
            return
        d, j = 1, m.end()
        while j < n and d:
            c = texte[j]
            if c == "#":
                j = texte.find("\n", j)
                if j == -1:
                    j = n
            elif c == "{":
                d += 1
            elif c == "}":
                d -= 1
            j += 1
        yield m.group(1), texte[m.start():j]
        i = j


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_file")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    src = open(args.vanilla_file, encoding="utf-8-sig", errors="replace").read()
    # Les @variables sont locales au fichier : sans ca, « Malformed token ».
    variables = dict(re.findall(r"^(@[A-Za-z0-9_]+)\s*=\s*(\S+)", src, re.M))

    def inline(b):
        for k in sorted(variables, key=len, reverse=True):
            b = re.sub(re.escape(k) + r"\b", variables[k], b)
        return b

    out, vus = [ENTETE], []
    for nom, bloc in blocs(src):
        if nom not in A_ELARGIR:
            continue
        if CIBLE not in bloc:
            raise SystemExit("%s : « %s » introuvable - le jeu de base a change"
                             % (nom, CIBLE))
        out.append("")
        out.append("### %s" % nom)
        out.append(inline(bloc).replace(CIBLE, AJOUT, 1))
        vus.append(nom)

    manquants = [k for k in A_ELARGIR if k not in vus]
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")

    print("tailles elargies : %d" % len(vus))
    for k in vus:
        print("   %s" % k)
    if manquants:
        print("INTROUVABLES DANS LE VANILLA : %s" % ", ".join(manquants))
    print("ecrit : %s" % args.out)


if __name__ == "__main__":
    main()
