---
name: restitution-entretien
description: Transforme le verbatim ou les notes d'un entretien client en restitution WAOUP actionnable, organisée par enjeu, avec verbatims exacts et angles morts. Phase Décoder.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# Restitution d'entretien

Le document qui transforme une heure de parole client en matière à décision. Il alimente directement la propale.

## Quand l'utiliser

Juste après un entretien, ou après une série d'entretiens sur une même mission. Entrée : le verbatim brut, la transcription, ou les notes prises à la volée. Une restitution n'est pas un compte rendu : elle trie.

## Ce qu'il faut savoir avant de commencer

Trois questions à poser à l'utilisateur si l'information manque. Ne pas inventer les réponses.

1. **Destinataire.** L'associé référent, l'équipe, ou le client lui-même. Le tri et le ton changent du tout au tout.
2. **Nombre d'entretiens couverts** et profils des interviewés (fonction, ancienneté, site).
3. **Ce que la restitution doit permettre de décider.** Cadrer la propale ? Trancher une hypothèse ? Préparer un atelier ?

## Procédure

```
- [ ] 1. Lire l'intégralité du verbatim avant de structurer
- [ ] 2. Repérer les insights qui CHANGENT une décision
- [ ] 3. Regrouper par enjeu (3 à 5), jamais par interviewé
- [ ] 4. Trier faits / interprétations / hypothèses à valider
- [ ] 5. Rédiger les 6 blocs
- [ ] 6. Écrire « ce que la restitution ne dit pas »
- [ ] 7. Vérifier chaque verbatim mot pour mot contre la source
```

**Étape 2, le critère de tri.** Garder ce qui change une décision : un chiffre, une contrainte, une opposition interne, un renoncement, une phrase qui dit un choix. Écarter le small talk, les généralités sectorielles, ce qui confirme ce qu'on savait déjà.

La grille complète, avec les six signaux à relever systématiquement et la façon de nommer un enjeu, est dans [references/grille-de-tri.md](references/grille-de-tri.md).

**Étape 3, l'organisation par enjeu.** Un enjeu se nomme par une conclusion, pas par un thème. « La caution bloque les petits artisans », pas « La question financière ». Pour chaque enjeu, trois colonnes : problèmes rencontrés, solutions envisagées par le terrain, verbatims exacts.

**Étape 5, la contrainte de volume.** Cinq enjeux maximum, cinq insights maximum par restitution. La contrainte force le choix : c'est elle qui produit la hiérarchie.

**Étape 6, les angles morts.** Une section finale « ce que la restitution ne dit pas » : les chiffres qu'il aurait fallu mesurer, les questions non posées, les profils manquants. C'est ce bloc qui prépare l'entretien suivant et démontre la rigueur au client.

## Format de sortie

Un fichier Markdown, titré « Restitution, [client], [date] », en six blocs :

1. **Cadrage** : la mission, la question posée, le périmètre de cette vague d'entretiens.
2. **Méthodologie et profils** : combien d'entretiens, quels profils, quelle durée, quelle date.
3. **Feedback global sur les entretiens** : la tonalité générale, ce qui a surpris, la qualité de l'accueil. Signature WAOUP, souvent oubliée.
4. **Synthèse par enjeu** : 3 à 5 enjeux, chacun en trois colonnes.
5. **Retours sur la solution** : ce que le terrain dit de la piste envisagée, adhésions et résistances nommées.
6. **Notre analyse et next steps** : le twist, puis les prochaines actions avec un porteur par action.

Puis la section « Ce que la restitution ne dit pas ».

Le gabarit littéral à reproduire, avec les volumes de référence par bloc, est dans [references/gabarit-sortie.md](references/gabarit-sortie.md).

Sortir en Markdown. La mise en forme chartée vient après, en une seule passe, avec la skill de mise en forme.

## Pièges

Ne pas paraphraser l'entretien. Une restitution qui suit l'ordre chronologique de la conversation est un compte rendu, pas une restitution.

Les verbatims se citent **exactement**, hésitations comprises. Un verbatim lissé perd sa force et devient contestable.

Ne jamais fusionner deux interviewés dans un même verbatim, même pour la clarté.

Séparer explicitement ce qui est dit (fait), ce qu'on en déduit (interprétation), et ce qui reste à vérifier (hypothèse). Le mélange des trois est le défaut le plus fréquent et le plus coûteux en réunion client.

Le bloc 3 est presque toujours sauté. Il ne doit pas l'être.

Si le verbatim contient des noms de personnes, des montants, ou des informations sensibles, passer par la skill d'anonymisation avant tout partage hors équipe.
