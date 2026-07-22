# claim_binding_validator — v0.8.10 Claim Binding Validator

Purpose:
Validate that every generated page text is bound to one or more approved evidence ledger claims, and that no page text creates a new claim by mixing unsupported fragments.

This module runs after content_graph_builder and before content_fidelity_guard. It validates page text before prompt_composer receives it.

## Output format

```json
{
  "page_claim_bindings": [
    {
      "page_id": "P01",
      "page_role": "cover | content | summary | action",
      "page_title": "",
      "page_subtitle": "",
      "page_points": [],
      "bound_claim_ids": [],
      "unbound_numbers": [],
      "unbound_time_units": [],
      "unbound_outcomes": [],
      "mixed_claim_risk": "none | low | medium | high",
      "requires_rewrite": false,
      "rewrite_reason": "",
      "approved_text": {
        "title": "",
        "subtitle": "",
        "points": []
      }
    }
  ],
  "overall_claim_binding_status": "PASS | WARNING | FAIL"
}
```

## Hard rules

- Every number on a page must map to exactly one claim_id.
- A page may combine multiple claims only if their differences are visible to the reader.
- If two claims have different study type, population, time window, or outcome, they must not be collapsed into one sentence.
- Cover pages should avoid precise percentages unless the percentage is the central source-supported claim and all anchors are preserved.
- If the cover uses a catchy qualitative hook, it should not attach an unanchored percentage.
- If the source title itself contains a catchy but weakly supported combination, the validator must prefer body-supported evidence.
- If a page title says “降低风险”, but evidence type is correlational or observational, rewrite to “相关下降”“风险更低相关”“可能降低” or a similarly cautious phrase.
- If a claim lacks comparison group, do not write it as a guaranteed effect.
- If a claim lacks time unit, do not invent daily/weekly/monthly wording.
- If a claim lacks population, do not imply “所有人都适用”.

## Binding checks

For each page:

1. Extract all numbers, percentages, durations, frequencies, sample sizes, and disease outcomes.
2. Check whether each item maps to exactly one claim_id.
3. Check whether time_window, population, comparison_group, outcome, and qualifier remain visible when required.
4. Check whether multiple claim_ids are merged into one catchy sentence.
5. If page text changed during repair or downgrade, re-run this validator.
6. Write only approved_text forward to content_fidelity_guard.

## Failure examples

FAIL:

> “每周运动几分钟，死亡风险降低31%”

If “每周几分钟” and “31%” come from different evidence lines or the body does not support them in one source anchor, this fails.

PASS:

> “每天几分钟运动零食，也可能有收益”

> “66万人研究：较不运动者，运动人群死亡风险更低”

> “可穿戴设备研究：每天短促高强度活动，与风险更低相关”

## Status behavior

```text
PASS = all page numbers and claims are bound.
WARNING = text is mostly safe but should be softened.
FAIL = unbound number, cross-study merge, invented time window, invented population, or causal overclaim.
```

If overall_claim_binding_status is FAIL:

```text
BLOCK image_gen
REWRITE page text
RE-RUN claim_binding_validator
RE-RUN content_fidelity_guard
```
