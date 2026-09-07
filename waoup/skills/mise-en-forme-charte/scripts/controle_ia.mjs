#!/usr/bin/env node
/*
  controle_ia.mjs
  Contrôle automatique des marqueurs de production IA sur un HTML ou un CSS.

  Adapté du détecteur d'anti-patterns du plugin Impeccable
  (cli/engine/, Copyright (c) 2026 Paul Bakaus, SPDX-License-Identifier: Apache-2.0,
  https://github.com/paulbakaus/impeccable). Les identifiants de règles, les seuils
  chiffrés et la liste des polices surexposées viennent de ce détecteur ; le code est
  réécrit en un seul fichier sans dépendance, les libellés sont en français, et six
  règles propres à la charte WAOUP sont ajoutées.
  Ce fichier est distribué sous Apache-2.0, comme l'original.

  Usage :
      node controle_ia.mjs fichier.html [fichier.css ...]
      node controle_ia.mjs --regles          liste les règles et leurs seuils

  Sortie : une ligne par défaut, au format
      règle · fichier:ligne · extrait
  Code de sortie 1 si au moins un défaut est trouvé, 0 sinon.
*/

import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

/* --------------------------------------------------------------------------
   1. SEUILS
   Valeurs reprises du détecteur d'Impeccable et de l'annexe du rapport 04.
   -------------------------------------------------------------------------- */

const SEUILS = {
  bordureLateraleAvecRayon: 2,   // px, liseré latéral coloré sur bloc arrondi
  bordureLateraleSansRayon: 3,   // px, liseré latéral coloré sur bloc à angle vif
  chromaCouleur: 30,             // écart max-min RVB au-delà duquel une couleur n'est plus neutre
  chromaNeutre: 20,              // en deçà, la couleur est tenue pour neutre
  flouOmbreLarge: 16,            // px, flou d'ombre qui, avec un filet fin, fait la ghost card
  filetFin: 1.5,                 // px, épaisseur en deçà de laquelle un filet est « fin »
  pastilleMin: 32,               // px, côté minimal d'une pastille d'icône
  pastilleMax: 128,              // px, côté maximal
  pastilleRatioMin: 0.7,
  pastilleRatioMax: 1.4,
  planchierTexte: 11,            // px, plancher absolu de tout texte fonctionnel
  rapportEchelle: 1.25,          // rapport minimal entre deux niveaux typographiques
  deficitTitre: 12,              // px, l'espace au-dessus d'un titre dépasse celui du dessous d'au moins autant
  capitalesLongues: 30,          // caractères en capitales au-delà desquels la silhouette du mot est perdue
  tiretCadratin: 0,              // position WAOUP : zéro tiret cadratin
  pointMedianChaine: 2,          // deux points médians sur une ligne = chaîne de métadonnées
  cremeCanalMin: 209,            // les trois canaux au-dessus = fond clair
  cremeChaleurMin: 6,            // R moins B
  cremeChaleurMax: 48,
};

// Liste noire des dix-sept polices surexposées (constante OVERUSED_FONTS d'Impeccable).
const POLICES_SUREXPOSEES = new Set([
  'inter', 'roboto', 'open sans', 'lato', 'montserrat', 'arial', 'helvetica',
  'fraunces', 'instrument sans', 'instrument serif',
  'geist', 'geist sans', 'geist mono', 'mona sans',
  'plus jakarta sans', 'space grotesk', 'recoleta',
]);

// Dérogation WAOUP, décidée et assumée : la charte nomme ces deux polices.
// Elles restent, la distinction se joue sur la grille et l'échelle typographique.
// Voir references/sans-marqueur-ia.md, section « Polices ».
const POLICES_DEROGEES = new Set(['inter', 'space grotesk']);

// Hex des dégradés violet et mauve, relevés littéralement par le détecteur d'Impeccable.
const VIOLETS = new Set([
  '#7c3aed', '#8b5cf6', '#a855f7', '#9333ea', '#7e22ce',
  '#6d28d9', '#6366f1', '#764ba2', '#667eea',
]);

// Contextes sombres de la charte : le lime y porte du texte à 15:1, c'est un usage sûr.
const CONTEXTES_SOMBRES = /couverture|encadre--fort|slide--couverture|slide--section|inverse|--sombre/;

// Surfaces de page, seules concernées par la règle du fond crème.
const SURFACES_DE_PAGE = /^(?:html|body|\.doc|\.page|\.slide|\.corps|main|section\.page)\b|\bpage-fond\b/;

/* --------------------------------------------------------------------------
   2. COULEUR
   -------------------------------------------------------------------------- */

function hexVersRvb(hex) {
  let h = hex.replace('#', '').toLowerCase();
  if (h.length === 3) h = h.split('').map((c) => c + c).join('');
  if (h.length === 8) h = h.slice(0, 6);
  if (h.length !== 6 || /[^0-9a-f]/.test(h)) return null;
  return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
}

function versRvb(valeur, tokens) {
  if (!valeur) return null;
  const v = valeur.trim().toLowerCase();
  const varr = v.match(/^var\(\s*(--[\w-]+)/);
  if (varr && tokens.has(varr[1])) return versRvb(tokens.get(varr[1]), tokens);
  if (v.startsWith('#')) return hexVersRvb(v);
  const rgb = v.match(/rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)/);
  if (rgb) return [+rgb[1], +rgb[2], +rgb[3]];
  const nommees = { black: [0, 0, 0], white: [255, 255, 255], transparent: null, currentcolor: null };
  if (v in nommees) return nommees[v];
  return null;
}

const chroma = (rvb) => (rvb ? Math.max(...rvb) - Math.min(...rvb) : 0);
const estNeutre = (rvb) => !rvb || chroma(rvb) < SEUILS.chromaNeutre;

/* --------------------------------------------------------------------------
   3. LECTURE DES FICHIERS ET DÉCOUPAGE CSS
   -------------------------------------------------------------------------- */

// Retire les commentaires CSS d'un fragment en conservant les sauts de ligne,
// pour que les numéros de ligne restent justes.
function sansCommentaires(texte) {
  return texte.replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '));
}

const ligneDe = (texte, index) => texte.slice(0, index).split('\n').length;

/*
  Découpe un fragment CSS en blocs { selecteur, decl, ligne }. Les at-rules à bloc
  (@media, @supports) sont traversées : seules leurs règles internes sont rendues.
*/
function blocsCss(css, ligneDepart = 0) {
  const propre = sansCommentaires(css);
  const blocs = [];
  const re = /([^{}]+)\{([^{}]*)\}/g;
  let m;
  while ((m = re.exec(propre)) !== null) {
    const selecteur = m[1].replace(/\s+/g, ' ').trim();
    if (selecteur.startsWith('@')) continue;
    const decl = new Map();
    for (const paire of m[2].split(';')) {
      const i = paire.indexOf(':');
      if (i < 0) continue;
      decl.set(paire.slice(0, i).trim().toLowerCase(), paire.slice(i + 1).trim());
    }
    blocs.push({
      selecteur,
      decl,
      ligne: ligneDepart + ligneDe(propre, m.index + m[1].length),
      brut: m[0],
    });
  }
  return blocs;
}

// Rassemble les fragments CSS d'un fichier : le fichier entier pour un .css,
// les blocs <style> pour un .html.
function fragmentsCss(texte, estHtml) {
  if (!estHtml) return [{ css: texte, ligneDepart: 0 }];
  const frags = [];
  const re = /<style\b[^>]*>([\s\S]*?)<\/style>/gi;
  let m;
  while ((m = re.exec(texte)) !== null) {
    frags.push({ css: m[1], ligneDepart: ligneDe(texte, m.index) - 1 });
  }
  return frags;
}

/* --------------------------------------------------------------------------
   4. RÈGLES
   Chaque règle produit des constats { regle, ligne, extrait }.
   -------------------------------------------------------------------------- */

const REGLES = {
  'liseré-latéral': 'bordure d\'un seul côté, non neutre, ≥ 2 px avec rayon ou ≥ 3 px sans',
  'accent-sur-arrondi': 'bordure haute ou basse ≥ 3 px sur un bloc arrondi',
  'texte-en-dégradé': 'background-clip: text posé sur un dégradé',
  'dégradé': 'dégradé de fond : la charte ne pose que des aplats et des filets',
  'rayures-répétées': 'fond à rayures repeating-linear-gradient',
  'ombre-colorée': 'ombre ou halo dont la couleur porte une chroma ≥ 30',
  'filet-et-ombre': 'filet fin ≤ 1,5 px et ombre floue ≥ 16 px sur le même bloc',
  'pastille-icône': 'tuile quasi carrée de 32 à 128 px, fond ou bordure, rayon > 0',
  'carte-dans-carte': 'bloc de classe carte imbriqué dans un autre',
  'fond-crème': 'fond clair chaud : trois canaux ≥ 209, R ≥ V ≥ B, chaleur 6 à 48',
  'violet-mauve': 'hex ou utilitaire de la famille violet, mauve, indigo',
  'police-surexposée': 'police de la liste noire des dix-sept, hors dérogation WAOUP',
  'sur-titre': 'libellé en capitales posé juste au-dessus d\'un titre',
  'capitales-longues': 'plus de 30 caractères en capitales hors titre',
  'numérotation-décorative': 'numéro de section 01, 02, 03 sans information portée',
  'tiret-cadratin': 'tiret cadratin, banni sans exception chez WAOUP',
  'point-médian': 'chaîne de métadonnées jointe par des points médians',
  'plancher-11px': 'texte fonctionnel sous 11 px, à l\'écran ou à l\'impression',
  'hiérarchie-plate': 'rapport inférieur à 1,25 entre deux niveaux typographiques',
  'rythme-des-titres': 'espace au-dessus d\'un titre inférieur à celui du dessous',
  'lime-porteur-de-texte': 'lime en couleur de texte hors des deux rôles nommés',
  'texte-justifié': 'text-align: justify sans hyphens: auto',
  'titre-sauté': 'niveau de titre sauté dans la hiérarchie du document',
  'easing-rebond': 'animation bounce, elastic, spring ou cubic-bezier hors bornes',
  'image-cassée': 'balise img sans src ou avec un src vide',
  'contenu-invisible': 'opacity: 0 au repos, texte suspendu à un script',
  'emoji-icône': 'emoji employé comme système d\'icônes',
  'lorem-ipsum': 'faux texte laissé dans le livrable',
};

function reglesCss(blocs, tokens, constats, basePt) {
  for (const b of blocs) {
    const { selecteur, decl, ligne } = b;
    const d = (p) => decl.get(p) || '';
    const tout = [...decl.entries()].map(([k, v]) => `${k}: ${v}`).join('; ');

    // Rayon du bloc, utilisé par plusieurs règles.
    const rayon = parseFloat(d('border-radius')) || 0;

    // --- liseré latéral, accent sur arrondi ---
    for (const cote of ['left', 'right', 'inline-start', 'inline-end']) {
      const raccourci = d(`border-${cote}`);
      const largeurSeule = d(`border-${cote}-width`);
      const val = raccourci || largeurSeule;
      if (!val) continue;
      const px = parseFloat(val);
      if (!px) continue;
      const couleur = versRvb((val.match(/#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|var\(\s*--[\w-]+\s*\)/) || [])[0], tokens);
      if (raccourci && estNeutre(couleur) && couleur) continue;
      const seuil = rayon > 0 ? SEUILS.bordureLateraleAvecRayon : SEUILS.bordureLateraleSansRayon;
      if (px >= seuil) {
        constats.push({ regle: 'liseré-latéral', ligne, extrait: `${selecteur} { border-${cote}: ${val} }` });
      }
    }
    for (const cote of ['top', 'bottom']) {
      const val = d(`border-${cote}`);
      const px = parseFloat(val);
      if (px >= 3 && rayon > 0) {
        constats.push({ regle: 'accent-sur-arrondi', ligne, extrait: `${selecteur} { border-${cote}: ${val} }` });
      }
    }

    // --- dégradés ---
    if (/repeating-linear-gradient/i.test(tout)) {
      constats.push({ regle: 'rayures-répétées', ligne, extrait: `${selecteur} { repeating-linear-gradient }` });
    } else if (/(linear|radial|conic)-gradient/i.test(tout)) {
      const type = tout.match(/(linear|radial|conic)-gradient/i)[0];
      if (/background-clip\s*:\s*text/i.test(tout) || /-webkit-background-clip\s*:\s*text/i.test(tout)) {
        constats.push({ regle: 'texte-en-dégradé', ligne, extrait: `${selecteur} { background-clip: text + ${type} }` });
      } else {
        constats.push({ regle: 'dégradé', ligne, extrait: `${selecteur} { ${type} }` });
      }
    }

    // --- ombres ---
    for (const prop of ['box-shadow', 'text-shadow']) {
      const val = d(prop);
      if (!val || val === 'none') continue;
      const couleur = versRvb((val.match(/#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)/) || [])[0], tokens);
      if (couleur && chroma(couleur) >= SEUILS.chromaCouleur) {
        constats.push({ regle: 'ombre-colorée', ligne, extrait: `${selecteur} { ${prop}: ${val} }` });
      }
    }

    // --- ghost card : filet fin plus ombre large ---
    const ombre = d('box-shadow');
    const flou = ombre ? parseFloat((ombre.match(/(?:[-\d.]+p?x?\s+){2}([\d.]+)px/) || [])[1] || 0) : 0;
    const filets = ['border', 'border-top', 'border-right', 'border-bottom', 'border-left']
      .map((p) => parseFloat(d(p)))
      .filter((n) => n > 0 && n <= SEUILS.filetFin);
    if (filets.length && flou >= SEUILS.flouOmbreLarge) {
      constats.push({ regle: 'filet-et-ombre', ligne, extrait: `${selecteur} { border ${filets[0]}px + box-shadow flou ${flou}px }` });
    }

    // --- pastille d'icône ---
    const l = parseFloat(d('width')), h = parseFloat(d('height'));
    if (l >= SEUILS.pastilleMin && l <= SEUILS.pastilleMax && h >= SEUILS.pastilleMin && h <= SEUILS.pastilleMax) {
      const ratio = l / h;
      const habille = d('background') || d('background-color') || d('border');
      if (ratio >= SEUILS.pastilleRatioMin && ratio <= SEUILS.pastilleRatioMax && habille && rayon > 0) {
        constats.push({ regle: 'pastille-icône', ligne, extrait: `${selecteur} { ${l}×${h} px, rayon ${rayon}px }` });
      }
    }

    // --- fond crème, violet ---
    const fond = versRvb((d('background') || d('background-color')).match(/#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|var\(\s*--[\w-]+\s*\)/)?.[0], tokens);
    // Comme chez Impeccable, la règle ne vise que les surfaces de page : un voile
    // chaud sur un encadré de 24 mm n'est pas « la surface de bon goût par défaut ».
    if (fond && SURFACES_DE_PAGE.test(selecteur)) {
      const [r, v, bl] = fond;
      if (r >= SEUILS.cremeCanalMin && v >= SEUILS.cremeCanalMin && bl >= SEUILS.cremeCanalMin
        && r >= v && v >= bl && (r - bl) >= SEUILS.cremeChaleurMin && (r - bl) <= SEUILS.cremeChaleurMax) {
        constats.push({ regle: 'fond-crème', ligne, extrait: `${selecteur} { background: rgb(${r}, ${v}, ${bl}) }` });
      }
    }
    for (const hex of tout.toLowerCase().match(/#[0-9a-f]{6}\b/g) || []) {
      if (VIOLETS.has(hex)) constats.push({ regle: 'violet-mauve', ligne, extrait: `${selecteur} { ${hex} }` });
    }

    // --- polices ---
    const famille = d('font-family');
    if (famille) {
      for (const nom of famille.split(',')) {
        const n = nom.replace(/["']/g, '').trim().toLowerCase();
        if (POLICES_SUREXPOSEES.has(n) && !POLICES_DEROGEES.has(n)) {
          constats.push({ regle: 'police-surexposée', ligne, extrait: `${selecteur} { font-family: ${n} }` });
        }
      }
    }

    // --- lime porteur de texte ---
    const couleurTexte = d('color');
    if (/var\(\s*--lime\s*\)|#e2ffa6/i.test(couleurTexte)) {
      const fondSombre = fond && (fond[0] + fond[1] + fond[2]) / 3 < 90;
      if (!fondSombre && !CONTEXTES_SOMBRES.test(selecteur)) {
        constats.push({ regle: 'lime-porteur-de-texte', ligne, extrait: `${selecteur} { color: ${couleurTexte} }` });
      }
    }

    // --- texte justifié ---
    if (/justify/.test(d('text-align')) && !/auto/.test(d('hyphens'))) {
      constats.push({ regle: 'texte-justifié', ligne, extrait: `${selecteur} { text-align: justify }` });
    }

    // --- easing de rebond ---
    const mouvement = `${d('animation')} ${d('animation-name')} ${d('transition')} ${d('transition-timing-function')} ${d('animation-timing-function')}`;
    if (/bounce|elastic|wobble|jiggle|spring/i.test(mouvement)) {
      constats.push({ regle: 'easing-rebond', ligne, extrait: `${selecteur} { ${mouvement.trim()} }` });
    }
    const bez = mouvement.match(/cubic-bezier\(\s*([\d.-]+)\s*,\s*([\d.-]+)\s*,\s*([\d.-]+)\s*,\s*([\d.-]+)\s*\)/);
    if (bez && ([+bez[2], +bez[4]].some((y) => y < -0.1 || y > 1.1))) {
      constats.push({ regle: 'easing-rebond', ligne, extrait: `${selecteur} { ${bez[0]} }` });
    }

    // --- contenu invisible au repos ---
    if (/^0(\.0+)?$/.test(d('opacity'))) {
      constats.push({ regle: 'contenu-invisible', ligne, extrait: `${selecteur} { opacity: 0 }` });
    }

    // --- plancher de 11 px ---
    for (const [prop, val] of decl) {
      if (prop !== 'font-size' && !/^--t-/.test(prop)) continue;
      const px = enPixels(val, basePt);
      if (px !== null && px < SEUILS.planchierTexte) {
        const ou = basePt && /rem$/.test(val.trim()) ? `${px.toFixed(1)} px à l'impression` : `${px.toFixed(1)} px`;
        constats.push({ regle: 'plancher-11px', ligne, extrait: `${selecteur} { ${prop}: ${val} } soit ${ou}` });
      }
    }

    // --- rythme des titres ---
    if (/^h[1-6]\b/.test(selecteur) && decl.has('margin')) {
      const parts = decl.get('margin').split(/\s+/).map((p) => enPixelsEspace(p, tokens));
      if (parts.length === 3 && parts[0] !== null && parts[2] !== null) {
        if (parts[0] < parts[2] + SEUILS.deficitTitre && parts[0] !== 0) {
          constats.push({ regle: 'rythme-des-titres', ligne, extrait: `${selecteur} { margin: ${decl.get('margin')} }` });
        }
      }
    }
  }
}

// Convertit une valeur de taille de texte en pixels. `basePt` est la base
// typographique de l'impression, quand le fichier bascule html en points.
function enPixels(valeur, basePt) {
  const v = valeur.trim();
  const rem = v.match(/^([\d.]+)rem$/);
  if (rem) {
    const ecran = parseFloat(rem[1]) * 16;
    const impression = basePt ? parseFloat(rem[1]) * basePt * (96 / 72) : Infinity;
    return Math.min(ecran, impression);
  }
  const px = v.match(/^([\d.]+)px$/);
  if (px) return parseFloat(px[1]);
  const pt = v.match(/^([\d.]+)pt$/);
  if (pt) return parseFloat(pt[1]) * (96 / 72);
  return null;
}

// Résout un espacement écrit en px ou via un token de la charte.
function enPixelsEspace(valeur, tokens) {
  const v = valeur.trim();
  if (v === '0') return 0;
  const varr = v.match(/^var\(\s*(--[\w-]+)\s*\)$/);
  if (varr && tokens.has(varr[1])) {
    const cible = tokens.get(varr[1]);
    const calc = cible.match(/calc\(\s*var\(\s*(--[\w-]+)\s*\)\s*\*\s*([\d.]+)\s*\)/);
    if (calc && tokens.has(calc[1])) return parseFloat(tokens.get(calc[1])) * parseFloat(calc[2]);
    return parseFloat(cible) || null;
  }
  return parseFloat(v) || null;
}

function reglesEchelle(tokens, constats, ligneRoot) {
  const echelle = ['--t-h1', '--t-h2', '--t-h3', '--t-h4', '--t-corps']
    .filter((t) => tokens.has(t))
    .map((t) => ({ nom: t, rem: parseFloat(tokens.get(t)) }))
    .filter((e) => !Number.isNaN(e.rem));
  for (let i = 0; i < echelle.length - 1; i++) {
    const rapport = echelle[i].rem / echelle[i + 1].rem;
    if (rapport < SEUILS.rapportEchelle) {
      constats.push({
        regle: 'hiérarchie-plate',
        ligne: ligneRoot,
        extrait: `${echelle[i].nom} / ${echelle[i + 1].nom} = ${rapport.toFixed(2)}`,
      });
    }
  }
}

function reglesHtml(texte, constats) {
  const lignes = texte.split('\n');

  // --- titres sautés ---
  let precedent = 0;
  for (const m of texte.matchAll(/<h([1-6])\b/gi)) {
    const niveau = +m[1];
    if (precedent && niveau > precedent + 1) {
      constats.push({ regle: 'titre-sauté', ligne: ligneDe(texte, m.index), extrait: `h${precedent} puis h${niveau}` });
    }
    precedent = niveau;
  }

  // --- sur-titre : libellé tout en capitales collé au-dessus d'un titre ---
  for (const m of texte.matchAll(/<(p|div|span)\b[^>]*>\s*([^<>]{6,80}?)\s*<\/\1>\s*(?:<[^>]+>\s*)?<h[1-3]\b/gi)) {
    const t = m[2].trim();
    if (t === t.toLocaleUpperCase('fr') && /[A-ZÀ-Ý]{3}/.test(t) && /\s/.test(t)) {
      constats.push({ regle: 'sur-titre', ligne: ligneDe(texte, m.index), extrait: t });
    }
  }

  // --- numérotation décorative ---
  for (const m of texte.matchAll(/>\s*(0[1-9])\s*[.\/]?\s*</g)) {
    constats.push({ regle: 'numérotation-décorative', ligne: ligneDe(texte, m.index), extrait: m[1] });
  }

  // --- carte dans carte ---
  const pile = [];
  for (const m of texte.matchAll(/<(\/?)(?:div|section|article|aside)\b([^>]*)>/gi)) {
    if (m[1] === '/') { pile.pop(); continue; }
    if (/\/>\s*$/.test(m[0])) continue;
    const estCarte = /class\s*=\s*["'][^"']*\b(?:carte|card|panel|tuile|tile)\b/i.test(m[2]);
    if (estCarte && pile.includes(true)) {
      constats.push({ regle: 'carte-dans-carte', ligne: ligneDe(texte, m.index), extrait: m[0].slice(0, 70) });
    }
    pile.push(estCarte);
  }

  // --- image cassée ---
  for (const m of texte.matchAll(/<img\b([^>]*)>/gi)) {
    if (!/\bsrc\s*=\s*["'][^"']+["']/i.test(m[1])) {
      constats.push({ regle: 'image-cassée', ligne: ligneDe(texte, m.index), extrait: m[0].slice(0, 70) });
    }
  }

  // --- opacity 0 en attribut de style ---
  for (const m of texte.matchAll(/style\s*=\s*["'][^"']*opacity\s*:\s*0(?:\.0+)?\s*[;"']/gi)) {
    constats.push({ regle: 'contenu-invisible', ligne: ligneDe(texte, m.index), extrait: m[0].slice(0, 60) });
  }

  // --- capitales longues dans le texte rendu ---
  const rendu = texte
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<script[\s\S]*?<\/script>/gi, '');
  for (const m of rendu.matchAll(/>([^<>]{20,})</g)) {
    const t = m[1].replace(/\s+/g, ' ').trim();
    const lettres = t.replace(/[^A-Za-zÀ-ÿ]/g, '');
    if (lettres.length > SEUILS.capitalesLongues && t === t.toLocaleUpperCase('fr') && /[A-ZÀ-Ý]/.test(t)) {
      constats.push({ regle: 'capitales-longues', ligne: ligneDe(rendu, m.index), extrait: t.slice(0, 60) });
    }
  }

  // --- emoji ---
  const emoji = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{23E0}-\u{23FF}\u{FE0F}]/u;
  lignes.forEach((l, i) => {
    if (emoji.test(l)) constats.push({ regle: 'emoji-icône', ligne: i + 1, extrait: l.trim().slice(0, 60) });
  });
}

function reglesTexte(texte, constats) {
  const lignes = texte.split('\n');
  lignes.forEach((l, i) => {
    // --- tiret cadratin : zéro toléré ---
    const tirets = (l.match(/—|&mdash;|&#8212;|&#x2014;/gi) || []).length;
    if (tirets > SEUILS.tiretCadratin) {
      constats.push({ regle: 'tiret-cadratin', ligne: i + 1, extrait: l.trim().slice(0, 70) });
    }
    // --- chaîne de points médians ---
    const medians = (l.match(/\s·\s/g) || []).length;
    if (medians >= SEUILS.pointMedianChaine) {
      constats.push({ regle: 'point-médian', ligne: i + 1, extrait: l.trim().slice(0, 70) });
    }
    // --- lorem ipsum ---
    if (/lorem\s+ipsum/i.test(l)) {
      constats.push({ regle: 'lorem-ipsum', ligne: i + 1, extrait: l.trim().slice(0, 60) });
    }
  });
}

/* --------------------------------------------------------------------------
   5. ANALYSE D'UN FICHIER
   -------------------------------------------------------------------------- */

function analyser(chemin) {
  const texte = readFileSync(chemin, 'utf8');
  const estHtml = /\.html?$/i.test(chemin);
  const constats = [];

  // Tokens du bloc :root, pour résoudre les var() et l'échelle typographique.
  const tokens = new Map();
  let ligneRoot = 1;
  const frags = fragmentsCss(texte, estHtml);
  for (const f of frags) {
    for (const b of blocsCss(f.css, f.ligneDepart)) {
      if (!/(^|,)\s*:root\s*$/.test(b.selecteur)) continue;
      ligneRoot = b.ligne;
      for (const [k, v] of b.decl) if (k.startsWith('--')) tokens.set(k, v);
    }
  }

  // Base typographique de l'impression, quand le fichier bascule html en points.
  const basePt = (() => {
    const m = sansCommentaires(texte).match(/@media\s+print[\s\S]{0,600}?html\s*\{[^}]*font-size\s*:\s*([\d.]+)pt/i);
    return m ? parseFloat(m[1]) : null;
  })();

  for (const f of frags) reglesCss(blocsCss(f.css, f.ligneDepart), tokens, constats, basePt);
  if (tokens.size) reglesEchelle(tokens, constats, ligneRoot);
  if (estHtml) reglesHtml(texte, constats);
  reglesTexte(texte, constats);

  // Dédoublonnage : une même règle sur une même ligne ne se dit qu'une fois.
  const vus = new Set();
  return constats.filter((c) => {
    const cle = `${c.regle}|${c.ligne}|${c.extrait}`;
    if (vus.has(cle)) return false;
    vus.add(cle);
    return true;
  }).sort((a, b) => a.ligne - b.ligne);
}

/* --------------------------------------------------------------------------
   6. LIGNE DE COMMANDE
   -------------------------------------------------------------------------- */

function principal(argv) {
  if (argv.includes('--regles')) {
    console.log('Règles du contrôle sans marqueur IA\n');
    for (const [id, libelle] of Object.entries(REGLES)) {
      console.log(`  ${id.padEnd(26)} ${libelle}`);
    }
    console.log('\nSeuils : ' + Object.entries(SEUILS).map(([k, v]) => `${k}=${v}`).join(', '));
    return 0;
  }
  const fichiers = argv.filter((a) => !a.startsWith('-'));
  if (!fichiers.length) {
    console.error('Usage : node controle_ia.mjs fichier.html [fichier.css ...]');
    console.error('        node controle_ia.mjs --regles');
    return 2;
  }

  let total = 0;
  for (const chemin of fichiers) {
    let constats;
    try {
      constats = analyser(chemin);
    } catch (e) {
      console.error(`lecture-impossible · ${chemin} · ${e.message}`);
      total++;
      continue;
    }
    const nom = basename(chemin);
    for (const c of constats) {
      console.log(`${c.regle} · ${nom}:${c.ligne} · ${c.extrait}`);
    }
    total += constats.length;
    if (!constats.length) console.log(`aucun défaut · ${nom}`);
  }

  console.log(`\n${total} défaut${total > 1 ? 's' : ''} sur ${fichiers.length} fichier${fichiers.length > 1 ? 's' : ''}.`);
  return total ? 1 : 0;
}

process.exit(principal(process.argv.slice(2)));
