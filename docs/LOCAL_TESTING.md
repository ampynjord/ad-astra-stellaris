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
