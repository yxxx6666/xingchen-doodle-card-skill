# generation_loop — v0.6.2 Simulation-first Pipeline

v0.6.2 upgrades generation_loop into a simulation-first pipeline for a production-grade deterministic AI pipeline.

## New state flow

```text
STATE 1: input parse
STATE 2: encoding guard check
STATE 3: content graph build
STATE 4: layout graph build
STATE 5: runtime simulation
STATE 6: execution controller decision
STATE 7: prompt compose
STATE 8: image_gen call (if allowed)
STATE 9: structure scoring
STATE 10:
IF SAFE → output
IF WARNING → repair once
IF FAIL → downgrade + regenerate
STATE 11: execution trace write
STATE 12: loop max 3
```

## Pre-execution validation stage

Before any real image generation:

1. encoding_guard must pass.
2. runtime_simulator must pass.
3. simulated_score must be >= 85.
4. execution_controller must approve.
5. gate_system must not block image_gen.

## Runtime simulation branch

```text
IF runtime_simulator FAIL:
  BLOCK image_gen
  execution_trace.image_gen_called = false
  ENTER repair loop
```

## Encoding branch

```text
IF encoding_guard FAIL:
  STOP SYSTEM
  BLOCK ALL
```

## Loop rule

```text
max_attempts = 3
```

No fallback renderer is allowed during any attempt. The legal path remains `image_gen.text2im` only.
