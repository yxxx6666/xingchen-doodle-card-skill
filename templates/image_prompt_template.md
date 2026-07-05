# Image Prompt Template v0.4.2

Only use `templates/image-gen-card-prompt-template.md`.
Only use `image_gen.text2im`.

## Execution Lock + Single Image Gen Authority

Only `image_gen.text2im` is allowed. No fallback renderer. No local text rendering. No post-processing typography layers. No multi-stage composition pipeline.

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

## v0.5.0 STRUCTURE SAFETY BLOCK（必须自动插入）

```text
STRUCTURE SAFETY BLOCK:
- Structure priority: structure correctness > readability > beauty > richness.
- One main character only by default.
- Exactly two hands and exactly two feet.
- All limbs clearly connected to the body.
- No third hand, no hidden hand, no hand emerging from desk/clothes/wall/bag/background.
- One simple main action only.
- Each hand has at most one clear action target.
- At most 1–2 interaction objects; extra objects become background props.
- Prefer seated pose, side-standing pose, slight hand extension, or static action.
- Avoid twisted body, crossed arms, multi-direction action, high dynamic pose, running, jumping.
- Do not use occlusion to hide anatomy errors; simplify instead.
```

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
