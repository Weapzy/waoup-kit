#!/usr/bin/env bash
# Fabrique le paquet .plugin du kit forgé, puis retire la Forge.
# Usage :
#   relais.sh paquet <dossier-du-kit> [dossier-de-sortie]
#   relais.sh retrait
set -euo pipefail

err() { printf '%s\n' "$*" >&2; }

paquet() {
  local src="${1:-}" out="${2:-}"
  [ -n "$src" ] || { err "Usage : relais.sh paquet <dossier-du-kit> [dossier-de-sortie]"; exit 2; }
  [ -d "$src" ] || { err "Dossier introuvable : $src"; exit 2; }
  [ -f "$src/.claude-plugin/plugin.json" ] || { err "Pas de .claude-plugin/plugin.json dans $src"; exit 2; }

  local nom
  nom=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["name"])' "$src/.claude-plugin/plugin.json") \
    || { err "plugin.json illisible ou sans champ name"; exit 2; }

  # Sortie : dossier fourni, sinon un dossier outputs voisin, sinon le dossier courant.
  if [ -z "$out" ]; then
    for c in "$PWD/outputs" "$(dirname "$src")/outputs" "$HOME/outputs"; do
      [ -d "$c" ] && { out="$c"; break; }
    done
    [ -n "$out" ] || out="$PWD"
  fi
  mkdir -p "$out"

  local tmp="${TMPDIR:-/tmp}/$nom.plugin"
  rm -f "$tmp"
  ( cd "$src" && zip -qr "$tmp" . -x '*.DS_Store' -x '__MACOSX/*' -x '.git/*' )
  # Deux extensions, même archive. Le .plugin sert quand Claude dépose le fichier
  # lui-même dans les sorties d'une session : il s'affiche alors avec un aperçu et
  # un bouton d'installation. Le .zip sert au téléversement manuel, qui est le seul
  # format que la fenêtre d'installation accepte de façon fiable.
  cp "$tmp" "$out/$nom.plugin"
  cp "$tmp" "$out/$nom.zip"
  printf 'Paquet prêt, deux extensions pour le même contenu :\n'
  printf '  %s   (dépôt par Claude, aperçu et bouton d\x27installation)\n' "$out/$nom.plugin"
  printf '  %s      (téléversement manuel, à privilégier pour un envoi par message)\n' "$out/$nom.zip"
  printf 'Taille : %s\n' "$(du -h "$out/$nom.zip" | cut -f1)"
  printf 'Contenu :\n'
  unzip -Z1 "$out/$nom.zip" | head -40
}

retrait() {
  if ! command -v claude >/dev/null 2>&1; then
    cat <<'TXT'
Retrait automatique indisponible ici (pas de commande claude).
Geste à faire à la main, dans Cowork :
  Personnaliser  ->  Plugins  ->  La Forge WAOUP  ->  Désinstaller
TXT
    return 0
  fi
  local cible=""
  cible=$(claude plugin list 2>/dev/null | grep -o 'waoup-forge@[^ ]*' | head -1 || true)
  [ -n "$cible" ] || cible="waoup-forge@waoup"
  printf 'Retrait de %s\n' "$cible"
  claude plugin uninstall "$cible" --yes 2>/dev/null \
    || claude plugin uninstall "$cible" 2>/dev/null \
    || { err "Échec du retrait. À faire à la main : claude plugin uninstall $cible"; return 1; }
  printf 'Forge retirée. Pour la réinstaller : claude plugin install waoup-forge@waoup\n'
}

case "${1:-}" in
  paquet)  shift; paquet "$@" ;;
  retrait) retrait ;;
  *) err "Usage : relais.sh paquet <dossier-du-kit> [dossier-de-sortie] | relais.sh retrait"; exit 2 ;;
esac
