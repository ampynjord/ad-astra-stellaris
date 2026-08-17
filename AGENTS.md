# AGENTS.md — Ad Astra (mod Stellaris 4.4)

Lis d'abord `PASSATION_CODEX.md` (état complet du projet au 18/08/2026) et
`retours_communaute.md` (journal des retours joueurs).

Règles de travail :
- Français dans les échanges et les commentaires (sans accents dans le code), commentaires datés qui expliquent le pourquoi.
- Ne jamais éditer un fichier « GENERE PAR tools/… » : modifier la source (`tools/*_data.py`, `tools/vanilla_*_map.py`) ou le générateur, puis régénérer.
- Après toute modification : `python3 tools/verify_1_2.py` (0 erreur), puis build (`tools/verify_release.py`, `tools/ci_release.py --sortie build`) et déploiement dans `C:\Users\Public\AdAstra\dev\ad_astra` (dossier lu par le launcher).
- Diagnostiquer avec `Documents\Paradox Interactive\Stellaris\logs\error.log` et les saves (zip → `gamestate`) plutôt qu'en devinant ; vérifier les noms de modificateurs/triggers dans le vanilla (`steamapps\common\Stellaris\common`).
- Interdit : `NOT = { has_country_flag = adastra_reached_<suivant> }` dans le potential d'une technologie (casse give_technology et la recherche) ; syntaxe CK3 (`if/limit`) dans les script_values ; `START_YEAR` hors du bloc `NGameplay`.
- Investiguer puis proposer avant de coder, sauf autorisation explicite ; une fois autorisé, corriger, vérifier, redéployer, et dire précisément quoi tester en jeu.
