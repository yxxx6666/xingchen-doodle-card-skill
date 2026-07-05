# execution_controller — v0.6.1 Central Execution Controller

v0.6.1 architecture = Execution-Controlled System.

This is the only scheduler for the whole pipeline. All `image_gen.text2im` calls must be approved by the execution_controller.

## Hard rules

```text
IF structure_score < 85:
  BLOCK image_gen
  ENTER repair loop

IF structure_score < 70:
  FORCE layout downgrade

IF structure_score < 50:
  FORCE content simplification
```

## Responsibilities

- 控制 content_graph → layout_graph
- 控制 layout_graph → prompt
- 控制 prompt → image_gen
- 控制 scorer → 是否通过
- 控制 repair → 是否触发
- 控制 downgrade → 是否执行

## Approval contract

Before calling `image_gen.text2im`, the controller must verify:

1. execution_state is ready for IMAGE_GEN_CALL.
2. layout_graph exists and was compiled from content_graph.
3. layout_prompt_mapping selected a valid template.
4. structure_score >= 85.
5. risk_level = SAFE.
6. repair_required = false.
7. Execution Lock and Aspect Ratio Lock remain present.
8. image path is still `image_gen.text2im` only.

If any item fails, approval is denied.

## Controller output

```json
{
  "execution_approval": false,
  "next_state": "REPAIR | DOWNGRADE | OUTPUT | IMAGE_GEN_CALL",
  "controller_reason": "",
  "required_action": ""
}
```

## Non-negotiable target

```text
structure_score → controls execution
execution_controller → controls pipeline
image_gen → only allowed under SAFE state
```

## v0.6.2 Full Orchestration Layer

The execution_controller is now the single source of truth and must manage:

- runtime_simulator
- structure_scorer
- encoding_guard
- execution_trace

## New execution order

```text
input
→ encoding_guard
→ content_graph
→ layout_graph
→ runtime_simulator
→ execution_controller decision
→ prompt_composer
→ image_gen (if allowed)
→ structure_scorer
→ execution_trace
→ repair loop
```

## New hard rules

```text
IF encoding_guard FAIL:
  STOP SYSTEM

IF runtime_simulator FAIL:
  BLOCK image_gen

IF structure_score < 85:
  REPAIR
```

## Production decision contract

The controller approves `image_gen.text2im` only when ALL checks pass:

- encoding_guard PASS
- runtime_simulator PASS
- simulated_score >= 85
- structure_score >= 85
- risk_prediction = SAFE
- risk_level = SAFE
- layout_prompt_mapping valid
- prompt_composer contains Execution Lock and Aspect Ratio Lock

```text
controller is single source of truth
image_gen only allowed if ALL checks pass
```
