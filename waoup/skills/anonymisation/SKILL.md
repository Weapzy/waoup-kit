---
name: anonymisation
description: Prépare un document ou un verbatim avant partage : repère les données sensibles, propose le niveau d'anonymisation adapté au destinataire et applique le remplacement.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# Anonymisation avant partage

WAOUP fait circuler des transcripts, des briefs et des données clients. Aucune règle écrite n'existait : celle-ci en tient lieu.

## Quand l'utiliser

Avant de partager hors du cercle de la mission : un exemple en formation, un cas dans une propale, un extrait sur les réseaux, un document envoyé à un prestataire, un fichier déposé dans un espace partagé.

## Les trois niveaux

**Niveau 1, interne mission.** Rien à retirer. Le document reste entre les personnes affectées à la mission.

**Niveau 2, interne WAOUP.** Retirer les coordonnées personnelles (téléphone, mail, adresse). Garder le nom du client et les fonctions.

**Niveau 3, externe.** Remplacer le nom du client par un descripteur sectoriel (« un réseau d'agences de matériel BTP »), les noms de personnes par leur fonction (« le directeur d'agence »), arrondir ou fourchetter les montants, retirer dates précises, noms de sites, marques de concurrents cités.

Demander le niveau si le contexte ne le donne pas. En cas de doute, appliquer le niveau supérieur.

## Ce qui se retire toujours

Identifiants et mots de passe, numéros de contrat, RIB et coordonnées bancaires, données de santé, données RH nominatives, jugements de valeur sur une personne nommée, tout document marqué confidentiel par le client.

## Procédure

1. Lister ce qui a été repéré, par catégorie, avec le nombre d'occurrences.
2. Proposer la table de remplacement, et la faire valider avant application.
3. Appliquer, en gardant la cohérence : la même personne porte le même pseudonyme dans tout le document.
4. Rendre le document anonymisé **et** la table de correspondance, séparément. La table ne quitte jamais la maison.
5. Relire le résultat : un document anonymisé se relit toujours, l'automatisme rate les identifications indirectes.

## Format de sortie

Le document traité, puis la table de correspondance dans un fichier distinct nommé `CORRESPONDANCE - NE PAS PARTAGER.md`.

## Pièges

L'identification indirecte est le vrai risque. « Le directeur de l'agence de Rouen ouverte en 2019 » identifie une personne aussi sûrement que son nom.

Un verbatim anonymisé garde ses mots exacts : seule l'identité change. Réécrire la phrase pour « brouiller » la détruit.

Ne pas anonymiser un document destiné au client lui-même : il connaît ses propres données, et un document caviardé lui fait douter du sérieux du travail.

Attention aux métadonnées : nom de fichier, auteur du document, chemins visibles dans un export, en-têtes de transcription.

Cette skill ne remplace pas l'accord du client. Si un cas doit servir de référence commerciale, l'accord se demande.
