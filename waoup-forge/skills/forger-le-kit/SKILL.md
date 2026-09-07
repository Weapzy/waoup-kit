---
name: forger-le-kit
description: Fabrique le kit de skills WAOUP personnalisé et révise les skills existantes : mène l'entretien, lit les documents maison, corrige une skill du hub sans la réécrire, livre un plugin partageable.
compatibility: Prévu pour Cowork (accès à un dossier de travail) ou Claude Code. En chat seul, la sortie est un jeu de fichiers à copier.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# La Forge

Fabriquer, en une séance, le kit de skills de la personne ou de l'équipe qui est en face. Le résultat est un plugin installable et partageable.

Ce n'est pas un questionnaire. C'est un entretien, mené comme WAOUP mène les siens : on part du dernier cas concret, on creuse les frictions, on ne prend jamais une opinion générale pour une donnée.

Deux modes, et il faut savoir lequel on ouvre. **Forger** : un kit entier, par l'entretien en cinq temps. **Réviser** : une skill déjà publiée, corrigée d'une à trois lignes à partir d'un défaut constaté. Le second est celui qui sert toutes les semaines.

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

## Réviser une skill existante

Le mode révision ne fabrique rien : il corrige une skill déjà publiée, sans la refaire. Une skill n'est pas un livrable qu'on rend, c'est un actif qui se corrige.

**Entrée.** Un retour du hub (`hub-waoup:journal`, `hub-waoup:ordre_du_jour`) ou un constat de passe critique : un défaut réel, daté, avec le texte fautif sous les yeux. Sans défaut nommé, il n'y a rien à réviser.

```
- [ ] 1. Lire la version courante par lire_skill
- [ ] 2. Proposer un diff d'une à trois lignes
- [ ] 3. Montrer le diff avant d'écrire
- [ ] 4. Rejouer le cas dans une conversation neuve
- [ ] 5. Préparer la note de version, en une phrase
- [ ] 6. Publier sur accord explicite
```

Les messages exacts, les gabarits et les points de rupture sont dans `references/reviser-une-skill.md`.

**1. Lire la version courante.** `hub-waoup:lire_skill` sur le nom de la skill. Jamais le fichier installé sur le disque : la copie présente dans Cowork ou dans Claude Code est un fichier de plugin, écrite par la dernière mise à jour de la place de marché et écrasée par la suivante ; ce qu'on y modifie ne sort pas du poste. La source est le hub. Relever le numéro de version et la section Pièges telle quelle.

**2. Proposer un diff d'une à trois lignes.** Une ligne de procédure au plus, une ligne de Pièges au plus. La ligne de Pièges nomme l'échec réel et daté, la ligne de procédure donne le geste qui l'évite. Si le défaut demande davantage, c'est qu'il en cache plusieurs : les traiter un par un, une révision chacun.

**3. Montrer avant d'écrire.** Afficher les lignes ajoutées et l'endroit exact où elles s'insèrent, puis attendre. Écrire d'abord et montrer ensuite retire à la personne la seule décision qui lui revient.

**4. Rejouer le cas.** Conversation neuve, même matière, même demande qu'au moment du défaut. Le défaut a disparu, le reste du livrable tient. Sans cette étape, on a modifié un fichier, pas corrigé un défaut.

**5. La note de version.** Une phrase, au présent, qui énonce la règle nouvelle et non le travail fait. Elle est ce que lira le collègue qui reçoit la mise à jour.

**6. Publier.** Avec la skill `publier-au-hub`, sur accord explicite de la personne. Une fois publiée, relire le diff tel que le hub l'a enregistré avec `hub-waoup:comparer_versions` : c'est exactement ce que le collègue verra arriver.

**Ce que la révision ne fait pas.**
- Réécrire la skill. La reformuler entière fait perdre des passages qui marchaient, exactement le reproche adressé aux corrections de prompt.
- Renommer la skill ou son dossier. Le nom relie le hub, le kit et les conversations en cours.
- Toucher à la description. C'est elle qui décide du déclenchement, et `publier_skill` refuse une description de plus de 200 caractères.
- Créer une skill de plus. Un défaut de skill se corrige dans cette skill.
- Publier sans accord explicite.
- Désinstaller quoi que ce soit.

## Enchaîner

Une fois le kit produit et éprouvé :
1. publier les skills au hub d'équipe, avec la skill `publier-au-hub` ;
2. livrer le paquet et poser la fiche de reprise, avec la skill `passer-le-relais`.

## Pièges

Ne pas écrire les skills avant d'avoir lu au moins un livrable réussi. Une skill écrite sur une description orale produit un document générique, et la personne le sent immédiatement.

Ne pas remplir la skill de ce que Claude sait déjà. Ce qui compte, c'est ce qui est propre à la maison : la structure, le vocabulaire, les chiffres de référence, les interdits.

Ne pas faire une skill par variante de ton ou par étape. Un livrable, une skill. Les variantes se traitent par un paramètre dans la procédure.

Ne pas recopier un fichier d'instructions de 400 lignes dans une skill. Le découper : ce qui est vrai partout va dans les instructions du dossier de travail, ce qui sert un livrable va dans sa skill.

Ne jamais mettre de données client identifiantes dans les exemples d'une skill destinée à être partagée. Anonymiser avant.

La section « Pièges » de chaque skill produite est la plus précieuse. La remplir avec les échecs réels racontés au temps 2, pas avec des précautions générales.
