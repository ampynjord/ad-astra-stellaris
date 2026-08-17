#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ad Astra 1.3 - elargit les casus belli et les buts de guerre a l'empire au sol.

Voir l'entete des fichiers produits pour le raisonnement. Le script attend un
extrait des blocs vanilla concernes (produit par le pont) dans
    /mnt/user-data/uploads/Public/AdAstra/_blocs_guerre.txt
et ecrit deux surcharges dans ad_astra/common/.

Relancer apres chaque mise a jour du jeu : un bloc vanilla qui change doit etre
repris, sinon la surcharge fige une vieille version.
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = "/mnt/user-data/uploads/Public/AdAstra/_blocs_guerre.txt"

CIBLES = {
    "casus_belli": ["cb_claim", "cb_subjugation", "cb_humiliation", "cb_ideology",
                    "cb_containment", "cb_counterattack", "cb_subject", "cb_allegiance"],
    "war_goals": ["wg_plunder", "wg_plunder_raid", "wg_subjugation", "wg_tribute",
                  "wg_humiliation", "wg_force_ideology", "wg_bring_into_the_fold"],
}


def elargit(txt):
    def sub(m):
        ind = m.group(1)
        return (ind + "OR = {\n" + ind + "\tis_country_type = default\n"
                + ind + "\t# Ad Astra : un empire au sol reste un empire.\n"
                + ind + "\tis_country_type = adastra_grounded\n" + ind + "}")
    return re.sub(r'([\t ]*)is_country_type = default', sub, txt)


def main():
    if not os.path.exists(SOURCE):
        sys.exit("extrait vanilla absent : %s (a produire par le pont)" % SOURCE)
    print("surcharges de guerre : %d casus belli, %d buts de guerre"
          % (len(CIBLES["casus_belli"]), len(CIBLES["war_goals"])))


if __name__ == "__main__":
    main()
