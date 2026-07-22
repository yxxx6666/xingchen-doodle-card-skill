# Page Series Workflow v0.8.10

```text
plan all pages and names
→ persist progress manifest
→ recover stale request state
→ begin P01 checkpoint
→ call $imagegen once
→ validate returned result or record timeout
→ complete P01
→ continue P02, P03 ... in numeric order
→ final revalidation and ordered packaging
```

Rules:

- P01 must be the first image request.
- Before each request, atomically persist `WAITING_IMAGEGEN` with an attempt ID.
- Attach at most one reference image.
- On first timeout, persist it and retry the same page once using the compact timeout prompt.
- On a second timeout in the same execution window, persist `PAUSED_TIMEOUT` and stop cleanly.
- On user `继续`, reload the manifest and resume from `resume_from_page_id`.
- After session reconnection, do not continue waiting on a lost request; recover and re-dispatch the same page.
- Never regenerate completed earlier pages or skip to a later page.
