#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.3 - reecrit le bloc monthly_progress de la situation.

Pourquoi un generateur : le verrou de passage d'age declare UN modificateur par
technologie, parce que le moteur affiche la ligne `desc` de chaque modificateur
qui s'applique. L'infobulle de la barre devient donc la liste exacte de ce qui
reste a trouver. A 100 technologies c'etait deja long a tenir a la main ; a 250,
c'est intenable.

Le generateur ecrit aussi les cles de localisation `adastra_manque_<cle>` dans
les deux langues, pour qu'aucune ligne ne sorte en clef brute.

    python3 tools/gen_situation_progress.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from age_techs_data import AGES, TECHS, BORNES, vagues  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITUATION = os.path.join(RACINE, "ad_astra", "common", "situations",
                         "zzz_adastra_situations.txt")

# Etape de situation et borne haute de chaque age.
ETAPES = {
    "stone":       ("adastra_stage_stone_age", 12),
    "bronze":      ("adastra_stage_bronze_age", 22),
    "iron":        ("adastra_stage_iron_age", 31),
    "medieval":    ("adastra_stage_late_medieval_age", 39),
    "renaissance": ("adastra_stage_renaissance_age", 47),
    "steam":       ("adastra_stage_steam_age", 55),
    "industrial":  ("adastra_stage_industrial_age", 64),
    "machine":     ("adastra_stage_machine_age", 74),
    "atomic":      ("adastra_stage_atomic_age", 86),
    "space":       ("adastra_stage_early_space_age", 100),
}

# 1.4 (17/08) : les trois etapes du programme spatial sont traitees COMME UN
# AGE. La barre monte, puis se fige a un point de la fin tant que le lot de
# technologies fondatrices de l'etape n'est pas recherche ET que le jalon de
# l'etape n'est pas atteint. Un seul mecanisme pour les treize etapes ; les
# evenements adastra.71/72 qui faisaient sauter la barre par jalon disparaissent.
PROGRAMME = [
    # (etape, fin, declencheurs de jeu dont le lot appartient a l'etape,
    #  cle de loc du jalon) - la condition du jalon est dans JALONS
    ("adastra_stage_program_explore", 110, ("adastra_gameplay_orbite", "adastra_gameplay_sol"),
     "adastra_manque_jalon_explore"),
    ("adastra_stage_program_orbital", 120, ("adastra_gameplay_chantier", "adastra_gameplay_vaisseaux", "adastra_gameplay_colonie"),
     "adastra_manque_jalon_orbital"),
    ("adastra_stage_program_hyperdrive", 130, ("adastra_gameplay_base",),
     "adastra_manque_jalon_hyper"),
]

JALONS = {
    # Exploration : chaque astre du systeme natal releve (ancien adastra.71).
    "adastra_stage_program_explore": """			owner = {
				NOT = {
					capital_scope = {
						solar_system = {
							NOT = {
								any_system_planet = {
									is_star = no
									NOT = { is_surveyed = { who = root.owner status = yes } }
								}
							}
						}
					}
				}
			}""",
    # Chantier orbital : la base stellaire batie ET une premiere station
    # d'extraction ou de recherche - ou le systeme occupe par un autre
    # empire, auquel cas on passe outre (ancien adastra.72).
    "adastra_stage_program_orbital": """			owner = {
				NOR = {
					AND = {
						has_country_flag = adastra_phase2_done
						count_owned_fleet = {
							count >= 1
							limit = { OR = { is_ship_size = mining_station is_ship_size = research_station } }
						}
					}
					capital_scope = {
						solar_system = {
							exists = starbase
							starbase = { exists = owner owner = { NOT = { is_same_value = root.owner } } }
						}
					}
				}
			}""",
    # Hyperespace : l'Hyperpropulsion elle-meme (ancien adastra.10).
    "adastra_stage_program_hyperdrive": """			owner = { NOT = { has_technology = tech_hyper_drive_1 } }""",
}

# Les technologies du jeu de base que l'Age spatial demande desormais de
# CHERCHER au lieu de les recevoir. Elles apparaissent dans le verrou au meme
# titre que les technologies d'epoque : le joueur doit voir ce qui lui manque.
# Chaque fondatrice porte le declencheur du jeu qu'elle sert. Le verrou de la
# situation ne la reproche au joueur que si elle est effectivement cherchable :
# sinon la barre se figerait sur une technologie qu'il n'a pas le droit de
# prendre, ce qui serait une impasse et non un objectif.
FONDATRICES = [
    ("tech_space_exploration", "Exploration spatiale", "Space Exploration", "adastra_gameplay_orbite"),
    ("tech_thrusters_1", "Propulseurs chimiques", "Chemical Thrusters", "adastra_gameplay_orbite"),
    ("tech_space_construction", "Construction hors-monde", "Offworld Construction", "adastra_gameplay_chantier"),
    ("tech_corvettes", "Corvettes", "Corvettes", "adastra_gameplay_vaisseaux"),
    ("tech_mass_drivers_1", "Conducteurs de masse", "Mass Drivers", "adastra_gameplay_vaisseaux"),
    ("tech_ship_armor_1", "Materiaux nanocomposites", "Nanocomposite Materials", "adastra_gameplay_vaisseaux"),
    ("tech_shields_1", "Deflecteurs", "Deflectors", "adastra_gameplay_vaisseaux"),
    ("tech_starbase_1", "Construction de bases stellaires", "Starbase Construction", "adastra_gameplay_base"),
    ("tech_starbase_2", "Ports stellaires", "Starports", "adastra_gameplay_base"),
    ("tech_space_defense_station_1", "Defenses spatiales", "Space Defense Stations", "adastra_gameplay_base"),
    ("tech_solar_panel_network", "Conversion d'energie orbitale", "Orbital Energy Conversion", "adastra_gameplay_base"),
    ("tech_colonization_1", "Protocole nouveaux mondes", "New Worlds Protocol", "adastra_gameplay_colonie"),
    ("tech_interplanetary_commerce", "Commerce interplanetaire", "Interplanetary Commerce", "adastra_gameplay_sol"),
    ("tech_hydroponics", "Cultures hydroponiques", "Hydroponics", "adastra_gameplay_sol"),
    ("tech_holo_entertainment", "Hololoisirs", "Holo Entertainment", "adastra_gameplay_sol"),
    ("tech_reactor_boosters_1", "Impulseurs", "Reactor Boosters", "adastra_gameplay_vaisseaux"),
]

DEBUT = "\t\t# --- Le verrou de passage d'age ---"
FIN = "\t}\n"


def bloc_verrou(cle_loc, etape, seuil, tech):
    return "\n".join([
        "\t\tmodifier = {",
        "\t\t\tmult = 0.001",
        "\t\t\tdesc = %s" % cle_loc,
        "\t\t\tcurrent_stage = %s" % etape,
        "\t\t\tsituation_progress >= %d" % seuil,
        "\t\t\towner = { NOT = { has_technology = %s } }" % tech,
        "\t\t}",
    ])


def corps():
    out = ["""\t\t# --- Le verrou de passage d'age ---
\t\t# On ne quitte pas un age tant qu'il reste quelque chose a y inventer.
\t\t# La barre monte pendant toute l'etape, puis se fige juste avant la fin
\t\t# tant que les vingt-cinq technologies de l'age ne sont pas trouvees.
\t\t#
\t\t# UN BLOC PAR TECHNOLOGIE, et non un par age : le moteur affiche la ligne
\t\t# desc de CHAQUE modificateur qui s'applique. L'infobulle de la barre est
\t\t# donc la liste exacte de ce qui reste a trouver, et elle se raccourcit a
\t\t# chaque decouverte.
\t\t#
\t\t# mult = 0.001 et non 0 : le jeu de base n'ecrit jamais mult = 0 dans un
\t\t# monthly_progress. A un millieme, il faudrait douze mille ans pour gagner
\t\t# un point - c'est un arret, sans le risque qu'une progression negative
\t\t# ferait courir.
\t\t#
\t\t# 1.3 : l'acceleration d'un age epuise a ete retiree. Elle existait pour
\t\t# eviter de regarder une barre monter sans rien a chercher ; le deblocage
\t\t# par vagues repond mieux au meme probleme, et un age epuise avant l'heure
\t\t# ne doit plus etre recompense.
\t\t#
\t\t# FICHIER PARTIELLEMENT GENERE - bloc reecrit par
\t\t# tools/gen_situation_progress.py. Ne pas editer ces modificateurs a la main.
"""]
    for age, _f, _c, _v in AGES:
        etape, fin = ETAPES[age]
        seuil = fin - 1
        out.append("\t\t# --- %s : les 25 technologies d'epoque ---" % age)
        for t in TECHS[age]:
            court = t["key"][len("tech_adastra_"):]
            out.append(bloc_verrou("adastra_manque_%s" % court, etape, seuil, t["key"]))
    # --- 1.4 : les trois etapes du programme, comme un age ---
    for etape, fin, decls, cle_jalon in PROGRAMME:
        seuil = fin - 1
        out.append("\t\t# --- %s : les fondatrices du jeu de base de l'etape ---" % etape)
        for tech, _fr, _en, decl in FONDATRICES:
            if decl not in decls:
                continue
            court = tech[len("tech_"):]
            out.append("\n".join([
                "\t\tmodifier = {",
                "\t\t\tmult = 0.001",
                "\t\t\tdesc = adastra_manque_base_%s" % court,
                "\t\t\tcurrent_stage = %s" % etape,
                "\t\t\tsituation_progress >= %d" % seuil,
                "\t\t\t# on ne reproche pas une technologie que le joueur n'a pas",
                "\t\t\t# encore le droit de chercher : le jeu qu'elle sert doit etre ouvert.",
                "\t\t\towner = {",
                "\t\t\t\t%s = yes" % decl,
                "\t\t\t\tNOT = { has_technology = %s }" % tech,
                "\t\t\t}",
                "\t\t}",
            ]))
        out.append("\t\t# --- %s : le jalon de l'etape ---" % etape)
        out.append("\n".join([
            "\t\tmodifier = {",
            "\t\t\tmult = 0.001",
            "\t\t\tdesc = %s" % cle_jalon,
            "\t\t\tcurrent_stage = %s" % etape,
            "\t\t\tsituation_progress >= %d" % seuil,
            JALONS[etape],
            "\t\t}",
        ]))
    return "\n".join(out) + "\n"


def loc():
    """Les lignes de localisation du verrou, dans les deux langues."""
    fr, en = [], []
    for age, _f, _c, _v in AGES:
        for t in TECHS[age]:
            court = t["key"][len("tech_adastra_"):]
            fr.append(' adastra_manque_%s:0 "§RIl manque :§! %s"' % (court, t["fr"]))
            en.append(' adastra_manque_%s:0 "§RStill missing:§! %s"' % (court, t["en"]))
    for tech, nfr, nen, _d in FONDATRICES:
        court = tech[len("tech_"):]
        fr.append(' adastra_manque_base_%s:0 "§RIl manque (fondatrice) :§! %s"' % (court, nfr))
        en.append(' adastra_manque_base_%s:0 "§RStill missing (founding tech):§! %s"' % (court, nen))
    fr.append(' adastra_manque_jalon_explore:0 "§RJalon :§! prospecter chaque astre du système natal"')
    en.append(' adastra_manque_jalon_explore:0 "§RMilestone:§! survey every body of the home system"')
    fr.append(' adastra_manque_jalon_orbital:0 "§RJalon :§! bâtir la base stellaire, puis une première station minière ou de recherche"')
    en.append(' adastra_manque_jalon_orbital:0 "§RMilestone:§! build the starbase, then a first mining or research station"')
    fr.append(' adastra_manque_jalon_hyper:0 "§RJalon :§! rechercher l\'Hyperpropulsion"')
    en.append(' adastra_manque_jalon_hyper:0 "§RMilestone:§! research Hyper Drive"')
    return fr, en


def remplace_loc(chemin, langue, lignes):
    txt = open(chemin, encoding="utf-8-sig").read()
    txt = re.sub(r"^ adastra_manque_\w+:0 \".*\"\n", "", txt, flags=re.M)
    marque = "\n# --- verrou de passage d'age (genere) ---\n"
    txt = txt.split(marque)[0].rstrip("\n")
    txt += marque + "\n".join(lignes) + "\n"
    with open(chemin, "w", encoding="utf-8-sig", newline="\n") as sortie:
        sortie.write(txt)
    return len(lignes)


def main():
    src = open(SITUATION, encoding="utf-8").read()
    i = src.find(DEBUT)
    if i < 0:
        sys.exit("bloc de verrou introuvable dans la situation")
    # on remonte pour avaler aussi les modificateurs d'acceleration
    j = src.rfind("\t\t# Quand il n'y a plus rien a inventer", 0, i)
    if j < 0:
        j = i
    else:
        j = src.rfind("\n", 0, src.rfind("\t\t# Le rythme d'un age", 0, j) if src.rfind(
            "\t\t# Le rythme d'un age", 0, j) > 0 else j) + 1
    # fin du bloc monthly_progress : la derniere accolade de niveau 2
    k = src.find("\n\t}\n", i)
    if k < 0:
        sys.exit("fin du bloc monthly_progress introuvable")
    nouveau = src[:j] + corps() + src[k + 1:]
    with open(SITUATION, "w", encoding="utf-8", newline="\n") as sortie:
        sortie.write(nouveau)

    n_tot = sum(len(TECHS[a]) for a, _b, _c, _d in AGES) + len(FONDATRICES)
    print("situation : %d blocs de verrou ecrits" % n_tot)

    fr, en = loc()
    a = remplace_loc(os.path.join(RACINE, "ad_astra", "localisation", "french",
                                  "adastra_l_french.yml"), "french", fr)
    b = remplace_loc(os.path.join(RACINE, "ad_astra", "localisation", "english",
                                  "adastra_l_english.yml"), "english", en)
    print("localisation : %d lignes FR, %d lignes EN" % (a, b))


if __name__ == "__main__":
    main()
