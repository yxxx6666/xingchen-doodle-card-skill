# Chinese Text In Image Rules v0.8.10

Chinese text must be generated inside the same `image_gen.text2im` result as the illustration. No local text renderer or post-processing layer is allowed.

## Exact-match critical fields

The following must be correct before acceptance:

- page title;
- all numbers and percentages;
- units and time windows;
- dates;
- medicine, disease, institution and research names when present;
- evidence-based conclusions and caution words.

A wrong or missing critical field requires regeneration of that page.

## Flexible fields

Minor punctuation differences or slight handwritten glyph deformation may be accepted only when meaning and readability are unaffected.

## Density

- Prefer a short title and concise body lines.
- Split dense content into additional pages instead of shrinking text.
- Keep critical text in independent card text areas, not on self-reading props.

## Fidelity

Only use `approved_page_text`. Do not add facts, numbers, English claims, stronger certainty or promotional promises.

## Forbidden

- external text rendering;
- PIL, Canvas, SVG, HTML/CSS typography;
- local deterministic Chinese layout;
- illustration plus later text overlay;
- fallback renderer;
- accepting a wrong title or wrong number because the image looks attractive.
