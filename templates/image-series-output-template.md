# Image Series Output Template v0.8.10

## Planning manifest

```text
01-cover-{topic-slug}.png — P01 — cover
02-content-{topic-slug}.png — P02 — content
03-content-{topic-slug}.png — P03 — content
04-action-{topic-slug}.png — P04 — action
```

Create the complete filename manifest and progress manifest before generating any page.

```text
generation_order = delivery_order = P01,P02,P03,P04
```

The representative anchor candidate never changes this order.

## Progress rule

After each page passes, write it as `COMPLETE` before starting the next page. On timeout, keep the current page incomplete and set `resume_from_page_id` to that page.

## Finalization manifest

```json
{
  "files": [
    {
      "page_id": "P01",
      "source_file": "generated-opaque-a.png",
      "ordered_file_name": "01-cover-topic-slug.png"
    },
    {
      "page_id": "P02",
      "source_file": "generated-opaque-b.png",
      "ordered_file_name": "02-content-topic-slug.png"
    }
  ]
}
```

Run `scripts/finalize_series_files.py` after all ratio and consistency gates pass. Deliver files and ZIP members in numeric order.
