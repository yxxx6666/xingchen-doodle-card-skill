# timeout_recovery_controller — v0.8.10

Purpose: handle `$imagegen` timeouts without losing completed pages, waiting indefinitely, skipping pages, or confusing a transport failure with a content failure.

## What `request timed out` means

Treat it as a service/transport event: the current `$imagegen` call did not return an image before the tool or session deadline. It may be caused by service queueing, backend load, connection interruption, session reconnection, too many reference images, or an overloaded page prompt. Do not claim a more specific cause unless the runtime exposes one.

It is not automatically a content, ratio, permission, or local-computer failure.

## Required failure classes

### `SERVICE_TIMEOUT`

No image was returned.

- Do not increment `content_attempt_count`.
- Keep approved text, page index, filename, ratio mode and completed earlier pages unchanged.
- Never start the next page.
- Persist the timeout before issuing another request.

### `SESSION_INTERRUPTED`

The conversation or Codex session reconnects while a page is `WAITING_IMAGEGEN`, and the old tool request no longer has a live result handle.

- Do not say that the old request is still running.
- Recover the stale state to `SERVICE_TIMEOUT`.
- Resume from the same page with a new dispatch.
- Never regenerate completed earlier pages.

### `RETURNED_IMAGE_FAILURE`

An image returned but failed ratio, Chinese text, facts, structure or consistency.

- Increment `content_attempt_count`.
- Discard or quarantine the returned file.
- Regenerate the same page only.

## Bounded retry policy

```text
backend/tool request deadline: controlled by the active $imagegen tool (commonly about 240 seconds)
maximum immediate dispatches in one execution window: 2
maximum cumulative service dispatches per page: 4
maximum returned-image content attempts per page: 3
cooldown before the one immediate retry: 15–30 seconds
```

Do not poll every 10 seconds when `$imagegen` exposes no progress API. Dispatch once and wait for the tool result. After one timeout, allow at most one immediate retry in the same execution window. If the second request also times out, write `PAUSED_TIMEOUT`, save `resume_from_page_id`, and stop cleanly. A later user `继续` resumes the same page without touching completed pages.

## Complexity-safe retry

The first timeout does not justify changing approved content. For the retry:

- use exactly one approved earlier page as the visual reference, never multiple reference images;
- keep `verbatim_style_block`, approved Chinese text and filename unchanged;
- compile the compact retry prompt;
- remove duplicate explanations and decorative requests;
- preserve required icons/charts, but omit nonessential decoration;
- never merge, skip or reorder pages.

## Atomic checkpoint protocol

Before every `$imagegen` call:

```bash
python scripts/series_progress_controller.py begin   --manifest SERIES_PROGRESS.json   --page-id P03   --execution-window-id CURRENT_WINDOW
```

After a tool timeout:

```bash
python scripts/series_progress_controller.py timeout   --manifest SERIES_PROGRESS.json   --page-id P03   --error "request timed out"
```

At the beginning of every resumed session or after a reconnect:

```bash
python scripts/series_progress_controller.py recover   --manifest SERIES_PROGRESS.json   --force-after-reconnect
```

A checkpoint write must be atomic. Never keep the only progress state in conversational memory.
