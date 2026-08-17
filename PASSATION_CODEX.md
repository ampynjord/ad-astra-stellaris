# Ad Astra — passation vers un nouvel agent (Codex)

*Rédigé le 18/08/2026 en fin de session. Tout ce qu'un agent doit savoir pour
reprendre le mod là où on l'a laissé, sans relire la conversation.*

---

## 1. Ce qu'est le projet

**Ad Astra** : mod Stellaris 4.4 (origine pré-PRL). Le joueur commence
confiné sur sa planète natale, choisit un âge de départ parmi dix (Pierre →
Spatial), traverse les âges en recherchant 25 technologies d'époque par âge
(250 en tout), puis mène un programme spatial en trois étapes jusqu'à
l'Hyperpropulsion (émergence). Publié sur le Steam Workshop (id `3781408257`,
version publiée **1.3.0**, ~1 000 abonnés) et GitHub
(`ampynjord/ad-astra-stellaris`). Version en développement : **1.4.0-dev**.

Auteur : ampynjord (Gwenvaël). Langue de travail : français. Style des
commentaires dans le code : français sans accents, datés, qui expliquent le
*pourquoi* — garder cette convention.

## 2. Où sont les fichiers (machine de l'auteur, Windows)

| Chemin | Rôle |
|---|---|
| `C:\Users\Public\AdAstra\` | Kit de travail : scripts `.bat`, `maj_1_4.zip` (dernier build), docs, `retours_communaute.md`, `PROTOCOLE_TEST_1_4.md`, ce fichier |
| `C:\Users\Public\AdAstra\dev\ad_astra\` | **Le mod réellement chargé par le launcher** (playset « Ad Astra Local », via `Documents\Paradox Interactive\Stellaris\mod\ad_astra_dev.mod`). C'est ici qu'on déploie pour tester |
| `C:\Users\Public\AdAstra\repo\` | Clone git du dépôt GitHub (README, CHANGELOG, tools, workshop) |
| `C:\Users\Public\AdAstra\_to_delete\` | Poubelle (fichiers temporaires que le pont ne peut pas supprimer) |
| `Documents\Paradox Interactive\Stellaris\logs\error.log` | **La source de vérité pour déboguer** — la relire après chaque partie |
| `Documents\Paradox Interactive\Stellaris\save games\` | Saves ; un `.sav` est un zip contenant `gamestate` (texte) — grep dedans pour flags, techs, budget |
| `Steam\steamapps\common\Stellaris\` | Vanilla 4.4.6 — chercher ici la syntaxe et les noms valides (modificateurs, triggers) |
| `Steam\steamapps\workshop\content\281990\3781408257\` | Copie Workshop de la 1.3.0 publiée |

Le launcher affiche la version lue dans `dev\ad_astra\descriptor.mod`
(`1.4.0-dev`). `poser_1_4_dev.bat` ne met PAS à jour ce dossier ; utiliser
`sync_dev_local.bat` (extrait `maj_1_4.zip` dans `dev\ad_astra`) ou copier
directement.

## 3. Structure du mod et générateurs

Le mod est en grande partie **généré**. Ne jamais éditer à la main un fichier
dont l'en-tête dit « GENERE PAR tools/… » : modifier le générateur ou sa
source de données, puis régénérer.

| Source de vérité | Générateur | Produit |
|---|---|---|
| `tools/age_techs_data.py` (250 techs, dates, bonus, bâtiments débloqués) | `tools/gen_age_techs.py` | `common/technology/adastra_age_techs.txt`, `scripted_triggers/zz_adastra_age_gates.txt`, `scripted_effects/zz_adastra_vagues.txt`, `scripted_effects/zz_adastra_age_grants.txt`, `localisation/*/adastra_ages_l_*.yml` |
| idem | `tools/gen_situation_progress.py` | bloc `monthly_progress` de `common/situations/zzz_adastra_situations.txt` + clés `adastra_manque_*` dans `adastra_l_*.yml` |
| `tools/age_buildings_data.py` | `tools/gen_age_buildings.py` | `common/buildings/adastra_age_buildings.txt` + loc |
| `tools/vanilla_age_map.py`, `vanilla_zone_age_map.py`, `vanilla_district_age_map.py`, `vanilla_building_age_map.py` | `gen_zone_age_overrides.py`, `gen_district_age_overrides.py`, `gen_building_age_overrides.py`, `gen_tier1_overrides.py`, `apply_vanilla_age_map.py` | `common/zones/zzz_adastra_zone_ages.txt`, `common/districts/zzz_adastra_district_ages.txt`, `common/buildings/zzz_adastra_building_ages.txt`, `common/technology/zzz_adastra_tier1_overrides.txt`, `zzz_adastra_tech_overrides.txt` |

Fichiers écrits à la main (les plus importants) : `events/adastra_events.txt`
(cœur : `adastra.1` choix d'âge, `adastra.2` initialisation, `adastra.40-49`
entrée d'âge, `adastra.80-89` programme spatial, `adastra.130` vivier),
`events/core_premiers_pas_events.txt`, `common/decisions/adastra_decisions.txt`,
`common/static_modifiers/adastra_modifiers.txt`,
`common/scripted_triggers/zz_adastra_scripted_triggers.txt`,
`common/script_values/adastra_script_values.txt`,
`common/defines/zz_adastra_defines.txt`, `localisation/*/adastra_l_*.yml`.

### Vérification et build (à faire après CHAQUE modification)

```
python3 tools/verify_1_2.py          # 0 erreur attendu
python3 tools/verify_release.py      # (dans le dossier de build : mod + tools + README/CHANGELOG)
python3 tools/ci_release.py --sortie build
```
`verify_release.py` a besoin de `README.md` et `CHANGELOG.md` à la racine du
dossier de build (ils viennent de `repo/`). Il refuse les noms de bâtiments
français dans la loc anglaise — le générateur traduit maintenant via
`BATIMENTS_EN`.

## 4. Mécaniques clés (comment ça marche vraiment)

- **Âges** : `adastra_choice_<age>` (choix), `adastra_reached_<age>` (atteint),
  `adastra_unlock_<age>` (verrous vanilla). `adastra.2` pose les `reached` de
  tous les âges antérieurs et appelle `adastra_grant_age_<age>` (25 techs +
  vanilla rattachées) **avant** le bloc `capital_scope`.
- **Vagues** : 25 techs par âge, 5 vagues à 0/20/40/60/80 % de la tranche de
  la situation ; drapeaux globaux `adastra_vague_2..5` recalculés chaque mois
  (`adastra.90` → `adastra_maj_vagues`). Pendant l'octroi de `adastra.2`, les
  4 vagues sont forcées puis recalculées.
- **give_technology / add_research_option** exigent que la tech ET ses
  prérequis soient valides ; les prérequis sont les piliers de l'âge
  précédent. **Ne jamais remettre `NOT adastra_reached_<suivant>` dans le
  potential des techs** — c'était le bug qui cassait tout (215 refus, boucle
  infinie au Bronze en 1.3.0). L'exclusion du tirage passe par
  `weight_modifier` (facteur 0).
- **Verrou de passage d'âge** : la barre de la situation se fige à 1 point de
  la fin tant qu'une des 25 techs manque (un modificateur `mult = 0.001` par
  tech, généré). Les 3 étapes du programme spatial (100→110→120→130)
  fonctionnent pareil depuis 1.4 : lot de fondatrices vanilla + jalon
  (système prospecté / base + station / Hyperpropulsion). Les anciens
  `adastra.71/72` (sauts) sont supprimés.
- **Fondatrices vanilla** (16 techs de l'Âge spatial) : ouvertes par étape via
  `adastra_gameplay_orbite/chantier/vaisseaux/base/colonie/sol`.
- **Le moteur supprime au chargement** toute zone / district / bâtiment dont le
  potential est faux — et avant le choix d'âge, tous les potentials d'âge sont
  faux. `adastra.2` **rebâtit** ensuite ce que l'âge justifie (tableau §6).
- **Ressources** : pas d'énergie avant l'Électricité, pas d'alliages avant le
  Bronze, pas de biens de conso avant la Machine à vapeur
  (`adastra_has_energy/alloys/consumer_goods` = has_technology ; modificateurs
  `adastra_pre_electric`, `adastra_pre_manufacture`).
- **Date** : `common/defines/zz_adastra_defines.txt` → `NGameplay.START_YEAR = 0`
  (l'an 0 comme compteur ; 1 et -1000 marchent aussi), plafonds des curseurs
  milieu/fin/victoire à 2500/5000/5000. Aucun curseur de date de départ
  n'est possible (écran de création non scriptable).
- **Système natal** : sans base stellaire, pas de propriétaire ; drapeau
  `adastra_home_system` + surcharge de
  `is_valid_drone_expansion_destination_system` pour écarter les drones.

## 5. Ce qui a été corrigé le 17-18/08 (tout est dans `dev\ad_astra` et `maj_1_4.zip`)

1. `NOT reached_<suivant>` retiré des potentials → weight_modifier (cause racine
   de « aucune tech », « boucle infinie au Bronze », déficit énergie/CG).
2. Octroi des âges déplacé avant `capital_scope` ; vagues forcées puis recalculées.
3. Zones Archives/Industrie, Fabrique, Laboratoire, 2 générateurs rebâtis selon
   l'âge ; Holothéâtres + Zone commerciale retirés à tous les âges ; Station de
   radiodiffusion pour Atomique/Spatial.
4. `add_research_option` de la 1ʳᵉ vague en différé (`adastra.130`, J+1 et J+30).
5. Programme spatial « comme un âge » (verrous + jalons générés).
6. Bonus des techs arrondis au %, plancher 1 % ; `pop_growth_speed` →
   `logistic_growth_mult`.
7. `core_telescopes.txt` : `planet_sensor_range_add` ; `core_premiers_pas` :
   `max_jumps` au lieu de `max_distance`.
8. `adastra_script_values.txt` réécrit en syntaxe Stellaris (surcoût des relances).
9. Loc `origin_adastra_effects` refusionnée (FR/EN) ; marqueur jaune
   `adastra_tech_marque_base_<age>` sur les 30 techs vanilla rattachées.
10. Grenier/Moulin/Fonderie : set `government` seul (constructibles en ville).
11. Drones miniers écartés du système natal.
12. Defines de date et de durée.

## 6. Capitale de départ attendue par âge

| Départ | Capitale | Défaut | Archives | Industrie | Générateurs |
|---|---|---|---|---|---|
| Pierre→Renaissance | Siège d'époque | — | zone vide dès Bronze | — | — |
| Vapeur | Siège (vapeur) | — | zone + Laboratoire | zone vide | — |
| Industriel | Siège (industriel) | — | zone + Labo | zone + Fabrique | — |
| Machine | Admin. planétaire | — | zone + Labo | zone + Fabrique | 2 |
| Atomique / Spatial | Admin. planétaire | Radio | zone + Labo | zone + Fabrique | 2 |

## 7. Tests restants (protocole complet : `PROTOCOLE_TEST_1_4.md`)

- **B bis** Atomique jour 1 : 3 zones, 2 générateurs, radio, CG/énergie en
  vert ; jour 2 : physique = Fission/Électronique/Transistor.
- **C** Atome jusqu'au bout : vagues, verrou, **durée en années** (donnée
  manquante pour équilibrer les prix).
- **D** Spatial + programme : la barre continue à 100, lots + jalons.
- **E** relance d'un programme : +35 %.
- **F** Pierre → Bronze : une tech du Bronze accordée (bug PoW).
- Un départ Vapeur/Industriel pour la colonne du milieu du tableau.

## 8. Reste à faire

- Réponses Discord : PoW/Hodge-podge (boucle Bronze — cause trouvée, 1.4),
  Argroww (Grenier corrigé, drones corrigés ; demander test sans mods + capture
  pour « Everyone makes their own »).
- `retours_communaute.md` et `CHANGELOG.md` : entrée 1.4 (verify_release lit
  encore « 1.3.0 »).
- Départ Machine sans bâtiment de divertissement (commodités à surveiller).
- Bâtiments de départ liés aux civiques (Résidences de luxe, Centre médical…)
  supprimés au chargement et non remis.
- Équilibrage des prix une fois la durée d'un âge mesurée.
- Publication 1.4 sur le Workshop dès que B/C/D/F passent (la 1.3.0 bloque
  les joueurs au Bronze — sortie rapide justifiée). Procédure : `INSTRUCTIONS.md`.

## 9. Retours communauté en attente

Voir `retours_communaute.md` (journal daté). Points ouverts : Giga
incompatibilité (non reproduite, probablement le même bug que ci-dessus),
« Everyone makes their own » (Argroww, autres mods actifs), rythme des âges.
