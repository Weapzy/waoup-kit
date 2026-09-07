# Obtenir un PowerPoint correct

Un PPTX demandé à Claude à partir d'un Markdown sort générique. Ce n'est pas une fatalité de l'outil, c'est une absence de référence : sans modèle ni rendu à copier, Claude invente une mise en forme, et il l'invente mal.

Deux voies donnent un résultat tenu. Elles ne s'opposent pas, elles répondent à deux situations.

## Choisir sa voie en une question

**Existe-t-il un fichier PowerPoint de départ, modèle WAOUP ou modèle du client ?**

| Réponse | Voie | Pourquoi |
| --- | --- | --- |
| Oui | **A. Add-in Claude for PowerPoint** | Il lit le masque, les mises en page, les polices et le jeu de couleurs du deck ouvert, et il les respecte. C'est la seule voie qui garantit la charte du client. |
| Non | **B. Markdown → HTML chartée → PPTX** | L'HTML chartée sert de référence visuelle. Elle produit aussi le PDF et la version web du même livrable. |

En cas de doute, voie A. La voie B reste indispensable pour tout ce qui n'est pas une diapositive.

---

# Voie A. L'add-in Claude for PowerPoint

## Ce qu'il fait, vérifié sur la documentation officielle

Source : `https://claude.com/docs/office-agents/powerpoint`.

- Add-in Microsoft 365, en disponibilité générale sur les plans Pro, Max, Team et Enterprise.
- **Il lit le masque de diapositives, les mises en page, les polices et le jeu de couleurs du deck ouvert, et il s'y conforme.** C'est exactement ce qui manquait à WAOUP.
- Il édite une diapositive précise sans régénérer le deck entier.
- Il transforme des puces en diagrammes et en graphiques PowerPoint **natifs et éditables**, pas en images collées.
- Il prend en charge les Skills et les connecteurs. Le kit WAOUP s'applique donc directement dans PowerPoint.
- Le panneau de réglages contient un champ **Instructions**, persistant et propre à PowerPoint. C'est là que se posent les règles de charte, une fois pour toutes.

## Installation

1. Microsoft AppSource, chercher **Claude for Microsoft 365**.
2. Bouton **Get it now**.
3. Se connecter avec le compte Claude.

Versions compatibles : PowerPoint web, PowerPoint Windows avec abonnement Microsoft 365 (build 16.0.13127.20296 ou plus récent), PowerPoint Mac 16.46 ou plus récent. Ne fonctionne pas sur PowerPoint 2016 ni 2019 en licence perpétuelle, ni sur iPad, ni sur Android.

## Procédure

```
- [ ] 1. Ouvrir le modèle PowerPoint : celui de WAOUP, ou celui fourni par le client
- [ ] 2. Vérifier que le masque porte bien la charte (couleurs, polices, logo)
- [ ] 3. Coller les règles de charte dans le champ Instructions de l'add-in
- [ ] 4. Fournir le Markdown validé, puis demander la génération
- [ ] 5. Relire diapositive par diapositive, corriger au coup par coup
```

L'ordre des deux premières étapes n'est pas négociable. La documentation officielle le dit : appliquer son modèle **avant** de demander à Claude de générer. Un deck généré sur le modèle vide de PowerPoint ne se rhabille pas après coup.

## À coller dans le champ Instructions

Ce texte reste en place d'une session à l'autre. Le poser une fois par poste.

```
Charte WAOUP. Noir et lime #E2FFA6 en signature.
Le lime accentue : filet sous un titre, soulignement d'étiquette, puce, chiffre clé.
Il ne remplit jamais un fond de diapositive entier ni un tableau complet.
N'utiliser aucune couleur absente du masque du deck ouvert.
Reprendre les polices du masque. Ne jamais substituer une police.
Un tableau reste un tableau PowerPoint, jamais une image.
Un graphique reste un graphique PowerPoint éditable, jamais une image.
Les citations de verbatim gardent leur mise en forme propre, distincte du corps.
Ne pas centrer le texte en dehors des titres.
Pied de page sur chaque diapositive : client, date, mention de confidentialité.
Ne jamais régénérer le deck entier pour corriger une diapositive.
```

## Ce qu'il faut lui fournir

- Le Markdown validé, fond figé.
- Le deck ouvert sur le bon modèle.
- Le nom du client, la date, la mention de confidentialité.
- Le découpage souhaité si le Markdown ne le porte pas : une diapositive par titre de niveau 2, ou par titre de niveau 3.

---

# Voie B. Markdown → HTML chartée → PPTX

À utiliser quand il n'existe aucun modèle PowerPoint de départ, ou quand le même livrable doit sortir en PDF et en web.

## Le principe : l'HTML sert de référence, pas de source

Aucun outil ne convertit l'HTML en PPTX de façon propre. La skill officielle `pptx` d'Anthropic n'en propose d'ailleurs aucune. L'HTML chartée ne se convertit pas : **elle se montre**. Claude lit un rendu déjà validé et le reproduit, au lieu d'inventer.

## Procédure

```
- [ ] 1. Produire l'HTML avec scripts/md_vers_html.py, la contrôler à l'écran
- [ ] 2. Exporter deux ou trois captures d'écran de l'HTML : couverture, page de corps, page de tableau
- [ ] 3. Ouvrir une session avec le Markdown, les captures, et assets/waoup-charte.css
- [ ] 4. Donner le prompt ci-dessous, littéralement
- [ ] 5. Contrôler le PPTX produit : contenu, fichier, rendu visuel
```

L'étape 2 est celle qu'on saute et qui fait tout échouer. Sans image, Claude n'a rien à reproduire.

## Le prompt à donner, littéralement

```
Tu vas produire un PowerPoint à partir d'un Markdown déjà validé.
Tu ne réinventes aucune mise en forme : tu reproduis celle des captures
d'écran que je te fournis.

Ce que je te donne :
1. Le Markdown source, fond figé.
2. Des captures de l'HTML chartée déjà validée : couverture, page de corps,
   page de tableau.
3. Le fichier waoup-charte.css, qui contient les valeurs exactes.

Ce que tu fais :
- Tu reprends de l'HTML la palette, les polices, la hiérarchie des titres,
  la mise en page des tableaux, le style des citations de verbatim, la
  couverture et le pied de page.
- Tu n'emploies que les couleurs déclarées dans le bloc :root du CSS.
  Aucune couleur approchante. Aucune couleur inventée.
- Tu ignores les tokens --navy et --forest : ils rendent en noir malgré leur
  nom, ils ne sont là que pour d'anciens fichiers.
- Le lime #E2FFA6 accentue : filet sous un titre, soulignement d'étiquette,
  puce, chiffre clé. Il ne remplit jamais une diapositive entière.
- Un titre de niveau 2 du Markdown ouvre une diapositive de section.
  Un titre de niveau 3 ouvre une diapositive de contenu.
- Un tableau reste un tableau PowerPoint. Jamais une image.
- Un verbatim garde un traitement distinct du corps de texte : cadre fin sur
  les quatre côtés, étiquette de source en tête, fond légèrement teinté.
  Pas de barre de couleur épaisse sur le bord gauche.
- Pied de page sur chaque diapositive : client, date, mention de
  confidentialité.

Contraintes de la charte qui priment sur tes règles de style par défaut :
- Le filet lime sous les titres de section est voulu. Ne le supprime pas.
- Le fond reste blanc ou noir. Jamais crème, jamais beige.

Avant de me rendre le fichier, tu fais les trois contrôles de la skill pptx :
contenu, validité du fichier, rendu visuel diapositive par diapositive.
```

## Se brancher sur la skill officielle `pptx` d'Anthropic

Chemin réel dans le dépôt public : **`anthropics/skills`, dossier `skills/pptx`**. Le chemin `document-skills/pptx` que l'on voit passer n'existe pas. Licence propriétaire, source-available, pas open source : on s'en sert, on ne la recopie pas dans le kit WAOUP.

Ce qu'elle fait réellement, à connaître avant de lui parler.

| Tâche | Ce qu'elle fait |
| --- | --- |
| Créer un deck | Écrit un script Node avec la bibliothèque `pptxgenjs` |
| Partir d'un modèle, ou éditer | Dézippe le `.pptx`, édite `ppt/slides/slideN.xml`, rezippe |
| Lire un deck | `markitdown deck.pptx`, plus une grille de vignettes |

Elle écarte explicitement `python-pptx`, qui ne sait ni dupliquer une diapositive, ni conserver la mise en forme quand on réécrit un texte, ni lire les SVG et EMF dont sont faits la plupart des modèles.

Ses quatre outils, ceux qui servent à WAOUP :

- `scripts/thumbnail.py deck.pptx` produit une grille de vignettes légendées. **C'est le mécanisme de reprise de modèle** : on regarde les mises en page du modèle et on choisit visuellement la bonne pour chaque section. Il n'existe aucune extraction de thème automatique.
- `scripts/add_slide.py` duplique une diapositive existante ou instancie une mise en page du modèle, en tenant à jour toute la plomberie du fichier.
- `scripts/clean.py` purge ce qui n'est plus référencé après édition.
- `scripts/office/validate.py out.pptx --original modele.pptx` valide le fichier produit contre les schémas OOXML, en tolérant les défauts déjà présents dans le modèle source.

Règle d'ordre imposée par la skill : **tout le travail de structure avant tout travail de contenu**. Ajouter, supprimer et réordonner les diapositives d'abord. Écrire dedans ensuite. L'inverse détruit le fichier.

Contrôle qualité en trois temps, à exiger : le contenu (`markitdown`, et une recherche de `lorem`, `TODO`, `xxx`), le fichier (`validate.py`), le visuel (conversion en images via LibreOffice, puis inspection diapositive par diapositive).

Dépendances si la chaîne tourne en local : `pptxgenjs` côté npm ; `markitdown[pptx]`, `Pillow`, `defusedxml`, `lxml` côté pip ; LibreOffice et `pdftoppm` côté système.

---

# Les cinq pièges qui font échouer la conversion

**1. Demander le PPTX directement depuis le Markdown.** Sans modèle ouvert ni capture à reproduire, Claude produit une mise en forme moyenne, et une mise en forme moyenne se corrige diapositive par diapositive. C'est le piège d'origine, celui qui a fait dire « dégueulasse ». Voie A ou voie B, jamais rien entre les deux.

**2. Générer avant d'appliquer le modèle.** L'add-in lit le masque du deck **ouvert au moment où on lui parle**. Un deck généré sur le modèle vide de PowerPoint garde ce modèle vide. On ne rhabille pas un deck après coup, on le refait.

**3. Croire que la police voyagera.** Le nom de police écrit dans un `.pptx` est rendu par le PowerPoint de celui qui l'ouvre, pas par la machine qui l'a produit. Si la police de charte n'est pas installée chez le client, il verra une substitution. Deux conséquences : ne jamais laisser Claude choisir Aptos par défaut, et vérifier ce que le client a réellement avant d'envoyer. Les polices qui passent partout sont Arial, Calibri, Cambria, Times New Roman et Courier New.

**4. Laisser passer une couleur approchante ou mal écrite.** Deux erreurs distinctes. La première est humaine : accepter un lime « presque » #E2FFA6. La seconde est technique : avec `pptxgenjs`, un code hexadécimal écrit avec le `#`, ou sur huit chiffres, **corrompt le fichier**. Les couleurs se donnent sur six chiffres, sans dièse. Même chose pour un décalage d'ombre négatif, qui casse le fichier lui aussi.

**5. Ne pas lever les règles anti-générique de la skill officielle.** La skill `pptx` porte une liste de règles destinées à éviter les diapositives qui sentent l'IA. Elle proscrit notamment **les barres et liserés d'accent** et les fonds crème. Le filet lime sous les titres de section WAOUP tombe pile dans cette interdiction. Sans consigne explicite, Claude le supprimera en croyant bien faire. Le prompt de la voie B lève ce point nommément. Le faire aussi dans le champ Instructions de l'add-in.

---

# Deux limites à connaître avant de livrer

L'add-in est déconseillé pour produire un livrable client final sans relecture humaine. Il existe par ailleurs un risque d'injection de prompt par un modèle téléchargé ou un fichier externe : un deck récupéré chez un tiers peut porter des instructions cachées. Ouvrir un modèle client, oui. Le faire les yeux fermés, non.

Un PPTX ne se corrige pas en régénérant tout. Corriger le Markdown, puis reprendre la diapositive concernée. L'add-in sait éditer une diapositive seule, c'est son intérêt principal au quotidien.
