#!/usr/bin/env python3
"""Construit Ad Astra et pose exactement l'archive dans le mod local."""
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


RACINE = Path(__file__).resolve().parent.parent
ESPACE_PAR_DEFAUT = RACINE.parent


def lance(command):
    print("+", " ".join(str(part) for part in command))
    subprocess.run(command, cwd=RACINE, check=True)


def version(chemin):
    for ligne in chemin.read_text(encoding="utf-8-sig").splitlines():
        if ligne.startswith("version="):
            return ligne.split('"')[1]
    raise RuntimeError("version absente de %s" % chemin)


def copie_miroir(source, cible):
    # 18/08 : le staging evite de laisser le launcher sur une copie incomplete.
    with tempfile.TemporaryDirectory(prefix="adastra_sync_", dir=cible.parent) as temporaire:
        nouveau = Path(temporaire) / "ad_astra"
        shutil.copytree(source, nouveau)
        precedent = cible.parent / ".ad_astra_precedent"
        if precedent.exists():
            raise RuntimeError("staging precedent present : %s" % precedent)
        if cible.exists():
            cible.rename(precedent)
        try:
            shutil.move(str(nouveau), str(cible))
        except Exception:
            if precedent.exists() and not cible.exists():
                precedent.rename(cible)
            raise
        if precedent.exists():
            shutil.rmtree(precedent)


def main():
    espace = ESPACE_PAR_DEFAUT.resolve()
    if (espace / "repo").resolve() != RACINE:
        raise RuntimeError("workspace local inattendu : %s" % espace)

    lance([sys.executable, "tools/verify_generated.py"])
    lance([sys.executable, "tools/verify_1_2.py"])
    lance([sys.executable, "tools/verify_release.py"])
    lance([sys.executable, "tools/ci_release.py", "--sortie", "build"])

    archives = sorted((RACINE / "build").glob("ad_astra_v*.zip"))
    if len(archives) != 1:
        raise RuntimeError("une archive Ad Astra attendue, trouvees : %s" % archives)
    archive = archives[0]
    shutil.copy2(archive, espace / "maj_1_4.zip")

    cible = espace / "dev" / "ad_astra"
    if not cible.parent.is_dir():
        raise RuntimeError("dossier dev absent : %s" % cible.parent)
    with tempfile.TemporaryDirectory(prefix="adastra_archive_", dir=espace) as temporaire:
        with zipfile.ZipFile(archive) as contenu:
            contenu.extractall(temporaire)
        source = Path(temporaire) / "ad_astra"
        if not (source / "descriptor.mod").is_file():
            raise RuntimeError("archive sans ad_astra/descriptor.mod")
        copie_miroir(source, cible)

    attendu = version(RACINE / "ad_astra" / "descriptor.mod")
    charge = version(cible / "descriptor.mod")
    if charge != attendu:
        raise RuntimeError("copie launcher %s, source %s" % (charge, attendu))
    print("deploiement local termine : %s" % charge)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError, zipfile.BadZipFile) as erreur:
        print("ERREUR : %s" % erreur, file=sys.stderr)
        sys.exit(1)
