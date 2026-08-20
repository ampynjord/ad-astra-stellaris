#!/usr/bin/env python3
"""Prepare tout ce que SteamCMD doit trouver, pour chaque mod de la collection.

  python tools/ci_release.py --sortie build              tous les mods publiables
  python tools/ci_release.py --sortie build --mod core   un seul

Produit, par mod :
  build/<cle>/content/            le mod, avec remote_file_id dans le descripteur
  build/<cle>/thumbnail.png       l'apercu
  build/<cle>/item.vdf            le manifeste, chemins absolus
  build/<nom>_v<version>.zip      l'archive attachee a la release GitHub

Un mod dont publishedfileid vaut null dans workshop/mods.json est IGNORE, avec
un message. Sa premiere publication passe par tools/premiere_publication.py :
c'est Steam qui attribue l'identifiant, et il faut le recopier dans le registre.

Rien n'est saisi a la main le jour de la sortie. C'est le point : la 1.3 a ete
publiee avec un .vdf edite par une expression reguliere trop gourmande, qui a
mange la ligne publishedfileid et cree un doublon du mod.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
REGISTRE = RACINE / "workshop" / "mods.json"


def mods():
    return json.loads(REGISTRE.read_text(encoding="utf-8"))["mods"]


def version(source):
    txt = (RACINE / source / "descriptor.mod").read_text(encoding="utf-8-sig")
    m = re.search(r'^version\s*=\s*"([^"]+)"', txt, re.M)
    if not m:
        sys.exit("%s/descriptor.mod : pas de version" % source)
    return m.group(1)


def changenote():
    out = subprocess.run([sys.executable, str(RACINE / "tools" / "changenote.py")],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def echapper(valeur):
    """Format Clausewitz : guillemets et antislashs a proteger, et pas de
    saut de ligne brut dans une valeur."""
    return (valeur.replace("\\", "\\\\")
                  .replace('"', "'")
                  .replace("\r\n", " ")
                  .replace("\n", " "))


def construire(mod, build, note):
    cle = mod["cle"]
    source = RACINE / mod["source"]
    dest = build / cle
    dest.mkdir(parents=True)

    contenu = dest / "content"
    shutil.copytree(source, contenu)

    # Sans remote_file_id, le jeu telecharge le mod mais ne l'active pas. Il
    # n'a rien a faire dans le depot - il vaut pour la copie publiee, pas pour
    # un mod local - donc on l'ajoute ici et seulement ici.
    desc = contenu / "descriptor.mod"
    txt = desc.read_text(encoding="utf-8-sig")
    if "remote_file_id" not in txt:
        txt = txt.rstrip() + '\nremote_file_id="%s"\n' % mod["publishedfileid"]
        desc.write_text(txt, encoding="utf-8-sig")

    apercu = dest / "thumbnail.png"
    shutil.copy2(RACINE / mod["apercu"], apercu)

    # SteamCMD n'ecrit que la langue par defaut : on y met l'anglaise. La
    # francaise se pose a la main sur la page, dans son onglet de langue.
    description = (RACINE / mod["description"]).read_text(encoding="utf-8")

    gabarit = (RACINE / "workshop" / "item.vdf.template").read_text(encoding="utf-8")
    vdf = (gabarit
           .replace("@PUBLISHEDFILEID@", mod["publishedfileid"])
           .replace("@TITLE@", echapper(mod["titre"]))
           .replace("@CONTENTFOLDER@", str(contenu))
           .replace("@PREVIEWFILE@", str(apercu))
           .replace("@DESCRIPTION@", echapper(description))
           .replace("@CHANGENOTE@", echapper(note)))

    restants = re.findall(r"@[A-Z_]+@", vdf)
    if restants:
        sys.exit("%s : marqueurs non remplaces : %s" % (cle, ", ".join(restants)))
    if mod["publishedfileid"] not in vdf:
        sys.exit("%s : publishedfileid absent du manifeste, on n'ecrit pas" % cle)

    (dest / "item.vdf").write_text(vdf, encoding="utf-8")

    v = version(mod["source"])
    archive = build / ("%s_v%s.zip" % (mod["source"], v))
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(contenu.rglob("*")):
            if f.is_file():
                z.write(f, Path(mod["source"]) / f.relative_to(contenu))

    fichiers = sum(1 for f in contenu.rglob("*") if f.is_file())
    print("  %-9s v%-10s %4d fichiers  %5.1f Mio"
          % (cle, v, fichiers, archive.stat().st_size / 1048576))

    # Origins embarque 250 icones de technologies. Une copie a la main peut
    # oublier gfx/ ; ce controle ne le peut pas.
    icones = contenu / "gfx" / "interface" / "icons" / "technologies"
    if cle == "origins":
        n = len(list(icones.glob("*.dds"))) if icones.exists() else 0
        if n < 200:
            sys.exit("origins : %d icones seulement, le dossier gfx/ n'a pas suivi" % n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--mod", help="ne construire que ce mod (sa cle)")
    args = ap.parse_args()

    build = Path(args.sortie).resolve()
    if build.exists():
        shutil.rmtree(build)
    build.mkdir(parents=True)

    note = changenote()
    choisis = [m for m in mods() if not args.mod or m["cle"] == args.mod]
    if args.mod and not choisis:
        sys.exit("aucun mod de cle %r dans workshop/mods.json" % args.mod)

    publiables, attente = [], []
    for m in choisis:
        (publiables if m["publishedfileid"] else attente).append(m)

    for m in publiables:
        construire(m, build, note)

    for m in attente:
        print("  %-9s IGNORE : jamais publie, pas d'identifiant Workshop."
              % m["cle"])
        print("            -> python tools/premiere_publication.py %s" % m["cle"])

    if not publiables:
        sys.exit("aucun mod publiable : tous les identifiants sont absents")

    (build / "publies.txt").write_text(
        "\n".join(m["cle"] for m in publiables) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
