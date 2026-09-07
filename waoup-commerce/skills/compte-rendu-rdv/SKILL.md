---
name: compte-rendu-rdv
description: Transforme une note vocale ou une transcription de rendez-vous en compte rendu commercial exploitable : signaux, engagements, prochaines actions et bloc à coller au CRM.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# Compte rendu de rendez-vous

La sortie de rendez-vous se dicte en trois minutes dans la voiture. Cette skill en fait un document que l'équipe peut lire et que le CRM peut avaler.

## Quand l'utiliser

Après un rendez-vous client ou prospect, à partir d'une **transcription texte** : Nota ou un équivalent, une dictée retranscrite, ou des notes brutes.

Claude n'accepte aucun fichier audio ni vidéo à l'envoi. Les formats acceptés sont PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX et les images. La transcription se fait donc en amont, dans l'outil qui a enregistré, puis le texte se colle ici.

## Procédure

1. **Reconstituer les faits** : qui était là, fonction, date, durée, format.
2. **Extraire les signaux** : budget évoqué, échéance, décideur cité, projet concurrent, contrainte interne, réorganisation. Un signal est une information qui change la façon d'aborder la suite.
3. **Distinguer trois registres** : ce que l'interlocuteur a dit, ce qu'il a laissé entendre, ce que j'en déduis. Ne jamais mélanger.
4. **Lister les engagements pris**, des deux côtés, avec la date annoncée.
5. **Formuler les prochaines actions**, un porteur et une date par action.
6. **Produire le bloc CRM** : compact, factuel, sans interprétation, prêt à coller.

## Format de sortie

```
# [Société] · [Date] · [Interlocuteurs]

## En une ligne
[la conclusion du rendez-vous]

## Signaux
| Signal | Ce que ça change |

## Ce qui a été dit / laissé entendre / déduit
## Engagements
| Qui | Quoi | Quand |

## Prochaines actions
- [ ] action, porteur, date

---
## Bloc CRM
[8 lignes maximum, factuel, sans adjectif]
```

Le gabarit du bloc CRM, avec ses règles de remplissage, est dans [assets/bloc-crm.md](assets/bloc-crm.md).

## Pièges

Une transcription automatique confond les locuteurs et écorche les noms propres. Vérifier les noms, les montants et les dates avant diffusion.

Ne pas perdre de temps à chercher comment envoyer le fichier audio : ce n'est pas possible. C'est l'outil de transcription qui fait ce travail, Claude reprend au texte.

Ne pas transformer une hypothèse en engagement client. « Il faudrait qu'on regarde ça » n'est pas un engagement.

Le bloc CRM ne contient aucune appréciation sur la personne. Il sera lu par d'autres, et parfois exporté.

Une note vocale contient souvent des jugements dits à chaud : les retirer du compte rendu partagé, les garder pour soi.

Si le rendez-vous concerne un client existant, vérifier ce qui a déjà été promis dans la propale avant d'écrire les prochaines actions.
