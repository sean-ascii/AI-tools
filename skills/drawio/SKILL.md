---
name: drawio
description: Use when the user asks for an editable draw.io/diagrams.net file, .drawio output, diagram export to PNG/SVG/PDF, or a diagram that naturally belongs in draw.io such as a flowchart, architecture diagram, ER diagram, sequence diagram, class diagram, network diagram, wireframe, or UI sketch. Prefer other tools when the user wants an implemented app UI, bitmap artwork, or a non-editable illustration.
disable-model-invocation: true
---

# Draw.io Diagram Skill

Generate draw.io diagrams as native `.drawio` files. Optionally export to PNG, SVG, or PDF with the diagram XML embedded (so the exported file remains editable in draw.io).

## How to create a diagram

1. **Generate draw.io XML** as a complete `<mxfile>` document containing one or more `<diagram>` elements with `mxGraphModel` content
2. **Write the XML** to a `.drawio` file in the current working directory using the current environment's normal file-editing mechanism
3. **Validate the XML** before export. Use an XML parser, `xmllint --noout`, or another available well-formedness check. Fix duplicate ids, missing root cells, unescaped attribute characters, and self-closing edges before continuing
4. **Preview when possible**. If a renderer is available, export a temporary PNG or SVG and inspect it for blank output, overlapping text, crossed lines, unreadable labels, and excessive canvas size. Fix layout issues before final delivery
5. **If the user requested an export format** (`png`, `svg`, `pdf`), read [references/export-cli.md](references/export-cli.md), export with embedded diagram XML, and keep the source `.drawio` file unless the user explicitly asks for only one exported artifact
6. **Return the result path** — the exported file if exported, or the `.drawio` file otherwise. If the environment allows opening or previewing the file, do that as a convenience

## Choosing the output format

Check the user's request for a format preference. Examples:

- `/drawio create a flowchart` → `flowchart.drawio`
- `/drawio png flowchart for login` → `login-flow.drawio.png`
- `/drawio svg: ER diagram` → `er-diagram.drawio.svg`
- `/drawio pdf architecture overview` → `architecture-overview.drawio.pdf`

If no format is mentioned, write the `.drawio` file. The user can always ask to export later.

### Supported export formats

| Format | Embed XML | Notes |
|--------|-----------|-------|
| `png` | Yes (`-e`) | Viewable everywhere, editable in draw.io |
| `svg` | Yes (`-e`) | Scalable, editable in draw.io |
| `pdf` | Yes (`-e`) | Printable, editable in draw.io |
| `jpg` | No | Lossy, no embedded XML support |

PNG, SVG, and PDF all support `--embed-diagram` — the exported file contains the full diagram XML, so opening it in draw.io recovers the editable diagram.

## Export and preview

For draw.io CLI detection, export flags, and open commands, read [references/export-cli.md](references/export-cli.md) only when the user requests PNG/SVG/PDF export or a visual preview is needed.

## File naming

- Use a descriptive filename based on the diagram content (e.g., `login-flow`, `database-schema`)
- Use lowercase with hyphens for multi-word names
- For export, use double extensions: `name.drawio.png`, `name.drawio.svg`, `name.drawio.pdf` — this signals the file contains embedded diagram XML
- Keep the source `.drawio` file by default. Only delete it when the user explicitly asks for a single exported artifact and the export was successful

## XML format

A `.drawio` file is native diagrams.net XML. Always generate XML directly — Mermaid and CSV formats require server-side conversion and cannot be saved as native files.

For new files, prefer the complete `<mxfile><diagram><mxGraphModel>` structure below. When editing or using an existing `.drawio` file as a reference, also accept files whose root is a bare `<mxGraphModel>`; preserve the existing wrapper style unless the user asks to normalize it.

### Basic structure

Every diagram must have this structure:

```xml
<mxfile host="app.diagrams.net">
  <diagram id="page-1" name="Page-1">
    <mxGraphModel adaptiveColors="auto">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- Cell `id="0"` is the root layer
- Cell `id="1"` is the default parent layer
- All diagram elements use `parent="1"` unless using multiple layers

## XML reference

For common styles, edge routing, containers, layers, metadata, dark mode colors, and XML well-formedness rules, read [references/xml-reference.md](references/xml-reference.md) only when those details are needed for the requested diagram.

For sequence diagrams, read [references/sequence-diagram.md](references/sequence-diagram.md). It includes lifelines, message arrows, return arrows, self-calls, phase bands, layout defaults, and readability checks.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| draw.io CLI not found | Desktop app not installed or not on PATH | Keep the `.drawio` file and tell the user to install the draw.io desktop app, or open the file manually |
| Export produces empty/corrupt file | Invalid XML (e.g. double hyphens in comments, unescaped special characters) | Validate XML well-formedness before writing; see the XML well-formedness section below |
| Diagram opens but looks blank | Missing root cells `id="0"` and `id="1"` | Ensure the basic mxGraphModel structure is complete |
| Edges not rendering | Edge mxCell is self-closing (no child mxGeometry element) | Every edge must have `<mxGeometry relative="1" as="geometry" />` as a child element |
| File won't open after export | Incorrect file path or missing file association | Print the absolute file path so the user can open it manually |

## CRITICAL: XML well-formedness

- **NEVER include ANY XML comments (`<!-- -->`) in the output.** XML comments are strictly forbidden — they waste tokens, can cause parse errors, and serve no purpose in diagram XML.
- Escape special characters in attribute values: `&amp;`, `&lt;`, `&gt;`, `&quot;`
- Always use unique `id` values for each `mxCell`
