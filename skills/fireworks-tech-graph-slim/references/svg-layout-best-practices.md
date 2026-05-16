# SVG Technical Diagram Layout Best Practices

Load this before creating or reviewing diagrams.

## Universal Rules

- Keep one diagram focused, but preserve end-to-end flow when the user asks for a complete process.
- Use a bounded canvas: default to `960x600`, `960x700`, or `1200x700`; export at 1920px width when PNG is requested.
- Keep component spacing at least `80px` edge-to-edge.
- Keep arrow paths at least `60px` away from unrelated component interiors.
- Snap major coordinates to a 8px or 10px grid.
- Use system fonts only. Do not use `@import`, remote fonts, or external image URLs.

## Arrow Routing

- Connect arrows to edge midpoints, not corners.
- Keep connection points at least `20px` from rounded corners.
- Prefer orthogonal paths for architecture, flowchart, data-flow, and ER diagrams.
- Use straight horizontal arrows for sequence diagrams.
- Stagger repeated arrows by `15-20px`.
- Put arrow labels at path midpoints with `5-10px` perpendicular offset.
- Give arrow labels a small white background when the label crosses a line, band, or busy area.

Good orthogonal path:

```svg
<path d="M 240 180 L 320 180 L 320 300 L 400 300"
      fill="none" stroke="#2563eb" stroke-width="1.5"
      marker-end="url(#arrow-blue)"/>
```

## Render Order

SVG renders later elements on top. Use this order:

1. Background
2. Phase bands or grouping containers
3. Arrow paths
4. Arrow label backgrounds
5. Components
6. Component labels
7. Arrow labels
8. Legend and annotations

## Text

- Keep node labels short: usually 1-4 words.
- Use descriptions only when they add meaning; keep them one short line.
- Avoid text smaller than `11px`.
- Use explicit `x`, `y`, `text-anchor`, and width-aware placement. SVG text will not wrap automatically.
- For multi-line labels, use separate `<text>` elements or `<tspan>` rows.

## Diagram-Type Defaults

### Architecture and Data Flow

- Arrange systems in layers or columns.
- Use shallow color semantics: UI/client, service/runtime, data/storage, external.
- Keep arrows out of node interiors; route around containers.
- Include a legend only when color or line style carries meaning.

### Flowchart

- Use top-to-bottom flow unless the user asks otherwise.
- Use rounded rectangles for start/end, rectangles for actions, diamonds for decisions.
- Label decision exits with short `yes/no` or condition labels.
- Avoid diagonal connectors; use orthogonal paths.

### Sequence

- Put actors left to right in execution order.
- Use at least `140px` between lifeline centers and `32px` between messages.
- Use dashed arrows for returns or async feedback.
- Do not auto-split only because of participant or message count. First expand the `viewBox`, increase height, and keep grid alignment.
- Split only when the user asks for separate diagrams or the complete diagram remains unreadable; if splitting, keep or offer a complete overview.

## Validation Checklist

- SVG parses as XML.
- Referenced markers exist.
- No important text overlaps shapes, arrows, or other labels.
- No arrow crosses through an unrelated node.
- Labels remain readable at 1920px export width.
- Render succeeds with `cairosvg` or `rsvg-convert` when PNG export is requested.

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Arrow crosses a component | Route around it with orthogonal segments |
| Label sits on top of a line | Add background rect or move the label |
| Components are too close | Increase spacing to at least `80px` |
| Arrow connects to a corner | Move the point to an edge midpoint |
| Every node has a unique color | Use 3-4 semantic color categories |
| Diagram is unreadable after layout | Keep an overview, then add focused detail diagrams |
