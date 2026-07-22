# generation_loop — v0.8.10

## Canonical state flow

```text
STATE 1: parse input and validate encoding
STATE 2: build evidence ledger and content graph
STATE 3: plan pages and allocate content
STATE 4: validate claims, fidelity and viewpoint
STATE 5: freeze typography/icon/chart manifest
STATE 6: plan ordered filenames and progress manifest
STATE 7: run version/backend preflight
STATE 8: authorize first incomplete page
STATE 9: compile current-page prompt
STATE 10: request current page with `$imagegen` in the selected ratio mode
STATE 11: read actual dimensions and SHA-256
STATE 12: reject or pass the selected native ratio gate
STATE 13: run series consistency gate
STATE 14: checkpoint current page as COMPLETE
STATE 15: repeat for next numeric page
STATE 16: independently revalidate every source file
STATE 17: copy/rename and ZIP in numeric order
```

## Canonical pipeline

```text
input
→ encoding_guard
→ evidence_ledger_builder
→ content_graph_builder
→ auto_page_planner
→ page_content_allocator
→ claim_binding_validator
→ content_fidelity_guard
→ viewpoint_visibility_guard
→ series_style_manifest
→ output_file_namer.plan
→ series_anchor_selector.plan
→ backend_preflight
→ sequential_generation_controller
→ prompt_composer(current page)
→ native_image_generation(current page, publish-3x4 by default)
→ native_aspect_ratio_gate
→ series_consistency_gate
→ progress_checkpoint
→ repeat next numeric page
→ output_file_namer.verify
→ final_native_revalidation
→ finalize_series_files
```

No page may be repaired into 3:4. Wrong-size output is discarded and the same page is regenerated.
