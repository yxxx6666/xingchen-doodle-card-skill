# execution_controller — v0.8.10

The execution controller is the single authorization point for every formal image request.

## Pre-generation approval

Approve the current page only when all are true:

1. content, evidence, page allocation, claim binding and viewpoint checks passed;
2. immutable series style manifest exists;
3. filename and progress manifests passed;
4. current page is the first incomplete page and every earlier page is COMPLETE;
5. `scripts/runtime_preflight.py` confirmed version `v0.8.10`;
6. the selected backend matches the chosen mode: Codex `$imagegen` for publish-3x4, ;
7. requested ratio is `3:4`; no exact pixel size is required;
8. no padding, crop, resize, stretch, local text or compositing path is enabled.

## Returned-image handling

A returned image must be written as raw model/API output bytes and enter:

```text
actual dimension read
→ 3:4 ratio check
→ SHA-256 record
→ series consistency check
```

A wrong-size image is a content failure. Delete or quarantine it and regenerate the same page. Never repair it and never advance the page pointer.

## Final delivery approval

Approve only when every page is COMPLETE and finalization independently reopens every file and confirms:

- actual ratio 0.75 within tolerance;
- ratio 0.75 within tolerance;
- source SHA-256 matches the progress manifest when a hash is recorded;
- final copied file hash equals source hash;
- generation and delivery order equal `P01..Pn`;
- filenames are continuous from `01`.

## Hard blocks

```text
IF runtime version != v0.8.10: BLOCK
IF backend capability is inferred only from prompt text: BLOCK
IF actual dimensions != requested dimensions: BLOCK
IF any pixel post-processing is proposed: BLOCK
IF current page != first incomplete page: BLOCK
IF finalizer relies only on manifest pass flags: BLOCK
```
