# Validation Rules v0.8.10

## Required active systems

- Codex `$imagegen` as the only formal image backend;
- evidence ledger, claim binding and content fidelity;
- automatic page planning and allocation;
- viewpoint visibility guard;
- immutable series style manifest;
- typography, icon and chart consistency;
- actual-file ratio and SHA-256 measurement;
- ordered filename planning, checkpointing and finalization.

## Per-page acceptance

- approved Chinese title/body and critical facts are accurate;
- `requested_ratio = 3:4`;
- `abs(width / height - 0.75) <= 0.001`;
- SHA-256 is recorded;
- structure and perspective are valid;
- typography, icon and chart grammar match the series;
- planned filename remains unchanged.

No exact width or height comparison is permitted.

## Series acceptance

- page count equals plan;
- generation and delivery order are `P01..Pn`;
- every page passes ratio and consistency gates;
- filenames are continuous `01,02,03...`;
- finalizer reopens every file and rechecks ratio and hash;
- ZIP member order follows numeric prefixes.

## Forbidden

- treating 3:4 as a fixed pixel size;
- asking for an API key;
- calling an external image API;
- accepting by visual guess without reading dimensions;
- padding, crop, resize, stretch, redraw or compositing;
- trusting old manifest pass flags without re-reading files.
