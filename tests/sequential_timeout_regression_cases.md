# Sequential and Timeout Regression Cases v0.8.10

## Case 1 — P03 timeout does not damage earlier pages

P01 and P02 are COMPLETE. P03 times out.

Expected: P01/P02 remain unchanged; P03 becomes SERVICE_TIMEOUT; P04 remains PLANNED.

## Case 2 — bounded immediate retry

First P03 request times out. One immediate retry is allowed. If the second request also times out in the same execution window, P03 becomes PAUSED_TIMEOUT and the run stops with `resume_from_page_id=P03`.

## Case 3 — timeout does not consume content attempts

After two service timeouts:

```text
service_dispatch_count = 2
content_attempt_count = 0
```

## Case 4 — reconnect recovery

P03 is WAITING_IMAGEGEN when the Codex session reconnects and the live tool handle is lost.

Expected: recover to SERVICE_TIMEOUT with `last_error_type=SESSION_INTERRUPTED`; issue a fresh P03 request; do not claim the old request is still running.

## Case 5 — one reference image only

A retry request must attach no more than one approved earlier image. The textual style manifest carries all remaining consistency constraints.

## Case 6 — returned image failure

An image returns but ratio or text is wrong. Increment content attempts and retry only the same page. Service attempts and content attempts remain separate.
