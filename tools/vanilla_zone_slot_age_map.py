#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sources de verite des emplacements de zones urbaines progressifs.

Depuis Stellaris 4.4, un district urbain contient une zone gouvernementale et
deux emplacements de specialisation. Le jeu de base ouvre le premier des le
depart et le second aux primitifs, ce qui donne a une civilisation de pierre
sa capacite de ville moderne. Ad Astra les ouvre avec les savoirs qui les
justifient, sans changer les autres empires.
"""

# (technologie, cle de localisation, justification)
CITY_ZONE_SLOT_TECH = {
    "slot_city_01": (
        "tech_adastra_first_city",
        "adastra_zone_city_01_prereq",
        "La Premiere cite organise le premier quartier urbain specialise",
    ),
    "slot_city_02": (
        "tech_adastra_law",
        "adastra_zone_city_02_prereq",
        "Le Code de lois permet une seconde institution urbaine specialisee",
    ),
}
