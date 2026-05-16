---
name: fireworks-tech-graph-slim
description: Use when the user wants a precise technical diagram as editable SVG with optional PNG export, especially UML sequence/class/use-case/state/ER diagrams, architecture diagrams, flowcharts, data-flow diagrams, swimlanes, and system visualizations. Prefer this over image generation for structured diagrams where labels, arrows, layout, and semantic clarity matter.
metadata:
  short-description: Generate clean SVG/PNG technical and UML diagrams
disable-model-invocation: true
---

# Fireworks Tech Graph Slim

Generate clean, structured SVG technical diagrams and optionally export PNG. Keep the SVG as the source of truth.

## Workflow

1. Identify diagram type: `sequence`, `class`, `use-case`, `state-machine`, `er-diagram`, `architecture`, `data-flow`, `flowchart`, `timeline`, or `swimlane`.
2. Choose style:
   - `style-4-notion-clean.md`: default for docs, README, UML, and dense technical diagrams.
   - `style-1-flat-icon.md`: default for architecture and product/system overviews.
   - `style-7-openai.md`: use only when the user asks for OpenAI-like visual styling.
3. Read only the needed style file plus `references/svg-layout-best-practices.md`.
4. For sequence diagrams, read `references/sequence-layout.md` and prefer `scripts/render-sequence-svg.py` from a structured JSON spec. For other supported diagram types, inspect the matching file in `templates/` and reuse its layout pattern instead of inventing structure from scratch.
5. Create a standalone `.svg` file in the working directory.
6. Run `scripts/validate-svg.sh <file.svg>`.
7. If PNG is requested or useful, run `scripts/export-png.sh <file.svg> [width]`.

## Diagram Quality Rules

- Prefer one clear diagram over one complete but crowded diagram.
- For sequence diagrams, default to one complete diagram. Do not split only because a diagram has more than 7 lifelines or 25 messages; the sequence renderer can expand the `viewBox`.
- Split sequence diagrams only when the user asks for separate views, or when a complete diagram remains unreadable after grid layout. If splitting, also keep or offer a complete overview diagram.
- Keep labels short. Move parameters, long payloads, and implementation details into notes or surrounding text.
- Use consistent spacing: at least 140px between sequence lifelines and 32px between messages.
- Avoid arrow paths crossing through nodes. Route with orthogonal paths when needed.
- Use dashed arrows for returns or optional/async feedback.
- Use shallow color semantics: actor/UI, service/runtime, data/storage, external systems. Do not make every node a different color.
- Keep the canvas bounded and readable at 1920px width.

## UML Rules

### Sequence

- Prefer `scripts/render-sequence-svg.py` for deterministic layout.
- Put lifelines in execution order from left to right.
- Use a fixed lifeline grid and fixed message y-step; do not manually drift arrows off-grid.
- Route self-calls as right-side loops sized to their label width.
- Keep message labels in a separate row above arrows; labels must not cover arrow strokes or self-call vertical segments.
- Group phases with subtle horizontal bands whose heights follow message count.
- Preserve end-to-end flow in a single SVG by default. Use detail diagrams as supplements, not replacements.
- If payloads are long, label the message with the action and put the payload in a note.

### Class

- Use three compartments: name, attributes, methods.
- Show only fields and methods relevant to the requested explanation.
- Use UML arrows consistently: inheritance, implementation, composition, aggregation, association, dependency.

### Use Case

- Keep actors outside the system boundary.
- Keep use cases as verb phrases.
- Use `include`/`extend` only when semantically required.

### State Machine

- Include initial and terminal states when the lifecycle has them.
- Label transitions with trigger/action only when helpful.
- Keep guard conditions short.

### ER

- Use table-like entities with primary keys and foreign keys.
- Keep relationship labels concise and place cardinality near endpoints.

## Files To Load On Demand

- `references/svg-layout-best-practices.md`: always load before creating or reviewing diagrams.
- `references/sequence-layout.md`: load for sequence diagrams; use with `scripts/render-sequence-svg.py` when possible.
- `references/style-4-notion-clean.md`: default style for UML and dense docs.
- `references/style-1-flat-icon.md`: simple architecture/product overview style.
- `references/style-7-openai.md`: clean OpenAI-style palette.
- `references/icons.md`: load for architecture, product, platform, integration, or agent diagrams that benefit from visual symbols.
- `templates/architecture.svg`: use for layered system architecture and product capability maps.
- `templates/agent-architecture.svg`: use for AI agent, tool-calling, RAG, memory, and orchestration diagrams.
- `templates/data-flow.svg`: use for product workflows, API flows, event/data pipelines, and integration diagrams.
- `templates/comparison-matrix.svg`: use for product/module/solution comparison diagrams.
- `templates/sequence.svg`: use for sequence diagram spacing, lifeline placement, message arrows, and notes.
- `templates/use-case.svg`: use for actors, system boundaries, and use-case ellipses.
- `templates/state-machine.svg`: use for state nodes, transitions, start, and terminal states.
- `templates/er-diagram.svg`: use for entity/table layout and relationship notation.
- `templates/flowchart.svg`: use for process/control-flow diagrams.
- `templates/timeline.svg`: use for roadmaps, release plans, migrations, lifecycle stages, and chronological event diagrams.

There is no bundled class template. For class diagrams, follow the UML class rules above and the selected style reference.

## Validation

Run validation before final delivery:

```bash
path/to/skill/scripts/validate-svg.sh diagram.svg
```

Export PNG when requested:

```bash
path/to/skill/scripts/export-png.sh diagram.svg 1920
```

If no renderer is installed, keep the SVG and explain which PNG export dependency is missing.

For generated sequence diagrams, also validate that the rendered `viewBox` covers the rightmost participant and all self-call loops.
