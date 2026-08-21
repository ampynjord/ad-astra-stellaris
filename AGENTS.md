# AGENTS.md — Ad Astra (Stellaris 4.4)

Lire d'abord `PASSATION_CODEX.md` et `retours_communaute.md`. Ils decrivent
respectivement l'etat technique et la memoire des retours joueurs.

## Sources et generation

- `ad_astra` est la source du mod ; `build` est une sortie jetable.
- Echanges et commentaires en francais ; commentaires de code sans accents,
  dates et centres sur le pourquoi.
- Ne jamais modifier un fichier `GENERE PAR tools/...`. Modifier la table ou
  le generateur, puis lancer `python tools/verify_generated.py`. Ce controle
  regenere les sorties internes et echoue si un diff n'est pas versionne.
- Ne melanger ni reformatage, ni refonte, ni contenu non necessaire avec une
  correction ciblee. Preserver les modifications existantes.

## Diagnostic et invariants

- Partir des faits reproductibles : `error.log`, save, version, age de depart,
  rythme et mods actifs. Verifier les noms et la syntaxe dans le vanilla avant
  toute hypothese.
- Ne jamais remettre `NOT = { has_country_flag = adastra_reached_<suivant> }`
  dans le `potential` d'une technologie : `give_technology` invaliderait ses
  prerequis. L'exclusion du tirage passe par `weight_modifier`.
- Ne pas employer la syntaxe CK3 (`if` / `limit`) dans les `script_values`, ni
  definir `START_YEAR` hors de `NGameplay`.
- Prouver une compatibilite en partie pure et avec `error.log`. Une surcharge
  vanilla seule ne prouve pas une incompatibilite.

## Verification et livraison

Apres toute modification du mod, executer :

```powershell
python tools/verify_generated.py
python tools/verify_1_2.py
python tools/verify_release.py
python tools/ci_release.py --sortie build
```

Le script `tools/build_and_sync_dev.py` execute cette boucle et deploie le
build dans le workspace local de reference. Verifier ensuite en jeu sur une
nouvelle partie adaptee a la modification, relire `error.log` et conserver la
save en cas de regression.

## Tests humains

- Stellaris ne fait pas partie de la CI : aucun workflow ne lance le jeu ni
  ne modifie `userdir.txt`. La CI valide les sources et fabrique l'archive de
  test ; la validation en jeu est humaine.
- Avant de demander un test, fournir une fiche courte et executable : version
  a charger, save ou age de depart, reglages, actions numerotees, resultat
  attendu, duree cible et preuve a renvoyer. Ne jamais demander un test vague.
- Viser une session de 5 a 15 minutes. Regrouper les controles compatibles
  dans une meme save et partir directement de l'age concerne lorsque le
  comportement ne depend pas de la progression precedente.
- Demander `error.log` et la save uniquement en cas d'echec ou de comportement
  ambigu. Un test concluant doit etre consigne dans le compte rendu avec sa
  version, sa date et son perimetre.
- Le multijoueur est un scenario distinct a deux joueurs. Ne le demander que
  pour une modification des contacts, scopes, cibles temporaires ou reseau ;
  utiliser le protocole de `docs/TESTING.md`.

La branche de travail est `dev`. Ne pas merger dans `main`, tagger, publier
Steam, modifier les secrets ou les protections sans demande explicite. Une
sortie aligne descripteur, changelog, archive, note et descriptions Workshop.

## Communaute

- `discord-bot` est l'interface de l'IA pour lire et administrer le serveur
  Discord du mod. Commencer par une lecture ciblee ; ne modifier que les
  contenus editoriaux fixes explicitement autorises.
- Ne jamais supprimer, deplacer ou editer les messages, rapports, captures ou
  fils des joueurs. Ne jamais exposer le jeton du bot.
- Repondre avec le numero de version et les conditions de test, puis demander
  confirmation. Reporter diagnostic et statut dans `retours_communaute.md`.
