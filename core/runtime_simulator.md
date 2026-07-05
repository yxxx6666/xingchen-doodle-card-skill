# runtime_simulator — v0.6.2 Runtime Simulation System

Purpose: run simulated execution validation before any real `image_gen.text2im` call.

This makes the system simulation-driven and prevents unsafe prompts from reaching image generation.

## Simulation flow

```text
input
→ content_graph
→ layout_graph
→ prompt_composer
→ fake_image_gen_simulation
→ structure_scorer
```

## Simulation goals

Validate without calling image_gen:

- 是否会出现三只手
- layout 是否过载
- prompt 是否安全
- structure_score 是否达标
- whether props or actions exceed safe limits
- whether image_gen text remains parseable

## Output

```json
{
  "simulated_score": 0,
  "risk_prediction": "SAFE | WARNING | FAIL",
  "predicted_issues": [],
  "should_execute": false
}
```

## Mandatory rule

```text
IF simulated_score < 85:
  DO NOT CALL image_gen
  FORCE repair loop
```

## Simulation failure

A runtime_simulator FAIL means:

- image_gen is blocked
- execution_controller must enter repair loop
- execution_trace must record `image_gen_called: false`

## Production target

```text
simulation before generation
```
