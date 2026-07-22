# sequential_generation_controller — v0.8.10

Purpose: enforce one visible, recoverable generation order for every multi-page series.

## Non-negotiable order

```text
generation_order = delivery_order = P01, P02, P03, ... Pn
```

- Generate `P01` cover first.
- Do not generate `Pn+1` until `Pn` is `COMPLETE` in the persisted manifest.
- Do not generate pages in parallel.
- Do not skip a timed-out, failed or missing page.
- A style-anchor candidate never changes generation order.

## Session-start rule

Before any generation or retry:

1. load `SERIES_PROGRESS.json` from disk;
2. run `series_progress_controller.py recover`;
3. compute `first_incomplete_page_id`;
4. authorize only that page;
5. keep all earlier `COMPLETE` pages unchanged.

Conversational statements such as “继续等待” are not execution state. If a reconnect lost the live request, mark it interrupted and issue a fresh request for the same page.

## Page authorization

Authorize the current page only when:

```text
current_page_index = first_incomplete_page_index
all earlier pages = COMPLETE
all later pages = PLANNED
ordered filename matches current page index
status is PLANNED, SERVICE_TIMEOUT, PAUSED_TIMEOUT, RATIO_FAILED, or CONTENT_FAILED
```

## Hard gates

```text
IF generation_order != delivery_order: BLOCK
IF first generated page != P01: BLOCK
IF any later page starts before all earlier pages are COMPLETE: BLOCK
IF parallel generation is attempted: BLOCK
IF a timeout causes the controller to skip forward: BLOCK
IF a reconnect causes completed pages to regenerate: BLOCK
```
