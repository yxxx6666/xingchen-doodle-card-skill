# Compact Prompt Template v0.4.2

Use only when the prompt must be shorter. It still must use `image_gen.text2im`.

## Execution Lock + Single Image Gen Authority

Only `image_gen.text2im` is allowed. No fallback renderer. No local text rendering. No post-processing typography layers. No multi-stage composition pipeline.

```text
A hand-drawn doodle editorial illustration. Scene: {主题}. Style: minimalist ink doodle, imperfect sketch lines, soft pastel accents, large white negative space. Composition: vertical 3:4, subject placed bottom-left or side, with large empty space reserved for text.

Chinese text integrated into image:
Title: "{标题}"
Subtitle: "{副标题}"
Optional points:
- {要点1}
- {要点2}

Mood: calm, warm, educational, reflective.
Avoid: any external text rendering, post-processing typography layers, PIL/Canvas/SVG/HTML rendering, CSS text systems, multi-stage composition pipeline, fallback renderer.
```


## v0.4.2 Canonical 3:4 Prompt

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


## Aspect Ratio Lock

Every image must be exact native 3:4. 2:3, 4:5, 9:16, square, A4, and long poster formats are failed outputs, not minor deviations.


## Aspect Ratio Verification Details

Page-by-page verification is required.

```text
width / height = 0.75
allowed tolerance = 0.745 to 0.755
high-resolution equivalent = 1536×2048
```

A 2:3 output is not a minor deviation. It is failed output.
