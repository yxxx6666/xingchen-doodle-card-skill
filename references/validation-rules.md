# Validation Rules v0.4.2

## Required semantics

Active generation files must include:

- image_gen.text2im
- Single Image Gen Authority or Execution Lock
- A hand-drawn doodle editorial illustration.
- Style: minimalist ink doodle, imperfect sketch lines, soft pastel accents, large white negative space.
- Composition: vertical 3:4, subject placed bottom-left or side, with large empty space reserved for text.
- Chinese text integrated into image:
- Title:
- Subtitle:
- Optional points:
- Mood: calm, warm, educational, reflective.
- any external text rendering
- post-processing typography layers
- PIL/Canvas/SVG/HTML rendering
- CSS text systems
- multi-stage composition pipeline
- fallback renderer

## Forbidden active implementation patterns

- PIL / Canvas / SVG / HTML / CSS rendering as a generation path.
- local deterministic Chinese layout as a generation path.
- illustration plus text overlay as a generation path.
- separated illustration/text pipeline as a generation path.
- fallback renderer as a generation path.
- bypassing image_gen to fix Chinese text.

## Acceptance

A valid output must be:

- complete illustration card
- Chinese visible in image
- no PPT / information-graphic feeling
- no programmatic drawing feeling
- no post-processing typography layer
- clear negative space
- editorial magazine layout feel
- unified style


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

## v0.5.0 Structure Stability Repair

This is not a feature expansion. It strengthens structure safety for image_gen doodle card prompts.

New priority system:

```text
结构正确性 > 可读性 > 美观 > 丰富度
```

New pipeline layers:

1. anatomy constraints layer
2. scene complexity limiter
3. pose safety layer
4. prompt repair loop
5. mandatory STRUCTURE SAFETY BLOCK in final prompts

Core goal: reduce three hands / three feet / disconnected limbs / hands growing from wrong places / multi-action collapse / scene overload distortion.

The v0.4.2 Execution Lock remains unchanged: the only legal renderer is `image_gen.text2im`. No PIL, Canvas, SVG, HTML, fallback renderer, or post-processing typography layer is allowed.

## v0.6.0 — Structure-aware Compilation System

v0.6.0 = structure-aware compilation system.

This is a system-level refactor: rule-based prompt system → compiler-based system.

It is a compilation system, not a free prompt system:

```text
input
→ content_graph_builder
→ layout_graph_compiler
→ anatomy_guard
→ scene_limiter
→ prompt_composer compiler
→ image_gen.text2im
→ structure_scorer
→ repair_policy_matrix if fail
→ regenerate
→ max_attempts = 3
```

Why structure scoring is needed:

- It gives anatomy, action, scene, and interaction risk a measurable score.
- It prevents rich but broken scenes from passing as acceptable.
- It triggers repair before repeated generation.

Why layout graph is core:

- It limits the image to one focal point.
- It controls props, action, character, and empty space before the prompt is written.
- It prevents every content point from becoming a drawn object.

Why repair loop is needed:

- It turns failures into deterministic simplification steps.
- Level 1 compresses and removes decoration.
- Level 2 repairs structure.
- Level 3 safely downgrades to title + single character + 3 points.

The legal renderer remains unchanged: only `image_gen.text2im` is allowed. 3:4 Aspect Ratio Lock remains active.

## v0.6.1 — Execution-Controlled System

This is NOT a prompt system.
This is a controlled visual compilation system.

v0.6.1 architecture adds:

- execution controller
- state machine
- hard gate system
- layout → prompt mapping
- scoring system as decision system
- repair loop controlled by structure_score

The system is upgraded from compiler → controlled compiler.

### Why execution controller is necessary

The execution_controller is the central scheduler. It controls content_graph → layout_graph, layout_graph → prompt, prompt → image_gen, scorer decisions, repair, and downgrade.

### Why scorer decides flow

`structure_score` is no longer a passive report. It controls execution:

```text
score >= 85 → allow image_gen
70–84 → repair once
50–69 → layout downgrade
<50 → full simplification
```

### Why layout drives prompt

The layout_graph is the prompt structure controller. `layout_prompt_mapping` maps:

```text
title_scene_bullets → template_A
single_scene_editorial → template_B
list_scene_hybrid → template_C
title_object_ring → template_D
```

### Why state machine is necessary

The state_machine prevents direct, uncontrolled image generation and forces every call through INIT → PARSE_CONTENT → BUILD_CONTENT_GRAPH → BUILD_LAYOUT_GRAPH → PROMPT_COMPOSE → IMAGE_GEN_CALL → SCORE → DECIDE.

### Final system target

```text
structure_score → controls execution
execution_controller → controls pipeline
layout_graph → controls prompt
state_machine → controls flow
repair_loop → controls recovery
image_gen → only allowed under SAFE state
```

## v0.6.2 — Production-grade Observable AI Visual Compilation Pipeline

v0.6.2 introduces:

- runtime simulation layer
- encoding safety layer
- execution trace system

The system is now observable, simulation-driven, and execution-traceable.

It upgrades the controlled compiler into a production-grade deterministic AI pipeline.

### Runtime simulation layer

Before real `image_gen.text2im`, the system runs:

```text
input → content_graph → layout_graph → prompt_composer → fake_image_gen_simulation → structure_scorer
```

If simulated_score < 85, do not call image_gen and force repair loop.

### Encoding safety layer

The encoding_guard enforces UTF-8 across SKILL.md, README.md, metadata, prompts, and Chinese text. If encoding_guard FAIL, stop system and block installation.

### Execution trace system

Each generation must record trace fields: input, content_graph, layout_graph, prompt_version, scorer_before, scorer_after, repair_triggered, downgrade_triggered, image_gen_called, final_state.

### Final target

```text
simulation before generation
encoding safety before pipeline
execution trace after generation
scorer controls execution
controller is single source of truth
image_gen only allowed if ALL checks pass
```
