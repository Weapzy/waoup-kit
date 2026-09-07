# Anatomie d'une skill

## Contenu
- Le fichier et son emplacement
- L'en-tête
- Le corps
- Le dosage
- Contrôles avant livraison

## Le fichier et son emplacement

Une skill est un dossier contenant un `SKILL.md`. Le nom du dossier est identique au champ `name`.

```
ma-skill/
├── SKILL.md          obligatoire
├── references/       lu à la demande, pour le détail
├── assets/           gabarits, chartes, exemples
└── scripts/          code exécutable, si nécessaire
```

Dans un plugin, les skills vivent dans `skills/`.

## L'en-tête

```yaml
---
name: restitution-entretien
description: Transforme le verbatim d'un entretien client en restitution WAOUP actionnable, organisée par enjeu, avec verbatims exacts et angles morts.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Prénom
  version: "1.0"
---
```

`name` : minuscules, chiffres et tirets, 64 caractères au plus, jamais deux tirets d'affilée, ni « claude » ni « anthropic ».

`description` : **200 caractères au maximum** pour rester installable sur claude.ai. C'est le seul texte lu en permanence par le modèle : il décide du déclenchement. Il doit dire **ce que la skill fait** et **quand l'utiliser**, à la troisième personne.

- Bon : « Transforme le verbatim d'un entretien client en restitution WAOUP actionnable, organisée par enjeu, avec verbatims exacts. »
- Mauvais : « Aide pour les entretiens. » Rien ne déclenche.
- Mauvais : « Je peux vous aider à rédiger vos restitutions. » Première personne, déclenchement instable.

## Le corps

Cinq sections, dans cet ordre :

1. **Quand l'utiliser.** La situation, la matière d'entrée, le livrable de sortie.
2. **Ce qu'il faut avant de commencer.** Les informations à réclamer si elles manquent. Une skill qui suppose invente.
3. **Procédure.** Numérotée. Pour une tâche en plus de quatre étapes, ouvrir par une liste à cocher que le modèle recopie et suit.
4. **Format de sortie.** Le gabarit, littéralement. C'est ce qui fait la constance d'un document à l'autre.
5. **Pièges.** La section la plus précieuse, et la seule qui ne peut pas être devinée. Elle se remplit avec les échecs réellement rencontrés.

## Le dosage

Rester sous 500 lignes. Au-delà, découper : le détail part dans `references/`, appelé depuis `SKILL.md` par un lien d'un seul niveau de profondeur.

N'écrire que ce que le modèle ne sait pas déjà. Expliquer ce qu'est une proposition commerciale est du gaspillage ; dire que la propale WAOUP ouvre sur l'enjeu reformulé et jamais sur la présentation de l'agence, c'est de l'information.

Doser la liberté selon la fragilité de la tâche :
- structure imposée à la lettre quand la constance prime (gabarits de livrables, formats CRM) ;
- canevas adaptable quand le contexte décide (analyse, critique, priorisation).

## Contrôles avant livraison

- [ ] `name` conforme et identique au nom du dossier
- [ ] `description` sous 200 caractères, à la troisième personne, avec le déclencheur
- [ ] corps sous 500 lignes
- [ ] format de sortie donné littéralement
- [ ] au moins trois pièges, tirés de cas réels
- [ ] aucune donnée client identifiante
- [ ] aucune information périssable en dur (chiffres de crédibilité, dates, versions d'outil)
- [ ] testée sur un vrai dossier, dans une conversation neuve
