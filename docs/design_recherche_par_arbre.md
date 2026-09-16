# Recherche et ascension

La progression d'Ad Astra n'est pas mensuelle : elle est exclusivement obtenue
par des recherches et des actes concrets. Cette regle vaut pour les parties
nouvelles et pour les sauvegardes recalees une seule fois par `adastra.133`.

## Ages historiques

Les dix ages historiques occupent les points 0 a 250 : Pierre, Bronze, Fer,
Medieval tardif, Renaissance, Vapeur, Industriel, Machine, Atomique et Espace
initial. Chaque age contient vingt-cinq technologies Ad Astra.

- Une technologie de l'age courant vaut un point.
- Le vivier applique les prerequis de rang dans chaque domaine : un rang ne
  doit pas apparaitre avant le rang precedent requis.
- Aucun verrou de fin d'age n'est place dans `potential`. Les technologies
  deja disponibles restent des prerequis valides quand l'age change.
- Les technologies vanilla sont ouvertes progressivement par les surcharges
  generees, sans remplacer le vivier vanilla.

Un depart dans un age tardif commence au seuil de cet age et possede les
technologies historiques precedentes necessaires a sa coherence economique.

## Programme spatial

Les six etapes suivantes conduisent de 250 a 400. Une etape se termine quand
ses fondations techniques et son geste de jeu sont tous deux accomplis.

1. **Premier lancement** (250-275) : reussir `Lancement suborbital`. Un echec
   laisse la decision disponible ; une reussite la retire definitivement.
2. **Exploration** (275-300) : rechercher Construction spatiale et
   Colonisation, lancer le Programme d'exploration, puis achever le releve des
   corps non stellaires du systeme natal avec le vaisseau scientifique livre.
3. **Construction** (300-325) : rechercher les cinq fondations de coque,
   armes, blindage, boucliers et reacteurs, puis lancer le programme qui livre
   le Batisseur.
4. **Avant-poste** (325-350) : rechercher `Starbase Construction` et utiliser
   le Batisseur pour construire normalement la premiere base stellaire dans le
   systeme natal. Aucun evenement ne cree gratuitement cette base.
5. **Infrastructure orbitale** (350-375) : obtenir les technologies de base
   stellaire et de station, puis construire une station miniere ou de recherche
   normale.
6. **Hyperespace** (375-400) : lancer le Programme hyperspatial puis terminer
   Hyperpropulsion. L'emergence n'a lieu qu'a ce dernier point.

Les points intermediaires rendus par les technologies fondatrices sont
intentionnellement visibles, mais aucun d'eux ne peut finir une etape sans son
geste concret. Le journal de situation et les evenements d'etape doivent
toujours nommer ce geste.

## Astronomie

L'astronomie est independante du programme spatial. L'observatoire se
developpe en trois niveaux historiques : optique, radio puis spatial. Construire
un telescope ne revele rien. Le joueur lance ensuite une Observation
astronomique, longue et payante, qui revele uniquement l'etoile d'un systeme
aleatoire jamais observe : portee d'un saut, trois sauts, puis cinq sauts. Elle
ne prospecte ni planetes, ni lunes, ni ressources.

## Maintien

`tools/gen_age_techs.py` est la source des technologies et regenere les
fichiers d'age. Toute modification de leur ordre, cout, prererequis ou texte
doit passer par la table source, puis par les validateurs et le build local.
