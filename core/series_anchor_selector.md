# series_anchor_selector — v0.8.10

Purpose: choose a representative content page as a future secondary visual reference without changing strict numeric generation order.

## Run order

Run after `series_style_manifest` and filename planning, before generation begins.

## Selection score

Score every planned page:

```text
+3 contains a normal page title and body text
+2 contains representative recurring icons
+2 contains a chart when any page in the series contains a chart
+1 contains the standard callout/highlight/divider components
+1 uses the dominant layout density of the series
-4 is cover-only with oversized decorative title
-3 is a closing page with very little content
```

Choose the highest-scoring page as `anchor_candidate_page_id`. Break ties by the lowest page index. For a one-page series, use P01.

## Strict order rule

- Generation order is always `P01, P02, P03, ... Pn`.
- Never generate the anchor candidate early.
- P01 is generated first using the immutable style manifest only.
- After P01 passes, it becomes the provisional visual reference for palette, paper texture, line weight and title treatment.
- When the anchor candidate is reached naturally in numeric order and passes, it becomes the secondary visual reference for body typography, recurring icons and chart grammar.
- The anchor candidate affects reference selection only, never scheduling.

## Required output

```json
{
  "anchor_selection_status": "PASS | FAIL",
  "anchor_candidate_page_id": "P02",
  "anchor_candidate_ordered_file_name": "02-content-topic.png",
  "active_visual_reference_before_p01": "manifest-only",
  "generation_order": ["P01", "P02", "P03", "P04"],
  "delivery_order": ["P01", "P02", "P03", "P04"],
  "selection_reason": "contains title, body, recurring icons and chart grammar"
}
```

## Hard gates

```text
IF generation_order does not start with P01: FAIL
IF generation_order != delivery_order: FAIL
IF anchor candidate is generated before its numeric turn: BLOCK
IF anchor selection changes filenames or page order: FAIL
IF a supported reference-image path exists but later eligible pages omit available approved references: RECOMPOSE
```
