# Changelog

## v0.5.0 - 2026-07-03

### Rename patch

- Renamed public display name to 涂鸦卡片.
- Renamed package / Skill ID to `xingchen-doodle-card-skill`.
- Kept Execution Lock + Single Image Gen Authority rules unchanged.

## v0.5.0 - 2026-07-02

Execution Lock + Single Image Gen Authority patch.

### Added

- Explicit Execution Lock.
- Explicit Single Image Gen Authority.
- Prohibition against bypassing image_gen to fix Chinese text.
- Standard prompt updated to use `imperfect sketch lines` and `with large empty space reserved for text`.
- Avoid list updated to include CSS text systems and multi-stage composition pipeline.

### Kept

- `image_gen.text2im` remains the only legal visual generation path.
- No fallback renderer.
- No local deterministic Chinese layout.
- No post-processing typography layers.

## v0.5.0 — Structure Stability Repair

- Added core/anatomy_guard.md.
- Added core/scene_limiter.md.
- Added core/pose_safety.md.
- Added core/prompt_repair_loop.md.
- Added core/prompt_composer.md with mandatory STRUCTURE SAFETY BLOCK.
- Added references/structure-stability-rules.md.
- Added structure priority system: 结构正确性 > 可读性 > 美观 > 丰富度.
- Added one-main-character default rule.
- Added exactly two hands / two feet / connected limbs constraints.
- Added one simple main action limit.
- Added 1–2 interaction object limit.
- Added scene overload repair rules.
- Added prompt repair loop with simplification priority.
- Updated prompt templates with structure safety block.
- Updated quick_validate.py for v0.5.0 structure stability checks.

## v0.6.0 — Structure-aware Compilation System

- added structure scorer
- added layout graph compiler
- added content graph builder
- added repair policy matrix
- added generation loop
- upgraded prompt composer to compiler
- added scoring-based repair loop
- added tests/regression_cases.md
- strengthened tests/test_cases.json with structure_score_expected, failure_modes_expected, repair_strategy_expected
- upgraded quick_validate.py for v0.6.0 semantic checks

## v0.6.1 — Execution-Controlled System

- added execution controller
- added state machine
- added hard gate system
- added layout_prompt_mapping
- upgraded layout_graph to controller role
- upgraded scorer to decision system
- converted generation_loop into state machine
- made image_gen.text2im calls controller-gated
- strengthened regression cases with expected structure_score and expected layout_type

## v0.6.2 — Production-grade Observable AI Visual Compilation Pipeline

- added runtime simulation system
- added encoding guard system
- added execution trace system
- upgraded controller to full orchestration layer
- added pre-execution validation stage
- upgraded generation_loop to simulation-first pipeline
- added simulation-aware structure scoring
- added production hard gates for encoding and runtime simulation
- added runtime_tests.md and trace_validation.md
