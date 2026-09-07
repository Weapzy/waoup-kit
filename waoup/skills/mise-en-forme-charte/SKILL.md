---
name: mise-en-forme-charte
description: Met en forme un livrable Markdown validé à la charte WAOUP : HTML chartée, PDF, ou PowerPoint fidèle au rendu HTML. Dernière étape, une seule fois.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.1"
---

# Mise en forme à la charte WAOUP

Le fond se travaille en Markdown, la forme se pose à la fin, en une passe. Un Markdown coûte dix fois moins de contexte qu'un PowerPoint et se corrige en trois secondes.

## Quand l'utiliser

Sur un Markdown dont le fond est arrêté et relu. Jamais sur un brouillon : chaque retouche de fond après mise en forme coûte une régénération complète.

## Ce que la skill fournit

| Fichier | À quoi il sert |
| --- | --- |
| `assets/waoup-charte.css` | La feuille de style. Tokens de couleur, styles de document, règles d'impression. Tient seule tant que le `waoup.css` maison n'est pas déposé. Son en-tête explique comment brancher le vrai fichier et quels tokens remplacer. |
| `assets/gabarit-livrable.html` | Le gabarit complet : couverture, sommaire, corps, tableau, verbatim, encadrés, pied de page. S'ouvre tel quel dans un navigateur. Sert de modèle à copier ou de cible d'injection. |
| `scripts/md_vers_html.py` | Convertit un Markdown en HTML chartée, en l'injectant dans le gabarit. Python 3, aucune dépendance. |
| `references/vers-pptx.md` | La recette PowerPoint, en deux voies départagées par une seule question. À lire avant tout PPTX. |

## Les trois sorties

**HTML chartée.** La sortie de référence. C'est celle que Claude réussit le mieux, parce que la charte est un CSS et que le CSS s'applique littéralement. Utiliser `assets/waoup-charte.css`, ne jamais réinventer les couleurs. Si WAOUP fournit son `waoup.css`, le charger **après** celui de la skill : il gagne sur tout ce qu'il redéfinit, et les règles d'impression restent en place.

**PDF.** Impression de l'HTML chartée. Passer par l'HTML, jamais générer un PDF directement. Le format est réglé pour A4 portrait, en-tête et pied répétés sur chaque page, couverture pleine page sans marge.

**PowerPoint.** Lire `references/vers-pptx.md` d'abord. Deux voies : l'add-in Claude for PowerPoint quand il existe un modèle de départ, sinon la chaîne Markdown → HTML validée → PPTX. Un PPTX généré sans modèle ni référence visuelle donne un rendu générique.

## Procédure

```
- [ ] 1. Vérifier que le fond est figé (aucune modification prévue)
- [ ] 2. Choisir le gabarit : document, restitution, deck
- [ ] 3. Générer l'HTML avec scripts/md_vers_html.py
- [ ] 4. Contrôler la charte (liste ci-dessous)
- [ ] 5. Exporter en PDF, ou dériver le PPTX selon references/vers-pptx.md
```

**Étape 3, la commande.**

```bash
python3 scripts/md_vers_html.py restitution.md "260906 ARDAN - RESTIT - V2.html" \
  --client "Groupe Ardan" \
  --titre "Reprendre la main sur le parc de location" \
  --date "6 septembre 2026"
```

`--confidentiel "texte"` remplace la mention par défaut, `--confidentiel ""` la retire. `--sous-titre` remplit la phrase de cadrage de la couverture. `--gabarit` vise un autre gabarit. `python3 scripts/md_vers_html.py --help` liste les syntaxes propres à la charte.

Le script lit aussi un front matter YAML simple : `client`, `titre`, `sous-titre`, `date`. Les options de ligne de commande priment.

**Ce que le script attend du Markdown.** Un seul titre de niveau 1, en tête : c'est le titre du livrable, il part sur la couverture et ne se répète pas dans le corps. Les titres de niveau 2 ouvrent les sections et fabriquent le sommaire. Sans titre de niveau 2, la page de sommaire est retirée.

Trois syntaxes en plus du Markdown courant :

```
::: cle Titre de l'encadré        encadré : cle, info, alerte, fort
contenu
:::

> La citation exacte.
> — Entretien Ardan · chef d'agence · Le Havre

| Famille | Parc |            une colonne alignée à droite
| --- | ---: |                  devient une colonne de chiffres
```

**Étape 5, le PDF.** Chrome, Imprimer, destination « Enregistrer au format PDF », marges par défaut, **case « Graphismes d'arrière-plan » cochée**. En ligne de commande :

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --no-pdf-header-footer \
  --print-to-pdf=livrable.pdf "file://$PWD/livrable.html"
```

## Contrôle de charte

- Le noir et le lime `#E2FFA6` sont la signature. Le lime accentue, il ne remplit pas des aplats entiers.
- Le lime ne borde pas non plus. Aucun onglet de couleur épais sur le côté gauche d'un bloc : c'est le marqueur visuel des documents produits à la chaîne, et il disparaît en photocopie. Un verbatim et un encadré se distinguent par un cadre fin sur les quatre côtés, une étiquette en tête, et un fond à peine teinté.
- Les tokens `--navy` et `--forest` existent encore dans le CSS pour compatibilité mais **rendent en noir**. Ne pas les employer dans un nouveau livrable.
- Les titres reprennent la hiérarchie du Markdown, sans niveau sauté.
- Un tableau reste un tableau : ne jamais le convertir en image.
- Les citations de verbatim ont leur propre style, distinct du corps de texte.
- Pied de page : client, date, mention de confidentialité si le document sort de la maison.
- Test noir et blanc : imprimer une page en niveaux de gris. Si un encadré devient indistinguable du corps, la couleur portait seule l'information.

## Format de sortie

Un fichier par livrable, nommé `AAMMJJ CLIENT - TYPE - Vn.html`. Le PDF et le PPTX portent le même nom, extension près. Le script reprend ce nom comme référence interne, en haut à droite de la couverture.

## Pièges

Ne pas demander un PowerPoint directement depuis le Markdown. Le résultat est générique et se corrige mal. Lire `references/vers-pptx.md` avant, il départage les deux voies en une question.

Ne pas régénérer tout le document pour corriger une phrase. Corriger le Markdown, puis relancer la mise en forme une seule fois.

Ne pas laisser Claude choisir des couleurs « proches » de la charte : lui donner le fichier CSS et lui interdire toute valeur hors tokens.

Un livrable qui doit être retravaillé à quatre mains ne se partage pas en HTML brut : partager le Markdown source, et ne diffuser l'HTML qu'en version finale. Sinon la personne qui reçoit ne peut plus rien modifier.

Vérifier les polices : si la police de charte n'est pas embarquée, le PDF se dégrade en Arial chez le client. Dans un PPTX, c'est pire : le nom de la police est rendu par le PowerPoint du destinataire, pas par la machine qui a produit le fichier.

Le CSS doit se trouver à côté de l'HTML. Le fichier produit pointe sur `waoup-charte.css` dans son propre dossier. Envoyer l'HTML seul revient à envoyer un document sans mise en forme. Le script le rappelle quand la sortie n'est pas dans `assets/`.

Cocher « Graphismes d'arrière-plan » à l'impression. Sans cette case, la couverture noire sort blanche, les en-têtes de tableau perdent leur fond, les encadrés s'effacent. Le CSS déclare `print-color-adjust: exact` partout où il faut, mais Chrome garde le dernier mot dans sa boîte de dialogue.

Ne pas démonter le tableau `class="grille"` du gabarit. Ce n'est pas de la mise en page : c'est le seul mécanisme que Chrome répète sur chaque page **en réservant la place**. Mesuré : `position: fixed` se répète mais écrase les dernières lignes, et tout décalage négatif ou `translateY` remonte l'élément en haut de page. Sans la grille, plus d'en-tête ni de pied courants.

Sur la dernière page, le pied courant se pose juste sous le texte au lieu du bas de feuille. C'est le comportement de `tfoot` quand le contenu est court. Rien à corriger, sauf à vouloir remplir la page.

Le sommaire prend sa page grâce à un saut posé sur le corps, pas sur lui-même. Dans une cellule de la grille, Chrome ignore un `break-after` et respecte un `break-before`.

La skill officielle `pptx` d'Anthropic porte des règles anti-générique qui proscrivent les liserés d'accent et les fonds crème. Le filet lime des titres de section WAOUP tombe dedans. Sans consigne explicite, Claude le supprimera en croyant bien faire.

Le HEX du cyan pastel n'est toujours pas confirmé, et le « test grandeur nature » de la charte n'a jamais été passé. Les valeurs marquées `[À CONFIRMER]` en tête du CSS sont des approximations assumées. Produire un livrable complet avec les seuls composants de la charte reste le meilleur moyen de fermer ce chantier.
