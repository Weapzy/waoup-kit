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

## Récupérer

- `hub-waoup:lister_skills` donne le catalogue : nom, description, auteur, version, dernière mise à jour.
- `hub-waoup:chercher_skills` cherche par mot-clé dans les descriptions et les contenus.
- `hub-waoup:lire_skill` renvoie le contenu complet d'une skill.
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
