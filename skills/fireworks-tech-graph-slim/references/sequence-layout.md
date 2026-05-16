# Sequence Diagram Layout

Load this for sequence diagrams. Prefer `scripts/render-sequence-svg.py` for medium or large sequence diagrams because it calculates lifeline grid, message y positions, phase bands, and `viewBox` bounds deterministically.

## Process

1. Extract participants in left-to-right execution order.
2. Group messages into phases.
3. Shorten long payloads into action labels; move details to notes or surrounding text.
4. Write a JSON spec with `participants`, `phases`, and `messages`.
5. Run `scripts/render-sequence-svg.py spec.json output.svg`.
6. Run `scripts/validate-svg.sh output.svg`.

Default to one complete sequence diagram. Do not split only because there are many participants or messages; the renderer expands the `viewBox`. Split only when the user asks for separate views or when the full diagram remains unreadable after shortening labels and using the generated grid. If splitting, preserve a complete overview and add detail diagrams as supplements.

## Spec Fields

- `participants[].id`: stable id used by messages.
- `participants[].label`: visible participant name.
- `participants[].subtitle`: optional role or implementation detail.
- `participants[].type`: `actor`, `ui`, `service`, `runtime`, `domain`, `data`, or `external`.
- `phases[].id`: stable phase id.
- `phases[].title`: visible phase label.
- `phases[].type`: color category for the phase band.
- `messages[].phase`: phase id.
- `messages[].from` / `to`: participant ids.
- `messages[].label`: short message label.
- `messages[].kind`: `call`, `return`, `callback`, or `self`.

## Geometry Rules

- Lifeline centers are evenly spaced; the script uses at least `190px` spacing and expands for long labels.
- Message y positions use a fixed `56px` step.
- Phase height is derived from message count.
- Self-calls use a right-side loop that expands for label width.
- Message labels sit in a separate row above the arrow and must not cover arrow strokes or self-call vertical segments.
- Calls use solid blue arrows; returns/callbacks use dashed gray arrows.
- `viewBox` expands from participant count and phase height, which prevents right-edge clipping.
- Large diagrams should grow wider or taller before being split.

## Minimal Spec

```json
{
  "title": "Skill execution sequence",
  "subtitle": "Command dispatch to result update",
  "participants": [
    {"id": "user", "label": "User", "type": "actor"},
    {"id": "ui", "label": "Frontend", "subtitle": "SkillPanel + WS", "type": "ui"},
    {"id": "server", "label": "Server", "subtitle": "SocketIO", "type": "service"}
  ],
  "phases": [
    {"id": "request", "title": "1. Command dispatch", "type": "ui"}
  ],
  "messages": [
    {"phase": "request", "from": "user", "to": "ui", "label": "choose parameters"},
    {"phase": "request", "from": "ui", "to": "server", "label": "execute_skill event"},
    {"phase": "request", "from": "server", "to": "server", "label": "validate state", "kind": "self"},
    {"phase": "request", "from": "server", "to": "ui", "label": "accepted", "kind": "return"}
  ]
}
```
