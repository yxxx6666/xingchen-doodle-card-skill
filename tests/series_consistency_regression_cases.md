# Series Consistency Regression Cases v0.8.10

## Case 1 — lettering-family drift

Page 1 uses thick rounded marker Chinese; page 2 uses thin brush calligraphy.

Expected: `series_consistency_status = FAIL`; regenerate page 2 with the same manifest and anchor reference.

## Case 2 — body/title family split

Page title matches the anchor, but body text looks like a printed serif/song type.

Expected: FAIL. Body, chart labels and small labels must use the same regular family token.

## Case 3 — numeral drift

`20%` uses rounded marker numerals on the anchor and narrow technical numerals later.

Expected: FAIL. Numeral and percent-sign construction are locked.

## Case 4 — icon grammar drift

Anchor uses outlined pastel doodles; later page uses solid vector stickers.

Expected: FAIL and regenerate only the later page.

## Case 5 — recurring calendar drift

`calendar-v1` changes from a three-ring desk calendar to a wall calendar.

Expected: FAIL. Reuse the canonical repeated-icon description.

## Case 6 — chart drift

Anchor line chart uses soft-black axes, sage line and orange dashed threshold; later chart uses blue digital grid and sharp vector arrows.

Expected: FAIL. Reuse the canonical chart grammar.

## Case 7 — cover generated after anchor

P02 is selected and approved first; P01 is generated second with the P02 style reference. Final names remain `01-cover-...` and `02-content-...`.

Expected: PASS. Generation order must not change publication order.

## Case 8 — final ZIP order

Source assets arrive in random order. Finalization manifest maps them to 01, 02, 03 names.

Expected: `finalize_series_files.py` produces folder and ZIP member order `01,02,03` without editing pixels.
