#!/usr/bin/env python3
"""La toute premiere publication d'un mod sur le Workshop. A LANCER A LA MAIN.

  python tools/premiere_publication.py core

C'est le seul geste de toute la chaine qui ne peut pas etre automatise, et
c'est volontaire. Steam attribue l'identifiant d'un objet au moment ou il le
cree : tant qu'on ne le connait pas, on ne peut pas verifier qu'on met a jour
le bon objet. Or publier sans identifiant ne provoque pas une erreur - ca cree
un SECOND objet, avec ses propres abonnes. C'est arrive le 16/08/2026 avec
Origins, et il a fallu supprimer le doublon a la main.

Donc : la CI ne publie que ce que ce script a deja fait naitre.

Le script :
  1. construit le contenu du mod, avec un manifeste SANS publishedfileid ;
  2. lance SteamCMD, qui cree l'objet et annonce son identifiant ;
  3. ecrit cet identifiant dans workshop/mods.json.

A partir de la, la CI reprend la main pour toujours.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
REGISTRE = RACINE / "workshop" / "mods.json"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cle = sys.argv[1]

    donnees = json.loads(REGISTRE.read_text(encoding="utf-8"))
    mod = next((m for m in donnees["mods"] if m["cle"] == cle), None)
    if mod is None:
        sys.exit("aucun mod de cle %r dans le registre" % cle)
    if mod["publishedfileid"]:
        sys.exit("%s a deja l'identifiant %s. La CI s'en occupe - ce script "
                 "ne sert qu'a la premiere fois." % (cle, mod["publishedfileid"]))

    build = RACINE / "build_premiere" / cle
    if build.exists():
        shutil.rmtree(build)
    build.mkdir(parents=True)

    contenu = build / "content"
    shutil.copytree(RACINE / mod["source"], contenu)
    apercu = build / "thumbnail.png"
    shutil.copy2(RACINE / mod["apercu"], apercu)
    description = (RACINE / mod["description"]).read_text(encoding="utf-8")
    plat = description.replace('"', "'").replace("\n", " ")

    # Pas de publishedfileid : c'est justement ce qu'on demande a Steam.
    vdf = build / "item.vdf"
    vdf.write_text(
        '"workshopitem"\n{\n'
        '\t"appid"\t\t"281990"\n'
        '\t"contentfolder"\t\t"%s"\n'
        '\t"previewfile"\t\t"%s"\n'
        '\t"visibility"\t\t"2"\n'
        '\t"title"\t\t"%s"\n'
        '\t"description"\t\t"%s"\n'
        '\t"changenote"\t\t"Premiere publication."\n'
        '}\n' % (contenu, apercu, mod["titre"], plat),
        encoding="utf-8")

    print("Mod        : %s" % mod["nom"])
    print("Contenu    : %s" % contenu)
    print("Manifeste  : %s" % vdf)
    print()
    print("visibility = 2 : l'objet naitra CACHE. Tu le rendras public depuis")
    print("sa page, une fois la description et les images en place.")
    print()
    identifiant = input("Lancer SteamCMD maintenant ? Tape ton pseudo Steam "
                        "(ou Entree pour t'arreter la) : ").strip()
    if not identifiant:
        print("\nArrete. Pour le faire toi-meme :")
        print('  steamcmd +login TON_PSEUDO +workshop_build_item "%s" +quit' % vdf)
        print("Puis recopie l'identifiant annonce dans workshop/mods.json.")
        return

    steamcmd = shutil.which("steamcmd") or shutil.which("steamcmd.exe")
    if not steamcmd:
        sys.exit("steamcmd introuvable dans le PATH.")

    sortie = subprocess.run(
        [steamcmd, "+login", identifiant, "+workshop_build_item", str(vdf), "+quit"],
        capture_output=True, text=True)
    print(sortie.stdout[-3000:])

    trouve = re.search(r"PublishFileID (\d+)", sortie.stdout) or \
        re.search(r"Success.*?(\d{9,})", sortie.stdout, re.S)
    if not trouve:
        sys.exit("SteamCMD n'a pas annonce d'identifiant. Rien n'a ete "
                 "enregistre - relis la sortie ci-dessus.")

    mod["publishedfileid"] = trouve.group(1)
    REGISTRE.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print("\n%s -> %s, enregistre dans workshop/mods.json." % (cle, mod["publishedfileid"]))
    print("Commite ce fichier : sans lui, la CI refusera de publier ce mod.")


if __name__ == "__main__":
    main()
