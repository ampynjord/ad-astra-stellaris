#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra - regenere la section « L'arborescence » de design_1.2_ages.md.

Ce tableau etait recopie a la main et se desynchronisait a chaque changement de
cout ou d'effet. Il est desormais produit depuis tools/age_techs_data.py, seule
source de verite.

    python3 tools/gen_design_tree.py [chemin_du_doc]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from age_techs_data import AGES, MAJEURES, TECHS, UNLOCKS  # noqa: E402

DOC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "design_1.2_ages.md")

TITRES = {
    "stone": "Âge de pierre — *survivre*",
    "bronze": "Âge du bronze — *fonder*",
    "iron": "Âge du fer — *organiser*",
    "medieval": "Âge médiéval tardif — *bâtir*",
    "renaissance": "Renaissance — *comprendre*",
    "steam": "Âge de la vapeur — *accélérer*",
    "industrial": "Âge industriel — *produire*",
    "machine": "Âge de la machine — *électrifier*",
    "atomic": "Âge de l'atome — *dominer*",
    "space": "Débuts de l'Âge spatial — *lever les yeux*",
}

AREA_FR = {"physics": "Physique", "society": "Société", "engineering": "Ingénierie"}

MOD_FR = {
    "all_technology_research_speed": ("recherche", "pct"),
    "army_damage_mult": ("dégâts des armées", "pct"),
    "country_unity_produces_mult": ("unité", "pct"),
    "logistic_growth_mult": ("croissance", "pct"),
    "planet_amenities_add": ("agréments", "flat"),
    "planet_crime_add": ("criminalité", "flat"),
    "planet_housing_add": ("logement", "flat"),
    "planet_jobs_alloys_produces_mult": ("alliages", "pct"),
    "planet_jobs_consumer_goods_produces_mult": ("biens de conso.", "pct"),
    "planet_jobs_energy_produces_mult": ("énergie", "pct"),
    "planet_jobs_food_produces_mult": ("nourriture", "pct"),
    "planet_jobs_minerals_produces_mult": ("minerais", "pct"),
    "planet_jobs_physics_research_produces_mult": ("recherche physique", "pct"),
    "planet_jobs_produces_mult": ("toute production", "pct"),
    "planet_jobs_society_research_produces_mult": ("recherche société", "pct"),
    "planet_stability_add": ("stabilité", "flat"),
    "pop_happiness": ("bonheur", "pct"),
}


def effet(t):
    bouts = []
    for k, v in t["mods"].items():
        label, kind = MOD_FR.get(k, (k, "flat"))
        if kind == "pct":
            bouts.append("%+g %% %s" % (round(v * 100, 2), label))
        else:
            bouts.append("%+g %s" % (v, label))
    s = ", ".join(bouts)
    if t["unlocks"]:
        s += " — *débloque : %s*" % t["unlocks"]
    return s


def section():
    total = sum(len(TECHS[a]) for a, _f, _c, _v in AGES)
    out = ["## L'arborescence (%d techs)" % total, ""]
    out.append("*Généré par `tools/gen_design_tree.py` depuis `tools/age_techs_data.py` —"
               " toute modification passe par cette table, jamais par ce tableau.*")
    out.append("")
    out.append("Chaque âge propose **%d technologies** réparties sur les trois domaines."
               " La **première technologie de chaque domaine** est le pilier de l'âge —"
               " c'est le seul prérequis de l'âge suivant dans ce domaine ; les autres"
               " sont facultatives."
               % (total // len(AGES)))
    out.append("")
    out.append("Le coût n'est pas le même pour toutes : c'est le coût de base de l'âge"
               " multiplié par le poids de la technologie. **×1,8** pour les inventions"
               " qui redéfinissent une civilisation (le feu, l'écriture, la machine à"
               " vapeur, l'électricité) ; **×1,4** quand elle débloque un bâtiment, une"
               " ressource ou un palier de capitale ; **×1,2** pour un pilier ; **×1**"
               " pour le reste. On garde la raison la plus forte.")
    out.append("")
    for age, _flag, cost, _v in AGES:
        out.append("### %s  <sub>coût de base %d</sub>" % (TITRES[age], cost))
        out.append("")
        out.append("| Tech | Domaine | Coût | Effet |")
        out.append("|---|---|---:|---|")
        seen = set()
        for t in TECHS[age]:
            est_pilier = t["area"] not in seen
            seen.add(t["area"])
            p = 1.0
            if est_pilier:
                p = max(p, 1.2)
            if t["unlocks"] or t["key"] in UNLOCKS:
                p = max(p, 1.4)
            if t["key"] in MAJEURES:
                p = max(p, 1.8)
            marque = " **·**" if est_pilier else ""
            out.append("| %s%s | %s | %d | %s |"
                       % (t["fr"], marque, AREA_FR[t["area"]],
                          int(round(cost * p / 5.0)) * 5, effet(t)))
        out.append("")
    out.append("**·** = pilier du domaine pour cet âge (prérequis obligatoire de l'âge suivant).")
    out.append("")
    return "\n".join(out)


def main():
    src = open(DOC, encoding="utf-8").read()
    m = re.search(r"^## L'arborescence.*?(?=^## )", src, re.M | re.S)
    if not m:
        print("section « L'arborescence » introuvable dans %s" % DOC)
        return 1
    open(DOC, "w", encoding="utf-8", newline="\n").write(
        src[:m.start()] + section() + src[m.end():])
    print("section regeneree : %s" % DOC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
