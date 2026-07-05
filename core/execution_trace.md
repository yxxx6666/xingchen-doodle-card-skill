# execution_trace — v0.6.2 Execution Trace System

Purpose: record the complete execution chain and make the system observable, verifiable, and traceable.

The system becomes a white-box AI pipeline（可解释生成系统）.

## Required trace output

Every generation must output trace:

```json
{
  "input": "...",
  "content_graph": "...",
  "layout_graph": "...",
  "prompt_version": "...",
  "scorer_before": 0,
  "scorer_after": 0,
  "repair_triggered": false,
  "downgrade_triggered": false,
  "image_gen_called": false,
  "final_state": "SAFE | FAIL"
}
```

## Required pipeline steps

The trace must contain all pipeline steps:

1. input parse
2. encoding_guard check
3. content_graph build
4. layout_graph build
5. runtime_simulator result
6. execution_controller decision
7. prompt_composer version
8. image_gen call state
9. structure_scorer before / after
10. repair loop decision
11. downgrade decision
12. final_state

## Reproducibility goal

The trace must be sufficient to reproduce the generation process without guessing hidden state.

## Production target

```text
execution trace after generation
white-box AI pipeline
```
