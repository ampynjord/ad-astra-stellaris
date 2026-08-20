# Refonte de la recherche — la progression, c'est la recherche (19/08/2026)

Décision d'ampynjord, 19/08 : « une refonte du système technologique s'impose,
c'est trop complexe ». Deux options posées — score par technologies, ou arbre
technologique — retenues **ensemble** : la progression vient des technologies,
l'ordre vient d'un arbre de prérequis. L'interface d'arbre viendra après, elle
n'affichera que ce que le moteur applique déjà.

## Ce qui disparaît

- La barre qui monte au mois (`monthly_progress` base 0,06 et ses modificateurs
  de rythme, d'approche, d'unité, de recherche).
- Les vagues (`adastra_vague_2..5`, `adastra_maj_vagues`, `adastra.90`, le
  forçage des vagues dans `adastra.2`).
- Le verrou de fin d'âge (266 modificateurs `mult = 0.001` générés) et ses
  clés `adastra_manque_*`.
- Les seuils `12/22/31/39/47/55/64/74/86/100/110/120/130`.

## Ce qui reste

- Les 250 technologies, leurs dates, bonus, coûts, bâtiments (`age_techs_data.py`).
- Les drapeaux d'âge (`adastra_reached_*`, `adastra_unlock_*`), posés à
  l'entrée d'étape par `adastra.40-49`.
- L'octroi des âges traversés pour un départ tardif, la capitale par âge,
  l'économie datée, les surcharges vanilla, les fondatrices par étape du
  programme, les jalons.
- La poussée de la première rangée dans le vivier (`adastra.130`).

## Les règles

1. **Treize étapes de 25 points** : dix âges puis les trois étapes du programme
   (Exploration 250→275, Chantier 275→300, Hyperespace 300→325). Un départ à
   l'âge N commence à 25·N.
2. **Une technologie d'époque acquise = +1 point** dans la situation, si elle
   appartient à l'âge courant (`on_tech_increased` → `adastra.132`). Vingt-cinq
   technologies font passer l'âge. Le verrou « toutes les techs » est inhérent.
3. **Un arbre par âge** : les techs sont rangées par date en cinq rangs de
   cinq. Le rang 1 exige le pilier du même domaine à l'âge précédent (règle
   existante) ; un rang N ≥ 2 exige une tech de rang N-1 du même domaine dans
   le même âge (à défaut, du rang N-1 tous domaines). Le moteur ne propose
   qu'une tech dont les prérequis sont acquis : l'ordre historique est tenu
   sans drapeau.
4. **Programme spatial** : chaque fondatrice du lot de l'étape ajoute
   `24 // N` points ; le jalon (système prospecté / base + station /
   Hyperpropulsion) porte l'étape à sa fin, à condition que le lot soit
   complet (`adastra.71/72/10`).
5. **Rythme** : les coûts par âge et les pénalités de recherche par étape.
   Les quatre rythmes (`adastra_pace_*`) deviennent des modificateurs de
   vitesse de recherche (rapide +50 %, lent -33 %, très lent -50 %) ; les
   approches échangent recherche contre stabilité/unité.

## Sauvegardes

Une partie 1.3/1.4 chargée en 1.5 garde ses technologies ; sa progression
est réalignée au chargement sur `25·(âge atteint) + techs de l'âge acquises`
(`adastra.133`, une fois). Les drapeaux de vagues sont ignorés.

## Ce que ça ne règle pas

La frontière vanilla / Ad Astra (paliers, exceptions d'économie, fondatrices)
reste une affaire de surcharges. Le vivier lent du moteur reste poussé à
l'entrée d'un âge.

## Interface à terminer

Quand une technologie Ad Astra rend une spécialisation de district disponible,
sa description doit l'annoncer explicitement, comme les technologies vanilla.
La liste doit être générée depuis la même table source que les gardes de zones,
afin qu'une spécialisation ne puisse jamais être déverrouillée sans être
annoncée au joueur.
