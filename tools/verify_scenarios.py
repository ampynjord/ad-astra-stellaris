#!/usr/bin/env python3
"""Contrats de regression pour les parcours jouables d'Ad Astra.

Ces controles ne lancent pas Stellaris : ils verifient les contrats source qui
ont deja casse des parties reelles. Ils completent les tests humains, ils ne
les remplacent pas.
"""
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
EVENTS = ROOT / "ad_astra" / "events" / "adastra_events.txt"
SITUATIONS = ROOT / "ad_astra" / "common" / "situations" / "zzz_adastra_situations.txt"
GFX = ROOT / "ad_astra" / "interface" / "adastra_event_pictures.gfx"
ART = ROOT / "artwork" / "event_pictures"
DDS = ROOT / "ad_astra" / "gfx" / "event_pictures"
LOCATIONS = (
    ROOT / "ad_astra" / "localisation" / "english" / "adastra_l_english.yml",
    ROOT / "ad_astra" / "localisation" / "french" / "adastra_l_french.yml",
)

errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def event_block(text, event_id):
	"""Extrait un evenement par son id sans confondre les blocs imbriques."""
	pattern = r"country_event\s*=\s*\{\s*id\s*=\s*adastra\." + re.escape(str(event_id)) + r"\b"
	for match in re.finditer(pattern, text):
		start = text.find("{", match.start())
		depth = 0
		for index in range(start, len(text)):
			char = text[index]
			if char == "{":
				depth += 1
			elif char == "}":
				depth -= 1
				if depth == 0:
					block = text[match.start():index + 1]
					if "is_triggered_only = yes" in block or "hide_window = yes" in block:
						return block
					break
	return ""


def has_localization(key, content):
    return bool(re.search(r"^\s*" + re.escape(key) + r":0\s+\"", content, re.MULTILINE))


def main():
    events = EVENTS.read_text(encoding="utf-8")
    situation = SITUATIONS.read_text(encoding="utf-8")
    gfx = GFX.read_text(encoding="utf-8") if GFX.exists() else ""
    localizations = [path.read_text(encoding="utf-8-sig") for path in LOCATIONS]

    # Choix de depart : les dix ages et leur initialisation ne doivent pas se perdre.
    picker = event_block(events, 1)
    choices = ("stone", "bronze", "iron", "medieval", "renaissance", "steam", "industrial", "machine", "atomic", "space")
    for age in choices:
        check("adastra_choice_%s" % age in picker, "choix de depart absent : %s" % age)
    check(picker.count("country_event = { id = adastra.2 }") == 10,
          "le choix de depart doit toujours lancer adastra.2 pour les dix ages")

    # La preparation est cachee mais l'age choisi doit etre annonce au joueur.
    init = event_block(events, 2)
    start = init.find("# La preparation cachee")
    end = init.find("# Fin d'initialisation")
    arrival = init[start:end] if start >= 0 and end > start else ""
    for index, age in enumerate(choices):
        if age == "space":
            check("else = { country_event = { id = adastra.59 } }" in arrival,
                  "arrivee initiale manquante pour l'age spatial")
        else:
            check("adastra_choice_%s" % age in arrival and "adastra.%d" % (50 + index) in arrival,
                  "arrivee initiale manquante pour l'age %s" % age)

    # Les arrivees reelles et initiales sont des popups localises et illustres.
    for index, age in enumerate(choices):
        event_id = 50 + index
        block = event_block(events, event_id)
        picture = "GFX_evt_adastra_age_%s" % age
        key = "adastra.%d.desc" % event_id
        check(block and "hide_window = yes" not in block, "adastra.%d doit rester visible" % event_id)
        check(picture in block, "adastra.%d doit employer %s" % (event_id, picture))
        for language, content in zip(("EN", "FR"), localizations):
            check(has_localization(key, content), "%s : localisation absente en %s" % (key, language))

    # Les quatre ecrans d'accueil doivent rester distincts, l'origine garde son image.
    expected_intro = {
        1: "GFX_evt_adastra_origins",
        4: "GFX_evt_adastra_welcome",
        5: "GFX_evt_adastra_pace",
        7: "GFX_evt_adastra_galaxy_pace",
    }
    for event_id, picture in expected_intro.items():
        check(picture in event_block(events, event_id),
              "adastra.%d doit employer %s" % (event_id, picture))

    # La situation ne doit jamais retomber sur une illustration vanilla.
    check("picture = GFX_evt_adastra_situation" in situation,
          "la situation d'ascension doit avoir son illustration dediee")
    required_images = ("welcome", "pace", "galaxy_pace", "situation")
    for name in required_images:
        sprite = "GFX_evt_adastra_%s" % name
        check(sprite in gfx, "sprite d'evenement absent : %s" % sprite)
        check((ART / ("adastra_%s.png" % name)).is_file(), "source image absent : %s" % name)
        check((DDS / ("adastra_%s.dds" % name)).is_file(), "DDS absent : %s" % name)

    # Les jalons spatiaux restent fondes sur des actions et non sur une horloge.
    contracts = {
        71: "adastra_stage_first_launch",
        72: "adastra_stage_program_explore",
        73: "adastra_stage_program_constructor",
        74: "adastra_stage_program_outpost",
        75: "adastra_stage_program_orbital",
        76: "adastra_stage_program_hyperdrive",
    }
    for event_id, token in contracts.items():
        check(token in event_block(events, event_id),
              "jalon spatial adastra.%d incomplet (%s absent)" % (event_id, token))

    # Le lancement est explicite : la recherche spatiale se termine avant
    # la decision, et le joueur recoit une fenetre qui indique le prochain geste.
    launch = event_block(events, 79)
    check(launch and "hide_window" not in launch,
          "adastra.79 doit annoncer le premier lancement au joueur")
    check("GFX_evt_adastra_age_space" in launch,
          "adastra.79 doit employer l'illustration de l'Age spatial")
    for localization in localizations:
        check(has_localization("adastra.79.desc", localization),
              "localisation manquante pour l'annonce du premier lancement")

    # Civil Education donne une Academie d'Etat au depart vanilla. Cette
    # structure consomme de l'energie : Ad Astra doit la reporter avant le
    # Reseau electrique, puis la recreer sur la capitale apres son invention.
    resources = event_block(events, 11)
    check("remove_building = building_state_academy" in resources,
          "Civil Education : Academie d'Etat non reportee avant l'electricite")
    check("capital_scope" in resources and
          "add_building = building_state_academy" in resources,
          "Civil Education : Academie d'Etat non restauree apres l'electricite")

    if errors:
        print("== scenarios de regression ==")
        for error in errors:
            print("ERREUR : " + error)
        return 1
    print("scenarios de regression : 0 erreur")
    return 0


if __name__ == "__main__":
    sys.exit(main())
