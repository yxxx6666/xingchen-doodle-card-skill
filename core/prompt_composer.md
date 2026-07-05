# prompt_composer — v0.5.0 Structure-Safe Prompt Composer

This module composes final image_gen.text2im prompts. It preserves the v0.4.2 Execution Lock and Aspect Ratio Lock, and adds mandatory structure safety.

## Required input layers

1. user content
2. image_gen-only contract
3. aspect ratio lock
4. anatomy constraints layer
5. scene complexity limiter
6. pose safety layer
7. prompt repair loop

## 🔴 STRUCTURE SAFETY BLOCK（必须自动插入）

Every final prompt must include this block before the visual style details:

```text
STRUCTURE SAFETY BLOCK:
- Structure priority: structure correctness > readability > beauty > richness.
- One main character only by default; do not add a second character unless explicitly requested.
- The character must have exactly two hands and exactly two feet.
- All limbs must be clearly connected to the body.
- No third hand, no hidden hand, no hand emerging from desk, clothes, wall, bag, or background object.
- One simple main action only.
- Each hand has at most one clear action target.
- At most 1–2 interaction objects; all extra objects become simple background props.
- Prefer safe pose: seated, side-standing, slight hand extension, or static action.
- Avoid twisted body, crossed arms, multi-direction action, running, jumping, or complex dynamic pose.
- Do not use occlusion to hide anatomy errors; simplify instead.
```

## Final prompt skeleton

```text
STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.
Create one complete image on a native 3:4 vertical canvas.
Target canvas: 1080×1440 Xiaohongshu-style card, or any exact 3:4 equivalent.

STRUCTURE SAFETY BLOCK:
{mandatory structure block}

A hand-drawn doodle editorial illustration.
Scene: {one simple scene}
Main character: one young Chinese woman, safe pose, one simple action.
Interaction: {one main object only}
Style: minimalist ink doodle, imperfect sketch lines, soft pastel accents, large white negative space.
Composition: exact 3:4 portrait card, subject placed bottom-left or side, large empty space reserved for text.
Chinese text integrated into image:
Title: "{标题}"
Subtitle: "{副标题}"
Optional points:
- {要点1}
- {要点2}
Avoid: extra hands, extra legs, hidden hands, disconnected limbs, complex pose, overloaded scene, multiple actions, fallback renderer, post-processing typography layers.
```

## Composer rule

If content asks for multiple actions or many objects, compose the prompt after repair, not before repair.

## Cross-layer enforcement keywords

This layer is part of v0.5.0 anatomy constraints layer / scene complexity limiter / pose safety / prompt repair loop. Final prompt must include the STRUCTURE SAFETY BLOCK. It reinforces: 结构正确性 > 可读性 > 美观 > 丰富度; one main character; 2只手 / exactly two hands; 2只脚 / exactly two feet; all limbs clearly connected; no 第三只手; no 隐藏手; no 从桌子/衣服/墙里伸出的手; 一个角色只能有一个主动作 / one simple main action; 1~2 个物体; 坐姿; 站立侧身; 删除非必要物体; 降低动作复杂度.

## v0.6.0 Compiler Upgrade

`prompt_composer` is now a compiler, not a free-form prompt writer.

### Compiler inputs

- content_graph
- layout_graph
- anatomy_guard
- scene_limiter
- structure_score

### Compiler output layers

Every final prompt must be compiled in this order:

1. Execution Lock
2. Aspect Ratio Lock
3. STRUCTURE SAFETY BLOCK
4. Layout Block
5. Scene Block
6. Character Block
7. Action Block
8. Props Block
9. Text Block
10. Style Block
11. Negative Block

### RETRY MODE

If structure_score < 85 or risk_level is WARNING / FAIL, add:

```text
RETRY MODE:
- reduce props
- simplify pose
- single action only
- single focal point
```

### Compiler rule

The compiler must not invent extra characters, actions, or props outside the layout_graph.
The compiler must not bypass `image_gen.text2im`.

## v0.6.1 Execution Check

Before calling image_gen:

- check execution_controller approval
- check structure_score
- check layout_mapping

The compiler must not call `image_gen.text2im` unless execution_controller returns approval.

Required compiler layers remain:

1. Execution Lock
2. Aspect Ratio Lock
3. STRUCTURE SAFETY BLOCK
4. Layout Block
5. Scene Block
6. Character Block
7. Action Block
8. Props Block
9. Text Block
10. Style Block
11. Negative Block

`layout_graph → controls prompt` and `layout_prompt_mapping → selects template`.

## v0.6.2 Simulation-first compiler check

Before final prompt is allowed to reach image_gen:

- encoding_guard must pass
- runtime_simulator must pass
- execution_controller must approve
- structure_score and simulated_score must both be >= 85
- execution_trace must be prepared to record the run

Prompt text must remain UTF-8 and Chinese text must be preserved.
