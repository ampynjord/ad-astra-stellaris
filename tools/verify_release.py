#!/usr/bin/env python3
"""Controle ce que verify_1_2.py ne regarde pas : la coherence entre le depot
et ce qu'on s'apprete a publier - pour les trois mods de la collection.

verify_1_2.py verifie le contenu d'Origins. Celui-ci verifie la SORTIE.

  python tools/verify_release.py            # sans tag : coherence interne
  python tools/verify_release.py v1.4.0     # avec tag : regles de publication

La difference entre les deux n'est pas cosmetique. Sur la branche de travail,
une version peut porter le suffixe -dev et le changelog peut annoncer une
section en cours : c'est normal, on developpe. Avec un tag, ces deux choses
deviennent des erreurs : on ne publie pas du travail en cours.

Ecrit apres deux incidents reels :
  - un .vdf regenere sans publishedfileid a cree un DOUBLON d'Origins sur le
    Workshop, avec ses propres abonnes ;
  - le CHANGELOG publie avec la 1.3 annoncait encore une 1.2.1 en cours.
"""
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
REGISTRE = RACINE / "workshop" / "mods.json"

LIMITE_DESCRIPTION = 8000     # caracteres, cote Steam
LIMITE_APERCU = 1024 * 1024   # 1 Mio, cote Steam

erreurs, avertissements = [], []


def err(m):
    erreurs.append(m)


def warn(m):
    avertissements.append(m)


def lire(chemin):
    p = RACINE / chemin
    if not p.exists():
        err("fichier absent : %s" % chemin)
        return None
    return p.read_text(encoding="utf-8-sig")


tag = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None
attendu = (tag[1:] if tag.startswith("v") else tag) if tag else None

mods = json.loads(REGISTRE.read_text(encoding="utf-8"))["mods"]
principal = next(m for m in mods if m["cle"] == "origins")


# ------------------------------------------------------------------ versions
def version_de(chemin, quoi):
    txt = lire(chemin)
    if txt is None:
        return None
    m = re.search(r'^version\s*=\s*"([^"]+)"', txt, re.M)
    if not m:
        err("%s : pas de ligne version=" % quoi)
        return None
    return m.group(1)


versions = {}
for mod in mods:
    d = version_de("%s/descriptor.mod" % mod["source"], "%s descriptor" % mod["cle"])
    l = version_de(mod["lanceur"], mod["lanceur"])
    if d and l and d != l:
        err("%s : descriptor.mod dit %s, %s dit %s"
            % (mod["cle"], d, mod["lanceur"], l))
    versions[mod["cle"]] = d
    if tag and d and "-dev" in d:
        err("%s : version %s - on ne publie pas un -dev" % (mod["cle"], d))

# Origins porte le numero de la collection. Le tag doit lui correspondre.
if attendu and versions.get("origins") and versions["origins"] != attendu:
    err("le tag annonce %s, Origins dit %s" % (attendu, versions["origins"]))


# ---------------------------------------------------------------- changelog
changelog = lire("CHANGELOG.md") or ""
m = re.search(r"^##\s+(\d+\.\d+\.\d+)", changelog, re.M)
tete = m.group(1) if m else None
if not tete:
    err("CHANGELOG.md : la premiere section n'annonce pas de version x.y.z")

premiere = next((l for l in changelog.splitlines() if l.startswith("## ")), "")
en_cours = bool(re.search(r"en cours|in progress|WIP|TODO", premiere, re.I))

if tag:
    if en_cours:
        err("CHANGELOG.md : section de tete marquee « en cours » (%s)"
            % premiere.strip())
    if tete and versions.get("origins") and tete != versions["origins"]:
        err("CHANGELOG.md commence par %s, Origins dit %s"
            % (tete, versions["origins"]))
elif en_cours:
    print("  (changelog en cours - normal sur la branche de travail)")


# --------------------------------------------------------------- par mod
for mod in mods:
    cle = mod["cle"]
    source = RACINE / mod["source"]
    if not source.is_dir():
        err("%s : dossier source %s absent" % (cle, mod["source"]))
        continue

    for langue, champ in (("EN", "description"), ("FR", "description_fr")):
        txt = lire(mod[champ])
        if txt is None:
            continue
        if len(txt) > LIMITE_DESCRIPTION:
            err("%s description_%s : %d caracteres, Steam en accepte %d"
                % (cle, langue, len(txt), LIMITE_DESCRIPTION))
        ouvrants = len(re.findall(r"\[(?!/)[a-z0-9]+[^\]]*\]", txt))
        fermants = len(re.findall(r"\[/[a-z0-9]+\]", txt))
        if abs(ouvrants - fermants) > 2:
            warn("%s description_%s : %d balises ouvertes pour %d fermees"
                 % (cle, langue, ouvrants, fermants))

    apercu = RACINE / mod["apercu"]
    if not apercu.exists():
        err("%s : apercu absent (%s)" % (cle, mod["apercu"]))
    elif apercu.stat().st_size > LIMITE_APERCU:
        err("%s : apercu de %.1f Mio, Steam plafonne a 1 Mio"
            % (cle, apercu.stat().st_size / 1048576))

    # Un mod jamais publie n'a pas d'identifiant : c'est normal AVANT sa
    # premiere publication, et bloquant si on tague sans l'avoir faite.
    if not mod["publishedfileid"]:
        if tag:
            warn("%s : jamais publie, il sera ignore par la sortie "
                 "(tools/premiere_publication.py %s)" % (cle, cle))
        else:
            print("  (%s : pas encore publie)" % cle)

# Une dependance declaree doit correspondre a un mod du registre : une faute
# de frappe dans un descripteur ne se voit qu'en jeu, et tard.
noms = {m["nom"] for m in mods}
for mod in mods:
    txt = lire("%s/descriptor.mod" % mod["source"]) or ""
    for dep in re.findall(r'dependencies\s*=\s*\{([^}]*)\}', txt, re.S):
        for nom in re.findall(r'"([^"]+)"', dep):
            if nom not in noms:
                err("%s : dependance « %s » inconnue du registre" % (mod["cle"], nom))


# ------------------------------------------------------- manifeste et gabarit
gabarit = lire("workshop/item.vdf.template") or ""
for champ in ("@PUBLISHEDFILEID@", "@TITLE@", "@CONTENTFOLDER@",
              "@PREVIEWFILE@", "@DESCRIPTION@", "@CHANGENOTE@"):
    if champ not in gabarit:
        err("workshop/item.vdf.template : marqueur %s absent" % champ)

# Origins ne doit JAMAIS changer d'identifiant : 954 abonnes en dependent.
if principal["publishedfileid"] != "3781408257":
    err("Origins porte l'identifiant %s au lieu de 3781408257. Publier ainsi "
        "creerait un doublon et abandonnerait les abonnes."
        % principal["publishedfileid"])


# ----------------------------------------------------- parite des traductions
def cles(chemin):
    p = RACINE / chemin
    if not p.exists():
        return None
    return set(re.findall(r"^\s*([a-zA-Z0-9_.]+):\d*\s+\"",
                          p.read_text(encoding="utf-8-sig"), re.M))


for mod in mods:
    dossier = Path(mod["source"]) / "localisation"
    for en in sorted((RACINE / dossier / "english").glob("*.yml")):
        fr = RACINE / dossier / "french" / en.name.replace("english", "french")
        if not fr.exists():
            err("%s : %s sans equivalent francais" % (mod["cle"], en.name))
            continue
        ken = cles(en.relative_to(RACINE))
        kfr = cles(fr.relative_to(RACINE))
        if ken - kfr:
            err("%s : %d cle(s) sans traduction francaise (%s...)"
                % (en.name, len(ken - kfr), ", ".join(sorted(ken - kfr)[:3])))
        if kfr - ken:
            err("%s : %d cle(s) sans traduction anglaise (%s...)"
                % (fr.name, len(kfr - ken), ", ".join(sorted(kfr - ken)[:3])))

# Des noms francais restes dans les textes anglais : trouves pour de vrai dans
# la 1.3 publiee, onze fois (« Unlocks the building: Citadelle »).
anglais = lire("ad_astra/localisation/english/adastra_ages_l_english.yml") or ""
for mot in ("Citadelle", "Fonderie", "Grenier", "Tribunal", "Moulin",
            "Université", "Universite", "Manufacture", "École", "Ecole"):
    if re.search(r"Unlocks the building: %s" % mot, anglais):
        err("texte anglais : nom de batiment francais « %s »" % mot)


# --------------------------------------------------------------------- sortie
print("=" * 58)
for mod in mods:
    print("%-9s %-12s %s" % (mod["cle"],
                             versions.get(mod["cle"]) or "?",
                             mod["publishedfileid"] or "(jamais publie)"))
print("changelog : %s%s" % (tete or "?", "  (en cours)" if en_cours else ""))
print("tag       : %s" % (tag or "(aucun)"))
print("=" * 58)
for a in avertissements:
    print("  avertissement : %s" % a)
for e in erreurs:
    print("  ERREUR : %s" % e)
print("%d erreur(s), %d avertissement(s)" % (len(erreurs), len(avertissements)))
sys.exit(1 if erreurs else 0)
