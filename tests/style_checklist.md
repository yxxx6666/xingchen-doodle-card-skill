# Style Checklist v0.4.2

## Execution Lock

- [ ] Only image_gen.text2im.
- [ ] Single complete image generation.
- [ ] No fallback renderer.
- [ ] No local text rendering.
- [ ] No PIL / Canvas / SVG / HTML / CSS text systems.
- [ ] No separated illustration/text pipeline.
- [ ] No post-processing typography layers.
- [ ] No bypassing image_gen to fix Chinese text.

## Required prompt fields

- [ ] A hand-drawn doodle editorial illustration.
- [ ] Scene.
- [ ] Style: minimalist ink doodle, imperfect sketch lines, soft pastel accents, large white negative space.
- [ ] Composition: vertical 3:4, subject placed bottom-left or side, with large empty space reserved for text.
- [ ] Chinese text integrated into image.
- [ ] Title.
- [ ] Subtitle.
- [ ] Optional points.
- [ ] Mood: calm, warm, educational, reflective.

## Aspect Ratio Lock

- [ ] Every page is exact native 3:4.
- [ ] First prompt line says STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.
- [ ] 1080×1440 or exact 3:4 equivalent is specified.
- [ ] 2:3 / 4:5 / 9:16 / square / A4 / long poster are explicitly forbidden.
- [ ] Each page is checked before continuing.
- [ ] Wrong ratio is marked failed, not a minor deviation.
