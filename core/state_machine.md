# state_machine — v0.6.1 Execution State Machine

The state_machine controls flow. generation_loop must follow this machine instead of describing a loose process.

## States

```text
INIT
→ PARSE_CONTENT
→ BUILD_CONTENT_GRAPH
→ BUILD_LAYOUT_GRAPH
→ PROMPT_COMPOSE
→ IMAGE_GEN_CALL
→ SCORE
→ DECIDE
→ (REPAIR | DOWNGRADE | OUTPUT)
```

## Max loop

```text
max_attempts = 3
```

## State responsibilities

1. INIT: create execution context and attempt counter.
2. PARSE_CONTENT: parse raw user content.
3. BUILD_CONTENT_GRAPH: call content_graph_builder.
4. BUILD_LAYOUT_GRAPH: call layout_graph_compiler.
5. PROMPT_COMPOSE: call prompt_composer compiler.
6. IMAGE_GEN_CALL: call `image_gen.text2im` only if execution_controller approves.
7. SCORE: call structure_scorer and produce structure_score / risk_level.
8. DECIDE: route to OUTPUT, REPAIR, or DOWNGRADE.
9. REPAIR: call repair_policy_matrix and prompt_repair_loop.
10. DOWNGRADE: force layout downgrade or content simplification.
11. OUTPUT: return final SAFE result.

## Decision routes

```text
IF SAFE → OUTPUT
IF WARNING → REPAIR once
IF FAIL → DOWNGRADE + regenerate
IF attempts >= 3 → safest output or stop, never switch renderer
```

## Enforcement

The state_machine must not allow direct image_gen calls outside IMAGE_GEN_CALL.
IMAGE_GEN_CALL must not execute without execution_controller approval.

## v0.6.2 Observable state extensions

The state_machine now includes:

- ENCODING_GUARD_CHECK before content graph
- RUNTIME_SIMULATION before IMAGE_GEN_CALL
- EXECUTION_TRACE_WRITE after scoring / decision

The system is now observable, simulation-driven, and execution-traceable.
