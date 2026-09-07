#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Détecteur de tics d'écriture IA pour les livrables WAOUP.

Le script détecte, il ne réécrit jamais. Il lit un fichier .txt, .md ou .html,
et sort la liste des passages à revoir, un score de densité et un verdict.
La réécriture reste au rédacteur, ou au modèle qui suit la skill voix-waoup.

Usage :
    python3 detecter_tics.py livrable.md
    python3 detecter_tics.py livrable.html --json
    python3 detecter_tics.py livrable.md --liste-mots ma-liste.txt
    cat livrable.md | python3 detecter_tics.py -

Codes de sortie :
    0  analyse terminée
    1  analyse terminée, tics au-dessus du seuil (avec --strict seulement)
    2  erreur d'entrée : fichier illisible, liste de mots absente, texte vide

Aucune dépendance externe. Python 3.8 minimum.
"""

import argparse
import bisect
import html
import json
import os
import re
import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Réglages. Chaque valeur porte sa justification : rien ici n'est arbitraire.
# ---------------------------------------------------------------------------

TIRET_CADRATIN = "—"
TIRET_DEMI_CADRATIN = "–"

# Séparateur de blocs. Il remplace les balises HTML de bloc pour que deux
# paragraphes ne se recollent pas en une phrase, sans ajouter de saut de ligne :
# les numéros de ligne du rapport doivent renvoyer au fichier d'origine.
SEPARATEUR_BLOC = "\x1e"

# Un extrait de 110 caractères tient sur une ligne de terminal de 120 colonnes
# une fois ajouté le préfixe « L.123 c.45 ».
LONGUEUR_EXTRAIT = 110

# Distance maximale, en caractères, entre les deux branches d'une
# négation-contraste. Au-delà, les deux membres n'appartiennent plus à la même
# respiration de phrase et le rapprochement devient un faux positif.
PORTEE_NEGATION = 160

# Une phrase de plus de 40 mots ne se dit plus d'une seule traite à l'oral.
# C'est le test de relecture que la skill demande d'appliquer.
MOTS_PHRASE_LONGUE = 40

# Une formule de politesse d'ouverture se loge dans les toutes premières lignes
# de contenu. Plus loin dans le texte, « Voici » appartient au corps du propos.
LIGNES_CONTENU_OUVERTURE = 3

# Au-delà de quatre mots, un membre de triade n'est plus un qualificatif mais
# une proposition : l'énumération devient factuelle et sort du champ du tic.
MOTS_MAX_MEMBRE_TRIADE = 4

# Le premier membre porte en plus le nom qualifié et son entrée de phrase
# (« Une démarche à la fois robuste »). On lui laisse deux fois plus de place.
MOTS_MAX_PREMIER_MEMBRE = 8

# Longueur minimale d'un mot pour que sa terminaison soit lue comme un suffixe
# d'adjectif. En dessous, la terminaison est un hasard graphique (« vue », « il »).
LONGUEUR_MIN_ADJECTIF = 4

# Poids de chaque catégorie dans l'indice de signature. Le tiret cadratin et la
# négation-contraste sont les deux marqueurs que l'équipe WAOUP reconnaît
# elle-même au premier coup d'oeil : ce sont eux qui font dire « c'est du
# Claude ». Ils comptent triple. Les tics de structure comptent double, les tics
# de vocabulaire comptent simple, parce qu'un mot creux isolé passe inaperçu.
POIDS_CATEGORIES = {
    "tiret": 3.0,
    "negation-contraste": 3.0,
    "ouverture": 2.0,
    "chute": 1.5,
    "triade": 1.5,
    "titre-theme": 1.0,
    "mot-creux": 1.0,
}

# Un signal marqué « à vérifier » demande un arbitrage humain : il ne peut pas
# peser autant qu'une certitude dans le verdict. Il compte pour moitié.
COEFFICIENT_A_VERIFIER = 0.5

# Seuils du verdict, en points d'indice pour mille mots. Repères de travail :
# un livrable relu à la main garde une ou deux marques de style au millier de
# mots ; au-delà de six, la lecture bascule et le lecteur voit la machine.
# À réétalonner avec l'équipe sur une dizaine de livrables signés.
SEUIL_ENVOYABLE = 2.0
SEUIL_RETOUCHE = 6.0

# Une densité pour mille mots ne veut rien dire sous quelques centaines de mots :
# un seul tiret dans un gabarit de trois cents mots afficherait douze pour mille.
# Sous ce seuil, on juge au nombre absolu de marqueurs certains.
MOTS_POUR_DENSITE = 400

# Le verdict le plus dur exige une répétition. Un marqueur isolé se corrige,
# il ne signe pas une écriture automatique.
CERTAINS_POUR_REPRENDRE = 3

# Nom du fichier de mots creux cherché à côté du script quand aucune liste
# n'est passée en argument.
LISTE_MOTS_PAR_DEFAUT = os.path.join("references", "mots-creux.txt")

LIBELLES_CATEGORIES = {
    "tiret": "TIRET CADRATIN OU DEMI-CADRATIN",
    "negation-contraste": "NÉGATION-CONTRASTE",
    "triade": "TRIADES",
    "mot-creux": "MOTS CREUX",
    "chute": "CHUTES DE PARAGRAPHE",
    "ouverture": "OUVERTURE DE POLITESSE",
    "titre-theme": "TITRES-THÈMES",
}

ORDRE_CATEGORIES = [
    "tiret",
    "negation-contraste",
    "triade",
    "mot-creux",
    "chute",
    "ouverture",
    "titre-theme",
]

# ---------------------------------------------------------------------------
# Lexiques
# ---------------------------------------------------------------------------

# Terminaisons d'adjectifs français. Sert à reconnaître une triade de
# qualificatifs (« claire, structurée et actionnable ») sans confondre avec une
# énumération de faits (« client, méthode et résultat »).
SUFFIXES_ADJECTIFS = (
    "able", "ables", "ible", "ibles",
    "ique", "iques",
    "if", "ifs", "ive", "ives",
    "eux", "euse", "euses",
    "aire", "aires",
    "el", "els", "elle", "elles",
    "al", "ale", "aux", "ales",
    "ant", "ante", "ants", "antes",
    "ent", "ente", "ents", "entes",
    "é", "ée", "és", "ées",
    "iste", "istes",
    "ien", "ienne", "iens", "iennes",
    "oire", "oires",
    "ile", "iles",
    "ace", "aces", "ide", "ides", "ple", "ples", "uste", "ustes", "aste", "astes",
)

# Adjectifs courants dont la terminaison n'appartient à aucune famille reconnue.
# Sans eux, « claire, structurée et efficace » passerait entre les mailles.
ADJECTIFS_FREQUENTS = {
    "efficace", "robuste", "simple", "souple", "rapide", "solide", "fiable",
    "juste", "propre", "sobre", "clair", "claire", "clairs", "claires",
    "franc", "franche", "riche", "proche", "large", "vaste", "mince", "rude",
    "vive", "brève", "brute", "nette", "forte", "courte", "longue", "lourde",
    "douce", "libre", "digne", "sage", "grave", "calme", "ferme", "stable",
    "utile", "flexible", "lisible", "crédible", "durable", "modeste", "honnête",
    "complète", "concrète", "discrète", "secrète", "inquiète", "prête",
    "chère", "fière", "entière", "légère", "première", "dernière", "sincère",
    "austère", "amère", "grande", "petite", "belle", "vieille", "nouvelle",
    "bonne", "mauvaise", "meilleure", "pire", "faible", "dense", "immense",
    "intense", "tendue", "floue", "aiguë", "ambiguë", "rare", "pure", "sûre",
    "mûre", "dure", "obscure", "précaire",
}

# Noms qui portent les terminaisons ci-dessus sans être des adjectifs.
NOMS_A_TERMINAISON_TROMPEUSE_BIS = {
    "surface", "surfaces", "place", "places", "face", "faces", "glace",
    "trace", "traces", "espace", "espaces", "menace", "menaces", "audace",
    "guide", "guides", "vide", "vides", "aide", "aides", "ride", "rides",
    "peuple", "peuples", "exemple", "exemples", "temple", "couple", "couples",
    "contraste", "contrastes", "geste", "gestes", "reste", "restes", "liste",
    "listes", "piste", "pistes", "buste", "veste",
}

# Noms très fréquents du registre conseil dont la terminaison imite celle d'un
# adjectif. Sans cette liste, « client, méthode et résultat » serait signalé
# comme une triade alors que c'est une énumération légitime.
NOMS_A_TERMINAISON_TROMPEUSE = {
    "client", "clients", "cliente", "clientes",
    "résultat", "résultats", "constat", "constats",
    "moment", "moments", "document", "documents", "argument", "arguments",
    "objectif", "objectifs", "dispositif", "dispositifs", "collectif", "collectifs",
    "actif", "actifs", "effectif", "effectifs", "motif", "motifs",
    "dirigeant", "dirigeants", "dirigeante", "dirigeantes",
    "participant", "participants", "intervenant", "intervenants",
    "consultant", "consultants", "adhérent", "adhérents", "agent", "agents",
    "salarié", "salariés", "salariée", "salariées", "employé", "employés",
    "gérant", "gérants", "commerçant", "commerçants", "habitant", "habitants",
    "étudiant", "étudiants", "patient", "patients", "résident", "résidents",
    "atelier", "ateliers", "chantier", "chantiers", "calendrier", "calendriers",
    "métier", "métiers", "dossier", "dossiers", "fichier", "fichiers",
    "partenaire", "partenaires", "questionnaire", "questionnaires",
    "gestionnaire", "gestionnaires", "affaire", "affaires", "horaire", "horaires",
    "salaire", "salaires", "inventaire", "inventaires", "scénario", "scénarios",
    "enjeu", "enjeux", "prix", "taux", "canal", "canaux", "journal", "journaux",
    "local", "locaux", "signal", "signaux", "capital", "hôpital", "vitrail",
    "entretien", "entretiens", "soutien", "soutiens", "moyen", "moyens",
    "clé", "clés", "idée", "idées", "année", "années", "journée", "journées",
    "durée", "durées", "donnée", "données", "entrée", "entrées", "tournée",
    "marché", "marchés", "budget", "budgets", "comité", "comités",
    "société", "sociétés", "unité", "unités", "priorité", "priorités",
    "histoire", "histoires", "trajectoire", "trajectoires", "mémoire", "mémoires",
    "laboratoire", "laboratoires", "territoire", "territoires",
    "produit", "produits", "service", "services", "process", "processus",
    "méthode", "méthodes", "équipe", "équipes", "projet", "projets",
    "mission", "missions", "réunion", "réunions", "terrain", "terrains",
    "usage", "usages", "besoin", "besoins", "parcours", "livrable", "livrables",
    "responsable", "responsables", "interlocuteur", "interlocuteurs",
    "artisan", "artisans", "particulier", "particuliers", "professionnel",
    "professionnels", "commercial", "commerciaux", "industriel", "industriels",
}

# Formes conjuguées les plus fréquentes du français de conseil. Un titre qui en
# contient une énonce quelque chose : ce n'est pas un titre-thème. La liste
# privilégie le rappel : mieux vaut rater un titre-étiquette que signaler un
# titre qui conclut déjà.
VERBES_CONJUGUES = {
    "est", "sont", "était", "étaient", "sera", "seront", "serait", "seraient",
    "soit", "soient", "suis", "sommes", "êtes", "fut", "furent",
    "a", "ont", "avait", "avaient", "aura", "auront", "aurait", "auraient",
    "ai", "avons", "avez", "eut", "eurent", "ait", "aient",
    "fait", "font", "faisait", "faisaient", "fera", "feront", "ferait", "fit",
    "va", "vont", "allait", "allaient", "ira", "iront", "irait",
    "peut", "peuvent", "pouvait", "pouvaient", "pourra", "pourront", "pourrait",
    "doit", "doivent", "devait", "devaient", "devra", "devront", "devrait",
    "veut", "veulent", "voulait", "voulaient", "voudra", "voudrait",
    "sait", "savent", "savait", "saura", "saurait",
    "faut", "fallait", "faudra", "faudrait",
    "vient", "viennent", "venait", "viendra", "vint",
    "tient", "tiennent", "tenait", "tiendra",
    "prend", "prennent", "prenait", "prendra", "prendrait",
    "met", "mettent", "mettait", "mettra", "mit",
    "voit", "voient", "voyait", "verra", "vit",
    "dit", "disent", "disait", "dira", "dirait",
    "reste", "restent", "restait", "restera",
    "devient", "deviennent", "devenait", "deviendra",
    "passe", "passent", "passait", "passera",
    "perd", "perdent", "perdait", "perdra",
    "gagne", "gagnent", "gagnait", "gagnera",
    "coûte", "coûtent", "coûtait", "coûtera",
    "bloque", "bloquent", "bloquait", "bloquera",
    "ferme", "ferment", "fermait", "fermera",
    "ouvre", "ouvrent", "ouvrait", "ouvrira",
    "manque", "manquent", "manquait", "manquera",
    "existe", "existent", "existait", "existera",
    "arrive", "arrivent", "arrivait", "arrivera",
    "part", "partent", "partait", "partira",
    "change", "changent", "changeait", "changera",
    "tombe", "tombent", "tombait", "tombera",
    "monte", "montent", "montait", "montera",
    "baisse", "baissent", "baissait", "baissera",
    "attend", "attendent", "attendait", "attendra",
    "cherche", "cherchent", "cherchait", "cherchera",
    "trouve", "trouvent", "trouvait", "trouvera",
    "achète", "achètent", "achetait", "achètera",
    "vend", "vendent", "vendait", "vendra",
    "paie", "paient", "payent", "payait", "paiera",
    "commence", "commencent", "commencera",
    "finit", "finissent", "finira",
    "arrête", "arrêtent", "arrêtait", "arrêtera",
    "décide", "décident", "décidait", "décidera",
    "choisit", "choisissent", "choisira",
    "refuse", "refusent", "refusera", "accepte", "acceptent",
    "signe", "signent", "signera", "recrute", "recrutent",
    "vaut", "valent", "valait", "vaudra",
    "compte", "comptent", "comptait", "comptera",
    "suffit", "suffisent", "suffisait", "suffira",
    "dépend", "dépendent", "dépendait",
    "repose", "reposent", "reposait",
    "révèle", "révèlent", "révélait", "révélera",
    "montre", "montrent", "montrait", "montrera",
    "prouve", "prouvent", "impose", "imposent", "imposera",
    "empêche", "empêchent", "oblige", "obligent",
    "risque", "risquent", "ignore", "ignorent",
    "pardonne", "pardonnent", "confond", "confondent",
    "hésite", "hésitent", "tue", "tuent", "sauve", "sauvent",
    "explose", "explosent", "sature", "saturent",
    "appelle", "appellent", "rappelle", "rappellent",
    "demande", "demandent", "répond", "répondent", "répondra",
    "traduit", "traduisent", "produit", "produisent",
    "tranche", "tranchent", "assume", "assument",
    "gêne", "gênent", "freine", "freinent", "casse", "cassent",
    "protège", "protègent", "sépare", "séparent", "organise", "organisent",
    "oriente", "orientent", "engage", "engagent", "décale", "décalent",
    "retarde", "retardent", "ralentit", "ralentissent", "accélère", "accélèrent",
    "améliore", "améliorent", "dégrade", "dégradent", "corrige", "corrigent",
    "alimente", "alimentent", "nourrit", "nourrissent", "éclaire", "éclairent",
    "masque", "masquent", "cache", "cachent", "rapporte", "rapportent",
    "économise", "économisent", "dépense", "dépensent", "facture", "facturent",
    "encaisse", "encaissent", "relance", "relancent", "fidélise", "fidélisent",
    "attire", "attirent", "repousse", "repoussent", "éloigne", "éloignent",
    "rapproche", "rapprochent", "connecte", "connectent", "isole", "isolent",
    "déborde", "débordent", "épuise", "épuisent", "use", "usent", "abîme",
    "répare", "réparent", "remplace", "remplacent", "supprime", "suppriment",
    "ajoute", "ajoutent", "réduit", "réduisent", "augmente", "augmentent",
    "double", "doublent", "triple", "triplent", "divise", "divisent",
    "multiplie", "multiplient", "dépasse", "dépassent", "atteint", "atteignent",
    "rate", "ratent", "échoue", "échouent", "réussit", "réussissent",
    "tarde", "tardent", "traîne", "traînent", "pèse", "pèsent", "colle",
    "collent", "glisse", "glissent", "dérive", "dérivent", "circule",
    "circulent", "remonte", "remontent", "descend", "descendent",
    "précède", "précèdent", "succède", "succèdent", "revient", "reviennent",
    "sort", "sortent", "entre", "entrent", "reprend", "reprennent",
}

# Terminaisons quasi exclusivement verbales en français. Elles complètent la
# liste ci-dessus sans la remplacer.
TERMINAISONS_VERBALES = (
    "ait", "aient", "era", "eras", "erez", "eront",
    "erait", "eraient", "irent", "èrent", "issent", "ira", "iront",
)

# « -ons » et « -ez » ne valent comme formes verbales qu'accompagnés de leur
# pronom sujet : sans cette règle, « recommandations » et « chez » passent pour
# des verbes conjugués et éteignent la détection des titres-thèmes.
TERMINAISONS_VERBALES_A_PRONOM = {"ons": "nous", "ez": "vous"}

# Noms à terminaison verbale trompeuse.
FAUX_VERBES = {
    "chez", "assez", "nez", "rez", "poumons", "talons", "salons", "jalons",
    "portrait", "portraits", "extrait", "extraits", "trait", "traits",
    "souhait", "souhaits", "attrait", "lait", "forfait", "forfaits",
    "retrait", "retraits", "méfait", "bienfait", "bienfaits", "parfait",
    "imparfait", "plait", "plaît",
}

# Titres de structure d'un livrable WAOUP. Ils nomment une section du squelette,
# ils n'ont pas à conclure. À ajuster avec l'équipe si la structure évolue.
TITRES_DE_STRUCTURE = {
    "sommaire", "table des matières", "annexe", "annexes", "glossaire",
    "sources", "références", "contacts", "next steps", "prochaines étapes",
    "méthodologie", "méthodologie et profils", "cadrage", "budget",
    "calendrier", "périmètre", "hors périmètre", "le dispositif", "dispositif",
    "verbatims", "introduction", "conclusion", "synthèse", "remerciements",
    "décoder", "dessiner", "développer", "déployer",
    # Documents internes : notes de méthode, skills, README. Ces intitulés
    # nomment une partie du document, ils n'ont pas à conclure.
    "procédure", "pièges", "quand l'utiliser", "format de sortie", "posture",
    "grille de lecture", "ancrage", "structure", "objet", "installation",
    "utilisation", "usage", "licence", "sommaire du kit",
}

# Adverbes en -ment les plus courants du registre conseil. Repérés d'office,
# sans passer par la règle du déterminant.
ADVERBES_EN_MENT = {
    "notamment", "également", "rapidement", "clairement", "précisément",
    "particulièrement", "véritablement", "réellement", "profondément",
    "largement", "fortement", "directement", "simplement", "seulement",
    "évidemment", "naturellement", "essentiellement", "principalement",
    "globalement", "concrètement", "effectivement", "forcément", "finalement",
    "généralement", "systématiquement", "structurellement", "historiquement",
    "culturellement", "opérationnellement", "stratégiquement", "totalement",
    "parfaitement", "difficilement", "facilement", "durablement",
    "régulièrement", "immédiatement", "progressivement", "vivement",
    "vraiment", "absolument", "quasiment", "poliment", "gentiment", "joliment",
    "hardiment", "résolument", "éperdument", "dûment", "assidûment", "crûment",
    "goulûment", "ingénument", "prudemment", "fréquemment", "apparemment",
    "différemment", "suffisamment", "abondamment", "constamment", "patiemment",
    "violemment", "intelligemment", "décemment", "sciemment",
    "nettement", "légèrement", "massivement", "constamment", "uniquement",
    "principalement", "actuellement", "prochainement", "récemment",
}

# Terminaisons réellement adverbiales. Sans ce filtre, « ferment », « forment »
# et « assument », qui sont des verbes, seraient comptés comme des adverbes.
TERMINAISONS_ADVERBIALES = ("ement", "ément", "amment", "emment")

# Noms en -ment. Ils portent la même finale que les adverbes de manière sans en
# être : sans cette liste, « le déploiement » gonflerait la densité d'adverbes.
NOMS_EN_MENT = {
    "comment", "moment", "ciment", "aliment", "argument", "instrument",
    "monument", "régiment", "sentiment", "bâtiment", "vêtement", "compliment",
    "événement", "evenement", "département", "gouvernement", "management",
    "environnement", "équipement", "engagement", "changement", "traitement",
    "développement", "investissement", "financement", "recrutement",
    "déploiement", "accompagnement", "positionnement", "fonctionnement",
    "alignement", "règlement", "paiement", "jugement", "mouvement",
    "abonnement", "logement", "licenciement", "renseignement", "enseignement",
    "comportement", "encadrement", "classement", "lancement", "remplacement",
    "placement", "avancement", "élément", "complément", "supplément",
    "document", "segment", "fragment", "testament", "parlement", "appartement",
    "raisonnement", "cheminement", "aboutissement", "élargissement",
    "établissement", "assainissement", "vieillissement", "revirement",
    "entraînement", "étonnement", "empêchement", "regroupement", "rassemblement",
    "aménagement", "agrandissement", "consentement", "dénouement",
}

# Déterminants et prépositions qui, devant un mot en -ment, signalent un nom
# (« le déploiement ») et non un adverbe (« déployer rapidement »).
DETERMINANTS = {
    "le", "la", "les", "l", "un", "une", "des", "du", "de", "d", "au", "aux",
    "ce", "cet", "cette", "ces", "son", "sa", "ses", "leur", "leurs",
    "notre", "nos", "votre", "vos", "mon", "ma", "mes", "ton", "ta", "tes",
    "chaque", "tout", "toute", "tous", "toutes", "plusieurs", "certains",
    "certaines", "quelques", "aucun", "aucune", "en", "par", "pour", "sur",
    "avec", "sans", "dans", "vers", "selon", "après", "avant", "chez", "entre",
}

# Abréviations dont le point ne termine pas une phrase.
ABREVIATIONS = {
    "m", "mm", "mme", "mmes", "dr", "pr", "st", "ste", "cf", "etc", "p", "ex",
    "art", "al", "env", "min", "max", "réf", "ref", "n", "fig", "vol", "éd",
    "ed", "tél", "av", "bd", "no", "nos", "ca", "hab",
}

# ---------------------------------------------------------------------------
# Structures
# ---------------------------------------------------------------------------


@dataclass
class Occurrence:
    categorie: str
    motif: str
    debut: int
    fin: int
    confiance: str = "haute"          # « haute » ou « à vérifier »
    protege: bool = False             # dans un verbatim ou une citation
    ligne: int = 0
    colonne: int = 0
    extrait: str = ""


@dataclass
class Texte:
    """Le texte préparé, ses index et ses zones protégées."""

    source: str
    brut: str
    analyse: str                      # même longueur que brut, zones neutralisées
    normalise: str                    # même longueur, apostrophes et espaces unifiés
    debuts_de_ligne: list = field(default_factory=list)
    zones_protegees: list = field(default_factory=list)
    phrases: list = field(default_factory=list)
    titres: list = field(default_factory=list)
    nb_mots: int = 0
    nb_lignes: int = 0


class ErreurEntree(Exception):
    """Erreur imputable à l'entrée : fichier, encodage, liste de mots."""


# ---------------------------------------------------------------------------
# Préparation du texte
# ---------------------------------------------------------------------------

RE_MOT = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)
RE_ENTITE_HTML = re.compile(r"&(?:#\d{1,6}|#[xX][0-9a-fA-F]{1,5}|[a-zA-Z][a-zA-Z0-9]{1,10});")
RE_COMMENTAIRE_HTML = re.compile(r"<!--.*?-->", re.S)
RE_BLOC_HTML = re.compile(r"<(script|style)\b[^>]*>.*?</\1\s*>", re.S | re.I)
RE_BALISE_BLOC = re.compile(
    r"</?(?:p|div|li|tr|td|th|h[1-6]|br|hr|section|article|header|footer|nav"
    r"|ul|ol|table|blockquote|figure|figcaption)\b[^>]*>",
    re.I | re.S,
)
RE_BALISE = re.compile(r"<[^<>]{0,500}>", re.S)
RE_TITRE_HTML = re.compile(r"<h([1-6])\b[^>]*>", re.I | re.S)
RE_CITATION_HTML_OUVRANTE = re.compile(r"<(?:blockquote|q|cite)\b[^>]*>", re.I | re.S)
RE_CITATION_HTML_FERMANTE = re.compile(r"</(?:blockquote|q|cite)\s*>", re.I | re.S)
RE_FRONT_MATTER = re.compile(r"\A---\n.*?\n---[ \t]*(?:\n|\Z)", re.S)
RE_BLOC_CODE = re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$", re.S | re.M)
RE_CODE_INLINE = re.compile(r"`[^`\n]{1,200}`")
RE_URL = re.compile(r"(?:https?://|www\.)[^\s<>\)\]]{2,300}")
RE_CIBLE_LIEN = re.compile(r"\]\([^)\n]{1,300}\)")

RE_CITATION_CHEVRONS = re.compile(r"«[^»]{0,3000}»", re.S)
RE_CITATION_COURBES = re.compile(r"“[^”]{0,3000}”", re.S)
RE_CITATION_DROITES = re.compile(r'"[^"\n]{3,400}"')
RE_LIGNE_CITATION = re.compile(r"^[ \t]{0,3}>[^\n]*$", re.M)

RE_TITRE = re.compile(
    r"(?:^|(?<=" + SEPARATEUR_BLOC + r"))[ \t]{0,3}(#{1,6})[ \t]+"
    r"([^\n" + SEPARATEUR_BLOC + r"]+?)[ \t]*#*[ \t]*(?=$|" + SEPARATEUR_BLOC + r")",
    re.M,
)


def _blanchir(fragment):
    """Remplace un fragment par des espaces en gardant longueur et sauts de ligne."""
    return "".join("\n" if c == "\n" else " " for c in fragment)


def _neutraliser(texte, motif):
    return motif.sub(lambda m: _blanchir(m.group(0)), texte)


def _remplacer_par_marqueur(marqueur):
    """Substitue une balise par un marqueur d'un caractère, complété d'espaces.
    La longueur et les sauts de ligne sont conservés."""

    def _sub(correspondance):
        balise = correspondance.group(0)
        if "\n" in balise or len(balise) < len(marqueur):
            return _blanchir(balise)
        return marqueur + " " * (len(balise) - len(marqueur))

    return _sub


def _titre_html(correspondance):
    """« <h2 class="x"> » devient « ␞## », pour que les titres HTML et Markdown
    passent par le même détecteur."""
    balise = correspondance.group(0)
    marqueur = SEPARATEUR_BLOC + "#" * int(correspondance.group(1))
    if "\n" in balise or len(balise) < len(marqueur):
        return _blanchir(balise)
    return marqueur + " " * (len(balise) - len(marqueur))


def _remplacer_entites(texte):
    """Décode les entités HTML. Le texte raccourcit, ce qui décale les colonnes
    mais jamais les lignes : aucune entité ne contient de saut de ligne, et
    c'est le nombre de sauts de ligne qui porte la numérotation du rapport.
    Compléter par des espaces serait pire : « propos&eacute;e » deviendrait
    « proposé e » et le mot cesserait d'être trouvable."""

    def _sub(m):
        brut = m.group(0)
        try:
            decode = html.unescape(brut)
        except Exception:
            return brut
        if decode == brut or "\n" in decode:
            return brut
        if decode in "<>":  # ne pas fabriquer de fausses balises après nettoyage
            return " " * len(brut)
        return decode

    return RE_ENTITE_HTML.sub(_sub, texte)


def _ressemble_a_du_html(texte):
    echantillon = texte[:4000].lower()
    marqueurs = ("<html", "<body", "<!doctype html", "<div", "<p>", "<span", "<section")
    return any(marqueur in echantillon for marqueur in marqueurs)


def preparer(brut, source, forcer_html=False):
    """Construit le texte d'analyse : même longueur que l'original, zones
    non rédactionnelles neutralisées, apostrophes et espaces unifiés."""

    analyse = brut

    est_html = forcer_html or source.lower().endswith((".html", ".htm")) or _ressemble_a_du_html(brut)
    if est_html:
        analyse = _neutraliser(analyse, RE_COMMENTAIRE_HTML)
        analyse = _neutraliser(analyse, RE_BLOC_HTML)
        # Les citations HTML deviennent des guillemets français : elles rejoignent
        # les zones protégées, au même titre qu'un verbatim en « … ».
        analyse = RE_CITATION_HTML_OUVRANTE.sub(_remplacer_par_marqueur("«"), analyse)
        analyse = RE_CITATION_HTML_FERMANTE.sub(_remplacer_par_marqueur("»"), analyse)
        analyse = RE_TITRE_HTML.sub(_titre_html, analyse)
        analyse = RE_BALISE_BLOC.sub(_remplacer_par_marqueur(SEPARATEUR_BLOC), analyse)
        analyse = _neutraliser(analyse, RE_BALISE)
        analyse = _remplacer_entites(analyse)
    else:
        analyse = _neutraliser(analyse, RE_FRONT_MATTER)
        analyse = _neutraliser(analyse, RE_BLOC_CODE)
        analyse = _neutraliser(analyse, RE_CODE_INLINE)
        analyse = _neutraliser(analyse, RE_CIBLE_LIEN)

    analyse = _neutraliser(analyse, RE_URL)

    # Garde-fou : les numéros de ligne du rapport reposent sur la conservation
    # exacte des sauts de ligne. La longueur, elle, peut varier (entités HTML).
    if analyse.count("\n") != brut.count("\n"):
        raise ErreurEntree(
            "Erreur interne : la préparation du texte a modifié le découpage en "
            "lignes. Signalez le fichier d'entrée à l'auteur de la skill."
        )

    normalise = (
        analyse.replace("’", "'")
        .replace("‘", "'")
        .replace("\u00a0", " ")   # espace insécable
        .replace("\u202f", " ")   # espace insécable fine
        .replace("\u2009", " ")   # espace fine
    )

    texte = Texte(source=source, brut=brut, analyse=analyse, normalise=normalise)
    texte.debuts_de_ligne = [0] + [m.end() for m in re.finditer(r"\n", analyse)]
    texte.nb_lignes = analyse.count("\n") + 1
    texte.nb_mots = len(RE_MOT.findall(analyse))
    texte.zones_protegees = reperer_zones_protegees(analyse)
    texte.phrases = decouper_phrases(analyse)
    texte.titres = [
        (m.start(2), m.end(2), len(m.group(1)), m.group(2).strip())
        for m in RE_TITRE.finditer(analyse)
    ]
    return texte


def reperer_zones_protegees(texte):
    """Verbatims et citations : la skill interdit d'y toucher. On les repère
    pour les signaler à part, jamais pour les corriger."""
    zones = []
    for motif in (
        RE_CITATION_CHEVRONS,
        RE_CITATION_COURBES,
        RE_CITATION_DROITES,
        RE_LIGNE_CITATION,
    ):
        for m in motif.finditer(texte):
            zones.append((m.start(), m.end()))
    return sorted(zones)


def decouper_phrases(texte):
    """Découpe en phrases. Coupe sur la ponctuation forte, sur les lignes vides
    et devant les marqueurs de bloc Markdown, en épargnant les abréviations et
    les nombres à décimale."""
    coupures = [0]
    motif = re.compile(
        r"[.!?…]+[\"»)\]]*"
        r"|\n{2,}"
        r"|" + SEPARATEUR_BLOC + r"+"
        r"|\n(?=[ \t]*(?:#{1,6}\s|[-*+]\s|\d{1,3}[.)]\s|\||>))"
    )
    for m in motif.finditer(texte):
        trouve = m.group(0)
        if trouve[0] in ".!?…":
            avant = texte[: m.start()]
            dernier = re.search(r"([^\W_]+)$", avant)
            if dernier and dernier.group(1).lower() in ABREVIATIONS:
                continue
            suite = texte[m.end(): m.end() + 1]
            if avant[-1:].isdigit() and suite.isdigit():
                continue
        coupures.append(m.end())
    coupures.append(len(texte))

    phrases = []
    for i in range(len(coupures) - 1):
        debut, fin = coupures[i], coupures[i + 1]
        if fin <= debut:
            continue
        fragment = texte[debut:fin]
        if fragment.strip():
            phrases.append((debut, fin, fragment))
    return phrases


def ligne_et_colonne(texte, position):
    index = bisect.bisect_right(texte.debuts_de_ligne, position) - 1
    return index + 1, position - texte.debuts_de_ligne[index] + 1


def est_protegee(texte, debut, fin):
    for zdebut, zfin in texte.zones_protegees:
        if debut < zfin and fin > zdebut:
            return True
    return False


def extraire(texte, debut, fin):
    """Extrait lisible, recadré sur la phrase qui contient l'occurrence."""
    phrase_debut, phrase_fin = debut, fin
    for pdebut, pfin, _ in texte.phrases:
        if pdebut <= debut < pfin:
            phrase_debut, phrase_fin = pdebut, max(pfin, fin)
            break
    fragment = texte.analyse[phrase_debut:phrase_fin]
    fragment = fragment.replace(SEPARATEUR_BLOC, " ")
    fragment = re.sub(r"\s+", " ", fragment)
    fragment = re.sub(r"«\s*«", "«", fragment)
    fragment = re.sub(r"»\s*»", "»", fragment)
    fragment = fragment.strip(" \t*_#>")
    if len(fragment) > LONGUEUR_EXTRAIT:
        # On recadre autour du passage fautif plutôt que de couper bêtement au début.
        decalage = max(0, debut - phrase_debut - LONGUEUR_EXTRAIT // 3)
        fragment = fragment[decalage: decalage + LONGUEUR_EXTRAIT].strip()
        fragment = ("…" if decalage else "") + fragment + "…"
    return fragment


def phrase_contenant(texte, position):
    for debut, fin, fragment in texte.phrases:
        if debut <= position < fin:
            return debut, fin, fragment
    return 0, len(texte.analyse), texte.analyse


def est_debut_de_phrase(texte, position):
    """Vrai si la position ouvre une phrase, en tolérant les marqueurs Markdown
    (puce, gras, citation, titre) qui la précèdent."""
    avant = texte.normalise[:position]
    avant = re.sub(r"[ \t>*_#\-–—•]+$", "", avant)
    if not avant:
        return True
    return avant[-1] in ".!?…:\n" + SEPARATEUR_BLOC

# ---------------------------------------------------------------------------
# Détecteur 1 : les tirets employés comme incise
# ---------------------------------------------------------------------------

RE_TIRET = re.compile("[" + TIRET_CADRATIN + TIRET_DEMI_CADRATIN + "]")
RE_DEBUT_DE_LIGNE = re.compile(r"(?:^|\n)[ \t>*+\-|]*$")
RE_FIN_NUMERIQUE = re.compile(r"(?:\d|\bh|\bp|\bpp)[  \t]*$", re.I)
RE_DEBUT_NUMERIQUE = re.compile(r"[  \t]*\d")
RE_CELLULE_AVANT = re.compile(r"\|[ \t]*$")
RE_CELLULE_APRES = re.compile(r"^[ \t]*\|")


def detecter_tirets(texte):
    occurrences = []
    for m in RE_TIRET.finditer(texte.normalise):
        debut, fin = m.start(), m.end()
        avant = texte.normalise[max(0, debut - 40):debut]
        apres = texte.normalise[fin:fin + 40]

        # Tiret en tête de ligne : puce de liste ou tiret de dialogue.
        if RE_DEBUT_DE_LIGNE.search(avant):
            continue
        # Plage de valeurs ou d'horaires : « 2019 – 2024 », « 14 h — 16 h ».
        if RE_FIN_NUMERIQUE.search(avant) and RE_DEBUT_NUMERIQUE.match(apres):
            continue
        # Tiret isolé en fin de ligne : reste de mise en page, pas une incise.
        if not apres.strip():
            continue
        # Cellule de tableau réduite à un tiret : la convention veut dire
        # « sans objet », ce n'est pas une incise.
        if RE_CELLULE_AVANT.search(avant) and RE_CELLULE_APRES.match(apres):
            continue

        est_cadratin = m.group(0) == TIRET_CADRATIN
        occurrences.append(
            Occurrence(
                categorie="tiret",
                motif="tiret cadratin" if est_cadratin else "tiret demi-cadratin",
                debut=debut,
                fin=fin,
            )
        )
    return occurrences


# ---------------------------------------------------------------------------
# Détecteur 2 : la négation-contraste
# ---------------------------------------------------------------------------

_P = str(PORTEE_NEGATION)
_CORPS = r"[^.!?\n" + SEPARATEUR_BLOC + r"]{1," + _P + r"}?"

MOTIFS_NEGATION = [
    ("ce n'est pas … c'est", r"\bce\s+n'est\s+pas\b" + _CORPS + r"[,;]?\s*c'est\b"),
    ("ce ne sont pas … ce sont", r"\bce\s+ne\s+sont\s+pas\b" + _CORPS + r"[,;]?\s*ce\s+sont\b"),
    ("… n'est pas …, c'est …", r"\bn'(?:est|était|sera)\s+pas\b" + _CORPS + r",\s*c'est\b"),
    ("… ne sont pas …, ce sont …", r"\bne\s+sont\s+pas\b" + _CORPS + r",\s*ce\s+sont\b"),
    ("il ne s'agit pas de … mais", r"\bne\s+s'agit\s+pas\s+(?:tant\s+)?(?:d'|de\s|du\s|des\s)" + _CORPS + r"\bmais\b"),
    ("il ne s'agit pas tant de … que", r"\bne\s+s'agit\s+pas\s+tant\s+(?:d'|de\s|du\s|des\s)" + _CORPS + r"\bque\b"),
    ("non pas … mais", r"\bnon\s+pas\b" + _CORPS + r"\bmais\b"),
    ("non seulement … mais", r"\bnon\s+seulement\b" + _CORPS + r"\bmais\b"),
    ("pas seulement … mais", r"\bpas\s+seulement\b" + _CORPS + r"\bmais\b"),
    ("loin d'être …, c'est", r"\bloin\s+d'être\b" + _CORPS + r",\s*(?:c'est|il\s+est|elle\s+est|ils\s+sont|elles\s+sont)\b"),
    ("… pas … mais bien …", r"\bpas\b" + _CORPS + r"\bmais\s+bien\b"),
    ("n'est pas tant … que", r"\bn'(?:est|sont|était)\s+pas\s+tant\b" + _CORPS + r"\bque\b"),
    ("plus qu'un …, c'est", r"\bplus\s+qu'une?\b" + _CORPS + r",\s*c'est\b"),
    (
        "… n'est pas …, mais …",
        r"\bn'(?:est|était|sera)\s+pas\b" + _CORPS
        + r",\s*mais\s+(?:bien\s+)?(?:un|une|des|le|la|les|l'|d'|de\s|du\s|celui|celle|ceux|celles)\b",
    ),
    (
        "… ne sont pas …, mais …",
        r"\bne\s+sont\s+pas\b" + _CORPS
        + r",\s*mais\s+(?:bien\s+)?(?:un|une|des|le|la|les|l'|d'|de\s|du\s|celui|celle|ceux|celles)\b",
    ),
]
MOTIFS_NEGATION = [(nom, re.compile(motif, re.I)) for nom, motif in MOTIFS_NEGATION]

# Après « mais », un sujet de première ou deuxième personne annonce une vraie
# proposition (« mais nous pouvons le faire ») : opposition légitime, pas un tic.
RE_SUJET_PERSONNEL = re.compile(r"\s*(?:je|j'|tu|nous|vous|on)\b", re.I)


def detecter_negation_contraste(texte):
    occurrences = []
    for nom, motif in MOTIFS_NEGATION:
        for m in motif.finditer(texte.normalise):
            if m.group(0).rstrip().lower().endswith("mais"):
                if RE_SUJET_PERSONNEL.match(texte.normalise[m.end(): m.end() + 12]):
                    continue
            occurrences.append(
                Occurrence(
                    categorie="negation-contraste",
                    motif=nom,
                    debut=m.start(),
                    fin=m.end(),
                )
            )
    return dedoublonner(occurrences)


def dedoublonner(occurrences):
    """Deux motifs peuvent décrire le même passage. On garde le plus long."""
    retenues = []
    for occ in sorted(occurrences, key=lambda o: (o.debut, -(o.fin - o.debut))):
        if any(occ.debut < autre.fin and occ.fin > autre.debut for autre in retenues):
            continue
        retenues.append(occ)
    return retenues


# ---------------------------------------------------------------------------
# Détecteur 3 : les triades
# ---------------------------------------------------------------------------

# Un membre de triade est une suite de mots sans ponctuation interne. La
# fenêtre est bornée en nombre de mots plutôt qu'en caractères : c'est ce qui
# permet au moteur de glisser jusqu'au bon découpage quand la phrase est longue.
_MOT_MEMBRE = r"[^\s,.;:!?()\[\]«»\n" + SEPARATEUR_BLOC + r"]+"


def _fenetre_de_membre(mots_max):
    return r"(?:" + _MOT_MEMBRE + r"[ \t]+){0," + str(mots_max - 1) + r"}" + _MOT_MEMBRE


RE_TRIADE = re.compile(
    "(" + _fenetre_de_membre(MOTS_MAX_PREMIER_MEMBRE) + r")[ \t]*,[ \t]*"
    "(" + _fenetre_de_membre(MOTS_MAX_MEMBRE_TRIADE) + r")\s+et\s+"
    "(" + _fenetre_de_membre(MOTS_MAX_MEMBRE_TRIADE) + ")"
    r"(?=[.,;:!?)\]\n" + SEPARATEUR_BLOC + r"]|$)"
)


def dernier_mot(fragment):
    mots = RE_MOT.findall(fragment)
    return mots[-1].lower() if mots else ""


def est_adjectif(mot):
    """Reconnaît un adjectif par sa terminaison, en écartant les noms du
    registre conseil qui portent les mêmes finales."""
    if len(mot) < LONGUEUR_MIN_ADJECTIF:
        return False
    if mot in NOMS_A_TERMINAISON_TROMPEUSE:
        return False
    # -ment et -ments ne sont jamais des adjectifs : ce sont des noms
    # (« déploiement ») ou des adverbes (« rapidement »).
    if mot.endswith("ment") or mot.endswith("ments"):
        return False
    if mot in NOMS_A_TERMINAISON_TROMPEUSE_BIS:
        return False
    if mot in ADJECTIFS_FREQUENTS:
        return True
    return mot.endswith(SUFFIXES_ADJECTIFS)


def qualifiant_du_dernier_membre(fragment):
    """Le troisième membre d'une triade est souvent collé au verbe de la phrase
    (« impactante permettrait »). Dans ce cas, le qualifiant est le premier mot
    et le reste appartient déjà à la suite de la phrase."""
    mots = RE_MOT.findall(fragment)
    if not mots:
        return ""
    dernier = mots[-1].lower()
    if est_adjectif(dernier) or len(mots) == 1:
        return dernier
    reste = " ".join(mots[1:])
    if contient_verbe_conjugue(reste):
        return mots[0].lower()
    return dernier


def membre_factuel(fragment, premier_membre, ouvre_la_phrase):
    """Un membre qui porte un chiffre, un nom propre ou trop de mots relève de
    l'énumération de faits, pas de la triade rhétorique."""
    if re.search(r"\d", fragment):
        return True
    mots = RE_MOT.findall(fragment)
    plafond = MOTS_MAX_PREMIER_MEMBRE if premier_membre else MOTS_MAX_MEMBRE_TRIADE
    if not mots or len(mots) > plafond:
        return True
    # Une majuscule ailleurs qu'en tête de phrase signale un nom propre.
    debut = 1 if (premier_membre and ouvre_la_phrase) else 0
    return any(mot[:1].isupper() for mot in mots[debut:])


def detecter_triades(texte):
    occurrences = []
    for m in RE_TRIADE.finditer(texte.normalise):
        membres = [m.group(1).strip(" \t*_"), m.group(2).strip(), m.group(3).strip()]
        if not all(membres):
            continue

        phrase_debut, _, _ = phrase_contenant(texte, m.start())
        ouvre_la_phrase = texte.normalise[phrase_debut:m.start(1)].strip(" \t*_#>-") == ""

        if any(
            membre_factuel(membre, index == 0, ouvre_la_phrase)
            for index, membre in enumerate(membres)
        ):
            continue

        finales = [dernier_mot(membre) for membre in membres[:2]]
        finales.append(qualifiant_du_dernier_membre(membres[2]))
        if not all(est_adjectif(mot) for mot in finales):
            continue

        # Triade d'adjectifs : le premier membre porte le nom qualifié, les deux
        # suivants sont des adjectifs nus. « claire, structurée et actionnable ».
        deux_derniers_simples = all(
            len(RE_MOT.findall(membre)) == 1 for membre in membres[1:]
        )
        if deux_derniers_simples:
            confiance, motif = "haute", "triade d'adjectifs"
        else:
            confiance, motif = "à vérifier", "triade de groupes parallèles"

        occurrences.append(
            Occurrence(
                categorie="triade",
                motif=motif,
                debut=m.start(),
                fin=m.end(),
                confiance=confiance,
            )
        )
    return dedoublonner(occurrences)


# ---------------------------------------------------------------------------
# Détecteur 4 : les mots creux
# ---------------------------------------------------------------------------


def charger_mots_creux(chemin, obligatoire):
    """Lit la liste externe. Une expression par ligne, « # » pour un commentaire,
    « ? » en tête pour une expression dont le caractère fautif dépend du sens."""
    if not os.path.exists(chemin):
        if obligatoire:
            raise ErreurEntree("Liste de mots creux introuvable : " + chemin)
        return [], "Liste de mots creux introuvable (" + chemin + "), catégorie non analysée."
    try:
        with open(chemin, "r", encoding="utf-8") as flux:
            lignes = flux.read().splitlines()
    except OSError as erreur:
        raise ErreurEntree("Liste de mots creux illisible : " + str(erreur))
    except UnicodeDecodeError:
        raise ErreurEntree("Liste de mots creux non encodée en UTF-8 : " + chemin)

    entrees = []
    for ligne in lignes:
        ligne = ligne.split("#", 1)[0].strip()
        if not ligne:
            continue
        a_verifier = ligne.startswith("?")
        expression = ligne.lstrip("?").strip()
        if not expression:
            continue
        entrees.append((expression, a_verifier))

    if not entrees:
        message = "Liste de mots creux vide (" + chemin + "), catégorie non analysée."
        return [], message
    return entrees, None


def compiler_expression(expression):
    """« il convient de » devient un motif tolérant aux espaces multiples et
    aux deux formes d'apostrophe."""
    morceaux = [re.escape(mot) for mot in expression.split()]
    corps = r"\s+".join(morceaux).replace(r"\'", r"'").replace("'", r"['’]\s*")
    return re.compile(r"(?<![^\W_])" + corps + r"(?![^\W_])", re.I)


def detecter_mots_creux(texte, entrees):
    occurrences = []
    for expression, a_verifier in entrees:
        try:
            motif = compiler_expression(expression)
        except re.error:
            continue
        for m in motif.finditer(texte.normalise):
            occurrences.append(
                Occurrence(
                    categorie="mot-creux",
                    motif="« " + expression + " »",
                    debut=m.start(),
                    fin=m.end(),
                    confiance="à vérifier" if a_verifier else "haute",
                )
            )
    return dedoublonner(occurrences)


# ---------------------------------------------------------------------------
# Détecteur 5 : les chutes de paragraphe
# ---------------------------------------------------------------------------

# (expression, exige d'ouvrir une phrase)
CHUTES = [
    ("en somme", True),
    ("en définitive", True),
    ("en résumé", True),
    ("pour résumer", True),
    ("pour conclure", True),
    ("en conclusion", True),
    ("au final", False),
    ("in fine", False),
    ("au bout du compte", False),
    ("tout compte fait", False),
    ("en fin de compte", False),
    ("ainsi, on peut dire", False),
    ("on peut donc dire", False),
    ("on peut ainsi dire", False),
    ("on retiendra", True),
    ("ce qu'il faut retenir", True),
    ("il ressort de tout cela", False),
    ("cela étant dit", False),
    ("ceci étant dit", False),
    ("en un mot", True),
    ("pour le dire autrement", False),
    ("autrement dit", True),
    ("en définitive, c'est", False),
    ("à l'arrivée", True),
    ("au terme de cette analyse", False),
]
CHUTES = [(expression, compiler_expression(expression), debut) for expression, debut in CHUTES]


def detecter_chutes(texte):
    occurrences = []
    for expression, motif, exige_debut in CHUTES:
        for m in motif.finditer(texte.normalise):
            if exige_debut and not est_debut_de_phrase(texte, m.start()):
                continue
            occurrences.append(
                Occurrence(
                    categorie="chute",
                    motif="« " + expression + " »",
                    debut=m.start(),
                    fin=m.end(),
                )
            )
    return dedoublonner(occurrences)


# ---------------------------------------------------------------------------
# Détecteur 6 : l'ouverture de politesse
# ---------------------------------------------------------------------------

# (expression, confiance). « Voici » et « Merci pour » peuvent ouvrir un mail
# légitime : ils sortent en « à vérifier », le rédacteur arbitre.
OUVERTURES = [
    ("bien sûr", "haute"),
    ("bien entendu", "haute"),
    ("excellente question", "haute"),
    ("très bonne question", "haute"),
    ("bonne question", "haute"),
    ("avec plaisir", "haute"),
    ("absolument", "haute"),
    ("tout à fait", "haute"),
    ("parfait", "haute"),
    ("je comprends", "haute"),
    ("j'espère que", "haute"),
    ("voici", "à vérifier"),
    ("vous trouverez ci-dessous", "à vérifier"),
    ("merci pour", "à vérifier"),
    ("dans ce document, nous allons", "haute"),
    ("dans cette note, nous allons", "haute"),
    ("je vais vous présenter", "haute"),
    ("permettez-moi", "haute"),
]
OUVERTURES = [
    (expression, re.compile(r"^\W{0,4}" + compiler_expression(expression).pattern, re.I), confiance)
    for expression, confiance in OUVERTURES
]


def lignes_de_contenu(texte):
    """Les premières lignes rédigées, hors titres, séparateurs et lignes vides."""
    retenues = []
    for index, debut in enumerate(texte.debuts_de_ligne):
        fin = texte.debuts_de_ligne[index + 1] if index + 1 < len(texte.debuts_de_ligne) else len(texte.analyse)
        ligne = texte.analyse[debut:fin].replace(SEPARATEUR_BLOC, " ")
        depouille = ligne.strip()
        if not depouille:
            continue
        if depouille.startswith("#") or set(depouille) <= set("-=_*| "):
            continue
        decalage = len(ligne) - len(ligne.lstrip())
        retenues.append((debut + decalage, depouille))
        if len(retenues) >= LIGNES_CONTENU_OUVERTURE:
            break
    return retenues


def detecter_ouvertures(texte):
    occurrences = []
    for position, ligne in lignes_de_contenu(texte):
        ligne_normalisee = ligne.replace("’", "'")
        for expression, motif, confiance in OUVERTURES:
            m = motif.match(ligne_normalisee)
            if not m:
                continue
            occurrences.append(
                Occurrence(
                    categorie="ouverture",
                    motif="« " + expression + " » en tête de texte",
                    debut=position + m.start(),
                    fin=position + m.end(),
                    confiance=confiance,
                )
            )
    return dedoublonner(occurrences)


# ---------------------------------------------------------------------------
# Détecteur 7 : les titres-thèmes
# ---------------------------------------------------------------------------


def contient_verbe_conjugue(phrase):
    mots = [mot.lower() for mot in RE_MOT.findall(phrase.replace("’", "'"))]
    if not mots:
        return False
    # Une négation « ne … pas » suppose un verbe conjugué entre les deux.
    if ("ne" in mots or "n" in mots) and any(
        negation in mots for negation in ("pas", "plus", "jamais", "rien", "aucun", "que")
    ):
        return True
    for index, mot in enumerate(mots):
        base = mot.split("'")[-1] if "'" in mot else mot
        if base in VERBES_CONJUGUES or mot in VERBES_CONJUGUES:
            return True
        if base in FAUX_VERBES:
            continue
        if len(base) >= 5 and base.endswith(TERMINAISONS_VERBALES):
            return True
        for terminaison, pronom in TERMINAISONS_VERBALES_A_PRONOM.items():
            if len(base) >= 5 and base.endswith(terminaison):
                if index > 0 and mots[index - 1].lower() == pronom:
                    return True
    return False


def detecter_titres_themes(texte):
    occurrences = []
    for index, (debut, fin, niveau, intitule) in enumerate(texte.titres):
        nettoye = re.sub(r"[*_`]", "", intitule).strip()
        if not nettoye:
            continue
        # Le titre du document nomme le document : ce n'est pas un titre-thème.
        if index == 0 and niveau == 1:
            continue
        cle = re.sub(r"^(le|la|les|l'|un|une|des|nos|vos|notre|votre)\s+", "", nettoye.lower())
        if nettoye.lower() in TITRES_DE_STRUCTURE or cle in TITRES_DE_STRUCTURE:
            continue
        # Un titre qui porte un chiffre énonce déjà un fait.
        if re.search(r"\d", nettoye):
            continue
        if nettoye.endswith("?"):
            continue
        if contient_verbe_conjugue(nettoye):
            continue
        occurrences.append(
            Occurrence(
                categorie="titre-theme",
                motif="titre sans verbe conjugué",
                debut=debut,
                fin=fin,
                confiance="à vérifier",
            )
        )
    return occurrences


# ---------------------------------------------------------------------------
# Mesures d'appoint : adverbes en -ment, phrases longues
# ---------------------------------------------------------------------------

RE_MOT_EN_MENT = re.compile(r"\b([^\W\d_]{2,}ment)\b", re.UNICODE)


def compter_adverbes(texte):
    """Un mot en -ment est un adverbe s'il figure dans la liste de référence,
    ou s'il n'est pas précédé d'un déterminant (« le déploiement » est un nom).
    Les verbatims sont exclus : la façon de parler du client ne se corrige pas."""
    releves = []
    for m in RE_MOT_EN_MENT.finditer(texte.analyse):
        if est_protegee(texte, m.start(), m.end()):
            continue
        mot = m.group(1).lower()
        if mot in ADVERBES_EN_MENT:
            releves.append((m.start(), mot))
            continue
        if mot in NOMS_EN_MENT:
            continue
        if not mot.endswith(TERMINAISONS_ADVERBIALES):
            continue
        avant = texte.analyse[max(0, m.start() - 30):m.start()]
        mots_avant = RE_MOT.findall(avant)
        precedent = mots_avant[-1].lower().rstrip("'’") if mots_avant else ""
        if precedent in DETERMINANTS:
            continue
        releves.append((m.start(), mot))
    return releves


def reperer_phrases_longues(texte):
    longues = []
    for debut, fin, fragment in texte.phrases:
        if est_protegee(texte, debut, fin):
            continue
        nettoye = re.sub(r"^[ \t>*_#\-]+", "", fragment)
        nb = len(RE_MOT.findall(nettoye))
        if nb > MOTS_PHRASE_LONGUE:
            longues.append((debut, nb))
    return longues

# ---------------------------------------------------------------------------
# Analyse complète
# ---------------------------------------------------------------------------


def analyser(texte, entrees_mots_creux):
    occurrences = []
    occurrences.extend(detecter_tirets(texte))
    occurrences.extend(detecter_negation_contraste(texte))
    occurrences.extend(detecter_triades(texte))
    occurrences.extend(detecter_mots_creux(texte, entrees_mots_creux))
    occurrences.extend(detecter_chutes(texte))
    occurrences.extend(detecter_ouvertures(texte))
    occurrences.extend(detecter_titres_themes(texte))

    for occ in occurrences:
        occ.ligne, occ.colonne = ligne_et_colonne(texte, occ.debut)
        occ.protege = est_protegee(texte, occ.debut, occ.fin)
        occ.extrait = extraire(texte, occ.debut, occ.fin)

    occurrences.sort(key=lambda o: (o.debut, o.categorie))
    return occurrences


def pour_mille(valeur, nb_mots):
    if nb_mots <= 0:
        return 0.0
    return round(valeur * 1000.0 / nb_mots, 1)


def calculer_verdict(indice_pour_mille, retenues, mots=None):
    if not retenues:
        return "envoyable", "Rien à signaler. Le texte ne porte aucun marqueur détectable."

    certains = [occ for occ in retenues if occ.confiance == "haute"]

    # Texte court : la densité s'affole. On juge au nombre de marqueurs certains.
    if mots is not None and mots < MOTS_POUR_DENSITE:
        if not certains:
            return "a_retoucher", (
                "À arbitrer. Aucun marqueur certain, mais des signaux à trancher. "
                "Texte trop court pour que la densité veuille dire quelque chose."
            )
        if len(certains) < CERTAINS_POUR_REPRENDRE:
            return "a_retoucher", (
                f"À retoucher. {len(certains)} marqueur(s) certain(s) sur un texte court : "
                "à corriger, sans conclure sur le style d'ensemble."
            )
        return "a_reprendre", "À reprendre. Le texte porte la signature d'une écriture automatique."

    if indice_pour_mille < SEUIL_ENVOYABLE:
        return "envoyable", "Envoyable. Les marques relevées restent sous le seuil de visibilité."
    if indice_pour_mille < SEUIL_RETOUCHE:
        return "a_retoucher", "À retoucher. Les passages signalés se voient à la lecture."
    # Un texte dont aucun signal n'est certain ne mérite pas le verdict le plus
    # dur : ce qui reste à arbitrer ne prouve rien à soi seul.
    if not certains:
        return "a_retoucher", (
            "À arbitrer. Aucun marqueur certain, mais assez de signaux douteux "
            "pour justifier une relecture."
        )
    # Une seule marque, même sur un texte dense, ne signe pas la machine.
    if len(certains) < CERTAINS_POUR_REPRENDRE:
        return "a_retoucher", (
            f"À retoucher. {len(certains)} marqueur(s) certain(s) : à corriger un par un."
        )
    return "a_reprendre", "À reprendre. Le texte porte la signature d'une écriture automatique."


# ---------------------------------------------------------------------------
# Rapport lisible
# ---------------------------------------------------------------------------

LARGEUR = 78


def nombre(valeur):
    """Format français : séparateur de milliers en espace insécable fine."""
    if isinstance(valeur, float):
        return ("%.1f" % valeur).replace(".", ",")
    return "{:,}".format(valeur).replace(",", " ")


def rendre_rapport(texte, occurrences, mesures, avertissements):
    lignes = []
    ajout = lignes.append

    ajout("=" * LARGEUR)
    ajout(" Détection de tics — " + os.path.basename(texte.source))
    ajout("=" * LARGEUR)
    ajout(
        " %s mots, %s lignes, %s titre(s)."
        % (nombre(texte.nb_mots), nombre(texte.nb_lignes), nombre(len(texte.titres)))
    )
    for message in avertissements:
        ajout(" ! " + message)
    ajout("")

    retenues = [occ for occ in occurrences if not occ.protege]
    protegees = [occ for occ in occurrences if occ.protege]

    if not retenues:
        ajout("Aucune occurrence retenue.")
        ajout("")

    for categorie in ORDRE_CATEGORIES:
        lot = [occ for occ in retenues if occ.categorie == categorie]
        if not lot:
            continue
        a_verifier = sum(1 for occ in lot if occ.confiance != "haute")
        entete = "%s — %d occurrence%s" % (
            LIBELLES_CATEGORIES[categorie],
            len(lot),
            "s" if len(lot) > 1 else "",
        )
        if a_verifier:
            entete += " (dont %d à vérifier)" % a_verifier
        ajout(entete)
        for occ in lot:
            marque = " [?]" if occ.confiance != "haute" else ""
            ajout("  L.%-5d %s%s" % (occ.ligne, occ.motif, marque))
            ajout("          " + occ.extrait)
        ajout("")

    if protegees:
        ajout("PROTÉGÉ — %d occurrence%s dans un verbatim ou une citation" % (
            len(protegees), "s" if len(protegees) > 1 else ""))
        ajout("  Ne pas corriger : la parole citée se reproduit telle quelle.")
        for occ in protegees:
            ajout("  L.%-5d %s" % (occ.ligne, occ.motif))
            ajout("          " + occ.extrait)
        ajout("")

    ajout("MESURES")
    gabarit = "  %-28s %7s   %s"
    ajout(gabarit % ("Occurrences retenues", nombre(len(retenues)),
                     "soit " + nombre(mesures["densite_pour_mille"]) + " pour mille mots"))
    ajout(gabarit % ("Indice de signature", nombre(mesures["indice"]),
                     "soit " + nombre(mesures["indice_pour_mille"]) + " pour mille mots"))
    ajout(gabarit % ("Adverbes en -ment", nombre(mesures["adverbes"]),
                     "soit " + nombre(mesures["adverbes_pour_mille"]) + " pour mille mots"))
    detail_longues = ""
    if mesures["phrases_longues"]:
        detail_longues = "(L." + ", L.".join(
            str(ligne) for ligne, _ in mesures["phrases_longues"][:8]
        ) + ")"
    ajout(gabarit % ("Phrases de plus de %d mots" % MOTS_PHRASE_LONGUE,
                     nombre(len(mesures["phrases_longues"])), detail_longues))
    ajout("")

    ajout("VERDICT")
    ajout("  " + mesures["verdict_libelle"])
    marqueurs = mesures["marqueurs_signature"]
    if marqueurs:
        ajout("  Les deux marqueurs reconnus au premier coup d'oeil (tiret cadratin,")
        ajout("  négation-contraste) sont présents %d fois." % marqueurs)
    if any(occ.confiance != "haute" for occ in retenues):
        ajout("  Les lignes marquées [?] demandent un arbitrage : le script signale,")
        ajout("  il ne trancherait pas à votre place.")
    ajout("")
    return "\n".join(ligne.rstrip() for ligne in lignes)


def rendre_json(texte, occurrences, mesures, avertissements):
    return json.dumps(
        {
            "fichier": texte.source,
            "mots": texte.nb_mots,
            "lignes": texte.nb_lignes,
            "titres": len(texte.titres),
            "avertissements": avertissements,
            "occurrences": [
                {
                    "categorie": occ.categorie,
                    "motif": occ.motif,
                    "ligne": occ.ligne,
                    "colonne": occ.colonne,
                    "confiance": occ.confiance,
                    "protege": occ.protege,
                    "extrait": occ.extrait,
                }
                for occ in occurrences
            ],
            "compte_par_categorie": mesures["compte_par_categorie"],
            "densite_pour_mille": mesures["densite_pour_mille"],
            "indice": mesures["indice"],
            "indice_pour_mille": mesures["indice_pour_mille"],
            "adverbes_en_ment": mesures["adverbes"],
            "adverbes_pour_mille": mesures["adverbes_pour_mille"],
            "phrases_longues": [
                {"ligne": ligne, "mots": nb} for ligne, nb in mesures["phrases_longues"]
            ],
            "verdict": mesures["verdict"],
            "verdict_libelle": mesures["verdict_libelle"],
        },
        ensure_ascii=False,
        indent=2,
    )


def mesurer(texte, occurrences):
    retenues = [occ for occ in occurrences if not occ.protege]
    compte = {}
    for occ in retenues:
        compte[occ.categorie] = compte.get(occ.categorie, 0) + 1

    indice = round(
        sum(
            POIDS_CATEGORIES.get(occ.categorie, 1.0)
            * (1.0 if occ.confiance == "haute" else COEFFICIENT_A_VERIFIER)
            for occ in retenues
        ),
        1,
    )
    indice_pour_mille = pour_mille(indice, texte.nb_mots)
    verdict, libelle = calculer_verdict(indice_pour_mille, retenues, texte.nb_mots)

    adverbes = compter_adverbes(texte)
    longues = reperer_phrases_longues(texte)

    return {
        "compte_par_categorie": compte,
        "densite_pour_mille": pour_mille(len(retenues), texte.nb_mots),
        "indice": indice,
        "indice_pour_mille": indice_pour_mille,
        "adverbes": len(adverbes),
        "adverbes_pour_mille": pour_mille(len(adverbes), texte.nb_mots),
        "phrases_longues": [
            (ligne_et_colonne(texte, position)[0], nb) for position, nb in longues
        ],
        "verdict": verdict,
        "verdict_libelle": libelle,
        "marqueurs_signature": compte.get("tiret", 0) + compte.get("negation-contraste", 0),
    }


# ---------------------------------------------------------------------------
# Entrée / sortie
# ---------------------------------------------------------------------------


def lire_source(chemin):
    if chemin == "-":
        contenu = sys.stdin.read()
        if not contenu.strip():
            raise ErreurEntree("Rien reçu sur l'entrée standard.")
        return contenu, "entrée standard"

    if not os.path.exists(chemin):
        raise ErreurEntree("Fichier introuvable : " + chemin)
    if os.path.isdir(chemin):
        raise ErreurEntree("Chemin attendu vers un fichier, reçu un dossier : " + chemin)
    try:
        with open(chemin, "rb") as flux:
            octets = flux.read()
    except OSError as erreur:
        raise ErreurEntree("Fichier illisible : " + str(erreur))

    if not octets.strip():
        raise ErreurEntree("Fichier vide : " + chemin)
    if b"\x00" in octets[:4096]:
        raise ErreurEntree(
            "Fichier binaire : " + chemin + ". Le script attend du texte, du Markdown ou du HTML."
        )

    for encodage in ("utf-8", "cp1252", "latin-1"):
        try:
            return octets.decode(encodage), chemin
        except UnicodeDecodeError:
            continue
    raise ErreurEntree("Encodage non reconnu : " + chemin + ". Convertir le fichier en UTF-8.")


def chemin_liste_par_defaut():
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(racine, LISTE_MOTS_PAR_DEFAUT)


def construire_parseur():
    parseur = argparse.ArgumentParser(
        prog="detecter_tics.py",
        description=(
            "Repère les tics d'écriture IA dans un livrable WAOUP. "
            "Le script détecte, il ne réécrit rien."
        ),
        epilog=(
            "Exemples :\n"
            "  python3 detecter_tics.py restitution.md\n"
            "  python3 detecter_tics.py propale.html --json\n"
            "  python3 detecter_tics.py note.md --liste-mots ma-liste.txt --strict\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parseur.add_argument(
        "fichier",
        help="Fichier .txt, .md ou .html à analyser. « - » pour lire l'entrée standard.",
    )
    parseur.add_argument(
        "--json",
        action="store_true",
        dest="json_",
        help="Sortie machine au format JSON au lieu du rapport lisible.",
    )
    parseur.add_argument(
        "--liste-mots",
        metavar="FICHIER",
        default=None,
        help="Liste de mots creux à utiliser. Par défaut : references/mots-creux.txt.",
    )
    parseur.add_argument(
        "--html",
        action="store_true",
        help="Force le nettoyage des balises, même si l'extension ne dit pas HTML.",
    )
    parseur.add_argument(
        "--strict",
        action="store_true",
        help="Rend un code de sortie 1 si le verdict n'est pas « envoyable ».",
    )
    return parseur


def principal(arguments=None):
    parseur = construire_parseur()
    options = parseur.parse_args(arguments)

    try:
        brut, source = lire_source(options.fichier)
        chemin_liste = options.liste_mots or chemin_liste_par_defaut()
        entrees, avertissement = charger_mots_creux(
            chemin_liste, obligatoire=options.liste_mots is not None
        )
        texte = preparer(brut, source, forcer_html=options.html)
        if texte.nb_mots == 0:
            raise ErreurEntree(
                "Aucun mot exploitable après nettoyage : " + source
                + ". Vérifier que le fichier contient bien du texte rédigé."
            )
    except ErreurEntree as erreur:
        sys.stderr.write("Erreur : " + str(erreur) + "\n")
        return 2

    avertissements = [avertissement] if avertissement else []
    occurrences = analyser(texte, entrees)
    mesures = mesurer(texte, occurrences)

    if options.json_:
        sys.stdout.write(rendre_json(texte, occurrences, mesures, avertissements) + "\n")
    else:
        sys.stdout.write(rendre_rapport(texte, occurrences, mesures, avertissements))

    if options.strict and mesures["verdict"] != "envoyable":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(principal())
