---
name: passe-critique
description: Relit un livrable WAOUP en associé exigeant et sort les faiblesses classées par gravité, avec la correction attendue. À lancer dans une conversation neuve, sur le brouillon.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# La passe critique

Le troisième réflexe WAOUP : le premier jet n'est jamais bon, et la correction se fait à froid, dans une conversation neuve, sur le seul fichier.

## Quand l'utiliser

Sur un brouillon Markdown jugé « à peu près bon », avant la mise en forme. Entrée : le fichier seul, plus le destinataire et l'objectif. Ne pas fournir l'historique de la conversation qui l'a produit.

## Posture

Relire comme l'associé référent le plus exigeant de la maison : celui qui cherche ce qui ne tient pas, pas ce qui est réussi. Aucun compliment d'ouverture, aucune reformulation du document.

## Procédure

1. Lire le document en entier.
2. Sortir **trois faiblesses majeures**, pas plus. Trois, parce qu'au-delà l'auteur ne corrige rien.
3. Pour chacune : le passage exact en cause, pourquoi ça ne tient pas devant un client, et la correction attendue formulée concrètement.
4. Ajouter la liste des **affirmations non sourcées** : toute phrase qui avance un fait, un chiffre ou un ressenti terrain sans verbatim ni source.
5. Ajouter les **angles morts** : ce que le document aurait dû traiter et ne traite pas.
6. Terminer par un verdict en une ligne : envoyable en l'état, à retoucher, ou à reprendre.

## Grille de lecture

- **Le twist existe-t-il ?** Un livrable WAOUP dit quelque chose que le client ne savait pas. Si le document se contente de restituer ce que le client a dit, il n'a pas de valeur.
- **Chaque titre est-il une conclusion ?** Un titre-étiquette signale une section qui ne tranche pas.
- **Les next steps ont-ils un porteur et une date ?** Sans porteur, ce n'est pas un next step.
- **Le document tiendrait-il si le client le contestait phrase par phrase ?**
- **Y a-t-il un endroit où le document prend un risque ?** Un livrable sans aucune phrase contestable ne dit rien.
- **Le volume est-il justifié ?** Repérer ce qui peut disparaître sans perte.

## Format de sortie

```
## Verdict
[une ligne]

## Trois faiblesses
### 1. [titre de la faiblesse]
Passage : « ... »
Pourquoi ça ne tient pas : ...
Correction attendue : ...

## Affirmations non sourcées
| Passage | Ce qui manque |

## Angles morts
```

## Pièges

Ne pas réécrire le document. Cette skill diagnostique, elle ne produit pas la version corrigée : c'est l'auteur qui arbitre.

Ne pas sortir dix faiblesses. Un rapport de dix points ne se traite pas, il se referme.

Ne pas confondre faiblesse de fond et faiblesse de langue. Les tics d'écriture relèvent de la skill de voix, et se traitent après, sur le fond validé.

Ne jamais lancer cette passe dans la conversation qui a produit le document : la relecture hérite alors de toutes les justifications déjà données et devient complaisante.
