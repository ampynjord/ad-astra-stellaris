# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - a quel age chaque batiment vanilla devient constructible.

POURQUOI CETTE CARTE EXISTE
    En 4.4, un batiment n'est plus debloque par une techno mais par une ZONE, et
    les zones ne sont pas gatees par techno. Les Fonderies d'alliage sont donc
    constructibles des le premier tour en vanilla - et des l'Age de pierre avec
    Ad Astra. Il n'y a aucun prerequis vanilla a lire : c'est au mod de trancher.

LA REGLE
    Chaque batiment prend l'age de la techno d'epoque EQUIVALENTE dans notre
    arbre. Le raisonnement est ecrit en commentaire de chaque ligne, c'est la
    seule justification qui compte quand il faudra rearbitrer.

VALEURS
    un age  : constructible a partir de cet age (drapeau adastra_reached_<age>)
    "keep"  : laisse disponible des le depart, aucun anachronisme
    "na"    : inatteignable par un empire Ad Astra (gestalt, civique ou origine
              incompatible) - aucune surcharge generee, on ne touche a rien
    "tech"  : 1.2 - date par sa techno prerequise, pas par une surcharge. Voir
              tools/vanilla_tech_age_map.py. Le batiment vanilla n'est PAS
              touche : un prerequis techno suffit deja a le tenir a sa place,
              et une surcharge de moins est un conflit de moins avec les autres
              mods. La valeur reste ici pour que la table dise pourquoi.
"""

BUILDING_AGE = {

# --- Production de base ---------------------------------------------------
# Les quatre paliers suivent la meme montee que nos technos : engrais chimiques
# (industriel), electrification (machine), petrochimie et electronique (atome),
# puis telematique et telediction (spatial).
"building_farming_districts_1":      ("tech", "Engrais chimiques : l'agriculture cesse d'etre artisanale - date par sa techno (industrial)"),
"building_farming_districts_2":      ("tech",    "Mecanisation et selection : XXe siecle - date par sa techno (machine)"),
"building_farming_districts_3":      ("tech",     "Complexe agricole automatise : automatisation d'apres-guerre - date par sa techno (atomic)"),
"building_farming_districts_4":      ("space",      "Grille de culture planetaire : echelle orbitale"),

"building_mining_districts_1":       ("tech", "Mine industrielle : machine a vapeur puis electrique - date par sa techno (industrial)"),
"building_mining_districts_2":       ("tech",    "Forage profond : moteurs et electricite - date par sa techno (machine)"),
"building_mining_districts_3":       ("tech",     "Tunnels sismiques : explosifs et sondage modernes - date par sa techno (atomic)"),
"building_mining_districts_4":       ("space",      "Extraction de croute profonde : hors echelle terrestre"),

"building_generator_districts_1":    ("tech",    "Reseau electrique - notre techno d'epoque exactement - date par sa techno (machine)"),
"building_generator_districts_2":    ("tech",     "Reseau de sous-stations : grille nationale d'apres-guerre - date par sa techno (atomic)"),
"building_generator_districts_3":    ("tech",      "Regulation plasma : au-dela de la fission - date par sa techno (space)"),
"building_generator_districts_4":    ("space",      "Nexus planetaire : echelle orbitale"),

"building_energy_grid":              ("tech",    "Meme logique que le reseau electrique - date par sa techno (machine)"),
"building_energy_nexus":             ("tech",     "Palier superieur : fission controlee - date par sa techno (atomic)"),
"building_mineral_purification_plant": ("tech", "Purification du minerai : procedes chimiques industriels - date par sa techno (industrial)"),
"building_mineral_purification_hub": ("tech",     "Palier superieur : petrochimie - date par sa techno (atomic)"),

# --- Manufacture ----------------------------------------------------------
"building_factory_1":                ("tech",      "Industries civiles = la Manufacture, notre batiment de l'age de la vapeur - date par sa techno (steam)"),
"building_factory_2":                ("tech", "Chaine de montage - date par sa techno (industrial)"),
"building_factory_3":                ("atomic",     "Repli-complexes : synthese moderne"),
"building_factory_upkeep_1":         ("atomic",     "Optimisation de la chaine : gestion de production moderne"),
"building_factory_efficiency_1":     ("atomic",     "Centre de conception distribue : informatique naissante"),

"building_foundry_1":                ("industrial", "Acier Bessemer : la fonderie moderne, c'est 1856"),
"building_foundry_2":                ("tech",    "Mega-forges : acier electrique - date par sa techno (machine)"),
"building_foundry_3":                ("atomic",     "Nano-usines : au-dela de la metallurgie classique"),
"building_foundry_upkeep_1":         ("atomic",     "Recyclage des alliages : procedes d'apres-guerre"),
"building_foundry_efficiency_1":     ("atomic",     "Laboratoire de metallurgie : science des materiaux"),

"building_offworld_expedition_hub":  ("space",      "Expedition hors-monde : par definition"),

# --- Logement et commodites -----------------------------------------------
"building_communal_housing":         ("keep",       "Se loger n'a aucune epoque : toute civilisation batit des logements"),
"building_luxury_residence":         ("renaissance","Residences de luxe : le palais est un fait de cour, pas de tribu"),
"building_toxic_bath":               ("space",      "Bains mutagenes : biotechnologie"),

# --- Logistique -----------------------------------------------------------
"building_maintenance_depot":        ("industrial", "Pole logistique : chemin de fer et entreposage de masse"),

# --- Gouvernement et societe ----------------------------------------------
"building_noble_estates":            ("medieval",   "Domaines nobiliaires : l'aristocratie fonciere est medievale"),
"building_order_keep":               ("medieval",   "Donjon d'un ordre : parfaitement a sa place au Moyen Age"),
"building_order_castle":             ("medieval",   "Chateau d'un ordre : idem"),
"building_dread_encampment":         ("iron",       "Camp de terreur : razzia et guerre organisee, age du fer"),
"building_ranger_lodge":             ("machine",    "Gardes forestiers : la protection de la nature nait vers 1900"),
"building_psi_corps":                ("space",      "Corps psionique : ascension tardive"),
"building_shroud_observatory_1":     ("space",      "Observatoire du Voile : au-dela du materiel"),

# --- Terraformation, clonage, robotique -----------------------------------
"building_gaiaseeders_1":            ("space",      "Terraformation : hors de portee avant l'orbite"),
"building_gaiaseeders_2":            ("space",      "Terraformation"),
"building_gaiaseeders_3":            ("space",      "Terraformation"),
"building_gaiaseeders_4":            ("space",      "Terraformation"),
"building_gaiaseeders_pc_gaia":      ("space",      "Terraformation"),

"building_clone_vats":               ("tech",      "Cuves de clonage : le plus anachronique de la liste - date par sa techno (space)"),
"building_clone_army_clone_vat":     ("space",      "Cuve de clonage antique"),
"building_robot_assembly_complex":   ("space",      "Assemblage robotique"),
"building_posthumous_employment_center": ("space",  "Emploi posthume : cybernetique"),
"building_automation_1":             ("tech",      "Automatisation - date par sa techno (space)"),
"building_automation_2":             ("space",      "Optimisation"),
"building_automation_farmer_1":      ("tech",      "Automatisation agricole - date par sa techno (space)"),
"building_automation_farmer_2":      ("space",      "Automatisation agricole"),
"building_automation_miner_1":       ("tech",      "Automatisation miniere - date par sa techno (space)"),
"building_automation_miner_2":       ("space",      "Automatisation miniere"),
"building_automation_technician_1":  ("tech",      "Automatisation energetique - date par sa techno (space)"),
"building_automation_technician_2":  ("space",      "Automatisation energetique"),
"building_necrophage_elevation_chamber": ("space",  "Chambre d'elevation necrophage"),
"building_necrophage_house_of_apotheosis": ("space","Maison de l'apotheose"),

# --- Inatteignables par un empire Ad Astra (gestalt) -----------------------
"building_machine_assembly_plant":   ("na", "Empire machine"),
"building_machine_assembly_complex": ("na", "Empire machine"),
"building_spawning_pool":            ("na", "Esprit ruche"),
"building_offspring_nest":           ("na", "Esprit ruche"),
"building_hive_warren":              ("na", "Esprit ruche"),
"building_toxic_bath_hive":          ("na", "Esprit ruche"),
"building_toxic_bath_machine":       ("na", "Empire machine"),
"building_drone_storage":            ("na", "Gestalt"),
"building_overseer_homes":           ("na", "Gestalt"),
"building_organic_sanctuary":        ("na", "Gestalt"),
"building_coordinated_fulfillment_center_1": ("na", "Gestalt"),
"building_coordinated_fulfillment_center_2": ("na", "Gestalt"),
}

# 1.2 - les batiments marques "tech" : quelle techno les porte, et a quel age
# on veut qu'ils arrivent. Cette table n'est PAS appliquee au jeu - elle sert a
# tools/verify_1_2.py, qui verifie que la techno de chaque batiment s'ouvre bien
# a cet age ou plus tard (tools/vanilla_tech_age_map.py). Sans ce controle,
# redater une techno decalerait silencieusement un batiment.
# 16/08 : six batiments passent de « space » a « ftl ». Leurs technologies sont
# de palier 2, et le palier 2 attend desormais l'emergence - c'est ce qui ferme
# le palier 3 et empeche la terraformation d'apparaitre a l'Age spatial. Ces
# batiments ne sont donc plus accessibles pendant le confinement. Ce n'est pas
# une perte : automatisation, cuves de clonage et centrales a plasma n'avaient
# rien a faire dans une civilisation qui n'a pas encore quitte son atmosphere.
BUILDING_TECH = {
    "building_automation_1": ("tech_assembly_pattern", "ftl"),
    "building_automation_farmer_1": ("tech_assembly_pattern", "ftl"),
    "building_automation_miner_1": ("tech_assembly_pattern", "ftl"),
    "building_automation_technician_1": ("tech_assembly_pattern", "ftl"),
    "building_clone_vats": ("tech_cloning", "ftl"),
    "building_energy_grid": ("tech_power_hub_1", "machine"),
    "building_energy_nexus": ("tech_power_hub_2", "atomic"),
    "building_factory_1": ("tech_basic_industry", "steam"),
    "building_factory_2": ("tech_luxuries_1", "industrial"),
    "building_farming_districts_1": ("tech_industrial_farming", "industrial"),
    "building_farming_districts_2": ("tech_eco_simulation", "machine"),
    "building_farming_districts_3": ("tech_gene_crops", "atomic"),
    "building_foundry_2": ("tech_alloys_1", "machine"),
    "building_generator_districts_1": ("tech_power_plant_1", "machine"),
    "building_generator_districts_2": ("tech_power_plant_2", "atomic"),
    "building_generator_districts_3": ("tech_power_plant_3", "ftl"),
    "building_mineral_purification_hub": ("tech_mineral_purification_2", "atomic"),
    "building_mineral_purification_plant": ("tech_mineral_purification_1", "industrial"),
    "building_mining_districts_1": ("tech_mechanized_mining", "industrial"),
    "building_mining_districts_2": ("tech_mining_1", "machine"),
    "building_mining_districts_3": ("tech_mining_2", "atomic"),
}
