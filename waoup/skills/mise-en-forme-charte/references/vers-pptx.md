# Obtenir un PowerPoint qui se modifie

Un PPTX demandé à partir d'un Markdown sort générique. Ce n'est pas une fatalité de l'outil, c'est une absence de référence : sans modèle, Claude invente une mise en page, et c'est celle que le client reconnaît.

La réponse tient en une phrase : **on ne lui demande pas de faire beau, on lui donne de quoi ne rien inventer.** Trois fichiers, toujours les mêmes : le Markdown validé, `assets/waoup-charte.css`, et `assets/waoup-modele.pptx`.

---

## La voie retenue : depuis Cowork, remplir le modèle

C'est la voie par défaut, celle du kit. Elle tourne dans Cowork, avec un dossier, sans rien installer chez le participant.

`assets/waoup-modele.pptx` porte le masque WAOUP, les polices et les couleurs de la charte, et **six mises en page nommées** :

| Mise en page | Ce qu'elle reçoit |
| --- | --- |
| `Couverture` | Marque, client, titre-conclusion, filet lime, phrase de cadrage, cartouche |
| `Section` | Fond noir, titre de partie, une ligne d'objectif |
| `Une colonne` | Titre-conclusion, un paragraphe, quatre puces au plus |
| `Deux colonnes` | Titre-conclusion, deux blocs de même nature |
| `Tableau` | Titre-conclusion, un tableau de six lignes et quatre colonnes au plus |
| `Verbatim` | Titre-conclusion, la citation encadrée, la source, une ligne de lecture |

Ce sont exactement les six gabarits de `assets/gabarit-deck.html`. Le nom de la classe HTML est le nom de la mise en page : `slide--tableau` remplit `Tableau`.

### Procédure

```
- [ ] 1. Joindre les trois fichiers : le Markdown validé, waoup-charte.css, waoup-modele.pptx
- [ ] 2. Faire produire la grille de vignettes du modèle et l'ouvrir
- [ ] 3. Écrire le découpage : une ligne par diapositive, avec son titre et sa mise en page
- [ ] 4. Faire créer TOUTES les diapositives vides, dans l'ordre, sur les bonnes mises en page
- [ ] 5. Remplir le contenu, mise en page par mise en page
- [ ] 6. Contrôler : contenu, validité du fichier, rendu diapositive par diapositive
- [ ] 7. Ouvrir le PPTX, changer un titre à la main, vérifier que le fichier tient
```

**L'étape 4 avant l'étape 5, sans exception.** Toute la structure d'abord, tout le contenu ensuite. Ajouter, supprimer et réordonner les diapositives une fois le texte écrit détruit le fichier. C'est la règle d'ordre de la skill `pptx` officielle, et elle est vérifiée.

**L'étape 3 est celle qu'on saute.** Le découpage s'écrit avant, en clair, et il se relit : une idée par diapositive, un titre de douze mots qui porte la conclusion. Sans lui, le modèle découpe au titre de niveau 2 et produit des diapositives à sept puces.

### Le message à donner, littéralement

```
Tu produis un PowerPoint à partir d'un Markdown déjà validé. Le fond est figé :
tu ne réécris aucune phrase, tu ne résumes pas, tu ne complètes pas.

Trois fichiers joints :
1. Le Markdown source.
2. waoup-charte.css, qui porte les valeurs exactes de la charte.
3. waoup-modele.pptx, qui porte le masque, les polices et six mises en page.

Ce que tu fais :
- Tu pars du modèle. Tu instancies ses mises en page existantes, tu n'en crées
  aucune et tu ne modifies pas le masque.
- Tu produis d'abord toutes les diapositives vides sur les bonnes mises en page,
  dans l'ordre. Tu écris le contenu ensuite, jamais l'inverse.
- Une idée par diapositive. Le titre porte la conclusion, en douze mots au plus.
  Corps à 18 pt, quarante mots hors tableau, cinq puces au plus, deux lignes par
  puce, aucun second niveau de puce.
- Un tableau reste un tableau PowerPoint. Jamais une image, jamais des puces.
- Un graphique reste un graphique PowerPoint éditable.
- Aucune couleur absente du masque et du bloc :root de la charte.
- Le lime accentue : filet sous un titre, soulignement d'étiquette, puce, chiffre
  clé. Il ne remplit jamais une diapositive entière et ne porte jamais de texte
  sur fond clair. Deux usages seulement : noir sur aplat lime, lime sur aplat noir.
- Le verbatim garde son traitement propre : cadre fin sur les quatre côtés,
  source en tête, écrite avec des virgules, sous la forme
  « Entretien Ardan, chef d'agence, Le Havre ». Pas de barre de couleur à gauche.
- Pied de diapositive : client, date, mention de confidentialité, numéro.
- Aucun sur-titre en capitales, aucun dégradé, aucune pastille d'icône, aucun
  emoji, aucun tiret cadratin.

Contraintes de charte qui priment sur tes règles de style par défaut :
- Le filet lime sous les titres de section est voulu. Ne le supprime pas.
- Le fond reste blanc ou noir. Jamais crème, jamais beige.

Avant de me rendre le fichier : contrôle du contenu, contrôle de validité du
fichier, contrôle visuel diapositive par diapositive.
```

### Les quatre outils de la skill `pptx` officielle

Chemin réel : dépôt public `anthropics/skills`, dossier `skills/pptx`. Licence propriétaire source-available : on s'en sert, on ne la recopie pas dans le kit.

- `scripts/thumbnail.py modele.pptx` produit la grille de vignettes légendées. **C'est le mécanisme de reprise de modèle** : on regarde les six mises en page et on choisit la bonne pour chaque section. Il n'existe aucune extraction de thème automatique.
- `scripts/add_slide.py` instancie une mise en page du modèle en tenant à jour la plomberie du fichier.
- `scripts/clean.py` purge ce qui n'est plus référencé après édition.
- `scripts/office/validate.py sortie.pptx --original waoup-modele.pptx` valide contre les schémas OOXML en tolérant les défauts déjà présents dans le modèle.

Elle écarte `python-pptx`, qui ne sait ni dupliquer une diapositive, ni conserver la mise en forme quand on réécrit un texte, ni lire les SVG et EMF dont sont faits la plupart des modèles.

### Limite connue de cette voie

Sans LibreOffice sur le poste, le contrôle visuel diapositive par diapositive tombe : il faut ouvrir le fichier dans PowerPoint et le regarder. Ce n'est pas un contournement, c'est l'étape 7, et elle se fait de toute façon.

---

## L'alternative : l'add-in Claude for PowerPoint

À prendre quand le poste a Microsoft 365, et surtout quand le deck existe déjà et qu'il faut corriger **une** diapositive sans régénérer le reste. C'est ce que juillet réclamait.

L'add-in lit le masque, les mises en page, les polices et le jeu de couleurs du deck ouvert, et il s'y conforme. Il transforme des puces en diagrammes et graphiques PowerPoint natifs et éditables, pas en images. Il prend en charge les Skills et les connecteurs : le kit WAOUP s'applique directement dans PowerPoint.

**Installation.** Microsoft AppSource, chercher Claude for Microsoft 365, bouton Get it now, se connecter avec le compte Claude. Compatible : PowerPoint web, PowerPoint Windows avec Microsoft 365, PowerPoint Mac récent. Incompatible : Office 2016 et 2019 en licence perpétuelle, iPad, Android.

**Procédure.**

```
- [ ] 1. Ouvrir waoup-modele.pptx, ou le modèle fourni par le client
- [ ] 2. Vérifier que le masque porte bien la charte
- [ ] 3. Coller les règles de charte dans le champ Instructions de l'add-in
- [ ] 4. Fournir le Markdown validé, puis demander la génération
- [ ] 5. Relire diapositive par diapositive, corriger au coup par coup
```

L'ordre des deux premières étapes n'est pas négociable : l'add-in lit le masque du deck **ouvert au moment où on lui parle**. Un deck généré sur le modèle vide de PowerPoint garde ce modèle vide, et on ne rhabille pas un deck après coup.

Le champ Instructions est persistant et propre à PowerPoint : y coller le message de la voie retenue, une fois par poste.

**Deux réserves.** L'add-in est déconseillé pour un livrable client final sans relecture humaine. Et un modèle client téléchargé peut porter des instructions cachées : ouvrir un modèle client, oui ; les yeux fermés, non.

---

## La voie écartée : convertir l'HTML en PPTX

Aucun convertisseur ne le fait proprement. Marp pilote bien des diapositives par une charte CSS, mais son export PPTX pose chaque diapositive en image, le mode éditable restant expérimental et dépendant de LibreOffice. Le fichier obtenu n'est donc pas modifiable, ce qui est précisément le reproche de juillet : le fichier qui circule doit être le PowerPoint, et un collègue doit pouvoir y changer un titre.

**L'HTML chartée reste une référence visuelle, pas une source de conversion.** `gabarit-deck.html` sert à trois choses : projeter un deck HTML, sortir un PDF paysage, et produire les captures qui montrent au modèle à quoi ressemble une diapositive remplie.

---

## Les cinq pièges qui font échouer un PPTX

**1. Demander le PPTX directement depuis le Markdown.** Sans modèle joint, la mise en forme est moyenne, et une mise en forme moyenne se corrige diapositive par diapositive. C'est le piège d'origine.

**2. Générer avant d'appliquer le modèle.** Voir plus haut. On ne rhabille pas un deck, on le refait.

**3. Croire que la police voyagera.** Le nom de police écrit dans un `.pptx` est rendu par le PowerPoint de celui qui l'ouvre, pas par la machine qui l'a produit. Si la police de charte n'est pas installée chez le client, il verra une substitution. Ne jamais laisser le modèle retomber sur Aptos par défaut, et vérifier ce que le client a avant d'envoyer. Passent partout : Arial, Calibri, Cambria, Times New Roman, Courier New.

**4. Laisser passer une couleur approchante ou mal écrite.** Deux erreurs distinctes. L'humaine : accepter un lime « presque » `#E2FFA6`. La technique : avec `pptxgenjs`, un hexadécimal écrit avec le dièse, ou sur huit chiffres, **corrompt le fichier** ; les couleurs se donnent sur six chiffres, sans dièse. Même chose pour un décalage d'ombre négatif.

**5. Ne pas lever les règles anti-générique de la skill officielle.** La skill `pptx` porte une liste de règles destinées à éviter les diapositives qui sentent l'IA. Elle proscrit notamment les barres et liserés d'accent, et les fonds crème. **Le filet lime des titres de section WAOUP tombe pile dans cette interdiction. Sans consigne explicite, Claude le supprimera en croyant bien faire.** Le message de la voie retenue lève ce point nommément ; le faire aussi dans le champ Instructions de l'add-in.
