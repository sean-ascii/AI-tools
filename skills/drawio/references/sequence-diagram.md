# Draw.io Sequence Diagram Reference

Load this reference when creating or editing a sequence diagram in draw.io XML.

## Structure

- Use `shape=umlLifeline;perimeter=lifelinePerimeter;size=50;whiteSpace=wrap;html=1;` for participants.
- Put phase backgrounds before lifelines and messages so they render behind the main diagram.
- Use phase labels as text cells near the top-left of each phase band.
- Use explicit `sourcePoint` and `targetPoint` coordinates for sequence messages. This is more predictable than `source` and `target` connection routing on lifeline shapes.
- Use stable ids: `p1`, `p2`, `m1`, `m2`, `bg1`, `lbl1`.

## Layout Defaults

- Start participants near `y=20`.
- Participant header width: `90-150`; height should span the full sequence body.
- Horizontal spacing between participant centers: `130-180`.
- Message vertical spacing: `25-40`.
- Keep message labels short enough to fit between lifelines. Split long explanations into multiple messages or phase labels.
- For more than 8-10 participants or 35-40 messages, consider multiple pages or separate diagrams by phase.

## Participant Example

```xml
<mxCell id="p1" value="Client" style="shape=umlLifeline;perimeter=lifelinePerimeter;size=50;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="40" y="20" width="110" height="620" as="geometry"/>
</mxCell>
```

Use `&#xa;` for intentional line breaks in participant labels:

```xml
<mxCell id="p2" value="API&#xa;(Service)" style="shape=umlLifeline;perimeter=lifelinePerimeter;size=50;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="210" y="20" width="130" height="620" as="geometry"/>
</mxCell>
```

## Message Examples

Forward call:

```xml
<mxCell id="m1" value="request(payload)" style="endArrow=open;endSize=6;html=1;fontSize=10;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="95" y="120" as="sourcePoint"/>
    <mxPoint x="275" y="120" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

Return message:

```xml
<mxCell id="m2" value="response" style="endArrow=open;endSize=6;html=1;fontSize=10;dashed=1;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="275" y="150" as="sourcePoint"/>
    <mxPoint x="95" y="150" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

Self-call:

```xml
<mxCell id="m3" value="validate()" style="endArrow=open;endSize=6;html=1;fontSize=10;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="275" y="185" as="sourcePoint"/>
    <mxPoint x="275" y="210" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="345" y="185"/>
      <mxPoint x="345" y="210"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## Phase Bands

Use low-opacity background rectangles to group long flows. Keep them wide enough to cover all lifelines and tall enough to include their messages.

```xml
<mxCell id="bg1" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;opacity=30;" vertex="1" parent="1">
  <mxGeometry x="20" y="95" width="700" height="140" as="geometry"/>
</mxCell>
<mxCell id="lbl1" value="1. Request phase" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontStyle=1;fontSize=11;fontColor=#3F51B5;" vertex="1" parent="1">
  <mxGeometry x="30" y="100" width="180" height="18" as="geometry"/>
</mxCell>
```

## Visual Semantics

- Use consistent colors by participant category. For example: UI/client blue, server/runtime yellow, domain/service green, external/simulator red, human/user gray.
- Use solid arrows for calls and dashed arrows for returns or callbacks.
- Keep phase band colors aligned with the dominant actor for that phase when possible.
- Avoid saturated backgrounds; use `opacity=20-35` for phase bands.

## Readability Checks

- The diagram should not look blank after export.
- Lifeline headers should not overlap.
- Message labels should not collide with phase labels or other messages.
- Self-call loops should have enough horizontal offset to be visible.
- Canvas size should be intentional. Very large diagrams should usually be split into pages or phase-specific files.
