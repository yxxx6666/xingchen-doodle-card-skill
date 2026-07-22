# Series Progress Manifest Template v0.8.10

```json
{
  "series_id": "topic-slug-v1",
  "version": "v0.8.10",
  "validation_mode": "publish-3x4",
  "requested_ratio": "3:4",
  "selected_backend": "codex-$imagegen",
  "fixed_pixel_size_required": false,
  "total_pages": 3,
  "generation_order": ["P01", "P02", "P03"],
  "delivery_order": ["P01", "P02", "P03"],
  "first_incomplete_page_id": "P01",
  "resume_from_page_id": "P01",
  "updated_at": null,
  "pages": [
    {
      "page_id": "P01",
      "page_index": 1,
      "ordered_file_name": "01-cover-topic-slug.png",
      "status": "PLANNED",
      "service_dispatch_count": 0,
      "content_attempt_count": 0,
      "execution_window_id": null,
      "window_dispatch_count": 0,
      "attempt_id": null,
      "dispatch_started_at": null,
      "source_file": null,
      "requested_ratio": "3:4",
      "actual_width": null,
      "actual_height": null,
      "actual_ratio": null,
      "ratio_passed": null,
      "sha256": null,
      "last_error_type": null,
      "last_error": null
    }
  ]
}
```

Allowed statuses:

```text
PLANNED
WAITING_IMAGEGEN
SERVICE_TIMEOUT
PAUSED_TIMEOUT
GENERATED
RATIO_FAILED
RATIO_PASS
CONSISTENCY_PASS
CONTENT_FAILED
COMPLETE
```

Write the manifest atomically before every image dispatch and after every transition. Only a continuous prefix may be `COMPLETE`.
