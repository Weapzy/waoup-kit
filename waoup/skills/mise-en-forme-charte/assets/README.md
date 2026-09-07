# Charte WAOUP

## Ce que contient ce dossier

- `waoup-charte.css` : la feuille de style de production. Elle tient seule, sans le
  fichier maison. Son en-tête dit comment brancher le vrai `waoup.css` et liste
  les tokens à remplacer, ceux marqués `[À CONFIRMER]` en premier.
- `gabarit-livrable.html` : le gabarit A4 complet, rempli d'un exemple fictif
  (Groupe Ardan, matériel BTP). S'ouvre tel quel dans un navigateur.
- `gabarit-deck.html` : le gabarit 16:9, six mises en page. Même feuille de style,
  même palette, une couche de géométrie de diapositive par-dessus. Trois usages :
  deck HTML projeté, PDF paysage, captures de référence pour le PowerPoint.
- `waoup-modele.pptx` : le modèle PowerPoint. Masque, six mises en page nommées
  (Couverture, Section, Une colonne, Deux colonnes, Tableau, Verbatim), polices et
  couleurs de la charte. C'est la troisième entrée obligatoire de la skill dès
  qu'un PPTX est demandé.

Les six mises en page portent les mêmes noms des deux côtés : la classe
`slide--tableau` de `gabarit-deck.html` remplit la mise en page `Tableau` du
modèle. Un gabarit ajouté d'un côté se déclare de l'autre, sinon la
correspondance se perd et Claude choisit à sa place.

## Les six corrections de la version 1.1 du CSS

Elles sortent du rapport `recherche/refonte2/04-powerpoint-charte.md`. Chacune est
commentée sur place dans le fichier, avec son numéro.

| # | Correction | Avant | Après |
| --- | --- | --- | --- |
| 1 | Rapport minimal de 1,25 entre deux niveaux typographiques | h4 à 1,02 rem contre 1 rem au corps | échelle 2,65 / 2,05 / 1,6 / 1,25 / 1 rem |
| 2 | Plancher de 11 px pour tout texte fonctionnel | `--t-micro` à 0,74 rem, soit 10,4 px à l'impression | 0,8 rem, soit 11,2 px |
| 3 | Le lime ne porte jamais de texte | `color: var(--lime)` posé directement | deux rôles nommés, `--lime-sur-noir` et `--texte-sur-lime` |
| 4 | Source de verbatim sans tiret cadratin ni point médian | séparateurs de chrome de template | `Entretien Ardan, chef d'agence, Le Havre` |
| 5 | Rythme d'espacement au-dessus des titres | valeurs anonymes dans les règles | six tokens nommés, déficit d'au moins 12 px garanti |
| 6 | Polices documentées | Inter et Space Grotesk sans mention | dérogation écrite, avec ce qu'elle coûte |

Aucune couleur n'a changé, aucune règle n'a été déplacée.

## Ce qu'il reste à déposer

Le fichier `waoup.css` de référence. Une fois déposé, le charger **après**
`waoup-charte.css` : il gagne sur tout ce qu'il redéfinit, et les règles
d'impression restent en place.

## Rappels issus de l'audit de la charte

- signature : noir `#26232E` et lime `#E2FFA6`
- `--navy` et `--forest` sont dépréciés et rendent en noir : à purger à la prochaine
  évolution de la charte
- le HEX du cyan pastel reste à confirmer. `waoup-charte.css` pose `#C7E7EF` en
  attendant, marqué `[À CONFIRMER]`
- le « test grandeur nature » (reproduire un livrable complet avec les seuls
  composants de la charte) reste à passer sur un vrai dossier. Les deux gabarits en
  sont une première passe

## Composants couverts

**Gabarit A4.** Page de garde, sommaire, titres h1 à h4, corps, chapô, listes à
puces et numérotées, tableau avec colonnes de chiffres, citation de verbatim avec
étiquette de source, quatre encadrés (à retenir, contexte, vigilance, affirmation
forte), chiffre clé, bloc de code, pied de page avec mention de confidentialité,
en-tête et pied répétés à l'impression.

**Gabarit 16:9.** Couverture, section, une colonne, deux colonnes, tableau,
verbatim. Format 338,7 x 190,5 mm, marges de 24 mm sur les côtés et 18 mm en haut
et en bas, corps à 18 pt, titre à 34 pt, pied de diapositive sur chaque page.

Ce qui n'est pas couvert et reste à trancher avec Fanny : les images et leurs
légendes, les schémas, la page de fin.

## Contrôler un fichier de ce dossier

```bash
node ../scripts/controle_ia.mjs waoup-charte.css gabarit-livrable.html gabarit-deck.html
```

Les trois passent à zéro défaut. Toute modification de ce dossier se termine par
cette commande : si elle sort autre chose que zéro, la modification n'est pas finie.
