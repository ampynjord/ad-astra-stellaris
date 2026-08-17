#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - genere les 11 batiments d'epoque, leurs sprites et leur
localisation FR/EN a partir de tools/age_buildings_data.py.

Le gabarit d'un batiment est concentre dans build_block() : si la 4.4 refuse un
champ, il se corrige ici une seule fois pour les 11 batiments.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from age_buildings_data import (AGE_COST, AGE_JOBS, AGE_UPKEEP_PRE,  # noqa: E402
                                BUILDINGS, CAPITAL, CAPITAL_CHAIN,
                                CAPITAL_UPKEEP)

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ad_astra")

HEADER = (
    "# Ad Astra 1.2 - batiments d'epoque.\n"
    "# FICHIER GENERE PAR tools/gen_age_buildings.py - NE PAS EDITER A LA MAIN.\n"
    "# Source de verite : tools/age_buildings_data.py\n"
    "#\n"
    "# potential ne teste que l'origine : un batiment dont le potential devient\n"
    "# faux est desactive par le moteur. Les batiments deja eleves doivent\n"
    "# survivre a l'emergence, c'est donc allow qui ferme la construction.\n")


def build_block(b):
    minerals, energy, buildtime = AGE_COST[b["age"]]
    out = ["%s = {" % b["key"]]
    out.append("\tcan_build = yes")
    out.append("\tbase_buildtime = %d" % buildtime)
    out.append("\tcategory = %s" % b["cat"])
    out.append('\ticon = "%s"' % b["icon"])
    out.append("")
    out.append("\t# Obligatoire en 4.4 : determine les zones ou le batiment peut etre eleve.")
    out.append("\tbuilding_sets = {")
    for st in b["sets"].split():
        out.append("\t\t%s" % st)
    out.append("\t}")
    out.append("")
    out.append('\tprerequisites = { "%s" }' % b["tech"])
    out.append("")
    out.append("\t# Un seul par planete. ATTENTION : ne JAMAIS mettre cette limite")
    out.append("\t# dans potential - un batiment dont le potential devient faux est")
    out.append("\t# detruit par le moteur, donc il se construisait puis disparaissait")
    out.append("\t# aussitot. planet_limit est le champ prevu pour ca (249 usages")
    out.append("\t# dans le jeu de base).")
    out.append("\tplanet_limit = {")
    out.append("\t\tbase = 1")
    out.append("\t}")
    out.append("")
    out.append("\tpotential = {")
    out.append("\t\texists = owner")
    out.append("\t\towner = { has_origin = origin_adastra }")
    out.append("\t}")
    out.append("")
    out.append("\t# Construction reservee au confinement ; l'existant survit a l'emergence.")
    out.append("\tallow = {")
    out.append("\t\towner = { NOT = { has_country_flag = adastra_completed } }")
    out.append("\t}")
    out.append("")
    out.append("\tresources = {")
    out.append("\t\tcategory = planet_buildings")
    out.append("\t\tcost = { minerals = %d }" % minerals)
    # 1.2 : l'entretien se paie en energie... quand l'energie existe.
    #
    # Verifie en jeu le 13/08 : un modificateur d'entretien ne descend jamais
    # en dessous de -90 %. « Un monde sans courant » affiche bien -100 %, et le
    # batiment coute quand meme 0,10 energie par mois - un dixieme de sa base,
    # que l'empire ne peut pas payer. La seule facon d'atteindre zero est
    # d'ecrire la regle ici, dans la definition, avec deux blocs upkeep
    # mutuellement exclusifs. Meme methode que pour les districts.
    #
    # 15/08 : la branche d'avant l'electricite ne paie plus en minerais seuls.
    # Une civilisation pre-industrielle entretient ses ouvrages avec de la
    # matiere qui s'use ET des bras qu'il faut nourrir - voir AGE_UPKEEP_PRE.
    pre_min, pre_food = AGE_UPKEEP_PRE[b["age"]]
    out.append("\t\tupkeep = {")
    out.append("\t\t\tenergy = %d" % energy)
    out.append("\t\t\ttrigger = { owner = { adastra_pays_energy_upkeep = yes } }")
    out.append("\t\t}")
    out.append("\t\tupkeep = {")
    out.append("\t\t\tminerals = %d" % pre_min)
    out.append("\t\t\tfood = %d" % pre_food)
    out.append("\t\t\ttrigger = { owner = { NOT = { adastra_pays_energy_upkeep = yes } } }")
    out.append("\t\t}")
    out.append("\t}")
    out.append("")
    out.append("\t# La production vient d'emplois, pas d'un pourcentage : le Grenier")
    out.append("\t# emploie des fermiers. Script du jeu de base, qui gere deja les")
    out.append("\t# variantes gestalt et empire dechu.")
    out.append("\tinline_script = {")
    out.append("\t\tscript = jobs/%s" % b["job"])
    out.append("\t\tAMOUNT = %s" % AGE_JOBS[b["age"]])
    out.append("\t}")
    out.append("")
    if b["mods"]:
        out.append("\tplanet_modifier = {")
        for k, v in b["mods"].items():
            out.append("\t\t%s = %s" % (k, "%g" % v))
        out.append("\t}")
        out.append("")
    out.append("\tai_weight = { weight = 5 }")
    out.append("}\n")
    return "\n".join(out)


def gen_buildings():
    parts = [HEADER]
    for b in BUILDINGS:
        parts.append("\n# --- %s (%s) ---\n" % (b["fr"], b["age"]))
        parts.append(build_block(b))
    return "\n".join(parts)


def gen_loc(lang):
    kn, kd = ("fr", "dfr") if lang == "french" else ("en", "den")
    out = ["﻿l_%s:" % lang,
           " # Ad Astra 1.2 - batiments d'epoque. GENERE par tools/gen_age_buildings.py."]
    for b in BUILDINGS:
        out.append(' %s:0 "%s"' % (b["key"], b[kn]))
        out.append(' %s_desc:0 "%s"' % (b["key"], b[kd]))
    out.append(" # Chaine des capitales d'epoque")
    for c in CAPITAL_CHAIN:
        out.append(' %s:0 "%s"' % (c["key"], c[kn]))
        out.append(' %s_desc:0 "%s"' % (c["key"], c[kd]))
    return "\n".join(out) + "\n"



CAPITAL_HEADER = """# Ad Astra 1.2 - la chaine des capitales d'epoque.
# FICHIER GENERE PAR tools/gen_age_buildings.py - NE PAS EDITER A LA MAIN.
# Source de verite : tools/age_buildings_data.py (CAPITAL_CHAIN)
#
# L'Administration planetaire du jeu de base donne +1000 logements, +1000
# services et 300 emplois : un gouvernement planetaire moderne sur un monde de
# l'age de pierre. Aucune capitale primitive du jeu n'est utilisable telle
# quelle - elles exigent toutes un empire primitif ou l'origine Broken Shackles,
# dont la fiction (une epave de vaisseau esclavagiste) n'a rien a voir avec la
# notre.
#
# On fait donc la notre, en SEPT paliers : un par age, du cercle de pierres aux
# ministeres. Chaque palier s'ameliore vers le suivant des que sa techno est
# connue ; le dernier debouche sur building_capital, qui reprend ensuite sa
# propre chaine vanilla (Centre administratif, Capitale systeme). Le siege du
# pouvoir suit donc la civilisation d'un bout a l'autre, sans rupture.
#
# can_build = no partout : on ne construit jamais une capitale, on l'ameliore.
#
# capital_tier CROISSANT de 0 a 6. Les sept paliers portaient tous « 1 » et
# aucun bouton d'amelioration n'apparaissait, techno acquise ou non - releve en
# jeu le 15/08, Langage articulé cherché, Cercle de pierres inchange. Toutes
# les chaines du jeu de base incrementent ce champ (Abri colonial 1,
# Administration planetaire 2, Centre administratif 3, Capitale systeme 4).
#
# RESERVE : le dernier palier, les Ministeres, pointe vers building_capital,
# qui est en tier 2 - soit MOINS que le tier 6 des Ministeres. Si le moteur
# exige un tier superieur, ce dernier maillon ne s'ouvrira pas et il faudra
# le traiter autrement (echange par evenement a la recherche du Gouvernement
# planetaire). A verifier en jeu, mais tres loin dans une partie.
"""


def capital_block(c, nxt, tier):
    b = ["%s = {" % c["key"]]
    b.append("\tcapital = yes")
    b.append("\tcan_build = no")
    b.append("\tcan_demolish = no")
    b.append("\tcan_be_ruined = no")
    b.append("\tcan_be_disabled = no")
    b.append("\tposition_priority = 0")
    # capital_tier CROISSANT. Les sept paliers portaient tous « 1 » et aucun
    # bouton d'amelioration n'apparaissait, techno acquise ou non. Toutes les
    # chaines de capitales du jeu de base incrementent ce champ d'un palier a
    # l'autre (Abri colonial 1, Administration planetaire 2, Centre
    # administratif 3, Capitale systeme 4) : le moteur s'en sert pour savoir
    # qu'un palier est SUPERIEUR au precedent.
    b.append("\tcapital_tier = %d" % tier)
    b.append("\tbase_buildtime = 360")
    b.append("")
    b.append("\tcategory = government")
    b.append('\ticon = "building_low_tech_capital"')
    b.append("\tbuilding_sets = { government }")
    b.append("")
    if c["tech"]:
        b.append('\tprerequisites = { "%s" }' % c["tech"])
        b.append("")
    # Un cout, meme symbolique : une amelioration sans prix n'a rien a
    # facturer, et aucune capitale du jeu de base n'en est depourvue.
    e, m, f = CAPITAL_UPKEEP[tier]
    b.append("\tresources = {")
    b.append("\t\tcategory = planet_buildings")
    b.append("\t\tcost = { minerals = %d }" % c["cost"])
    b.append("\t\tupkeep = {")
    b.append("\t\t\tenergy = %d" % e)
    b.append("\t\t\ttrigger = { owner = { adastra_pays_energy_upkeep = yes } }")
    b.append("\t\t}")
    b.append("\t\tupkeep = {")
    b.append("\t\t\tminerals = %d" % m)
    b.append("\t\t\tfood = %d" % f)
    b.append("\t\t\ttrigger = { owner = { NOT = { adastra_pays_energy_upkeep = yes } } }")
    b.append("\t\t}")
    b.append("\t}")
    b.append("")
    b.append("\t# Portee planete : la garde de pays passe par owner.")
    b.append("\tpotential = {")
    b.append("\t\texists = owner")
    b.append("\t\towner = {")
    b.append("\t\t\thas_origin = origin_adastra")
    b.append("\t\t\tNOT = { has_country_flag = adastra_completed }")
    b.append("\t\t}")
    b.append("\t}")
    b.append("")
    b.append("\tplanet_modifier = {")
    b.append("\t\tplanet_housing_add = %d" % c["housing"])
    b.append("\t\tplanet_amenities_add = %d" % c["amenities"])
    b.append("\t}")
    b.append("")
    b.append("\tinline_script = {")
    b.append("\t\tscript = shroud/jobs/colonist_add")
    b.append("\t\tAMOUNT = %d" % c["colonists"])
    b.append("\t}")
    if c["enforcers"]:
        b.append("")
        b.append("\tinline_script = {")
        b.append("\t\tscript = jobs/enforcers_add")
        b.append("\t\tAMOUNT = %d" % c["enforcers"])
        b.append("\t}")
    b.append("")
    b.append("\t# L'amelioration suivante. Le dernier palier rend la main au")
    b.append("\t# jeu de base : building_capital et toute sa chaine.")
    b.append("\tupgrades = {")
    b.append("\t\t%s" % nxt)
    b.append("\t}")
    b.append("}")
    return "\n".join(b)


def gen_capitals():
    parts = [CAPITAL_HEADER]
    for i, c in enumerate(CAPITAL_CHAIN):
        nxt = (CAPITAL_CHAIN[i + 1]["key"] if i + 1 < len(CAPITAL_CHAIN)
               else "building_capital")
        parts.append("\n# --- %s (%s) ---\n" % (c["fr"], c["age"]))
        parts.append(capital_block(c, nxt, i))
    return "\n".join(parts) + "\n"


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  ecrit : %s" % os.path.relpath(path, ROOT))


def main():
    print("Ad Astra 1.2 - generation de %d batiments d'epoque" % len(BUILDINGS))
    write(os.path.join(ROOT, "common", "buildings", "adastra_age_buildings.txt"),
          gen_buildings())
    write(os.path.join(ROOT, "common", "buildings", "zzz_adastra_capital.txt"),
          gen_capitals())
    write(os.path.join(ROOT, "localisation", "french", "adastra_buildings_l_french.yml"),
          gen_loc("french"))
    write(os.path.join(ROOT, "localisation", "english", "adastra_buildings_l_english.yml"),
          gen_loc("english"))
    print("OK")


if __name__ == "__main__":
    main()
