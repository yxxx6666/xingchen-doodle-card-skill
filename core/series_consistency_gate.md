# series_consistency_gate — v0.8.10

Purpose: compare every generated page with the immutable manifest and available approved earlier references before marking the page complete.

## Inputs

- `series_style_manifest`
- `series_anchor_selector` candidate plan
- approved earlier page images, if any
- approved secondary anchor image, only after it is reached in numeric order
- current generated page
- current page prompt
- page role and ordered filename

## Required checks

Score each dimension `PASS`, `WARNING` or `FAIL`:

1. Chinese character family and skeleton
2. title stroke weight, terminals and roundness
3. body-text family, density and line spacing
4. numeral, percent-sign and punctuation construction
5. background paper tone
6. icon and chart outline weight
7. pastel palette and fill density
8. icon perspective and detail band
9. repeated icon identity
10. chart axis, series color, marker and label grammar
11. callout, highlight, divider and corner-radius system
12. safe margins, title zone and overall visual rhythm

## Reference progression

- P01 compares against the immutable manifest only.
- P02 and later compare against the manifest plus already approved earlier pages.
- The representative anchor candidate becomes a secondary reference only after its numeric turn and approval.
- Never require an ungenerated later anchor before P01 or P02 can proceed.
- Different layouts and content-specific objects are allowed; typography family, numerals, icon/chart grammar, palette and components remain locked.

## Major drift examples

- thick rounded marker title changes to thin brush calligraphy;
- body characters become printed or use a different handwriting family;
- number or percent-sign shapes visibly change;
- outlined pastel doodles change to solid vector stickers;
- recurring glass, plate, moon, shoe, calendar or check mark changes silhouette or perspective;
- chart axes, line colors, arrowheads or labels switch style;
- background, callout boxes, highlights or dividers change design language;
- a page introduces gradients, glossy effects, 3D or photorealism.

## Decision

```json
{
  "series_consistency_status": "PASS | WARNING | FAIL",
  "page_id": "P03",
  "reference_page_ids": ["P01", "P02"],
  "secondary_anchor_page_id": "P02",
  "drift_detected": [],
  "repair_instruction": ""
}
```

## Hard gates

```text
IF typography family or numeral drift = FAIL: REGENERATE current page
IF icon or chart grammar drift = FAIL: REGENERATE current page
IF repeated component identity drift = FAIL: REGENERATE current page
IF background, palette or component-system drift = FAIL: REGENERATE current page
IF the prompt lacks the exact manifest style block: RECOMPOSE
IF a later unapproved page is used as a reference: FAIL
IF series_consistency_status != PASS: BLOCK page completion
```

Repair only the current failed page. Preserve approved text, page count, ordered filename, ratio and already approved pages.
