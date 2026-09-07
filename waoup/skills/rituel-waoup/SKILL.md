---
name: rituel-waoup
description: Anime le rituel hebdomadaire WAOUP : va chercher l'ordre du jour préparé par le hub, mène les quinze minutes, écrit les corrections décidées et ferme les retours traités.
compatibility: Nécessite le connecteur hub-waoup pour l'ordre du jour. Sans lui, la skill mène le rituel à partir de ce que l'équipe apporte.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# Le rituel du lundi

Quinze minutes par semaine. C'est le seul mécanisme qui empêche le kit de mourir, et le premier que les équipes abandonnent. Cette skill le rend impossible à préparer : l'ordre du jour arrive tout fait.

## Quand l'utiliser

Au créneau hebdomadaire, animé par le gardien de la cohérence. Aussi quand quelqu'un demande « où on en est du kit » ou « qu'est-ce qui a bougé cette semaine ».

## Procédure

```
- [ ] 1. Récupérer l'ordre du jour
- [ ] 2. Lire l'alerte à voix haute
- [ ] 3. Traiter les points dans l'ordre, montre en main
- [ ] 4. Écrire les corrections dans les skills, tout de suite
- [ ] 5. Fermer les retours traités
- [ ] 6. Sortir avec une ligne de backlog
```

**1. L'ordre du jour.** Appeler `hub-waoup:ordre_du_jour`. Il renvoie les points, minutés, dans l'ordre où ils comptent, plus les identifiants des retours en attente. Ne pas réordonner : le hub met en tête ce qui souffre.

**2. L'alerte.** La première phrase dit l'état du système. Si elle dit que rien n'a bougé, c'est le sujet de la réunion, pas les skills. Une semaine sans retour signifie que personne ne remonte ce qui rate, pas que tout marche.

**3. Les points.** Chaque point porte sa durée et sa décision attendue. Tenir les minutes. Ce qui déborde part au backlog, avec un porteur et une date.

**4. Les corrections.** Une correction décidée s'écrit pendant la réunion, jamais après. Ouvrir la skill, ajouter la ligne dans la procédure ou dans les pièges, publier. Une correction reportée est une correction perdue.

**5. Fermer les retours.** Pour chaque retour traité, appeler `hub-waoup:traiter_retour` avec son identifiant et la suite donnée en une phrase. Un retour classé sans suite se ferme aussi, avec le motif : c'est une décision, pas un oubli.

**6. Le backlog.** Une seule ligne : la skill à créer, qui la porte, pour quand.

## Format de sortie

Un compte rendu de dix lignes maximum, à coller dans le canal de l'équipe :

```
Rituel du [date] · [durée réelle]

Corrigé      [skill] : [ce qui a changé]
Fermé        [n] retour(s)
Publié       [skill] v[n] par [prénom]
Backlog      [skill à créer] · [porteur] · [échéance]
À surveiller [ce qui n'a pas été traité et pourquoi]
```

## Pièges

Ne pas transformer le rituel en revue de projet. Quinze minutes, sur le kit uniquement. Les sujets de mission se traitent ailleurs.

Ne pas préparer l'ordre du jour à la main. Le hub le fait, et c'est précisément ce qui rend le rituel tenable dans la durée.

Ne pas laisser un retour ouvert plus de deux rituels. Au troisième, soit on corrige, soit on ferme avec le motif. Une liste qui s'allonge décourage ceux qui remontent.

Une skill qui dort depuis un mois, sans retour et sans version 2, n'est pas parfaite : elle est inutilisée. Trancher plutôt que la laisser encombrer le catalogue.

Si le hub est injoignable, mener le rituel quand même, avec ce que chacun apporte. Un rituel tenu sans outil vaut mieux qu'un rituel annulé pour cause d'outil.
