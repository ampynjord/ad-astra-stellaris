# Rapports Discord et issues GitHub

GitHub est la source de verite technique : une issue garde le diagnostic, les
versions, les etiquettes, les decisions et le correctif. Discord reste l'espace
de conversation et de retours de partie.

Le bot propose une liaison volontaire dans un fil de forum. Il ne lit ni ne
copie automatiquement les messages des joueurs. L'auteur remplit les champs de
la commande `/github creer`, puis le bot publie une liaison vers l'issue. Les
etiquettes et l'etat GitHub sont ensuite repris dans le seul message du bot.

## Etiquettes de suivi

- `source: discord` : issue creee volontairement depuis un fil Discord ;
- `statut: informations requises` : donnees insuffisantes pour enqueter ;
- `statut: a reproduire` : diagnostic en attente d'une reproduction fiable ;
- `statut: confirme` : comportement observe en partie ou dans les fichiers ;
- `statut: corrige` : correctif sur `dev`, a valider avant fermeture ;
- `compatibilite` et `equilibrage` : axes qui peuvent s'ajouter a `bug` ou
  `idee`.

Une issue fermee est affichee comme fermee dans Discord. Les commentaires ne
sont pas recopies automatiquement : ils sont souvent contextuels et risquent
de melanger une discussion communautaire avec un diagnostic technique.
