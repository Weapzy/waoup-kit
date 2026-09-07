#!/usr/bin/env python3
"""Convertit un livrable Markdown en HTML à la charte WAOUP.

Le script ne réinvente rien : il transforme le Markdown en fragments HTML, puis
les injecte dans assets/gabarit-livrable.html. La mise en forme reste dans le
CSS, jamais dans le script.

Usage minimal :
    python3 md_vers_html.py restitution.md sortie.html --client "Groupe Ardan"

Bibliothèque standard uniquement. Aucune installation.
"""

from __future__ import annotations

import argparse
import datetime
import html
import re
import sys
import unicodedata
from pathlib import Path

# --- Constantes -------------------------------------------------------------

# Emplacement du gabarit et du CSS, relativement à ce script.
DOSSIER_SKILL = Path(__file__).resolve().parent.parent
GABARIT_DEFAUT = DOSSIER_SKILL / "assets" / "gabarit-livrable.html"

# Mention posée par défaut sur la couverture, l'en-tête et le pied. WAOUP la
# met sur tout document qui sort de la maison. `--confidentiel ""` la retire.
MENTION_DEFAUT = "Document confidentiel — diffusion restreinte"

# Les mois en toutes lettres : la locale française n'est pas garantie présente
# sur le poste qui lance le script.
MOIS_FR = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)

# Types d'encadrés reconnus par la syntaxe `::: cle Titre`. La clé donne la
# classe CSS, définie dans assets/waoup-charte.css.
ENCADRES = {
    "cle": "encadre--cle",
    "info": "encadre--info",
    "alerte": "encadre--alerte",
    "fort": "encadre--fort",
}

# Encodages essayés dans l'ordre. Le second couvre les fichiers venus de Word
# sur Windows, cas fréquent quand le Markdown a transité par un client.
ENCODAGES = ("utf-8", "cp1252")

# Une ligne d'attribution de verbatim commence par un tiret long, un tiret demi
# cadratin ou un double tiret ASCII.
MOTIF_ATTRIBUTION = re.compile(r"^\s*(—|–|--)\s*(?P<source>.+)$")

MOTIF_TITRE = re.compile(r"^(?P<niveau>#{1,6})\s+(?P<texte>.+?)\s*#*$")
MOTIF_FILET = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
MOTIF_PUCE = re.compile(r"^(?P<indent>\s*)[-*+]\s+(?P<texte>.*)$")
MOTIF_NUMERO = re.compile(r"^(?P<indent>\s*)(?P<num>\d{1,3})[.)]\s+(?P<texte>.*)$")
MOTIF_SEPARATEUR_TABLEAU = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")
MOTIF_CLOTURE_CODE = re.compile(r"^\s*(?P<cloture>```+|~~~+)\s*(?P<langue>\S*)\s*$")
MOTIF_ENCADRE = re.compile(r"^\s*:::\s*(?P<cle>\S+)?\s*(?P<titre>.*?)\s*:*\s*$")


class ErreurConversion(Exception):
    """Erreur prévue, affichée à l'utilisateur sans trace d'exécution."""


# --- Lecture ----------------------------------------------------------------

def lire_texte(chemin: Path, role: str) -> str:
    """Lit un fichier texte en disant précisément ce qui a échoué."""
    if not chemin.exists():
        raise ErreurConversion(f"{role} introuvable : {chemin}")
    if chemin.is_dir():
        raise ErreurConversion(f"{chemin} est un dossier, pas un fichier ({role.lower()}).")

    dernier_echec = None
    for encodage in ENCODAGES:
        try:
            contenu = chemin.read_text(encoding=encodage)
        except UnicodeDecodeError as echec:
            dernier_echec = echec
            continue
        except OSError as echec:
            raise ErreurConversion(f"Lecture impossible de {chemin} : {echec}") from echec
        if encodage != ENCODAGES[0]:
            print(
                f"Note : {chemin.name} lu en {encodage}, pas en UTF-8. "
                "Vérifier les accents dans le HTML produit.",
                file=sys.stderr,
            )
        return contenu

    raise ErreurConversion(
        f"{role} illisible : encodage non reconnu ({', '.join(ENCODAGES)} essayés). "
        f"Réenregistrer {chemin.name} en UTF-8. Détail : {dernier_echec}"
    )


def extraire_front_matter(texte: str) -> tuple[dict[str, str], str]:
    """Sépare un éventuel front matter YAML simple du corps du document.

    Seules les paires `cle: valeur` sur une ligne sont lues. Le reste est
    ignoré sans bruit : ce n'est pas un analyseur YAML.
    """
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != "---":
        return {}, texte

    for i in range(1, len(lignes)):
        if lignes[i].strip() in ("---", "..."):
            entetes: dict[str, str] = {}
            for ligne in lignes[1:i]:
                if ":" in ligne:
                    cle, _, valeur = ligne.partition(":")
                    entetes[cle.strip().lower()] = valeur.strip().strip("\"'")
            return entetes, "\n".join(lignes[i + 1:])

    return {}, texte


# --- Conversion en ligne ----------------------------------------------------

def _proteger_code(texte: str, coffre: list[str]) -> str:
    """Met les `codes en ligne` de côté avant les autres substitutions."""
    def remplacer(trouve: re.Match) -> str:
        coffre.append(f"<code>{trouve.group('contenu')}</code>")
        return f"\x00{len(coffre) - 1}\x00"

    return re.sub(r"`(?P<contenu>[^`]+)`", remplacer, texte)


def _restituer_code(texte: str, coffre: list[str]) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda t: coffre[int(t.group(1))], texte)


def _attribut(valeur: str) -> str:
    """Rend une chaîne sûre entre guillemets d'attribut.

    Le texte a déjà été échappé pour `&`, `<` et `>`. Seul le guillemet droit
    reste à traiter : lui seul peut refermer l'attribut trop tôt.
    """
    return valeur.replace('"', "&quot;")


def en_ligne(texte: str) -> str:
    """Applique les marques de niveau caractère : code, liens, gras, italique.

    L'échappement laisse les apostrophes et les guillemets intacts : ils sont
    licites dans du texte HTML, et une charte française en est pleine. Un
    document dont la source reste lisible se relit et se corrige à la main.
    """
    coffre: list[str] = []
    sortie = _proteger_code(html.escape(texte, quote=False), coffre)

    sortie = re.sub(
        r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)\)",
        lambda t: f'<img src="{_attribut(t.group("src"))}" '
                  f'alt="{_attribut(t.group("alt"))}">',
        sortie,
    )
    sortie = re.sub(
        r"\[(?P<texte>[^\]]+)\]\((?P<url>[^)\s]+)\)",
        lambda t: f'<a href="{_attribut(t.group("url"))}">{t.group("texte")}</a>',
        sortie,
    )
    sortie = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", sortie)
    sortie = re.sub(r"__(?=\S)(.+?)(?<=\S)__", r"<strong>\1</strong>", sortie)
    sortie = re.sub(r"(?<![\w*])\*(?=\S)([^*]+?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", sortie)
    sortie = re.sub(r"(?<![\w_])_(?=\S)([^_]+?)(?<=\S)_(?![\w_])", r"<em>\1</em>", sortie)
    sortie = re.sub(r"==(?=\S)(.+?)(?<=\S)==", r"<mark>\1</mark>", sortie)

    return _restituer_code(sortie, coffre)


def ancre(texte: str, deja_prises: set[str]) -> str:
    """Fabrique un identifiant d'ancre stable à partir d'un intitulé."""
    sans_accent = unicodedata.normalize("NFKD", texte)
    sans_accent = "".join(c for c in sans_accent if not unicodedata.combining(c))
    base = re.sub(r"[^a-z0-9]+", "-", sans_accent.lower()).strip("-") or "section"

    candidat, suffixe = base, 2
    while candidat in deja_prises:
        candidat = f"{base}-{suffixe}"
        suffixe += 1
    deja_prises.add(candidat)
    return candidat


# --- Conversion en blocs ----------------------------------------------------

class Convertisseur:
    """Parcourt le Markdown ligne à ligne et produit le HTML du corps.

    L'état porté d'un bloc à l'autre se réduit à deux choses : la liste des
    titres de niveau 2 (elle alimente le sommaire) et les ancres déjà prises.
    """

    def __init__(self) -> None:
        self.sections: list[tuple[str, str]] = []
        self._ancres: set[str] = set()
        self.titre_h1: str | None = None

    def convertir(self, texte: str) -> str:
        lignes = texte.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        return "\n".join(self._blocs(lignes, profondeur=0))

    # -- aiguillage --

    def _blocs(self, lignes: list[str], profondeur: int) -> list[str]:
        sortie: list[str] = []
        i = 0
        while i < len(lignes):
            ligne = lignes[i]

            if not ligne.strip():
                i += 1
                continue

            cloture = MOTIF_CLOTURE_CODE.match(ligne)
            if cloture:
                html_bloc, i = self._code(lignes, i, cloture)
                sortie.append(html_bloc)
                continue

            if ligne.lstrip().startswith(":::"):
                html_bloc, i = self._encadre(lignes, i, profondeur)
                sortie.append(html_bloc)
                continue

            titre = MOTIF_TITRE.match(ligne)
            if titre:
                sortie.append(self._titre(titre))
                i += 1
                continue

            if MOTIF_FILET.match(ligne):
                sortie.append("<hr>")
                i += 1
                continue

            if ligne.lstrip().startswith(">"):
                html_bloc, i = self._citation(lignes, i)
                sortie.append(html_bloc)
                continue

            if self._est_tableau(lignes, i):
                html_bloc, i = self._tableau(lignes, i)
                sortie.append(html_bloc)
                continue

            if MOTIF_PUCE.match(ligne) or MOTIF_NUMERO.match(ligne):
                html_bloc, i = self._liste(lignes, i, profondeur)
                sortie.append(html_bloc)
                continue

            html_bloc, i = self._paragraphe(lignes, i)
            sortie.append(html_bloc)

        return [bloc for bloc in sortie if bloc]

    # -- blocs --

    def _titre(self, trouve: re.Match) -> str:
        niveau = len(trouve.group("niveau"))
        texte = trouve.group("texte").strip()

        # Le h1 unique et initial est le titre du livrable : il part sur la
        # couverture, il ne se répète pas dans le corps.
        if niveau == 1 and self.titre_h1 is None and not self.sections:
            self.titre_h1 = texte
            return ""

        if niveau == 2:
            identifiant = ancre(texte, self._ancres)
            self.sections.append((identifiant, texte))
            return f'<h2 id="{identifiant}">{en_ligne(texte)}</h2>'

        return f"<h{niveau}>{en_ligne(texte)}</h{niveau}>"

    def _paragraphe(self, lignes: list[str], i: int) -> tuple[str, int]:
        morceaux: list[str] = []
        while i < len(lignes) and lignes[i].strip():
            ligne = lignes[i]
            if (
                MOTIF_TITRE.match(ligne)
                or MOTIF_FILET.match(ligne)
                or ligne.lstrip().startswith((">", ":::"))
                or MOTIF_CLOTURE_CODE.match(ligne)
                or MOTIF_PUCE.match(ligne)
                or MOTIF_NUMERO.match(ligne)
                or self._est_tableau(lignes, i)
            ):
                break
            morceaux.append(ligne.strip())
            i += 1

        if not morceaux:
            return "", i + 1
        return f"<p>{en_ligne(' '.join(morceaux))}</p>", i

    def _code(self, lignes: list[str], i: int, ouverture: re.Match) -> tuple[str, int]:
        marque = ouverture.group("cloture")[0] * 3
        corps: list[str] = []
        i += 1
        while i < len(lignes) and not lignes[i].strip().startswith(marque):
            corps.append(lignes[i])
            i += 1
        # Un bloc non refermé se ferme en fin de fichier plutôt que d'échouer.
        return f"<pre><code>{html.escape(chr(10).join(corps))}</code></pre>", i + 1

    def _citation(self, lignes: list[str], i: int) -> tuple[str, int]:
        contenu: list[str] = []
        while i < len(lignes) and lignes[i].lstrip().startswith(">"):
            contenu.append(re.sub(r"^\s*>\s?", "", lignes[i]))
            i += 1

        paragraphes: list[str] = []
        attribution: str | None = None
        tampon: list[str] = []

        def vider() -> None:
            if tampon:
                paragraphes.append(f"<p>{en_ligne(' '.join(tampon))}</p>")
                tampon.clear()

        for ligne in contenu:
            if not ligne.strip():
                vider()
                continue
            source = MOTIF_ATTRIBUTION.match(ligne)
            if source:
                vider()
                attribution = source.group("source").strip()
                continue
            tampon.append(ligne.strip())
        vider()

        if attribution:
            paragraphes.append(f"<footer>{en_ligne(attribution)}</footer>")
        return "<blockquote>\n" + "\n".join(paragraphes) + "\n</blockquote>", i

    def _encadre(self, lignes: list[str], i: int, profondeur: int) -> tuple[str, int]:
        ouverture = MOTIF_ENCADRE.match(lignes[i])
        cle = (ouverture.group("cle") or "").lower() if ouverture else ""
        titre = (ouverture.group("titre") or "").strip() if ouverture else ""

        # `::: Titre libre` sans clé connue : la première partie est le titre.
        if cle and cle not in ENCADRES:
            titre = (cle + " " + titre).strip()
            cle = ""

        corps: list[str] = []
        i += 1
        while i < len(lignes) and lignes[i].strip() != ":::":
            corps.append(lignes[i])
            i += 1

        classe = "encadre"
        if cle:
            classe += " " + ENCADRES[cle]

        interieur = self._blocs(corps, profondeur + 1)
        entete = f'<p class="encadre__titre">{en_ligne(titre)}</p>' if titre else ""
        return (
            f'<div class="{classe}">\n'
            + ("\n".join([entete] + interieur) if entete else "\n".join(interieur))
            + "\n</div>",
            i + 1,
        )

    def _est_tableau(self, lignes: list[str], i: int) -> bool:
        return (
            "|" in lignes[i]
            and i + 1 < len(lignes)
            and "|" in lignes[i + 1]
            and "-" in lignes[i + 1]
            and MOTIF_SEPARATEUR_TABLEAU.match(lignes[i + 1]) is not None
        )

    def _tableau(self, lignes: list[str], i: int) -> tuple[str, int]:
        def cellules(ligne: str) -> list[str]:
            return [c.strip() for c in ligne.strip().strip("|").split("|")]

        entetes = cellules(lignes[i])
        alignements = cellules(lignes[i + 1])
        i += 2

        # Une colonne alignée à droite dans le Markdown est une colonne de
        # chiffres : elle reçoit la classe .num de la charte.
        classes = [
            ' class="num"' if a.endswith(":") and not a.startswith(":") else ""
            for a in alignements
        ]

        lignes_html: list[str] = []
        while i < len(lignes) and "|" in lignes[i] and lignes[i].strip():
            valeurs = cellules(lignes[i])
            cases = []
            for rang, valeur in enumerate(valeurs):
                classe = classes[rang] if rang < len(classes) else ""
                balise = "th" if rang == 0 else "td"
                portee = ' scope="row"' if rang == 0 else ""
                cases.append(f"<{balise}{portee}{classe}>{en_ligne(valeur)}</{balise}>")
            lignes_html.append("<tr>" + "".join(cases) + "</tr>")
            i += 1

        entete_html = "".join(
            f'<th scope="col"{classes[rang] if rang < len(classes) else ""}>'
            f"{en_ligne(valeur)}</th>"
            for rang, valeur in enumerate(entetes)
        )

        return (
            '<div class="tableau-conteneur">\n<table>\n'
            f"<thead><tr>{entete_html}</tr></thead>\n"
            "<tbody>\n" + "\n".join(lignes_html) + "\n</tbody>\n"
            "</table>\n</div>",
            i,
        )

    def _liste(self, lignes: list[str], i: int, profondeur: int) -> tuple[str, int]:
        premiere = MOTIF_NUMERO.match(lignes[i]) or MOTIF_PUCE.match(lignes[i])
        assert premiere is not None
        ordonnee = MOTIF_NUMERO.match(lignes[i]) is not None
        marge = len(premiere.group("indent"))
        balise = "ol" if ordonnee else "ul"

        articles: list[list[str]] = []
        while i < len(lignes):
            ligne = lignes[i]
            if not ligne.strip():
                # Ligne vide : la liste continue si l'élément suivant en fait
                # partie, sinon elle s'arrête.
                suivante = i + 1
                while suivante < len(lignes) and not lignes[suivante].strip():
                    suivante += 1
                if suivante >= len(lignes):
                    break
                suite = MOTIF_NUMERO.match(lignes[suivante]) or MOTIF_PUCE.match(lignes[suivante])
                if not suite or len(suite.group("indent")) < marge:
                    break
                if articles:
                    articles[-1].append("")
                i = suivante
                continue

            item = MOTIF_NUMERO.match(ligne) if ordonnee else MOTIF_PUCE.match(ligne)
            autre = MOTIF_PUCE.match(ligne) if ordonnee else MOTIF_NUMERO.match(ligne)

            if item and len(item.group("indent")) == marge:
                articles.append([item.group("texte")])
                i += 1
                continue
            if autre and len(autre.group("indent")) == marge:
                break  # changement de type de liste au même niveau
            if len(ligne) - len(ligne.lstrip()) > marge and articles:
                articles[-1].append(ligne[marge:])
                i += 1
                continue
            break

        rendu: list[str] = []
        for corps in articles:
            interieur = self._blocs(corps, profondeur + 1)
            # Le premier paragraphe d'un élément n'est jamais emballé dans un
            # <p> : c'est lui qui porte la puce, et un <p> lui ajouterait une
            # marge que les éléments voisins n'ont pas.
            if interieur and interieur[0].startswith("<p>") and interieur[0].endswith("</p>"):
                interieur[0] = interieur[0][3:-4]
            rendu.append("<li>" + "\n".join(interieur) + "</li>")

        return f"<{balise}>\n" + "\n".join(rendu) + f"\n</{balise}>", i


# --- Injection dans le gabarit ---------------------------------------------

def remplacer_bloc(gabarit: str, nom: str, contenu: str, chemin: Path) -> str:
    debut, fin = f"<!-- waoup:{nom}:debut -->", f"<!-- waoup:{nom}:fin -->"
    i, j = gabarit.find(debut), gabarit.find(fin)
    if i == -1 or j == -1 or j < i:
        raise ErreurConversion(
            f"Balises « {debut} » et « {fin} » absentes ou inversées dans {chemin}. "
            "Le gabarit a été modifié : les rétablir autour de la zone à remplir."
        )
    return gabarit[: i + len(debut)] + "\n" + contenu + "\n" + gabarit[j:]


def remplir_emplacement(gabarit: str, cle: str, valeur: str) -> tuple[str, int]:
    motif = re.compile(
        r"(<(?P<balise>[a-zA-Z][a-zA-Z0-9]*)(?=[\s>])[^>]*?"
        r'data-waoup="' + re.escape(cle) + r'"[^>]*>)'
        r"(?P<contenu>.*?)"
        r"(</(?P=balise)>)",
        re.DOTALL,
    )
    return motif.subn(lambda t: t.group(1) + valeur + t.group(4), gabarit)


def injecter(gabarit: str, chemin: Path, valeurs: dict[str, str],
             sommaire: str, contenu: str) -> str:
    resultat = remplacer_bloc(gabarit, "sommaire", sommaire, chemin)
    resultat = remplacer_bloc(resultat, "contenu", contenu, chemin)

    for cle, valeur in valeurs.items():
        resultat, nombre = remplir_emplacement(resultat, cle, html.escape(valeur, quote=False))
        if nombre == 0:
            print(
                f"Note : aucun emplacement data-waoup=\"{cle}\" dans {chemin.name}, "
                "valeur ignorée.",
                file=sys.stderr,
            )
    return resultat


def batir_sommaire(sections: list[tuple[str, str]]) -> str:
    if not sections:
        return ""
    articles = "\n".join(
        f'      <li><a href="#{identifiant}">{en_ligne(texte)}</a></li>'
        for identifiant, texte in sections
    )
    return (
        '  <section class="page sommaire">\n'
        '    <h2 class="sommaire__titre">Sommaire</h2>\n'
        "    <ol>\n" + articles + "\n    </ol>\n"
        "  </section>"
    )


# --- Ligne de commande ------------------------------------------------------

def date_du_jour() -> str:
    aujourd_hui = datetime.date.today()
    return f"{aujourd_hui.day} {MOIS_FR[aujourd_hui.month - 1]} {aujourd_hui.year}"


def analyser_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    analyseur = argparse.ArgumentParser(
        prog="md_vers_html.py",
        description="Markdown vers HTML à la charte WAOUP.",
        epilog=(
            "Syntaxes propres à la charte, en plus du Markdown courant :\n"
            "  ::: cle Titre ... :::   encadré (cle = cle, info, alerte, fort)\n"
            "  > citation\n"
            "  > — Fonction, site   attribution du verbatim\n"
            "  ==texte==            surlignage lime\n"
            "  | a | b |\n  | --: |  colonne alignée à droite = colonne de chiffres\n\n"
            "Un unique titre de niveau 1 en tête de fichier devient le titre du\n"
            "livrable et passe sur la couverture. Les titres de niveau 2 forment\n"
            "le sommaire ; sans titre de niveau 2, la page de sommaire est retirée."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    analyseur.add_argument("entree", type=Path, help="fichier Markdown source")
    analyseur.add_argument("sortie", type=Path, help="fichier HTML à écrire")
    analyseur.add_argument("--client", default="", help="nom du client")
    analyseur.add_argument("--titre", default="", help="titre du livrable")
    analyseur.add_argument("--sous-titre", default="", dest="sous_titre",
                           help="phrase de cadrage sur la couverture")
    analyseur.add_argument("--date", default="",
                           help="date affichée (défaut : aujourd'hui, en toutes lettres)")
    analyseur.add_argument("--confidentiel", default=MENTION_DEFAUT,
                           help='mention de confidentialité ; --confidentiel "" la retire')
    analyseur.add_argument("--gabarit", type=Path, default=GABARIT_DEFAUT,
                           help="gabarit HTML cible (défaut : assets/gabarit-livrable.html)")
    return analyseur.parse_args(argv)


def executer(options: argparse.Namespace) -> None:
    source = lire_texte(options.entree, "Fichier Markdown")
    entetes, corps = extraire_front_matter(source)

    if not corps.strip():
        raise ErreurConversion(
            f"{options.entree} ne contient aucun contenu à mettre en forme "
            "(fichier vide, ou réduit à son front matter)."
        )

    convertisseur = Convertisseur()
    contenu = convertisseur.convertir(corps)
    if not contenu.strip():
        raise ErreurConversion(
            f"{options.entree} n'a produit aucun bloc HTML. "
            "Vérifier que le fichier est bien du Markdown."
        )

    titre = options.titre or entetes.get("titre") or convertisseur.titre_h1
    if not titre:
        titre = options.entree.stem
        print(
            f"Note : aucun titre fourni ni trouvé, « {titre} » repris du nom de fichier. "
            "Utiliser --titre pour le fixer.",
            file=sys.stderr,
        )

    client = options.client or entetes.get("client", "")
    if not client:
        print("Note : aucun client fourni (--client), l'emplacement reste vide.",
              file=sys.stderr)

    valeurs = {
        "titre-page": f"{client} — {titre}" if client else titre,
        "client": client,
        "titre": titre,
        "sous-titre": options.sous_titre or entetes.get("sous-titre", ""),
        "date": options.date or entetes.get("date") or date_du_jour(),
        "reference": options.sortie.stem,
        "confidentiel": options.confidentiel,
    }

    gabarit = lire_texte(options.gabarit, "Gabarit HTML")
    page = injecter(gabarit, options.gabarit,
                    valeurs, batir_sommaire(convertisseur.sections), contenu)

    try:
        options.sortie.parent.mkdir(parents=True, exist_ok=True)
        options.sortie.write_text(page, encoding="utf-8")
    except OSError as echec:
        raise ErreurConversion(f"Écriture impossible de {options.sortie} : {echec}") from echec

    sections = len(convertisseur.sections)
    print(
        f"{options.sortie} écrit — {sections} section{'s' if sections > 1 else ''}, "
        f"{len(page)} caractères."
    )
    if options.gabarit.parent.resolve() != options.sortie.parent.resolve():
        print(
            f"Rappel : copier {options.gabarit.parent / 'waoup-charte.css'} à côté du "
            "HTML, ou corriger le <link> du fichier produit.",
            file=sys.stderr,
        )


def main(argv: list[str] | None = None) -> int:
    try:
        executer(analyser_arguments(argv))
    except ErreurConversion as echec:
        print(f"Erreur : {echec}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrompu.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
