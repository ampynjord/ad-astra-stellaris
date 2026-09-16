#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - controles automatiques avant deploiement.

Verifie ce qui peut l'etre hors ligne. Les noms de modificateurs, eux, ne sont
verifiables que contre les fichiers vanilla : la liste est imprimee en fin de
rapport pour un grep une fois le PC en ligne.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from age_techs_data import (AGES, TECHS, ANNEES, BORNES,  # noqa: E402
                            TECHS_PAR_AGE, vagues)

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ad_astra")
AREAS = ("physics", "society", "engineering")
errors, warnings = [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def strip_comments(text):
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


# ---------------------------------------------------------------- accolades

print("== equilibrage des accolades ==")
for dirpath, _d, files in os.walk(ROOT):
    for name in sorted(files):
        if not name.endswith(".txt"):
            continue
        path = os.path.join(dirpath, name)
        with open(path, encoding="utf-8") as f:
            body = strip_comments(f.read())
        d = body.count("{") - body.count("}")
        rel = os.path.relpath(path, ROOT)
        if d:
            err("accolades desequilibrees (%+d) : %s" % (d, rel))
        elif name.startswith("adastra_age") or "age_gates" in name:
            print("  ok  %s" % rel)

# ------------------------------------------------------------- techs / cles
print("\n== illustration de l'origine ==")
_origine = os.path.join(ROOT, "common", "governments", "civics", "zzz_adastra_origins.txt")
_origine_gfx = os.path.join(ROOT, "interface", "adastra_event_pictures.gfx")
_origine_dds = os.path.join(ROOT, "gfx", "event_pictures", "adastra_origins.dds")
if not os.path.exists(_origine) or "picture = GFX_evt_adastra_origins" not in open(_origine, encoding="utf-8").read():
    err("origine : illustration Ad Astra absente")
elif not os.path.exists(_origine_gfx) or "name = \"GFX_evt_adastra_origins\"" not in open(_origine_gfx, encoding="utf-8").read():
    err("origine : sprite de l'illustration absent")
elif not os.path.exists(_origine_dds):
    err("origine : illustration DDS absente")
else:
    print("  illustration 450x150 declaree")

print("\n== illustrations des evenements ==")
_evenements = os.path.join(ROOT, "events")
_pics = []
for _nom in sorted(os.listdir(_evenements)):
    if not _nom.endswith(".txt"):
        continue
    _texte = open(os.path.join(_evenements, _nom), encoding="utf-8").read()
    _pics += re.findall(r"^\s*picture\s*=\s*(GFX_evt_\w+)", _texte, re.M)
_vanilla_pics = sorted({p for p in _pics if not p.startswith("GFX_evt_adastra_")})
_sprites = open(_origine_gfx, encoding="utf-8").read() if os.path.exists(_origine_gfx) else ""
_missing_pics = sorted({p for p in _pics if p not in _sprites})
if _vanilla_pics:
    err("evenements : illustrations vanilla restantes : %s" % ", ".join(_vanilla_pics))
elif _missing_pics:
    err("evenements : sprites Ad Astra manquants : %s" % ", ".join(_missing_pics))
else:
    print("  %d fenetre(s), toutes avec une illustration Ad Astra" % len(_pics))

# ------------------------------------------------------------- techs / cles
print("\n== techs d'age ==")
keys = []
for age, flag, cost, vflag in AGES:
    keys += [t["key"] for t in TECHS[age]]
dupes = {k for k in keys if keys.count(k) > 1}
if dupes:
    err("cles de tech en double : %s" % ", ".join(sorted(dupes)))
print("  %d techs, %d cles uniques" % (len(keys), len(set(keys))))

for age, flag, cost, vflag in AGES:
    got = {a: 0 for a in AREAS}
    for t in TECHS[age]:
        if t["area"] not in AREAS:
            err("area inconnue '%s' pour %s" % (t["area"], t["key"]))
        else:
            got[t["area"]] += 1
    missing = [a for a in AREAS if got[a] == 0]
    if missing:
        err("age %s : aucune tech en %s (file de recherche vide dans cette area)"
            % (age, "/".join(missing)))
    # 1.2 : 10 technos par age, dont au moins 3 dans chacune des trois areas.
    # En dessous de 3, une area n'a plus de choix reel : la file propose 3
    # options a la fois, elle serait pleine des la premiere.
    # 1.3 : cible 25 par age. Un age encore a 10 n'est pas une faute, c'est un
    # chantier en cours - on le dit, sans crier.
    _n = len(TECHS[age])
    if _n == TECHS_PAR_AGE:
        pass
    elif _n in (7, 10) or _n < TECHS_PAR_AGE:
        print("   age %-12s %2d/%d - reprise 1.3 a faire" % (age, _n, TECHS_PAR_AGE))
    else:
        warn("age %s : %d techs (%d attendues)" % (age, _n, TECHS_PAR_AGE))
    thin = [a for a in AREAS if got[a] < 3]
    if thin:
        warn("age %s : seulement %s tech(s) en %s - pas de choix reel dans cette area"
             % (age, "/".join(str(got[a]) for a in thin), "/".join(thin)))
    print("  %-12s %d techs  phys=%d soc=%d eng=%d  cout=%d  vanilla=%s"
          % (age, len(TECHS[age]), got["physics"], got["society"],
             got["engineering"], cost, vflag or "-"))

# ------------------------------------------------------------- prerequis
print("\n== prerequis ==")
tech_file = os.path.join(ROOT, "common", "technology", "adastra_age_techs.txt")
src = open(tech_file, encoding="utf-8").read()
declared = set(re.findall(r"^(tech_adastra_\w+) = \{", src, re.M))
if declared != set(keys):
    err("desync entre la table et le fichier genere : %s"
        % (declared.symmetric_difference(set(keys))))

# Le programme spatial reste volontairement sous les premiers couts vanilla.
# Cette plage garde une progression lisible sans faire depasser nos cartes
# par les technologies tier 1 disponibles apres l'emergence.
_space_costs = {}
for _tech in TECHS["space"]:
    _match = re.search(r"^%s = \{.*?^\}" % re.escape(_tech["key"]), src, re.S | re.M)
    if not _match:
        continue
    _cost = re.search(r"^\s*cost\s*=\s*(\d+)", _match.group(0), re.M)
    if not _cost:
        err("%s : cout absent" % _tech["key"])
        continue
    _space_costs[_tech["key"]] = int(_cost.group(1))
if _space_costs and (min(_space_costs.values()) < 500 or max(_space_costs.values()) >= 1000):
    err("les technologies spatiales doivent rester entre les premiers couts vanilla")
elif _space_costs:
    print("  programme spatial : couts %d-%d, alignes sur les premiers paliers vanilla"
          % (min(_space_costs.values()), max(_space_costs.values())))
refs = re.findall(r'prerequisites = \{ ([^}]+) \}', src)
bad = set()
for r in refs:
    for k in re.findall(r'"([^"]+)"', r):
        if k not in declared:
            bad.add(k)
if bad:
    err("prerequis pointant vers une tech inexistante : %s" % ", ".join(sorted(bad)))
first_age = AGES[0][0]
# 1.5 : a la Pierre, seules les techs de rang 1 sont des racines ; les rangs
# 2-5 sont chaines dans l'age comme partout ailleurs.
roots = [t["key"] for t in TECHS[first_age] if vagues(TECHS[first_age])[t["key"]] == 1]
n_with = len(refs)
print("  %d techs avec prerequis, %d racines (age %s)" % (n_with, len(roots), first_age))
if n_with + len(roots) != len(keys):
    err("certaines techs hors age initial n'ont pas de prerequis")

# La progression est portee par les recherches et leurs prerequis, jamais par
# une vague qui injecte des options dans le vivier. Une telle injection rend
# les technologies instantanees des qu'un age est atteint.
_grants = open(os.path.join(ROOT, "common", "scripted_effects",
                      "zz_adastra_age_grants.txt"), encoding="utf-8").read()
_events = open(os.path.join(ROOT, "events", "adastra_events.txt"), encoding="utf-8").read()
if "adastra_offre_age_" in _grants:
    err("les effets generes contiennent encore des vagues de recherche")
if "id = adastra.130" in _events or "adastra_offre_age_" in _events:
    err("adastra_events reinjecte encore des technologies d'age")
_capital_start = _events[_events.index("# 1.2 : la capitale demarre specialisee"):
                         _events.index("# 1.2 : les DISTRICTS aussi.")]
_day4_start = _events[_events.index("id = adastra.8"):
                      _events.index("# adastra.9 : Garde mensuelle")]
for _archive_fragment in (
    "add_zone = { district = district_city zone = zone_research_unity",
    "add_building = { district = district_city zone = zone_research_unity building = building_research_lab_1 }",
):
    if _archive_fragment in _capital_start or _archive_fragment in _day4_start:
        err("depart : les Archives et leur laboratoire ne doivent pas etre offerts")
if "remove_zone = { district = district_city zone = zone_research_unity }" not in _day4_start:
    err("depart : les Archives ne sont pas retirees apres l'initialisation vanilla")
if "num_districts = { type = district_city value > 1 }" not in _day4_start:
    err("depart : les districts urbains excedentaires ne sont pas retires apres l'initialisation vanilla")

# La garde mensuelle pre-PRL retire les bases prematurees, mais ne doit jamais
# supprimer les flottes que le joueur vient de construire.
_monthly_guard = _events[_events.index("# adastra.9 : Garde mensuelle"):
                        _events.index("# adastra.5 : Le rythme de l'ascension")]
if "delete_fleet" in _monthly_guard:
    err("garde pre-PRL : une flotte construite par le joueur serait detruite")
elif "dismantle = yes" not in _monthly_guard:
    err("garde pre-PRL : le nettoyage des bases prematurees est absent")
else:
    print("  garde pre-PRL : bases prematurees nettoyees, flottes preservees")

# ------------------------------------------------------------- localisation
print("\n== localisation ==")


def loc_keys(path):
    out = set()
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            m = re.match(r"\s*([A-Za-z0-9_.]+):\d*\s+\"", line)
            if m:
                out.add(m.group(1))
    return out


fr = loc_keys(os.path.join(ROOT, "localisation", "french", "adastra_ages_l_french.yml"))
en = loc_keys(os.path.join(ROOT, "localisation", "english", "adastra_ages_l_english.yml"))
if fr != en:
    err("parite FR/EN rompue : FR seulement %s | EN seulement %s"
        % (sorted(fr - en), sorted(en - fr)))
expected = set()
for k in keys:
    expected.add(k)
    expected.add(k + "_desc")
if fr != expected:
    err("cles de loc manquantes/en trop : %s" % sorted(expected.symmetric_difference(fr)))
print("  %d cles FR, %d cles EN, parite ok" % (len(fr), len(en)))

# ------------------------------------------------------------- verrous
print("\n== verrous vanilla ==")
gates = open(os.path.join(ROOT, "common", "scripted_triggers",
                          "zz_adastra_age_gates.txt"), encoding="utf-8").read()
for age, flag, cost, vflag in AGES:
    if not vflag:
        continue
    if "adastra_vanilla_open_%s = {" % age not in gates:
        err("declencheur adastra_vanilla_open_%s absent" % age)
    if "has_country_flag = adastra_completed" not in gates:
        err("filet de securite adastra_completed absent des verrous")
used = set()
for name in ("zzz_adastra_tech_overrides.txt", "zzz_adastra_tier1_overrides.txt"):
    body = open(os.path.join(ROOT, "common", "technology", name), encoding="utf-8").read()
    used |= set(re.findall(r"adastra_vanilla_open_(\w+) = yes", body))
    raw = re.findall(r"has_country_flag = adastra_unlock_(\w+)", body)
    for r in raw:
        if r != "ftl":
            err("%s : drapeau brut adastra_unlock_%s encore utilise comme garde"
                % (name, r))
for age in sorted(used):
    if "adastra_vanilla_open_%s = {" % age not in gates:
        err("garde adastra_vanilla_open_%s utilisee mais non definie" % age)
print("  verrous utilises : %s" % ", ".join(sorted(used)))

gfx = open(os.path.join(ROOT, "interface", "adastra_icons.gfx"), encoding="utf-8").read()

# -------------------------------------------- repartition historique vanilla
print("\n== technos vanilla de depart par age ==")
from vanilla_age_map import VANILLA_AGE_MAP  # noqa: E402
from clausewitz import top_level_blocks  # noqa: E402

ovr = open(os.path.join(ROOT, "common", "technology",
                        "zzz_adastra_tech_overrides.txt"), encoding="utf-8").read()
by_age = {}
seen = set()
for key, s, e in top_level_blocks(ovr):
    seen.add(key)
    if key not in VANILLA_AGE_MAP:
        err("techno %s presente dans les overrides mais absente de vanilla_age_map" % key)
        continue
    want_age, _grant = VANILLA_AGE_MAP[key]
    block = ovr[s:e]
    m = re.search(r"adastra_vanilla_open_(\w+) = yes", block)
    got = m.group(1) if m else ("ftl" if "adastra_unlock_ftl" in block else "?")
    if got != want_age:
        err("%s : garde sur '%s' alors que la carte dit '%s'" % (key, got, want_age))
    by_age.setdefault(want_age, []).append(key)
for key in VANILLA_AGE_MAP:
    if key not in seen:
        err("carte : %s n'a aucun bloc d'override" % key)

# Exceptions assumees : technos d'un age anterieur re-octroyees a l'Age spatial
# parce qu'une techno du paquet spatial en depend, ou parce qu'un composant de
# nos propres modeles de vaisseaux l'exige.
#
# tech_fission_power : nos quatre coques sous-luminiques declarent toutes
# « required_component = CORVETTE_FISSION_REACTOR ». Sans fission, aucun de nos
# vaisseaux n'existe - et les impulseurs (tech_reactor_boosters_1) la reclament
# aussi comme prerequis. Elle garde son verrou d'Age de l'atome : on ne fait que
# rattraper le joueur qui serait arrive au ciel sans elle.
OCTROIS_DE_PREREQUIS = {"tech_fission_power"}

grants = open(os.path.join(ROOT, "events", "adastra_events.txt"), encoding="utf-8").read()
granted = set(re.findall(r"give_technology = \{ tech = (\w+)", grants))
for age, _f, _c, _v in AGES:
    vt = by_age.get(age, [])
    g = [t for t in vt if VANILLA_AGE_MAP[t][1]]
    print("  %-12s %2d techno(s) vanilla, dont %d offerte(s)" % (age, len(vt), len(g)))
    if age != "space" and g:
        err("age %s : %d techno(s) vanilla offerte(s) a l'entree - elles passeraient"
            " avant les technos d'epoque du meme age" % (age, len(g)))
for t, (age, grant) in VANILLA_AGE_MAP.items():
    if grant and t not in granted:
        err("%s marquee offerte dans la carte mais absente des events" % t)
    if not grant and t in granted and t not in OCTROIS_DE_PREREQUIS:
        err("%s encore offerte dans les events alors que la carte dit non" % t)

# ------------------------------------------------------------- batiments
print("\n== batiments d'epoque ==")
from age_buildings_data import AGE_COST, BUILDINGS  # noqa: E402

bsrc = open(os.path.join(ROOT, "common", "buildings",
                         "adastra_age_buildings.txt"), encoding="utf-8").read()
bdecl = [k for k, _s, _e in top_level_blocks(bsrc)]
if len(bdecl) != len(BUILDINGS):
    err("%d batiments generes pour %d dans la table" % (len(bdecl), len(BUILDINGS)))
cap = os.path.join(ROOT, "common", "buildings", "zzz_adastra_capital.txt")
if not os.path.exists(cap) or "building_adastra_seat" not in open(cap, encoding="utf-8").read():
    err("capitale d'epoque absente")
elif "has_origin = origin_adastra" not in open(cap, encoding="utf-8").read():
    err("capitale d'epoque : garde d'origine absente")
if len(set(bdecl)) != len(bdecl):
    err("cles de batiment en double")
for b in BUILDINGS:
    if b["tech"] not in declared:
        err("batiment %s : prerequis %s inexistant" % (b["key"], b["tech"]))
    if b["age"] not in AGE_COST:
        err("batiment %s : age %s absent de AGE_COST" % (b["key"], b["age"]))
    if "GFX_adastra_age_%s" % b["age"] not in gfx:
        err("batiment %s : sprite GFX_adastra_age_%s non defini dans adastra_icons.gfx"
            % (b["key"], b["age"]))
bfr = loc_keys(os.path.join(ROOT, "localisation", "french", "adastra_buildings_l_french.yml"))
ben = loc_keys(os.path.join(ROOT, "localisation", "english", "adastra_buildings_l_english.yml"))
bexp = set()
for b in BUILDINGS:
    bexp.add(b["key"])
    bexp.add(b["key"] + "_desc")
# les capitales d'epoque ne sont pas dans la table des batiments d'epoque :
# elles ne se construisent pas, elles s'ameliorent d'un age a l'autre.
from age_buildings_data import CAPITAL_CHAIN  # noqa: E402
for _c in CAPITAL_CHAIN:
    bexp.add(_c["key"])
    bexp.add(_c["key"] + "_desc")
if bfr != ben:
    err("parite FR/EN des batiments rompue : %s" % sorted(bfr.symmetric_difference(ben)))
if bfr != bexp:
    err("cles de loc de batiment manquantes/en trop : %s" % sorted(bexp.symmetric_difference(bfr)))
if "potential" in bsrc and "adastra_completed" not in bsrc:
    err("les batiments ne referencent pas adastra_completed : la construction"
        " resterait ouverte apres l'emergence")

# building_sets : un nom invalide ne produit AUCUNE erreur dans error.log, le
# batiment disparait simplement de toutes les zones. C'est comme ca que le
# Tribunal avait ete publie avec « building_government » au lieu de
# « government » : genere, valide, invisible en jeu. Liste relevee sur les 498
# batiments du jeu de base 4.4.6.
VALID_SETS = {
    "government", "urban", "unity", "research", "industrial", "foundry",
    "factory", "farming", "generator", "mining", "physics", "society",
    "engineering", "trade", "fortress", "entertainment", "medical", "pre_ftl",
    "resort", "harvest", "hydroponics", "automation", "urban_automation", "betharian", "zoo",
    "adastra_food_storage",
    "knights", "origin", "bio_trophy", "hunting_zone", "fallen_empire",
    "cosmogenesis_world", "ark_forever_cruise_crew",
    "ark_forever_cruise_passengers",
}
for m in re.finditer(r"(\w+) = \{[^{}]*?building_sets = \{([^}]*)\}", bsrc, re.S):
    bad = [w for w in m.group(2).split() if w not in VALID_SETS]
    if bad:
        err("batiment %s : building_sets inconnu(s) %s - le batiment"
            " n'apparaitra dans aucune zone" % (m.group(1), bad))
if any("government" in b["sets"].split() for b in BUILDINGS):
    err("batiment d'epoque dans le set government : les zones Ad Astra ne l'incluent pas")
if any("urban_automation" in b["sets"].split() for b in BUILDINGS):
    err("batiment d'epoque dans urban_automation : il contournerait les specialisations")
EXPECTED_AGE_BUILDING_SETS = {
    "building_adastra_cave": {"unity"},
    "building_adastra_granary": {"adastra_food_storage"},
    "building_adastra_foundry": {"industrial", "foundry"},
    "building_adastra_tablet_house": {"research"},
    "building_adastra_courthouse": {"unity"},
    "building_adastra_mill": {"adastra_food_storage"},
    "building_adastra_citadel": {"fortress"},
    "building_adastra_university": {"research"},
    "building_adastra_manufactory": {"industrial", "factory"},
    "building_adastra_radio": {"unity"},
    "building_adastra_school": {"research"},
}
for _building in BUILDINGS:
    _got_sets = set(_building["sets"].split())
    _want_sets = EXPECTED_AGE_BUILDING_SETS[_building["key"]]
    if _got_sets != _want_sets:
        err("batiment %s : ensembles %s au lieu de %s"
            % (_building["key"], sorted(_got_sets), sorted(_want_sets)))
print("  %d batiments, %d cles de loc, parite ok" % (len(bdecl), len(bfr)))


# ------------------------------- parite FR/EN globale (1.2)
# Les controles precedents ne couvrent que les technos et les batiments. Celui-ci
# compare TOUTES les cles des deux dossiers de localisation : une cle presente
# d'un seul cote s'affiche en brut pour la moitie des joueurs, et rien ne le
# signale en jeu.
print("\n== parite francais / anglais ==")


def _loc_keys(d):
    out = {}
    for f in sorted(os.listdir(d)):
        if not f.endswith(".yml"):
            continue
        for line in open(os.path.join(d, f), encoding="utf-8-sig"):
            m = re.match(r'\s*([A-Za-z0-9_.]+):\d*\s+"(.*)"\s*$', line)
            if m:
                out[m.group(1)] = (f, m.group(2))
    return out


_fr = _loc_keys(os.path.join(ROOT, "localisation", "french"))
_en = _loc_keys(os.path.join(ROOT, "localisation", "english"))
_only_fr = sorted(set(_fr) - set(_en))
_only_en = sorted(set(_en) - set(_fr))
if _only_fr:
    err("%d cle(s) sans version anglaise : %s"
        % (len(_only_fr), ", ".join(_only_fr[:6])))
if _only_en:
    err("%d cle(s) sans version francaise : %s"
        % (len(_only_en), ", ".join(_only_en[:6])))
_vides = sorted(k for k, (_f, v) in _fr.items() if not v.strip())
_vides += sorted(k for k, (_f, v) in _en.items() if not v.strip())
if _vides:
    err("cle(s) de localisation vide(s) : %s" % ", ".join(sorted(set(_vides))[:6]))
# meme texte des deux cotes sur une phrase : signe d'un oubli de traduction
_jumeaux = sorted(k for k in set(_fr) & set(_en)
                  if _fr[k][1] == _en[k][1] and len(_fr[k][1]) > 25)
if _jumeaux:
    warn("%d cle(s) au texte identique en FR et EN, traduction probablement"
         " oubliee : %s" % (len(_jumeaux), ", ".join(_jumeaux[:6])))
_ffr = {f for f, _v in _fr.values()}
_fen = {f for f, _v in _en.values()}
if {f.replace("_l_french", "") for f in _ffr} != {f.replace("_l_english", "") for f in _fen}:
    warn("les deux dossiers de localisation n'ont pas les memes fichiers : %s / %s"
         % (sorted(_ffr), sorted(_fen)))
print("  %d cles, parite exacte des deux cotes" % len(_fr))

# Les titres, descriptions, options et noms de flotte font reference a des
# cles de localisation. Une cle commune absente des deux langues ne serait pas
# detectee par la parite seule et apparaitrait brute en jeu.
print("\n== references de texte visibles ==")
_visible_refs = {}
_visible_fields = r"(?:title|desc|name|custom_tooltip|tooltip|text)"
for _base, _dirs, _files in os.walk(ROOT):
    _rel_base = os.path.relpath(_base, ROOT)
    if _rel_base.startswith("localisation") or _rel_base.startswith("gfx"):
        continue
    for _file in _files:
        if not _file.endswith(".txt"):
            continue
        _path = os.path.join(_base, _file)
        for _number, _line in enumerate(open(_path, encoding="utf-8"), 1):
            _line = _line.split("#", 1)[0]
            _match = re.search(r"\b%s\s*=\s*\"?([A-Za-z0-9_.]+)\"?" % _visible_fields,
                               _line)
            if not _match:
                continue
            _key = _match.group(1)
            if _key.startswith(("adastra", "decision_core_", "origin_adastra",
                                "tech_adastra", "building_adastra", "core_")):
                _visible_refs.setdefault(_key, []).append("%s:%d" % (_path, _number))
for _lang, _loc in (("FR", _fr), ("EN", _en)):
    _missing = sorted(set(_visible_refs) - set(_loc))
    if _missing:
        err("%s : %d reference(s) de texte visible sans localisation : %s"
            % (_lang, len(_missing), ", ".join(_missing[:6])))
print("  %d reference(s) visibles, FR et EN" % len(_visible_refs))

# --------------------------- retours visibles des Premiers pas (1.4)
# La parite FR/EN ne suffit pas : deux dossiers peuvent oublier exactement les
# memes cles. Le chargement du 17/08 affichait alors les evenements core_ avec
# leur identifiant brut. Toute cle locale referencee par leurs titres, textes,
# options ou infobulles doit exister dans les deux langues.
print("\n== localisation des Premiers pas ==")
_core_refs = set()
for _rel in (os.path.join("events", "core_premiers_pas_events.txt"),
             os.path.join("common", "decisions", "core_premiers_pas.txt"),
             os.path.join("common", "decisions", "core_sonde_profonde.txt")):
    _path = os.path.join(ROOT, _rel)
    if not os.path.exists(_path):
        err("Premiers pas : fichier absent : %s" % _rel)
        continue
    _body = strip_comments(open(_path, encoding="utf-8").read())
    _core_refs |= set(re.findall(
        r'\b(?:title|desc|name|custom_tooltip)\s*=\s*"?((?:adastra\.\d+\.|decision_core_)\w+)"?',
        _body))
for _lang, _loc in (("FR", _fr), ("EN", _en)):
    _missing = sorted(_core_refs - set(_loc))
    if _missing:
        err("Premiers pas : %d cle(s) absente(s) en %s : %s"
            % (len(_missing), _lang, ", ".join(_missing[:6])))
print("  %d cle(s) visibles, FR et EN" % len(_core_refs))

# -------------------------------- logique des Premiers pas (1.4)
# Le risque de lancement est une promesse de jeu : 50, 40, 30, 20 puis 10 %.
# Une random_list ne peut pas prendre une variable comme poids ; les cinq
# tirages doivent donc rester explicites. Les cibles de recherche sont locales
# au pays, jamais globales, pour ne pas survivre a un autre lancement.
print("\n== logique des Premiers pas ==")
_core_path = os.path.join(ROOT, "events", "core_premiers_pas_events.txt")
_core = strip_comments(open(_core_path, encoding="utf-8").read())
if re.search(r"save_global_event_target_as\s*=\s*core_", _core):
    err("Premiers pas : une cible core_ est globale et peut fuir entre empires")
for _echec, _succes in ((50, 50), (40, 60), (30, 70), (20, 80), (10, 90)):
    _fail = "%d = { country_event = { id = adastra.101 } }" % _echec
    _ok = "%d = { country_event = { id = adastra.103 } }" % _succes
    if _fail not in _core or _ok not in _core:
        err("Premiers pas : palier de lancement %d/%d absent" % (_echec, _succes))
if "clear_variable = core_risque" not in _core:
    err("Premiers pas : core_risque n'est pas nettoye apres le tirage")
_m103 = re.search(r"country_event = \{\s*\n\tid = adastra\.103(.*?)\n\}",
                  _core, re.S)
if not _m103 or "set_country_flag = core_suborbital_fait" not in _m103.group(1):
    err("Premiers pas : la reussite suborbitale ne pose plus son drapeau")
if not _m103 or "set_situation_progress = 275" in _m103.group(1):
	err("Premiers pas : le lancement suborbital ne doit pas ouvrir seul le programme spatial")
_m102 = re.search(r"country_event = \{\s*\n\tid = adastra\.102(.*?)\n\}",
                  _core, re.S)
if not _m102 or "set_country_flag = core_satellite_fait" not in _m102.group(1):
	err("Premiers pas : la reussite du premier satellite ne pose plus son drapeau")
_m110 = re.search(r"country_event = \{\s*\n\tid = adastra\.110(.*?)\n\}",
                  _core, re.S)
if (not _m110 or "set_country_flag = core_sonde_profonde_fait" not in _m110.group(1)
        or "set_situation_progress = 275" not in _m110.group(1)):
	err("Premiers pas : seule la sonde profonde doit conclure les jalons orbitaux")
_m71 = re.search(r"country_event = \{\s*\n\tid = adastra\.71(.*?)\n\}",
                 open(os.path.join(ROOT, "events", "adastra_events.txt"), encoding="utf-8").read(), re.S)
if (not _m71 or "core_suborbital_fait" not in _m71.group(1)
		or "core_satellite_fait" not in _m71.group(1)
		or "core_vol_habite_fait" not in _m71.group(1)
		or "core_sonde_profonde_fait" not in _m71.group(1)
        or "adastra_stage_early_space_age" not in _m71.group(1)
        or "adastra_stage_first_launch" not in _m71.group(1)
        or "adastra_recalage_progression = yes" not in _m71.group(1)
        or "set_situation_progress = 275" not in _m71.group(1)):
	err("Premiers pas : le seuil spatial ne recale pas les recherches spatiales ou le lancement")
_m132 = re.search(r"country_event = \{\s*\n\tid = adastra\.132(.*?)\n\}",
                  open(os.path.join(ROOT, "events", "adastra_events.txt"), encoding="utf-8").read(), re.S)
if (not _m132 or "has_country_flag = adastra_reached_space" not in _m132.group(1)
        or "adastra_recalage_progression = yes" not in _m132.group(1)):
	err("Premiers pas : les commandes de recherche ne recalculent plus l Age spatial immediatement")
_age_techs = open(os.path.join(ROOT, "common", "technology", "adastra_age_techs.txt"),
                  encoding="utf-8").read()
_space_techs = re.search(r"# AGE : SPACE.*", _age_techs, re.S)
if not _space_techs or "has_country_flag = adastra_stage_" in _space_techs.group(0):
	err("Progression spatiale : une technologie d Age spatial attend encore une etape qu elle doit elle-meme permettre d atteindre")
# La mission de 1969 est explicitement lunaire. Sans lune dans le systeme
# natal, elle ne doit jamais etre proposee au joueur.
_core_decisions_path = os.path.join(ROOT, "common", "decisions", "core_premiers_pas.txt")
_core_decisions = strip_comments(open(_core_decisions_path, encoding="utf-8").read())
_suborbital = re.search(r"decision_core_suborbital\s*=\s*\{(.*?)\n\}", _core_decisions, re.S)
if (not _suborbital or "adastra_stage_first_launch" not in _suborbital.group(1)
        or "NOT = { has_country_flag = core_suborbital_fait }" not in _suborbital.group(1)):
	err("Premiers pas : le premier lancement doit attendre son jalon et disparaitre apres une reussite")
_satellite = re.search(r"decision_core_satellite\s*=\s*\{(.*?)(?=\n\w+\s*=\s*\{|\Z)", _core_decisions, re.S)
if (not _satellite or "has_country_flag = core_suborbital_fait" not in _satellite.group(1)
        or "NOT = { has_country_flag = core_satellite_fait }" not in _satellite.group(1)):
	err("Premiers pas : le premier satellite doit suivre le lancement suborbital et rester unique")
_crewed = re.search(r"decision_core_vol_habite\s*=\s*\{(.*?)(?=\n\w+\s*=\s*\{|\Z)", _core_decisions, re.S)
if (not _crewed or "has_country_flag = core_satellite_fait" not in _crewed.group(1)
        or "NOT = { has_country_flag = core_vol_habite_fait }" not in _crewed.group(1)):
	err("Premiers pas : le vol habite doit suivre le premier satellite et rester unique")
_deep_probe = re.search(r"decision_core_sonde_profonde\s*=\s*\{(.*?)(?=\n\w+\s*=\s*\{|\Z)",
					open(os.path.join(ROOT, "common", "decisions", "core_sonde_profonde.txt"), encoding="utf-8").read(), re.S)
if (not _deep_probe or "has_country_flag = core_vol_habite_fait" not in _deep_probe.group(1)
		or "core_premier_corps_fait" not in _deep_probe.group(1)
		or "influence = 300" not in _deep_probe.group(1)
		or "value:adastra_cout_relance_sonde" not in _deep_probe.group(1)
		or "minerals = 1000" not in _deep_probe.group(1)
		or "alloys = 100" not in _deep_probe.group(1)):
	err("Premiers pas : la sonde doit suivre l alunissage quand il est possible, et son cout croitre")
_lunar_decision = re.search(
    r"decision_core_premier_corps\s*=\s*\{(.*?)(?=\n\w+\s*=\s*\{|\Z)",
    _core_decisions, re.S)
if not _lunar_decision:
    err("Premiers pas : la mission du premier corps est absente")
elif "country_event = { id = adastra.106 }" not in _lunar_decision.group(1):
    err("Premiers pas : la mission du premier corps ne delegue pas le choix de cible")
elif ("capital_scope = {" not in _lunar_decision.group(1)
      or "any_system_planet = { is_moon = yes }" not in _lunar_decision.group(1)):
	err("Premiers pas : la mission du premier corps doit exiger une lune du systeme natal")
if _lunar_decision and re.search(r"any_owned_planet\s*=\s*\{\s*limit\s*=", _lunar_decision.group(1), re.S):
	err("Premiers pas : le filtre lunaire utilise un limit invalide dans any_owned_planet")
if (not _m110 or "random_system =" in _m110.group(1)
        or "random_system_planet =" not in _m110.group(1)
        or "is_surveyed = { who = root status = yes }" not in _m110.group(1)
        or "set_surveyed = { surveyed = yes surveyor = root }" not in _m110.group(1)
        or "has_country_flag = core_premier_corps_fait" not in _m110.group(1)):
	err("Premiers pas : la sonde doit reconnaitre un seul astre inconnu du systeme natal apres l alunissage")
print("  5 paliers de risque, cibles locales et reussite verifies")

# ------------------- plans de vaisseaux reconstructibles (1.2, Sithiya)
# Les programmes livrent un exemplaire ; sans le PLAN, un vaisseau perdu l'est
# pour toute la partie - l'auto-conception echoue sans hyperpropulsion. Chaque
# design sous-luminique doit donc etre donne a l'empire par create_ship_design.
print("\n== plans de vaisseaux ==")
dpath3 = os.path.join(ROOT, "common", "global_ship_designs",
                      "adastra_ship_designs.txt")
dsrc3 = open(dpath3, encoding="utf-8").read() if os.path.exists(dpath3) else ""
designs = set(re.findall(r'name = "(NAME_Adastra_\w+)"', dsrc3))
sous_luminiques = {d for d in designs if not d.endswith("_FTL")}
for d in sorted(sous_luminiques):
    if 'create_ship_design = { design = "%s" }' % d not in grants:
        err("le plan %s n'est jamais donne a l'empire : un vaisseau perdu"
            " le serait definitivement" % d)
    # tout design doit avoir un nom affichable
    for lang, src2 in (("FR", _fr), ("EN", _en)):
        if d not in src2:
            err("design %s : nom absent en %s" % (d, lang))
print("  %d designs sous-luminiques, tous donnes et nommes"
      % len(sous_luminiques))

# ------------------------ designations de capitale (1.2, retour Sithiya)
# Cinq designations de capitale du jeu de base exigent is_country_type = default.
# Sans elargissement, un empire confine n'a acces a AUCUNE designation - sa seule
# planete est sa capitale.
print("\n== designations de capitale ==")
COLONY_TYPES = ["col_capital", "col_capital_foundry", "col_capital_factory",
                "col_capital_trade", "col_capital_extraction"]
ctpath2 = os.path.join(ROOT, "common", "colony_types",
                       "zzz_adastra_colony_types.txt")
if not os.path.exists(ctpath2):
    err("surcharges de designations absentes (lancer gen_colony_type_overrides.py)")
else:
    csrc = strip_comments(open(ctpath2, encoding="utf-8").read())
    got = {k for k, _s, _e in top_level_blocks(csrc)}
    if not set(COLONY_TYPES) <= got:
        err("designations elargies manquantes : %s"
            % sorted(set(COLONY_TYPES) - got))
    # 31/08 : le fichier verrouille desormais TOUTES les designations vanilla
    # avant l'emergence ; les col_pre_ftl_* sont surchargees ailleurs et ne
    # doivent pas apparaitre ici (l'ordre de chargement ecraserait leur
    # elargissement).
    intruses = sorted(k for k in got if k.startswith("col_pre_ftl"))
    if intruses:
        err("designations pre-PRL presentes dans le fichier de verrou : %s"
            % intruses)
    n_verrou = 0
    for k, s2, e2 in top_level_blocks(csrc):
        blk = csrc[s2:e2]
        if "has_country_flag = adastra_locked" not in blk:
            err("designation %s : garde de verrou absente" % k)
        else:
            n_verrou += 1
        if k in COLONY_TYPES:
            # chaque mention du type default doit etre accompagnee du notre
            n_def = len(re.findall(r"is_country_type = default", blk))
            n_nous = len(re.findall(
                r"is_country_type = adastra_grounded", blk)) - 1  # la garde
            if n_def != n_nous:
                err("designation %s : %d fois « default » pour %d fois notre"
                    " type - une condition n'a pas ete elargie"
                    % (k, n_def, n_nous))
    print("  %d designations verrouillees avant emergence, dont %d elargies"
          % (n_verrou, len(COLONY_TYPES)))

# La Grande Archive a exactement la meme garde, et le meme symptome.
gapath = os.path.join(ROOT, "common", "megastructures",
                      "zzz_adastra_grand_archive.txt")
if not os.path.exists(gapath):
    err("surcharge de la Grande Archive absente")
else:
    gasrc = strip_comments(open(gapath, encoding="utf-8").read())
    if "grand_archive_0" not in gasrc:
        err("la surcharge ne declare pas grand_archive_0")
    if gasrc.count("is_country_type = default") != gasrc.count("is_country_type = adastra_grounded"):
        err("Grande Archive : une condition n'a pas ete elargie")
    print("  Grande Archive : constructible pendant le confinement")

# ------------------------- localisation des modificateurs du mod (1.2)
# Un modificateur sans localisation s'affiche par sa cle brute dans la liste des
# modificateurs de l'empire, et le jeu ecrit « Missing modifier localization »
# au chargement. Trois cles par modificateur : le nom, la description, et
# mod_<cle> pour l'infobulle.
print("\n== localisation des modificateurs ==")
MODS_A_LOCALISER = ["adastra_pre_electric", "adastra_pre_manufacture"]
_lfr = open(os.path.join(ROOT, "localisation", "french",
                         "adastra_l_french.yml"), encoding="utf-8").read()
_len = open(os.path.join(ROOT, "localisation", "english",
                         "adastra_l_english.yml"), encoding="utf-8").read()
for _m in MODS_A_LOCALISER:
    for _k in (_m, _m + "_desc", "mod_" + _m):
        for _lang, _src in (("FR", _lfr), ("EN", _len)):
            if not re.search(r'^ %s:0 "..' % re.escape(_k), _src, re.M):
                err("modificateur %s : cle %s absente ou vide en %s"
                    % (_m, _k, _lang))
print("  %d modificateurs, nom + description + infobulle, FR et EN"
      % len(MODS_A_LOCALISER))

# Les trois telescopes sont ecrits a la main, hors du generateur des
# batiments d'epoque. Leur absence de localisation rendait les cles brutes
# visibles dans le menu de construction et salissait error.log.
print("\n== localisation des telescopes ==")
TELESCOPES_A_LOCALISER = ["building_core_observatory",
                          "building_core_radio_telescope",
                          "building_core_space_telescope"]
for _building in TELESCOPES_A_LOCALISER:
    for _key in (_building, _building + "_desc"):
        for _lang, _src in (("FR", _lfr), ("EN", _len)):
            if not re.search(r'^ %s:0 "..' % re.escape(_key), _src, re.M):
                err("telescope %s : cle %s absente ou vide en %s"
                    % (_building, _key, _lang))
            if len(re.findall(r'^ %s:0 ' % re.escape(_key), _src, re.M)) != 1:
                err("telescope %s : cle %s dupliquee en %s"
                    % (_building, _key, _lang))
print("  3 niveaux d observatoire, nom + description, FR et EN")

# Le brouillard galactique doit etre une action volontaire. Une regression
# vers un pulse mensuel invisible rendrait a nouveau l'exploration confuse.
print("\n== observation astronomique ==")
_premiers_pas = open(os.path.join(ROOT, "common", "decisions",
                                  "core_premiers_pas.txt"), encoding="utf-8").read()
_on_actions = open(os.path.join(ROOT, "common", "on_actions",
                                "adastra_on_actions.txt"), encoding="utf-8").read()
_observation = re.search(
    r"decision_core_astronomical_observation\s*=\s*\{(.*?)(?=\ndecision_|\Z)",
    _premiers_pas, re.S)
if not _observation:
    err("observation astronomique : decision absente")
else:
    _bloc = _observation.group(1)
    for _building in TELESCOPES_A_LOCALISER:
        if _building not in _bloc:
            err("observation astronomique : telescope %s non pris en compte" % _building)
    for _needle in ("has_technology = tech_adastra_astronomy",
                    "country_event = { id = adastra.92 }"):
        if _needle not in _bloc:
            err("observation astronomique : verrou ou effet absent (%s)" % _needle)
    # 31/08 : cout releve (100 influence, 500 mineraux) et progressif
    # (+30 % par campagne via value:adastra_cout_campagne_astro).
    for _needle in ("enactment_time = 720", "influence = 100", "minerals = 500",
                    "mult = value:adastra_cout_campagne_astro"):
        if _needle not in _bloc:
            err("observation astronomique : duree ou cout absent (%s)" % _needle)
_astronomy_events = open(os.path.join(ROOT, "events", "adastra_events.txt"), encoding="utf-8").read()
_astronomy_result = re.search(r"country_event = \{\s*\n\tid = adastra\.93(.*?)(?=\n\}\n)",
                              _astronomy_events, re.S)
_astronomy_reveal = re.search(r"country_event = \{\s*\n\tid = adastra\.92(.*?)(?=\n\}\n)",
                              _astronomy_events, re.S)
if not _astronomy_reveal or "country_event = { id = adastra.93 }" not in _astronomy_reveal.group(1):
    err("observation astronomique : adastra.92 ne lance pas l'evenement de decouverte")
if not _astronomy_result:
    err("observation astronomique : evenement de decouverte adastra.93 absent")
else:
    _bloc = _astronomy_result.group(1)
    for _needle in ("picture = GFX_evt_adastra_situation",):
        if _needle not in _bloc:
            err("observation astronomique : evenement de decouverte incomplet (%s)" % _needle)
if _astronomy_reveal and "set_surveyed" in _astronomy_reveal.group(1):
    _reveal_body = _astronomy_reveal.group(1)
    # 1.4 (30/08) : l'astronomie DECOUVRE sans prospecter (set_visited +
    # clear_uncharted_space). Aucun astre ne doit etre releve par elle.
    if "set_visited" not in _reveal_body:
        err("observation astronomique : la decouverte doit passer par set_visited")
    if "set_surveyed" in _reveal_body:
        err("observation astronomique : l'astronomie ne doit prospecter aucun astre")
if _astronomy_reveal:
    _reveal_body = _astronomy_reveal.group(1)
    # La portee est geometrique : l'observation ne depend pas des hyperlignes
    # deja connues. Chaque niveau choisit exactement une cible par campagne.
    if _reveal_body.count("random_system = {") != 3:
        err("observation astronomique : un palier doit choisir une unique cible")
    if "max_jumps" in _reveal_body:
        err("observation astronomique : la portee ne doit pas suivre les hyperlignes")
    for _radius in ("max_distance <= 35", "max_distance <= 75", "max_distance <= 140"):
        if _radius not in _reveal_body:
            err("observation astronomique : portee euclidienne manquante (%s)" % _radius)
    if _reveal_body.count("type = euclidean") != 3:
        err("observation astronomique : les trois portees doivent etre euclidiennes")
for _lang, _src in (("FR", _lfr), ("EN", _len)):
    for _key in ("decision_core_astronomical_observation",
                 "decision_core_astronomical_observation_desc",
                 "decision_core_astronomical_observation_tooltip",
                 "adastra.93.name", "adastra.93.desc", "adastra.93.a",
                 "adastra.93.a.tooltip", "adastra.94.name", "adastra.94.desc",
                 "adastra.94.a", "adastra.94.a.tooltip", "adastra.95.name",
                 "adastra.95.desc", "adastra.95.a", "adastra.95.a.tooltip"):
        if not re.search(r'^ %s:0 "..' % re.escape(_key), _src, re.M):
            err("observation astronomique : localisation %s absente en %s" % (_key, _lang))
    if "event_target:adastra_astronomy_target.GetName" not in _src:
        err("observation astronomique : nom du systeme absent en %s" % _lang)
if re.search(r"on_monthly_pulse_country\s*=\s*\{.*?adastra\.92", _on_actions, re.S):
    err("observation astronomique : adastra.92 est encore declenche chaque mois")
else:
	print("  telescope, decision, localisations et absence de pulse verifies")

# Les jalons spatiaux sont des premiers historiques : le satellite est unique,
# l observation coute, et leurs bonus ne doivent pas devenir permanents.
print("\n== jalons spatiaux ==")
_satellite = re.search(r"decision_core_satellite\s*=\s*\{(.*?)(?=\ndecision_|\Z)",
                       _premiers_pas, re.S)
if not _satellite or "NOT = { has_country_flag = core_satellite_fait }" not in _satellite.group(1):
    err("jalons spatiaux : premier satellite repetable")
_premiers_events = open(os.path.join(ROOT, "events", "core_premiers_pas_events.txt"), encoding="utf-8").read()
for _event, _modifier in (("adastra.103", "core_mod_suborbital"),
                          ("adastra.102", "core_mod_satellites"),
                          ("adastra.104", "core_mod_vol_habite"),
                          ("adastra.108", "core_mod_premier_corps"),
                          ("adastra.107", "core_mod_station_permanente")):
    _match = re.search(r"country_event = \{\s*\n\tid = %s(.*?)(?=\n\}\n)" % re.escape(_event),
                       _premiers_events, re.S)
    if not _match or ("modifier = %s" % _modifier) not in _match.group(1) or "days = 3600" not in _match.group(1):
        err("jalons spatiaux : bonus temporaire absent pour %s" % _event)
    elif "add_monthly_resource_mult" in _match.group(1):
        err("jalons spatiaux : revenu mensuel permanent encore present pour %s" % _event)
_telescopes = open(os.path.join(ROOT, "common", "buildings", "core_telescopes.txt"), encoding="utf-8").read()
for _source, _target in (("building_core_observatory", "building_core_radio_telescope"),
                         ("building_core_radio_telescope", "building_core_space_telescope")):
    _match = re.search(r"%s\s*=\s*\{(.*?)(?=\n\n\n#|\Z)" % _source, _telescopes, re.S)
    if not _match or ("upgrades =" not in _match.group(1)) or _target not in _match.group(1):
        err("observatoire : chaine d amelioration absente (%s -> %s)" % (_source, _target))
# Une civilisation qui commence tard ne doit pas devoir eriger l'observatoire
# optique puis payer deux reconstructions. Chaque palier est constructible si
# sa technologie est deja connue ; les paliers inferieurs restent accessibles
# comme ameliorations pour les campagnes qui les ont construits plus tot.
for _upgrade, _tech in (("building_core_radio_telescope", "tech_adastra_radio_astronomy"),
                        ("building_core_space_telescope", "tech_adastra_remote_sensing")):
    _match = re.search(r"%s\s*=\s*\{(.*?)(?=\n\n\n#|\Z)" % _upgrade, _telescopes, re.S)
    if not _match or "can_build = yes" not in _match.group(1):
        err("observatoire : palier %s non constructible directement" % _upgrade)
    elif _tech not in _match.group(1):
        err("observatoire : palier %s sans prerequis %s" % (_upgrade, _tech))
print("  cout, unicite, bonus temporaires et chaine d observatoire verifies")

# Chaque etape du programme spatial vaut exactement vingt-cinq points : les
# technologies fondatrices et le geste du joueur doivent etre visibles dans la
# barre, sans saut opaque jusqu'au jalon suivant. Ces contrats protegent les
# valeurs de la 1.4 et empechent de retomber sur le comportement 225 -> 250.
print("\n== repartition de la progression spatiale ==")
_events_programme = open(os.path.join(ROOT, "events", "adastra_events.txt"), encoding="utf-8").read()
_decisions_programme = open(os.path.join(ROOT, "common", "decisions", "adastra_decisions.txt"), encoding="utf-8").read()
_m132 = re.search(r"country_event = \{\s*\n\tid = adastra\.132(.*?)(?=\ncountry_event = \{|\Z)", _events_programme, re.S)
if not _m132:
    err("progression spatiale : evenement adastra.132 absent")
else:
    _body132 = _m132.group(1)
    for _trigger, _points in (("adastra_lot_explore_tech", 5),
                              ("adastra_lot_constructor_tech", 4),
                              ("adastra_lot_outpost_tech", 10),
                              ("adastra_lot_orbital_tech", 5)):
        _section = re.search(r"if = \{\s*limit = \{.*?%s.*?\n\t\}" % re.escape(_trigger), _body132, re.S)
        if not _section or "add_situation_progress = %d" % _points not in _section.group(0):
            err("progression spatiale : %s ne vaut plus %d points" % (_trigger, _points))
for _event, _points in ((74, 15), (75, 10), (76, 15), (85, 15), (86, 5)):
    _body = re.search(r"country_event = \{\s*\n\tid = adastra\.%d(.*?)(?=\ncountry_event = \{|\Z)" % _event, _events_programme, re.S)
    if not _body or "add_situation_progress = %d" % _points not in _body.group(1):
        err("progression spatiale : adastra.%d ne rend plus %d points" % (_event, _points))
_catchup72 = re.search(r"country_event = \{\s*\n\tid = adastra\.72(.*?)(?=\ncountry_event = \{|\Z)", _events_programme, re.S)
if (not _catchup72 or "set_situation_progress = 300" not in _catchup72.group(1)
        or "adastra_lot_explore_complet = yes" not in _catchup72.group(1)
        or "adastra_phase1_done" not in _catchup72.group(1)
        or "is_surveyed" in _catchup72.group(1)):
    err("progression spatiale : adastra.72 doit recalibrer le programme sans exiger la prospection")
_hyper = re.search(r"decision_adastra_hyperdrive\s*=\s*\{(.*?)(?=\ndecision_|\Z)", _decisions_programme, re.S)
if not _hyper or "add_situation_progress = 10" not in _hyper.group(1):
    err("progression spatiale : le Programme hyperspatial ne rend plus 10 points")
print("  25 points par etape : fondations et gestes verifies")

# ---------------- compatibilite civiques / infrastructures de depart (1.4)
# Les ethiques et les traits ordinaires ne posent pas de batiment. Le moteur
# vanilla peut en revanche ajouter une structure de depart selon un civisme ou
# un contenu DLC apres on_game_start. La sortie generee doit couvrir toutes les
# structures datees, etre appelee aux deux passes et rendre une reforme gratuite
# a l'emergence.
print("\n== compatibilite de depart ==")
from vanilla_building_age_map import (  # noqa: E402
    CIVIC_BUILDING_UNLOCKS,
    STARTUP_BUILDING_AGE,
)
from vanilla_zone_age_map import ZONE_AGE, ZONE_BUILDING_SLOTS  # noqa: E402
_compat_path = os.path.join(ROOT, "common", "scripted_effects",
                            "zz_adastra_start_compatibility.txt")
if not os.path.exists(_compat_path):
    err("effet de compatibilite de depart absent")
else:
    _compat = open(_compat_path, encoding="utf-8").read()
    for _building, _age in STARTUP_BUILDING_AGE.items():
        if "remove_building = %s" % _building not in _compat:
            err("compatibilite : %s n'est pas neutralise au depart" % _building)
    if "building_communal_housing" in _compat:
        err("compatibilite : le logement communautaire ne doit pas etre retire")
    for _civic, _data in CIVIC_BUILDING_UNLOCKS.items():
        _building = _data["building"]
        if "owner = { has_civic = %s }" % _civic not in _compat:
            err("compatibilite : civisme %s absent de la restitution" % _civic)
        if "owner = { has_country_flag = adastra_reached_%s }" % _data["age"] not in _compat:
            err("compatibilite : age de restitution de %s absent" % _building)
        for _trigger in _data["triggers"]:
            if "owner = { %s = yes }" % _trigger not in _compat:
                err("compatibilite : entretien de %s absent (%s)" % (_building, _trigger))
        if "free_building_slots > 0" not in _compat:
            err("compatibilite : restitution sans emplacement libre")
        if "NOT = { has_building = %s }" % _building not in _compat:
            err("compatibilite : restitution de %s non protegee" % _building)
        if "add_building = %s" % _building not in _compat:
            err("compatibilite : %s n'est pas rendu quand son economie le permet" % _building)
    print("  %d infrastructures datees, logement communautaire preserve"
          % len(STARTUP_BUILDING_AGE))
if grants.count("adastra_cleanup_start_infrastructure = yes") < 2:
    err("compatibilite : nettoyage absent de l'initialisation ou du jour 4")
_i = grants.find("\n\tid = adastra.15\n")
_j = grants.find("\ncountry_event = {", _i)
_emergence = grants[_i:_j if _j > 0 else len(grants)]
if "set_country_flag = free_government_reform" not in _emergence:
    err("emergence : reforme gouvernementale gratuite absente")
if "country_event = { id = adastra.29 days = 1 }" not in _emergence:
    err("emergence : notification de reforme absente")
if _emergence.count("set_country_flag = free_government_reform") != 1:
    err("emergence : la reforme gratuite doit etre accordee une seule fois")
if "capital_scope = { adastra_grant_civic_infrastructure = yes }" not in _emergence:
    err("emergence : restitution des batiments civiques absente")
if grants.count("capital_scope = { adastra_grant_civic_infrastructure = yes }") < 3:
    err("compatibilite : restitution absente du depart, de la recherche ou de l'emergence")
_on_actions = open(os.path.join(ROOT, "common", "on_actions", "adastra_on_actions.txt"),
                   encoding="utf-8").read()
if "adastra.134" not in _on_actions:
    err("compatibilite : reprise mensuelle des infrastructures civiques absente")
_wait_event = re.search(r"\n\s*id = adastra\.134\b(.*?)(?=\ncountry_event = \{|\Z)", grants, re.S)
if not _wait_event or "capital_scope = { free_building_slots > 0 }" not in _wait_event.group(1):
    err("compatibilite : reprise civique sans garde d'emplacement libre")
for _lang in ("french", "english"):
    _loc = open(os.path.join(ROOT, "localisation", _lang,
                             "adastra_l_%s.yml" % ("french" if _lang == "french" else "english")),
                encoding="utf-8-sig").read()
    for _key in ("adastra.29.name", "adastra.29.desc", "adastra.29.a", "adastra.29.a.tooltip"):
        if not re.search(r'^ %s:0 "[^"]+' % re.escape(_key), _loc, re.M):
            err("reforme : localisation %s absente ou vide en %s" % (_key, _lang))
print("  civismes et traits ordinaires conserves ; reforme unique a l'emergence")

# ----------------------- capacite des zones et emplacements (1.4)
# Les emplacements sont produits par les zones depuis Stellaris 4.4. Chaque
# zone datee doit donc porter la capacite graduelle definie dans la table, y
# compris la zone urbaine de base. Une faction ne peut pas retirer ces slots.
print("\n== capacite de construction progressive ==")
_zones_path = os.path.join(ROOT, "common", "zones", "zzz_adastra_zone_ages.txt")
if not os.path.exists(_zones_path):
    err("capacite : surcharges de zones absentes")
else:
    _zones = open(_zones_path, encoding="utf-8").read()
    for _zone, _slots in ZONE_BUILDING_SLOTS.items():
        _match = re.search(r"^%s\s*=\s*\{(.*?)(?=^### |\Z)" % re.escape(_zone),
                           _zones, re.M | re.S)
        if not _match:
            err("capacite : zone %s absente" % _zone)
        elif "zone_building_slots_add = %d" % _slots not in _match.group(1):
            err("capacite : %s doit offrir %d emplacement(s)" % (_zone, _slots))
        elif ZONE_AGE[_zone][1] and "has_technology = %s" % ZONE_AGE[_zone][1] not in _match.group(1):
            err("capacite : %s doit etre verrouillee par %s" % (_zone, ZONE_AGE[_zone][1]))
print("  %d zones, de 1 a 2 emplacements selon le developpement" % len(ZONE_BUILDING_SLOTS))

# ----------------------- emplacements de zones urbaines (1.4)
# Les zones urbaines sont les vrais emplacements de construction depuis 4.4.
# Le jeu de base les laisse tous ouverts aux primitifs ; l'origine doit les
# reveler au rythme de la Premiere cite et du Code de lois.
print("\n== emplacements urbains progressifs ==")
from vanilla_zone_slot_age_map import CITY_ZONE_SLOT_TECH  # noqa: E402
_slots_path = os.path.join(ROOT, "common", "zone_slots", "zzz_adastra_zone_slot_ages.txt")
if not os.path.exists(_slots_path):
    err("emplacements urbains : surcharges absentes (lancer gen_zone_slot_age_overrides.py)")
else:
    _slots = open(_slots_path, encoding="utf-8").read()
    _slot_names = {k for k, _s, _e in top_level_blocks(_slots)}
    if _slot_names != set(CITY_ZONE_SLOT_TECH):
        err("emplacements urbains desynchronises : %s" % sorted(_slot_names ^ set(CITY_ZONE_SLOT_TECH)))
    for _slot, (_tech, _tooltip, _why) in CITY_ZONE_SLOT_TECH.items():
        _match = re.search(r"^%s\s*=\s*\{(.*?)(?=^### |\Z)" % re.escape(_slot),
                           _slots, re.M | re.S)
        if not _match:
            continue
        if "has_technology = %s" % _tech not in _match.group(1):
            err("emplacement urbain %s sans technologie %s" % (_slot, _tech))
        if "fail_text = %s" % _tooltip not in _match.group(1):
            err("emplacement urbain %s sans infobulle" % _slot)
        if _slot == "slot_city_02" and (
                "has_upgraded_capital" in _match.group(1) or
                re.search(r"fail_text\s*=\s*zone_city_02_prereq(?:\s|$)",
                          _match.group(1))):
            err("second emplacement urbain : verrou vanilla de centralisation encore present")
    for _lang in ("french", "english"):
        _loc_path = os.path.join(ROOT, "localisation", _lang,
                                 "adastra_l_%s.yml" % ("french" if _lang == "french" else "english"))
        _loc = open(_loc_path, encoding="utf-8-sig").read()
        for _tech, _tooltip, _why in CITY_ZONE_SLOT_TECH.values():
            if not re.search(r"^ %s:0 \"[^\"]+" % re.escape(_tooltip), _loc, re.M):
                err("emplacement urbain : infobulle %s absente en %s" % (_tooltip, _lang))
    print("  2 emplacements : Bronze puis Fer")

_capital_setup = grants[grants.index("capital_scope = {", grants.index("# 1.2 : la capitale demarre specialisee")):
                        grants.index("# Les departs tardifs recoivent deja les technologies")]
if "num_districts = { type = district_city value > 1 }" not in _capital_setup:
    err("depart : les districts urbains initiaux ne sont pas reduits a un noyau")
if "remove_building = building_capital" not in _capital_setup or "building = building_capital" not in _capital_setup:
    err("depart : la capitale n'est pas recomposee apres la reduction urbaine")

# --------------------------------- cycle de vie des modificateurs (1.2)
# Tout modificateur permanent pose par le mod doit avoir un chemin de retrait.
# Le piege est adastra.11 : son trigger exige adastra_locked, drapeau retire a
# l'emergence - un modificateur qui ne compte que sur lui reste a vie si le
# joueur emerge sans avoir cherche la techno correspondante.
print("\n== cycle de vie des modificateurs ==")
PERMANENTS_VOULUS = {"adastra_heritage_scientific", "adastra_heritage_industrial",
                     "adastra_heritage_civic", "adastra_heritage_pioneer",
					 "adastra_heritage_orbital",
                     "adastra_heritage_trial",
                     *{"adastra_heritage_depth_%s" % age for age in (
                         "stone", "bronze", "iron", "medieval", "renaissance",
                         "steam", "industrial", "machine", "atomic", "space")}}
poses = set()
for m in re.finditer(r"add_modifier = \{ modifier = (adastra_\w+)([^}]*)\}", grants):
    if "days = " in m.group(2) and "days = -1" not in m.group(2):
        continue          # temporaire, il expire tout seul
    poses.add(m.group(1))
retires = set(re.findall(r"remove_modifier = (adastra_\w+)", grants))
orphelins = sorted(poses - retires - PERMANENTS_VOULUS)
if orphelins:
    err("modificateur(s) permanent(s) sans retrait : %s" % ", ".join(orphelins))
# le retrait doit exister ailleurs que dans adastra.11
_i = grants.find("\n\tid = adastra.15\n")   # la DEFINITION, pas un appel
_j = grants.find("\ncountry_event = {", _i)
emergence = grants[_i:_j if _j > 0 else len(grants)]
for mod in ("adastra_pre_electric", "adastra_pre_manufacture"):
    if "remove_modifier = %s" % mod not in emergence:
        err("%s n'est pas retire a l'emergence : adastra.11 ne repasse plus une"
            " fois adastra_locked tombe" % mod)
if "adastra_trade_restored" not in emergence:
    err("la conversion du commerce n'est pas retablie a l'emergence")

# L'heritage ne doit etre accorde qu'une fois, apres l'emergence. Il remplace
# l'ancien empilement de bonus dependant de l'age de depart.
heritages = ("adastra_heritage_scientific", "adastra_heritage_industrial",
             "adastra_heritage_civic", "adastra_heritage_pioneer",
             "adastra_heritage_orbital")
_heritage_path = os.path.join(ROOT, "common", "static_modifiers", "adastra_modifiers.txt")
_heritage_modifiers = open(_heritage_path, encoding="utf-8").read()
if "country_event = { id = adastra.30 days = 2 }" not in emergence:
    err("emergence : choix de l'heritage absent")
for heritage in heritages:
    if "modifier = %s" % heritage not in grants:
        err("heritage absent de l'evenement : %s" % heritage)
    if "%s = {" % heritage not in _heritage_modifiers:
        err("heritage absent des modificateurs : %s" % heritage)
for age in ("stone", "bronze", "iron", "medieval", "renaissance", "steam",
            "industrial", "machine", "atomic", "space"):
    profondeur = "adastra_heritage_depth_%s" % age
    if "modifier = %s" % profondeur not in emergence:
        err("emergence : heritage de profondeur absent : %s" % age)
    if "%s = {" % profondeur not in _heritage_modifiers:
        err("heritage de profondeur absent des modificateurs : %s" % age)
if "adastra_heritage_1" in grants or "adastra_heritage_bold" in grants:
    err("emergence : ancien heritage cumulatif encore present")
print("  %d modificateur(s) permanent(s) pose(s), tous retires ou voulus a vie"
      % len(poses))

# ----------------------------------------------- districts (1.2)
# Le troisieme etage du systeme de 4.4 : un district cree ses emplois tout seul,
# sans batiment ni zone. Oublie jusqu'au 13/08, il donnait +11,50 energie par
# mois a l'Age de pierre.
print("\n== districts ==")
from vanilla_district_age_map import (DISTRICT_TECH,  # noqa: E402
                                      STARTING_DISTRICTS_TO_REMOVE, UPKEEP_SWAP)
dpath2 = os.path.join(ROOT, "common", "districts", "zzz_adastra_district_ages.txt")
if not os.path.exists(dpath2):
    err("surcharges de districts absentes (lancer gen_district_age_overrides.py)")
else:
    dsrc2 = open(dpath2, encoding="utf-8").read()
    got = {k for k, _s, _e in top_level_blocks(dsrc2)}
    want = ({k for k, v in DISTRICT_TECH.items() if v[0] not in ("na", "keep")}
            | set(UPKEEP_SWAP))
    if got != want:
        err("surcharges de districts desynchronisees : %s" % sorted(got ^ want))
    # L'entretien d'epoque doit rester conditionnel des deux cotes : si le bloc
    # miroir en minerais saute, l'empire ne paie plus rien ; si la garde saute,
    # il paie en energie une facture qu'il ne peut pas honorer.
    for k in UPKEEP_SWAP:
        blk = [dsrc2[a:b] for n2, a, b in top_level_blocks(dsrc2) if n2 == k]
        if not blk:
            continue
        if "adastra_pays_energy_upkeep = yes" not in blk[0]:
            err("district %s : entretien energetique sans garde" % k)
        if "NOT = { adastra_pays_energy_upkeep = yes }" not in blk[0]:
            err("district %s : pas d'entretien de remplacement en minerais" % k)
    if "adastra_pays_energy_upkeep = {" not in open(
            os.path.join(ROOT, "common", "scripted_triggers",
                         "zz_adastra_scripted_triggers.txt"), encoding="utf-8").read():
        err("declencheur adastra_pays_energy_upkeep absent")
    for k, (tech, _why) in DISTRICT_TECH.items():
        if tech in ("na", "keep"):
            continue
        if tech not in declared:
            err("district %s : la techno %s n'existe pas" % (k, tech))
        if "NOT = { has_origin = origin_adastra }" not in dsrc2:
            err("district %s : garde sans exclusion des autres empires" % k)
for k in STARTING_DISTRICTS_TO_REMOVE:
    if "remove_district = %s" % k not in grants:
        err("adastra.2 ne retire pas le district de depart %s" % k)
# Les ages deja traverses doivent offrir leurs technologies : sans ca un depart
# tardif repart d'un arbre vide, sans metallurgie ni electricite.
gpath = os.path.join(ROOT, "common", "scripted_effects", "zz_adastra_age_grants.txt")
if not os.path.exists(gpath):
    err("effets d'octroi des ages absents (lancer gen_age_techs.py)")
else:
    gsrc = open(gpath, encoding="utf-8").read()
    for age, _f, _c, _v in AGES:
        if "adastra_grant_age_%s = {" % age not in gsrc:
            err("octroi de l'age %s absent" % age)
        for t in TECHS[age]:
            if "tech = %s " % t["key"] not in gsrc:
                err("octroi de l'age %s : %s manquante" % (age, t["key"]))
    for age, _f, _c, _v in AGES[:-1]:
        if "adastra_grant_age_%s = yes" % age not in grants:
            err("adastra.2 n'offre pas l'age %s aux departs posterieurs" % age)
    if "adastra_grant_age_space = yes" in grants:
        err("l'Age spatial ne doit jamais etre offert : c'est le dernier age joue")
print("  %d district(s) verrouille(s), %d retire(s) au demarrage"
      % (len([1 for v in DISTRICT_TECH.values() if v[0] not in ("na", "keep")]),
         len(STARTING_DISTRICTS_TO_REMOVE)))

# --------------------------------- ressources verrouillees par techno (1.2)
# Une ressource ne doit pas exister avant la techno qui l'invente. Deux moities
# a garder en phase : la PRODUCTION de base (common/country_types) et la
# CONSOMMATION (modificateurs poses par adastra.11). Si l'une des deux saute,
# l'empire se retrouve soit avec une ressource gratuite, soit avec un deficit
# permanent qu'il ne peut pas combler.
print("\n== ressources verrouillees par techno ==")
# 1.2 : la garde n'est plus « has_technology » en dur mais le declencheur
# genere adastra_has_<ressource>, qui accepte aussi un age de depart posterieur.
# Un empire qui commence a l'age de la machine n'a pas recherche le Reseau
# electrique, il l'a par definition - sans ca il n'aurait jamais d'energie.
from age_techs_data import RESOURCE_TECH  # noqa: E402
RES_TECH = {res: "adastra_has_%s = yes" % res for res in RESOURCE_TECH}
gatesrc = open(os.path.join(ROOT, "common", "scripted_triggers",
                            "zz_adastra_age_gates.txt"), encoding="utf-8").read()
ctpath = os.path.join(ROOT, "common", "country_types", "adastra_country_types.txt")
ctsrc = open(ctpath, encoding="utf-8").read() if os.path.exists(ctpath) else ""
gi = ctsrc.find("adastra_grounded = {")
grounded = ctsrc[gi:] if gi >= 0 else ""
for res, tech in sorted(RES_TECH.items()):
    if RESOURCE_TECH[res][0] not in declared:
        err("ressource %s : la techno %s n'existe pas" % (res, RESOURCE_TECH[res][0]))
    if "adastra_has_%s = {" % res not in gatesrc:
        err("declencheur adastra_has_%s absent de zz_adastra_age_gates.txt" % res)
    for m in re.finditer(r"produces = \{(.*?)\n\t\t\}", grounded, re.S):
        body = m.group(1)
        if re.search(r"\b%s = " % res, body) and tech not in body:
            # le bloc de compensation des biens de conso est le seul autorise a
            # produire sans sa techno : il ne fait que rendre ce que le moteur
            # refuse d'annuler (plancher a -90 % sur les entretiens).
            if not (res == "consumer_goods" and "NOT = { %s }" % tech in body):
                err("%s produit sans %s dans adastra_grounded - la ressource"
                    " existerait des l'Age de pierre" % (res, tech))
for mod, tech in (("adastra_pre_electric", "adastra_has_energy"),
                  ("adastra_pre_manufacture", "adastra_has_consumer_goods")):
    if mod not in open(os.path.join(ROOT, "common", "static_modifiers",
                                    "adastra_modifiers.txt"), encoding="utf-8").read():
        err("modificateur %s absent" % mod)
    if mod not in grants or tech not in grants:
        err("adastra.11 ne gere pas %s / %s" % (mod, tech))
_mods_src = open(os.path.join(ROOT, "common", "static_modifiers",
                              "adastra_modifiers.txt"), encoding="utf-8").read()
_pre_manu = re.search(r"adastra_pre_manufacture = \{(.*?)^\}", _mods_src, re.S | re.M)
if not _pre_manu:
    err("adastra_pre_manufacture introuvable")
else:
    _pre_manu = _pre_manu.group(1)
    if "consumer_goods_upkeep_mult" in _pre_manu:
        err("adastra_pre_manufacture utilise un multiplicateur plafonne a -90 %")
    if "planet_politicians_consumer_goods_upkeep_add" in _pre_manu:
        err("adastra_pre_manufacture utilise un modificateur politicien invalide")
    for _key in ("planet_bureaucrats_consumer_goods_upkeep_add",
                 "planet_entertainers_consumer_goods_upkeep_add"):
        if _key not in _pre_manu:
            err("adastra_pre_manufacture n'annule pas %s" % _key)
_event_11 = re.search(r"\n\s*id = adastra\.11\n(.*?)(?=\ncountry_event = \{|\Z)",
                      grants, re.S)
if not _event_11 or not re.search(r"NOT = \{ adastra_has_consumer_goods = yes \}.*?"
                                  r"set_resource = \{ resource = consumer_goods value = 0 \}",
                                  _event_11.group(1), re.S):
    err("les biens de consommation peuvent encore s'accumuler avant la Manufacture")
if "add_building = { district = district_city zone = zone_default building = building_adastra_radio }" in grants:
    err("la radio est encore posee dans une zone incompatible au demarrage")
# La conversion commerciale doit etre coupee ET rendue. Si le retablissement
# saute, l'empire sort du confinement avec un commerce qui ne produit plus rien
# pour le restant de la partie, et rien ne le signale.
if "set_trade_conversions = { trade = 1 }" not in grants:
    err("la conversion du commerce n'est pas coupee pendant le confinement")
if "adastra_trade_restored" not in grants:
    err("la conversion du commerce n'est jamais retablie apres l'electricite")
for _flag in ("trade_conversion_consumer_goods", "trade_conversion_unity",
              "trade_conversion_trade_league", "trade_conversion_holy_covenant",
              "trade_conversion_mutual_aid"):
    if _flag not in grants:
        warn("retablissement du commerce : la politique %s n'est pas traitee,"
             " le joueur retomberait sur la conversion par defaut" % _flag)

if "adastra.11" not in open(os.path.join(ROOT, "common", "on_actions",
                                         "adastra_on_actions.txt"), encoding="utf-8").read():
    err("adastra.11 n'est branche sur aucune on_action : les modificateurs ne"
        " seraient jamais retires")
print("  alliages/bronze, biens de conso/vapeur, energie/electricite")

# ------------------------------- entretien d'epoque des batiments (1.2)
# Un modificateur d'entretien ne descend jamais sous -90 % : verifie en jeu le
# 13/08, « Un monde sans courant » affiche -100 % et le batiment coute quand
# meme un dixieme de sa base. Zero ne s'atteint qu'en ecrivant deux blocs
# upkeep mutuellement exclusifs dans la definition.
print("\n== entretien d'epoque des batiments ==")
_nb = 0
for m in re.finditer(r"^(building_adastra_\w+) = \{", bsrc, re.M):
    e2 = bsrc.find("\n}", m.end())
    blk = bsrc[m.end():e2]
    if "upkeep = {" not in blk:
        continue
    _nb += 1
    if "adastra_pays_energy_upkeep = yes" not in blk:
        err("batiment %s : entretien energetique sans garde" % m.group(1))
    if "NOT = { adastra_pays_energy_upkeep = yes }" not in blk:
        err("batiment %s : pas d'entretien de remplacement en minerais" % m.group(1))
print("  %d batiments avec entretien conditionnel" % _nb)

# ------------------------------------------- scripts d'emploi des batiments
# Les emplois viennent des inline_scripts du jeu de base. Un nom errone donne
# « Unknown inline_script » au chargement, et le batiment se construit sans
# creer le moindre emploi - invisible en jeu, c'est le bug le plus couteux
# qu'on ait eu. Liste relevee sur common/inline_scripts/jobs/ en 4.4.6.
print("\n== scripts d'emploi ==")
from age_buildings_data import JOBS  # noqa: E402
VALID_JOBS = {
    "unity_jobs_add", "farmers_add", "miners_add", "researchers_add",
    "enforcers_add", "technicians_add", "soldiers_add", "factory_add",
    "foundry_add", "entertainers_add", "clerks_add", "physicists_add",
    "biologists_add", "engineers_add", "trader_add", "priests_add",
    "politician_add", "healthcare_add", "refiner_add", "chemist_add",
    "roboticist_add", "telepaths_add", "wranglers_add",
}
for k, v in sorted(JOBS.items()):
    if v not in VALID_JOBS:
        err("batiment %s : inline_script d'emploi inconnu « jobs/%s » -"
            " le batiment ne creera aucun emploi" % (k, v))
for m in re.finditer(r"script = jobs/(\S+)", bsrc):
    if m.group(1) not in VALID_JOBS:
        err("adastra_age_buildings.txt : jobs/%s n'existe pas" % m.group(1))
print("  %d batiments, scripts d'emploi valides" % len(JOBS))

# ------------------------------------------------------------- decisions
# Le bloc resources d'une decision n'accepte que category et des blocs cost.
# Un « modifier » ecrit la produit « Unexpected token: modifier » au chargement
# et le prix reste bloque a sa valeur de base, sans que rien ne le signale en
# jeu. Pour un cout conditionnel, la forme valide est plusieurs blocs cost
# mutuellement exclusifs, chacun avec son trigger.
print("\n== decisions ==")
dpath = os.path.join(ROOT, "common", "decisions", "adastra_decisions.txt")
if not os.path.exists(dpath):
    err("fichier de decisions absent")
else:
    dsrc = strip_comments(open(dpath, encoding="utf-8").read())
    bad = 0
    for m in re.finditer(r"\n\tresources = \{", dsrc):
        depth, j = 1, m.end()
        while j < len(dsrc) and depth:
            if dsrc[j] == "{":
                depth += 1
            elif dsrc[j] == "}":
                depth -= 1
            j += 1
        body = dsrc[m.end():j]
        # on ne regarde que le premier niveau du bloc resources
        lvl, k, top = 0, 0, []
        while k < len(body):
            if body[k] == "{":
                lvl += 1
            elif body[k] == "}":
                lvl -= 1
            elif lvl == 0:
                top.append(body[k])
            k += 1
        if re.search(r"\bmodifier\s*=", "".join(top)):
            bad += 1
    if bad:
        err("%d bloc(s) resources contiennent un « modifier » : le moteur refuse"
            " ce token et le cout reste fige" % bad)
    else:
        print("  aucun modifier illegal dans un bloc resources")

# Le programme national remplace les quatre campagnes lineaires de la 1.3.
# Les anciennes decisions restent dans les sources uniquement pour les saves
# existantes : elles doivent etre invisibles, tandis que le nouveau choix doit
# toujours offrir ses trois orientations pour chacun des dix ages.
print("\n== programme national ==")
if not os.path.exists(dpath):
    err("programme national : fichier de decisions absent")
else:
    _decisions = open(dpath, encoding="utf-8").read()
    _events_path = os.path.join(ROOT, "events", "adastra_events.txt")
    _events = open(_events_path, encoding="utf-8").read() if os.path.exists(_events_path) else ""
    _modifiers_path = os.path.join(ROOT, "common", "static_modifiers", "adastra_modifiers.txt")
    _modifiers = open(_modifiers_path, encoding="utf-8").read() if os.path.exists(_modifiers_path) else ""
    _locations = {
        "french": open(os.path.join(ROOT, "localisation", "french", "adastra_l_french.yml"), encoding="utf-8").read(),
        "english": open(os.path.join(ROOT, "localisation", "english", "adastra_l_english.yml"), encoding="utf-8").read(),
    }
    _ages_programme = ("stone", "bronze", "iron", "medieval", "renaissance",
                       "steam", "industrial", "machine", "atomic", "space")
    _choix_programme = {
        "stone": ("stores", "craft", "clans"),
        "bronze": ("granaries", "foundries", "trade"),
        "iron": ("cadastre", "civic_works", "markets"),
        "medieval": ("guilds", "estates", "royal_works"),
        "renaissance": ("trade", "workshops", "patronage"),
        "steam": ("rail", "mechanisation", "reform"),
        "industrial": ("mass_production", "public_education", "extraction"),
        "machine": ("electrification", "consumption", "public_health"),
        "atomic": ("reconstruction", "civil_science", "strategic_industry"),
        "space": ("logistics", "research", "social_investment"),
    }
    if "decision_adastra_national_programme = {" not in _decisions:
        err("programme national : decision principale absente")
    if "id = adastra.140" not in _events:
        err("programme national : evenement adastra.140 absent")
    for _old in ("harvest", "mining", "fuel", "industry"):
        _old_block = re.search(r"decision_adastra_campaign_%s\s*=\s*\{(.*?)(?=\ndecision_|\Z)" % _old,
                               _decisions, re.S)
        if not _old_block or "always = no" not in _old_block.group(1):
            err("programme national : ancienne campagne %s encore visible" % _old)
    _attendus = []
    for _age in _ages_programme:
        for _choix in _choix_programme[_age]:
            _cle = "%s_%s" % (_age, _choix)
            _mod = "adastra_programme_%s" % _cle
            _loc = "adastra.140.%s" % _cle
            _attendus.append(_mod)
            if _loc not in _events or _mod not in _events:
                err("programme national : choix incomplet %s" % _cle)
            if not re.search(r"%s\s*=\s*\{.*?\}" % re.escape(_mod), _modifiers, re.S):
                err("programme national : modificateur absent %s" % _mod)
            for _lang, _texte in _locations.items():
                if not re.search(r"^\s+%s(?:_desc)?\s*:" % re.escape(_loc), _texte, re.M):
                    err("programme national : localisation %s absente en %s" % (_loc, _lang))
                if not re.search(r"^\s+%s(?:_desc)?\s*:" % re.escape(_mod), _texte, re.M):
                    err("programme national : localisation %s absente en %s" % (_mod, _lang))
            if not re.search(r"(?m)^\s*add_modifier\s*=\s*\{\s*modifier\s*=\s*%s\s+days\s*=\s*1800\s*\}" % re.escape(_mod), _events):
                err("programme national : effet visible absent pour %s" % _cle)
    if re.search(r"hidden_effect\s*=\s*\{\s*add_modifier\s*=\s*\{\s*modifier\s*=\s*adastra_programme_", _events):
        err("programme national : un effet de choix est encore masque")
    _programme = re.search(r"decision_adastra_national_programme\s*=\s*\{(.*?)(?=\ndecision_|\Z)", _decisions, re.S)
    if not _programme or not re.search(r"allow\s*=\s*\{\s*owner\s*=\s*\{\s*#.*?NOT\s*=\s*\{\s*OR\s*=\s*\{", _programme.group(1), re.S):
        err("programme national : le verrou doit verifier les modificateurs du pays")
    elif not all("unity = %d" % _cost in _programme.group(1) for _cost in (25, 60, 140, 280)):
        err("programme national : couts d unite attendus 25 / 60 / 140 / 280")
    _icons = os.path.join(ROOT, "gfx", "interface", "icons", "decisions")
    if not os.path.exists(os.path.join(_icons, "decision_adastra_national_programme.dds")):
        err("programme national : icone DDS absente")
    if len(_attendus) == 30:
        print("  30 orientations d'age, localisations et icone presentes")

# ------------------------------ ce que les technos annoncent debloquer (1.2)
# Le moteur affiche le bloc modifier d'une techno, jamais le reste. Une techno
# qui debloque un batiment, une ressource ou un palier de capitale doit le dire
# dans sa description, sinon le joueur cherche a l'aveugle.
print("\n== annonces de deblocage ==")
from age_techs_data import GAMEPLAY_ANNOUNCEMENTS, UNLOCKS  # noqa: E402
from vanilla_zone_age_map import specialization_unlocks  # noqa: E402
from vanilla_zone_slot_age_map import city_zone_slot_unlocks  # noqa: E402
locfr = open(os.path.join(ROOT, "localisation", "french",
                          "adastra_ages_l_french.yml"), encoding="utf-8").read()
locen = open(os.path.join(ROOT, "localisation", "english",
                          "adastra_ages_l_english.yml"), encoding="utf-8").read()
annonces = {}
for source in (UNLOCKS, GAMEPLAY_ANNOUNCEMENTS, specialization_unlocks(),
               city_zone_slot_unlocks()):
    for key, textes in source.items():
        if key in annonces:
            annonces[key] = tuple(
                "%s %s" % (annonces[key][i], textes[i]) for i in range(2))
        else:
            annonces[key] = textes
attendus = set(annonces)
for age, _f, _c, _v in AGES:
    for t in TECHS[age]:
        if t["unlocks"]:
            attendus.add(t["key"])
for key in sorted(attendus):
    for lang, src2 in (("french", locfr), ("english", locen)):
        m = re.search(r'^ %s_desc:0 "(.*)"$' % re.escape(key), src2, re.M)
        if not m:
            err("%s : description absente en %s" % (key, lang))
        elif "§Y" not in m.group(1):
            err("%s : la description %s n'annonce pas ce que la techno debloque"
                % (key, lang))
for key in annonces:
    if key not in {t["key"] for age, _f, _c, _v in AGES for t in TECHS[age]}:
        err("UNLOCKS decrit %s, qui n'existe pas" % key)
for key, textes in annonces.items():
    for lang, src2, texte in (("french", locfr, textes[0]),
                              ("english", locen, textes[1])):
        m = re.search(r'^ %s_desc:0 "(.*)"$' % re.escape(key), src2, re.M)
        if not m or texte not in m.group(1):
            err("%s : le deblocage n'est pas annonce en %s" % (key, lang))

# Les verrous de gameplay ecrits a la main ne passent pas par le champ
# `unlocks` de la table des ages. Toute nouvelle technologie directement
# requise par ces batiments, decisions ou evenements doit donc etre ajoutee a
# GAMEPLAY_ANNOUNCEMENTS et apparaitre dans les deux langues.
manual_paths = (
    os.path.join(ROOT, "common", "buildings", "core_telescopes.txt"),
    os.path.join(ROOT, "common", "decisions", "core_premiers_pas.txt"),
    os.path.join(ROOT, "events", "core_premiers_pas_events.txt"),
    os.path.join(ROOT, "events", "adastra_events.txt"),
)
manual_techs = set()
for path in manual_paths:
    with open(path, encoding="utf-8") as f:
        manual_techs.update(re.findall(r"tech_adastra_[a-z0-9_]+", f.read()))
missing_manual = manual_techs - set(GAMEPLAY_ANNOUNCEMENTS)
if missing_manual:
    err("deblocages core non annonces : %s" % ", ".join(sorted(missing_manual)))
else:
    print("  %d verrous core annonces explicitement" % len(manual_techs))
print("  %d technos annoncent un deblocage, FR et EN" % len(attendus))

# ------------------------------------------------------- icones des technos
# Une techno Stellaris n'a pas de champ icon : le moteur cherche
# gfx/interface/icons/technologies/<cle>.dds. Une icone manquante ne produit
# aucune erreur dans le journal, la techno s'affiche juste avec un carre vide.
print("\n== icones des technos d'age ==")
from age_techs_data import TECHS  # noqa: E402
icon_dir = os.path.join(ROOT, "gfx", "interface", "icons", "technologies")
attendus = {
    "%s.dds" % tech["key"]
    for technologies in TECHS.values()
    for tech in technologies
}
if not os.path.isdir(icon_dir):
    err("dossier d'icones absent : %s" % icon_dir)
else:
    presents = {f for f in os.listdir(icon_dir) if f.endswith(".dds")}
    manquantes = sorted(attendus - presents)
    orphelines = sorted(presents - attendus)
    if manquantes:
        err("%d icone(s) de techno manquante(s) : %s"
            % (len(manquantes), ", ".join(manquantes[:8])))
    if orphelines:
        warn("%d icone(s) orpheline(s) (techno supprimee ?) : %s"
             % (len(orphelines), ", ".join(orphelines[:8])))
    if not manquantes and not orphelines:
        print("   %d icones originales, aucune manquante" % len(attendus))

tech_source = open(os.path.join(ROOT, "common", "technology", "adastra_age_techs.txt"),
                   encoding="utf-8").read()
for technology in (tech for technologies in TECHS.values() for tech in technologies):
    expected_icon = "\ticon = %s" % technology["key"]
    if expected_icon not in tech_source:
        err("%s ne pointe pas vers son icone personnalisee" % technology["key"])

# Une carte qui n'apporte ni modificateur ni deblocage est une fausse
# decision de recherche. Un ancien arrondi du generateur ecrivait
# `modifier = {}` pour les bonus historiques inferieurs a 1 %. Le controle
# porte sur la sortie generee : il empeche que ce defaut revienne, meme si la
# table ou le generateur changent.
print("\n== effets concrets des technologies d'age ==")
_vides = []
for _k, _s, _e in top_level_blocks(tech_source):
    if not _k.startswith("tech_adastra_"):
        continue
    _bloc = tech_source[_s:_e]
    if re.search(r"\n\tmodifier = \{\s*\n\t\}", _bloc):
        _vides.append(_k)
if _vides:
    err("technologies d'age sans effet concret : %s" % ", ".join(_vides[:8]))
else:
    print("   250 technologies : modificateur ou deblocage concret")
        
# ------------------------------------------------- chaine des capitales
# Le siege du pouvoir doit aller d'un bout a l'autre sans trou : chaque palier
# pointe vers le suivant, et le dernier rend la main a building_capital. Un
# maillon casse, et la capitale reste bloquee a son age pour toute la partie.
print("\n== chaine des capitales ==")
capsrc = open(cap, encoding="utf-8").read() if os.path.exists(cap) else ""
declared_caps = {k for k, _s, _e in top_level_blocks(capsrc)}
want_caps = {c["key"] for c in CAPITAL_CHAIN}
if declared_caps != want_caps:
    err("chaine des capitales desynchronisee : %s"
        % sorted(declared_caps ^ want_caps))
# 1.4 (29/08) : chaine LINEAIRE, un seul successeur par palier. Le moteur
# rejette les chemins multiples (« upgrades loop », building_type.cpp:2175)
# et casse alors toute la chaine d'amelioration.
for i, c in enumerate(CAPITAL_CHAIN):
    upgrades = ([CAPITAL_CHAIN[i + 1]["key"]] if i + 1 < len(CAPITAL_CHAIN)
                else ["building_capital"])
    span = [(s2, e2) for k, s2, e2 in top_level_blocks(capsrc) if k == c["key"]]
    if not span:
        continue
    blk = capsrc[span[0][0]:span[0][1]]
    for nxt in upgrades:
        if not re.search(r"upgrades = \{[^}]*\b%s\b" % re.escape(nxt), blk, re.S):
            err("capitale %s : ne s'ameliore pas vers %s" % (c["key"], nxt))
    if c["tech"] and c["tech"] not in declared:
        err("capitale %s : prerequis %s inexistant" % (c["key"], c["tech"]))
    if "can_build = no" not in blk:
        err("capitale %s : can_build absent - elle serait constructible" % c["key"])
print("  %d paliers, du %s a building_capital"
      % (len(CAPITAL_CHAIN), CAPITAL_CHAIN[0]["fr"]))

# ------------------------------------------- ages des batiments vanilla
print("\n== ages des batiments vanilla ==")
from vanilla_building_age_map import BUILDING_AGE  # noqa: E402
bpath = os.path.join(ROOT, "common", "buildings", "zzz_adastra_building_ages.txt")
if not os.path.exists(bpath):
    err("surcharges d'age des batiments absentes (lancer gen_building_age_overrides.py)")
else:
    bsrc2 = open(bpath, encoding="utf-8").read()
    got = {k for k, _s, _e in top_level_blocks(bsrc2)}
    want = {k for k, v in BUILDING_AGE.items() if v[0] not in ("na", "keep", "tech")}
    if got != want:
        err("surcharges de batiments desynchronisees : %s" % sorted(got ^ want))
    valid = {a for a, _f, _c, _v in AGES} | {"na", "keep", "tech"}
    for k, (age, why) in BUILDING_AGE.items():
        if age not in valid:
            err("batiment %s : age inconnu '%s'" % (k, age))
        if not why.strip():
            warn("batiment %s : pas de justification ecrite" % k)
    for k in want:
        blk = bsrc2[[s2 for kk, s2, _e in top_level_blocks(bsrc2) if kk == k][0]:]
        if "NOT = { has_origin = origin_adastra }" not in blk[:1200]:
            err("batiment %s : garde sans exclusion des autres empires" % k)
    from collections import Counter as _C
    for a, n in sorted(_C(v[0] for v in BUILDING_AGE.values()).items()):
        print("  %-12s %2d" % (a, n))

# --------------------------------- coherence techno <-> batiment (1.2)
# Un batiment marque "tech" n'a plus de surcharge : c'est sa techno prerequise
# qui le tient. Si cette techno s'ouvre APRES l'age voulu, le batiment arrive en
# retard sans que rien ne le signale ; si elle s'ouvre avant, il arrive en
# avance. Ce controle est la seule chose qui relie les deux tables.
print("\n== coherence techno <-> batiment ==")
from vanilla_building_age_map import BUILDING_TECH  # noqa: E402
from vanilla_tech_age_map import TECH_AGE  # noqa: E402
from vanilla_age_map import VANILLA_AGE_MAP  # noqa: E402
ORDER = [a for a, _f, _c, _v in AGES] + ["ftl"]
tsrc = ""
for _n in ("zzz_adastra_tech_overrides.txt", "zzz_adastra_tier1_overrides.txt"):
    _p = os.path.join(ROOT, "common", "technology", _n)
    if os.path.exists(_p):
        tsrc += open(_p, encoding="utf-8").read() + "\n"
# 16/08 : une techno de palier 2 ne porte plus adastra_vanilla_open_space mais
# has_country_flag = adastra_completed - le palier 2 attend l'emergence, ce qui
# ferme le palier 3 et avec lui la terraformation. C'est une garde PLUS forte
# que n'importe quel age : on la note "ftl", le dernier cran de ORDER.
gate_age = {}
for _k, _s, _e in top_level_blocks(tsrc):
    _bloc = tsrc[_s:_e]
    _g = re.search(r"adastra_vanilla_open_(\w+) = yes", _bloc)
    if _g:
        gate_age[_k] = _g.group(1)
    elif "has_country_flag = adastra_completed" in _bloc:
        gate_age[_k] = "ftl"
for _k, (_a, _grant) in VANILLA_AGE_MAP.items():
    gate_age.setdefault(_k, _a)

marked = {k for k, v in BUILDING_AGE.items() if v[0] == "tech"}
if marked != set(BUILDING_TECH):
    err("BUILDING_TECH desynchronisee de BUILDING_AGE : %s"
        % sorted(marked ^ set(BUILDING_TECH)))
for b, (t, want_age) in sorted(BUILDING_TECH.items()):
    if want_age not in ORDER:
        err("%s : age voulu inconnu '%s'" % (b, want_age))
        continue
    got = gate_age.get(t)
    if got is None:
        err("%s : sa techno %s n'a aucune garde d'age - le batiment n'est plus"
            " tenu par rien" % (b, t))
    elif ORDER.index(got) < ORDER.index(want_age):
        err("%s voulu a l'age %s mais sa techno %s s'ouvre des %s"
            % (b, want_age, t, got))
    elif ORDER.index(got) > ORDER.index(want_age):
        warn("%s voulu a l'age %s mais sa techno %s n'arrive qu'a %s"
             % (b, want_age, t, got))
for t, (a, why) in sorted(TECH_AGE.items()):
    if a not in ORDER:
        err("techno %s : age inconnu '%s'" % (t, a))
    if not why.strip():
        warn("techno %s : pas de justification ecrite" % t)
print("  %d batiments dates par leur techno, %d technos redatees"
      % (len(BUILDING_TECH), len(TECH_AGE)))

# ------------------------------------------------------------- modificateurs
mods = sorted({m for age, _f, _c, _v in AGES for t in TECHS[age] for m in t["mods"]}
              | {m for b in BUILDINGS for m in b["mods"]})
print("\n== modificateurs a valider contre le vanilla (PC en ligne) ==")
for m in mods:
    print("   " + m)

# --- le palier 2 du jeu de base attend l'emergence -------------------------
#
# 16/08 : les paliers 1 et 2 partageaient la garde adastra_vanilla_open_space.
# Six technos de palier 1 ouvraient le palier 2, six de palier 2 ouvraient le
# palier 3 - ou se trouve la terraformation, et que personne ne surcharge. Un
# joueur l'a trouve avant nous. Cette passe empeche la regression : une techno
# de palier 2 qui reprendrait une garde d'age rouvrirait la cascade.
print("\n== paliers du jeu de base ==")
_t1 = os.path.join(ROOT, "common", "technology", "zzz_adastra_tier1_overrides.txt")
if os.path.exists(_t1):
    _src = open(_t1, encoding="utf-8").read()
    _fautifs, _t1_sans_garde, _n1, _n2 = [], [], 0, 0
    for _k, _s, _e in top_level_blocks(_src):
        _b = _src[_s:_e]
        _tm = re.search(r"\btier\s*=\s*(\d+)", _b)
        if not _tm:
            continue
        if _tm.group(1) == "1":
            _n1 += 1
            # Une techno de palier 1 doit attendre soit son age historique,
            # soit la sortie du confinement. L'age est un trigger, la sortie
            # un drapeau de pays : les deux formes sont des gardes valides.
            if not re.search(r"(?:adastra_vanilla_open_\w+ = yes|has_country_flag = adastra_\w+)", _b):
                _t1_sans_garde.append(_k)
        elif _tm.group(1) == "2":
            _n2 += 1
            if "has_country_flag = adastra_completed" not in _b:
                _fautifs.append(_k)
    # Quatre technos de palier 2 sont volontairement redatees a un age
    # anterieur (tools/vanilla_tech_age_map.py) : purification du minerai,
    # forage profond, cultures modifiees, centrales ameliorees. Elles restent
    # accessibles pendant le confinement, et c'est voulu.
    #
    # Le palier 3 exige SIX technos de palier 2 deja cherchees. Tant qu'il en
    # existe moins de six d'accessibles, il ne peut pas s'ouvrir. C'est cette
    # marge qu'on surveille, pas la liste : redater une cinquieme techno reste
    # sans danger, une sixieme rouvrirait la terraformation.
    if len(_fautifs) >= 6:
        err("%d technos de palier 2 accessibles au sol - a six, le palier 3 "
            "s'ouvre et la terraformation avec : %s"
            % (len(_fautifs), ", ".join(sorted(_fautifs))))
    elif _fautifs:
        print("   %d technos de palier 2 volontairement redatees (marge : %d "
              "avant reouverture du palier 3) : %s"
              % (len(_fautifs), 6 - len(_fautifs), ", ".join(sorted(_fautifs))))
    if _t1_sans_garde:
        err("technos de palier 1 sans garde d'age : %s"
            % ", ".join(sorted(_t1_sans_garde)[:8]))
    print("   palier 1 : %d technos a l'Age spatial | palier 2 : %d a l'emergence"
          % (_n1, _n2))
else:
    warn("zzz_adastra_tier1_overrides.txt introuvable")

# --- le programme spatial ne doit pas s'enchainer sur lui-meme -------------
#
# Aucune decision de programme ne doit exiger adastra_phase*_done : un programme
# qui echoue - ciel occupe, systeme revendique - ne doit jamais en condamner un
# autre. La dependance se fait sur l'ETAPE, pas sur la reussite.
print("\n== enchainement des programmes ==")
_d = os.path.join(ROOT, "common", "decisions", "adastra_decisions.txt")
if os.path.exists(_d):
    _src = open(_d, encoding="utf-8").read()
    _mauvais = []
    for _k, _s, _e in top_level_blocks(_src):
        if not _k.startswith("decision_adastra_"):
            continue
        _pot = re.search(r"\tpotential = \{.*?\n\t\}", _src[_s:_e], re.S)
        if not _pot:
            continue
        # « NOT = { has_country_flag = adastra_phaseN_done } » est legitime :
        # c'est ce qui rend un programme jouable une seule fois. Ce qu'on
        # traque, c'est l'exigence POSITIVE - un programme qui refuse de
        # s'ouvrir tant qu'un autre n'a pas abouti.
        for _l in _pot.group(0).split("\n"):
            if "adastra_phase" in _l and "_done" in _l and "NOT" not in _l:
                _mauvais.append(_k)
                break
    if _mauvais:
        err("decision(s) conditionnee(s) a la reussite d'un autre programme : %s"
            % ", ".join(_mauvais))
    else:
        print("   aucune decision ne depend de la reussite d'une autre")


# ============================================================ icones des technos
# Ajoute le 16/08 apres avoir constate que kit/content/ n'embarquait pas gfx/ :
# les 101 .dds des technologies d'epoque n'etaient pas publies, et rien ne le
# signalait. Une copie a la main omet un dossier ; ce controle ne peut pas.
print("\n== icones des technologies d'epoque ==")
_dos = os.path.join(ROOT, "gfx", "interface", "icons", "technologies")
if not os.path.isdir(_dos):
    err("dossier absent : gfx/interface/icons/technologies")
else:
    _presentes = {f[:-4] for f in os.listdir(_dos) if f.endswith(".dds")}
    # le moteur cherche gfx/interface/icons/technologies/<cle>.dds :
    # c'est la CLE de la techno qui nomme le fichier, pas l'icone source.
    _attendues = {t["key"] for age, _f, _c, _v in AGES for t in TECHS[age]}
    _manque = sorted(_attendues - _presentes)
    if _manque:
        for _m in _manque[:10]:
            err("icone absente : %s.dds" % _m)
        if len(_manque) > 10:
            err("... et %d autres" % (len(_manque) - 10))
    else:
        print("   %d icones presentes pour %d technologies"
              % (len(_presentes), len(_attendues)))


# ================================================ ordre des octrois de technos
# Ajoute le 16/08 apres lecture de l'error.log de la partie 1.2 : seize lignes
# « Attempting to give invalid technology ». Le paquet de l'Age spatial etait
# refuse EN ENTIER dans la version publiee, pour deux raisons cumulees - les
# drapeaux qui ouvrent le `potential` etaient poses apres les octrois, et
# l'ordre des octrois ignorait les prerequis. Rien en jeu ne le signalait.
#
# Prerequis releves contre les fichiers du jeu de base le 16/08.
print("\n== ordre des octrois de technologies ==")
_PREREQ = {
    "tech_colonization_1": ["tech_space_exploration"],
    "tech_reactor_boosters_1": ["tech_fission_power"],
    "tech_solar_panel_network": ["tech_starbase_2"],
    "tech_space_defense_station_1": ["tech_starbase_1"],
    "tech_starbase_1": ["tech_space_construction"],
    "tech_starbase_2": ["tech_starbase_1"],
}
_ev = strip_comments(open(os.path.join(ROOT, "events", "adastra_events.txt"),
                         encoding="utf-8").read())
_n_blocs = 0
for _m in re.finditer(r"country_event = \{\s*\n\s*id = (adastra\.\d+)(.*?)\n\}\n",
                      _ev, re.S):
    _eid, _corps = _m.group(1), _m.group(2)
    _grants = re.findall(r"give_technology = \{ tech = (\w+)", _corps)
    if not _grants:
        continue
    _n_blocs += 1
    _pos = {}
    for _i, _t in enumerate(_grants):
        _pos.setdefault(_t, _i)
    for _t, _i in _pos.items():
        for _p in _PREREQ.get(_t, []):
            if _p not in _pos:
                err("%s : %s est octroyee mais son prerequis %s ne l'est jamais"
                    % (_eid, _t, _p))
            elif _pos[_p] > _i:
                err("%s : %s octroyee avant son prerequis %s"
                    % (_eid, _t, _p))
    _premier = _corps.find("give_technology")
    for _f in re.finditer(r"set_country_flag = (adastra_unlock_\w+|adastra_vanilla_gift_\w+)",
                          _corps):
        if _f.start() > _premier:
            err("%s : drapeau %s pose APRES le premier octroi - les technos "
                "seront refusees en silence" % (_eid, _f.group(1)))
if _n_blocs:
    print("   %d bloc(s) d'octroi verifie(s), ordre des prerequis et des drapeaux"
          % _n_blocs)


# ================================================= bornes historiques et vagues
# 1.3 : chaque technologie porte son annee, et la vague est deduite de la date.
# Ce controle est ce qui empeche l'Informatique de retomber a l'Age spatial.
print("\n== bornes historiques ==")
_dates = 0
for _age, _f, _c, _v in AGES:
    _lo, _hi = BORNES[_age]
    _datees = [t for t in TECHS[_age] if t.get("year") is not None]
    if not _datees:
        continue
    _dates += len(_datees)
    for _t in _datees:
        if not (_lo <= _t["year"] <= _hi):
            err("%s (%s) : annee %d hors des bornes de l'age %s (%d a %d)"
                % (_t["key"], _t["fr"], _t["year"], _age, _lo, _hi))
    if len(_datees) == len(TECHS[_age]) == TECHS_PAR_AGE:
        _v = vagues(TECHS[_age])
        from collections import Counter as _C
        _rep = _C(_v.values())
        if set(_rep.values()) != {5}:
            err("age %s : rangs desequilibres %s" % (_age, dict(_rep)))
        else:
            print("   %-12s 25 technos datees, 5 rangs de 5, ordre historique" % _age)
print("   %d technologie(s) datee(s) sur %d" % (_dates, sum(len(TECHS[a]) for a, _b, _c2, _d in AGES)))


# ============================================ l'arbre de l'age (1.5, 19/08)
# La progression, c'est la recherche : plus de vagues ni de verrou genere.
# L'ordre historique dans un age est tenu par les prerequis : chaque tech de
# rang N >= 2 doit exiger une tech de rang N-1 du MEME age, et chaque tech de
# rang 1 le pilier de l'age precedent (ou rien, a la Pierre). Une tech
# d'epoque acquise vaut un point : le declencheur genere de chaque age doit
# citer ses 25 technologies, et l'effet de progression doit couvrir les dix.
print("\n== arbre des ages ==")
_src_t = open(os.path.join(ROOT, "common", "technology", "adastra_age_techs.txt"),
              encoding="utf-8").read()
_blocs = dict(re.findall(r"^(tech_adastra_\w+) = \{(.*?)^\}", _src_t, re.S | re.M))
_age_de = {t["key"]: a for a, _b, _c2, _d in AGES for t in TECHS[a]}
_erreurs_arbre = 0
for _a, _b, _c2, _d in AGES:
    _rangs = vagues(TECHS[_a])
    for _t in TECHS[_a]:
        _bloc = _blocs.get(_t["key"], "")
        _pre = re.search(r'prerequisites = \{([^}]*)\}', _bloc)
        _pres = re.findall(r'"([^"]+)"', _pre.group(1)) if _pre else []
        if "adastra_vague_" in _bloc:
            err("%s : drapeau de vague dans le potential (1.5 : interdit)" % _t["key"]); _erreurs_arbre += 1
        if _rangs[_t["key"]] >= 2:
            if not (_pres and _age_de.get(_pres[0]) == _a and vagues(TECHS[_a])[_pres[0]] == _rangs[_t["key"]] - 1):
                err("%s (rang %d) : prerequis attendu de rang %d du meme age, trouve %s"
                    % (_t["key"], _rangs[_t["key"]], _rangs[_t["key"]] - 1, _pres)); _erreurs_arbre += 1
        elif _pres and _age_de.get(_pres[0]) == _a:
            err("%s (rang 1) : prerequis dans le meme age" % _t["key"]); _erreurs_arbre += 1
if not _erreurs_arbre:
    print("   250 technologies en arbre : rang 1 sur le pilier precedent, rangs 2-5 chaines dans l'age")
_prog_t = open(os.path.join(ROOT, "common", "scripted_triggers", "zz_adastra_progression.txt"),
               encoding="utf-8").read()
_prog_e = open(os.path.join(ROOT, "common", "scripted_effects", "zz_adastra_progression.txt"),
               encoding="utf-8").read()
for _a, _flag, _c2, _d in AGES:
    _m = re.search(r"adastra_tech_epoque_%s = \{(.*?)^\}" % _a, _prog_t, re.S | re.M)
    if not _m or _m.group(1).count("last_increased_tech = ") != len(TECHS[_a]):
        err("progression : le declencheur de %s ne cite pas ses %d technologies" % (_a, len(TECHS[_a])))
    if "adastra_tech_epoque_%s = yes" % _a not in _prog_e:
        err("progression : l'effet ignore l'age %s" % _a)
if _prog_e.count("add_situation_progress = 1") < len(AGES):
    err("progression : moins d'un point par age dans l'effet")
_situ = open(os.path.join(ROOT, "common", "situations", "zzz_adastra_situations.txt"),
             encoding="utf-8").read()
_ends = [int(x) for x in re.findall(r"^\t\t\tend = (\d+)", _situ, re.M)]
if _ends != [25 * i for i in range(1, 17)]:
	err("situation : fins d'etape attendues 25..400 par pas de 25, trouve %s" % _ends)
if re.search(r"monthly_progress = \{\s*base = 0\s*\}", _situ) is None:
    err("situation : la barre ne doit plus monter au mois (monthly_progress base = 0, sans modificateur)")
_events_recherche = open(os.path.join(ROOT, "events", "adastra_events.txt"), encoding="utf-8").read()
_loc_recherche = "\n".join(open(os.path.join(ROOT, "localisation", _lang, "adastra_l_%s.yml" % _lang), encoding="utf-8").read()
                           for _lang in ("french", "english"))
for _obsolete in ("adastra.12", "adastra_verrou_vu_"):
    if _obsolete in _events_recherche or _obsolete in _loc_recherche:
        err("progression : ancien avertissement de verrou encore present (%s)" % _obsolete)
print("   16 etapes de 25 points, barre sans progression mensuelle, recherche spatiale puis lancement")


# ================================================== icones sans chiffre romain
# 1.3, signale par ampynjord : dans le jeu de base, le I / II / III est peint
# DANS l'image - c'est le meme objet a un palier superieur. Emprunte par une de
# nos technologies, ce chiffre ne renvoie a rien et le joueur cherche un palier
# qui n'existe pas. 118 de nos 250 cartes etaient dans ce cas.
print("\n== icones sans palier romain ==")
_num = [t["key"] for _a, _b, _c3, _d in AGES for t in TECHS[_a]
        if re.search(r"_\d+$", t["icon"])] if False else []
_num = []
for _age, _f, _c4, _v in AGES:
    for _t in TECHS[_age]:
        if re.search(r"_\d+$", _t["icon"]):
            _num.append(_t["key"])
if _num:
    err("%d techno(s) portent une icone numerotee (le chiffre s'affiche sur la carte) : %s"
        % (len(_num), ", ".join(_num[:6])))
else:
    print("   aucune des %d icones ne porte de palier romain"
          % sum(len(TECHS[a]) for a, _b2, _c5, _d2 in AGES))


# =============================================== le jeu avant la technologie
# 1.3 : une fondatrice ne doit etre cherchable que si ce qu'elle sert est
# jouable. Sans ca le joueur depense son budget de recherche dans une carte qui
# ne changera rien avant des dizaines d'annees.
print("\n== fondatrices conditionnees au jeu ==")
_ov = open(os.path.join(ROOT, "common", "technology", "zzz_adastra_tech_overrides.txt"),
           encoding="utf-8").read()
# Les technologies de depart vanilla coutent parfois zero parce que le jeu
# normal les offre immediatement. Ad Astra les remet dans le tirage : zero
# rendrait alors la carte terminee des son ouverture.
_zero_start = []
for _name, _block in re.findall(r"^(tech_\\w+) = \\{(.*?)^\\}", _ov, re.S | re.M):
    if "start_tech = yes" in _block and re.search(r"^\\s*cost\\s*=\\s*0\\s*$", _block, re.M):
        _zero_start.append(_name)
if _zero_start:
    err("technologies de depart remises au tirage avec cout zero : %s"
        % ", ".join(_zero_start))
else:
    print("   aucune technologie de depart remise au tirage ne coute zero")
_fond = ["tech_space_exploration", "tech_thrusters_1", "tech_space_construction",
         "tech_corvettes", "tech_mass_drivers_1", "tech_ship_armor_1", "tech_shields_1",
         "tech_reactor_boosters_1", "tech_starbase_1", "tech_starbase_2",
         "tech_space_defense_station_1", "tech_solar_panel_network",
         "tech_colonization_1", "tech_interplanetary_commerce", "tech_hydroponics",
         "tech_holo_entertainment"]
_sans = []
for _t in _fond:
    _m = re.search(r"^%s = \{(.*?)\n\}" % re.escape(_t), _ov, re.S | re.M)
    if not _m or "adastra_gameplay_" not in _m.group(1):
        _sans.append(_t)
if _sans:
    err("fondatrice(s) sans condition de jeu : %s" % ", ".join(_sans))
else:
    print("   les %d fondatrices portent leur condition de jeu" % len(_fond))


# ============================================ modificateurs qui n'existent pas
# Deux fois dans ce projet un modificateur invente a ete pose et ignore en
# silence par le moteur : mod_leaders_upkeep_mult (le prefixe de localisation
# pris pour le nom) et decision_cost_mult (qui n'existe tout simplement pas).
# Aucun des deux n'a produit la moindre ligne dans error.log.
print("\n== modificateurs inventes ==")
MODIFICATEURS_INVENTES = ["decision_cost_mult", "mod_leaders_upkeep_mult",
                          "planet_structures_upkeep_mult",
                          "planet_buildings_build_speed_mult", "trade_value_mult"]
_fautes = []
for _rep, _d, _fs in os.walk(os.path.join(ROOT, "common")):
    for _f in _fs:
        if not _f.endswith(".txt"):
            continue
        _src = open(os.path.join(_rep, _f), encoding="utf-8", errors="replace").read()
        _src = strip_comments(_src)
        for _m in MODIFICATEURS_INVENTES:
            if re.search(r"\b%s\s*=" % re.escape(_m), _src):
                _fautes.append("%s dans %s" % (_m, _f))
if _fautes:
    for _x in _fautes:
        err("modificateur inexistant : %s" % _x)
else:
    print("   aucun des %d modificateurs connus comme inexistants" % len(MODIFICATEURS_INVENTES))


# ======================================== nos vaisseaux dans un ciel revendique
# 1.3 : quand un empire revendique le systeme natal, le moteur traite nos
# vaisseaux en intrus et les teleporte hors du systeme. Un empire confine n'a
# nulle part ou aller : ils disparaissent. `needs_border_access = no` est le
# seul moyen de garder ses propres vaisseaux au-dessus de sa propre planete.
print("\n== vaisseaux en ciel revendique ==")
_ct = open(os.path.join(ROOT, "common", "country_types", "adastra_country_types.txt"),
           encoding="utf-8").read()
_m = re.search(r"^adastra_grounded = \{(.*?)\n\}", _ct, re.S | re.M)
if not _m or "needs_border_access = no" not in _m.group(1):
    err("adastra_grounded : needs_border_access = no manquant - les vaisseaux "
        "seront expulses du systeme natal des qu'un empire le revendique")
else:
    print("   adastra_grounded : needs_border_access = no")


# =============================================== premier contact pre-PRL
# Le confinement garde le reseau diplomatique isole, mais ne doit jamais
# supprimer une rencontre : les sites, indices et evenements vanilla doivent
# fonctionner jusqu'a l'emergence.
print("\n== premier contact pre-PRL ==")
if not _m or "share_communications = no" not in _m.group(1):
    err("adastra_grounded : le partage automatique des communications doit rester bloque")
if not _m or "standard_diplomacy_module = { contact_rule = does_first_contact_sites }" not in _m.group(1):
    err("adastra_grounded : les sites de premier contact vanilla doivent etre actives")
_events = open(os.path.join(ROOT, "events", "adastra_events.txt"), encoding="utf-8").read()
_on_actions = open(os.path.join(ROOT, "common", "on_actions", "adastra_on_actions.txt"),
                   encoding="utf-8").read()
if "remove_communications" in _events:
    err("premier contact : aucun script Ad Astra ne doit supprimer les communications vanilla")
if "adastra_foreign_observer" in _events:
    err("premier contact : le systeme natal ne doit pas etre reconnu par les empires etrangers au demarrage")
if re.search(r"\badastra\.135\b", _events) or re.search(r"\badastra\.135\b", _on_actions):
    err("premier contact : le filet adastra.135 obsolete ne doit plus etre appele")
else:
    print("   premiers contacts vanilla actifs sans partage automatique du reseau")

_veille_path = os.path.join(ROOT, "common", "first_contact", "zz_adastra_stages.txt")
_veille = open(_veille_path, encoding="utf-8").read()
if not re.search(r"adastra_stage_veille\s*=\s*\{.*?on_roll_failed\s*=\s*\{.*?standard_first_contact_on_roll_failed\s*=\s*\{\s*RANDOM_EVENTS\s*=\s*no_events", _veille, re.S):
    err("premier contact : adastra_stage_veille doit definir on_roll_failed sans evenement aleatoire")
else:
    print("   veille de premier contact : echec de tirage gere sans revelation")


# ============================================== jamais de vide de recherche
# Retour de test du 16/08 : « veille a ce qu'il y ait toujours des techs a
# rechercher tant qu'on n'a pas atteint la fin de la phase, sinon c'est
# frustrant ». On compte ce qui s'ouvre a chaque phase du programme spatial.
print("\n== de quoi chercher a chaque phase ==")
_PHASES = {
    "Age spatial (avant les programmes)": 25,   # les 25 technologies d'epoque
    "phase Exploration": 0, "phase Base stellaire": 0,
    # la derniere phase n'a qu'un objet : l'Hyperpropulsion elle-meme.
    "phase Hyperpropulsion": 1,
}
_G = {"adastra_gameplay_orbite": "phase Exploration",
      "adastra_gameplay_sol": "phase Exploration",
      "adastra_gameplay_chantier": "phase Base stellaire",
      "adastra_gameplay_vaisseaux": "phase Base stellaire",
      "adastra_gameplay_colonie": "phase Base stellaire",
      "adastra_gameplay_base": "phase Base stellaire"}
_ov = open(os.path.join(ROOT, "common", "technology", "zzz_adastra_tech_overrides.txt"),
           encoding="utf-8").read()
for _g, _ph in _G.items():
    _PHASES[_ph] += len(re.findall(r"%s = yes" % re.escape(_g), _ov))
_vides = [k for k, v in _PHASES.items() if v < 2 and "Hyperpropulsion" not in k]
for _k, _v in _PHASES.items():
    print("   %-38s %2d technologie(s)" % (_k, _v))
if _vides:
    warn("phase(s) sans de quoi chercher : %s" % ", ".join(_vides))


# ================================ ce qui peut apparaitre avant l'emergence
# Regle posee le 16/08 : une technologie du jeu de base qu'on CHERCHE dans une
# partie classique n'a rien a faire dans le tirage d'un empire confine. Seules
# passent les technologies de DEPART - celles qu'un empire normal possede des
# la premiere seconde - et douze exceptions qui debloquent une ressource ou un
# batiment dont un age a besoin.
print("\n== technologies vanilla avant l'emergence ==")
EXCEPTIONS_ECONOMIE = {
    "tech_mining_1", "tech_mining_2", "tech_mineral_purification_1",
    "tech_mineral_purification_2", "tech_alloys_1", "tech_luxuries_1",
    "tech_power_plant_2", "tech_power_hub_1", "tech_power_hub_2",
    "tech_eco_simulation", "tech_food_processing_1", "tech_gene_crops",
    "tech_genome_mapping",
}
_src = ""
for _n in ("zzz_adastra_tier1_overrides.txt", "zzz_adastra_tech_overrides.txt"):
    _src += open(os.path.join(ROOT, "common", "technology", _n), encoding="utf-8").read()
_fuites = []
for _k, _b in re.findall(r"^(tech_\w+) = \{(.*?)\n\}", _src, re.S | re.M):
    if "start_tech = yes" in _b or _k in EXCEPTIONS_ECONOMIE:
        continue
    if re.search(r"adastra_vanilla_open_\w+ = yes", _b):
        _fuites.append(_k)
if _fuites:
    err("%d techno(s) vanilla non-depart proposees avant l'emergence : %s"
        % (len(_fuites), ", ".join(_fuites[:8])))
else:
    print("   aucune fuite ; %d exceptions d'economie assumees" % len(EXCEPTIONS_ECONOMIE))


# ==================================================== l'identifiant Workshop
# 16/08 : une substitution par regex sur workshop_item.vdf a mange la ligne
# `publishedfileid`. SteamCMD n'a pas mis a jour le mod, il en a publie un
# SECOND, qu'il a fallu supprimer a la main. Le vdf ne se modifie plus que par
# tools/ci_release.py, qui le reconstruit depuis le registre - et ce controle
# verifie que l'identifiant y est.
print("\n== identifiant Workshop ==")
# 1.4 : la collection a trois mods, donc trois identifiants. Ils vivent dans
# workshop/mods.json, seul endroit ou ils soient ecrits. On verifie ici celui
# d'Origins, parce que 954 abonnes en dependent et qu'en changer signifierait
# les abandonner sur un mod mort.
import json  # noqa: E402
_reg = os.path.join(os.path.dirname(ROOT), "workshop", "mods.json")
if not os.path.exists(_reg):
    _reg = os.path.join(os.path.dirname(ROOT), "kit", "workshop_item.vdf")
    if os.path.exists(_reg):
        _t = open(_reg, encoding="utf-8").read()
        if "3781408257" not in _t:
            err("manifeste Workshop : identifiant d'Origins absent ou faux")
        else:
            print("   publishedfileid = 3781408257")
    else:
        print("   (aucun registre a verifier)")
else:
    _m = json.load(open(_reg, encoding="utf-8"))["mods"]
    _o = next((x for x in _m if x["cle"] == "origins"), None)
    if _o is None:
        err("workshop/mods.json : pas d'entree « origins »")
    elif _o["publishedfileid"] != "3781408257":
        err("workshop/mods.json : Origins porte %r au lieu de 3781408257 - "
            "publier ainsi creerait un doublon et abandonnerait les abonnes"
            % _o["publishedfileid"])
    else:
        for _x in _m:
            print("   %-9s %s" % (_x["cle"], _x["publishedfileid"] or "(jamais publie)"))

# ============================================ technologies citees par core_
# 17/08 : l'echelle de propulsion citait deux technologies qui n'existaient
# pas (tech_adastra_nuclear_rocket, tech_adastra_fusion_drive). Sur une cle
# inconnue, `has_technology` remplit l'error.log et renvoie faux pour
# toujours - le programme spatial se serait bloque en silence. Meme classe de
# bug que les seize `give_technology` refuses de la 1.2.
print("\n== technologies citees par les fichiers core_ ==")
_vanilla_ok = {"tech_hyper_drive_1", "tech_colonization_1", "tech_fission_power"}
_connues = set()
for _f in ("adastra_age_techs.txt",):
    _p = os.path.join(ROOT, "common", "technology", _f)
    if os.path.exists(_p):
        _connues |= set(re.findall(r"^(tech_\w+)\s*=\s*\{", open(_p, encoding="utf-8").read(), re.M))
_cites, _manquantes = 0, []
for _d in ("scripted_triggers", "scripted_effects", "decisions"):
    _dir = os.path.join(ROOT, "common", _d)
    if not os.path.isdir(_dir):
        continue
    for _n in sorted(os.listdir(_dir)):
        if not _n.startswith("core_"):
            continue
        _t = open(os.path.join(_dir, _n), encoding="utf-8")
        for _l in _t:
            if _l.lstrip().startswith("#"):
                continue
            for _k in re.findall(r"has_technology\s*=\s*(tech_\w+)", _l):
                _cites += 1
                if _k not in _connues and _k not in _vanilla_ok:
                    _manquantes.append("%s -> %s" % (_n, _k))
_evdir = os.path.join(ROOT, "events")
if os.path.isdir(_evdir):
    for _n in sorted(os.listdir(_evdir)):
        if not _n.startswith("core_"):
            continue
        for _l in open(os.path.join(_evdir, _n), encoding="utf-8"):
            if _l.lstrip().startswith("#"):
                continue
            for _k in re.findall(r"has_technology\s*=\s*(tech_\w+)", _l):
                _cites += 1
                if _k not in _connues and _k not in _vanilla_ok:
                    _manquantes.append("%s -> %s" % (_n, _k))
if _manquantes:
    for _m in _manquantes:
        err("technologie inconnue citee par un fichier core_ : %s" % _m)
else:
    print("   %d reference(s), toutes resolues" % _cites)

# ------------------------------------------------------------- rapport
print("\n" + "=" * 58)
for w in warnings:
    print("AVERTISSEMENT : " + w)
for e in errors:
    print("ERREUR : " + e)
print("%d erreur(s), %d avertissement(s)" % (len(errors), len(warnings)))
sys.exit(1 if errors else 0)
