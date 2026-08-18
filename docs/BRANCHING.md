# Flux de branches

`main` contient uniquement les versions publiees et les correctifs qui leur
sont destines. Toute modification y arrive par une pull request controlee.

`dev` est la branche d integration de la prochaine version mineure. C est la
branche de travail de la 1.4 tant qu elle n est pas figee.

Les nouvelles fonctions partent de `dev` dans `feature/<sujet>` et reviennent
vers `dev` par pull request. Les changements de documentation et de bot qui
sont destines a la prochaine version suivent le meme chemin.

Une fois le contenu fige, creer `release/<version>` depuis `dev`. Cette
branche n accepte que les corrections de sortie, la documentation et le
packaging. Sa pull request cible `main`.

Un correctif d une version deja publiee part du tag correspondant dans
`hotfix/<version>` et cible directement `main`. Il ne contient aucun travail
de la prochaine version. Apres merge, reporter `main` dans `dev` par pull
request afin que le correctif ne soit jamais perdu.

Un tag `v<version>` est cree uniquement sur le commit de `main` qui a ete
teste en jeu. Il declenche la publication Steam et la release GitHub. Ne pas
retagger, ne pas force-push et ne pas publier Steam hors de ce flux.

Flux actuel : `hotfix/1.3.1` vient de `v1.3.0` et cible `main`; `dev` porte la
1.4. Apres la sortie 1.3.1, merger `main` vers `dev` avant de poursuivre la
1.4.
