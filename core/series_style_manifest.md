# series_style_manifest — v0.8.10

Purpose: freeze one immutable typography, icon, chart, palette and component system before any publishable page prompt is composed.

## Run order

Run after page allocation, content fidelity and viewpoint validation, and before anchor selection, filename planning, layout compilation and prompt composition.

Read:

- [Typography Consistency Rules](../references/typography-consistency-rules.md)
- [Icon Consistency Rules](../references/icon-consistency-rules.md)
- [Chart Consistency Rules](../references/chart-consistency-rules.md) when any page contains a chart
- [Series Style Manifest Template](../templates/series-style-manifest-template.md)

## Required output

```json
{
  "series_style_status": "PASS | FAIL",
  "series_id": "topic-slug-v1",
  "typography": {
    "family_token": "exact immutable token",
    "cover_title_token": "same family, extra bold",
    "page_title_token": "same family, bold",
    "body_token": "same family, regular",
    "numeral_token": "same family and construction",
    "max_type_families": 1,
    "max_text_levels": 3
  },
  "illustration": {
    "icon_grammar_token": "exact immutable token",
    "line_weight_token": "one stable medium outline",
    "fill_token": "flat low-saturation pastel",
    "perspective_token": "flat front or gentle three-quarter view",
    "detail_band_token": "simple editorial detail",
    "shadow_token": "none or one faint paper shadow"
  },
  "chart_system": {
    "enabled": true,
    "chart_grammar_token": "exact immutable token",
    "axis_token": "soft-black medium axes with rounded arrowheads",
    "primary_series_token": "muted sage",
    "secondary_series_token": "muted orange",
    "label_token": "same as body typography"
  },
  "palette": {
    "background": "warm cream paper",
    "ink": "soft black",
    "accent_1": "muted orange",
    "accent_2": "sage green",
    "accent_3": "dusty blue"
  },
  "components": {
    "callout_shape": "one locked rounded rectangle treatment",
    "highlight_shape": "one locked underline or marker-strip treatment",
    "divider_style": "one locked line or dotted-path treatment",
    "corner_radius_token": "one soft rounded radius"
  },
  "layout_system": {
    "safe_margin": "outer 7 percent",
    "title_zone": "top 18 to 25 percent",
    "content_zone": "middle 60 to 68 percent",
    "footer_zone": "bottom 8 to 12 percent when used",
    "alignment_token": "one chosen alignment system"
  },
  "repeated_icon_dictionary": {},
  "repeated_chart_dictionary": {},
  "verbatim_style_block": "exact block copied unchanged into every prompt"
}
```

## Immutable block rule

- Build `verbatim_style_block` once.
- Copy it byte-for-byte into every page prompt.
- Do not summarize, paraphrase, translate or optimize it per page.
- Page content may change; typography family, numeral construction, icon grammar, chart grammar, palette and component shapes may not.

## Hard gates

```text
IF max_type_families > 1: FAIL
IF max_text_levels > 3: FAIL
IF verbatim_style_block is missing: FAIL
IF any repeated object lacks a canonical icon description: FAIL
IF charts exist and chart_grammar_token is missing: FAIL
IF a later prompt changes or paraphrases the style block: FAIL
```
