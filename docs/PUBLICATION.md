# Publier Ad Astra

Trois branches d'idées : on développe en local, `dev` valide, `main` publie.
Rien ne part sur Steam sans avoir traversé exactement les mêmes contrôles deux
fois.

```
    local  ──push──▶  dev  ──pull request──▶  main  ──tag v*──▶  Steam
                      │                        │                  │
                   contrôles               contrôles          contrôles
                                                              + publication
```

Chaque push sur `dev` regenere et verifie les sorties internes, execute les
controles du mod et produit une archive de test disponible pendant 14 jours.
Cette archive n'est jamais envoyee sur Steam : seul un tag sur `main` declenche
la publication.

---

## Le cycle normal

```bash
git switch dev
# ... tu développes, tu génères, tu testes en jeu ...
python tools/build_and_sync_dev.py  # controles, archive et copie launcher
git commit -am "..."
git push origin dev
```

La CI de `dev` tourne. Si elle est verte :

```bash
gh pr create --base main --head dev --fill
```

La pull request relance les mêmes contrôles. **`main` est protégée : tant que
le job est rouge, le bouton de merge est gris.** Une fois mergée, rien ne part
sur Steam — c'est voulu. Corriger une faute dans le README ne doit pas envoyer
une notification à 954 abonnés.

## Publier

La publication est déclenchée par un tag, et seulement par un tag.

```bash
git switch main && git pull
# 1. la version dans ad_astra/descriptor.mod ET ad_astra.mod
# 2. la section de tête du CHANGELOG.md, qui doit porter la même version
#    et ne PAS être marquée « en cours »
git commit -am "1.3.1"
git push origin main
git tag -a v1.3.1 -m "1.3.1"
git push origin v1.3.1
```

À partir de là tout est automatique : contrôles, construction du contenu,
manifeste, envoi sur le Workshop, release GitHub avec l'archive attachée.

Si le tag, le descripteur et le changelog ne disent pas la même chose, la CI
s'arrête **avant** d'avoir touché à Steam.

---

## Les secrets à poser une fois

*Settings → Secrets and variables → Actions → New repository secret.*

| Secret | Ce que c'est |
|---|---|
| `STEAM_USERNAME` | ton identifiant Steam, en clair |
| `STEAM_CONFIG_VDF` | le `config.vdf` d'un SteamCMD déjà authentifié, encodé en base64 |

**Ton mot de passe Steam n'est jamais stocké nulle part**, ni ici, ni dans un
secret, ni dans un fichier. Le `config.vdf` contient un jeton de session que
Steam a déjà validé avec Steam Guard, et rien d'autre.

### Fabriquer `STEAM_CONFIG_VDF`

Sur ta machine, avec le SteamCMD que tu as déjà :

```powershell
cd C:\Users\Public\AdAstra\steamcmd
.\steamcmd.exe +login TON_PSEUDO +quit
```

Il demande le mot de passe puis le code Steam Guard. Une fois connecté, il a
écrit `config\config.vdf`. Encode-le :

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("$PWD\config\config.vdf")) | Set-Clipboard
```

Colle le presse-papiers dans le secret `STEAM_CONFIG_VDF`. C'est tout.

### Quand ça casse

Ce jeton n'est pas éternel. Il est invalidé si tu changes ton mot de passe, si
tu révoques tes sessions, et parfois tout seul après plusieurs mois. Le
symptôme est net : le job **sortie** échoue à l'étape *envoyer sur le
Workshop*, avec un refus de connexion. Le mod n'est pas touché — la CI vérifie
que SteamCMD a répondu `Success` avant de considérer que c'est publié.

Refais les deux commandes ci-dessus, remplace le secret, puis rejoue le tag :

```bash
git tag -d v1.3.1 && git push origin :v1.3.1
git tag -a v1.3.1 -m "1.3.1" && git push origin v1.3.1
```

C'est la seule pièce de la chaîne qui demandera de l'entretien. Il n'existe pas
de moyen d'authentifier SteamCMD sans un geste humain quelque part : Steam
Guard est fait pour ça.

---

## La description française

**Steam garde bien une description par langue** — chaque langue a son propre
titre et son propre texte, l'anglais servant de repli pour tout le monde.
Mais le manifeste de SteamCMD (`workshop_build_item`) **n'a pas de champ de
langue** : il n'écrit que la description par défaut, l'anglaise.

Donc :

- `workshop/description_EN.txt` part automatiquement à chaque publication ;
- `workshop/description_FR.txt` se pose à la main, et seulement quand elle
  change — c'est-à-dire une ou deux fois par an.

Le geste, sur la page du mod : menu `≡` à droite → **Modifier le nom et la
description** → choisir **français** dans la liste des langues → coller.

**La CI te le rappelle toute seule.** À chaque sortie, le résumé du job
compare `description_FR.txt` au tag précédent et écrit soit « description
française inchangée, rien à faire », soit la marche à suivre. Tu n'as pas à y
penser.

---

## Protéger `main`

*Settings → Branches → Add branch ruleset*, sur `main` :

- **Require a pull request before merging** — pas de push direct sur `main`.
- **Require status checks to pass** → coche `vérifier le mod`.
- **Require branches to be up to date before merging**.
- Laisse *Allow force pushes* décoché.

Sans ça, la chaîne fonctionne mais rien n'empêche de la contourner un soir de
fatigue. C'est précisément ce soir-là qu'on en a besoin.

---

## Ce que la CI contrôle

Un seul fichier, `.github/workflows/checks.yml`, appelé à l'identique par la
chaîne `dev` et par la chaîne de sortie. Ajouter un contrôle à un endroit
l'ajoute aux deux.

**`tools/verify_1_2.py`** — 35 règles sur le mod lui-même : bornes historiques
des 250 technologies, exclusivité des vagues, icônes présentes et sans chiffre
romain, verrous de la situation, ordre des octrois, modificateurs inventés,
fuite de technologies vanilla avant l'émergence, `needs_border_access`,
identifiant Workshop.

**`tools/verify_release.py`** — la cohérence de la sortie : version identique
dans `descriptor.mod`, `ad_astra.mod`, le `CHANGELOG` et le tag ; section de
tête du changelog pas marquée « en cours » ; descriptions sous les 8000
caractères de Steam et BBCode équilibré ; aperçu sous 1 Mio ; parité des clés
de traduction FR/EN ; noms de bâtiments français restés dans les textes
anglais.

**`tools/changenote.py`** — la note de changement se construit, donc elle
existe. Une note qui ne se génère pas le jour de la sortie est une sortie
ratée.

**`tools/ci_release.py`** — refuse d'écrire un manifeste sans
`publishedfileid`, et refuse de publier un contenu qui n'embarque pas ses 250
icônes. Ces deux garde-fous ne sont pas théoriques : le premier a coûté un
mod dupliqué sur le Workshop, le second a failli coûter une version sans
aucune icône.
