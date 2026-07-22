# state_machine — v0.8.10

```text
PARSE
→ BUILD_EVIDENCE
→ BUILD_CONTENT_GRAPH
→ PLAN_PAGES
→ ALLOCATE_CONTENT
→ VALIDATE_CLAIMS
→ VALIDATE_FIDELITY
→ VALIDATE_VIEWPOINT
→ FREEZE_SERIES_STYLE
→ PLAN_FILENAMES
→ INIT_PROGRESS_MANIFEST
→ PREFLIGHT_VERSION_AND_BACKEND
→ AUTHORIZE_FIRST_INCOMPLETE_PAGE
→ BUILD_LAYOUT
→ COMPOSE_CURRENT_PROMPT
→ REQUEST_IMAGE_IN_SELECTED_MODE
→ HANDLE_SERVICE_RESULT
→ READ_DIMENSIONS_AND_HASH
→ VERIFY_SELECTED_RATIO_MODE
→ VERIFY_SERIES_CONSISTENCY
→ CHECKPOINT_COMPLETE
→ NEXT_NUMERIC_PAGE_OR_FINALIZE
→ FINAL_INDEPENDENT_REVALIDATION
→ ORDERED_COPY_AND_ZIP
```

A transition to image generation is illegal unless the current page is the first incomplete page and the backend matches the selected mode. Publish mode uses Codex `$imagegen`; strict mode requires an explicit exact-size path.

A returned image that fails the selected mode transitions to `RATIO_FAILED` in publish mode or `STRICT_SIZE_FAILED` in strict mode, deletes/quarantines that result and returns to the same page. It never transitions to a repair operation or the next page.

A transition to final delivery is illegal unless every file is independently reopened and passes dimensions, ratio and hash checks.
