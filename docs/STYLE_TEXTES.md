# Le modele de texte Ad Astra (31/08/2026)

Demande d'ampynjord : tous les textes (techs, decisions, evenements,
situation, batiments) suivent UN modele, calque sur le vanilla — l'exact et
le lore, jamais l'un sans l'autre, en FR **et** EN (parite verifiee).

## Le modele par type de contenu

**Technologie**
- `nom` : titre historique sobre (« Maitrise du feu », pas « Tech de feu I »).
- `desc` : 1-3 phrases de lore ; PUIS, en jaune `§Y...§!` :
  - `Debloque le batiment : X.` (champ `unlocks` de `age_techs_data.T`) ;
  - toute decision ou mecanique ouverte (table `GAMEPLAY_ANNOUNCEMENTS`).
- Le moteur affiche seul le bloc `modifier` — ne jamais le paraphraser.
- Tout passe par `tools/age_techs_data.py` + `gen_age_techs.py`, jamais par
  la loc generee.

**Decision**
- `nom` / `desc` = lore (le geste, pas la regle).
- `custom_tooltip` obligatoire pour toute regle que le moteur n'affiche pas,
  au gabarit :
  ```
  Phrase d'action.
  §HCe que X apporte :§!
  £ship_size_science£ effet exact 1
  £ship_size_science£ effet exact 2
  §RContrainte (unique / relancable / cout progressif / condition).§!
  ```
- Le cout et la duree sont affiches par le moteur ; l'infobulle ne les
  repete que s'ils EVOLUENT (ex. « chaque campagne rencherit la suivante de
  30 % »).

**Batiment**
- `desc` : lore ; PUIS `§Y...§!` pour ce que le moteur ne montre pas
  (portee d'observation, chaine d'amelioration et sa technologie).

**Evenement**
- `title` court, `desc` = recit ; chaque option qui a un effet cache porte un
  `custom_tooltip` recapitulatif prefixe `£ship_size_science£`.

**Situation / cartes d'objectifs**
- La description de la situation enumere TOUTES les exigences d'etape avec
  leurs seuils (`§Y225-250§! : ...`).
- Cartes d'objectif : structure fixe `name/desc/fail/hint/lore/success` ;
  `desc` tient en une phrase, `hint` donne le geste exact dans l'interface.

**Action diplomatique**
- Jeu de cles vanilla complet (`_TYPE`, `_TYPE_DESC`, `_OFFER_DESC`,
  `_TITLE`, `_DESC`, `_IMPOSSIBLE_DESC`, `_PROPOSAL_FAILED_*`,
  `_NOTIFICATION`) ; chaque raison d'acceptation IA a sa cle `desc` lisible.

## Les invariants

- FR et EN toujours ensemble ; la parite de cles est un controle de sortie.
- UTF-8 BOM + espace de tete sur chaque ligne de loc.
- Balises : `§H` titre de bloc, `§Y` exact/debloque, `§R` contrainte,
  `£ship_size_science£` puce de liste.
- Jamais deux sources pour le meme texte : ce qui est genere se corrige dans
  `tools/*_data.py`, le reste dans `adastra_l_*.yml`.
