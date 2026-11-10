# Test local

Le mod source vit dans `ad_astra`. Le launcher local ne le lit pas directement :
il charge la copie voisine `..\dev\ad_astra` via `ad_astra_dev.mod`.

Depuis la racine du depot, une seule commande couvre la boucle locale :

```powershell
python tools\build_and_sync_dev.py
```

Elle regenere les sorties internes, execute les controles, construit l'archive,
la copie dans `..\maj_1_4.zip`, puis remplace la copie chargee par le launcher.
Elle s'arrete avant tout deploiement si une verification echoue.

Lancer ensuite une nouvelle partie adaptee a la modification, relire
`Documents\Paradox Interactive\Stellaris\logs\error.log` et conserver la
sauvegarde lorsqu'une regression est observee.

La commande ne publie rien. Steam est declenche seulement par le workflow de
tag documente dans `PUBLICATION.md`.

Pour relever la progression et les jalons du pays joueur dans une sauvegarde
solo, depuis la racine du depot :

```powershell
python tools\inspect_playtest.py "C:\chemin\vers\B06-first-launch.sav"
```

Le rapport JSON donne la version de Stellaris enregistree dans la sauvegarde,
les mods declares, la progression de l'ascension et les marqueurs de lancement
et d'emergence. Joindre aussi le numero de beta, le checksum et les observations
de l'interface a la carte du cahier de tests.
