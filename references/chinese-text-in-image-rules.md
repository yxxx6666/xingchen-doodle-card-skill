# Chinese Text In Image Rules v0.4.2

## Required

Chinese must be written directly into the `image_gen.text2im` prompt.

Required fields:

```text
Title: "{中文标题}"
Subtitle: "{中文副标题}"
Optional points:
- {要点1}
- {要点2}
```

## Text priority

- Chinese must not be missing.
- Slight imperfection is acceptable.
- Style consistency is more important than perfect Chinese typography.
- Do not bypass image_gen to fix Chinese errors.

## Forbidden

- external text rendering
- post-processing typography layers
- PIL/Canvas/SVG/HTML rendering
- CSS text systems
- local deterministic Chinese layout
- multi-stage composition pipeline
- fallback renderer


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
