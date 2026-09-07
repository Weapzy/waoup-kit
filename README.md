# Le kit WAOUP

Trois plugins Claude, un marketplace. Conçus pour Claude Cowork, compatibles Claude Code,
et téléversables une par une sur claude.ai.

```
kit/
├── .claude-plugin/marketplace.json   le catalogue (c'est ce fichier que Cowork lit)
├── waoup/                            le socle : 10 skills, une par livrable
├── waoup-commerce/                   le développement commercial : 3 skills
└── waoup-forge/                      la Forge : fabrique un kit, puis se retire
```

## Installer

**Cowork.** Personnaliser, Plugins, Ajouter une place de marché, coller `Weapzy/waoup-kit`
(ou `https://github.com/Weapzy/waoup-kit`). Les trois kits apparaissent : Installer sur chacun.
Cowork n'accepte qu'un dépôt Git public comme place de marché : le kit vit sur GitHub, et le hub
y pousse chaque publication. Pour récupérer une skill publiée : Plugins, place de marché waoup,
Mettre à jour. En secours, les ZIP du hub (`https://waoup.weapzy.com/paquets/<plugin>.zip`)
s'importent par « importer un fichier » sur la page Plugins.

**Claude Code**

```bash
claude plugin marketplace add Weapzy/waoup-kit
claude plugin install waoup@waoup
claude plugin install waoup-forge@waoup      # seulement quand on fabrique une skill
```

**claude.ai.** Les plugins ne s'y installent pas. Télécharger la skill voulue au format
`.skill` depuis le hub, puis Personnaliser, Compétences, Téléverser.

**En local, pour essayer sans rien installer**

```bash
claude --plugin-dir ./waoup --plugin-dir ./waoup-forge
```

## Les skills

### waoup, le socle

| Skill | Entrée | Sortie |
|---|---|---|
| `guide-entretien` | le brief de mission | hypothèses, trame en cinq temps, relances |
| `restitution-entretien` | le verbatim, les notes | la restitution en six blocs + les angles morts |
| `defis` | la restitution | cinq à sept défis priorisés |
| `synthese-marathon` | la matière d'atelier | concepts, arbitrages, prototypes |
| `propale` | brief + restitution | la proposition en huit parties |
| `deck-investisseur` | le business plan | le récit en douze pages |
| `passe-critique` | un brouillon | trois faiblesses, les affirmations non sourcées |
| `voix-waoup` | un texte validé sur le fond | le texte sans signature IA + le tableau des corrections |
| `mise-en-forme-charte` | un markdown figé | HTML chartée, PDF, PowerPoint dérivé |
| `anonymisation` | un document à partager | le document traité + la table de correspondance |

### waoup-commerce

| Skill | Entrée | Sortie |
|---|---|---|
| `compte-rendu-rdv` | une note vocale, une transcription | le compte rendu + le bloc CRM |
| `panorama-entreprise` | un nom de société ou de personne | la fiche avant rendez-vous, sourcée |
| `business-case` | le profil de l'interlocuteur | le bon cas, le bon angle, le bon format |

### waoup-forge

`forger-le-kit` mène l'entretien de forge et écrit les skills. `publier-au-hub` les partage.
`passer-le-relais` fabrique le paquet, l'installe et pose la fiche de reprise. Chez WAOUP la Forge reste installée : elle révise les skills du kit à partir des retours du hub (section « Réviser une skill existante » de `forger-le-kit`).

## Modifier une skill

Un `SKILL.md` est un fichier texte. Les règles qui comptent :

- `name` en minuscules avec tirets, identique au nom du dossier ;
- `description` **200 caractères maximum** (limite claude.ai), à la troisième personne,
  avec la situation, la matière d'entrée et le livrable de sortie ;
- corps sous 500 lignes ; le détail part dans `references/` ;
- la section **Pièges** se remplit avec les échecs réellement rencontrés. C'est la partie
  la plus utile et la seule qui ne peut pas être devinée.

Après modification : `claude plugin validate ./waoup --strict`, puis publication au hub.

## Fabriquer le paquet partageable

```bash
bash waoup-forge/skills/passer-le-relais/scripts/relais.sh paquet ./waoup ./dist
```

Produit `waoup.plugin` : un fichier unique, installable en un clic dans Cowork.

## Configuration du connecteur

`waoup-forge` déclare trois réglages, demandés à l'installation dans Claude Code :
`hub_url` (adresse du hub), `hub_jeton` (le jeton personnel), `prenom` (signe les publications).

En Cowork, le connecteur du hub est configuré depuis la page du plugin.
