#!/usr/bin/env python3
"""Synchronise la source du mod vers les dossiers de publication.

Une seule source de verite : ad_astra/. Tout le reste en decoule.
Ecrit apres avoir constate que kit/content/ n'embarquait pas gfx/ :
les 101 icones des technologies d'epoque n'etaient pas publiees.
Une copie a la main omet un dossier ; ce script ne peut pas.
"""
import shutil, subprocess, sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "ad_astra"
CIBLES = [RACINE / "kit" / "content", RACINE / "kit" / "repo" / "ad_astra"]
ARCHIVE = RACINE / "kit" / "ad_astra_1.2.1.zip"


def version():
    for ligne in (SOURCE / "descriptor.mod").read_text(encoding="utf-8").splitlines():
        if ligne.startswith("version="):
            return ligne.split('"')[1]
    sys.exit("descriptor.mod : pas de version")


def main():
    v = version()
    print(f"source : {SOURCE}  (version {v})")
    for cible in CIBLES:
        if cible.exists():
            shutil.rmtree(cible)
        shutil.copytree(SOURCE, cible)
        print(f"  -> {cible.relative_to(RACINE)}")

    # le .mod de lancement suit la meme version
    lanceur = RACINE / "ad_astra.mod"
    txt = lanceur.read_text(encoding="utf-8")
    depot = RACINE / "kit" / "repo" / "ad_astra.mod"
    depot.write_text(txt, encoding="utf-8")

    archive = RACINE / "kit" / f"ad_astra_{v}.zip"
    for vieille in (RACINE / "kit").glob("ad_astra_*.zip"):
        vieille.unlink()
    subprocess.run(["zip", "-qr", str(archive), "."],
                   cwd=CIBLES[0], check=True)
    print(f"  -> {archive.relative_to(RACINE)}")

    # controle : l'archive doit contenir exactement la source
    attendus = sorted(p.relative_to(SOURCE).as_posix()
                      for p in SOURCE.rglob("*") if p.is_file())
    sortie = subprocess.run(["unzip", "-Z1", str(archive)],
                            capture_output=True, text=True, check=True)
    obtenus = sorted(l for l in sortie.stdout.split() if not l.endswith("/"))
    if attendus != obtenus:
        manque = set(attendus) - set(obtenus)
        trop = set(obtenus) - set(attendus)
        sys.exit(f"ECART archive/source\n  manquant : {sorted(manque)[:5]}\n  en trop : {sorted(trop)[:5]}")
    print(f"controle : {len(attendus)} fichiers, archive conforme")


if __name__ == "__main__":
    main()
