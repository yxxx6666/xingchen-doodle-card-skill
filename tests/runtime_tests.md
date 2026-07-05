# Runtime Tests — v0.6.2

These tests validate the production-grade deterministic AI pipeline.

| Test | Expected behavior |
|---|---|
| encoding failure case | encoding_guard FAIL → BLOCK ALL → BLOCK installation → REQUIRE repair |
| simulation failure case | runtime_simulator FAIL → BLOCK image_gen → FORCE repair loop |
| layout overload case | simulated_score < 85 → DO NOT CALL image_gen → reduce props / split layout |
| multi-hand risk case | predicted_issues includes multi-hand risk → BLOCK image_gen → anatomy repair |
| scoring instability case | large scorer delta → repair_policy_matrix uses simulation result + execution trace + scorer delta |

## Required assertions

- image_gen_called must be false for failed simulation.
- final_state must be SAFE or FAIL.
- execution_trace must record scorer_before and scorer_after.
- max_attempts remains 3.
