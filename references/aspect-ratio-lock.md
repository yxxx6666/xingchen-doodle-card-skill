# Aspect Ratio Lock v0.4.2

## Core rule

3:4 is a hard requirement, not a prompt suggestion.

Every output must be a native 3:4 portrait image.

```text
valid width / height = 0.75
allowed tolerance = 0.745–0.755
reference size = 1080×1440
high-resolution equivalent = 1536×2048
```

## Invalid ratios

- 2:3
- 4:5
- 9:16
- 1:1
- A4
- landscape
- long poster

2:3 is not a minor deviation. It is failed output.

## Parameter first

If `image_gen.text2im` supports generation arguments, always set:

```text
aspect_ratio: "3:4"
```

If size is supported, use:

```text
size: "1080x1440"
```

or:

```text
size: "1536x2048"
```

Prompt-only ratio control is not sufficient.

## Prompt first line

Every final prompt must begin with:

```text
STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.
Create one complete image on a native 3:4 vertical canvas.
Target canvas: 1080×1440 Xiaohongshu-style card, or any exact 3:4 equivalent.
Do not use 2:3, 4:5, 9:16, square, A4, landscape, or long poster format.
```

## Page-by-page verification

Do not generate a full carousel in one unchecked batch.

Workflow:

```text
Page 1 prompt → image_gen.text2im → ratio check → pass → Page 2
```

If a page fails ratio, regenerate that page before continuing.

## Ratio-only retry

```text
Regenerate the same page as an exact native 3:4 portrait image.
Keep the same content, same scene, same style, and same Chinese text.
Only correct the canvas ratio.
No 2:3. No 4:5. No 9:16. No square. No A4. No long poster.
```

## Forbidden claims

- Do not say a 2:3 image is acceptable.
- Do not call wrong ratio a minor deviation.
- Do not continue to the next page before fixing ratio.
- Do not crop, pad, stretch, or locally redraw the image as a replacement for native 3:4 generation.


## Execution Lock + Single Image Gen Authority

This ratio protocol is part of Execution Lock and Single Image Gen Authority.
Only image_gen.text2im is allowed. No fallback renderer. No local text rendering. No post-processing typography layers. No multi-stage composition pipeline.

## Canonical prompt skeleton

```text
STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.
Create one complete image on a native 3:4 vertical canvas.
Target canvas: 1080×1440 Xiaohongshu-style card, or any exact 3:4 equivalent.
Do not use 2:3, 4:5, 9:16, square, A4, landscape, or long poster format.

A hand-drawn doodle editorial illustration.

Scene: {主题}
Style: minimalist ink doodle, imperfect sketch lines, soft pastel accents, large white negative space.

Composition: exact 3:4 portrait card, subject placed bottom-left or side, with large empty space reserved for text.

Chinese text integrated into image:
Title: "{标题}"
Subtitle: "{副标题}"
Optional points:
- {要点1}
- {要点2}

Mood: calm, warm, educational, reflective.

Avoid:
- 2:3 aspect ratio
- 4:5 aspect ratio
- 9:16 aspect ratio
- square image
- A4 page
- long poster format
- any external text rendering
- post-processing typography layers
- PIL/Canvas/SVG/HTML rendering
- CSS text systems
- multi-stage composition pipeline
- fallback renderer
```
