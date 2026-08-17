# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - repartition des technologies vanilla de depart entre les ages.

Regle : chaque techno vanilla de depart est rattachee a l'age ou l'humanite a
reellement fait la decouverte correspondante. Le commentaire de chaque ligne
justifie le rattachement ; c'est la seule documentation qui compte quand il
faudra rearbitrer.

GRANT indique si la techno est OFFERTE a l'entree dans l'age (give_technology
dans les events adastra.40-49) ou seulement RENDUE RECHERCHABLE.

  Depuis la 1.2 : plus rien n'est offert avant l'Age spatial. Offrir une techno
  vanilla a l'entree dans l'age la ferait arriver AVANT les technos d'epoque du
  meme age, exactement l'inverse de la regle « les technos custom precedent le
  vanilla ». Les technos d'epoque se recherchent d'abord, le vanilla de l'age
  s'ouvre ensuite (verrou adastra_vanilla_open_<age>).

  Le tier 0 entre bien dans le tirage - verifie en jeu le 13/08 : nos technos
  d'age sont en tier 0 et apparaissent normalement. Ces technos de depart sont
  donc recherchables sans etre offertes.

  L'Age spatial reste la seule exception : ses technos vanilla forment la boite
  a outils du programme d'ascension (vaisseaux, bases stellaires, colonisation),
  qui est une sequence scriptee. Les casser reviendrait a casser la fin du mod.
"""

# tech vanilla -> (age, offerte a l'entree dans l'age ?)
VANILLA_AGE_MAP = {
    # --- Renaissance : la science devient une institution -------------------
    "tech_basic_science_lab_1":   ("renaissance", False),  # premiers cabinets et academies

    # --- Age de la vapeur : la manufacture ----------------------------------
    "tech_basic_industry":        ("steam", False),        # atelier mecanise, avant la grande usine

    # --- Age industriel : la production de masse ----------------------------
    "tech_mechanized_mining":     ("industrial", False),   # mine a vapeur puis electrique
    "tech_industrial_farming":    ("industrial", False),   # engrais et mecanisation agricole
    # 16/08 : deplacee de industrial a machine. give_technology REFUSE une
    # techno dont les prerequis manquent, et tech_assault_armies exige
    # tech_planetary_defenses, offerte a l'age de la machine. Un depart
    # tardif la perdait en silence - « Attempting to give invalid
    # technology » dans error.log, seize fois par partie.
    "tech_assault_armies":        ("machine", False),      # conscription de masse

    # --- Age de la machine : electricite, etat moderne, guerre totale -------
    "tech_power_plant_1":         ("machine", False),      # centrale electrique
    "tech_planetary_government":  ("machine", False),      # etat bureaucratique moderne
    "tech_basic_health":          ("machine", False),      # theorie microbienne, sante publique
    "tech_planetary_defenses":    ("machine", False),      # 1.2 : deplace depuis atomique.
                                                           # Fortifications et defense du
                                                           # territoire : 1914-1945, pas 1950.
    "tech_flak_batteries_1":      ("machine", False),      # 1.2 : deplace depuis atomique.
                                                           # La DCA est une arme des deux
                                                           # guerres mondiales.

    # --- Age de l'atome ------------------------------------------------------
    "tech_fission_power":         ("atomic", False),       # fission controlee, 1942
    "tech_missiles_1":            ("atomic", False),       # fusee balistique, 1944
    "tech_pd_tracking_1":         ("atomic", False),       # radar de conduite de tir
    "tech_lasers_1":              ("atomic", False),       # premier laser, 1960

    # --- Age spatial : la boite a outils de l'ascension (offertes) ----------
    "tech_holo_entertainment": ("space", False),         # 1.2 : deplace depuis atomique.
                                                           # L'age atomique a deja la Television
                                                           # cote technos d'epoque ; l'holo est
                                                           # de la science-fiction, pas 1950.
    "tech_space_exploration": ("space", False),
    "tech_thrusters_1": ("space", False),
    "tech_solar_panel_network": ("space", False),         # module orbital, pas le panneau au sol
    "tech_space_construction": ("space", False),
    "tech_space_defense_station_1": ("space", False),
    "tech_ship_armor_1": ("space", False),
    "tech_shields_1": ("space", False),
    "tech_reactor_boosters_1": ("space", False),
    "tech_corvettes": ("space", False),
    "tech_starbase_1": ("space", False),
    "tech_starbase_2": ("space", False),
    "tech_colonization_1": ("space", False),
    "tech_interplanetary_commerce": ("space", False),
    "tech_mass_drivers_1": ("space", False),
    "tech_hydroponics": ("space", False),         # baie hydroponique orbitale

    # --- Percee finale : pose par la decision de phase 3, pas par un age ----
    "tech_hyper_drive_1":         ("ftl", False),
}

# Ages qui possedent un verrou adastra_vanilla_open_<age>.
GATED_AGES = ["renaissance", "steam", "industrial", "machine", "atomic", "space"]

# id d'event adastra.4X -> age
AGE_EVENTS = {
    40: "stone", 41: "bronze", 42: "iron", 43: "medieval", 44: "renaissance",
    45: "steam", 46: "industrial", 47: "machine", 48: "atomic", 49: "space",
}


# Prerequis VANILLA des technos ci-dessus, releves le 16/08 sur Stellaris 4.4.6.
#
# POURQUOI CETTE TABLE EXISTE. give_technology REFUSE une technologie dont les
# prerequis manquent, en silence cote jeu et par une ligne « Attempting to give
# invalid technology » dans error.log. Les octrois d'age etaient emis par ordre
# ALPHABETIQUE : tech_assault_armies passait avant tech_planetary_defenses, son
# prerequis, et se faisait refuser a chaque depart tardif. Le joueur perdait la
# techno sans jamais l'apprendre.
#
# Le generateur trie desormais chaque age en ordre de dependance. A relire
# apres une mise a jour de Stellaris : un prerequis ajoute par Paradox se
# verrait de la meme facon, dans error.log.
VANILLA_PREREQ = {
    "tech_assault_armies": ["tech_planetary_defenses"],
    "tech_colonization_1": ["tech_space_exploration"],
    "tech_reactor_boosters_1": ["tech_fission_power"],
    "tech_solar_panel_network": ["tech_starbase_2"],
    "tech_space_defense_station_1": ["tech_starbase_1"],
    "tech_starbase_1": ["tech_space_construction"],
    "tech_starbase_2": ["tech_starbase_1"],
}
