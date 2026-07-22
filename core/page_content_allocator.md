# page_content_allocator — v0.8.10 Page Content Allocator

Purpose: allocate evidence groups, claims, definitions, mechanisms, and action tips into the exact page_role_plan created by auto_page_planner.

This module prevents prompt_composer from deciding page count or merging pages after planning.

## Input requirements

- evidence_ledger
- content_graph
- auto_page_planner result
- page_role_plan

## Output format

```json
{
  "allocation_status": "PASS | WARNING | FAIL",
  "recommended_total_pages": 0,
  "allocated_page_count": 0,
  "page_allocations": [
    {
      "page_id": "P01",
      "page_role": "cover | content | mechanism | action | closing",
      "source_evidence_group_ids": [],
      "bound_claim_ids": [],
      "page_intent": "",
      "approved_text_draft": {
        "title": "",
        "subtitle": "",
        "points": []
      },
      "must_include": [],
      "must_avoid": [],
      "compression_risk": "low | medium | high"
    }
  ],
  "unallocated_claim_ids": [],
  "overloaded_pages": [],
  "underfilled_pages": [],
  "allocation_notes": ""
}
```

## Hard rules

- allocated_page_count must equal auto_page_planner.recommended_total_pages.
- page_allocations length must equal recommended_total_pages.
- Every non-decorative factual page text must bind to evidence_ledger claims.
- One content page should preferably carry one evidence group.
- If a page has too many claims, split earlier by returning FAIL / WARNING to auto_page_planner.
- Do not merge pages to make generation faster.
- Do not reduce page count for convenience.
- Do not allocate high-risk numeric claims to cover unless fully anchored and approved.

## Allocation pattern for long science/health content

Typical 6-page structure:

1. P01 cover — broad insight, no unsafe percentage merge.
2. P02 evidence group 1 — main meta-analysis or background study.
3. P03 evidence group 2 — wearable / sensor / second study.
4. P04 action tips — practical movement snacks.
5. P05 mechanism — cautious “可能” mechanism page.
6. P06 closing — action close and boundary reminder.

## Failure modes

```text
IF allocated_page_count != recommended_total_pages:
  FAIL

IF unallocated_claim_ids not empty and compression_risk = high:
  FAIL

IF prompt_composer attempts to merge allocated pages:
  BLOCK image_gen
```
