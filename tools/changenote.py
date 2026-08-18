#!/usr/bin/env python3
"""Extrait la note de changement Steam de la premiere section du CHANGELOG.

Une seule source de verite. On ecrit le changelog une fois, et Steam, la
release GitHub et la CI lisent tous le meme texte. La note de la 1.3 avait
ete recopiee a la main dans le .vdf, la description et l'annonce : trois
copies, dont une parlait encore d'un programme de satellites abandonne.

  python tools/changenote.py              -> texte plat pour Steam
  python tools/changenote.py --markdown   -> markdown pour la release GitHub
"""
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CHANGELOG = RACINE / "CHANGELOG.md"

# Steam accepte 8000 caracteres dans une note de changement. On se garde une
# marge : un texte coupe net au caractere 8000 finit au milieu d'un mot.
LIMITE = 7800


def premiere_section(texte):
    """Le bloc entre le premier '## ' et le suivant, titre compris."""
    lignes = texte.splitlines()
    debut = None
    for i, l in enumerate(lignes):
        if l.startswith("## "):
            if debut is None:
                debut = i
            else:
                return lignes[debut:i]
    if debut is None:
        sys.exit("CHANGELOG.md : aucune section '## ' trouvee")
    return lignes[debut:]


def en_texte_plat(lignes):
    """Deshabille le markdown. Steam n'affiche pas de gras dans une note."""
    out = []
    for l in lignes:
        if l.startswith("> "):          # les encadres ne passent pas en texte plat
            l = l[2:]
        if l.startswith("### "):
            out.append("")
            out.append("== %s ==" % l[4:].strip())
            continue
        if l.startswith("## "):
            out.append(l[3:].strip())
            continue
        l = re.sub(r"\*\*(.+?)\*\*", r"\1", l)      # gras
        l = re.sub(r"\*(.+?)\*", r"\1", l)          # italique
        l = re.sub(r"`(.+?)`", r"\1", l)            # code
        l = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", l)  # liens
        l = re.sub(r"^- ", "- ", l)
        out.append(l.rstrip())
    return "\n".join(out).strip() + "\n"


def couper(texte, limite=LIMITE):
    """Coupe a la derniere phrase entiere sous la limite."""
    if len(texte) <= limite:
        return texte
    tronque = texte[:limite]
    fin = max(tronque.rfind(". "), tronque.rfind(".\n"), tronque.rfind("\n\n"))
    if fin > limite // 2:
        tronque = tronque[:fin + 1]
    return tronque.rstrip() + "\n\n(suite : voir le CHANGELOG sur GitHub)\n"


def main():
    markdown = "--markdown" in sys.argv
    lignes = premiere_section(CHANGELOG.read_text(encoding="utf-8"))
    if markdown:
        # La release GitHub rend le markdown : on garde tout sauf le titre,
        # que GitHub affiche deja comme nom de la release.
        sys.stdout.write("\n".join(lignes[1:]).strip() + "\n")
        return
    sys.stdout.write(couper(en_texte_plat(lignes)))


if __name__ == "__main__":
    main()
