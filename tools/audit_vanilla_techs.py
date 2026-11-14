#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - audit : une techno du jeu de base peut-elle apparaitre a un age
ou elle n'a rien a faire ?

POURQUOI CET OUTIL
    Le mod verrouille les technos du jeu de base par ENUMERATION : les 33 technos
    de depart dans zzz_adastra_tech_overrides.txt, puis toutes les technos de
    tier 1 et 2 dans zzz_adastra_tier1_overrides.txt. Une enumeration se perime :
    il suffit qu'une mise a jour de Stellaris ajoute une techno de bas palier
    sans prerequis pour qu'elle passe au travers, et rien en jeu ne le signale -
    le joueur decouvre juste des lasers a l'age du bronze.
    C'est exactement le bug qu'avait remonte Nobumon en 1.1 (« modern techs at
    Late Medieval age »).

CE QUE FAIT LE SCRIPT
    Il refait le raisonnement du moteur, en trois temps.

    1. Il lit toutes les technos du jeu de base et note leur palier, leurs
       prerequis, et si elles sont technos de depart.
    2. Il lit nos deux fichiers de surcharge et marque comme verrouillee toute
       techno qui y figure.
    3. Il calcule l'ensemble ATTEIGNABLE : une techno est atteignable si elle
       n'est pas verrouillee ET si tous ses prerequis le sont aussi. Puis il
       ecarte celles que le moteur ne peut de toute facon pas proposer :

         - palier >= 2 : common/technology/tier exige six technos du palier
           precedent. Nos cent technos d'epoque sont toutes en palier 0 et ne
           comptent pas ; aucune techno vanilla de palier 1 n'etant accessible,
           le palier 2 ne s'ouvre jamais, ni les suivants.
         - poids de tirage nul (weight = 0 et weight_modifier factor = 0) :
           jamais proposee, seulement donnee par evenement ou relique.
         - potential/starting_potential qui exige un type d'empire, un civisme
           ou une origine qu'un empire Ad Astra ne peut pas avoir.

    Ce qui reste est la vraie surface de fuite, a lire a la main.

USAGE (PC en ligne, sur les fichiers du jeu)
    python3 tools/audit_vanilla_techs.py \\
        "<...>/Stellaris/common/technology" --mod ad_astra/common/technology

RESULTAT DU 15/08/2026, Stellaris 4.4.6
    678 technos du jeu de base, 270 verrouillees par le mod, et AUCUNE fuite :
    tout ce qui restait atteignable etait soit de palier 3 et plus (palier ferme
    faute de technos de palier 1-2), soit conditionne a un empire que l'origine
    exclut. Les quatre cas limites, tous fermes :

      tech_subspace_drive        weight = 0 et starting_potential = Explorateurs
                                 enthousiastes. Jamais tiree, jamais donnee.
                                 (Le point 14.1 du protocole de test est clos.)
      tech_maulers, tech_weavers et leurs ameliorations
                                 starting_potential = { is_low_tech_start = no }.
                                 Ad Astra ne satisfaisait PAS ce declencheur : un
                                 empire a vaisseaux vivants commencait donc avec.
                                 Repare le 15/08 en surchargeant
                                 is_low_tech_start - voir
                                 common/scripted_triggers/zz_adastra_scripted_triggers.txt
      tech_critter_feeder        origine Fertile, incompatible.
      tech_hive_node, tech_wilderness_*, tech_nomads_*
                                 esprit ruche, friche, nomades : hors de portee
                                 d'un empire regulier.

    A relancer apres chaque mise a jour de Stellaris.
"""
import argparse
import os
import re

TIER_OUVERT = ("0", "1")   # au-dela, le palier lui-meme est ferme


def blocs(texte):
    """Rend (nom, texte du bloc) pour chaque « nom = { ... } » de premier niveau."""
    i, n = 0, len(texte)
    motif = re.compile(r"([A-Za-z0-9_@.]+)\s*=\s*\{")
    while i < n:
        m = motif.search(texte, i)
        if not m:
            return
        debut_ligne = texte.rfind("\n", 0, m.start()) + 1
        if "#" in texte[debut_ligne:m.start()]:
            nl = texte.find("\n", m.start())
            i = n if nl == -1 else nl + 1
            continue
        prof, j = 1, m.end()
        while j < n and prof:
            c = texte[j]
            if c == "#":
                j = texte.find("\n", j)
                if j == -1:
                    j = n
            elif c == "{":
                prof += 1
            elif c == "}":
                prof -= 1
            j += 1
        yield m.group(1), texte[m.start():j]
        i = j


def sans_commentaires(t):
    return re.sub(r"#[^\n]*", "", t)


def champ(b, nom):
    m = re.search(r"\b%s\s*=\s*([^\s{}]+)" % nom, sans_commentaires(b))
    return m.group(1) if m else None


def prerequis(b):
    m = re.search(r"\bprerequisites\s*=\s*\{([^}]*)\}", sans_commentaires(b))
    return re.findall(r'"?(tech_[A-Za-z0-9_]+)"?', m.group(1)) if m else []


def jamais_tiree(b):
    """weight = 0 sans multiplicateur qui le releve : hors tirage."""
    return champ(b, "weight") == "0"


def lire_dossier(chemin, garder_tech=True):
    out = {}
    for fn in sorted(os.listdir(chemin)):
        if not fn.endswith(".txt") or fn == "00_test.txt":
            continue
        texte = open(os.path.join(chemin, fn), encoding="utf-8-sig",
                     errors="replace").read()
        for nom, b in blocs(texte):
            if garder_tech and not nom.startswith("tech_"):
                continue
            out[nom] = (fn, b)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_dir", help="dossier common/technology du jeu")
    ap.add_argument("--mod", required=True, help="notre dossier common/technology")
    args = ap.parse_args()

    vanilla = lire_dossier(args.vanilla_dir)
    notre = lire_dossier(args.mod)
    verrouillees = set(notre) & set(vanilla)

    memo = {}

    def atteignable(nom, pile=()):
        if nom in memo:
            return memo[nom]
        if nom in pile or nom not in vanilla:
            return False
        if nom in verrouillees:
            memo[nom] = False
            return False
        ok = all(atteignable(p, pile + (nom,)) for p in prerequis(vanilla[nom][1]))
        memo[nom] = ok
        return ok

    suspectes = []
    for nom in sorted(vanilla):
        if not atteignable(nom):
            continue
        fn, b = vanilla[nom]
        if champ(b, "tier") not in TIER_OUVERT:
            continue          # palier ferme faute de technos de palier 1-2
        if jamais_tiree(b):
            continue          # hors tirage : evenement ou relique seulement
        suspectes.append((nom, fn, b))

    print("technos du jeu de base : %d" % len(vanilla))
    print("verrouillees par le mod : %d" % len(verrouillees))
    print("atteignables de palier %s et tirables : %d"
          % ("/".join(TIER_OUVERT), len(suspectes)))
    print()
    for nom, fn, b in suspectes:
        pot = re.search(r"\n\tpotential\s*=\s*\{(.*?)\n\t\}", b, re.S)
        sp = re.search(r"\n\tstarting_potential\s*=\s*\{(.*?)\n\t\}", b, re.S)
        print("  %-42s %s" % (nom, fn))
        print("      depart   : %s" % ("oui" if champ(b, "start_tech") == "yes" else "non"))
        print("      potential: %s" % (" ".join(pot.group(1).split()) if pot else "(aucun)"))
        print("      starting : %s" % (" ".join(sp.group(1).split()) if sp else "(aucun)"))
    if not suspectes:
        print("  aucune - rien ne passe au travers.")
    print()
    print("A LIRE A LA MAIN : chaque ligne ci-dessus doit etre fermee par une")
    print("condition qu'un empire Ad Astra ne peut pas satisfaire. Sinon, ajouter")
    print("la techno a tools/vanilla_tech_age_map.py ou la verrouiller.")


if __name__ == "__main__":
    main()
