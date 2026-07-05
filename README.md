# 涂鸦卡片

Owner tag: `xingchen`
Skill ID: `xingchen-doodle-card-skill`

Version: v0.6.2

## Positioning

Execution Lock + Single Image Gen Authority.

The only goal is to use `image_gen.text2im` to generate a complete Chinese hand-drawn doodle editorial illustration card in one pass.

The image must include illustration character, scene, mood, composition, Chinese title, and Chinese body text.

## Only legal path

1. Generate complete prompt.
2. Directly call `image_gen.text2im`.
3. No post-processing.

## Prohibited

- PIL / Canvas / SVG / HTML / CSS text rendering.
- local deterministic Chinese layout.
- illustration generation + text overlay.
- separated illustration/text pipeline.
- fallback renderer.
- bypassing image_gen to fix Chinese text.

## Standard prompt

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


## Aspect Ratio Lock v0.5.0

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

The v0.5.0 Execution Lock remains unchanged: the only legal renderer is `image_gen.text2im`. No PIL, Canvas, SVG, HTML, fallback renderer, or post-processing typography layer is allowed.

## 🔴 STRUCTURE SAFETY BLOCK（必须自动插入）

```text
STRUCTURE SAFETY BLOCK:
- Structure priority: 结构正确性 > 可读性 > 美观 > 丰富度.
- Use one main character / 每个画面默认仅 1 个主角色.
- The character must have 2只手 / exactly two hands.
- The character must have 2只脚 / exactly two feet.
- all limbs clearly connected / 所有肢体必须明确连接身体.
- No 第三只手, no 隐藏手, no 从桌子/衣服/墙里伸出的手.
- 一个角色只能有一个主动作 / one simple main action only.
- 每个角色最多交互 1~2 个物体; extra objects become background props.
- scene complexity limiter: 单画面最多 1 个主场景; 静态物体最多 6~12 个; 信息 > 5 个要点必须视觉分组或拆卡片.
- pose safety: prefer 坐姿, 站立侧身, 轻微伸手, 静态动作.
- Avoid 大幅扭转身体, 双臂交叉复杂动作, 多方向同时动作, 高动态姿态.
- prompt repair loop: 删除非必要物体 → 降低动作复杂度 → 将双手动作改为单手 → 改为坐姿/静态姿态 → 减少场景元素 → 强制重新生成 prompt.
- Do not use occlusion to hide anatomy errors; 宁可简化，不可错误.
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
