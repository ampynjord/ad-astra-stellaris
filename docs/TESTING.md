# Protocole de test humain

La CI controle les sources, la generation, les localisations, la version et
l'archive de test. Stellaris n'est pas lance automatiquement : le test en jeu
est une etape humaine ciblee, apres le deploiement local du build.

## Regle de la fiche de test

Toute demande de test doit donner, dans cet ordre :

1. la version et le build a charger ;
2. la save de depart ou l'age a choisir, avec les reglages utiles ;
3. les actions numerotees a faire ;
4. ce qui confirme la reussite et ce qui constitue un echec ;
5. la duree cible, limitee a 5-15 minutes ;
6. la preuve a joindre seulement en cas d'echec : `error.log`, save et capture
   si elle eclaire le probleme.

Ne pas demander une partie exploratoire. Une fiche teste un comportement et
une modification precise. En cas de doute, interrompre la partie et joindre
la save plutot que de chercher a deviner la cause.

## Packs solo

### Demarrage et economie

Utiliser ce pack pour les origines, les ages de depart, les districts, les
zones, les batiments et les couts initiaux.

1. Nouvelle partie, empire Ad Astra, petite galaxie, sans mods tiers.
2. Choisir directement l'age concerne, puis une progression acceleree.
3. Attendre le premier jour, ouvrir Terra et la barre de ressources.
4. Verifier seulement les elements nommes dans la fiche : par exemple deux
   generateurs, zones Industrie et Archives, Fabrique et Laboratoire pour un
   depart Atomique.
5. Quitter et lire `error.log` si un element manque ou si une ressource est
   incoherente.

Duree cible : 5 minutes. Ne pas refaire les autres ages sauf si la correction
les touche.

### Progression Pierre vers Bronze

Utiliser ce pack uniquement pour les technologies, vagues, verrous et la
situation Beyond the Stars.

1. Nouvelle partie Ad Astra, Age de pierre, petite galaxie, progression
   acceleree et sans mods tiers.
2. Choisir la technologie indiquee par la fiche et lancer la vitesse maximale.
3. A la fin de la recherche, verifier qu'elle passe dans les technologies
   recherchees et ne revient pas dans le vivier.
4. Verifier que le verrou ou la situation ouvre l'etape Bronze attendue.
5. En cas de refus, de carte vide ou de boucle, quitter immediatement et
   joindre la save et `error.log`.

Duree cible : 10-15 minutes. Une correction qui ne touche pas la progression
ne doit pas demander ce pack.

### Premier lancement et sonde

Utiliser ce pack pour les decisions, les cibles et les evenements spatiaux.

1. Charger la save fournie par la fiche, ou partir directement de l'Age espace.
2. Executer une seule fois la decision indiquee.
3. Lire le texte de resultat et verifier la cible citee.
4. Refaire seulement le cas sans cible proche si la fiche le demande.
5. Quitter et joindre `error.log` uniquement si une ancienne cible reapparait,
   si le texte manque ou si la decision echoue.

Duree cible : 5-10 minutes.

## Pack multijoueur

Le multijoueur ne se teste pas a chaque version. Il est requis seulement pour
les changements de premier contact, cibles temporaires, scopes pays/planete,
reseau ou synchronisation d'evenements.

1. Les deux joueurs chargent exactement la meme archive et aucun autre mod.
2. L'hote cree une petite galaxie avec un empire Ad Astra Age de pierre ; le
   second joueur choisit l'empire indique dans la fiche, par exemple nomade.
3. L'hote et le client avancent jusqu'au premier contact puis observent le
   journal pendant trois minutes.
4. Succes : un premier contact progresse normalement et chaque message est
   emis une seule fois. Echec : boucle, message repete, blocage ou desync.
5. En cas d'echec, les deux joueurs conservent leur save et joignent chacun
   leur `error.log` avec le role hote/client et la date en jeu.

Duree cible : 10-15 minutes.

## Compte rendu

Apres une session, le compte rendu doit contenir la version, le pack execute,
le resultat, la date en jeu et les fichiers joints en cas d'echec. Un test
concluant ne prouve que le perimetre execute ; ne pas l'etendre a des
fonctionnalites non testees.
