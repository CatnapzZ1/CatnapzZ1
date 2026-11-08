#!/usr/bin/env bash
# Regenerate every hand-built SVG in assets/ from the scripts in this folder.
# Needs python3 with Pillow. The Ark Pixel font (~3.5 MB) is downloaded once into a cache dir.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
assets="$here/../assets"

font_version="2026.10.25"
cache="${XDG_CACHE_HOME:-$HOME/.cache}/catnap-profile-assets"
font="$cache/ark-pixel-12px-monospaced-latin.otf"

if [ ! -f "$font" ]; then
  mkdir -p "$cache"
  zip="$cache/ark-pixel-font.zip"
  curl -fsSL --retry 3 -o "$zip" \
    "https://github.com/TakWolf/ark-pixel-font/releases/download/$font_version/ark-pixel-font-12px-monospaced-otf-v$font_version.zip"
  python3 -I -c 'import sys, zipfile; zipfile.ZipFile(sys.argv[1]).extract("ark-pixel-12px-monospaced-latin.otf", sys.argv[2])' "$zip" "$cache"
  rm "$zip"
fi

python3 -I "$here/title.py" "$font" "Catnap_zZ" "$assets/title"
python3 -I "$here/cover.py" "$assets/railing.jpg" "$assets/cover.svg"
python3 -I "$here/sky.py" "$assets/sky.svg"
python3 -I "$here/interlude.py" "$assets/interlude.svg"
