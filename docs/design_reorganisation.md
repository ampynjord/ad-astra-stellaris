# Réorganiser Ad Astra: Origins

*17/08/2026. Ce que l'analyse de* Before the Stars *et les dix idées retenues
impliquent pour la structure du mod, pas seulement pour son contenu.*

---

## Le défaut de structure, en une phrase

**Neuf âges se jouent de la même façon, et le dixième contient tout le jeu.**

Regarde ce que le joueur fait, âge par âge. De la pierre à l'atome : il choisit
une approche, il lance une campagne d'exploitation de temps en temps, il
regarde une barre monter, il coche vingt-cinq technologies. Ces neuf âges ne
diffèrent que par **des nombres** — une pénalité de recherche, un coût de
technologie, des noms d'inventions. C'est la même partie jouée dix fois avec
des curseurs différents.

Puis arrive l'Âge spatial, et il porte à lui seul : vingt-cinq technologies
d'époque, seize fondatrices du jeu de base, quatre programmes, la prospection,
le chantier orbital, la flotte, la colonisation, et la percée.

La situation le dit noir sur blanc. Les neuf premiers âges occupent 0 → 86 de
la barre. Le dernier occupe 86 → 100, **plus trois étapes supplémentaires**
jusqu'à 130. Un dixième de la progression porte un tiers des étapes.

Ce n'est pas un problème d'équilibrage. C'est que **les âges n'ont pas de
verbe**.

---

## La proposition : trois actes, dix âges

On garde les dix âges — ils sont bons, ils sont datés, ils portent 250
technologies. On les regroupe en **trois actes**, et chaque acte allume une
mécanique qui ne s'éteint plus.

| Acte | Âges | Verbe | Ce qui s'allume |
|---|---|---|---|
| **I — Le sol** | Pierre → Fer | **bâtir** | les campagnes, la chaîne des capitales, l'économie qui se crée invention par invention |
| **II — Le monde** | Médiéval → Industriel | **unifier et payer** | les nations rivales, les grands travaux, le prix industriel |
| **III — Le ciel** | Machine → Spatial | **regarder, lancer, atteindre** | les télescopes, les Premiers pas, l'échelle de propulsion, les programmes |

Trois textures au lieu d'une texture à dix réglages. Et surtout : **chaque acte
donne au joueur une nouvelle question**, pas seulement des nombres plus grands.

### Acte I — Le sol *(Pierre, Bronze, Fer)*

C'est ce que le mod fait déjà le mieux, on n'y touche presque pas. Une
civilisation qui apprend à ne pas mourir. Les quatre campagnes d'exploitation
sont la mécanique centrale, la chaîne des capitales avance, et l'économie
s'ouvre ressource par ressource — les alliages avec le bronze, et rien avant.

**Le seul ajout** : la première fouille possible n'existe pas encore, mais elle
regardera *ici*. C'est ce qu'on déterrera à l'acte II.

### Acte II — Le monde *(Médiéval, Renaissance, Vapeur, Industriel)*

Le monde cesse d'être un décor. Deux mécaniques s'ouvrent et ne se referment
plus :

**Les nations rivales** (1.4). Ta planète n'est pas un peuple. Des nations avec
leur part de population, leurs exigences, leur chef. L'unification devient
quelque chose qu'on obtient, et la règle qui en découle est la colonne
vertébrale de tout l'acte : **un monde divisé ne va pas aux étoiles.**

**Le prix industriel** (à partir de la Vapeur). La production abîme le monde
qui la porte. Nier, corriger ou transformer — et ce choix s'inscrit dans
l'Héritage.

C'est l'acte qui manque aujourd'hui. Entre le Fer et la Machine, il y a quatre
âges où le joueur n'a rien à décider. **Ces quatre âges sont le vrai chantier
de la 1.4**, plus que la taille de la planète.

### Acte III — Le ciel *(Machine, Atomique, Spatial)*

C'est ici que la réorganisation change le plus de choses. Aujourd'hui, tout le
programme spatial est empilé sur l'Âge spatial. **On l'étale sur trois âges**,
et le ciel se remplit progressivement au lieu de s'ouvrir d'un coup.

| Âge | Ce qu'on peut faire | Poussée |
|---|---|---|
| **Machine** | observatoire optique, radiotélescope, première fusée-sonde *(elle peut exploser)* | poudre et étages |
| **Atomique** | satellites visibles en orbite, vol habité, station orbitale basse, sonde profonde vers un système voisin | propulsion nucléaire |
| **Spatial** | le premier corps, le vaisseau scientifique, le chantier orbital, la flotte, la percée | ionique, puis fusion |

**Et l'échelle de propulsion remplace les seize technologies fondatrices comme
gardien.** Aujourd'hui, chaque programme attend sa fondatrice, et le joueur lit
une liste de seize noms. Demain, il lit une seule chose : *jusqu'où ma poussée
me porte-t-elle ?* Les seize fondatrices restent à chercher — elles ne
disparaissent pas — mais elles cessent d'être la grammaire du programme
spatial. Elles redeviennent ce qu'elles sont : les technologies dont un empire
spatial a besoin.

---

## Ce que ça règle

**Les quatre âges morts du milieu.** Médiéval, Renaissance, Vapeur, Industriel
cessent d'être un tunnel entre le Fer et la Machine.

**L'Âge spatial obèse.** Il perd les télescopes, les satellites, le vol habité,
la station et la sonde, qui remontent d'un ou deux âges. Il garde ce qui est
vraiment son sujet : quitter la planète.

**Le seul vrai écart avec** Before the Stars. Le joueur a des objets en orbite
dès l'Âge de la machine, et une carte à regarder pendant tout l'acte III.

**Les trois étapes supplémentaires de la situation.** Aujourd'hui la barre va à
130 avec `program_explore`, `program_orbital`, `program_hyperdrive` collées
après l'Âge spatial. Si les programmes s'étalent, ces étapes deviennent
inutiles : la barre s'arrête à 100 et la percée est un événement, pas une
quatrième étape. C'est plus lisible et ça retire trois blocs de code.

---

## Ce que ça coûte, honnêtement

**Douze technologies changent d'âge.** Les télescopes, les satellites, le vol
habité migrent de l'Âge spatial vers Machine et Atomique. Le contrôle de bornes
historiques va refuser certaines de ces migrations — *The Artificial Satellite*
est daté 1957, il ne peut pas descendre à l'Âge de la machine (1900–1945) sans
mentir sur la date. **La contrainte historique gagne, toujours.** Ce qui
descend, ce sont les technologies dont la date le permet ; ce qui ne le permet
pas reste où il est, et c'est la *décision* qui descend, pas la technologie.

**Les vagues sont à recalculer.** Cinq par cinq et dérivées de la date : si des
technologies changent d'âge, les vagues des deux âges concernés bougent. C'est
`gen_age_techs.py` qui le refait, pas toi.

**Le verrou de situation compte 266 entrées.** Toute migration le modifie.
`gen_situation_progress.py` le régénère, et `verify_1_2.py` refuse le résultat
s'il ne colle pas.

**Ce n'est pas une version, c'est deux.** L'acte III est une refonte du
gardiennage et une addition de contenu — c'est de la 1.4. L'acte II est le gros
morceau — nations rivales et prix industriel — et c'est probablement 1.5. Les
annoncer ensemble serait la même erreur que la 1.2.1 : un chantier qui déborde
et qui n'est jamais publié.

---

## Ce que je ne réorganiserais pas

**Les dix âges.** Ils sont la promesse du mod, ils sont datés, ils marchent. On
les regroupe, on ne les fusionne pas.

**Les 250 technologies et les vagues.** C'est le dos technologique de la 1.3,
il vient d'être posé et il tient. On y touche pour douze migrations, pas plus.

**L'économie par invention.** C'est la meilleure décision de conception du mod
et la faiblesse centrale du concurrent. On n'y touche pas du tout.

**Les trois approches et les quatre campagnes.** Elles sont l'acte I, elles y
sont bien.

---

## Et l'organisation des sources

Question différente, réponse courte : **pas maintenant.**

Le plan prévoit d'extraire un mod-bibliothèque `Ad Astra: Core` pour partager
les Premiers pas, les Télescopes et les Sondes entre Origins et Frontier.
Extraire Core aujourd'hui coûte une dépendance supplémentaire à installer, une
page Workshop de plus à tenir, et un risque de version croisée — **pour zéro
bénéfice joueur tant que Frontier n'existe pas.**

Ce qui vaut la peine tout de suite, et qui ne coûte presque rien : **ranger les
sources comme si l'extraction avait déjà eu lieu.** Un dossier par futur pilier
à l'intérieur du même mod, des préfixes de fichiers cohérents, aucun appel
croisé entre dossiers autrement que par les déclencheurs scriptés partagés. Le
jour où Frontier existe, l'extraction est un `git mv` et non une réécriture.

C'est la même logique que la CI qu'on vient de poser : on ne construit pas
l'usine avant d'avoir le produit, mais on ne se met pas dans une position d'où
on ne pourra pas la construire.

---

## Résumé en trois lignes

1. Les âges n'ont pas de verbe : neuf se jouent pareil, le dixième porte tout.
2. Trois actes — bâtir, unifier et payer, regarder et atteindre — chacun
   allumant une mécanique permanente.
3. La 1.4 fait l'acte III (le ciel se remplit tôt), la 1.5 fait l'acte II (les
   nations et le prix industriel). Pas les deux à la fois.
