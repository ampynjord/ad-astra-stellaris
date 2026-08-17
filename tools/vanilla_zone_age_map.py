# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - a quel age chaque specialisation de district devient possible.

CE QUI A ETE TROUVE (retour ampynjord, test en jeu)
    La 4.0 a ajoute un troisieme etage sous les batiments : les ZONES, affichees
    en jeu sous le nom de « specialisations de district ». Elles ne sont
    pratiquement pas gatees par le jeu de base : sur 145 zones, la plupart sont
    disponibles des le premier jour. Un empire a l'Age de pierre pouvait donc
    specialiser son district urbain en « Industrie lourde » ou en
    « Specialisation de recherche en physique ».

LA REGLE
    Meme principe que pour les batiments : chaque zone recoit l'age de la
    techno d'epoque equivalente. La justification est en commentaire.

VALEURS
    un age  : specialisation possible a partir de cet age
    "keep"  : disponible des le depart, aucun anachronisme
    "na"    : inatteignable par un empire Ad Astra (gestalt), non touchee
"""

ZONE_AGE = {
    # --- Disponible des le depart ------------------------------------------
    "zone_urban":            ("keep",       "Expansion urbaine : une population qui grandit s'etale, a toute epoque"),

    # --- Age du fer : l'Etat, la loi, la monnaie, les murs ------------------
    "zone_unity":            ("iron",       "Site administratif : le Code de lois et le Tribunal, c'est l'age du fer"),
    "zone_unity_spiritualist": ("iron",     "Enclave spirituelle : meme age que l'administration"),
    "zone_fortress":         ("iron",       "Defenses militaires : fortifications organisees"),
    "zone_trade":            ("iron",       "Centre du commerce : la Monnaie frappee rend le commerce possible"),

    # --- Age du bronze : l'ecrit --------------------------------------------
    "zone_research_unity":   ("bronze",     "Archives : c'est exactement la Maison des tablettes, l'ecriture"),

    # --- Age medieval : l'etude organisee -----------------------------------
    "zone_research":         ("medieval",   "Enclave de recherche : la Scolastique et l'Universite"),

    # --- Renaissance : la science se specialise -----------------------------
    "zone_research_physics": ("renaissance", "Recherche specialisee : la Methode experimentale separe les disciplines"),
    "zone_research_society": ("renaissance", "Recherche specialisee : idem"),
    "zone_research_engineering": ("renaissance", "Recherche specialisee : idem"),

    # --- Age de la vapeur puis industriel : l'usine --------------------------
    "zone_industrial":       ("steam",      "Industrie mixte : la Machine a vapeur, premiere vraie industrie"),
    "zone_factory":          ("industrial", "Industrie civile : la Chaine de montage"),
    "zone_foundry":          ("industrial", "Industrie lourde : l'Acier Bessemer"),

    # --- Hors de portee d'un empire Ad Astra ---------------------------------
    "zone_spawning":         ("na", "Esprit ruche"),
    "zone_machine_replication": ("na", "Empire machine"),
    "zone_unity_bio_trophy": ("na", "Gestalt"),
}

# Zones installees d'office sur la capitale au demarrage, a retirer pendant le
# confinement. Le district les porte ; on les enleve dans adastra.2.
STARTING_ZONES = ["zone_research_unity", "zone_industrial"]

# Batiments poses d'office sur la capitale au demarrage et manifestement
# anachroniques. building_capital est conserve : sans lui la planete n'a plus
# d'administration du tout.
STARTING_BUILDINGS_TO_REMOVE = {
    "building_holo_theatres": "Holotheatres : divertissement holographique, techno de l'Age spatial",
    "building_commercial_zone": "Zones commerciales : tours de bureaux et centres d'affaires",
}

# Ce qu'on met a la place, par age de depart. Batiments bas-de-gamme du jeu de
# base, ceux-la memes qu'utilise l'origine Broken Shackles.
STARTING_BUILDINGS_TO_ADD = {
    "stone":       ["building_low_tech_admin_hub"],
    "bronze":      ["building_low_tech_admin_hub"],
    "iron":        ["building_low_tech_admin_hub"],
    "medieval":    ["building_low_tech_admin_hub"],
    "renaissance": ["building_low_tech_admin_hub"],
    "steam":       ["building_low_tech_admin_hub"],
    "industrial":  ["building_low_tech_admin_hub"],
    "machine":     [],   # a partir d'ici l'administration moderne suffit
    "atomic":      [],
    "space":       [],
}
