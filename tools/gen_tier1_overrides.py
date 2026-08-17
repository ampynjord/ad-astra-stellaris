#!/usr/bin/env python3
"""
Ad Astra 1.1 - Générateur d'overrides pour les techs de tier 1 sans prérequis.

Bug bêta : notre verrou couvre les 31 techs de départ, mais les techs de TIER 1
SANS prérequis restent proposables par le tirage dès le début de partie
("modern techs at Late Medieval age" - retour Nobumon).

Ce script se lance quand le PC est en ligne, sur les fichiers vanilla 4.4 :
    python3 gen_tier1_overrides.py "<...>/Stellaris/common/technology" \
        --ours ../ad_astra/common/technology/zzz_adastra_tech_overrides.txt \
        --out  ../ad_astra/common/technology/zzz_adastra_tier1_overrides.txt

Il copie chaque bloc vanilla concerné TEL QUEL et insère notre garde dans le
potential (même formule que les 31 techs de départ) :
    OR = { NOT = { has_origin = origin_adastra } has_country_flag = adastra_unlock_space }
Les techs déjà couvertes par notre override et les start_tech sont exclues.
Un rapport liste ce qui a été gaté pour relecture manuelle (mapping d'âge affinable).
"""
import argparse, os, re, sys

# 1.2 : la table d'ages vit dans tools/vanilla_tech_age_map.py, seule source de
# verite, partagee avec tools/apply_vanilla_tech_ages.py. La 1.1 gardait ici un
# dictionnaire local d'une seule entree ; il y en a douze maintenant, et elles
# doivent survivre a une regeneration.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vanilla_tech_age_map import TECH_AGE  # noqa: E402

HISTORICAL = {k: "adastra_unlock_%s" % v[0] for k, v in TECH_AGE.items()}

# 16/08 : le palier 1 s'ouvre a l'Age spatial, le palier 2 attend l'emergence.
# Le palier 3 exigeant six technos de palier 2 deja cherchees, il se ferme de
# lui-meme - c'est ce qui empeche la terraformation et les cuirassiers
# d'apparaitre avant la percee, sans enumerer un seul tech de palier 3.
def guard_tier(tier):
    drapeau = ("adastra_unlock_space" if tier == "1" else "adastra_completed")
    return ("\t\t# Ad Astra : verrou d'age (tier %s)\n"
            "\t\tOR = {\n"
            "\t\t\tNOT = { has_origin = origin_adastra }\n"
            "\t\t\thas_country_flag = %s\n"
            "\t\t}" % (tier, drapeau))


GUARD = guard_tier("1")

def strip_comments(text):
    return re.sub(r"#[^\n]*", "", text)

def top_level_blocks(text):
    """Yield (name, block_text) for each top-level `name = { ... }`."""
    i, n = 0, len(text)
    while i < n:
        m = re.compile(r"([A-Za-z0-9_@\.]+)\s*=\s*\{").search(text, i)
        if not m:
            return
        # Ignorer les blocs commentés : un '#' entre le début de ligne et le match
        line_start = text.rfind("\n", 0, m.start()) + 1
        if "#" in text[line_start:m.start()]:
            nl = text.find("\n", m.start())
            i = n if nl == -1 else nl + 1
            continue
        depth, j = 1, m.end()
        while j < n and depth:
            c = text[j]
            if c == "#":
                j = text.find("\n", j)
                if j == -1: j = n
            elif c == "{": depth += 1
            elif c == "}": depth -= 1
            j += 1
        yield m.group(1), text[m.start():j]
        i = j

def block_field(block, field):
    m = re.search(rf"\b{field}\s*=\s*([^\s{{}}]+)", strip_comments(block))
    return m.group(1) if m else None

def has_block(block, field):
    return re.search(rf"\b{field}\s*=\s*\{{", strip_comments(block)) is not None

def inject_guard(block, tier='1'):
    """Insert GUARD inside existing potential, or add a potential block."""
    garde = guard_tier(tier)
    m = re.search(r"\bpotential\s*=\s*\{", block)
    if m:
        return block[:m.end()] + "\n" + garde + block[m.end():]
    # pas de potential : on en ajoute un avant la derniere accolade
    last = block.rfind("}")
    return block[:last] + "\tpotential = {\n" + garde + "\n\t}\n" + block[last:]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vanilla_dir", help="dossier common/technology du jeu")
    ap.add_argument("--ours", required=True, help="notre zzz_adastra_tech_overrides.txt")
    ap.add_argument("--out", required=True, help="fichier d'override a generer")
    args = ap.parse_args()

    ours = open(args.ours, encoding="utf-8", errors="replace").read()
    already = set(re.findall(r"^(tech_[A-Za-z0-9_]+)\s*=\s*\{", ours, re.M))

    picked, skipped = [], []
    # 00_test.txt : fichier de test livre avec le jeu, il contient tech_alpha,
    # tech_beta, tech_gamma et tech_overridden. Sans cette exclusion on genere
    # des surcharges pour des technologies qui n'existent pas en partie.
    IGNORES = {"00_test.txt"}
    for fname in sorted(os.listdir(args.vanilla_dir)):
        if not fname.endswith(".txt") or fname in IGNORES:
            continue
        path = os.path.join(args.vanilla_dir, fname)
        text = open(path, encoding="utf-8", errors="replace").read()
        # Les @variables sont locales au fichier : on inline leurs valeurs dans les blocs copies.
        at_vars = dict(re.findall(r"^(@[A-Za-z0-9_]+)\s*=\s*(\S+)", text, re.M))
        def inline_vars(b):
            for k in sorted(at_vars, key=len, reverse=True):
                b = b.replace(k, at_vars[k])
            return b
        for name, block in top_level_blocks(text):
            block = inline_vars(block)
            if not name.startswith("tech_"):
                continue
            tier = block_field(block, "tier")
            if tier not in ("1", "2"):
                continue
            # v2 (1.1) : les techs AVEC prerequis sont gatees aussi - leurs prerequis
            # (labos, etc.) sont donnes par les granters d'age bien avant l'epoque voulue.
            if block_field(block, "start_tech") == "yes":
                skipped.append((name, "start_tech"))
                continue
            if name in already:
                skipped.append((name, "deja dans notre override"))
                continue
            picked.append((fname, name, block))

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("# Ad Astra 1.1 - Overrides generes : techs de tier 1 et 2,\n")
        f.write("# gatees a l'Age spatial pour l'origine Ad Astra (les autres empires ne sont pas affectes).\n")
        f.write("# Genere par tools/gen_tier1_overrides.py - NE PAS EDITER A LA MAIN.\n\n")
        for fname, name, block in picked:
            f.write(f"# source vanilla : {fname}\n")
            out_block = inject_guard(block, block_field(block, "tier") or "1")
            if name in HISTORICAL:
                out_block = out_block.replace("adastra_unlock_space", HISTORICAL[name])
            f.write(out_block.rstrip() + "\n\n")

    print(f"{len(picked)} tech(s) gatee(s) -> {args.out}")
    for fname, name, _ in picked:
        print(f"  GATE  {name}  ({fname})")
    if skipped:
        print(f"{len(skipped)} exclue(s) :")
        for name, why in skipped:
            print(f"  SKIP  {name}  ({why})")
    print("\nRelecture manuelle : si une tech merite un age plus precoce que l'Age spatial,")
    print("remplacer adastra_unlock_space par le flag d'age voulu dans le fichier genere.")

if __name__ == "__main__":
    main()
