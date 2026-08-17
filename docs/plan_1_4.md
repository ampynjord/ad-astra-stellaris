# Ad Astra 1.4 — plan de version

*Un seul chantier : l'acte III — le ciel se remplit tôt.*

*L'éclatement en collection a été préparé le 17/08 puis reporté. Tout reste
dans Origins.*

---

## Ce que 1.4 est, en une phrase

**Le ciel cesse d'attendre l'Âge spatial.**

L'acte II — nations rivales, prix industriel — n'est **pas** dans cette
version. Il est la 1.5. Faire les deux à la fois, c'est refaire la 1.2.1 : un
chantier qui déborde et qui ne sort jamais.

---

## L'architecture — décision du 17/08 : **un seul mod**

La collection a été préparée — descripteurs, dépendances, registre, CI à trois
mods — puis **reportée**. Tout reste dans **Ad Astra: Origins**.

C'était la bonne décision, et c'est celle que je recommandais avant de la
construire. Éclater en trois pages Workshop coûte trois versions à garder
alignées, trois descriptions à tenir, un joueur qui peut installer Origins sans
Core, et une dépendance déclarée vers un mod qui n'existe pas encore. Tout ça
avant même d'avoir écrit une ligne de contenu pour Core ou Frontier.

**Ce qu'on garde du travail préparatoire**, et qui vaut d'être gardé :

- **Le préfixe `core_`** marque ce qui est extractible. Un fichier `core_` a le
  droit d'être lu par n'importe quoi ; il n'a le droit de dépendre de rien
  d'`adastra_`. Le jour où Core naîtra, ces fichiers déménagent par un `git mv`,
  sans une ligne à réécrire.
- **L'API des âges** — `core_age_atteint`, `core_est_confine`, `core_a_emerge`.
  Personne ne lit plus `has_country_flag = adastra_reached_*` directement. Ça
  vaut même sans collection : le jour où la représentation change, un seul
  fichier bouge.
- **L'échelle de propulsion**, cinq rangs, nouvelle grammaire du programme
  spatial.
- **Le registre des surcharges vanilla**, dans un fichier unique. Il n'existait
  nulle part, et c'est la première cause de conflit entre mods.
- **Le registre `workshop/mods.json`** garde sa forme de liste avec une seule
  entrée. Le jour de l'éclatement, c'est une entrée de plus et rien d'autre.

Ce qui est abandonné pour l'instant : les dossiers `ad_astra_core/` et
`ad_astra_frontier/`, leurs `.mod`, et la dépendance déclarée dans le
descripteur d'Origins — **celle-là devait partir**, une dépendance vers un mod
absent est signalée par le launcher et fait fuir des joueurs.

Frontier n'est pas annulé. Il est simplement remis à sa place : après la 1.4,
quand il aura du contenu à lui.

## Périmètre de la 1.4

### La bibliothèque intérieure — préfixe `core_`

- **L'API des âges** : `core_age_atteint = { age = X }`, `core_est_confine`,
  `core_a_emerge`, `core_poussee_au_moins = { rang = X }`.
- **L'échelle de propulsion**, cinq rangs : *poudre et étages*, *nucléaire*,
  *ionique*, *fusion*, *hyperpropulsion*. Chaque rang est une technologie et
  une portée. La 1.3 gardait chaque programme derrière sa propre fondatrice —
  quatre gardiens sans rapport et seize noms à lire. Le joueur ne lit plus
  qu'une question : *jusqu'où ma poussée me porte-t-elle ?*
- **Premiers pas** : fusée-sonde, satellite, vol habité, station orbitale
  basse, premier corps. Décisions, objets visibles en orbite, modificateurs,
  et l'**échec au lancement** dont la probabilité décroît avec les technologies
  du rang.
- **Télescopes** : observatoire optique, radiotélescope, télescope spatial.
- **Sondes profondes** : décision de lancement, choix du système cible, trajet
  calculé sur la distance réelle, système révélé mais non prospecté à
  l'arrivée. Le vaisseau scientifique garde son métier.
- **Le registre des surcharges vanilla**.

### L'origine — préfixe `adastra_`

- **Les trois actes.** Les dix âges restent, regroupés ; chaque acte allume une
  mécanique permanente.
- **L'acte III étalé sur trois âges.** Machine : observatoire, radiotélescope,
  première fusée. Atomique : satellites, vol habité, station, sonde profonde.
  Spatial : le premier corps, le vaisseau scientifique, le chantier, la flotte,
  la percée.
- **Les seize fondatrices restent à chercher** — elles ne disparaissent pas.
  Elles cessent d'être la grammaire du programme et redeviennent ce qu'elles
  sont : les technologies dont un empire spatial a besoin.
- **La situation s'arrête à 100.** Les trois étapes `program_explore`,
  `program_orbital`, `program_hyperdrive` disparaissent : les programmes sont
  dans les âges, la percée est un événement. Trois blocs de code en moins.
- **Migrations de technologies** : celles dont la date le permet descendent
  vers Machine et Atomique. **Les autres ne bougent pas** — la contrainte
  historique gagne, et c'est la décision qui descend, pas la technologie.
- Loc FR/EN à parité, comme toujours.

### Reporté

- **La terraformation par étapes**, les avant-postes et bio-dômes, Observation
  & Contact : c'était le périmètre de Frontier. Ça attend que Frontier existe.

## Ce qui bouge dans les fichiers

Tout reste sous `ad_astra/`. Ce qui change, c'est le rangement à l'intérieur.

| Fichier | Ce qui lui arrive |
|---|---|
| `scripted_triggers/core_00_api_ages.txt` | **nouveau** — l'interface des âges |
| `scripted_triggers/core_01_poussee.txt` | **nouveau** — l'échelle de propulsion |
| `scripted_triggers/core_99_registre_surcharges.txt` | **nouveau** — le registre des surcharges vanilla |
| `scripted_effects/core_00_conventions.txt` | **nouveau** — effets partagés |
| `scripted_triggers/zz_adastra_scripted_triggers.txt` | les cinq portes de jeu de la 1.3 se réécrivent en termes de poussée |
| `decisions/adastra_decisions.txt` | les quatre programmes changent de gardien ; les lancements, satellites et sondes s'ajoutent en `core_` |
| `situations/zzz_adastra_situations.txt` | les trois étapes de programme disparaissent, la barre s'arrête à 100 |
| `technology/adastra_age_techs.txt` | régénéré — migrations et nouvelles technologies de propulsion |
| `tools/age_techs_data.py` | source de vérité des 250, on y touche pour les migrations |

**Convention de préfixe**, à tenir à partir de maintenant : `core_` pour ce qui
serait extractible dans une bibliothèque, `adastra_` pour ce qui appartient à
l'origine pré-PRL. Un fichier `core_` n'a le droit de dépendre d'aucun fichier
`adastra_`. Les clés de localisation suivent la même règle.

C'est la seule discipline à tenir, et elle rend l'éclatement futur gratuit.

---

## Publication

**Un seul objet Workshop**, `3781408257`, celui qu'ont déjà 954 abonnés. Ils
reçoivent la 1.4 comme une mise à jour normale. Pas de nouvelle page, pas de
collection Steam, rien à recréer.

La machinerie qui gérait trois mods reste en place et ne coûte rien : le
registre a une seule entrée, `premiere_publication.py` attend son heure. Le
jour où Frontier existera, c'est une entrée de plus dans un fichier JSON.

## Ordre de travail

1. **L'API des âges et l'échelle de propulsion.** Rien de visible, mais tout le
   reste en dépend. Fait — les fichiers sont posés.
2. **Origins : l'acte III.** Migrations, gardiennage par la poussée, situation
   ramenée à 100.
3. **Premiers pas** : satellites, station, échec au lancement. C'est là que se
   comble le seul vrai écart de sensation avec *Before the Stars*.
4. **Le premier corps**, une fois tranchée en jeu la question de l'avant-poste
   sur un corps stérile — habitat exclu, c'est Utopia.
5. **Télescopes et sondes profondes.**
6. **Les images d'événement**, au fil de l'eau.

## Ce qui n'est pas dans 1.4

- Les nations rivales et le prix industriel → **1.5**, l'acte II.
- Le monde qui grandit case par case → **1.5** aussi. Ces deux-là vont
  ensemble : une planète qui s'agrandit sans nations à y loger est un décor.
- La terraformation, les avant-postes, Observation & Contact → **Frontier**,
  quand il existera.
- Fortune, Warfare, Gestalt → plus tard, un pilier par cycle.
- The SkyArk, Interstellar → en veille, et elles y restent.
