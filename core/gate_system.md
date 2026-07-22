# gate_system — v0.8.10

## Pre-generation gate order

```text
encoding
→ evidence
→ page planning
→ page allocation
→ claim binding
→ content fidelity
→ viewpoint visibility
→ filename planning
→ series style freeze
→ runtime version/backend preflight
→ explicit size plan
→ prompt composition
→ native image backend authorization
```

## Hard blocks

```text
IF skill_version != v0.8.10: BLOCK
IF current_page != first_incomplete_page: BLOCK
IF any padding/crop/resize/compositing path is enabled: BLOCK
IF content/viewpoint/filename/style checks fail: BLOCK
```

## Post-generation gates

```text
IF publish mode ratio != 0.75, or strict mode exact dimensions fail: DISCARD AND REGENERATE SAME PAGE
IF ratio != 0.75 ± 0.001: DISCARD AND REGENERATE SAME PAGE
IF Chinese text/facts/structure/style fail: REGENERATE SAME PAGE
IF SHA-256 missing: BLOCK page completion
IF final independent revalidation fails: BLOCK package
IF numeric filenames are discontinuous: BLOCK package
```
