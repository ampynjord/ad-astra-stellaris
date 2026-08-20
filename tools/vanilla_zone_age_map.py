# -*- coding: utf-8 -*-
"""Sources de verite des technologies qui ouvrent les specialisations."""

# (age historique, technologie fondatrice, justification)
ZONE_AGE = {
    "zone_urban": ("keep", None, "Expansion urbaine : une population qui grandit s'etale, a toute epoque"),
    "zone_research_unity": ("bronze", "tech_adastra_writing", "Archives : l'ecriture permet de conserver et d'organiser le savoir"),
    "zone_research": ("medieval", "tech_adastra_scholasticism", "Enclave de recherche : l'etude organisee commence avec la scolastique"),
    "zone_research_physics": ("renaissance", "tech_adastra_experimental_method", "Recherche specialisee : la methode experimentale separe les disciplines"),
    "zone_research_society": ("renaissance", "tech_adastra_experimental_method", "Recherche specialisee : la methode experimentale separe les disciplines"),
    "zone_research_engineering": ("renaissance", "tech_adastra_experimental_method", "Recherche specialisee : la methode experimentale separe les disciplines"),
    "zone_unity": ("iron", "tech_adastra_law", "Site administratif : le Code de lois rend possible une administration specialisee"),
    "zone_unity_spiritualist": ("bronze", "tech_adastra_priesthood", "Enclave spirituelle : le sacerdoce organise son administration"),
    "zone_fortress": ("iron", "tech_adastra_standing_army", "Defenses militaires : une armee permanente organise la defense"),
    "zone_trade": ("iron", "tech_adastra_coinage", "Centre du commerce : la monnaie frappee rend le commerce specialise possible"),
    "zone_industrial": ("steam", "tech_adastra_steam_engine", "Industrie mixte : la machine a vapeur permet la premiere industrie moderne"),
    "zone_factory": ("industrial", "tech_adastra_assembly_line", "Industrie civile : la chaine de montage permet la production specialisee"),
    "zone_foundry": ("industrial", "tech_adastra_bessemer", "Industrie lourde : l'acier Bessemer permet la production lourde specialisee"),
    "zone_spawning": ("na", None, "Esprit ruche"),
    "zone_machine_replication": ("na", None, "Empire machine"),
    "zone_unity_bio_trophy": ("na", None, "Gestalt"),
}

STARTING_ZONES = ["zone_research_unity", "zone_industrial"]
STARTING_BUILDINGS_TO_REMOVE = {
    "building_holo_theatres": "Holotheatres : divertissement holographique, techno de l'Age spatial",
    "building_commercial_zone": "Zones commerciales : tours de bureaux et centres d'affaires",
}
STARTING_BUILDINGS_TO_ADD = {
    "stone": ["building_low_tech_admin_hub"],
    "bronze": ["building_low_tech_admin_hub"],
    "iron": ["building_low_tech_admin_hub"],
    "medieval": ["building_low_tech_admin_hub"],
    "renaissance": ["building_low_tech_admin_hub"],
    "steam": ["building_low_tech_admin_hub"],
    "industrial": ["building_low_tech_admin_hub"],
    "machine": [],
    "atomic": [],
    "space": [],
}
