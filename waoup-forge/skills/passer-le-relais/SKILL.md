---
name: passer-le-relais
description: Livre le kit forgé sous forme de paquet installable et partageable, l'installe et le publie au hub, puis retire la Forge dans le seul cas d'une forge initiale chez un client.
compatibility: Le retrait de la Forge ne concerne qu'une forge initiale chez un client. Automatique en Claude Code, en deux clics en Cowork, guidés par la skill.
license: Proprietary. Usage interne WAOUP.
metadata:
  auteur: Weapzy
  version: "1.0"
---

# Passer le relais

Livrer le kit forgé : le contrôler, le mettre en paquet, l'installer, le publier au hub, laisser une fiche de reprise.

Chez WAOUP, la Forge reste installée. C'est elle qui révise les skills du kit à chaque retour remonté au hub, et le kit ne vit que par ces révisions. L'étape de retrait ne vaut que pour la forge initiale d'un kit chez un client : la personne repart avec son kit, elle n'a pas de raison de garder l'atelier ouvert.

## Quand l'utiliser

Quand le kit forgé a été éprouvé sur un vrai dossier et que la personne le juge utilisable. Pas avant.

## Procédure

```
- [ ] 1. Contrôler le kit
- [ ] 2. Fabriquer le paquet .plugin
- [ ] 3. Livrer le paquet
- [ ] 4. Installer le kit
- [ ] 5. Publier au hub
- [ ] 6. Retirer la Forge (forge initiale chez un client seulement)
- [ ] 7. Remettre la fiche de reprise
```

**1. Contrôler.** Lancer `claude plugin validate <dossier>` si la commande existe. Sinon, vérifier à la main : `.claude-plugin/plugin.json` présent et valide, `name` en minuscules avec tirets, chaque dossier de `skills/` contient un `SKILL.md`, chaque `name` correspond à son dossier, chaque description tient sous 200 caractères.

**2. Fabriquer le paquet.** Lancer `scripts/relais.sh paquet <dossier-du-kit>`. Le script produit la même archive sous deux extensions : `<nom>.plugin` et `<nom>.zip`. Le contenu est à la racine de l'archive, jamais dans un dossier de trop.

**3. Livrer.** Deux chemins, et le choix compte.

Quand Claude dépose lui-même le fichier dans le dossier de sortie de la session, utiliser le **`.plugin`** : il s'affiche avec un aperçu de son contenu et un bouton d'installation.

Quand le fichier part par message et que la personne l'installe elle-même, envoyer le **`.zip`**. La fenêtre d'installation depuis un fichier propose les deux extensions mais n'accepte pas toujours le `.plugin`, et le message d'erreur n'explique rien. Le `.zip` passe dans tous les cas.

**4. Installer.** En Cowork : bouton d'installation sur le paquet déposé, ou Personnaliser puis Plugins puis installer depuis un fichier, en choisissant le `.zip`. Sur Windows, le bouton de téléversement peut rester masqué tant qu'aucun plugin n'est installé : faire installer d'abord n'importe quel plugin du catalogue Anthropic, le bouton apparaît ensuite. En Claude Code : `claude plugin install <nom>@waoup` si le kit est passé par la place de marché `Weapzy/waoup-kit`, sinon `claude --plugin-dir <dossier>` pour un essai immédiat.

**5. Publier au hub.** Enchaîner avec la skill `publier-au-hub` pour que le reste de l'équipe voie le kit et puisse l'installer sans attendre un envoi de fichier.

**6. Retirer la Forge, chez un client seulement.** Chez WAOUP, sauter cette étape : la Forge reste installée, la révision des skills passe par elle. Chez un client dont le kit vient d'être forgé, lancer `scripts/relais.sh retrait`. En Claude Code, la désinstallation est automatique. En Cowork, le script ne peut pas agir : afficher alors le geste, Personnaliser puis Plugins puis La Forge WAOUP puis Désinstaller, et confirmer avec la personne que c'est fait.

Ne jamais retirer la Forge avant que l'installation du kit soit vérifiée. Contrôle : demander une tâche qui doit déclencher une skill du kit, et vérifier qu'elle se déclenche.

**7. La fiche de reprise.** Écrire dans le dossier de travail un fichier `KIT.md` de vingt lignes maximum : ce que contient le kit, comment le mettre à jour, où se trouve le hub, qui arbitre les versions, quand a lieu le rituel. C'est ce fichier qu'on relira dans trois mois.

## Réinstaller la Forge plus tard

La Forge se réinstalle en une commande quand il faut fabriquer une nouvelle skill ou refondre le kit :

- Cowork : Personnaliser, Plugins, place de marché `Weapzy/waoup-kit`, installer La Forge WAOUP.
- Claude Code : `claude plugin install waoup-forge@waoup`.

Chez un client, elle n'a pas à rester installée entre deux chantiers. Chez WAOUP, elle reste : réviser une skill après un retour du hub est un geste hebdomadaire, pas un chantier.

## Pièges

Ne pas confondre le paquet et le dossier source. Le paquet est une photo : toute modification ultérieure du kit demande un nouveau paquet, ou passe par le hub.

Si un téléversement échoue avec « Upload failed » sans autre explication, l'extension est presque toujours en cause. Renvoyer le `.zip`.

Un paquet fabriqué depuis le mauvais répertoire donne une archive avec un dossier de trop à la racine, et l'installation échoue sans message clair. Toujours passer par le script.

Ne jamais retirer la Forge chez WAOUP au motif que le kit est livré. Le kit livré est un kit qui commence à vivre, et sa révision demande la Forge.

Chez un client, ne pas retirer la Forge dans la même conversation que celle qui a servi à forger : finir la conversation, ouvrir une session neuve, vérifier que le kit répond, retirer ensuite.

Si la personne n'a pas encore de jeton de hub, sauter l'étape 5 et le noter dans `KIT.md`. Un kit non publié reste un kit qui marche.
