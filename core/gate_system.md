# gate_system — v0.6.1 Hard Gate System

The gate_system defines non-negotiable blocks before generation.

## Hard gates

```text
structure_score < 85 → BLOCK image_gen
structure_score < 70 → FORCE repair
structure_score < 50 → FORCE simplification
```

## Gate table

| Condition | Gate action | Next state |
|---|---|---|
| score >= 85 and SAFE | allow image_gen | IMAGE_GEN_CALL / OUTPUT |
| 70 <= score <= 84 | BLOCK image_gen, repair once | REPAIR |
| 50 <= score <= 69 | BLOCK image_gen, FORCE layout downgrade | DOWNGRADE |
| score < 50 | BLOCK image_gen, FORCE content simplification | DOWNGRADE |

## Image generation rule

`image_gen.text2im` is only allowed under SAFE state.

No fallback renderer is allowed. No local rendering system is allowed.

## v0.6.2 Production hard gates

```text
IF encoding_guard FAIL:
  BLOCK ALL

IF runtime_simulator FAIL:
  BLOCK image_gen

IF structure_score < 85:
  BLOCK image_gen
```

The gate_system must evaluate encoding safety before pipeline execution and runtime simulation before image generation.

`image_gen.text2im` is allowed only if ALL checks pass.
