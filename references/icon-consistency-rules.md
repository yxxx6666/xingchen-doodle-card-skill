# Icon Consistency Rules v0.8.10

## Goal

Make illustrations, chart symbols and supporting objects share one stable icon grammar across the entire series.

## Default icon grammar

Copy this exact grammar unchanged into every page prompt through the series style manifest:

```text
flat 2D hand-drawn editorial doodle icon, soft-black imperfect outline, one stable medium line weight, rounded joins and terminals, low-saturation pastel fill covering about half to three quarters of the shape, sparse pencil texture, simple front or gentle three-quarter view, no gradient, no glossy highlight, no 3D extrusion, no photorealistic shadow
```

## Line-weight lock

- Use one outline-weight token for all icons and charts.
- Small supporting icons may be simplified, but their visible stroke must not appear much thinner or thicker than the anchor icon system.
- Do not mix fine pen, thick crayon, vector hairline and sticker-outline systems.

## Repeated icon dictionary

Before generating the anchor, register every object likely to repeat. Each entry defines:

- canonical name and version;
- silhouette and proportions;
- viewpoint;
- outline weight and terminal style;
- fill colors and fill density;
- texture and shadow rule;
- prohibited variations.

Example:

```text
calendar-v1: small standing desk calendar, rounded rectangular page, three soft-black top rings, pale cream paper, sage grid, muted orange check mark, gentle front three-quarter view, same medium outline, no shadow, no alternate binding.
```

Whenever `calendar-v1` reappears, reuse the exact description. Do not replace it with a wall calendar, phone calendar, emoji, vector check icon or different perspective.

## Complexity lock

Choose one detail band for the series:

```text
simple editorial detail: recognizable silhouette, 2–5 interior detail lines, flat pastel fill, sparse texture
```

A hero illustration may be larger, but must not become photorealistic or far more detailed than supporting icons.

## Chart integration

Charts use the same outline, palette, rounded terminals and texture as icons. Follow [Chart Consistency Rules](chart-consistency-rules.md).

## Failures requiring regeneration

- outlined doodle on one page and solid sticker/vector icon on another;
- recurring object changes silhouette, viewpoint, line weight or color identity;
- one page adds emoji, clip art, gradients, heavy shadows, 3D or photorealism;
- a plate, glass, shoe, moon, calendar or check mark is redrawn in a different component language;
- chart symbols look digitally typeset while surrounding icons are hand drawn.
