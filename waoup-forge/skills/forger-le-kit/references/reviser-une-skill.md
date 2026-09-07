# Réviser une skill existante

## Contenu
- Les messages, dans l'ordre
- La ligne de Pièges, gabarit
- La ligne de procédure
- La note de version
- Les points de rupture

## Les messages, dans l'ordre

**Tracer le retour**, quand le défaut vient d'être constaté et n'est pas encore au hub :

> Remonte au hub WAOUP un retour sur restitution-entretien v1.
> Demandé : la restitution de l'entretien Ardan pour l'associé référent.
> Ce qui n'a pas marché : un chiffre non mesuré est passé en titre d'enjeu, et le périmètre a changé entre la source (« de mes appels ») et le titre (« des appels »).
> Ce que j'attendais : aucun titre d'enjeu ne porte un chiffre que personne n'a mesuré.
> N'ajoute ni transcription, ni nom de client.

**Ouvrir la version du hub**, pas celle du disque :

> Avec le connecteur Hub WAOUP, lis la fiche complète de restitution-entretien. Donne-moi son numéro de version et sa section Pièges, telle quelle.

Le dire à voix haute au passage : la copie installée est un fichier de plugin, la source est le hub.

**Lancer la révision.** Le message type du formateur, à recopier en changeant le nom de la skill et le défaut :

> Utilise forger-le-kit en révision, sur la seule skill restitution-entretien.
> Pars de la version que le hub vient de renvoyer, pas d'une réécriture.
> Défaut à corriger : un chiffre non mesuré est passé en titre d'enjeu, et le périmètre a changé entre la source et le titre.
> Ajoute au maximum une ligne à la procédure et une ligne aux Pièges. Ne touche à rien d'autre : ni le nom, ni la description, ni les six blocs, ni les références.
> Montre-moi les deux lignes ajoutées avant d'écrire quoi que ce soit.
> Ne crée aucune skill, n'en renomme aucune, ne publie rien, ne désinstalle rien.

Les trois dernières lignes ne sont pas des précautions de style : ce sont les six interdits du mode révision, écrits dans le message pour qu'ils tiennent même si la conversation dérive.

**Publier**, une fois le cas rejoué et l'accord donné :

> Publie restitution-entretien sur le hub avec cette note de version : « Un titre d'enjeu ne porte plus de chiffre non mesuré ; le périmètre d'un chiffre se cite comme la source le dit. »
> Garde la description telle quelle. Donne-moi le numéro de version et la phrase exacte que le hub renvoie.

## La ligne de Pièges, gabarit

Quatre éléments, dans cet ordre, en une à deux phrases : la date, ce qui a été demandé, ce qui est sorti, la règle qui en découle.

> Septembre 2026, restitution d'un entretien dirigeant : le titre d'enjeu annonçait « Quatre-vingts pour cent des appels » quand la source disait « de mes appels ». Un titre d'enjeu ne porte jamais un chiffre non mesuré, et le périmètre d'un chiffre se cite comme la source le dit.

Sans la date, on ne sait plus si le piège est encore d'actualité. Sans le texte fautif, la ligne se lit comme une précaution générale, et une précaution générale ne change rien à ce que Claude produit.

## La ligne de procédure

Un geste, un endroit, un critère de fin. Elle s'insère dans l'étape où le défaut est né, pas en fin de liste.

> Avant d'écrire un titre d'enjeu, vérifier dans le verbatim que le chiffre qu'il porte a été mesuré, et reprendre le déterminant de la source.

Quand le défaut se corrige par un interdit et non par un geste, il n'y a pas de ligne de procédure : la ligne de Pièges suffit. Un diff d'une seule ligne est un bon diff.

## La note de version

Une phrase, au présent, qui énonce la règle nouvelle. C'est le seul texte que lira le collègue qui reçoit la mise à jour.

> Un titre d'enjeu ne porte plus de chiffre non mesuré ; le périmètre d'un chiffre se cite comme la source le dit.

Mauvais : « corrections diverses », « mise à jour de la section Pièges », « v2 ». Rien de ce qui a changé pour celui qui reçoit.

## Les points de rupture

**Le hub répond « contenu identique ».** Sa phrase exacte : « Contenu identique à celui déjà sur la place de marché Weapzy/waoup-kit : rien à pousser ». Le fichier n'a pas été modifié, ou c'est la copie installée qui l'a été. Reprendre par `lire_skill` et rejouer le diff.

**La publication est refusée sur la description.** `publier_skill` refuse au-delà de 200 caractères. Le mode révision ne touche pas à la description : si le refus tombe, c'est qu'elle a été réécrite. Remettre celle de la version du hub, mot pour mot.

**Le dépôt ne répond pas.** Le hub le dit lui-même : « La place de marché n'a pas pu être mise à jour ». La skill est enregistrée au hub et le paquet ZIP est à jour, mais le bouton Mettre à jour ne proposera rien. Lire la phrase, passer par le ZIP en attendant.

**La révision a été écrite dans le fichier installé.** Elle sera écrasée à la prochaine mise à jour du kit, sans avertissement, et personne d'autre ne l'aura vue. Recommencer depuis `lire_skill`.

**Le rejeu se fait dans la conversation qui a servi à réviser.** Elle contient déjà le défaut, la correction et la discussion : le résultat ne prouve rien. Conversation neuve, même matière, même demande.

**Le collègue clique Mettre à jour sans ouvrir une conversation neuve.** Il relance l'ancienne version, chargée à l'ouverture de sa conversation. Conversation neuve des deux côtés.
