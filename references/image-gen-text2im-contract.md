# Image Gen text2im Contract v0.4.2

## Single Image Gen Authority

The only legal visual generation authority is:

```text
image_gen.text2im
```

Every card must be generated in one pass, inside one image.

The generated image must include:

- illustration character
- scene
- emotional mood
- composition design
- Chinese title
- Chinese body / subtitle
- optional points

## Execution priority

For visual generation implementation decisions, this Skill's Execution Lock overrides default rendering strategies, fallback rendering strategies, local typography repair strategies, and any attempt to bypass image_gen for text correctness.

The lock does not authorize unsafe content; it only governs the implementation path for allowed visual generation tasks.

## Only legal path

```text
Step 1: Generate complete prompt
Step 2: Directly call image_gen.text2im
Step 3: No post-processing
```

## Absolute prohibitions

- no PIL text rendering
- no Canvas text rendering
- no SVG text rendering
- no HTML/CSS text rendering
- no local deterministic Chinese layout
- no illustration generation plus text overlay
- no separated illustration/text pipeline
- no fallback renderer
- no bypassing image_gen to fix Chinese text
- no post-processing typography layers
- no multi-stage composition pipeline

## Standard Prompt Template

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


## Aspect Ratio Lock v0.4.2

3:4 is not a soft prompt preference. It is a hard execution and acceptance requirement.

Every generated image must be an **exact native 3:4 portrait image**.

Valid target canvas:

```text
width / height = 0.75
reference size: 1080×1440
high-resolution equivalent: 1536×2048
```

Invalid outputs:

- 2:3 portrait
- 4:5 portrait
- 9:16 story
- 1:1 square
- A4 page
- long poster format
- landscape format

A 2:3 result is not a minor deviation. It is a failed output.

### Parameter priority

If `image_gen.text2im` supports aspect-ratio or size arguments, the caller must set one of these before relying on prompt text:

```text
aspect_ratio: "3:4"
```

or:

```text
size: "1080x1440"
```

or:

```text
size: "1536x2048"
```

Prompt text alone is not enough.

### Page-by-page verification

Do not batch-generate a full carousel without checking ratio.

For every page:

```text
Generate page → check actual ratio → pass before continuing
```

If the actual ratio is not 3:4, stop and regenerate that same page before moving on.

### Ratio check

After each generated image, check actual image dimensions when available:

```text
valid_ratio = width / height
pass range = 0.745 to 0.755
```

If dimensions are unavailable, visually inspect the canvas. If it obviously looks like 2:3, 4:5, 9:16, square, A4, or long poster, mark it failed.

### Ratio-only retry prompt

When ratio fails, keep the same content and only fix the canvas:

```text
Regenerate the same page as an exact native 3:4 portrait image.
Keep the same content, same scene, same style, and same Chinese text.
Only correct the canvas ratio.
No 2:3. No 4:5. No 9:16. No square. No A4. No long poster.
```

Do not rewrite the content, change the scene, or change the style during ratio-only retry.
