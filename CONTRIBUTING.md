# Contribuer à Ad Astra / Contributing to Ad Astra

## 🇫🇷 Comment contribuer

La branche `main` est protégée : **toute contribution passe par une Pull Request.**

1. **Forkez** le dépôt, puis créez une branche depuis `main` :
   `git checkout -b fix/mon-correctif` ou `feature/ma-fonctionnalite`
2. Faites vos modifications dans `ad_astra/`.
3. **Testez en jeu** (Stellaris v4.4.x, nouvelle partie requise) et vérifiez `error.log`.
4. Ouvrez une **Pull Request** vers `main` en décrivant : le problème, la solution, et comment vous avez testé.
5. Une approbation est requise avant la fusion.

### Règles du projet

- **Localisation** : chaque clé doit exister dans `localisation/french/` **et** `localisation/english/`, fichiers en UTF-8 **avec BOM**. Pas de caractères non supportés par la police du jeu (— et • deviennent `-`).
- **Style vanilla** : réutilisez les clés, icônes (`£energy£`…), couleurs (`§Y…§!`) et le vocabulaire du jeu de base.
- **Pas d'override d'événements vanilla** (impossible dans Clausewitz : le premier chargé gagne). Les techs, scripted triggers et focus cards, eux, sont surchargeables.
- **Équilibrage** : expliquez le raisonnement de tout changement de coût/pénalité dans la PR.

### Rapports de bug

Ouvrez une *Issue* avec : version du jeu, liste de mods, étapes de reproduction, et si possible la sauvegarde + `error.log` (`Documents/Paradox Interactive/Stellaris/logs/`).

---

## 🇬🇧 How to contribute

The `main` branch is protected: **all contributions go through Pull Requests.**

1. **Fork** the repository, then branch off `main`:
   `git checkout -b fix/my-fix` or `feature/my-feature`
2. Make your changes inside `ad_astra/`.
3. **Test in-game** (Stellaris v4.4.x, new game required) and check `error.log`.
4. Open a **Pull Request** against `main` describing: the problem, the solution, and how you tested it.
5. One approval is required before merging.

### Project rules

- **Localisation**: every key must exist in both `localisation/french/` **and** `localisation/english/`, files saved as UTF-8 **with BOM**. No characters unsupported by the game font (— and • become `-`).
- **Vanilla style**: reuse base-game keys, icons (`£energy£`…), color codes (`§Y…§!`) and vocabulary.
- **No vanilla event overrides** (impossible in Clausewitz: first loaded wins). Techs, scripted triggers and focus cards are overridable.
- **Balance**: explain the reasoning behind any cost/penalty change in the PR.

### Bug reports

Open an *Issue* with: game version, mod list, reproduction steps, and if possible the save file + `error.log` (`Documents/Paradox Interactive/Stellaris/logs/`).
