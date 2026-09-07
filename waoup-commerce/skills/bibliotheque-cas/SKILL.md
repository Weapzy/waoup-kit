---
name: bibliotheque-cas
description: Tient la bibliothèque de cas clients WAOUP : ajoute un cas depuis un livrable, trouve celui qui parlera à un interlocuteur, signale les fiches périmées et les trous par secteur.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# La bibliothèque de cas

Un cas raconté cinquante fois se déforme cinquante fois. La bibliothèque garde la matière
stable et laisse la narration varier.

## Quand l'utiliser

Quatre situations, quatre sorties.

| Situation | Entrée | Sortie |
|---|---|---|
| Une mission vient de se terminer | propale, restitution, synthèse de marathon | une fiche de cas remplie |
| Un rendez-vous se prépare | secteur, fonction, problème de l'interlocuteur | trois cas classés, avec l'angle et l'accroche |
| Trimestre écoulé | la bibliothèque | la liste des fiches à revérifier ou à déclasser |
| La bibliothèque semble incomplète | les fiches et les comptes rendus de rendez-vous | la carte des trous et les trois à combler |

Pour raconter le cas une fois choisi, c'est la skill `business-case` qui prend le relais.

## Ce qu'il faut avant de commencer

**Où vit la bibliothèque.** Un dossier partagé, un fichier par cas, et rien d'autre
dedans.

```
Bibliothèque de cas/
├── sommaire.md                        une ligne par cas
├── 2024 DELMONT - fiche cas.md
├── 2023 HABOUEST - fiche cas.md
└── accords/                           les accords de citation, un par cas
```

Le nom du fichier commence par l'année de fin de mission, pour que le tri alphabétique
donne l'ordre chronologique.

**Pour ajouter un cas**, il faut la restitution. Sans elle, pas de verbatims et pas de
twist : la fiche sera une plaquette. Si elle manque, la réclamer avant de commencer.

**Pour chercher un cas**, il faut la fonction de l'interlocuteur et le problème qu'il
cherche à résoudre. Le nom de sa société ne suffit pas. Si le problème n'est pas connu,
le dire et proposer trois hypothèses plutôt que de sortir un cas au hasard.

**Les deux fichiers de référence.** Le gabarit de fiche est dans
[assets/gabarit-fiche-cas.md](assets/gabarit-fiche-cas.md). Les listes fermées de
problèmes, de secteurs et de fonctions sont dans
[references/taxonomie-cas.md](references/taxonomie-cas.md). Elles ne s'inventent pas au
fil de l'eau.

Trois fiches d'exemple montrent le niveau attendu :
[marque agroalimentaire](assets/exemple-fiche-marque-agroalimentaire.md),
[réseau d'agences](assets/exemple-fiche-reseau-agences.md),
[promotion immobilière](assets/exemple-fiche-promotion-immobiliere.md). Leurs chiffres
sont inventés. Elles se lisent, elles ne se citent pas.

## Procédure

Quatre procédures indépendantes. Repérer laquelle s'applique, recopier sa liste, la suivre
dans l'ordre.

### A. Ajouter un cas depuis un livrable existant

- [ ] 1. Réunir la matière : propale, restitution, synthèse de marathon, compte rendu de clôture. Si la restitution manque, s'arrêter et la demander.
- [ ] 2. Copier le gabarit dans un fichier `AAAA CLIENT - fiche cas.md`.
- [ ] 3. Remplir la carte d'identité. Le problème et le secteur se choisissent dans les listes fermées, jamais formulés librement.
- [ ] 4. Remplir les faits en recopiant. Ne pas reformuler, ne pas lisser les verbatims, ne pas ajouter d'adjectif.
- [ ] 5. Extraire les chiffres un par un, avec source, périmètre, date et niveau de solidité. Un chiffre lu dans une propale est un objectif annoncé : il est déclaratif tant que sa mesure n'a pas été retrouvée.
- [ ] 6. Remplir les droits. Sans accord écrit retrouvé dans le dossier, le cas est en N3 sectoriel.
- [ ] 7. Écrire les six angles. Chaque accroche doit s'appuyer sur un fait du bloc 2 et un chiffre du bloc 3. Un angle sans preuve reste dans la fiche, marqué « sans preuve, ne pas utiliser ».
- [ ] 8. Remplir la table des interlocuteurs. Laisser vides les fonctions à qui ce cas ne parle pas.
- [ ] 9. Lire chaque accroche à voix haute. Une accroche qui ne passe pas à l'oral se réécrit tout de suite.
- [ ] 10. Réclamer à l'équipe de mission l'obstacle et le twist s'ils manquent. Ce sont les deux seuls éléments qu'aucun livrable ne contient.
- [ ] 11. Ajouter la ligne au sommaire et la ligne de création au journal de la fiche.

Écrire la fiche dans les deux semaines qui suivent la clôture. Pendant la mission, on ne
sait pas encore ce qui en est sorti. Six mois après, l'obstacle a disparu de la mémoire de
tout le monde.

### B. Chercher le cas d'un interlocuteur

1. Qualifier : société, secteur, taille, fonction de l'interlocuteur, ce qu'il cherche à résoudre, ce qu'il craint.
2. Traduire le besoin en un problème de la liste fermée. Si le besoin en couvre deux, retenir celui que l'interlocuteur a formulé en premier.
3. Filtrer sur le problème. Le secteur ne sert qu'à départager deux cas déjà retenus.
4. Écarter les cas dont le client est concurrent direct du prospect, en lisant le bloc 9 de chaque fiche.
5. Écarter les cas dont l'angle correspondant à cette fonction est vide ou marqué « sans preuve ».
6. Vérifier les droits et l'âge. Un cas ancien peut sortir, à condition d'annoncer sa date.
7. Sortir trois cas classés, avec pour chacun l'angle, l'accroche, le chiffre et le niveau de citation.
8. Si aucun cas ne sort, le dire. Proposer le cas le plus proche en annonçant l'écart, ou ne raconter aucun cas. Ne jamais fabriquer un cas ni transposer un chiffre d'une fiche à l'autre.

### C. Passer la bibliothèque en revue

Une fois par trimestre, quinze minutes. Sept règles, appliquées fiche par fiche.

| Constat | Ce qu'on fait |
|---|---|
| Fiche non vérifiée depuis 12 mois | statut « à revérifier » |
| Mission terminée depuis plus de 3 ans | la fiche reste utilisable, son âge s'annonce en la racontant |
| Accord de citation expiré, sans date, ou donné oralement | retour en N3 sectoriel |
| Personne qui a donné l'accord partie de l'entreprise | retour en N3, accord à reconfirmer auprès du successeur |
| Chiffre dont l'exercice a plus de 3 ans | l'exercice s'annonce à chaque fois qu'on cite le chiffre |
| Client racheté, renommé, ou en procédure collective | vérifier avant toute citation, avec les sources de `panorama-entreprise` |
| Interlocuteur cité parti de l'entreprise | le verbatim reste valable, la référence commerciale non |

Puis : mettre à jour le statut et la date, écrire la ligne au journal, sortir la liste des
actions à mener.

Poser une alerte BODACC sur les clients de la bibliothèque prend dix minutes et fait la
moitié de cette revue toute seule.

### D. Dresser la carte des trous

1. Compter les fiches par croisement secteur et problème, dans le tableau de `references/taxonomie-cas.md`.
2. Relire les comptes rendus de rendez-vous des six derniers mois et relever, pour chacun, le secteur et le problème.
3. Croiser. Un croisement demandé au moins deux fois en six mois et sans aucune fiche est un trou. Une case vide jamais demandée n'est pas un trou.
4. Séparer les trous de secteur, comblables par un cas du même problème dans un autre secteur, et les trous de problème, qui ne se comblent pas.
5. Pour chaque trou de problème, chercher dans « Livrables réussis » une mission close et jamais transformée en fiche.
6. Sortir la carte, les trois trous prioritaires, et une action par trou.

## Format de sortie

**Recherche de cas** (procédure B)

```
# Trois cas pour [Nom, fonction] · [Société] · [date du rendez-vous]

Problème retenu : [code du problème] · Secteur : [code] · Droits utilisables : [N1, N2, N3]

## 1. [Code du cas] · [nom sectoriel ou nom réel selon droits]
Angle : [A_] · Format conseillé : [30 secondes, 3 minutes, page écrite]
Accroche : « [mot pour mot] »
Chiffre : [valeur, source, solidité]
Citation : [N1, N2, N3] · [ce qu'on peut dire, ce qu'on ne peut pas]
Pourquoi celui-là : [une ligne]

## 2. [idem]
## 3. [idem]

## Ce que je n'ai pas
[Le trou, s'il y en a un. Le cas manquant. Ce qu'il ne faut pas promettre.]
```

**Revue de péremption** (procédure C)

```
# Revue de la bibliothèque · [date]

| Cas | Statut | Ce qui a changé | Action | Pour quand |
|---|---|---|---|---|

Fiches saines : [n] · À revérifier : [n] · Déclassées en N3 : [n] · Périmées : [n]
```

**Carte des trous** (procédure D)

```
# Carte des trous · [date]

[Le tableau secteur par problème, avec le nombre de fiches par case.]

## Les trois trous à combler
1. [secteur] × [problème] : demandé [n] fois en six mois, aucune fiche.
   Action : [écrire la fiche depuis tel livrable, ou assumer le cas voisin X].
2.
3.

## Les cases vides sans enjeu
[Les croisements jamais demandés. Ne rien y faire.]
```

**Ligne de sommaire**

```
| Code | Client | Secteur | Problème | Année | Droits | Statut | Angles utilisables |
```

## Pièges

Un chiffre lu dans une propale est une promesse, pas un résultat. La moitié des chiffres
qui circulent dans les cas commerciaux sont des objectifs annoncés au démarrage et jamais
mesurés. Retrouver la mesure, ou classer le chiffre en déclaratif.

Le secteur attire, le problème sélectionne. Trier par secteur donne des cas qui rassurent
en réunion interne et qui ne prouvent rien devant le client.

Une fiche sans obstacle n'est pas finie. Aucune mission ne s'est passée sans accroc. Si
l'obstacle manque, c'est qu'il n'a pas été demandé à l'équipe de mission, pas qu'il
n'existe pas.

Le niveau de citation ne se déduit pas de la qualité de la relation. Un client très content
qui n'a jamais rien signé reste en N3.

Ne jamais remplir une case par déduction. « Ils ont dû gagner du temps » devient un fait
en deux lectures et un chiffre en trois.

Quinze fiches justes valent mieux que quarante approximatives. Une seule ligne fausse dite
en rendez-vous coûte plus cher que dix cas manquants.

Le dossier « Livrables réussis » est classé par taux d'intervention humaine. Il ne permet
pas de retrouver un cas. La bibliothèque se range par cas, jamais par livrable, et les deux
dossiers vivent séparément.

La bibliothèque ne remplace pas l'équipe. Elle remplace la question posée la veille au
soir. Les questions qui restent à poser deviennent plus précises, et les réponses arrivent
plus vite.

Avant de sortir une fiche du dossier partagé, la passer par `anonymisation` si elle
contient des noms de personnes autres que les signataires d'accords.
