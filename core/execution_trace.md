# execution_trace — v0.8.10 Stable Execution Trace

Purpose: record the complete execution chain and make the system observable, verifiable, and traceable.

## Required trace output

Every generation must output trace:

```json
{
  "input": "...",
  "encoding_guard_status": "PASS | FAIL",
  "evidence_ledger_version": "v0.8.10",
  "claim_inventory_count": 0,
  "content_graph": "...",
  "auto_page_planner_result": {},
  "recommended_total_pages": 0,
  "page_role_plan": [],
  "page_content_allocator_result": {},
  "allocated_page_count": 0,
  "page_claim_bindings": [],
  "content_fidelity_status": "PASS | WARNING | FAIL",
  "content_fidelity_warnings": [],
  "content_fidelity_failed_checks": [],
  "layout_graph": "...",
  "viewpoint_visibility_guard_result": {},
  "prop_visibility_plan": [],
  "visibility_conflicts": [],
  "readability_misuse_detected": false,
  "runtime_simulator_result": "...",
  "prompt_version": "v0.8.10",
  "prompt_count": 0,
  "output_file_namer_result": {},
  "ordered_file_names": [],
  "scorer_before": 0,
  "scorer_after": 0,
  "repair_triggered": false,
  "downgrade_triggered": false,
  "native_image_backend_called": false,
  "final_state": "SAFE | FAIL"
}
```

## Required pipeline steps

The trace must contain all pipeline steps:

1. input parse
2. encoding_guard check
3. evidence_ledger build
4. claim_inventory_count
5. content_graph build from evidence_ledger
6. auto_page_planner result
7. recommended_total_pages
8. page_role_plan
9. page_content_allocator result
10. allocated_page_count
11. page_claim_bindings
12. claim_binding_validator result
13. content_fidelity_guard result
14. layout_graph build
15. viewpoint_visibility_guard result
16. prop_visibility_plan
17. runtime_simulator result
18. execution_controller decision
19. prompt_composer version
20. prompt_count
21. image_gen call state
22. output_file_namer result
23. ordered_file_names
24. structure_scorer before / after
25. repair loop decision
26. downgrade decision
27. final_state

## Reproducible chain

```text
source text → evidence ledger → content graph → auto_page_planner → page_content_allocator → page text → page_claim_bindings → content_fidelity_guard result → layout graph → viewpoint_visibility_guard → prop_visibility_plan → prompt count → selected image mode/backend → aspect_ratio_gate → output_file_namer → ordered_file_names → final delivery
```

The trace must show whether evidence_ledger_builder, auto_page_planner, page_content_allocator, claim_binding_validator, content_fidelity_guard, and output_file_namer passed.

### v0.8.10 prop role trace

The trace must preserve the exact prop role for every text-bearing prop: `self_reading`, `viewer_presentation`, or `background_prop`. This makes private reading, public presentation, and decorative background usage auditable.


## v0.8.10 ratio and timeout trace fields

- `requested_ratio`
- `actual_width`
- `actual_height`
- `actual_ratio`
- `ratio_passed`
- `attempt_id`
- `execution_window_id`
- `service_dispatch_count`
- `window_dispatch_count`
- `content_attempt_count`
- `dispatch_started_at`
- `last_error_type`
- `resume_from_page_id`
- `sha256`

## v0.8.10 native image trace fields

Record `skill_version`, `validation_mode`, `backend`, `requested_ratio`, `request_id`, `actual_width`, `actual_height`, `actual_ratio`, `ratio_passed`, `sha256`, `service_attempt` and `content_attempt`.
