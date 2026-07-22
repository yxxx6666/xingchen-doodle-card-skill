# Chart Consistency Rules v0.8.10

## Goal

Treat every chart as part of the same hand-drawn component library. Charts must not switch between doodle illustration, polished vector dashboard, spreadsheet grid, 3D chart or infographic sticker styles.

## Canonical chart grammar

Copy this grammar unchanged into the series style manifest when charts are present:

```text
hand-drawn editorial chart on warm cream paper; soft-black imperfect axes with one stable medium stroke; small rounded arrowheads; muted sage primary data line; muted orange comparison, threshold or warning line; rounded line caps; sparse labels in the same regular handwritten Chinese family as body text; no gradients, no 3D, no digital dashboard chrome, no dense grid and no photorealistic effects
```

## Locked chart tokens

Before generating the anchor page, define:

- `axis_token`: color, stroke weight, arrowhead shape;
- `primary_series_token`: color and line treatment;
- `secondary_series_token`: color and line treatment;
- `point_marker_token`: none, small circle or small dot—choose one;
- `label_token`: same family and weight as body text;
- `grid_token`: absent by default, or one faint sparse grid system only;
- `chart_frame_token`: no frame by default, or the same rounded callout frame used elsewhere;
- `chart_perspective_token`: flat front-facing 2D only.

## Reuse rule

When a chart type repeats, register a canonical component description such as:

```text
line-chart-v1: flat front-facing hand-drawn line chart, soft-black x/y axes, small rounded arrowheads, muted sage curved primary line, muted orange dashed threshold, no grid, no shadow, body-family labels.
```

Reuse the exact description. Do not change axis color, line weight, arrowheads, curve style, label family or palette on later pages.

## Failures requiring regeneration

- one chart has thin digital axes and another has thick sketch axes;
- green means the primary series on one page but orange means the same series later;
- labels use a different lettering family from body text;
- chart changes from flat doodle to vector dashboard, glossy, 3D or grid-heavy style;
- repeated chart type changes arrowheads, markers, curve treatment or frame without a manifest rule.
