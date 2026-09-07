# Cinq évaluations de la skill voix-waoup

Ces scénarios servent à vérifier que la skill corrige la langue sans abîmer le
fond. Chacun donne la requête, les fichiers d'entrée, les comportements attendus
et les signaux d'échec. Un scénario est réussi quand tous les comportements
attendus sont observés et qu'aucun signal d'échec n'apparaît.

Mode d'emploi : ouvrir une conversation neuve, créer le fichier d'entrée, lancer
la requête, comparer la sortie à la grille. Rejouer la série après toute
modification de `SKILL.md`, de `scripts/detecter_tics.py` ou de
`references/mots-creux.txt`.

---

## Évaluation 1. Le verbatim reste intact

**Requête**
> Passe cette restitution à la voix WAOUP avant que je l'envoie au client.

**Fichier d'entrée** — `restitution-verdier.md`

```
# Restitution, groupe Verdier, 14 mars 2025

## Les enjeux de la relation client

Ce n'est pas un problème de moyens, c'est un problème de gouvernance. La
démarche proposée — issue de nos quinze missions comparables — se veut claire,
structurée et actionnable.

Un conseiller de l'agence de Vienne : « nous, on fait ça depuis toujours —
personne n'a jamais rien changé, et honnêtement ce n'est pas notre métier,
c'est celui du siège ».
```

**Comportements attendus**
- Le script est lancé avant toute réécriture, et son rapport est cité ou résumé.
- Le verbatim entre guillemets français est reproduit caractère pour caractère,
  tiret cadratin compris et négation-contraste comprise.
- Le tiret cadratin de la phrase rédigée, lui, disparaît.
- La négation-contraste rédigée est remplacée par une affirmation directe.
- La triade « claire, structurée et actionnable » est réduite.
- Le tableau des corrections ne contient aucune ligne portant sur le verbatim.

**Signaux d'échec**
- Le verbatim est lissé, raccourci, reponctué ou reformulé.
- Le tiret du verbatim est remplacé par une virgule.
- La skill signale le verbatim comme un tic à corriger.

---

## Évaluation 2. Les chiffres ne bougent pas

**Requête**
> Nettoie ce mail avant envoi, il part chez la directrice générale ce soir.

**Fichier d'entrée** — `mail-caution.md`

```
Bien sûr, voici comme convenu la synthèse.

Il ne s'agit pas d'un problème de demande, mais d'un problème de barrière à
l'entrée : sur 12 entretiens, 9 citent la caution de 1 200 euros comme premier
motif d'abandon. Le panier moyen a baissé de 18 % depuis 2016, et 64 % des
retraits se font entre 16 h et 18 h alors que trois agences sur cinq ferment à
16 h 30.

En somme, il convient d'agir avant le comité du 4 avril.
```

**Comportements attendus**
- Tous les nombres se retrouvent à l'identique dans la sortie : 12, 9, 1 200,
  18 %, 2016, 64 %, 16 h, 18 h, trois, cinq, 16 h 30, 4 avril.
- Les unités et les formats sont conservés : « 16 h 30 », pas « 16h30 ».
- L'ouverture de politesse disparaît, le mail commence par le contenu.
- La négation-contraste et la chute « en somme » disparaissent.
- Le mail garde une formule d'adresse et de signature s'il en avait une.

**Signaux d'échec**
- Un chiffre est arrondi, converti, déplacé d'une phrase à l'autre ou supprimé.
- Une date est reformulée (« début avril » pour « 4 avril »).
- Un pourcentage change de base (« 18 % de baisse » devient « une baisse d'un
  cinquième »).

---

## Évaluation 3. Le texte propre ne bouge pas

**Requête**
> Passe ce texte à la voix WAOUP.

**Fichier d'entrée** — `note-propre.md`

```
# Restitution, coopérative Le Pré Vert, 12 mars 2025

## La caution bloque les petits artisans

Sur douze entretiens, neuf mentionnent la caution de 1 200 euros comme premier
motif d'abandon. Un artisan de Vienne l'a dit sans détour : « je repars avec ma
remorque vide, je vais chez le concurrent, il me demande rien ».

Le montant n'a pas bougé depuis 2016. Le panier moyen, lui, a baissé de 18 %.

Nous avons interrogé Paul Mercier, Marie Dujardin et Jean Ravel sur ce point.
Les trois donnent la même réponse : personne n'a jamais demandé à changer les
horaires.

## Ce que la restitution ne dit pas

Trois profils manquent : les clients perdus, les saisonniers, les prescripteurs.
```

**Comportements attendus**
- Le script rend le verdict « Rien à signaler » et zéro occurrence retenue.
- La skill annonce que le texte est envoyable en l'état.
- Le tableau des corrections est vide, ou remplacé par une ligne « aucune
  correction nécessaire ».
- L'énumération « Paul Mercier, Marie Dujardin et Jean Ravel » est intacte.
- L'énumération « les clients perdus, les saisonniers, les prescripteurs » est
  intacte.

**Signaux d'échec**
- La skill invente des corrections pour justifier son passage.
- L'énumération de noms propres est traitée comme une triade et amputée.
- Les titres, qui sont déjà des conclusions, sont réécrits.
- Le texte est raccourci « pour faire plus WAOUP ».

---

## Évaluation 4. Le texte ne devient pas plat

**Requête**
> Corrige les tics de ce passage de propale, mais garde du relief.

**Fichier d'entrée** — `propale-relief.md`

```
## Nos trois convictions

Votre réseau ne perd pas des clients au moment du devis. Il les perd trente
secondes plus tôt, quand personne ne lève la tête au comptoir. C'est brutal,
et c'est ce que douze entretiens montrent sans ambiguïté.

Le modèle actuel repose sur une organisation robuste, holistique et
structurante, véritable pierre angulaire de la performance globale du groupe.
En définitive, il conviendra d'engager une transformation en profondeur.
```

**Comportements attendus**
- Le premier paragraphe est conservé quasiment tel quel : sa brutalité est le
  fond, pas un tic.
- « C'est brutal » n'est pas adouci.
- Le second paragraphe est réécrit : triade, mots creux et chute disparaissent.
- La réécriture remplace les mots creux par un fait, pas par un autre mot creux.
- La sortie conserve au moins une phrase qui tranche.
- Le rythme alterne encore phrases courtes et phrases longues.

**Signaux d'échec**
- Le texte final est une suite de phrases courtes sans aucune emphase.
- « C'est brutal » devient « ce constat mérite attention ».
- Le parti pris du premier paragraphe est neutralisé.
- Les mots creux sont remplacés par d'autres mots creux (« robuste » devient
  « solide », « holistique » devient « global »).

---

## Évaluation 5. Le HTML et le rapport machine

**Requête**
> Lance le détecteur sur ce fichier HTML en sortie JSON, puis dis-moi ce qu'il
> faut corriger. Ne réécris rien pour l'instant.

**Fichier d'entrée** — `propale.html`

```
<h1>Proposition commerciale &mdash; Verdier</h1>
<p>Bien s&ucirc;r, nous avons structur&eacute; notre r&eacute;ponse.</p>
<p>Ce n'est pas une question d'outil, c'est une question de m&eacute;thode.
La d&eacute;marche se veut pragmatique, mesurable et actionnable.</p>
<blockquote>« on nous demande tout &mdash; et son contraire »</blockquote>
<h2>Les b&eacute;n&eacute;fices attendus</h2>
```

**Comportements attendus**
- Le script est appelé avec `--json` et la sortie est du JSON valide.
- Les entités HTML sont décodées : le tiret de `&mdash;` est bien détecté.
- Les numéros de ligne renvoient aux lignes réelles du fichier HTML.
- Le tiret cadratin de la citation est classé `"protege": true`.
- Le titre `<h2>` est repéré comme titre-thème.
- La skill s'arrête au diagnostic et ne produit aucune réécriture.

**Signaux d'échec**
- Le contenu des balises `<script>` ou `<style>` est analysé.
- Les numéros de ligne sont décalés par rapport au fichier.
- Le tiret de la citation est compté dans les occurrences retenues.
- La skill réécrit alors que la requête l'interdit.

---

## Chaque évaluation protège une chose

| Évaluation | Ce qu'elle protège |
|---|---|
| 1 | La parole du client |
| 2 | Les faits chiffrés |
| 3 | Le texte déjà bon |
| 4 | Le relief et le parti pris |
| 5 | La fiabilité technique du détecteur |
