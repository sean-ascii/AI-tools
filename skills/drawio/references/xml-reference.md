# Draw.io XML Reference

Load this reference only when a diagram needs concrete draw.io XML patterns beyond the basic structure in `SKILL.md`.

## Cells

- The root layer must contain `<mxCell id="0"/>` and `<mxCell id="1" parent="0"/>`.
- Vertices use `vertex="1"` and must include an `mxGeometry` child with `x`, `y`, `width`, `height`, and `as="geometry"`.
- Edges use `edge="1"` and must include `<mxGeometry relative="1" as="geometry"/>`.
- Use stable, unique ids. Descriptive ids such as `api`, `db`, and `edge-api-db` are easier to debug than generated numbers.

## Common Vertex Example

```xml
<mxCell id="api" value="API" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="160" y="120" width="120" height="60" as="geometry"/>
</mxCell>
```

## Common Edge Example

```xml
<mxCell id="edge-api-db" value="" style="endArrow=block;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1" source="api" target="db">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## Style Notes

- Keep styles inline on each cell unless the user explicitly needs reusable style metadata.
- Use `whiteSpace=wrap;html=1` for text wrapping.
- Use `rounded=1` for rounded rectangles and `ellipse` for circles/ovals.
- Use `swimlane` or grouped cells for containers when a diagram needs bounded areas.
- Prefer readable contrast: dark text on light fills, or light text on dark fills.

## Containers and Layers

- Use parent-child relationships for contained items: set the child cell's `parent` to the container cell id.
- Keep layer cells as direct children of `id="0"`. Ordinary diagram cells should usually stay under `parent="1"`.
- Containers need `vertex="1"` and their own `mxGeometry`; contained cells use coordinates relative to the container.

## Metadata and Pages

- A single-page file should use one `<diagram>` inside `<mxfile>`.
- Multi-page diagrams use multiple `<diagram>` elements, each with its own `id`, `name`, and `mxGraphModel`.
- Put user-visible labels in `value` attributes. Avoid hidden metadata unless the user explicitly asks for tags or custom properties.

## Dark Mode

- `adaptiveColors="auto"` helps draw.io adapt colors across themes.
- Avoid relying on transparent fills for important shapes; they can disappear against dark backgrounds.
- Prefer explicit fill and stroke colors with enough contrast.

## Well-Formedness

- Do not emit XML comments.
- Escape attribute values: `&` as `&amp;`, `<` as `&lt;`, `>` as `&gt;`, and `"` as `&quot;`.
- Avoid raw newlines inside attribute values.
- Every opening tag must be closed unless it is intentionally self-closing.
- Edge cells must not be self-closing; they need the `mxGeometry` child.
