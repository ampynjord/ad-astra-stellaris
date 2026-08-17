# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - table des 11 batiments d'epoque.

Chaque batiment est debloque par une techno d'epoque (voir age_techs_data.py) et
ne se construit que pendant le confinement. Une fois l'Ascension achevee, les
batiments deja construits restent : seule la construction de nouveaux se ferme.

ATTENTION : le schema exact des batiments a change avec la 4.0 (zones, districts).
Le gabarit vit dans gen_age_buildings.py, a un seul endroit : si un champ est
refuse par le jeu, il se corrige la et se repercute sur les 11 batiments.
"""

# Zones dans lesquelles chaque batiment peut etre eleve. Tous incluent
# `government` : c'est la zone de la capitale, la seule garantie sur une
# planete unique. Sans building_sets, le moteur refuse le batiment.
# 1.4 (18/08) : plus de set « farming » ni « mining ». La zone par defaut du
# district urbain (zone_default, jeu de base) inclut tout SAUF farming, mining,
# generator... : un batiment qui porte l'un de ces sets n'y est pas constructible,
# et n'a de place que dans la specialisation d'un district rural - que le joueur
# n'a pas forcement. Argroww (Discord, 17/08) : « after researching the tech that
# gives a Granary I have nowhere I can build it ». Le Grenier, le Moulin et la
# Fonderie se batissent donc en ville, comme le Monument et la Maison des tablettes.
SETS = {'building_adastra_cave': 'government unity', 'building_adastra_granary': 'government', 'building_adastra_foundry': 'government', 'building_adastra_tablet_house': 'government research', 'building_adastra_courthouse': 'government', 'building_adastra_mill': 'government', 'building_adastra_citadel': 'government fortress', 'building_adastra_university': 'government research', 'building_adastra_manufactory': 'government industrial factory', 'building_adastra_radio': 'government unity entertainment', 'building_adastra_school': 'government research'}

# Emploi cree par chaque batiment : la production vient de gens qui travaillent,
# pas d'un pourcentage abstrait. Scripts d'emplois du jeu de base, qui gerent
# deja les variantes gestalt et empire dechu.
# ATTENTION : le nom est celui du fichier dans common/inline_scripts/jobs/ du
# jeu de base, SANS prefixe. La 1.2 a ete publiee en interne avec
# « building_farmers_add » au lieu de « farmers_add » : le moteur ecrivait
# « Unknown inline_script » au chargement et les batiments d'epoque ne
# creaient AUCUN emploi. Rien ne le montrait en jeu, le batiment se
# construisait normalement.
JOBS = {
    'building_adastra_cave': 'unity_jobs_add',
    'building_adastra_granary': 'farmers_add',
    'building_adastra_foundry': 'miners_add',
    'building_adastra_tablet_house': 'researchers_add',
    'building_adastra_courthouse': 'enforcers_add',
    'building_adastra_mill': 'farmers_add',
    'building_adastra_citadel': 'soldiers_add',
    'building_adastra_university': 'researchers_add',
    'building_adastra_manufactory': 'factory_add',
    'building_adastra_radio': 'entertainers_add',
    'building_adastra_school': 'researchers_add',
}

# Nombre d'emplois par age, en variables du jeu de base.
AGE_JOBS = {
    "stone": "@building_static_jobs_low_3", "bronze": "@building_static_jobs_low_3",
    "iron": "@building_static_jobs_3", "medieval": "@building_static_jobs_3",
    "steam": "@building_static_jobs_low", "machine": "@building_static_jobs_low",
}

# La capitale d'epoque : posee au demarrage, pas construite par le joueur, donc
# hors de la liste BUILDINGS - mais sa localisation doit vivre au meme endroit.
# La chaine des capitales d'epoque. Posee au demarrage, jamais construite : le
# joueur l'AMELIORE d'un age a l'autre, et le dernier palier debouche sur
# l'Administration planetaire du jeu de base, qui reprend ensuite sa propre
# chaine (Centre administratif, Capitale systeme). Le siege du pouvoir suit donc
# la civilisation du cercle de pierres jusqu'aux ministeres.
#
# La techno prerequise d'un palier appartient a l'age PRECEDENT, jamais au sien.
# Deux raisons. D'abord un depart tardif : la capitale de l'age de depart doit
# etre posable le premier jour, or les technos de l'age de depart ne sont pas
# offertes - seules celles des ages deja traverses le sont. Ensuite le rythme :
# l'amelioration devient disponible vers la fin de l'age en cours, juste avant
# d'entrer dans le suivant, ce qui est exactement le moment ou le siege du
# pouvoir change de forme.
#
# Champs : cle, techno prerequise (None = pose au demarrage), age, nom FR/EN,
# description FR/EN, logement, agrements, emplois de colon, emplois de gardien.
# Les emplois sont en centiemes, convention du jeu de base : 100 = un emploi.
CAPITAL_CHAIN = [
    dict(key="building_adastra_seat", age="stone", tech=None,
         fr="Cercle de pierres", en="Ring of Stones",
         dfr="Pas un batiment : un endroit. On s'y assoit en rond parce que personne n'accepte d'etre derriere un autre.",
         den="Not a building: a place. People sit in a ring because nobody accepts standing behind anyone else.",
         housing=200, amenities=300, colonists=100, enforcers=0, cost=50),
    dict(key="building_adastra_seat_bronze", age="bronze", tech="tech_adastra_language",
         fr="Maison commune", en="Common House",
         dfr="Un toit assez grand pour contenir tout le monde en cas d'orage, et assez central pour qu'on sache ou aller quand ca ne va pas.",
         den="A roof big enough to hold everyone in a storm, and central enough that people know where to go when things go wrong.",
         housing=300, amenities=400, colonists=100, enforcers=0, cost=75),
    dict(key="building_adastra_seat_iron", age="iron", tech="tech_adastra_first_city",
         fr="Palais", en="Palace",
         dfr="Le pouvoir cesse de se deplacer et se met a habiter quelque part. C'est plus commode, et beaucoup plus dangereux.",
         den="Power stops travelling and starts living somewhere. That is more convenient, and far more dangerous.",
         housing=400, amenities=500, colonists=100, enforcers=100, cost=110),
    dict(key="building_adastra_seat_medieval", age="medieval", tech="tech_adastra_law",
         fr="Cour et chancellerie", en="Court and Chancery",
         dfr="Une salle pour trancher, une piece a cote pour ecrire ce qui a ete tranche. La seconde finira par compter davantage que la premiere.",
         den="A hall for ruling, a room next door for writing down what was ruled. The second will end up mattering more than the first.",
         housing=500, amenities=600, colonists=200, enforcers=100, cost=150),
    dict(key="building_adastra_seat_renaissance", age="renaissance", tech="tech_adastra_stone_architecture",
         fr="Hotel de ville", en="Town Hall",
         dfr="La ville se paie un batiment a elle, avec une horloge dessus. Elle annonce que le temps de tous vaut la peine d'etre affiche.",
         den="The city buys itself a building, with a clock on top. It announces that everyone's time is worth displaying.",
         housing=600, amenities=700, colonists=200, enforcers=200, cost=200),
    dict(key="building_adastra_seat_steam", age="steam", tech="tech_adastra_printing",
         fr="Palais du gouvernement", en="Government House",
         dfr="On y compte les habitants, on y leve l'impot, on y decide du trace des voies ferrees. L'Etat commence a savoir ce qu'il contient.",
         den="Here the inhabitants are counted, the taxes levied, the railway lines drawn. The state begins to know what it contains.",
         housing=750, amenities=800, colonists=300, enforcers=200, cost=260),
    dict(key="building_adastra_seat_industrial", age="industrial", tech="tech_adastra_steam_engine",
         fr="Ministeres", en="The Ministries",
         dfr="Le gouvernement ne tient plus dans une salle : il lui faut des couloirs, des services, des archives. Le dernier siege avant l'administration planetaire.",
         den="Government no longer fits in one hall: it needs corridors, departments, archives. The last seat before planetary administration.",
         housing=900, amenities=900, colonists=300, enforcers=300, cost=330),
]

# Entretien des sept sieges du pouvoir : (energie, minerais, nourriture).
# L'energie s'applique une fois le Reseau electrique connu ; sinon c'est le
# couple minerais/nourriture. Un palais coute a entretenir - on n'a jamais loge
# un gouvernement gratuitement.
CAPITAL_UPKEEP = [
    (1, 1, 1),   # Cercle de pierres
    (1, 1, 1),   # Maison commune
    (2, 2, 1),   # Palais
    (2, 2, 1),   # Cour et chancellerie
    (3, 3, 2),   # Hotel de ville
    (3, 3, 2),   # Palais du gouvernement
    (4, 4, 2),   # Ministeres
]

# Compatibilite : le premier palier reste designe par CAPITAL dans le reste de
# l'outillage.
CAPITAL = CAPITAL_CHAIN[0]

# Entretien d'AVANT l'electricite, en (minerais, nourriture).
#
# Le principe pose le 15/08 : couper la facture energetique ne veut pas dire
# rendre les batiments gratuits. Une civilisation pre-industrielle entretient
# ses ouvrages avec deux choses, et deux seulement - de la matiere qui s'use
# (pierre, bois, chaume, metal) et des bras qu'il faut nourrir. C'est donc en
# minerais et en nourriture que la facture est reecrite, pas en rien du tout.
#
# Le total vaut environ le double de la ligne energetique du meme age. Les
# excedents releves en jeu a l'age de pierre (+26 minerais, +21 nourriture par
# mois) laissent largement la place ; l'objectif est qu'un batiment se sente,
# pas qu'il etrangle.
AGE_UPKEEP_PRE = {
    "stone":    (1, 1),
    "bronze":   (1, 1),
    "iron":     (2, 1),
    "medieval": (2, 1),
    "steam":    (2, 2),
    "machine":  (3, 2),
}

# Cout et duree par age, appliques a tous les batiments de cet age.
AGE_COST = {
    "stone":    (40, 1, 240),
    "bronze":   (60, 1, 300),
    "iron":     (80, 2, 330),
    "medieval": (110, 2, 360),
    "steam":    (150, 3, 420),
    "machine":  (200, 3, 480),
}

ICONS = {'building_adastra_cave': 'building_autochthon_monument', 'building_adastra_granary': 'building_primitive_farm', 'building_adastra_foundry': 'building_primitive_mine', 'building_adastra_tablet_house': 'building_primitive_research', 'building_adastra_courthouse': 'building_low_tech_admin_hub', 'building_adastra_mill': 'building_food_processing_facility', 'building_adastra_citadel': 'building_stone_palace', 'building_adastra_university': 'building_primitive_labs', 'building_adastra_manufactory': 'building_primitive_factory', 'building_adastra_radio': 'building_pre_ftl_radio_telescope', 'building_adastra_school': 'building_state_academy'}


import re as _re
PROD_MOD = _re.compile(r"planet_jobs_\w+_produces_mult")

B = lambda key, age, tech, cat, fr, en, dfr, den, mods: dict(
    key=key, age=age, tech=tech, cat=cat, fr=fr, en=en, dfr=dfr, den=den,
    mods={k: v for k, v in mods.items() if not PROD_MOD.match(k)},
    icon=ICONS[key], job=JOBS[key], sets=SETS[key])

BUILDINGS = [
 B("building_adastra_cave", "stone", "tech_adastra_cave_art", "unity",
   "Monument des ancêtres", "Ancestral Monument",
   "Une pierre dressée à l'écart du campement, couverte de mains peintes. On y vient depuis quatre générations, et chaque génération ajoute la sienne à côté des autres.",
   "A stone raised apart from the camp, covered in painted hands. Four generations have come here, and each one adds its own beside the others.",
   {"planet_jobs_unity_produces_mult": 0.15, "planet_stability_add": 3}),

 B("building_adastra_granary", "bronze", "tech_adastra_agriculture", "resource",
   "Grenier", "Granary",
   "Le premier bâtiment que nous ayons construit pour un moment qui n'est pas encore arrivé. Une civilisation commence quand elle apprend à se méfier de l'hiver.",
   "The first building we ever raised for a moment that has not yet come. A civilisation begins when it learns to distrust the winter.",
   {"planet_jobs_food_produces_mult": 0.15, "planet_stability_add": 3}),

 B("building_adastra_foundry", "bronze", "tech_adastra_bronze", "manufacturing",
   "Fonderie", "Foundry",
   "Le feu y est entretenu jour et nuit. Le fondeur est le seul artisan que personne ne songe à contredire.",
   "The fire is kept alive day and night. The smelter is the one craftsman nobody thinks to argue with.",
   {"planet_jobs_minerals_produces_mult": 0.15}),

 B("building_adastra_tablet_house", "bronze", "tech_adastra_writing", "research",
   "Maison des tablettes", "House of Tablets",
   "On y apprend à tracer les signes, et surtout à les relire. Le premier endroit où le savoir survit à celui qui l'a écrit.",
   "Here one learns to draw the signs, and above all to read them back. The first place where knowledge outlives the one who wrote it.",
   {"planet_jobs_physics_research_produces_mult": 0.15, "planet_jobs_society_research_produces_mult": 0.15, "planet_jobs_engineering_research_produces_mult": 0.15}),

 B("building_adastra_courthouse", "iron", "tech_adastra_law", "government",
   "Tribunal", "Courthouse",
   "La loi y est affichée à l'entrée, lisible par quiconque sait lire. Le reste du bâtiment ne sert qu'à tenir cette promesse.",
   "The law is posted at the entrance, legible to anyone who can read. The rest of the building exists only to keep that promise.",
   {"planet_stability_add": 8, "planet_crime_add": -10}),

 B("building_adastra_mill", "medieval", "tech_adastra_mills", "resource",
   "Moulin", "Mill",
   "Il tourne tant que le vent souffle ou que l'eau descend, sans qu'on lui demande rien. Le premier ouvrier qui ne se plaint jamais - et il moud assez de grain pour nourrir un village entier.",
   "It turns as long as the wind blows or the water falls, asking nothing. The first worker who never complains - and it grinds enough grain to feed a whole village.",
   {"planet_jobs_food_produces_mult": 0.15}),

 B("building_adastra_citadel", "medieval", "tech_adastra_stone_architecture", "government",
   "Citadelle", "Citadel",
   "Des murs assez épais pour que la population entière puisse y tenir pendant un siège. On espère ne jamais avoir à vérifier.",
   "Walls thick enough to hold the whole population through a siege. One hopes never to have to check.",
   {"planet_housing_add": 5, "planet_stability_add": 5}),

 B("building_adastra_university", "medieval", "tech_adastra_scholasticism", "research",
   "Université", "University",
   "Une corporation de maîtres et d'élèves, avec ses propres règles et ses propres querelles. Elle survivra aux royaumes qui l'ont fondée.",
   "A corporation of masters and students, with its own rules and its own feuds. It will outlast the kingdoms that founded it.",
   {"planet_jobs_physics_research_produces_mult": 0.20, "planet_jobs_society_research_produces_mult": 0.20, "planet_jobs_engineering_research_produces_mult": 0.20}),

 B("building_adastra_manufactory", "steam", "tech_adastra_steam_engine", "manufacturing",
   "Manufacture", "Manufactory",
   "Le bruit s'entend depuis l'autre bout de la ville, et ne s'arrête jamais tout à fait. On y produit en un mois ce qu'un atelier faisait en un an.",
   "The noise carries across the town and never quite stops. A month here makes what a workshop made in a year.",
   {"planet_jobs_consumer_goods_produces_mult": 0.20}),

 B("building_adastra_radio", "machine", "tech_adastra_radio", "unity",
   "Station de radiodiffusion", "Broadcasting Station",
   "Un mât, un studio, et soudain la même voix dans chaque cuisine du pays. Personne n'a encore mesuré ce que cela va changer.",
   "A mast, a studio, and suddenly the same voice in every kitchen in the country. Nobody has yet measured what that will change.",
   {"planet_jobs_unity_produces_mult": 0.20, "planet_amenities_add": 5}),

 B("building_adastra_school", "machine", "tech_adastra_mass_education", "research",
   "École publique", "Public School",
   "Gratuite, obligatoire, et vivement contestée. Dans deux générations, plus personne ne se souviendra qu'elle a dû être imposée.",
   "Free, compulsory and fiercely contested. In two generations nobody will remember that it had to be imposed.",
   {"planet_jobs_physics_research_produces_mult": 0.15, "planet_jobs_society_research_produces_mult": 0.15, "planet_jobs_engineering_research_produces_mult": 0.15, "logistic_growth_mult": 0.10}),
]
