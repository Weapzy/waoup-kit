# Charte WAOUP

## Ce que contient ce dossier

- `waoup-charte.css` : la feuille de style de production. Elle tient seule, sans le
  fichier maison. Son en-tête dit comment brancher le vrai `waoup.css` et liste
  les tokens à remplacer, ceux marqués `[À CONFIRMER]` en premier.
- `gabarit-livrable.html` : le gabarit complet, rempli d'un exemple fictif
  (Groupe Ardan, matériel BTP). S'ouvre tel quel dans un navigateur.

## Ce qu'il reste à déposer

Le fichier `waoup.css` de référence et, si disponible, `slide-base.html`.
Une fois `waoup.css` déposé, le charger **après** `waoup-charte.css` : il gagne
sur tout ce qu'il redéfinit, et les règles d'impression restent en place.

## Rappels issus de l'audit de la charte

- signature : noir + lime `#E2FFA6`
- `--navy` et `--forest` sont dépréciés et rendent en noir : à purger à la prochaine
  évolution de la charte
- le HEX du cyan pastel reste à confirmer. `waoup-charte.css` pose `#C7E7EF` en
  attendant, marqué `[À CONFIRMER]`
- le « test grandeur nature » (reproduire un livrable complet avec les seuls
  composants de la charte) n'a jamais été passé : c'est le meilleur moyen de valider
  ce dossier. `gabarit-livrable.html` en est une première passe, à confronter à un
  vrai livrable

## Composants couverts par le gabarit

Page de garde, sommaire, titres h1 à h4, corps, chapô, listes à puces et numérotées,
tableau avec colonnes de chiffres, citation de verbatim avec étiquette de source,
quatre encadrés (à retenir, contexte, vigilance, affirmation forte), chiffre clé,
bloc de code, pied de page avec mention de confidentialité, en-tête et pied répétés
à l'impression.

Ce qui n'est pas couvert et reste à trancher avec Fanny : les images et leurs
légendes, les schémas, la page de fin, la déclinaison paysage.
