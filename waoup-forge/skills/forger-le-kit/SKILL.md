---
name: forger-le-kit
description: Fabrique le kit de skills WAOUP personnalisé : mène l'entretien de cadrage, lit les documents maison, écrit les skills à la voix de l'équipe et livre un plugin partageable.
compatibility: Prévu pour Cowork (accès à un dossier de travail) ou Claude Code. En chat seul, la sortie est un jeu de fichiers à copier.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# La Forge

Fabriquer, en une séance, le kit de skills de la personne ou de l'équipe qui est en face. Le résultat est un plugin installable et partageable.

Ce n'est pas un questionnaire. C'est un entretien, mené comme WAOUP mène les siens : on part du dernier cas concret, on creuse les frictions, on ne prend jamais une opinion générale pour une donnée.

## Ce qu'il faut avant de commencer

Demander à la personne d'ouvrir ou de déposer dans le dossier de travail :
- son fichier d'instructions maison, s'il existe ;
- deux ou trois livrables qu'elle juge **réussis**, du même type ;
- un livrable **raté** ou repris à la main, si elle en a un sous la main. C'est souvent le plus instructif ;
- la charte graphique, si la mise en forme fait partie du besoin.

Si rien n'est disponible, la forge fonctionne quand même, en s'appuyant uniquement sur l'entretien. Le dire, ne pas bloquer.

## Le déroulé, en cinq temps

Suivre `references/entretien-de-forge.md` pour les questions exactes. Le résumé :

```
- [ ] 1. Cadrage : qui, quel métier, quels livrables, quelle fréquence
- [ ] 2. Le dernier cas raté : ce qui a coincé, précisément
- [ ] 3. La matière : lire les documents fournis, en tirer la structure réelle
- [ ] 4. Rédaction : écrire les skills, une par livrable
- [ ] 5. Épreuve : rejouer un vrai cas avec la skill, corriger
```

**Temps 1, cadrage.** Trois questions, pas plus. Quel est votre rôle. Quels documents produisez-vous le plus souvent. Lequel vous coûte le plus de temps aujourd'hui.

**Temps 2, le dernier cas raté.** La question qui ouvre tout : « racontez-moi la dernière fois où le résultat n'était pas bon ». Creuser jusqu'à obtenir la cause exacte : brief trop court, structure absente, ton à côté, chiffres perdus, mise en forme. Chaque cause devient une section de la skill.

**Temps 3, la matière.** Lire les livrables réussis. En extraire la structure réellement employée, pas celle qui est déclarée. Nommer les sections avec les mots de la maison. Relever les tournures récurrentes, les formats de titre, les conventions de nommage de fichiers.

Poser la question de contrôle : « dans ce document, qu'est-ce qui est du WAOUP et qu'est-ce qui est de la circonstance ? »

**Temps 4, rédaction.** Une skill par livrable, jamais une skill par micro-tâche. Suivre `references/anatomie-skill.md`. Réutiliser les skills du catalogue (`references/catalogue-kit.md`) comme base quand elles couvrent le besoin, et les personnaliser : structures, exemples, vocabulaire, pièges rencontrés par la personne.

**Temps 5, épreuve.** Prendre un vrai cas récent de la personne, le passer dans la skill fraîchement écrite, comparer au livrable qu'elle avait produit à la main. Lui demander ce qui manque. Corriger la skill, pas le résultat. Recommencer une fois.

## Ce que la forge produit

Un dossier de plugin complet :

```
<nom-du-kit>/
├── .claude-plugin/plugin.json
├── skills/
│   └── <une-skill-par-livrable>/SKILL.md
├── assets/            (charte, gabarits, exemples autorisés)
└── README.md          (ce que contient le kit, comment l'installer)
```

Les descriptions de skills font **200 caractères au maximum** : c'est la limite de claude.ai, et une skill qui dépasse ne s'installe pas partout.

Le nom du plugin est en minuscules avec tirets. Le nom de chaque dossier de skill est identique au champ `name` de son `SKILL.md`.

## Enchaîner

Une fois le kit produit et éprouvé :
1. publier les skills au hub d'équipe, avec la skill `publier-au-hub` ;
2. livrer le paquet et retirer la forge, avec la skill `passer-le-relais`.

## Pièges

Ne pas écrire les skills avant d'avoir lu au moins un livrable réussi. Une skill écrite sur une description orale produit un document générique, et la personne le sent immédiatement.

Ne pas remplir la skill de ce que Claude sait déjà. Ce qui compte, c'est ce qui est propre à la maison : la structure, le vocabulaire, les chiffres de référence, les interdits.

Ne pas faire une skill par variante de ton ou par étape. Un livrable, une skill. Les variantes se traitent par un paramètre dans la procédure.

Ne pas recopier un fichier d'instructions de 400 lignes dans une skill. Le découper : ce qui est vrai partout va dans les instructions du dossier de travail, ce qui sert un livrable va dans sa skill.

Ne jamais mettre de données client identifiantes dans les exemples d'une skill destinée à être partagée. Anonymiser avant.

La section « Pièges » de chaque skill produite est la plus précieuse. La remplir avec les échecs réels racontés au temps 2, pas avec des précautions générales.
