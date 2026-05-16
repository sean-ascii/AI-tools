#!/usr/bin/env python3
"""Render a structured sequence-diagram spec to SVG.

Usage:
  render-sequence-svg.py spec.json output.svg

Spec shape:
{
  "title": "fly_to sequence",
  "subtitle": "optional subtitle",
  "participants": [
    {"id": "user", "label": "User", "subtitle": "operator", "type": "actor"}
  ],
  "phases": [
    {"id": "request", "title": "1. Request", "type": "ui"}
  ],
  "messages": [
    {"phase": "request", "from": "user", "to": "api", "label": "submit"},
    {"phase": "request", "from": "api", "to": "api", "label": "validate", "kind": "self"},
    {"phase": "request", "from": "api", "to": "user", "label": "ok", "kind": "return"}
  ]
}
"""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path


PALETTE = {
    "actor": ("#f8fafc", "#cbd5e1", "#64748b"),
    "ui": ("#eff6ff", "#93c5fd", "#2563eb"),
    "service": ("#fff7ed", "#fdba74", "#ea580c"),
    "runtime": ("#fef3c7", "#facc15", "#a16207"),
    "domain": ("#f0fdf4", "#86efac", "#059669"),
    "data": ("#f5f3ff", "#c4b5fd", "#7c3aed"),
    "external": ("#fef2f2", "#fca5a5", "#dc2626"),
}

PHASE_FILL = {
    "actor": "#f8fafc",
    "ui": "#eff6ff",
    "service": "#fff7ed",
    "runtime": "#fef3c7",
    "domain": "#f0fdf4",
    "data": "#f5f3ff",
    "external": "#fef2f2",
}


def usage() -> None:
    print("Usage: render-sequence-svg.py spec.json output.svg", file=sys.stderr)


def text_width(text: str, size: int = 12) -> int:
    # Conservative mixed CJK/Latin approximation for label backgrounds.
    width = 0
    for ch in text:
        width += size if ord(ch) > 127 else int(size * 0.58)
    return max(width, 24)


def svg_text(value: object) -> str:
    return escape(str(value), quote=False)


def attr(value: object) -> str:
    return escape(str(value), quote=True)


def line(x1: int, y1: int, x2: int, y2: int, dashed: bool = False) -> str:
    stroke = "#64748b" if dashed else "#2563eb"
    marker = "arrow-gray" if dashed else "arrow-blue"
    dash = ' stroke-dasharray="5,4"' if dashed else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="1.5"{dash} marker-end="url(#{marker})"/>'
    )


def render(spec: dict) -> str:
    participants = spec.get("participants") or []
    messages = spec.get("messages") or []
    phases = spec.get("phases") or [{"id": "main", "title": "1. Flow", "type": "ui"}]
    if not participants:
        raise SystemExit("spec must include participants")

    participant_ids = [p["id"] for p in participants]
    unknown = sorted(
        {
            endpoint
            for m in messages
            for endpoint in (m.get("from"), m.get("to"))
            if endpoint not in participant_ids
        }
    )
    if unknown:
        raise SystemExit(f"unknown participant id(s): {', '.join(unknown)}")

    phase_ids = [p["id"] for p in phases]
    phase_messages = {phase_id: [] for phase_id in phase_ids}
    for m in messages:
        phase_id = m.get("phase") or phase_ids[0]
        if phase_id not in phase_messages:
            raise SystemExit(f"unknown phase id: {phase_id}")
        phase_messages[phase_id].append(m)

    max_label = max(text_width(p.get("label", ""), 14) for p in participants)
    box_w = min(max(120, max_label + 42), 180)
    max_message_label = max((text_width(m.get("label", ""), 12) for m in messages), default=80)
    spacing = max(190, box_w + 80, min(max_message_label + 80, 260))
    left = 96
    top = 76
    header_h = 42
    phase_x = 40
    phase_top = 132
    message_step = 56
    phase_gap = 14
    self_w = max(88, min(max_message_label + 44, 180))
    right_pad = max(96, self_w + 52)

    centers = {p["id"]: left + i * spacing for i, p in enumerate(participants)}
    content_w = (len(participants) - 1) * spacing + left + right_pad
    width = max(960, content_w)

    phase_layout = []
    y = phase_top
    for phase in phases:
        count = len(phase_messages[phase["id"]])
        height = max(144, 70 + count * message_step)
        phase_layout.append((phase, y, height))
        y += height + phase_gap
    height = max(640, y + 64)
    lifeline_bottom = height - 52

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        "  <defs>",
        '    <marker id="arrow-blue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '      <polygon points="0 0, 10 3.5, 0 7" fill="#2563eb"/>',
        "    </marker>",
        '    <marker id="arrow-gray" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">',
        '      <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>',
        "    </marker>",
        "  </defs>",
        "  <style>",
        '    text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; }',
        "    .title { font-size: 24px; font-weight: 700; fill: #1e293b; }",
        "    .subtitle { font-size: 13px; fill: #64748b; }",
        "    .participant { font-size: 14px; font-weight: 600; fill: #1e293b; }",
        "    .participant-sub { font-size: 12px; fill: #64748b; }",
        "    .phase { font-size: 12px; font-weight: 700; fill: #64748b; letter-spacing: 0.08em; }",
        "    .message { font-size: 12px; fill: #334155; }",
        "    .lifeline { stroke: #cbd5e1; stroke-width: 1.5; stroke-dasharray: 5,5; }",
        "  </style>",
        f'  <rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'  <text x="{width // 2}" y="44" text-anchor="middle" class="title">{svg_text(spec.get("title", "Sequence Diagram"))}</text>',
    ]
    if spec.get("subtitle"):
        out.append(f'  <text x="{width // 2}" y="68" text-anchor="middle" class="subtitle">{svg_text(spec["subtitle"])}</text>')

    # Phase backgrounds first.
    for idx, (phase, py, ph) in enumerate(phase_layout, start=1):
        phase_type = phase.get("type", "ui")
        fill = PHASE_FILL.get(phase_type, "#f8fafc")
        title = phase.get("title", f"{idx}. Phase")
        out.append(f'  <rect x="{phase_x}" y="{py}" width="{width - phase_x * 2}" height="{ph}" rx="8" fill="{fill}" opacity="0.72"/>')
        out.append(f'  <text x="{phase_x + 24}" y="{py + 30}" class="phase">{svg_text(title)}</text>')

    # Participants and lifelines.
    for p in participants:
        cx = centers[p["id"]]
        p_type = p.get("type", "actor")
        fill, stroke, _ = PALETTE.get(p_type, PALETTE["actor"])
        x = cx - box_w // 2
        out.append(f'  <rect x="{x}" y="{top}" width="{box_w}" height="{header_h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        label_y = top + 18 if p.get("subtitle") else top + 27
        out.append(f'  <text x="{cx}" y="{label_y}" text-anchor="middle" class="participant">{svg_text(p.get("label", p["id"]))}</text>')
        if p.get("subtitle"):
            out.append(f'  <text x="{cx}" y="{top + 34}" text-anchor="middle" class="participant-sub">{svg_text(p["subtitle"])}</text>')
        out.append(f'  <line x1="{cx}" y1="{top + header_h}" x2="{cx}" y2="{lifeline_bottom}" class="lifeline"/>')

    # Messages.
    for phase, py, _ in phase_layout:
        for index, m in enumerate(phase_messages[phase["id"]]):
            y_msg = py + 70 + index * message_step
            src = centers[m["from"]]
            dst = centers[m["to"]]
            kind = m.get("kind", "call")
            dashed = kind in {"return", "callback", "async-return"}
            label = str(m.get("label", "message"))
            raw_label_w = max(text_width(label, 12) + 24, 64)
            label_w = min(raw_label_w, max(96, abs(dst - src) - 24 if src != dst else self_w + 44))

            if kind == "self" or src == dst:
                loop_w = max(self_w, label_w + 36)
                loop_x = src + loop_w
                loop_h = 34
                out.append(
                    f'  <path d="M {src} {y_msg} L {loop_x} {y_msg} L {loop_x} {y_msg + loop_h} L {src} {y_msg + loop_h}" '
                    'fill="none" stroke="#2563eb" stroke-width="1.5" marker-end="url(#arrow-blue)"/>'
                )
                lx = src + loop_w // 2
                label_top = y_msg - 34
            else:
                out.append("  " + line(src, y_msg, dst, y_msg, dashed=dashed))
                lx = (src + dst) // 2
                label_top = y_msg - 34

            out.append(f'  <rect x="{lx - label_w // 2}" y="{label_top}" width="{label_w}" height="24" rx="5" fill="#ffffff" opacity="0.96"/>')
            out.append(f'  <text x="{lx}" y="{label_top + 16}" text-anchor="middle" class="message">{svg_text(label)}</text>')

    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    if len(sys.argv) != 3:
        usage()
        return 2
    spec_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    output_path.write_text(render(spec), encoding="utf-8")
    print(f"SVG written: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
