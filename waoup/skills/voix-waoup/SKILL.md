---
name: voix-waoup
description: Réécrit un texte dans la voix WAOUP et retire les tics d'écriture IA (tirets cadratins, négation-contraste, triades, mots creux). À utiliser avant tout envoi client.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.1"
---

# La voix WAOUP

Un livrable qui « sent l'IA » perd sa crédibilité avant d'être lu. Un client a déjà commenté un document WAOUP par « ah, c'est fait avec Claude » sans en regarder le fond. Cette skill est la dernière passe avant envoi.

Le repérage est confié à un script, la réécriture au modèle. Un script trouve toutes les occurrences, toujours les mêmes, sans se fatiguer. Le jugement, lui, sert à réécrire.

## Quand l'utiliser

Sur tout texte destiné à sortir de la maison : restitution, propale, défis, deck, mail client, post. Elle s'applique au **texte déjà validé sur le fond**. Elle ne réécrit pas les idées, elle réécrit la langue.

## Procédure

Travailler dans une conversation neuve, avec le seul texte à traiter. Ne pas enchaîner sur la conversation qui a produit le fond : le brouillon raté pollue la réécriture.

1. Lire le texte en entier avant de toucher une phrase.
2. Lancer le détecteur sur le fichier (voir ci-dessous). Il rend la liste des passages fautifs, ligne par ligne, catégorie par catégorie.
3. Reprendre le rapport catégorie par catégorie. Traiter les tirets et les négations-contrastes d'abord : ce sont les deux marqueurs que le lecteur reconnaît.
4. Réécrire les passages signalés, **sans changer une idée, un chiffre ni un verbatim**.
5. Lire les paires de `references/avant-apres.md` si le ton de la réécriture hésite.
6. Relire à voix haute mentalement : si une phrase ne pourrait pas être dite en réunion, elle est à refaire.
7. Relancer le détecteur sur la version corrigée. Le verdict attendu est « envoyable ».
8. Rendre le texte corrigé **plus un tableau des corrections** (avant / après / motif), pour que l'auteur garde la main.

## Le détecteur

```bash
python3 scripts/detecter_tics.py livrable.md
python3 scripts/detecter_tics.py propale.html --json
python3 scripts/detecter_tics.py note.md --liste-mots ma-liste.txt
cat livrable.md | python3 scripts/detecter_tics.py -
```

Python 3, aucune dépendance. Il lit du texte, du Markdown ou du HTML dont il retire les balises. Il ne modifie jamais le fichier.

Le rapport donne, par catégorie, le nombre d'occurrences, le numéro de ligne et l'extrait fautif. Puis une densité pour mille mots, un indice de signature et un verdict en trois états : envoyable, à retoucher, à reprendre.

Ce qu'il faut savoir lire dans le rapport :

- **Les lignes marquées `[?]`** sont des signaux à arbitrer, pas des fautes établies. Une triade de groupes parallèles peut être une énumération de faits. Un titre sans verbe peut être un intitulé de rubrique. Le script signale, il ne tranche pas.
- **Le bloc PROTÉGÉ** liste les tics repérés dans un verbatim ou une citation. Ils ne se corrigent pas. Ils sont exclus du score.
- **L'indice de signature** pondère les catégories. Le tiret cadratin et la négation-contraste comptent triple.
- **Les adverbes en -ment et les phrases de plus de 40 mots** sont des mesures d'appoint. Aucun seuil ne les condamne : ils indiquent une prose qui s'alourdit.

Options : `--json` pour une sortie machine, `--liste-mots` pour une autre liste de mots creux, `--html` pour forcer le nettoyage des balises, `--strict` pour un code de sortie 1 quand le verdict n'est pas « envoyable ».

## Les tics à éliminer

**Le tiret cadratin.** Marqueur numéro un. Remplacer par une virgule, un deux-points, ou couper la phrase.
- Avant : « La restitution — document central de la phase Décoder — structure la propale. »
- Après : « La restitution structure la propale. C'est le document central de la phase Décoder. »

**La négation-contraste.** La construction « ce n'est pas X, c'est Y », « il ne s'agit pas de X mais de Y », « non pas X, mais Y », « loin d'être X, c'est Y ». Signature reconnaissable entre toutes. Affirmer directement.
- Avant : « Il ne s'agit pas d'un problème de machine, mais d'un problème de disponibilité. »
- Après : « Le problème n'est pas la machine. Elle est en stock. C'est l'agence qui ferme à 16 h 30. »

**La triade.** Trois adjectifs, trois groupes nominaux, trois exemples, systématiquement. Garder les deux qui portent, ou un seul.
- Avant : « Une démarche claire, structurée et actionnable. »
- Après : « Une démarche actionnable. »

**Les mots creux.** « robuste », « holistique », « synergie », « écosystème », « levier » (hors sens propre), « pierre angulaire », « véritable », « il convient de », « force est de constater », « dans un monde où », « à l'ère de ». La liste complète vit dans `references/mots-creux.txt`, une expression par ligne. Supprimer, ou remplacer par le fait précis qu'ils recouvrent.

**Les chutes de paragraphe.** « En somme », « En définitive », « Au final », « In fine », « Ainsi, on peut dire que ». Un paragraphe s'arrête quand l'idée est finie.

**L'introduction de politesse.** « Voici », « Bien sûr », « Excellente question », un résumé de la demande avant de répondre. Commencer par le contenu.

**Les listes à puces qui remplacent la pensée.** Trois puces de six mots ne disent rien. Si le point mérite d'exister, il mérite une phrase avec un verbe et un fait. Le script ne voit pas ce tic : il reste à la charge du relecteur.

**Les titres-thèmes.** Un titre WAOUP est une conclusion, pas une étiquette.
- Avant : « Les enjeux de la relation client »
- Après : « Le client ne pardonne pas l'interlocuteur introuvable »

## Ce qui fait la voix WAOUP

- Le parti pris assumé. Un document WAOUP tranche. Si aucune phrase ne peut être contestée, le document ne dit rien.
- Le concret avant l'abstrait. Le chiffre, la date, le verbatim, le nom de la personne concernée.
- La phrase courte quand elle porte, la phrase longue quand elle démontre. Alterner.
- L'emphase dosée, règle 70/20/10 : sept phrases sur dix neutres, deux appuyées, une seule qui claque. Le gras et l'italique se méritent.
- Deux expressions signatures au maximum par livrable, aux moments de parti pris. Au-delà, l'effet s'inverse.
- Le vouvoiement client, le « nous » WAOUP, jamais le « on » impersonnel dans un livrable.

## Format de sortie

Le texte réécrit, puis, sous un séparateur, le tableau des corrections :

| Passage d'origine | Réécriture | Motif |
|---|---|---|

Le motif reprend le nom de catégorie du rapport, pour que l'auteur retrouve la ligne d'origine.

## Ce que la skill embarque

- `scripts/detecter_tics.py` : le détecteur. Il repère, il ne réécrit pas.
- `references/mots-creux.txt` : la liste des mots creux, éditable. Un `#` ouvre un commentaire, un `?` en tête signale une expression dont le caractère fautif dépend du sens.
- `references/avant-apres.md` : quinze paires avant / après du registre du conseil. La matière d'apprentissage du style.
- `references/evaluations.md` : cinq scénarios pour vérifier que la skill ne casse rien. À rejouer après toute modification de la skill.

## Pièges

Ne jamais réécrire un verbatim d'entretien : la parole du client se cite exactement, tics compris. C'est ce qui rend une restitution crédible. Le script les repère et les met à part, mais il ne reconnaît que les guillemets français, les guillemets droits et les lignes de citation Markdown. Un verbatim posé en texte courant, sans guillemets, lui échappe.

Ne pas lisser les aspérités du fond en croyant lisser la langue. Si une phrase est brutale parce que le constat est brutal, elle reste.

Ne pas remplacer un tiret cadratin par un tiret demi-cadratin : c'est le même marqueur, et le script attrape les deux.

Ne pas appliquer cette skill à un brouillon de travail. Sur un texte dont le fond n'est pas arrêté, elle fait perdre du temps deux fois.

Attention à la sur-correction : un texte sans aucune emphase ni respiration devient plat, et un texte plat ne signe pas WAOUP non plus.

Ne pas corriger une occurrence sans la relire dans sa phrase. Le script travaille sur des motifs, pas sur du sens. Une énumération de faits (« le client, la méthode et le résultat ») n'est pas une triade rhétorique, et le script s'en abstient déjà. Mais il signale aussi des tournures que le contexte justifie.

Ne pas prendre le verdict pour une note. Un texte à 0 occurrence peut être creux, un texte à trois occurrences peut être excellent. Le verdict mesure la surface, pas la valeur.

Sur un texte court, la densité pour mille mots s'emballe : deux tics dans un mail de cent mots donnent 20 pour mille. Lire le nombre brut d'occurrences avant l'indice.

Le script ne voit ni le parti pris manquant, ni l'emphase mal dosée, ni la puce qui remplace une idée. Ces trois-là restent à l'oeil du relecteur.

Quand une expression revient en relecture et qu'elle n'est pas dans la liste, l'ajouter à `references/mots-creux.txt`. C'est le fichier qui apprend, pas la conversation.
