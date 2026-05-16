# Draw.io Export CLI

Load this reference only when exporting or previewing a `.drawio` file.

## Locate the CLI

Prefer a command already on `PATH`:

```bash
command -v drawio
command -v draw.io
```

Common fallbacks:

```bash
# macOS
/Applications/draw.io.app/Contents/MacOS/draw.io

# Linux
drawio

# WSL2 default Windows install
DRAWIO_CMD="/mnt/c/Program Files/draw.io/draw.io.exe"

# WSL2 per-user Windows install
DRAWIO_CMD="/mnt/c/Users/$WIN_USER/AppData/Local/Programs/draw.io/draw.io.exe"
```

WSL2 can be detected with:

```bash
grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null
```

## Export

Use embedded diagram XML for editable exports:

```bash
drawio -x -f png -e -b 10 -o diagram.drawio.png diagram.drawio
drawio -x -f svg -e -b 10 -o diagram.drawio.svg diagram.drawio
drawio -x -f pdf -e -b 10 -o diagram.drawio.pdf diagram.drawio
```

Key flags:

- `-x` / `--export`: export mode
- `-f` / `--format`: `png`, `svg`, or `pdf`
- `-e` / `--embed-diagram`: embed XML in PNG/SVG/PDF
- `-o` / `--output`: output path
- `-b` / `--border`: border around the diagram
- `-t` / `--transparent`: transparent PNG background
- `-a` / `--all-pages`: export all pages, mainly useful for PDF
- `-p` / `--page-index`: export one page

WSL2 path-with-space example:

```bash
DRAWIO_CMD="/mnt/c/Program Files/draw.io/draw.io.exe"
"$DRAWIO_CMD" -x -f png -e -b 10 -o diagram.drawio.png diagram.drawio
```

## Open or Preview

```bash
# macOS
open diagram.drawio

# Linux
xdg-open diagram.drawio

# WSL2
cmd.exe /c start "" "$(wslpath -w diagram.drawio)"
```

If opening fails, return the absolute file path.
