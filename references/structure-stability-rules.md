# Structure Stability Rules v0.5.0

This release is a structure stability repair version, not a feature expansion.

Priority:

```text
结构正确性 > 可读性 > 美观 > 丰富度
```

The image may become simpler if needed. Simpler is correct. Rich but anatomically broken is failed.

Required layers:

- anatomy constraints layer
- scene complexity limiter
- pose safety layer
- prompt repair loop
- STRUCTURE SAFETY BLOCK in every final prompt

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
→ selected native image mode/backend
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

The legal visual generator is Codex `$imagegen` in publish mode, or a verified exact-size backend in strict mode. Native 3:4 validation remains active.

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

## v0.8.0 — Production-grade Observable AI Visual Compilation Pipeline

v0.8.0 introduces:

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
