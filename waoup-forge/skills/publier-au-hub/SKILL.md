---
name: publier-au-hub
description: Publie une skill au hub WAOUP pour la partager avec l'équipe, récupère celles des autres, et remonte les retours d'usage. Nécessite le connecteur hub-waoup.
compatibility: Nécessite le connecteur hub-waoup (serveur MCP) configuré avec l'adresse du hub et un jeton personnel.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# Publier au hub

Le hub est l'endroit où les skills de l'équipe se rangent. Sans lui, chacun garde les siennes sur son poste, et le travail de l'un ne profite jamais à l'autre.

## La source est le hub, pas le fichier installé

La copie d'une skill installée dans Cowork ou dans Claude Code est un fichier de plugin. Elle vient de la dernière mise à jour du kit sur la place de marché, elle sera écrasée par la suivante sans avertissement, et ce qu'on y modifie ne sort jamais du poste.

Donc, dans cet ordre : lire par `hub-waoup:lire_skill`, corriger avec la Forge en mode révision (`forger-le-kit`), publier par `hub-waoup:publier_skill`. On ne bricole pas sa copie : on publie, ou on remonte un retour.

## Quand l'utiliser

- Quand une skill fonctionne et mérite d'être partagée.
- Quand on cherche si quelqu'un a déjà outillé un besoin.
- Après un usage décevant, pour remonter ce qui a manqué.
- Au rituel hebdomadaire, pour voir ce qui a bougé.

## Publier

1. Vérifier la skill avant publication : description sous 200 caractères, aucune donnée client identifiante, pièges renseignés.
2. Appeler `hub-waoup:publier_skill` avec le nom, la description, le contenu complet du `SKILL.md`, et une note de version en une phrase (« ce qui change et pourquoi »).
3. Le hub attribue le numéro de version et horodate. Ne pas gérer les versions à la main.
4. Annoncer la publication à l'équipe, en une ligne : ce que la skill fait, et sur quel type de dossier elle a été éprouvée.

Une skill déjà présente au hub est mise à jour, pas dupliquée. Si la modification change la façon de travailler des autres, le dire dans la note de version.

### Les deux numéros

Une publication fait monter deux numéros, qui ne comptent pas la même chose.

- **La skill passe en v2** au hub. C'est le numéro de la skill, celui que renvoie `lire_skill` et qu'affiche le catalogue. Il compte les corrections apportées à ce fichier.
- **Le kit passe en 1.1.1** sur la place de marché. C'est le numéro du plugin, celui que voit Cowork. Il monte d'un cran à chaque publication, quelle que soit la skill touchée, et c'est lui qui fait apparaître le bouton Mettre à jour chez les autres.

Personne ne gère ces numéros à la main : le hub numérote la skill, le déploiement monte la version du kit.

### Ce que le hub renvoie

La réponse de `publier_skill` est le seul endroit où les deux numéros se croisent. Elle se lit telle quelle :

> Publiée : **restitution-entretien** v2 par Fanny.
> Kit WAOUP passe en 1.1.1 sur la place de marché Weapzy/waoup-kit. Le reste de l'équipe la récupère dans Cowork : Personnaliser, Plugins, place de marché waoup, Mettre à jour.
> Paquet ZIP (secours) : https://waoup.weapzy.com/paquets/waoup.zip

Trois autres réponses possibles, et chacune veut dire quelque chose :

- « Contenu identique à celui déjà sur la place de marché Weapzy/waoup-kit : rien à pousser » : le fichier envoyé est celui qui est déjà en ligne. La modification n'a pas été écrite, ou elle l'a été dans la copie installée.
- « La place de marché n'a pas pu être mise à jour (...) » : la skill est bien au hub et le paquet ZIP est à jour, mais le bouton Mettre à jour ne proposera rien. Passer par le ZIP en attendant.
- « Publication refusée : ... » : le plus souvent une description au-delà de 200 caractères. Reprendre celle de la version du hub, mot pour mot.

### Ce que fait le collègue

Rien à recevoir, rien à lire par message. De son côté : Personnaliser, Plugins, place de marché waoup, Mettre à jour. Avant d'accepter la mise à jour, il voit ce qui a changé avec `hub-waoup:comparer_versions` : les lignes ajoutées et retirées, avec les notes de version. Puis il relance son cas **dans une conversation neuve** : une conversation déjà ouverte tourne avec la version chargée à son ouverture, et il rejouerait l'ancienne skill malgré la mise à jour.

Le jeton, lui, ne circule jamais dans une conversation. Il se saisit une seule fois sur la page Connecter du hub, au moment de brancher le connecteur, et il signe ensuite les publications tout seul.

## Récupérer

- `hub-waoup:lister_skills` donne le catalogue : nom, description, auteur, version, dernière mise à jour.
- `hub-waoup:chercher_skills` cherche par mot-clé dans les descriptions et les contenus.
- `hub-waoup:lire_skill` renvoie le contenu complet d'une skill.
- `hub-waoup:comparer_versions` montre ce qui a changé entre deux versions : lignes ajoutées, lignes retirées, notes de version. À lire avant d'accepter une mise à jour du kit.
- `hub-waoup:paquet_installation` donne l'adresse du paquet à jour et les gestes d'installation pour chaque surface.

Avant d'écrire une skill, toujours chercher au hub. La moitié du travail est souvent déjà faite.

## Remonter un retour

Après un usage qui n'a pas donné ce qui était attendu, appeler `hub-waoup:remonter_retour` avec le nom de la skill, ce qui était demandé, ce qui est sorti, et ce qui manquait. Ces retours alimentent la section « Pièges » à la révision suivante.

C'est le mécanisme le plus rentable du hub : une skill s'améliore par les échecs qu'on lui rapporte, pas par les intentions de son auteur.

## Pièges

Ne pas publier une skill jamais utilisée en vrai. Le hub se remplirait de gabarits jamais éprouvés, et plus personne ne saurait lesquels valent.

Ne pas publier une skill contenant un exemple client nominatif. Passer par l'anonymisation d'abord.

Ne pas créer une variante personnelle d'une skill d'équipe sans le dire. Si la variante est meilleure, elle remplace l'originale ; si elle est spécifique, elle porte un autre nom et sa description dit en quoi elle diffère.

Le jeton du hub est personnel. Il signe les publications : ne pas le partager, ne pas le coller dans une conversation.
