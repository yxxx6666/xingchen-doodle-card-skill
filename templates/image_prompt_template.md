# Image Generation Card Prompt Template v0.8.10

> Formal backend: Codex `$imagegen`. The request is aspect-ratio-only. Never require fixed pixels.

```text
PAGE: {page_id}/{total_pages}
OUTPUT FILE: {ordered_file_name}
REQUESTED RATIO: 3:4 portrait

Create one complete Chinese doodle editorial card in one native image generation attempt.
The canvas must be native 3:4 portrait, not 2:3, 4:5, 9:16, A4 or a long poster.
Do not target or promise a fixed pixel size.

APPROVED CHINESE TEXT:
{approved_text}

SERIES STYLE LOCK — copy verbatim:
{verbatim_style_block}

LAYOUT:
{layout_graph}

ICON/CHART RULES:
{visual_component_rules}

Keep all critical text inside the outer 7% safe margin. Do not add facts, numbers or English conclusions. Generate the illustration and Chinese text together. The final native canvas must be 3:4 portrait; no fixed pixels are required.
```

After generation, read actual dimensions. Accept only when `abs(width/height-0.75)<=0.001`. Never crop, pad, resize or composite.
