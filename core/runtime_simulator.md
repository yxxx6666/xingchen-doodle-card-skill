# runtime_simulator — v0.8.10

Purpose: predict failures before any real image-model call.

## Simulation flow

```text
evidence_ledger
→ content_graph
→ auto_page_planner
→ page_content_allocator
→ claim_binding_validator
→ content_fidelity_guard
→ viewpoint_visibility_guard
→ output_file_namer.plan
→ layout_graph_compiler
→ prompt_composer simulation
→ structure and risk prediction
```

## Required predictions

- missing or unbound evidence;
- causal overclaim or misleading cover claim;
- insufficient or excessive page count;
- prompt count mismatch;
- missing, duplicated or discontinuous filenames;
- self-reading props with readable viewer-facing text;
- anatomy, occlusion and overloaded-scene risk;
- critical Chinese text density risk;
- unsupported aspect-ratio parameter claims.

## Output

```json
{
  "simulated_score": 0,
  "risk_prediction": "SAFE | WARNING | FAIL",
  "content_risk_prediction": "SAFE | WARNING | FAIL",
  "page_count_risk_prediction": "SAFE | WARNING | FAIL",
  "filename_risk_prediction": "SAFE | WARNING | FAIL",
  "viewpoint_risk_prediction": "SAFE | WARNING | FAIL",
  "ratio_capability_risk_prediction": "SAFE | WARNING | FAIL",
  "predicted_issues": [],
  "should_execute": false
}
```

## Hard rules

```text
IF simulated_score < 85: BLOCK image_gen
IF content_risk_prediction = FAIL: BLOCK image_gen
IF page_count_risk_prediction = FAIL: RE-RUN auto_page_planner
IF filename_risk_prediction = FAIL: RE-RUN output_file_namer.plan
IF viewpoint_risk_prediction = FAIL: REPAIR prop_visibility_plan
IF ratio_capability_risk_prediction = FAIL: REMOVE unsupported tool arguments
```

Simulation does not call an image model and does not pretend that a generated image was validated.

## v0.8.10 backend simulation

Simulation must verify version, backend capability source, explicit requested size and absence of pixel post-processing before dispatch. It cannot treat prompt text or a static test schema as backend proof.
