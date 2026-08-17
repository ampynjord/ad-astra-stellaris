# Ad Astra — audit des retours communauté

*Chaque retour reçu depuis la publication, et ce qu'on en a fait. Un retour sans ligne ici est un retour perdu.*

**Légende** — ✅ traité · 🔄 en cours · ⏳ en attente (action hors code) · 📋 noté pour plus tard · ❌ écarté (avec raison)

---

## Steam Workshop

| Qui | Retour | Statut | Où |
|---|---|---|---|
| **Sithiya** | Partie « rester pré-PRL pour toujours » : diplomatie extrêmement limitée, on ne peut qu'accepter, jamais proposer | ✅ 1.2 | Cause trouvée : 14 actions diplomatiques vanilla testent `is_country_type = default` en dur. Les trois actions de négociation sont reprises et élargies |
| **Sithiya** | On peut déclarer la guerre sans pouvoir quitter son système | ✅ 1.2 | `diplomatic_wars = yes` : la guerre redevient possible **dans les deux sens**, c'est le risque de la galaxie vivante |
| **Sithiya** | Le programme de flotte fabrique des bio-vaisseaux « en transformant des rochers en vaisseaux vivants » | ✅ 1.2 | Cause : `random_existing_design = corvette` pioche dans les designs de l'empire. Les empires à bio-vaisseaux paient désormais en nourriture au lieu de minerais |
| **Sithiya** | Les réserves de ressources sont effacées à la percée supraluminique | ✅ 1.1 | Instantané des stocks avant `set_country_type`, restitution après |
| **Nobumon** | Des technos modernes proposées au Moyen Âge | ✅ 1.1 | 239 technos de tier 1-2 verrouillées jusqu'à l'Âge spatial |
| **Nobumon** | Les âges passent trop vite | ✅ 1.1 + ✅ 1.2 | Choix de rythme au premier jour (1.1), puis durée par défaut doublée (1.2) |
| **argroww** | Âge du fer : aucune techno propre, rien à faire | ✅ 1.2 | 50 technos d'époque, 5 par âge, sur les 3 domaines |
| **argroww** | A dû désactiver à la main les bâtiments vanilla anachroniques | ✅ 1.2 | 56 bâtiments recalés sur l'âge de leur équivalent d'époque, 12 laissés (gestalt), 1 disponible |
| **argroww** | Un arbre technologique dans l'esprit de Caveman2Cosmos | ✅ 1.2 | C'est exactement la forme retenue : chaînage par domaine entre âges |
| **argroww** | Rallonger les âges (écho de Nobumon) | ✅ 1.2 | Progression mensuelle divisée par deux, tous modificateurs à l'échelle |
| **argroww** | Héritage plus généreux quand on ne bride pas les autres empires | ✅ 1.2 | 4 paliers « audacieux » ×2, si la galaxie est restée vivante |
| **argroww** | Se propose pour écrire des textes (pas de l'équilibrage) | ⏳ | À inviter sur GitHub : descriptions des technos et bâtiments |
| **Drakelord138** | Captures d'écran en anglais sur la page Workshop | ⏳ | Ne peut se faire qu'en jeu |
| **baronjutter** | Captures d'écran en anglais (2ᵉ demande indépendante) | ⏳ | Idem — priorité relevée, trois demandes au total |
| **baronjutter** | Un mode « tous les empires en pré-PRL », âges technologiques aléatoires | ❌ 1.2 | Hors périmètre d'Origins : c'est une refonte de génération de galaxie → noté pour **Frontier** ou **Core** |
| **dkr127054** | Propose de faire la localisation russe | ⏳ | À inviter une fois le dépôt prêt à accueillir des PR de traduction |
| **Nova Starborn** | Compatible Gigastructural Engineering et ACOT ? | ✅ | Réponse technique établie (voir section Compatibilité) |
| **Sithiya** | Sans hyperpropulsion : impossible de fabriquer un colonisateur, donc impossible de peupler un complexe d'habitat pourtant construit | 🔄 1.2 | Cause : sans `HYPER_DRIVE_1`, l'auto-conception ne produit pas de design de colonisateur valide — même échec que pour le vaisseau scientifique, déjà contourné par un design fourni. Design **colonisateur sous-luminique** ajouté, plus sa version PRL pour après l'émergence. **À tester en jeu** |
| **Sithiya** | Aucune désignation de capitale ni de colonie possible en pré-PRL | ✅ 1.2 | Cinq désignations de capitale exigent `is_country_type = default`, dont `col_capital` sous une forme retournée en `NAND`. Comme la seule planète d'un empire confiné est sa capitale, il n'avait accès à **aucune** désignation. Les cinq sont élargies |
| **Sithiya** | La Grande Archive ne se construit pas ; l'essaim de Dyson oui | ✅ 1.2 | Même cause : `potential = { is_country_type = default }` sur `grand_archive_0`. L'essaim de Dyson n'a pas cette garde, d'où la différence. Condition élargie |
| **Sithiya** | Création d'issue GitHub restreinte | ⏳ | Réglage du dépôt, pas du mod : Settings → Features → Issues doit être coché, et la restriction des interactions levée |
| **Sithiya** | Terraformation : marche peut-être en pré-PRL, incertain — système capitale uniquement | 📋 | À instruire : rien dans le mod ne la bloque, mais un système à une seule planète n'offre probablement aucune cible |
| **Sithiya** | Un départ donnant l'armure en métal vivant produit des corvettes ainsi blindées via la décision de flotte, sans jamais dépenser la ressource | 📋 | Exploit mineur reconnu (« kinda cheesy but w/e »). La décision pioche un design existant de l'empire. Corrigeable en imposant un design fourni plutôt qu'un design pioché |
| **Sithiya** | Un événement du Vide a détruit le vaisseau scientifique pré-PRL ; impossible d'en refaire un, ni un vaisseau de construction | ✅ 1.2 | Les programmes livraient un exemplaire **sans jamais donner le plan**. Sans hyperpropulsion, l'auto-conception échoue : un vaisseau perdu l'était pour toute la partie. `create_ship_design` donne désormais les trois plans sous-luminiques (scientifique, construction, colonisateur), reconstructibles au chantier de la base stellaire |
| **Skullzi** | « Been waiting for a mod like this forever » | — | Enthousiasme, rien à traiter |
| **Abusabus** | « Pourquoi pas de machine ni d'esprit ruche ? » | 📋 | Réponse à donner : le confinement suppose un empire régulier (chaîne de capitales, catégories de pops, textes). Un gestalt a besoin de sa propre chaîne de capitales et de ses propres textes — livrer à moitié casserait la partie. Prévu, pas bâclé |
| **Frettchen** | « Est-il possible de changer l'année de départ à zéro ? » | ❌ | Impossible : `START_YEAR` est une constante globale des defines, aucun jeton de réglage n'existe pour l'année de départ dans l'écran de création de partie, et le plafond `VICTORY_YEAR_MAX` mettrait 2200 hors d'atteinte depuis une date antérieure. Le choix de l'âge de départ est la réponse du mod |
| **« Ai mod create »** | Publicité pour un site de génération de mods par IA, postée deux fois (chinois + anglais, avec lien) | ❌ | Spam — signaler et supprimer, ne pas répondre |
| **Nathaniel Herapen the Third** | « I was literally just thinking about playing PreFTL » | — | Enthousiasme, rien à traiter |
| **Dwagons_Fwame / getglad188alt** | Discussion mods civilisation, Katzenartig Imperium, ancien mainteneur de Pre-FTL Players | — | Contexte, pas une demande |

## Reddit — r/Stellaris

| Qui | Retour | Statut | Où |
|---|---|---|---|
| **Lucky13crocket** | Pierre → Spatial en ~30 ans de jeu, plus court que KotG ; « une seule génération entre l'outil de pierre et le vol spatial » | ✅ 1.2 | Durée par défaut doublée |
| **Lucky13crocket** | Bloquer la progression de la situation par des technos, pas seulement par l'unité accumulée | ✅ 1.2 | C'est le rôle des 50 technos : le vanilla d'un âge n'ouvre qu'après ses technos d'époque |
| **Lucky13crocket** | Pouvoir conquérir davantage de sa planète natale : boost de population contre gros malus de stabilité | 📋 post-1.2 | Bonne idée, mécanique distincte de l'arborescence — à traiter séparément |
| *(retour antérieur)* | « Un gameplay de fenêtres qui s'ouvrent, c'est pas terrible » | ✅ | Règle de conception : pas de nouvelle pop-up, tout passe par situation, décisions et technos |

## Tests internes (ampynjord)

| Retour | Statut |
|---|---|
| Unité négative et pénuries immédiates aux premiers âges | ✅ 1.1 — entretien allégé par âge |
| Infobulle de l'origine différente des autres origines | ✅ 1.1.1 — `possible` seul, comme le jeu de base |
| Origine sélectionnable par les empires gestalt | ✅ 1.1.1 — `NOR` sur les deux autorités |
| Mobilisation de ressources trop faible / peu intéressante | ✅ 1.1 — 4 campagnes avec vrais compromis |
| Malus des campagnes trop faibles | ✅ 1.1 — renforcés, et `logistic_growth_mult` corrigé |
| Le bonus de rythme n'a pas l'air appliqué | ✅ 1.1 — vérifié, modificateurs de progression |
| L'étoile est déjà découverte au départ | ✅ intentionnel — documenté dans l'infobulle |
| On peut prendre des traditions pendant les âges — normal ? | ✅ 1.2 — **tranché : verrouillées avant l'émergence.** 33 catégories surchargées, tout se rouvre à la percée |

---

## Compatibilité avec les autres mods

Question posée par **Nova Starborn**, vérifiée sur les fichiers du jeu et la documentation des mods concernés.

- **Gigastructural Engineering & More** — déclare surcharger les mégastructures vanilla et le déclencheur scripté `habitable_structure`. Ad Astra ne touche ni aux mégastructures, ni à ce déclencheur : pas de collision. Ad Astra surcharge `is_regular_empire`, que Gigas ne revendique pas. Les origines ajoutées par Gigas ont leurs propres clés. **Compatible.** Seule réserve : les technos ajoutées par Gigas ne figurent pas dans notre énumération, donc rien ne les empêche d'être proposées pendant le confinement si l'une d'elles est de bas palier et sans prérequis.
- **ACOT / Ancient Cache of Technologies** — ajoute des paliers *au-delà* du tier 5 vanilla (ZPR améliorée, matière noire, Phanon, Stellarite, Omegan) au lieu de modifier les paliers existants. Toutes ses technos sont de fin de partie avec de lourds prérequis : aucun risque de les voir à l'Âge de pierre. **Compatible.**
- **Conséquence de conception** : l'idée d'un verrou global au niveau des paliers technologiques est **écartée**. Les paliers vanilla n'ont pas de bloc `possible` (seulement `previously_unlocked` et `weight_modifier`), et surtout ACOT étend ce fichier — le surcharger casserait ACOT. L'énumération, plus verbeuse, est le choix compatible.
- **Surface de conflit réelle d'Ad Astra** : un seul déclencheur scripté vanilla surchargé, `is_regular_empire`. Tout mod qui le surcharge aussi entrera en conflit ; c'est le point à surveiller en priorité pour les rapports de compatibilité.

---

## Curious — « plus une preuve de concept qu'une bêta » (14/08)

> *« Very cool concept, but it feels more like a proof of concept than a beta. It's extremely bare bones and all you do for a while is micro manage jobs while keeping game speed at Fastest. There's no content until the early space age and it's easy to break your save and have it become unplayable. »*

Trois reproches, à séparer.

- **« Bare bones, rien à faire avant l'âge spatial »** — exact, et c'est le diagnostic exact de la 1.2. La 1.1 livre le cadre sans le contenu : dix âges qui ne changent que des modificateurs. La 1.2 répond point par point (100 technos d'époque, 11 bâtiments, 7 paliers de capitale, contenu vanilla daté par âge). Rien à instruire, c'est déjà en test.
- **« Vitesse maximale en permanence »** — même cause. À noter tout de même : allonger les âges ×2 en 1.2 **aggrave** ce symptôme si le contenu ne suit pas. C'est l'argument le plus fort pour ne pas sortir la 1.2 avant que le rythme de recherche soit mesuré en jeu (bloc 2 du protocole).
- **« Easy to break your save and have it become unplayable »** — **le seul point réellement neuf, et le plus grave.** Aucun détail : ni l'âge, ni le moment, ni le symptôme. Rien d'exploitable en l'état. Demande de précision envoyée. À suivre : si c'est reproductible, ça passe devant tout le reste.

## Paradox — build de test de la 1.2 ? (14/08)

Demande d'accès anticipé. Réponse : non, pas de build public tant qu'une partie complète ne tient pas. Deuxième demande du genre — si elle revient, envisager une branche `beta` sur GitHub plutôt qu'un second élément Workshop.

---

## L'orbite occupee — question de conception ouverte (16/08)

Le **Programme de base stellaire** dure 360 jours. La decision exige une orbite libre au moment ou on la prend, mais rien n'empeche un empire de s'y installer pendant l'annee de travaux. Au terme du programme, le chantier ne peut plus etre pose.

Traitement actuel : evenement **« Le ciel est deja pris »**. Les quatre plans restent acquis, le drapeau de phase 2 n'est pas pose, la decision reste proposable. Rien n'est bati, rien n'est vole.

Ce qui a ete ecarte, et pourquoi : une vraie negociation — payer en influence pour qu'ils liberent l'orbite. **Le moteur n'autorise qu'une base stellaire par systeme.** Toute negociation reussie revient donc a detruire la leur. On peut l'habiller en diplomatie, ca reste un acte de guerre, et un empire pre-PRL qui chasse une puissance spatiale de son orbite par la parole n'est credible dans aucune fiction.

Trois pistes pour l'apres-1.2, aucune tranchee :

1. **Le droit d'amarrage.** On ne construit pas, on loue. L'empire proprietaire nous ouvre sa base : on peut y construire nos vaisseaux contre un tribut mensuel. Colle a la fiction du protectorat deja presente a l'emergence.
2. **Le chantier au sol.** Une variante du programme qui pose un chantier planetaire au lieu d'une base orbitale. Plus lent, plus cher, mais personne ne peut nous le prendre.
3. **Rien.** L'orbite occupee est une vraie perte, et le joueur doit vivre avec jusqu'a ce que la galaxie bouge.

La question est posee aux joueurs dans les deux descriptions Workshop.

---

## cooldude808 — le retour le plus utile depuis la sortie (16/08)

Cinq points, tous justes, et le premier est chiffrable. Je l'ai chiffré.

### 1. « You basically become a one planet fallen empire »

> *« buffs stack from technologies so much that you basically become a one planet
> fallen empire. make debuffs bigger or buffs smaller so that when you finish
> with the whole pre ftl thing you will be where the game actually starts »*

**Il a raison, et c'est pire que ce qu'il décrit.** Cumul des modificateurs des
cent technologies d'époque, calculé sur `tools/age_techs_data.py` :

| Modificateur | Cumul à l'émergence |
|---|---|
| Production des emplois, toutes ressources | **+635 %** |
| Vitesse de recherche | +185 % |
| Nourriture | +134 % |
| Croissance des pops | +129 % |
| Énergie | +105 % |
| Unité | +96 % |
| Stabilité | **+71 points** |
| Bonheur | +49 % |

Par âge, la production des emplois monte de +23 % à l'Âge de pierre à +71 % au
seul Âge spatial, sans jamais redescendre. Les pénalités d'étape, elles,
s'effacent en avançant et disparaissent à l'émergence. Un empire qui perce
sort donc avec **six fois la production d'un empire neuf**, plus 71 points de
stabilité sur une échelle qui plafonne à 100.

Personne n'avait additionné la colonne. C'est le genre d'erreur qu'on ne voit
pas en jouant vingt ans et qui saute aux yeux d'un joueur qui va au bout.

**Trois façons de corriger, à trancher :**

1. **Diviser les valeurs.** Simple, immédiat, une passe sur la table de données.
   Un facteur 4 ramène à +160 %, un facteur 6 à +106 %. Mais la montée perd de
   son relief : c'est justement ces bonus qui font sentir qu'on progresse.
2. **Faire porter la montée par les étapes de la situation** plutôt que par les
   technologies. Les pénalités d'étape s'effacent déjà toutes seules à
   l'émergence — c'est le bon véhicule pour un effet temporaire. Les technologies
   ne gardent qu'un reliquat permanent, modeste.
3. **Le plus juste sur le fond** : ce que vous avez appris du feu au
   microprocesseur, c'est ce qu'un empire normal sait déjà le premier jour. Les
   bonus d'époque sont l'échelle, pas la récompense — et l'échelle ne monte pas
   avec vous. Ils expireraient à l'émergence, et l'Héritage de l'Ascension
   resterait la seule récompense permanente. C'est la lecture que je défendrais.

### 2. « Too many technologies are free »

> *« makes me breeze though the research tree and makes me wait until the next
> age to gain new research »*

Le verrou d'âge marche dans un seul sens : la barre attend les technologies. Le
cas inverse — les dix technologies finies avant la barre — n'a jamais été
traité, et il produit du temps mort.

**Correctif proposé, et il est élégant** : quand les dix technologies d'un âge
sont trouvées, la barre **accélère**. On a tout appris de cet âge, le temps s'y
comprime. Un modificateur de plus dans `monthly_progress`, symétrique du verrou
qui existe déjà.

### 3. L'Hyperpropulsion interminable

> *« why not make it progress when researching research vessels or smth »*

La dernière recherche est un mur. Piste : la faire progresser avec l'activité
spatiale — prospections, stations bâties, décisions du programme.

### 4. Les ruptures d'immersion

- **Les émissaires.** On peut envoyer un envoyé sans pouvoir quitter
  l'atmosphère. Conséquence de l'ouverture de la diplomatie en 1.2 ; il faudrait
  distinguer ce qui se fait par radio de ce qui demande un vaisseau.
- **Les autres civilisations pré-PRL dans la communauté galactique.** Pas de nous,
  mais visible depuis chez nous.
- **Terraformation et cuirassés à l'Âge spatial.** *Celui-là est un vrai bug, et
  je l'avais vu venir.* Le drapeau `adastra_vanilla_gift_space`, posé le 15/08
  pour débloquer le paquet de seize technologies, ouvre TOUT le vanilla de
  l'âge. Les paliers s'enchaînent ensuite d'eux-mêmes : tier 1, puis 2 après six
  technologies, puis 3. La terraformation est en palier 3. **À corriger en
  1.2.1** — le drapeau doit n'ouvrir que les seize, pas la porte.
- **Les bâtiments verrouillés derrière une exploitation elle-même verrouillée**
  jusqu'à l'Âge spatial, « basically making them useless ». À instruire.

---

## Curious — impossible de prospecter son propre système (16/08)

> *« an AI took the system I was in and met me (using envoy), which made me
> unable to survey the system I was in once I built my first space ship because
> "you can't survey someone else's system". Happened in 2 out of my 5 games. »*

**Bloquant, et fréquent : deux parties sur cinq.** Le Programme d'exploration
livre un vaisseau scientifique dont le seul travail est de prospecter le système
natal. Si un empire l'a revendiqué entre-temps, le jeu de base refuse la
prospection — et le programme spatial n'a plus aucun sens.

C'est le pendant du cas « Le ciel est déjà pris » traité le 16/08 pour la base
stellaire, mais une étape plus tôt et bien plus grave : on peut vivre sans
chantier orbital, on ne peut pas avancer sans prospection.

Pistes, aucune vérifiée :

1. **Prospecter chez soi ne devrait pas dépendre du propriétaire.** Chercher si
   la condition vanilla peut être élargie pour le système natal d'un empire
   confiné, comme on l'a fait pour les désignations et les tailles de vaisseaux.
2. **Se passer de la prospection.** Le programme pourrait révéler le système
   natal directement, la prospection n'étant qu'un moyen. Moins beau, mais
   robuste.
3. **Empêcher la revendication** du système natal d'un empire Ad Astra pendant
   le confinement. Radical, et discutable : c'est un morceau de fiction qu'on
   perdrait.

La deuxième est la plus sûre pour une 1.2.1 ; la première est la bonne si elle
est possible.

---

## Aldran — deux questions après la 1.2 (16/08)

> *« what does PRL mean? »*

**Ce n'est pas une question, c'est un défaut.** PRL est l'abréviation française
de « Plus Rapide que la Lumière » — FTL. Elle est parfaitement transparente pour
un francophone et parfaitement opaque pour tout le monde d'autre.

Où elle traîne, vérifié le 16/08 :

| Où | État |
|---|---|
| `localisation/english/*.yml` | **propre** — 710 clés, aucune occurrence, aucun écart avec le français |
| Titre Workshop | `Ad Astra - Pre-FTL Origin / Origine pre-PRL [BETA]` — bilingue, assumé |
| Vignette | `PRÉ-PRL · PRE-FTL` — bilingue, assumé |
| Description EN | propre, dit « pre-FTL » partout |

Donc le texte en jeu ne fautait pas : Aldran a lu le titre ou la vignette, où
les deux langues se côtoient sans que rien n'explique la seconde. Un lecteur
anglophone y voit un sigle inconnu collé au sien.

**À faire en 1.2.1 :** une ligne dans la description anglaise, au premier
paragraphe, du genre *« PRL is simply FTL in French — the mod ships in both
languages, and the title carries both. »* Coût nul, et ça épargne la question à
tous ceux qui ne la poseront pas.

---

## Aldran — le type de civilisation nomade (16/08)

> *« are you supposed to be able to choose the nomad civilisation type? »*

**Non. C'est un trou dans le filtre de l'origine.**

`possible` ne barre aujourd'hui que les autorités gestaltes (ruche, machine).
Le type de civilisation se choisit ailleurs dans le créateur d'empire, et rien
ne l'empêche de se combiner avec Ad Astra.

**Ce que ça casse, sur pièces.** Les surcharges de tailles de vaisseaux du mod
ont été générées depuis le jeu de base : le `potential_country` vanilla de
`constructor` et de `colonizer` porte `is_nomadic = no` **au premier niveau**,
hors du `OR` que le mod élargit. Un empire nomade n'a donc jamais ces deux
tailles — quoi que fasse notre clause. Conséquence directe :

- **Programme de base stellaire** — livre les plans du Bâtisseur et de l'Arche.
  Deux plans pour des coques qui n'existent pas.
- **Programme de colonisation** — ne peut rien livrer du tout.
- `tech_nomads_mechanized_mining` est de son côté verrouillée sur
  `is_nomadic = yes`, donc l'arbre nomade et l'arbre d'époque se croisent sans
  se parler.

Et sur le fond : un type de civilisation nomade, c'est une capitale mobile et
une flotte pour maison. L'origine dit l'inverse — un monde, et pas d'ailleurs
avant très longtemps. C'est la même raison que pour les gestaltes.

**✅ Corrigé le 16/08, après vérification contre le jeu de base.** Ma prudence
était justifiée mais la réponse est simple : `is_nomadic = no` **est** valide
dans le `possible` d'une origine, et six origines vanilla s'en servent
exactement comme ça — Géante rouge, Aube cosmique, Forgé par le Voile, Porteurs
de fin, Prédateurs évolutifs, Citadelle étoilée. Une ligne, la forme du jeu de
base, aucun risque de rendre l'origine injouable.

**Et une trouvaille au passage : le nomadisme est un DLC.** Les cinq civics qui
le portent — `civic_caravan_masters`, `civic_deep_sleep`, `civic_void_reavers`,
`civic_flight_schools`, `civic_hired_guns` — sont toutes gardées par
`playable = { has_nomads_dlc = yes }`. Aldran le possède donc. Ça ne change pas
le correctif, mais ça explique pourquoi personne d'autre n'a signalé le
problème.

*Commandes passées (conservées pour mémoire) :*

```bash
# Comment une origine vanilla restreint-elle le type de civilisation ?
grep -n "nomad" ~/mnt/common--Stellaris/common/governments/civics/00_origins.txt
grep -rn "civilization_type\|is_nomadic" ~/mnt/common--Stellaris/common/governments/civics/*.txt | head -20
ls ~/mnt/common--Stellaris/common/civilization_types/ 2>/dev/null
```

Après correction, **relancer le créateur d'empire et confirmer qu'Ad Astra est
toujours sélectionnable** — c'est le seul test qui compte.

---

## bandage_shi — une galaxie asymétrique (16/08)

> *« Really promising mod! If this can be applied to more AI empires, it has the
> potential to create a truly asymmetrical galaxy rather than the standard 4X
> experience. »*

**Troisième formulation du même souhait** (baronjutter, Curious, lui) — mais la
première qui ne demande pas une galaxie *entièrement* pré-PRL. Il demande *plus
d'un*. Nuance décisive : ça, c'est à moitié construit.

L'IA peut prendre l'origine depuis la 1.2 (`random_weight = { base = 1 }`, plus
les personnalités sous `adastra_grounded` et les `ai_weight` des décisions). Le
code est livré ; il est simplement si rare que personne ne l'a vu. La question
n'est donc pas « est-ce possible » mais **combien, et qui décide**.

**Vérifié le 16/08 : `remove_technology` n'existe pas.** Zéro occurrence dans
`common/` et `events/` du jeu de base. On ne reprend pas une technologie à un
empire.

Conséquence, nette : **la conversion d'empires IA après le premier jour est
morte.** `is_low_tech_start` est lu par `game_start.txt` avant que le moindre
événement se déclenche ; un empire IA a donc déjà sa flotte et son arbre de
départ quand on pourrait l'atteindre, et rien ne permet de les lui retirer.

Il reste **les empires prédéfinis** (piste c de `kit/brainstorm_1_3.md`) : une
poignée de `predefined_countries` portant l'origine, que la génération de
galaxie place comme n'importe quel empire prédéfini. Ils naissent au sol, comme
le joueur — pas de conversion, rien à reprendre. Plus lourd à écrire, et
meilleur : des voisins **nommés**, avec leur portrait et leur éthique.

---

## Les chiffres au 16/08, 16h — cinq jours après la première bêta

| | |
|---|---|
| Visites uniques | 5 491 |
| Abonnés | 954 |
| Favoris | 237 |
| Commentaires | 43 |
| Collections | 16 |
| Note | ★★★★☆ sur 40 évaluations |

Trois rapports valent mieux que les valeurs brutes :

- **Favoris / abonnés = 25 %.** Un abonné installe ; celui qui met en favori
  revient. Un quart de l'audience s'est mise en position d'attente de mise à
  jour.
- **Commentaires / abonnés = 4,5 %.** Le taux qui explique la qualité des
  retours de la semaine.
- **Visites → abonnés = 17 %**, obtenu avec la vignette du premier jet et des
  captures françaises sur un titre anglais. Chaque point de conversion gagné
  vaut ~55 abonnés sur le trafic déjà encaissé.

**Ce que ces chiffres changent à la priorité :** 954 personnes ont la 1.2 avec
le blocage de prospection intact. Le seul joueur qui ait compté l'estime à deux
parties sur cinq. Le correctif est écrit et n'a jamais été lancé.

**Et la note est la seule métrique qui ne se rattrape pas.** 40 évaluations,
4,2 % des abonnés — taux élevé, comme le reste. Un abonné se désabonne sans
laisser de trace ; une évaluation reste. Chaque jour où le blocage de
prospection tourne en ligne se convertit en étoiles définitives. À quatre
étoiles sur 40 votes, une poignée d'évaluations basses pèse encore lourd dans
la moyenne — dans les deux sens.

---

## Ce qui reste ouvert

1. **`tech_subspace_drive`** — techno de départ passée au travers du verrouillage, à vérifier en jeu.
2. **Captures d'écran anglaises** — trois demandes indépendantes, action en jeu.
3. **Contributeurs** — argroww (textes) et dkr127054 (russe) attendent une invitation.
4. **Colonisation de la planète natale** — idée de Lucky13crocket, à instruire après la 1.2.
5. ~~**Type nomade barré dans `possible`**~~ — ✅ corrigé en 1.2.1, la syntaxe est celle du jeu de base.

---

## Audit du jeu de base — 16/08, au retour du pont

Six investigations en un passage, lecture seule. Trois décisions tombent.

| # | Question | Réponse | Effet |
|---|---|---|---|
| 1 | Comment barrer le type nomade ? | `is_nomadic = no` dans `possible`, **six origines vanilla le font** | ✅ **corrigé en 1.2.1** |
| 2 | `is_country_type = default` dans les casus belli et buts de guerre ? | **39 et 29**, aucun sous un `NOT` | à traiter en **1.2.1b** |
| 3 | Les factions sont-elles fermées pendant le confinement ? | **40 gardes** sur 12 des 14 fichiers | la **1.3 garde son cœur** |
| 4 | `remove_technology` existe-t-il ? | **non**, zéro occurrence | tue la conversion d'IA, **1.3** |
| 5 | Une règle `can_survey_planet` ? | **non** — seul `is_surveyed`, dans une règle de faille astrale | tue le mécanisme 1 de l'exploration occultée, **1.3** |
| 6 | L'occultation est-elle gardée par un DLC ? | aucune garde visible dans `component_templates` | non concluant, faible priorité |

**Le point 3 est le plus important pour la suite.** Les factions du jeu de base
sont bien fermées à un empire au sol, exactement comme l'étaient les actions
diplomatiques, les désignations de capitale et la Grande Archive. La 1.3 ne
part donc pas de zéro et ne se heurte pas à un mur : elle demande **le même
travail d'élargissement, déjà fait quatre fois**, sur 40 gardes réparties sur
douze fichiers. `tools/gen_diplomacy_overrides.py` sait faire ça sans remplacer
le bloc vanilla.

**Le point 4 tranche la galaxie asymétrique.** `remove_technology` n'existe pas :
on ne reprend pas une technologie à un empire. La conversion d'empires IA au
premier jour est donc morte — `is_low_tech_start` est lu par `game_start.txt`
avant tout événement, l'IA a déjà sa flotte et son arbre quand on pourrait
l'atteindre. Il reste **les empires prédéfinis** : ils naissent au sol comme le
joueur, rien à leur reprendre, et ils ont un nom et un visage.

**Le point 5 tranche l'exploration occultée.** Il n'y a pas de règle de
prospection à élargir : le refus est dans le moteur. Il faudra le mécanisme 2 —
la prospection par effet depuis un vaisseau présent dans le système. Moins net
dans l'interface, mais ça marche à coup sûr.

**Et une trouvaille de côté : le nomadisme est un DLC.** Les cinq civics qui le
portent (`civic_caravan_masters`, `civic_deep_sleep`, `civic_void_reavers`,
`civic_flight_schools`, `civic_hired_guns`) sont gardées par
`playable = { has_nomads_dlc = yes }`. Aldran le possède donc — et ça explique
que personne d'autre n'ait signalé le problème.

---

## Incompatibilité Gigastructural — confirmée par argroww (16/08)

> *« Confirmed, This mod is currently not compatible with Giga, results in a
> colony with no city district. (Ran a game with only Giga and this mod) »*

**Le rapport le plus utile depuis la sortie, et il me donne tort.** J'avais
conclu à la compatibilité en lisant les fichiers de Giga et je l'ai écrit dans
les deux descriptions. Un test à deux mods dit le contraire. **La revendication
est retirée des descriptions**, remplacée par l'incompatibilité connue.

Premiers relevés, pour ne pas repartir de zéro :

| Vérifié | Résultat |
|---|---|
| Giga redéfinit-il `district_city` ? | **non** — seulement `district_city_katzen` |
| Giga déclare-t-il un `replace_path` ? | **non** |
| `@base_rural_district_jobs`, la seule variable que notre fichier emprunte | vanilla, dans `scripted_variables/100_scripted_variables_zones.txt`, non touchée par Giga |

Donc ce n'est **pas** un écrasement direct. La cause est ailleurs — zones,
inline scripts, ou un effet de bord de notre copie figée de `district_city`. À
traquer avec un test à deux mods et un `error.log`.

**Et argroww a trouvé un second conflit :** *Ethics and Civics Classic*
perturbe la chaîne des capitales. C'est très probablement notre surcharge de
`is_regular_empire` — celle que la description signale déjà comme le point de
rencontre le plus probable.

### Piste trouvée en code, 17/08 — minniefinnie confirme le symptôme

> *« ye canne build any o the structures cuz ye start w/o a city district also
> the buff that reduces upkeep fer yer civ dosent go away ever »*

Un deuxième témoignage, indépendant d'argroww, avec le même symptôme exact :
**pas de district de ville dès le départ.** Ça élimine l'hypothèse d'un
mauvais relevé isolé.

En relisant `adastra.2` (l'événement d'initialisation, déclenché par
`on_game_start_country`) plutôt que le fichier `district_city` lui-même, un
point n'avait pas encore été vérifié : **le bloc `capital_scope` de `adastra.2`
suppose que `district_city` existe déjà sur la capitale au moment où il
tourne.**

```
capital_scope = {
    remove_zone = { district = district_city zone = zone_research_unity }
    remove_zone = { district = district_city zone = zone_industrial }
    ...
    add_building = { district = district_city zone = zone_default building = building_adastra_seat }
    ...
}
```

`remove_building = building_capital` réussit toujours (une capitale n'est pas
liée à un slot de zone). Mais si `district_city` n'existe pas encore — ou pas
du tout — sur la planète au moment où `adastra.2` s'exécute, le
`add_building` qui pose notre capitale d'époque (Cercle de pierres, etc.)
**échoue silencieusement.** Aucune erreur dans `error.log`, aucun blocage :
juste une capitale qui n'apparaît jamais et une planète sans district de
ville. Ça explique d'un coup les trois symptômes rapportés : pas de district
de ville, incapacité à construire (les bâtiments de recherche visent aussi des
slots de `district_city`), et le palier « pré-manufacture » qui ne se retire
jamais (`adastra_has_consumer_goods` dépend de `tech_adastra_steam_engine`,
jamais recherchée si la planète ne peut plus rien produire).

Le fichier ne contient nulle part un `add_district` défensif : il a toujours
tenu pour acquis que la génération de galaxie pose le district avant que le
premier `on_game_start_country` ne tourne. C'est vrai en solo. Reste à vérifier
si Giga retarde ou modifie cette génération pour une origine non standard —
exactement le test à deux mods déjà demandé plus haut, mais on sait maintenant
*où* regarder dans nos propres fichiers plutôt que dans ceux de Giga.

**Correctif possible, pas encore écrit :** garder un `if = { limit = { NOT =
{ ... } } add_district ... }` avant le `remove_zone`/`add_building`, pour que
`adastra.2` répare la planète au lieu de supposer qu'elle est déjà en ordre.
À faire quand le test à deux mods aura confirmé le diagnostic — pas avant,
pour ne pas corriger un symptôme qu'on n'a pas encore vu se reproduire dans
nos propres logs.

## Nova Starborn — « je ne peux rien rechercher ni rien construire » (16/08, puis 17/08)

Diagnostiqué par **argroww** avant moi : ses fichiers n'étaient pas passés en
1.2 correctement, et forcer la mise à jour a tout réglé. Steam laisse parfois
des fichiers 1.1 à côté des 1.2 ; les verrous d'âge ne s'ouvrent jamais.
Réponse rédigée : désabonner, supprimer le dossier résiduel, réabonner,
nouvelle partie.

**17/08 : même pseudo, même plainte, dans le même fil que minniefinnie et
argroww.** Deux causes possibles cette fois, à distinguer avant de renvoyer la
même réponse que le 16/08 : soit le même problème de fichiers résiduels,
soit — vu le contexte du fil — la même incompatibilité Giga que ci-dessus. À
lui demander explicitement si Giga est actif avant de répondre, plutôt que de
supposer que c'est rejouer le bug du 16/08.

**Sur « also progess is so slow it puts ye to sleep » (minniefinnie) :** pas de
piste de bug séparée trouvée en code. Le rythme de l'ascension a déjà été
délibérément ralenti en 1.2 (`monthly_progress` de la situation mis à l'échelle
×0,5, âges deux fois plus longs, en réponse à d'autres retours qui demandaient
l'inverse) — c'est un compromis de rythme assumé, pas un bug. Et pour
minniefinnie précisément, une planète sans district de ville qui ne peut
quasiment rien produire donne mécaniquement une impression de partie à
l'arrêt : très probablement le même symptôme que le district de ville manquant
plutôt qu'un second problème de rythme à traiter séparément.

### 17/08 au soir — la vraie cause, mesurée en jeu, et elle est dans la 1.3.0 publiée

Trois parties de test successives sur le pont, error.log à l'appui, ont fini
par isoler le mécanisme. `give_technology` refuse une technologie dont le
potential est faux — c'était connu — mais il exige AUSSI que ses **prérequis**
soient des technologies valides pour l'empire. Or depuis le 16/08 le potential
de chaque techno d'âge porte `NOT = { has_country_flag = adastra_reached_<âge
suivant> }` pour la retirer du tirage une fois l'âge passé ; et chaque techno à
partir du Bronze a pour prérequis le pilier de l'âge précédent. Dès qu'on pose
le drapeau du Bronze, la Pierre devient invalide, et TOUT le Bronze est refusé.
Chiffres du dernier log : les 25 technologies de la Pierre (aucun prérequis)
passent, les 200 autres échouent, 215 refus en tout. Peu importe l'ordre ou le
jour de l'octroi — deux hypothèses testées et écartées avant celle-ci.

Conséquence en cascade : sans les technologies des âges traversés, un départ
Machine/Atomique/Spatial n'a ni `tech_adastra_electricity` ni la machine à
vapeur, donc `adastra_has_energy` et `adastra_has_consumer_goods` sont faux au
moment où `adastra.2` décide quoi retirer de la capitale — générateurs
supprimés, énergie et biens de consommation mis à zéro dès 2200.01.01, et
aucun prérequis d'Âge spatial disponible : **vivier de recherche vide et
pénuries dès le premier tour, exactement les deux plaintes du fil Steam.** Le
dossier Workshop 3781408257 (1.3.0) contient les 225 clauses d'exclusion et les
225 prérequis : Nova Starborn et minniefinnie décrivent très probablement ce
bug-là, pas Giga.

Correctif (1.4) : l'exclusion du tirage passe par `weight_modifier` (facteur 0
dès l'âge suivant atteint), plus par le potential ; le bloc d'octroi est
déplacé AVANT le bloc `capital_scope` de `adastra.2` ; les vagues sont ouvertes
le temps de l'octroi puis recalculées. Le tout dans `tools/gen_age_techs.py`,
qui régénère `adastra_age_techs.txt`.

## Mr Gambler (16/08)

> *« Finally this mod exists. I've wanted this for years »*

Enthousiasme. Réponse rédigée — le mod auquel il pense est probablement
Pre-FTL Players, dont un ancien mainteneur est passé dans ces commentaires.
