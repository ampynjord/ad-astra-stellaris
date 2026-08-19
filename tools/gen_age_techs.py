#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.2 - génère les 50 technologies d'âge, leur localisation FR/EN
et les déclencheurs scriptés qui font passer les techs custom AVANT le vanilla.

Usage :  python3 tools/gen_age_techs.py [racine_du_mod]

Règle de conception (1.2) : les techs custom ne concurrencent jamais le vanilla,
elles le précèdent. Le vanilla d'un âge ne s'ouvre qu'une fois les 5 techs de
cet âge terminées (déclencheur adastra_vanilla_open_<age>).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from age_techs_data import vagues  # noqa: E402
from age_techs_data import (AGES, MAJEURES, RESOURCE_TECH,  # noqa: E402
                            TECHS, UNLOCKS)
from vanilla_age_map import VANILLA_AGE_MAP, VANILLA_PREREQ  # noqa: E402

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ad_astra")

AREAS = ("physics", "society", "engineering")

# Noms anglais des batiments d'epoque cites dans les descriptions.
BATIMENTS_EN = {
    "Monument des ancêtres": "Ancestral Monument",
    "Grenier": "Granary",
    "Fonderie": "Foundry",
    "Maison des tablettes": "House of Tablets",
    "Tribunal": "Courthouse",
    "Moulin": "Mill",
    "Citadelle": "Citadel",
    "Université": "University",
    "Manufacture": "Manufactory",
    "Station de radiodiffusion": "Broadcasting Station",
    "École publique": "Public School",
}
HEADER = ("# Ad Astra 1.2 - Les Ages : arborescence historique (50 techs, tier 0).\n"
          "# FICHIER GENERE PAR tools/gen_age_techs.py - NE PAS EDITER A LA MAIN.\n"
          "# Source de verite : tools/age_techs_data.py\n")


def prereq_map():
    """L'arbre d'un age (1.5, 19/08 - docs/design_recherche_par_arbre.md).

    Les 25 techs d'un age sont rangees par date en cinq rangs de cinq
    (fonction `vagues`, le nom est historique). Le rang 1 exige le PILIER du
    meme domaine a l'age precedent (regle 1.2 : la premiere techno declaree
    du domaine, la plus emblematique). Un rang N >= 2 exige UNE tech de rang
    N-1 du meme domaine dans le meme age ; a defaut, la premiere tech de rang
    N-1 tous domaines confondus.

    Le moteur ne propose une techno que si ses prerequis sont acquis : c'est
    lui qui tient l'ordre historique, sans drapeau ni recalcul mensuel. Et
    comme il faut les 25 pour passer l'age, aucune branche ne peut etre
    laissee de cote."""
    anchor = {a: None for a in AREAS}
    out = {}
    for age, _flag, _cost, _vflag in AGES:
        rangs = vagues(TECHS[age])
        par_rang = {}
        for t in sorted(TECHS[age], key=lambda t: (t.get("year") or 0)):
            par_rang.setdefault(rangs[t["key"]], []).append(t)
        current = {a: None for a in AREAS}
        for t in TECHS[age]:
            a = t["area"]
            r = rangs[t["key"]]
            if r == 1:
                out[t["key"]] = [anchor[a]] if anchor[a] else []
            else:
                prev = par_rang.get(r - 1, [])
                meme_domaine = [p for p in prev if p["area"] == a]
                choix = (meme_domaine or prev)[0]
                out[t["key"]] = [choix["key"]]
            if current[a] is None:
                current[a] = t["key"]
        for a in AREAS:
            if current[a]:
                anchor[a] = current[a]
    return out


def poids(t, est_pilier):
    """Le multiplicateur de cout d'une techno. On garde la raison la plus forte."""
    p = 1.0
    if est_pilier:
        p = max(p, 1.2)
    if t["unlocks"] or t["key"] in UNLOCKS:
        p = max(p, 1.4)
    if t["key"] in MAJEURES:
        p = max(p, 1.8)
    return p


def couts(base, age_techs):
    """Cout de chaque techno de l'age : base x poids, arrondi a la dizaine."""
    vus = set()
    out = {}
    for t in age_techs:
        pilier = t["area"] not in vus
        vus.add(t["area"])
        c = base * poids(t, pilier)
        out[t["key"]] = int(round(c / 5.0)) * 5
    return out


# 1.4 (17/08) : « certaines techs ont +0 % ». Les bonus par techno etaient
# de 0,3 a 0,8 % ; l'interface les arrondit a l'entier, donc « +0 % ». Retour
# d'ampynjord : meme nombre de technos, mais un bonus lisible. Regle : tout
# multiplicateur est arrondi au pour-cent, plancher 1 %. Les valeurs _add
# (stabilite, logements, commodites) s'affichent en decimal et ne bougent pas.
# Au passage pop_growth_speed, qui n'existe pas en 4.4 (« Invalid modifier »
# dans error.log), devient logistic_growth_mult.
def modificateur_lisible(k, v):
    if k == "pop_growth_speed":
        k = "logistic_growth_mult"
    if k.endswith("_add"):
        return k, v
    signe = -1 if v < 0 else 1
    return k, signe * max(0.01, round(abs(v) * 100) / 100.0)


def gen_techs(prereqs):
    lines = [HEADER]
    for _i, (age, flag, cost, _vflag) in enumerate(AGES):
        suivant = AGES[_i + 1][1] if _i + 1 < len(AGES) else None
        lines.append("\n" + "#" * 60)
        lines.append("# AGE : %s (cout de base %d)" % (age.upper(), cost))
        lines.append("#" * 60 + "\n")
        cmap = couts(cost, TECHS[age])
        vg = vagues(TECHS[age])
        for t in TECHS[age]:
            b = ["%s = {" % t["key"]]
            b.append("\tcost = %d" % cmap[t["key"]])
            b.append("\tarea = %s" % t["area"])
            b.append("\t# tier 0 : verifie en jeu, ces technos entrent bien dans le tirage.")
            b.append("\t# Le tier 0 ne compte pas pour le deverrouillage des tiers suivants,")
            b.append("\t# donc nos 50 technos n'ouvrent aucun palier vanilla par accident.")
            b.append("\ttier = 0")
            b.append("\tcategory = { %s }" % t["cat"])
            b.append("\tweight = 100")
            p = prereqs[t["key"]]
            if p:
                b.append("\tprerequisites = { %s }" % " ".join('"%s"' % k for k in p))
            b.append("")
            b.append("\t# Visible uniquement pour Ad Astra, a partir de son age,")
            b.append("\t# et retiree du tirage une fois l'Ascension achevee.")
            b.append("\tpotential = {")
            b.append("\t\thas_origin = origin_adastra")
            b.append("\t\thas_country_flag = %s" % flag)
            b.append("\t\tNOT = { has_country_flag = adastra_completed }")
            # 1.3 : L'AGE COURANT, ET LUI SEUL.
            #
            # Les drapeaux d'age s'accumulent : sans cette exclusion, toutes les
            # technologies des ages traversees restent dans le tirage. Sur un
            # depart a l'Age spatial - ou l'initialisation pose les dix drapeaux
            # d'un coup - le joueur se retrouvait avec l'Atomisme et l'Astrolabe
            # proposes a cote du microprocesseur. Signale en test le 16/08.
            #
            # Aucun risque de perdre une techno en route : le verrou de la
            # situation interdit de quitter un age avant de les avoir toutes.
            #
            # 1.4 (17/08) : l'exclusion NE DOIT PLUS etre dans le potential.
            # give_technology exige que la techno ET SES PREREQUIS soient
            # valides pour l'empire ; or chaque techno a partir du Bronze a
            # pour prerequis le pilier de l'age precedent, dont le potential
            # devenait faux des que le drapeau de l'age suivant etait pose.
            # Resultat mesure en jeu : les 25 techs de la Pierre (sans
            # prerequis) passaient, et les 200 autres etaient TOUTES
            # refusees - « Attempting to give invalid technology » - quel
            # que soit l'ordre ou le jour de l'octroi. L'exclusion du
            # tirage passe donc par le poids (weight_modifier a zero),
            # ce qui laisse la techno valide comme prerequis.
            if suivant:
                b.append("\t\t# (l'age suivant retire la techno du tirage via")
                b.append("\t\t#  weight_modifier, pas via le potential - voir 1.4)")
            # 1.3 : la vague. Les vingt-cinq technologies d'un age ne s'ouvrent
            # pas toutes a l'entree : cinq par cinq, a 0, 20, 40, 60 et 80 % de
            # l'etape. La vague est deduite de la DATE de la techno, donc a
            # l'interieur d'un age elles arrivent dans l'ordre historique.
            # 1.5 : plus de drapeau de vague - l'ordre dans l'age est tenu par
            # les prerequis (arbre), voir prereq_map.
            b.append("\t\t# rang %d dans l'arbre de l'age" % vg[t["key"]])
            b.append("\t}")
            b.append("")
            # 1.4 : L'AGE COURANT, ET LUI SEUL - version qui ne casse pas
            # give_technology. Poids nul des que l'age suivant est atteint :
            # la techno sort du tirage mais reste une techno valide.
            if suivant:
                b.append("\tweight_modifier = {")
                b.append("\t\tfactor = 1")
                b.append("\t\tmodifier = {")
                b.append("\t\t\tfactor = 0")
                b.append("\t\t\thas_country_flag = %s" % suivant)
                b.append("\t\t}")
                b.append("\t}")
                b.append("")
            b.append("\tmodifier = {")
            for k, v in t["mods"].items():
                k, v = modificateur_lisible(k, v)
                b.append("\t\t%s = %s" % (k, ("%g" % v)))
            b.append("\t}")
            b.append("")
            # Marqueur visible sur la CARTE de recherche, pas seulement dans
            # l'infobulle. Retour du 15/08 : « toutes les techs spatiales
            # vanilla ont spawn, je savais pas lesquelles prendre ». A l'Age
            # spatial le tirage melange nos dix technos d'epoque et celles du
            # jeu de base, et rien ne les distingue a l'oeil. prereqfor_desc
            # ajoute une ligne coloree sur la carte elle-meme.
            b.append("\tprereqfor_desc = {")
            b.append("\t\tcustom = {")
            b.append('\t\t\ttitle = "adastra_tech_marque_%s"' % age)
            b.append('\t\t\tdesc = "adastra_tech_marque_desc"')
            b.append("\t\t}")
            b.append("\t}")
            b.append("")
            b.append("\tai_weight = { factor = 5 }")
            if t["unlocks"]:
                b.append("\t# Debloque le batiment d'epoque : %s" % t["unlocks"])
            b.append("}\n")
            lines.append("\n".join(b))
    return "\n".join(lines)



def gen_progression():
    """1.5 : la progression, c'est la recherche.

    Un declencheur par age (`adastra_tech_epoque_<age>` : la derniere techno
    acquise est l'une de ses 25) et un effet `adastra_progression_recherche`
    appele par adastra.132 sur on_tech_increased : si la techno appartient a
    l'age courant, +1 point de situation. Vingt-cinq points font passer
    l'etape (docs/design_recherche_par_arbre.md)."""
    out = ["# Ad Astra 1.5 - la progression, c'est la recherche.",
           "# FICHIER GENERE PAR tools/gen_age_techs.py - NE PAS EDITER A LA MAIN.",
           "#",
           "# Une technologie d'epoque acquise vaut un point de situation si elle",
           "# appartient a l'age courant. Vingt-cinq points font passer l'age.",
           ""]
    for age, flag, _c, _v in AGES:
        out.append("adastra_tech_epoque_%s = {" % age)
        out.append("\tOR = {")
        for t in TECHS[age]:
            out.append("\t\tlast_increased_tech = %s" % t["key"])
        out.append("\t}")
        out.append("}\n")
    return "\n".join(out) + "\n"


def gen_progression_effet():
    from age_techs_data import ETAPES_SITU
    out = ["# Ad Astra 1.5 - la progression, c'est la recherche.",
           "# FICHIER GENERE PAR tools/gen_age_techs.py - NE PAS EDITER A LA MAIN.",
           "",
           "# Recalage d'une sauvegarde d'avant la 1.5 (adastra.133, une fois) : la",
           "# progression devient 25 x (age atteint) + technologies de l'age acquises.",
           "adastra_recalage_progression = {"]
    for i_age, (age, flag, _c, _v) in enumerate(AGES):
        suivant = AGES[i_age + 1][1] if i_age + 1 < len(AGES) else None
        debut = ETAPES_SITU[age][0]
        out.append("\tif = {")
        out.append("\t\tlimit = {")
        out.append("\t\t\thas_country_flag = %s" % flag)
        if suivant:
            out.append("\t\t\tNOT = { has_country_flag = %s }" % suivant)
        else:
            out.append("\t\t\tNOT = { has_country_flag = adastra_program_started }")
        out.append("\t\t}")
        out.append("\t\tevery_situation = {")
        out.append("\t\t\tlimit = { is_situation_type = situation_adastra_ascension }")
        out.append("\t\t\tset_situation_progress = %d" % debut)
        for t in TECHS[age]:
            out.append("\t\t\tif = { limit = { owner = { has_technology = %s } } add_situation_progress = 1 }" % t["key"])
        out.append("\t\t}")
        out.append("\t}")
    out.append("}")
    out.append("")
    out.append("adastra_progression_recherche = {")
    for i_age, (age, flag, _c, _v) in enumerate(AGES):
        suivant = AGES[i_age + 1][1] if i_age + 1 < len(AGES) else None
        out.append("\tif = {")
        out.append("\t\tlimit = {")
        out.append("\t\t\thas_country_flag = %s" % flag)
        if suivant:
            out.append("\t\t\tNOT = { has_country_flag = %s }" % suivant)
        out.append("\t\t\tadastra_tech_epoque_%s = yes" % age)
        out.append("\t\t}")
        out.append("\t\tevery_situation = {")
        out.append("\t\t\tlimit = { is_situation_type = situation_adastra_ascension }")
        out.append("\t\t\tadd_situation_progress = 1")
        out.append("\t\t}")
        out.append("\t}")
    out.append("}")
    return "\n".join(out) + "\n"


def gen_loc(lang):
    """La description porte le texte d'ambiance PUIS ce que la techno debloque.

    Le moteur affiche tout seul le bloc modifier, mais rien d'autre : ni la
    ressource qu'une techno fait exister, ni le batiment qu'elle ouvre, ni le
    palier de capitale. Sans ces lignes, le joueur cherche a l'aveugle.
    §Y ... §! : le jaune du jeu de base, celui des effets."""
    key_name, key_desc = ("fr", "dfr") if lang == "french" else ("en", "den")
    fr = lang == "french"
    idx = 0 if fr else 1
    out = ["\ufeffl_%s:" % lang,
           " # Ad Astra 1.2 - Les Ages. GENERE par tools/gen_age_techs.py."]
    for age, _flag, _cost, _vflag in AGES:
        out.append(" # --- %s ---" % age)
        for t in TECHS[age]:
            desc = t[key_desc]
            extra = []
            if t["unlocks"]:
                # 1.4 : le nom anglais du batiment - la version anglaise avait
                # ete corrigee a la main et le generateur l'ecrasait.
                nom = t["unlocks"] if fr else BATIMENTS_EN.get(t["unlocks"], t["unlocks"])
                extra.append(("Débloque le bâtiment : %s." if fr
                              else "Unlocks the building: %s.") % nom)
            if t["key"] in UNLOCKS:
                extra.append(UNLOCKS[t["key"]][idx])
            if extra:
                desc += "\\n\\n§Y" + " ".join(extra) + "§!"
            out.append(' %s:0 "%s"' % (t["key"], t[key_name]))
            out.append(' %s_desc:0 "%s"' % (t["key"], desc))
    return "\n".join(out) + "\n"


def gen_gates():
    out = ["# Ad Astra 1.2 - verrous d'age.",
           "# GENERE PAR tools/gen_age_techs.py - NE PAS EDITER A LA MAIN.",
           "#",
           "# adastra_age_<age>_done      : 6 des 10 technos de l'age sont terminees.",
           "#   Un seuil, pas la totalite : un age propose 10 technos pour un budget",
           "#   de recherche d'environ 8, donc exiger les 10 verrouillerait le vanilla",
           "#   de l'age pour un joueur qui a simplement fait d'autres choix.",
           "# adastra_vanilla_open_<age>  : garde utilisee par les overrides de techs",
           "#   vanilla. Le vanilla d'un age ne s'ouvre qu'apres ses techs custom :",
           "#   les techs custom PRECEDENT le vanilla, elles ne le concurrencent pas.",
           "#   Le OR sur adastra_completed est un filet de securite : apres l'emergence",
           "#   les techs d'age quittent le tirage, le vanilla ne doit jamais rester",
           "#   verrouille a cause d'un age laisse inacheve.",
           ""]
    for age, _flag, _cost, vflag in AGES:
        n = len(TECHS[age])
        need = (n * 6 + 9) // 10          # 60 % arrondi au superieur
        out.append("# %s : %d technos sur %d suffisent." % (age, need, n))
        out.append("adastra_age_%s_done = {" % age)
        out.append("\tcalc_true_if = {")
        out.append("\t\tamount >= %d" % need)
        for t in TECHS[age]:
            out.append("\t\thas_technology = %s" % t["key"])
        out.append("\t}")
        out.append("}\n")
    # --- le verrou de passage d'age -------------------------------------
    out.append("")
    out.append("# adastra_age_<age>_all : les 10 technos de l'age, sans exception.")
    out.append("#")
    out.append("# Distinct de _done, qui n'en demande que six. Les deux ne servent pas a")
    out.append("# la meme chose : _done ouvre le vanilla de l'age (un joueur qui a fait")
    out.append("# d'autres choix ne doit pas perdre le contenu du jeu de base), tandis que")
    out.append("# _all commande le PASSAGE a l'age suivant. On ne quitte pas un age tant")
    out.append("# qu'il reste quelque chose a y inventer : la barre de la situation atteint")
    out.append("# la fin de l'etape et s'y arrete, en attendant la derniere decouverte.")
    out.append("")
    for age, _flag, _cost, vflag in AGES:
        out.append("adastra_age_%s_all = {" % age)
        for t in TECHS[age]:
            out.append("\thas_technology = %s" % t["key"])
        out.append("}\n")
    for age, _flag, _cost, vflag in AGES:
        if not vflag:
            continue
        out.append("adastra_vanilla_open_%s = {" % age)
        out.append("\tOR = {")
        out.append("\t\thas_country_flag = adastra_completed")
        # Paquet offert par l'evenement d'age : l'Age spatial livre les seize
        # technos de vaisseau du jeu de base des l'arrivee, sinon aucun de nos
        # vaisseaux sous-luminiques ne peut etre construit - leurs composants
        # n'existent pas encore. give_technology respecte le potential, donc le
        # drapeau doit ouvrir la porte avant l'octroi. Voir adastra.49.
        out.append("\t\thas_country_flag = adastra_vanilla_gift_%s" % age)
        out.append("\t\tAND = {")
        out.append("\t\t\thas_country_flag = %s" % vflag)
        out.append("\t\t\tadastra_age_%s_done = yes" % age)
        out.append("\t\t}")
        out.append("\t}")
        out.append("}\n")
    # --- ressources : la techno OU un age de depart assez tardif -----------
    out.append("")
    out.append("# --- Ressources -------------------------------------------------------")
    out.append("# Une ressource n'existe pas avant l'invention qui la produit.")
    out.append("#")
    out.append("# La condition est la TECHNOLOGIE seule. C'est suffisant depuis que les ages")
    out.append("# deja traverses offrent leurs technologies au demarrage (adastra.2 appelle")
    out.append("# adastra_grant_age_<age> pour chaque age anterieur) : un empire qui commence")
    out.append("# a l'Age de l'atome connait deja le Reseau electrique, il ne l'a pas")
    out.append("# recherche mais il l'a. Un empire qui commence a l'Age de la machine, lui,")
    out.append("# doit encore l'inventer - c'est justement l'age ou il l'invente.")
    out.append("")
    for res, (tech, _age) in RESOURCE_TECH.items():
        out.append("adastra_has_%s = {" % res)
        out.append("\tOR = {")
        out.append("\t\thas_country_flag = adastra_completed")
        out.append("\t\thas_technology = %s" % tech)
        out.append("\t}")
        out.append("}\n")
    return "\n".join(out)



def tri_par_dependance(techs):
    """Ordonne les technos du jeu de base pour qu'un prerequis precede toujours
    celui qui l'exige. give_technology refuse sinon - voir VANILLA_PREREQ."""
    reste, sortie, vus = list(techs), [], set()
    while reste:
        avance = False
        for t in list(reste):
            besoins = [b for b in VANILLA_PREREQ.get(t, []) if b in techs]
            if all(b in vus for b in besoins):
                sortie.append(t)
                vus.add(t)
                reste.remove(t)
                avance = True
        if not avance:            # cycle : on rend l'ordre alphabetique
            sortie.extend(reste)
            break
    return sortie


def gen_grants():
    """Effets scriptes : offrir les technologies d'un age deja traverse.

    Un empire qui commence a l'Age de la machine n'a pas invente le feu la
    veille : les ages precedents sont derriere lui, leurs technologies sont
    acquises. Sans ca, l'arbre repart de zero au demarrage tardif, les verrous
    d'age du vanilla restent fermes et les ressources avancees n'existent pas.

    L'age de DEPART lui-meme n'est jamais offert : c'est celui qu'on joue.
    """
    out = ["# Ad Astra 1.2 - technologies des ages deja traverses.",
           "# GENERE PAR tools/gen_age_techs.py - NE PAS EDITER A LA MAIN.",
           "#",
           "# Appeles par adastra.2 pour chaque age anterieur a l'age de depart.",
           "# message = no : on n'inonde pas le joueur de dix notifications par age.",
           ""]
    for age, _flag, _cost, _v in AGES:
        out.append("adastra_grant_age_%s = {" % age)
        # 1.5 : dans l'ordre de l'arbre (rang, puis declaration), pour qu'un
        # prerequis soit toujours donne avant la techno qui l'exige.
        rangs = vagues(TECHS[age])
        for t in sorted(TECHS[age], key=lambda t: rangs[t["key"]]):
            out.append("\tgive_technology = { tech = %s message = no }" % t["key"])
        van = tri_par_dependance(
            sorted(k for k, (a, _g) in VANILLA_AGE_MAP.items() if a == age))
        if van:
            out.append("\t# Technos du jeu de base rattachees a cet age.")
            for k in van:
                out.append("\tgive_technology = { tech = %s message = no }" % k)
        out.append("}\n")
    # 1.4 (18/08) : a l'ENTREE dans un age, on pousse ses cinq technologies de
    # premiere vague dans le vivier de recherche. Constat du test B : au jour 1
    # d'un depart Atomique, le vivier de physique reste vide pendant des mois
    # - le moteur ne retire de nouvelles options qu'au compte-gouttes - et les
    # seules technos visibles sont les deux exceptions d'economie du jeu de base
    # (Ecosimulation, Fracturation geothermique). add_research_option force la
    # main : appele par adastra.4x, une fois, quand le drapeau de l'age est pose.
    out.append("# --- entree dans un age : premier rang de l'arbre pousse dans le vivier ---")
    for age, _flag, _cost, _v in AGES:
        vg = vagues(TECHS[age])
        out.append("adastra_offre_age_%s = {" % age)
        for t in TECHS[age]:
            if vg[t["key"]] == 1:
                out.append("\tadd_research_option = %s" % t["key"])
        out.append("}\n")
    return "\n".join(out)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  ecrit : %s (%d octets)" % (os.path.relpath(path, ROOT), len(content.encode("utf-8"))))


def main():
    prereqs = prereq_map()
    total = sum(len(TECHS[a]) for a, _f, _c, _v in AGES)
    print("Ad Astra 1.2 - generation de %d technologies d'age" % total)
    write(os.path.join(ROOT, "common", "technology", "adastra_age_techs.txt"),
          gen_techs(prereqs))
    write(os.path.join(ROOT, "common", "scripted_triggers", "zz_adastra_age_gates.txt"),
          gen_gates())
    write(os.path.join(ROOT, "common", "scripted_triggers", "zz_adastra_progression.txt"),
          gen_progression())
    write(os.path.join(ROOT, "common", "scripted_effects", "zz_adastra_progression.txt"),
          gen_progression_effet())
    write(os.path.join(ROOT, "common", "scripted_effects", "zz_adastra_age_grants.txt"),
          gen_grants())
    write(os.path.join(ROOT, "localisation", "french", "adastra_ages_l_french.yml"),
          gen_loc("french"))
    write(os.path.join(ROOT, "localisation", "english", "adastra_ages_l_english.yml"),
          gen_loc("english"))
    print("OK")


if __name__ == "__main__":
    main()
