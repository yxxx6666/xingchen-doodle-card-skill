# output_file_namer — v0.8.10 Filename Planner, Verifier and Finalizer

Purpose: plan stable names before generation, verify them after generation and enforce final folder/ZIP order.

## Phase A: plan

Run after `series_style_manifest` and before anchor selection / prompt composition.

Required input:

- `page_id`
- `page_index`
- `page_role`
- `recommended_total_pages`
- `topic_slug`

Output:

```json
{
  "output_file_naming_status": "PASS | FAIL",
  "recommended_total_pages": 4,
  "named_file_count": 4,
  "files": [
    {
      "page_id": "P01",
      "page_index": 1,
      "page_role": "cover",
      "ordered_file_name": "01-cover-topic-slug.png",
      "zip_order_key": "01"
    }
  ],
  "missing_page_ids": [],
  "duplicate_order_keys": [],
  "duplicate_file_names": []
}
```

## Default pattern

```text
{page_index:02d}-{page_role}-{topic_slug}.png
```

Examples:

```text
01-cover-blood-sugar-habits.png
02-content-blood-sugar-habits.png
03-content-blood-sugar-habits.png
04-action-blood-sugar-habits.png
```

## Planning rules

- Use continuous two-digit prefixes from `01`.
- `P01` maps to `01-cover-...`.
- Use lowercase ASCII letters, digits and hyphens for `topic_slug` when practical.
- Remove unsafe characters and collapse repeated hyphens.
- Never reuse a name within one series.
- `named_file_count = recommended_total_pages`.
- `prompt_composer` receives the exact planned name and may not change it.
- Anchor-first generation does not alter filenames or publication order.

## Phase B: verify

After every page passes ratio and consistency gates, verify:

- generated count equals planned count;
- every page maps to one planned name;
- prefixes are continuous with no gaps;
- no duplicate names, sources or order keys;
- retries preserve the same filename;
- final delivery follows `zip_order_key`, not generation time or upload order.

## Phase C: finalize

Create a manifest:

```json
{
  "files": [
    {
      "page_id": "P01",
      "source_file": "opaque-generated-name.png",
      "ordered_file_name": "01-cover-blood-sugar-habits.png"
    },
    {
      "page_id": "P02",
      "source_file": "another-generated-name.png",
      "ordered_file_name": "02-content-blood-sugar-habits.png"
    }
  ]
}
```

Run:

```bash
python scripts/finalize_series_files.py \
  --manifest OUTPUT_MANIFEST.json \
  --source-dir GENERATED_IMAGES \
  --output-dir FINAL_IMAGES \
  --zip FINAL_SERIES.zip
```

The finalizer changes filenames and archive member order only. It never edits pixels.

## Hard gates

```text
IF named_file_count != recommended_total_pages: FAIL
IF any prefix is missing or duplicated: FAIL
IF any page lacks ordered_file_name: FAIL
IF prompt_composer changes ordered_file_name: FAIL
IF generation order replaces publication order: FAIL
IF final folder or ZIP order differs from 01,02,03...: BLOCK delivery
```

If the environment cannot physically rename generated assets, preserve the exact planned names in the manifest and state that physical rename is unavailable. Never falsely claim a rename occurred.

generation order does not alter filenames or publication order.
