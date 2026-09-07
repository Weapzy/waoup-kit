---
name: mise-en-forme-charte
description: Met en forme un livrable Markdown validé à la charte WAOUP en HTML, PDF ou PowerPoint modifiable depuis le modèle maison. Dernière étape, une seule fois, sans marqueur d'IA.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "2.0"
---

# Mise en forme à la charte WAOUP

Le fond se fige en Markdown, la forme se pose une fois, à la fin. Un Markdown coûte dix fois moins de contexte qu'un PowerPoint et se corrige en trois secondes. Le fichier qui circule ensuite est le PowerPoint, pas le PDF.

Cette skill ne fait pas de beau. Elle donne à Claude de quoi ne rien inventer, puis elle vérifie qu'il n'a rien inventé.

## Quand l'utiliser

Sur un Markdown dont le fond est arrêté et relu, quand il faut en sortir un HTML chartée, un PDF ou un PowerPoint.

Jamais sur un brouillon : chaque retouche de fond après mise en forme coûte une régénération complète. Jamais deux fois de suite sur le même document : on corrige le Markdown, puis on relance une seule fois.

## Ce qu'il faut avant de commencer

**Trois entrées, et elles sont obligatoires.** Si l'une manque, réclamer, et s'arrêter là. Ne pas se dire « je vais approcher » : sans modèle, Claude invente une mise en page, et c'est celle que le client reconnaît.

| Entrée | Pourquoi | Sortie concernée |
| --- | --- | --- |
| **Le Markdown validé** | Le fond est figé. La skill met en forme, elle ne réécrit pas. | Toutes |
| **`assets/waoup-charte.css`** | Les valeurs exactes. Sans lui, Claude choisit d'autres couleurs, et il en choisit de reconnaissables. | Toutes |
| **`assets/waoup-modele.pptx`** | Le masque, les polices et les six mises en page. | PowerPoint seulement |

Réclamer aussi, si le Markdown ne les porte pas : le nom du client, la date d'émission, la mention de confidentialité, et le type de livrable.

**Formulation de la demande, quand une entrée manque.**

```
Il me manque [le modèle PowerPoint / la charte CSS / le Markdown validé] pour
produire ce livrable. Sans lui, la mise en forme sera inventée, et c'est
exactement ce qu'on cherche à éviter. Le fichier est dans le kit, à
kit/waoup/skills/mise-en-forme-charte/assets/. Peux-tu me le joindre ?
```

## Ce que la skill fournit

| Fichier | À quoi il sert |
| --- | --- |
| `assets/waoup-charte.css` | La feuille de style. Tokens, styles de document, règles d'impression. Son en-tête dit comment brancher le `waoup.css` maison. |
| `assets/gabarit-livrable.html` | Le gabarit A4 complet : couverture, sommaire, corps, tableau, verbatim, encadrés, pied. S'ouvre tel quel. |
| `assets/gabarit-deck.html` | Le gabarit 16:9, six mises en page. Deck HTML, PDF paysage, et captures de référence pour le PPTX. |
| `assets/waoup-modele.pptx` | Le modèle PowerPoint : masque, six mises en page nommées, polices et couleurs de la charte. |
| `scripts/md_vers_html.py` | Convertit un Markdown en HTML chartée. Python 3, aucune dépendance. |
| `scripts/controle_ia.mjs` | Le détecteur de marqueurs IA. Node, aucune dépendance, aucune installation. |
| `references/sans-marqueur-ia.md` | Les règles avec leur seuil et leur contre-mesure. À lire avant de trancher une question de mise en forme. |
| `references/vers-pptx.md` | La recette PowerPoint. À lire avant tout PPTX. |

## Procédure

```
- [ ] 0. Contrôler les entrées : Markdown validé, charte CSS, et le modèle si PPTX
- [ ] 1. Vérifier que le fond est figé (aucune modification prévue)
- [ ] 2. Choisir la sortie : HTML A4, PDF, PowerPoint
- [ ] 3. Produire, selon la sortie (ci-dessous)
- [ ] 4. Lancer scripts/controle_ia.mjs et corriger jusqu'à zéro
- [ ] 5. Passer les six contrôles avant d'envoyer
```

### Étape 0. Contrôle des entrées

Lister les trois entrées à voix haute et dire lesquelles sont là. Il en manque une, on réclame et on s'arrête. Aucune exception, y compris quand la demande semble simple : c'est justement sur les demandes simples que la mise en forme part en générique.

### Étape 3, sortie HTML

C'est la sortie de référence, et celle que Claude réussit le mieux : la charte est un CSS, et un CSS s'applique littéralement.

```bash
python3 scripts/md_vers_html.py restitution.md "260912 ARDAN - RESTIT - V2.html" \
  --client "Groupe Ardan" \
  --titre "Reprendre la main sur le parc de location" \
  --date "12 septembre 2026"
```

`--confidentiel "texte"` remplace la mention par défaut, `--confidentiel ""` la retire. `--sous-titre` remplit la phrase de cadrage de la couverture. `--gabarit` vise un autre gabarit. `--help` liste les syntaxes propres à la charte.

Le script lit un front matter YAML simple : `client`, `titre`, `sous-titre`, `date`. Les options de ligne de commande priment.

**Ce que le script attend du Markdown.** Un seul titre de niveau 1, en tête : c'est le titre du livrable, il part sur la couverture et ne se répète pas. Les titres de niveau 2 ouvrent les sections et fabriquent le sommaire ; sans eux, la page de sommaire est retirée.

Trois syntaxes en plus du Markdown courant :

```
::: cle Titre de l'encadré        encadré : cle, info, alerte, fort
contenu
:::

> La citation exacte.
> Entretien Ardan, chef d'agence, Le Havre

| Famille | Parc |            une colonne alignée à droite
| --- | ---: |                  devient une colonne de chiffres
```

La source de verbatim s'écrit avec des virgules, dans l'ordre source, fonction, lieu. Ni tiret cadratin d'ouverture, ni points médians de séparation : c'était deux tics de chrome de template, et c'est corrigé.

Si WAOUP fournit son `waoup.css`, le charger **après** celui de la skill : il gagne sur tout ce qu'il redéfinit, et les règles d'impression restent en place.

### Étape 3, sortie PDF

Impression de l'HTML chartée. Toujours par l'HTML, jamais un PDF généré directement.

Chrome, Imprimer, destination « Enregistrer au format PDF », marges par défaut, **case « Graphismes d'arrière-plan » cochée**. En ligne de commande :

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --no-pdf-header-footer \
  --print-to-pdf=livrable.pdf "file://$PWD/livrable.html"
```

Pour un deck, partir de `gabarit-deck.html` et imprimer en **paysage** : le fichier déclare son propre format de page, 338,7 x 190,5 mm.

### Étape 3, sortie PowerPoint

Lire `references/vers-pptx.md` avant. Voie retenue : **depuis Cowork, remplir `assets/waoup-modele.pptx`**, mise en page par mise en page. L'add-in Claude for PowerPoint est l'alternative quand le poste a Microsoft 365, et le bon outil pour corriger une seule diapositive d'un deck existant. La conversion automatique de l'HTML vers le PPTX est écartée : elle pose chaque diapositive en image, et une image ne se modifie pas.

Les six mises en page du modèle portent les mêmes noms que les six gabarits de `gabarit-deck.html` : Couverture, Section, Une colonne, Deux colonnes, Tableau, Verbatim.

**Ce qui ne se négocie pas.**

- **Le texte ne change pas d'une ligne.** Le fond est figé. Pas de résumé, pas de reformulation, pas de complément. Si une diapositive ne tient pas, on la coupe en deux, on ne raccourcit pas le texte du client.
- **Toute la structure avant tout le contenu.** Créer les diapositives vides sur les bonnes mises en page, dans l'ordre, puis écrire dedans. L'inverse détruit le fichier.
- **Un tableau reste un tableau PowerPoint.** Jamais une image, jamais une liste à puces. Un graphique reste un graphique éditable.
- **Une idée par diapositive.** Quatre idées font quatre diapositives, pas une grille de quatre cartes.
- **Le titre porte la conclusion, en douze mots au plus.** « Le retour de matériel n'a pas de propriétaire », pas « Le processus de retour ».
- **Corps à 18 pt.** C'est le plancher de lisibilité au fond d'une salle. Quarante mots hors tableau, cinq puces au plus, deux lignes par puce, aucun second niveau de puce, six lignes de tableau au plus.
- **Aucune couleur hors du masque et du bloc `:root` de la charte.**

### Étape 4, contrôle automatique

```bash
node scripts/controle_ia.mjs livrable.html
node scripts/controle_ia.mjs assets/waoup-charte.css assets/gabarit-deck.html
node scripts/controle_ia.mjs --regles      # la liste des règles et leurs seuils
```

Sortie : une ligne par défaut, au format `règle · fichier:ligne · extrait`. Code de sortie 1 s'il trouve quelque chose, 0 sinon.

On corrige jusqu'à zéro. **On ne discute pas un constat du détecteur, on le corrige** : chaque règle porte un seuil chiffré et une source, et `references/sans-marqueur-ia.md` donne la contre-mesure de chacune.

Le détecteur ne lit pas les PPTX. Sur un deck, il contrôle l'HTML de référence et la charte ; le PowerPoint se contrôle à l'oeil, diapositive par diapositive.

## Format de sortie

Un fichier par livrable, nommé `AAMMJJ CLIENT - TYPE - Vn`. Le PDF et le PPTX portent le même nom, extension près. Le script reprend ce nom comme référence interne, en haut à droite de la couverture.

```
260912 ARDAN - RESTIT - V2.html
260912 ARDAN - RESTIT - V2.pdf
260912 ARDAN - RESTIT - V2.pptx
```

Le CSS voyage avec l'HTML : le fichier produit pointe sur `waoup-charte.css` dans son propre dossier. Envoyer l'HTML seul revient à envoyer un document sans mise en forme.

## Contrôle sans marqueur IA

Le critère n'est pas « c'est joli », c'est « personne ne pose la question ». Un goût ne se transmet pas, une liste se vérifie.

**Cinq marqueurs de mise en forme**, ceux que Claude produit tout seul, et ce que la charte impose à la place.

| Marqueur | Ce qu'il fait tout seul | Ce que la charte impose |
| --- | --- | --- |
| Police | Inter, Space Grotesk, ou la sans du système | Celle de la charte, et rien d'autre |
| Liseré | Une barre de 4 px à gauche des encadrés | Un cadre fin sur quatre côtés, une étiquette en tête |
| Dégradé | Un fond dégradé derrière titres et chiffres | Un aplat, un filet lime |
| Accent | Le lime remplit des blocs | Il souligne, un dixième de page au plus, et il ne porte jamais de texte |
| Pastille d'icône | Une icône arrondie au-dessus de chaque titre | Aucune icône décorative |

Cinquante-quatre marqueurs sont répertoriés, dont trois dans notre propre charte. Le détail, avec les seuils, est dans `references/sans-marqueur-ia.md`.

### Les six contrôles avant d'envoyer

1. **Le détecteur passe sans défaut.** `node scripts/controle_ia.mjs` sort zéro.
2. **Une page en niveaux de gris reste compréhensible.** Chrome, Imprimer, Couleur : Noir et blanc. Si un encadré devient indistinguable du corps, la couleur portait seule l'information.
3. **Les tableaux sont des tableaux.** On clique dans une cellule et le curseur s'y met. Si c'est une image, le livrable est mort à la première correction.
4. **Un collègue change un titre et le fichier tient.** Ouvrir le PPTX, modifier un titre, sauvegarder, rouvrir. Rien ne s'est décalé, rien n'a disparu.
5. **La police affichée est celle de la charte.** Pas une substitution. Sur un PPTX, le nom de police est rendu par le PowerPoint du destinataire : vérifier ce que le client a réellement installé.
6. **Le test d'interchangeabilité.** Remplacer le nom du client par celui d'un concurrent. **Si rien ne devient faux, le livrable est générique.** C'est le seul de ces contrôles qui porte sur le fond, et c'est le plus important : un document qui passe le détecteur à zéro et rate celui-là n'a rien à faire chez un client.

Un scan mécanique propre est un plancher, pas une preuve de qualité. Le détecteur dit ce qui est cassé, jamais que c'est bon.

## Pièges

**La charte s'applique, elle ne se corrige pas.** C'est le piège central de cette skill. Les règles de design du marché rangent le duo noir et lime parmi les cinq agrégats où le design généré se regroupe, et mettent Inter et Space Grotesk sur la liste des polices surexposées. Un modèle qui lit ces règles va vouloir « améliorer » la charte. **Le brief gagne** : là où la charte fixe une direction, on la suit exactement. Ce qui se corrige est listé dans `references/sans-marqueur-ia.md`, et rien d'autre. Trois marqueurs sont assumés et documentés ; ils restent.

**Le piège symétrique : Claude supprime le filet lime en croyant bien faire.** Sa capacité PowerPoint porte des règles anti-générique qui proscrivent nommément les barres et liserés d'accent. Le filet lime des titres de section WAOUP tombe pile dedans. Sans consigne explicite, il le retire, et il a l'air d'avoir raison. Le message de `references/vers-pptx.md` lève ce point mot pour mot ; le coller aussi dans le champ Instructions de l'add-in.

**Ne pas demander un PowerPoint directement depuis le Markdown.** Sans le modèle joint, le résultat est générique et se corrige diapositive par diapositive. C'est le piège d'origine, celui qui a fait dire « dégueulasse ».

**Ne pas régénérer tout le document pour corriger une phrase.** Corriger le Markdown, relancer la mise en forme une seule fois. Sur un PPTX déjà livré, corriger la seule diapositive concernée : c'est l'intérêt principal de l'add-in.

**Ne pas laisser Claude choisir des couleurs « proches » de la charte.** Lui donner le fichier CSS et lui interdire toute valeur hors tokens. Les tokens `--navy` et `--forest` existent pour compatibilité mais **rendent en noir** : le nom ment, ne pas les employer.

**Vérifier les polices.** Si la police de charte n'est pas embarquée, le PDF se dégrade en Arial chez le client. Dans un PPTX c'est pire : le nom de la police est rendu par le PowerPoint du destinataire, pas par la machine qui a produit le fichier.

**Cocher « Graphismes d'arrière-plan » à l'impression.** Sans cette case, la couverture noire sort blanche, les en-têtes de tableau perdent leur fond, les encadrés s'effacent. Le CSS déclare `print-color-adjust: exact` partout où il faut, mais Chrome garde le dernier mot dans sa boîte de dialogue.

**Ne pas démonter le tableau `class="grille"` du gabarit A4.** Ce n'est pas de la mise en page : c'est le seul mécanisme que Chrome répète sur chaque page **en réservant la place**. Mesuré : `position: fixed` se répète mais écrase les dernières lignes, et tout décalage négatif remonte l'élément en haut de page. Sans la grille, plus d'en-tête ni de pied courants.

**Un livrable à retravailler à quatre mains ne se partage pas en HTML brut.** Partager le Markdown source, ne diffuser l'HTML qu'en version finale. Sinon la personne qui reçoit ne peut plus rien modifier. Pour un deck, c'est le PPTX qui circule.

**Vérifier en passes bornées, pas en boucle.** Produire complètement, inspecter une fois, corriger tout d'un bloc, confirmer au plus une fois. Deux rounds au plafond. Une skill qui repasse indéfiniment sur un document finit par le lisser.

**Sur la dernière page, le pied courant se pose sous le texte** au lieu du bas de feuille. C'est le comportement de `tfoot` quand le contenu est court. Rien à corriger, sauf à vouloir remplir la page.

**Le HEX du cyan pastel n'est toujours pas confirmé.** Les valeurs marquées `[À CONFIRMER]` en tête du CSS sont des approximations assumées. Produire un livrable complet avec les seuls composants de la charte reste le meilleur moyen de fermer ce chantier.
