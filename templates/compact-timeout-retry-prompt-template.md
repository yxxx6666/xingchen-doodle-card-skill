# Compact Timeout Retry Prompt v0.8.10

Use only after a `$imagegen` service timeout. Do not change approved content.

```text
OUTPUT FILE NAME: {ordered_file_name}
PAGE: {page_index}/{recommended_total_pages} — {page_role}

Generate one finished 3:4 portrait Xiaohongshu doodle card. The returned image itself must be true 3:4, not 2:3, 4:5, 9:16 or square.

EXACT APPROVED CHINESE TEXT:
{approved_page_text}

STYLE LOCK:
{verbatim_style_block}

LAYOUT:
{layout_graph_for_page}

REQUIRED ICONS/CHARTS ONLY:
{required_canonical_components}

Use one main subject/action, simple flat editorial composition, one visual reference image at most, and no nonessential decoration. Keep all facts, numbers and Chinese wording unchanged. Generate illustration and text together. No crop, padding, resize, overlay or post-processing.

FINAL: Return one native true 3:4 portrait card.
```
