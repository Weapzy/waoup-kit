# Ce qui trahit une mise en forme produite par une IA

Règles extraites du plugin `impeccable` (détecteur chiffré et référence de design), de `make-interfaces-feel-better`, de `ui-ux-pro-max` et de `frontend-design` ; ne sont retenues que celles qui valent pour un document A4 ou une diapositive 16:9, avec leur seuil d'origine.

Le critère n'est pas « c'est joli ». C'est « personne ne pose la question ». Un goût ne se transmet pas, une liste se vérifie. Les règles marquées **auto** sont celles que `scripts/controle_ia.mjs` contrôle tout seul ; les autres se regardent.

---

## La règle qui commande toutes les autres

**Le brief gagne.** Là où la charte fixe une direction, on la suit exactement, y compris quand elle tombe sous un avertissement de motif saturé. Rediriger un brief clair vers son propre goût est un échec, pas une amélioration. La charte WAOUP s'applique, elle ne se corrige pas.

Trois marqueurs sont dans la charte elle-même, et ils y restent :

| Marqueur | Ce qu'en dit la source | Décision WAOUP |
| --- | --- | --- |
| Presque-noir plus un accent vert acide | Agrégat esthétique n° 2 du design généré | Conservé. La distinction se joue sur la grille, l'échelle typographique et le fond, pas sur la palette. |
| Inter et Space Grotesk | Liste noire des dix-sept polices surexposées | Conservées, et dérogées dans le détecteur. Voir « Polices » ci-dessous. |
| La marque en capitales sur la couverture | Tic de chrome de template n° 1 | Conservée sur la seule couverture. Interdite partout ailleurs. |

Ce qui n'est pas une dérogation se corrige : la source de verbatim a été réécrite, l'échelle typographique relevée, le plancher de texte remonté.

---

## Marqueurs bannis, sans rachat possible

Aucun brief ne les justifie. Ce sont les défauts par défaut, ceux que tout générateur produit sur n'importe quel sujet.

| Marqueur | Seuil de détection | Contre-mesure WAOUP |
| --- | --- | --- |
| **Liseré latéral coloré** (auto) | Bordure d'un seul côté, non neutre, ≥ 2 px avec rayon, ≥ 3 px sans. Bande horizontale de 3 à 12 px. | Cadre fin sur les quatre côtés, plus une étiquette en tête. C'est le marqueur le plus reconnaissable de tous. |
| **Sur-titre en capitales** (auto) | Libellé au-dessus d'un titre, capitales avec interlettrage ≥ 1,6 px, ou graisse ≥ 700 en couleur d'accent. | Le titre porte son propre poids. Si les mots comptent, ils entrent dans le titre. Ne pas confondre avec l'étiquette d'encadré, qui est *dans* le cadre et reste. |
| **Texte en dégradé** (auto) | `background-clip: text` posé sur un dégradé. | L'emphase vient de la graisse ou de la taille. |
| **Numérotation décorative** (auto) | Sections numérotées 01, 02, 03 sans information portée. | Numéroter seulement quand la séquence sert au lecteur. |
| **Ombre ou halo coloré** (auto) | Chroma ≥ 30 sur la couleur d'ombre. Halo à décalage nul avec flou > 4 px. | Aucune ombre dans la charte. Un filet de 1 px sépare, il n'a jamais besoin d'aide. |
| **Halo en dégradé radial** (auto) | `radial-gradient` en fond. | Même marqueur, dessiné autrement. Zéro dégradé dans un livrable. |
| **Filet fin plus large ombre diffuse** (auto) | Deux bordures ≤ 1,5 px et un flou d'ombre ≥ 16 px sur le même bloc. | Choisir : bordure ou ombre, jamais les deux. Chez WAOUP, bordure. |
| **Pastille d'icône au-dessus d'un titre** (auto) | Tuile de 32 à 128 px, ratio 0,7 à 1,4, fond ou bordure, rayon > 0. | Aucune icône décorative. C'est la carte-feature universelle de l'IA. |
| **Carte dans une carte** (auto) | Deux conteneurs de classe carte imbriqués. | La carte est le conteneur paresseux. L'espacement suffit. |
| **Grille de cartes identiques** icône, titre, texte | Trois ou quatre cartes de même poids alignées | Quatre idées font quatre diapositives, pas une grille de quatre cartes. |
| **Fond crème ou beige** (auto) | Trois canaux ≥ 209, ordre chaud R ≥ V ≥ B, chaleur R moins B entre 6 et 48, sur une surface de page. | Papier blanc, ou noir de charte. Jamais crème, même pour un sujet chaleureux. |
| **Violets et mauves** (auto) | Hex `#7c3aed`, `#8b5cf6`, `#a855f7`, `#9333ea`, `#7e22ce`, `#6d28d9`, `#6366f1`, `#764ba2`, `#667eea`. Teinte 260 à 310° avec chroma ≥ 50 sur un titre. | Aucune couleur hors du bloc `:root` de la charte. |
| **Emoji en système d'icônes** (auto) | Tout emoji dans le rendu. | Aucune icône, ou une famille dessinée, une épaisseur, une taille optique. |
| **Police système en voix de titrage** | Impact, Arial Black, la sans de la plateforme. | La police installée la plus proche est un échec, pas un repli. |
| **Glassmorphism, flou décoratif, ombre dure sans flou** | Hors univers réellement néobrutaliste. | Absents de la charte, et ils le restent. |
| **Le gabarit hero-métrique** | Gros chiffre, petit libellé, statistiques de soutien, accent. | Le bloc `.chiffre` de la charte porte une source. Un chiffre sans source est de la décoration. |
| **Contenu invisible au repos** (auto) | `opacity: 0` en attente d'un script. | Un document ne s'anime pas. |
| **Image cassée ou d'attente** (auto) | `<img>` sans `src`. | Défaut bloquant. |
| **Lorem ipsum** (auto) | Le faux texte, sous toutes ses formes. | Des données d'exemple réalistes, et le vrai sujet du brief du début à la fin. |

---

## Typographie

| Règle | Seuil | Contre-mesure |
| --- | --- | --- |
| Rapport entre deux niveaux (auto) | ≥ 1,25 entre deux pas voisins de l'échelle. | Corrigé dans la charte : 2,65 / 2,05 / 1,6 / 1,25 / 1 rem, tous les rapports entre 1,25 et 1,29. |
| Amplitude de l'échelle | Rapport ≥ 2,0 entre la plus petite et la plus grande taille. | Charte : 2,65 rem sur 0,8 rem, soit 3,3. |
| Plancher du texte fonctionnel (auto) | 11 px absolus pour libellés, cellules, méta, légendes. 10 px seulement pour du légal non interactif. | Corrigé : `--t-micro` passe de 0,74 à 0,8 rem, soit 11,2 px une fois `html` basculé à 10,5 pt. |
| Plancher du corps | 16 px. Secondaire à 14 px. Défaut sous 12 px. | Charte : `--t-corps: 1rem`. |
| Mesure de lecture | 65 à 75 caractères par ligne. Défaut au-delà de 85. | Charte : `max-width: 78ch` sur `p` et `li`, 62ch sur le chapô. |
| Interligne du corps | 1,5 à 1,7. Défaut sous 1,3. | Charte : 1,62. Sur fond sombre, monter à 1,7 : la couverture et les deux diapositives noires le font. |
| Interlettrage | Jamais au-delà de 0,05 em au corps. Tracking négatif : plancher moins 0,04 em. | Charte : 0 au corps, moins 0,02 em sur les grands titres, 0,06 à 0,22 em réservés aux étiquettes courtes en capitales. |
| Capitales longues (auto) | Plus de 30 caractères en capitales hors titre. | On reconnaît un mot à sa silhouette, que les capitales suppriment. |
| Texte justifié (auto) | `text-align: justify` sans `hyphens: auto`. | Fer à gauche par défaut. |
| Hiérarchie de titres (auto) | Aucun niveau sauté, h1 puis h3 est un défaut. | Le script de conversion reprend la hiérarchie du Markdown telle quelle. |
| Un titre se distingue du corps | Par la taille et la graisse, jamais par la seule couleur. | Filet, graisse 700, famille de titrage. |
| Titre surdimensionné | Défaut si ≥ 72 px **et** ≥ 40 caractères **et** ≥ 28 % de la hauteur. Plafond de titrage : 6 rem. | Deux mots à 80 px sont légitimes ; c'est la longueur combinée à la domination qui est le marqueur. |
| Chiffres tabulaires | Toute colonne de chiffres, montant, durée. Jamais sur un numéro de téléphone ou de version. | Charte : `tabular-nums` posé sur `body`. Vérifier le dessin du 1 avec Inter. |
| Rythme de paragraphe | Espacement **ou** alinéa, pas les deux. | Charte : espacement seul. |
| Graisses | Corps 400, libellés 500, emphase 600, titres 600 à 700. | Ne pas descendre sous 400 en petit corps. |
| Deux familles au maximum | Une seule suffit souvent. | Charte : titrage plus labeur, plus une chasse fixe pour les étiquettes de données. |

### Polices

La liste noire des dix-sept polices surexposées : Inter, Roboto, Open Sans, Lato, Montserrat, Arial, Helvetica, Fraunces, Instrument Sans, Instrument Serif, Geist, Geist Sans, Geist Mono, Mona Sans, Plus Jakarta Sans, Space Grotesk, Recoleta. Seuil d'application : la police couvre ≥ 15 % des éléments textuels, sur au moins vingt.

**La charte WAOUP en nomme deux, Inter et Space Grotesk.** Elles restent, c'est une décision. Le détecteur les déroge nommément, et signale les quinze autres. Ce que cela coûte : la police ne fait plus la distinction, donc la grille, l'échelle typographique, le fond et le motif propre au métier la font seuls. Ce que cela évite : un chantier de charte au milieu d'un livrable.

Si un jour la question se rouvre, les appariements sobres pour un cabinet sont EB Garamond avec Lato, Crimson Pro avec Atkinson Hyperlegible, Libre Bodoni avec Public Sans, Lexend avec Source Sans 3, ou IBM Plex Sans seule.

---

## Hiérarchie

| Règle nommée | Seuil | Contre-mesure |
| --- | --- | --- |
| **Test du plissement des yeux** | Détail flouté, on identifie encore le primaire, le secondaire, les grands groupes. | Si tout se ressemble, c'est le plancher de bruit visuel. |
| **Un primaire, deux à trois secondaires** | Tout le reste atténué. | Un seul élément porte la page. |
| **Règle de la mémoire de travail** | Quatre éléments au maximum par point de décision. Cinq à sept : regrouper. Huit : surcharge. | Quatre puces par diapositive, quatre lignes par encadré, quatre colonnes par tableau de synthèse. |
| **Test du squelette** | Retirer le texte. Si la structure ne dit plus ce qu'est la section, la force était dans la taille du texte. | Refaire la structure, pas la typographie. |
| **Test du retrait** | Enlever l'élément. Si personne ne le remarque, il ne méritait pas sa place. | S'applique à chaque filet, chaque étiquette, chaque encadré. |
| **Règle Chanel** | Avant de livrer, regarder l'ensemble et retirer un accessoire. | Concentrer l'audace en un seul endroit. |
| **La structure est de l'information** | Numérotations, sur-titres, filets, libellés doivent encoder quelque chose de vrai. | Sinon c'est de la décoration, et la décoration est le marqueur. |
| **La couverture est une thèse** | Pas un en-tête. | Le titre de couverture porte la conclusion, pas le thème. La couverture du deck fait pareil. |
| **Deuxième passe** | Ne pas ajouter de graphisme, raffiner l'existant. | Deux rounds de correction au plafond, puis on arrête. |
| **Sévérités P0 à P3** | P0 bloquant, P1 majeur ou violation AA, P2 mineur, P3 finition. | Si tout est important, rien ne l'est. |

---

## Espacement

| Règle | Seuil | Contre-mesure |
| --- | --- | --- |
| Plus d'espace au-dessus d'un titre qu'en dessous (auto) | Défaut si l'espace supérieur < 0,75 fois l'inférieur, avec un déficit ≥ 12 px, sur au moins deux titres. | Corrigé et nommé dans la charte : h2 72 sur 24, h3 48 sur 12, h4 36 sur 6. Un titre appartient au bloc qu'il ouvre. |
| Espacement monotone | Défaut si une valeur domine plus de 60 % des espacements avec trois valeurs uniques ou moins. | Groupes serrés, séparations généreuses. Le rythme naît du contraste entre intervalles. |
| Base 4 plutôt que base 8 | Une base 4 fournit les pas intermédiaires. | Charte : `--pas: 6px`, dérivés x1, x2, x3, x4, x6, x8, x12. |
| Padding d'un bloc encadré | Minimum 8 px, idéalement 12 à 16 px. Vertical `max(4px, taille x 0,3)`, horizontal `max(8px, taille x 0,5)`. | Charte : encadrés et verbatims à 18 sur 24 px. |
| Le corps ne touche jamais le bord | Minimum 16 px, idéalement 24 à 32. | Charte : marges A4 de 20 mm, marges de diapositive de 24 et 18 mm. |
| Un seul rythme sur tout le document | Avec des variations de densité assumées. | Un passage dense mérite un passage calme. |

---

## Grille et couleur

| Règle | Seuil | Contre-mesure |
| --- | --- | --- |
| Alignement unique | Choisir et s'y tenir, sans bascule d'un bloc à l'autre. | Aucun texte centré hors couverture et titre de section. |
| Largeur de conteneur constante | Pas de largeurs arbitraires d'une page à l'autre. | Charte : zone de texte de 170 mm sur toutes les pages. |
| Rien ne déborde, rien ne chevauche | Les marges ne sont pas négociables. | `overflow: hidden` sur chaque diapositive, conteneur en défilement pour un tableau large. |
| Texte répété trois fois dans un conteneur | Redondance. | Le dire une fois, là où il compte. |
| Stratégie couleur avant les couleurs | Quatre stratégies : retenue, engagée, palette complète, immersive. | **WAOUP : retenue.** Des neutres plus un accent, le défaut quand on vient lire. |
| Rareté de l'accent | L'accent primaire occupe 10 % d'une page au plus. Règle 60/30/10. | Plus exigeant que « plus de lime que de blanc ». C'est la version vérifiable. |
| Contraste AA sur les valeurs calculées (auto pour le lime) | Corps ≥ 4,5:1, grand texte ≥ 3:1 à 24 px ou 18,67 px en gras, contrôles ≥ 3:1. | **Le lime sur blanc donne 1,1:1. Il ne porte jamais de texte, et ne fait pas un filet fin sur fond clair.** Deux usages sûrs, mesurés à 15:1 : noir sur aplat lime, lime sur aplat noir. La charte les a nommés `--texte-sur-lime` et `--lime-sur-noir`. |
| Jamais de gris sur fond coloré | Texte de chroma < 20 sur un fond dont les stops ont une chroma ≥ 40. | Une nuance plus sombre du fond, ou du blanc. |
| La couleur seule ne porte jamais l'information | Doubler par texte, forme ou position. | C'est le test noir et blanc de la charte. |
| Ni noir pur ni blanc pur | Le presque-noir teinté est lui-même un tic. | Le noir WAOUP est violacé, `#26232E`. Assumé et documenté. |
| Rôles, pas nuancier | Canevas, surfaces, texte primaire et secondaire, action, bordures, sémantiques. | Charte : bloc « Rôles » déjà présent, à modifier là et pas dans les règles. |

---

## Finition

- **Bordure ou ombre, jamais les deux.** L'élévation se déclare une fois. Charte : filet de 1 px, aucune ombre à l'impression.
- **Filet d'abord.** Un filet de 1 px avant toute ombre. C'est une force de la charte, pas un manque.
- **Rayons concentriques.** Rayon extérieur égale rayon intérieur plus padding. Un rayon identique sur parent et enfant est ce qui fait sonner faux le plus souvent. Charte : rayon unique de 3 px sur des blocs à 18 ou 24 px de padding, à revoir ou à assumer en passant à 0.
- **Contour d'image.** 1 px, opacité 0,1, noir pur en clair, blanc pur en sombre, `outline-offset: -1px`. Jamais un presque-noir teinté, jamais l'accent de marque. Non négociable, et non couvert par la charte à ce jour.
- **Une seule famille d'icônes**, une épaisseur de trait de 1,5 ou 2 px, une taille optique, alignée sur la ligne de base.
- **Alignement optique après inspection du rendu**, pas seulement mathématique.
- **Thématiser les surfaces qu'on n'a pas dessinées** : sélection de texte, anneaux de focus, décalage de soulignement, chiffres de tableau. C'est le signal le plus économique qu'une page a été construite et non assemblée, et celui que les modèles sautent le plus.
- **Graphiques** : type adapté à la donnée, pas de camembert au-delà de cinq catégories, valeurs étiquetées directement sur les petits jeux, traits ≥ 3:1 contre le fond, étiquettes ≥ 4,5:1. Toujours fournir l'alternative tabulaire.
- **Formats localisés** pour nombres, dates et montants.

---

## Document, impression, diapositive

**Adaptation écran vers impression, liste complète.** Sauts de page à des points logiques ; retirer navigation et éléments cliquables ; marges correctes ; développer les URL abrégées ; numéros de page, en-têtes et pieds ; métadonnées d'impression ; graphiques en version imprimable. La charte couvre en-tête, pied et sauts ; il manque les numéros de page, les URL développées et les métadonnées.

**Un fond sombre est contre-indiqué pour du contenu destiné à l'impression.** Conséquence : couverture noire admise puisque c'est une page, corps sur papier blanc, et pour le deck un thème écran distinct. Un seul système, deux thèmes.

### Les six règles de diapositive

1. **Format 16:9 verrouillé.** 338,7 x 190,5 mm, soit 13,333 x 7,5 pouces, soit 1280 x 720 px à 96 dpi. `overflow: hidden` sur chaque diapositive.
2. **Marges de 24 mm sur les côtés, 18 mm en haut et en bas.** Le contenu critique tient dans les 70 à 80 % centraux. Rien à moins de 50 px d'un bord.
3. **Une idée par diapositive.** Quatre idées font quatre diapositives.
4. **Le titre porte la conclusion, en douze mots au plus.** Pas le thème : la conclusion. « Le retour de matériel n'a pas de propriétaire », pas « Le processus de retour ».
5. **Corps à 18 pt plancher, titre entre 32 et 40 pt.** Quarante mots de corps hors tableau, cinq puces au plus, deux lignes par puce, aucun second niveau de puce, six lignes de tableau au plus.
6. **Grille.** Gouttière de 48 px en deux colonnes, 24 px en trois, 16 px pour une rangée de métriques. Trois à six blocs au maximum. Prévoir 30 à 40 % d'espace en plus qu'en anglais : le français est plus long.

Longueur d'un deck selon l'usage : commercial 7 à 10 diapositives, revue trimestrielle 10 à 15, comité 15 à 20, atelier 20 à 40, étude de cas 8 à 12.

---

## Ce qui trahit l'IA dans la rédaction

La mise en forme se contrôle au détecteur, l'écriture se contrôle à la relecture. La skill `voix-waoup` porte le détail ; voici ce qui se voit dans un livrable mis en forme.

**Les tics ponctuels.**

- **Le tiret cadratin.** Le détecteur d'origine signale la saturation, à partir de huit tirets et d'une densité d'un pour 500 caractères. **La position WAOUP est plus dure : zéro.** C'est un évitement de décision, l'auteur n'ayant pas choisi la relation entre ses propositions. À la place : virgule, deux-points, point-virgule, point, parenthèses. Le double tiret est pire encore, il signale un nettoyage raté.
- **Les chaînes de métadonnées jointes par des points médians.** Deux points médians sur une même ligne font une chaîne, et une chaîne est un tic. *Contre-exemple, cité comme tel :* l'ancienne source de verbatim du gabarit s'écrivait « — Entretien Ardan · chef d'agence · Le Havre », cumulant le tiret cadratin et la chaîne. Elle s'écrit maintenant « Entretien Ardan, chef d'agence, Le Havre ».
- **Les libellés « MOT tiret fragment »**, le presque-noir teinté tenant lieu de noir, la chasse fixe sur les petits libellés de données, la flèche accolée au texte des liens : les quatre autres tics du chrome de template.
- **Les mots creux.** `voix-waoup/references/mots-creux.txt` porte la liste française. En anglais, `delve` est le marqueur le plus signalé de tous.

**Les tics de construction.**

- **Le pivot par négation.** « Ce n'est pas X, c'est Y », « moins X que Y ». Marqueur plus fort que n'importe quel mot de vocabulaire.
- **La cadence aphoristique.** Trois sections ou plus qui atterrissent sur une courte réfutation. Une fois c'est du style, le motif est le marqueur. Seuil : trois occurrences.
- **Tout en triades.** Chaque liste à exactement trois items, chaque adjectif par trois. Varier : deux, quatre, ou un.
- **Longueur de paragraphe uniforme.** Le marqueur le plus profond. Insérer une phrase de quatre mots, un paragraphe d'une ligne.
- **La dissertation en cinq paragraphes** sur chaque page. Ouvrir par l'exemple, sauter la conclusion, laisser des sections tenir en une phrase.
- **L'équilibre synthétique.** Pour et contre de longueur égale alors qu'un côté est le bon. Écrire la recommandation.
- **La confiance creuse.** « Puissant » sans chiffre. Couper « léger », écrire « 54 Ko ».
- **Les piles de précautions.** « Il pourrait potentiellement être utile d'envisager ».

---

## Les trois tests qui décident

**Le test d'interchangeabilité.** Remplacer le nom du client par celui d'un concurrent. Si rien ne devient faux, le livrable est générique. C'est le seul de ces tests qui porte sur le fond, et c'est celui à enseigner en séance : un document qui passe le détecteur à zéro et rate celui-là n'a rien à faire chez un client.

**Le test du paragraphe.** Pour chaque paragraphe, désigner la phrase qui le rend spécifiquement vôtre. Si on ne peut pas, le paragraphe est de l'IA par défaut, même si un humain l'a tapé.

**Le test de re-dérivation.** Après avoir posé la mise en forme, se demander : sur un brief voisin, est-ce que j'arriverais exactement là ? Si oui, c'est un défaut par défaut et non un choix.

Et le rappel qui vaut pour les trois : **un scan mécanique propre est un plancher, pas une preuve de qualité.** Le détecteur dit ce qui est cassé. Il ne dit jamais que c'est bon.
