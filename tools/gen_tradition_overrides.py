#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - verrouillage des traditions pendant le confinement.

Decision : une civilisation encore clouee au sol n'adopte pas de traditions
galactiques. Elles se rouvrent toutes a l'emergence.

Le verrou se pose sur les CATEGORIES de traditions, qui acceptent un bloc
`potential` evalue en scope pays. Le script repart des fichiers vanilla et
reinjecte chaque categorie telle quelle, en ajoutant la garde - on ne reecrit
jamais le contenu a la main, donc une mise a jour du jeu se re-absorbe en
relancant le script.

    python3 gen_tradition_overrides.py <dossier_vanilla_tradition_categories> --out <fichier>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clausewitz import top_level_blocks  # noqa: E402

GUARD = (
    "\tpotential = {\n"
    "\t\t# Ad Astra : pas de traditions tant que la civilisation est au sol.\n"
    "\t\tOR = {\n"
    "\t\t\tNOT = { has_origin = origin_adastra }\n"
    "\t\t\thas_country_flag = adastra_completed\n"
    "\t\t}\n"
)


def inject(name, block):
    """Ajoute la garde au bloc potential existant, ou en cree un."""
    m = re.search(r"^\tpotential = \{", block, re.M)
    if m:
        # on ouvre le potential existant avec notre garde : semantique ET
        return block[:m.start()] + GUARD + block[m.end():]
    # pas de potential : on en insere un juste apres l'accolade ouvrante
    head = block.index("{") + 1
    return block[:head] + "\n" + GUARD + "\t}\n" + block[head:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_dir")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out, count, skipped = [], 0, []
    out.append("# Ad Astra 1.2 - verrouillage des traditions pendant le confinement.")
    out.append("# FICHIER GENERE PAR tools/gen_tradition_overrides.py - NE PAS EDITER A LA MAIN.")
    out.append("#")
    out.append("# Les categories sont reprises telles quelles depuis le jeu de base, avec")
    out.append("# une seule garde ajoutee. Aucun autre empire n'est affecte.")
    out.append("")

    for fname in sorted(os.listdir(args.vanilla_dir)):
        if not fname.endswith(".txt") or "README" in fname:
            continue
        path = os.path.join(args.vanilla_dir, fname)
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            src = f.read()
        # les @variables doivent rester resolvables : on les recopie en tete
        for m in re.finditer(r"^(@\w+\s*=\s*\S+)\s*$", src, re.M):
            line = m.group(1)
            if line not in out:
                out.append(line)
        for name, s, e in top_level_blocks(src):
            if not name.startswith("tradition_"):
                skipped.append(name)
                continue
            out.append("")
            out.append("### %s (%s)" % (name, fname))
            out.append(inject(name, src[s:e]))
            count += 1

    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("categories verrouillees : %d" % count)
    if skipped:
        print("blocs ignores (non-categorie) : %s" % ", ".join(sorted(set(skipped))))
    print("ecrit : %s" % args.out)


if __name__ == "__main__":
    main()
