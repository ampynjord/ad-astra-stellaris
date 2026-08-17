# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - age d'ouverture des technologies vanilla NON de depart.

CE QUI A ETE TROUVE (13/08)
    Les 269 gardes posees sur les technos vanilla envoient 254 d'entre elles a
    l'Age spatial : « tout le vanilla s'ouvre a la fin ». C'est le verrou brut
    herite de la 1.1, quand le mod n'avait pas encore d'arbre d'epoque.

    Consequence mesuree : sur les 56 batiments vanilla qu'on recalait a la main,
    37 ont un prerequis techno, et pour 13 d'entre eux la techno arrivait APRES
    l'age qu'on donnait au batiment. La surcharge du batiment ne servait donc a
    rien - c'est la techno qui decidait, et elle disait « Age spatial ».

LA REGLE
    Quand un batiment vanilla a un prerequis techno, c'est la TECHNO qui porte
    l'age, pas le batiment. On ne touche plus au batiment du tout : on date sa
    techno, et le batiment suit. Une surcharge de moins, un conflit de moins
    avec les autres mods, et un comportement identique pour n'importe quel
    empire qui prend l'origine.

    Le batiment ne garde une surcharge que si sa techno s'ouvre PLUS TOT que
    l'age voulu pour le batiment (cas de deux batiments d'ages differents
    partageant une meme techno), ou si la techno n'est pas gatee du tout.

CE QUE CETTE TABLE CONTIENT
    Uniquement les technos qu'on sort de l'Age spatial. Tout ce qui n'est pas
    liste garde le verrou par defaut. Les technos de DEPART sont ailleurs :
    tools/vanilla_age_map.py.
"""

TECH_AGE = {
    # --- Age industriel : la production de masse ----------------------------
    "tech_luxuries_1": ("industrial",
        "Biens de consommation produits en serie : c'est la definition meme de "
        "la revolution industrielle. Debloque l'Industrie civile."),
    "tech_mineral_purification_1": ("industrial",
        "Purification du minerai : la metallurgie industrielle du XIXe siecle. "
        "Debloque l'Usine de purification."),

    # --- Age de la machine : electricite, chimie, reseaux -------------------
    "tech_power_hub_1": ("machine",
        "Reseau electrique : le maillage national, annees 1920-1930. Debloque "
        "le Reseau energetique."),
    "tech_alloys_1": ("machine",
        "Alliages ameliores : aciers speciaux et premiers alliages legers, "
        "l'aeronautique des annees 1930. Debloque la Fonderie 2."),
    "tech_mining_1": ("machine",
        "Extraction amelioree : mines electrifiees et convoyeurs. Debloque le "
        "district minier 2."),
    "tech_eco_simulation": ("machine",
        "Simulation ecologique : agronomie scientifique et selection dirigee, "
        "les annees qui menent a la Revolution verte."),

    # --- Age de l'atome : chimie fine, genetique, automatisation ------------
    "tech_power_plant_2": ("atomic",
        "Centrale amelioree : la generation d'apres-guerre, thermique puis "
        "nucleaire civile."),
    "tech_power_hub_2": ("atomic",
        "Nexus energetique : interconnexion des reseaux a l'echelle du "
        "continent, annees 1960-1970."),
    "tech_mining_2": ("atomic",
        "Extraction avancee : mines a ciel ouvert mecanisees, engins geants."),
    "tech_mineral_purification_2": ("atomic",
        "Purification avancee : hydrometallurgie et electrolyse industrielle."),
    "tech_gene_crops": ("atomic",
        "Cultures modifiees : la Revolution verte, puis les premiers travaux "
        "sur le genome vegetal - 1953 pour l'ADN, comme tech_genome_mapping."),

    # --- Deja pose en 1.1, conserve ici pour avoir une seule source ---------
    "tech_genome_mapping": ("atomic",
        "Cartographie du genome : structure de l'ADN, 1953."),
}

# Ce que le moteur accepte comme suffixe de adastra_vanilla_open_<age>.
GATED_AGES = ["renaissance", "steam", "industrial", "machine", "atomic", "space"]
