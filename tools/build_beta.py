#!/usr/bin/env python3
"""Construit une archive locale pour le canal beta GitHub.

La beta ne doit jamais reutiliser l'identifiant Workshop de la version stable.
Elle porte donc son propre nom et son propre dossier de launcher local.
"""

import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "ad_astra"
LAUNCHER = ROOT / "ad_astra.mod"
INSTALL = ROOT / "docs" / "BETA.md"
BETA_NAME = "Ad Astra: Origins - Beta"
BETA_FOLDER = "adastra_beta"


def read_version(text):
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise SystemExit("descriptor.mod : version absente")
    return match.group(1)


def replace_field(text, field, value):
    pattern = rf'^{field}\s*=\s*"[^"]*"\s*$'
    replaced, count = re.subn(pattern, f'{field}="{value}"', text,
                              count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f"champ {field} introuvable dans le descripteur")
    return replaced


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sortie", required=True,
                        help="dossier qui recevra l'archive beta")
    args = parser.parse_args()

    descriptor = (SOURCE / "descriptor.mod").read_text(encoding="utf-8-sig")
    version = read_version(descriptor)
    launcher = LAUNCHER.read_text(encoding="utf-8-sig")
    if read_version(launcher) != version:
        raise SystemExit("les descripteurs du mod et du launcher divergent")

    output = Path(args.sortie).resolve()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"ad_astra_beta_v{version}.zip"

    with tempfile.TemporaryDirectory(prefix="ad_astra_beta_") as temporary:
        staging = Path(temporary)
        mod_root = staging / "mod"
        content = mod_root / BETA_FOLDER
        shutil.copytree(SOURCE, content)

        beta_descriptor = replace_field(descriptor, "name", BETA_NAME)
        beta_descriptor = re.sub(r'^remote_file_id\s*=.*\n?', "", beta_descriptor,
                                 flags=re.MULTILINE)
        (content / "descriptor.mod").write_text(beta_descriptor, encoding="utf-8")

        beta_launcher = replace_field(launcher, "name", BETA_NAME)
        beta_launcher = replace_field(beta_launcher, "path", f"mod/{BETA_FOLDER}")
        beta_launcher = re.sub(r'^remote_file_id\s*=.*\n?', "", beta_launcher,
                                flags=re.MULTILINE)
        (mod_root / f"{BETA_FOLDER}.mod").write_text(beta_launcher, encoding="utf-8")

        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zipped:
            for file in sorted(staging.rglob("*")):
                if file.is_file():
                    zipped.write(file, file.relative_to(staging))
            zipped.write(INSTALL, "INSTALL_BETA.md")

    with zipfile.ZipFile(archive) as zipped:
        names = set(zipped.namelist())
        required = {
            "INSTALL_BETA.md",
            f"mod/{BETA_FOLDER}.mod",
            f"mod/{BETA_FOLDER}/descriptor.mod",
        }
        missing = required - names
        if missing:
            raise SystemExit("archive beta incomplete : " + ", ".join(sorted(missing)))
        packaged = zipped.read(f"mod/{BETA_FOLDER}/descriptor.mod").decode("utf-8")
        if BETA_NAME not in packaged or "remote_file_id" in packaged:
            raise SystemExit("descripteur beta invalide")

    print(f"beta v{version}: {archive.name} ({archive.stat().st_size / 1048576:.1f} Mio)")


if __name__ == "__main__":
    main()
