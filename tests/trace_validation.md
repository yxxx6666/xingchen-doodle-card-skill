# Trace Validation — v0.8.10

Purpose: verify execution trace completeness and reproducibility.

## Trace completeness

Trace must record:

- input
- content_graph
- layout_graph
- prompt_version
- scorer_before
- scorer_after
- repair_triggered
- downgrade_triggered
- image_gen_called
- final_state

## Pipeline step coverage

Trace must include all pipeline steps:

1. input parse
2. encoding guard check
3. content graph build
4. layout graph build
5. runtime simulation
6. execution controller decision
7. prompt compose
8. image_gen call if allowed
9. structure scoring
10. repair / downgrade / output decision
11. execution trace write
12. loop max 3

## Reproducibility

A valid trace must allow the generation process to be replayed or audited without hidden state.

This makes the system a white-box AI pipeline.

## 中文验证目标

- trace 是否完整记录
- 是否包含所有 pipeline steps
- 是否能复现生成过程

## v0.8.10 Viewpoint visibility trace fields

Trace must record:

- viewpoint_visibility_guard_result
- prop_visibility_plan
- visibility_conflicts
- readability_misuse_detected
- viewpoint_visibility_risk_prediction
- readable_surface_perspective_prediction

A valid trace must show whether viewpoint_visibility_guard passed before image_gen.text2im was authorized.

## Required prop role values

Trace validation must preserve `self_reading`, `viewer_presentation`, and `background_prop` in the prop_visibility_plan.
