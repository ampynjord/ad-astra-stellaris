# Flux de branches

Le depot n'a que deux branches.

`main` contient uniquement les versions stables publiees et les correctifs qui
leur sont destines. C'est la branche par defaut et la page d'accueil du depot.
Toute modification y arrive par une pull request controlee (CI verte,
historique lineaire : fusion par *squash* ou *rebase*).

`beta` porte le developpement de la prochaine version et ses betas publiques.
On y travaille directement ; chaque push relance les controles du mod et
produit une archive de test.

Une beta publique est publiee depuis `beta` par le workflow manuel
**beta release** (tag `beta-X.Y.Z-beta.N`, pre-release GitHub, jamais de
Steam). Une beta publiee n'est pas remplacee : un correctif devient le numero
suivant. La remplacer (supprimer sa release et son tag, puis la republier)
reste une exception decidee par le mainteneur.

Quand la version est prete, une pull request `beta` → `main` la fait entrer
dans `main`. Le tag `v<version>` est ensuite pose sur le commit de `main` teste
en jeu : il declenche la publication Steam et la release GitHub. Ne pas
retagger, ne pas forcer l'historique de `main` et ne pas publier Steam hors de
ce flux.

Un correctif urgent de la version stable se fait par une pull request courte
vers `main`, puis `main` est reporte dans `beta` pour ne jamais le perdre. Les
branches de travail temporaires sont supprimees des leur fusion.
