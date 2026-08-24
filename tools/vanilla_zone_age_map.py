# -*- coding: utf-8 -*-
"""Sources de verite des technologies qui ouvrent les specialisations."""

# Noms affiches par le jeu de base. Cette table accompagne ZONE_AGE : elle
# permet aux descriptions des technologies d'annoncer exactement ce que les
# gardes des zones rendent disponible.
SPECIALIZATION_NAMES = {
    "zone_research_unity": ("Archives", "Archives"),
    "zone_research": ("Enclave de recherche", "Research Enclave"),
    "zone_research_physics": ("Spécialisation de recherche en physique", "Physics Research Specialization"),
    "zone_research_society": ("Spécialisation de recherche sociétale", "Society Research Specialization"),
    "zone_research_engineering": ("Spécialisation de recherche en ingénierie", "Engineering Research Specialization"),
    "zone_unity": ("Site administratif", "Administrative Hub"),
    "zone_unity_spiritualist": ("Enclave spirituelle", "Spiritual Enclave"),
    "zone_fortress": ("Défenses militaires", "Military Defenses"),
    "zone_trade": ("Centre du commerce", "Commercial Nexus"),
    "zone_industrial": ("Industrie mixte", "Mixed Industry"),
    "zone_factory": ("Industrie civile", "Civilian Industry"),
    "zone_foundry": ("Industrie lourde", "Heavy Industry"),
}

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

# Une zone avancee ouvre naturellement davantage d'emplacements. Le joueur ne
# recoit donc pas toute la capacite de construction des le premier district
# urbain. Cette capacite depend du developpement urbain et des technologies,
# jamais du soutien fluctuant d'une faction : perdre un soutien ne doit pas
# rendre un batiment deja construit illegitime.
ZONE_BUILDING_SLOTS = {
    "zone_urban": 1,
    "zone_research_unity": 1,
    "zone_research": 2,
    "zone_research_physics": 2,
    "zone_research_society": 2,
    "zone_research_engineering": 2,
    "zone_unity": 1,
    "zone_unity_spiritualist": 1,
    "zone_fortress": 1,
    "zone_trade": 1,
    "zone_industrial": 2,
    "zone_factory": 2,
    "zone_foundry": 2,
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


def specialization_unlocks():
    """Retourne les annonces FR/EN deduites des gardes de specialisation."""
    out = {}
    for zone, (_age, tech, _why) in ZONE_AGE.items():
        if not tech:
            continue
        fr, en = SPECIALIZATION_NAMES[zone]
        slots = ZONE_BUILDING_SLOTS[zone]
        fr_slots = "%d emplacement%s" % (slots, "" if slots == 1 else "s")
        en_slots = "%d building slot%s" % (slots, "" if slots == 1 else "s")
        out.setdefault(tech, [[], []])
        out[tech][0].append("%s (%s)" % (fr, fr_slots))
        out[tech][1].append("%s (%s)" % (en, en_slots))
    return {
        tech: (
            "Débloque la spécialisation de district : %s." % ", ".join(names[0]),
            "Unlocks district specialization: %s." % ", ".join(names[1]),
        )
        for tech, names in out.items()
    }
