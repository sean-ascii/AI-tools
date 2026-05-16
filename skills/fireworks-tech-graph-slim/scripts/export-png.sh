#!/bin/bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <svg-file> [width]"
  exit 1
fi

SVG_FILE="$1"
WIDTH="${2:-1920}"
PNG_FILE="${SVG_FILE%.svg}.png"

if [ ! -f "$SVG_FILE" ]; then
  echo "Error: file not found: $SVG_FILE"
  exit 1
fi

if python3 -c "import cairosvg" 2>/dev/null; then
  python3 - "$SVG_FILE" "$PNG_FILE" "$WIDTH" <<'PY'
import sys
import xml.etree.ElementTree as ET
import cairosvg

svg, png, width = sys.argv[1], sys.argv[2], int(sys.argv[3])
root = ET.parse(svg).getroot()
view_box = root.get("viewBox", "").split()
if len(view_box) == 4:
    source_width = float(view_box[2])
elif root.get("width"):
    source_width = float(str(root.get("width")).replace("px", ""))
else:
    source_width = 960.0
scale = width / source_width
cairosvg.svg2png(url=svg, write_to=png, scale=scale)
PY
  echo "PNG exported: $PNG_FILE"
  exit 0
fi

if command -v rsvg-convert >/dev/null 2>&1; then
  rsvg-convert -w "$WIDTH" "$SVG_FILE" -o "$PNG_FILE"
  echo "PNG exported: $PNG_FILE"
  exit 0
fi

echo "No PNG renderer found. Install cairosvg or librsvg."
echo "Recommended: pip install cairosvg"
exit 1
