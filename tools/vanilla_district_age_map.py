# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - a quel age chaque district devient constructible.

CE QUI A ETE TROUVE (test du 13/08, capture de la barre de ressources)
    On avait verrouille les batiments, les zones et les technos, et l'energie
    montait quand meme de +11,50 par mois a l'Age de pierre. La source :
    la planete de depart porte deux DISTRICTS GENERATEURS, et un district cree
    ses emplois tout seul, sans batiment ni zone. Le troisieme etage du systeme
    de 4.4 nous avait echappe.

LA REGLE
    Meme principe que partout ailleurs : un district n'existe pas avant la
    technologie qui le rend possible. Ici la garde est une TECHNO et non un age,
    parce que c'est la ressource qu'elle produit qui est en jeu :
    - les generateurs produisent de l'energie -> Reseau electrique
    - les mines et les fermes existent depuis toujours : carriere et champ
    - le district urbain, c'est habiter quelque part : rien a verrouiller

VALEURS
    une techno : constructible a partir de cette techno
    "keep"     : disponible des le depart, aucun anachronisme
    "na"       : inatteignable par un empire Ad Astra, on ne touche a rien
"""

DISTRICT_TECH = {
    "district_city":      ("keep", "Habiter quelque part n'a pas d'epoque"),
    "district_mining":    ("keep", "La carriere est aussi vieille que l'outil de pierre"),
    "district_farming":   ("keep", "Le champ arrive avec l'agriculture, deja couverte par nos technos"),
    # « keep » ne veut pas dire « intact » : ces trois-la restent constructibles
    # des le premier jour, mais leur ENTRETIEN est paye en energie par le jeu de
    # base. Voir UPKEEP_SWAP juste en dessous.
    "district_generator": ("tech_adastra_electricity",
                           "Un district generateur produit de l'energie, et l'energie "
                           "c'est l'electricite : rien avant le Reseau electrique"),

    # Hors de portee d'un empire Ad Astra : on ne les surcharge pas.
    "district_hive":      ("na", "Esprit ruche"),
    "district_nexus":     ("na", "Empire machine"),
}

# Districts poses d'office sur la capitale au demarrage et anachroniques avant
# leur techno. Retires dans adastra.2, comme les zones.
STARTING_DISTRICTS_TO_REMOVE = {
    "district_generator": "Deux generateurs de base sur un monde qui n'a pas "
                          "l'electricite : +11,50 energie par mois a l'Age de pierre",
}


# --- Entretien d'epoque ---------------------------------------------------
# Releve en jeu le 13/08 : district agricole 0,30, district minier 0,20,
# districts urbains 0,60 - soit 1,10 energie par mois a l'Age de pierre, et un
# deficit rouge permanent puisque l'energie n'existe pas encore.
#
# On a d'abord essaye de l'annuler par modificateur
# (planet_structures_upkeep_mult, planet_districts_energy_upkeep_mult) : sans
# effet sur l'entretien des districts. On ecrit donc la regle la ou elle ne peut
# pas etre ignoree, dans la definition du district : un bloc upkeep accepte un
# trigger, exactement comme un bloc cost.
#
# Avant l'electricite, l'entretien passe en MINERAIS - un village entretient ses
# carrieres et ses champs avec du materiau et du travail, pas avec du courant.
# Le montant ne change pas, seule la ressource change.
#
# La garde passe par adastra_pays_energy_upkeep, qui laisse TOUS les autres
# empires sur l'energie : ces trois districts sont ceux de tout le monde.
# Le montant de remplacement est un couple (minerais, nourriture) : la matiere
# qui s'use d'un cote, les bras qu'il faut nourrir de l'autre. Le champ fait
# exception - un district agricole qui couterait de la nourriture serait absurde,
# il ne paie qu'en materiau.
UPKEEP_SWAP = {
    "district_city": [("energy = 2", (2, 1))],
    "district_mining": [("energy = 1", (1, 1))],
    "district_farming": [("energy = 1", (1, 0))],
}
