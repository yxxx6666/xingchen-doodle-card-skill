# auto_page_planner — v0.8.10 Automatic Page Count Planner

Purpose: decide the correct total page count and page roles before page text is allocated. It prevents the model from treating “封面页加内容页” as exactly two pages.

## Core principle

“封面页加内容页” = 页面角色结构
不是固定2页。

- P01 = cover
- P02...Pn = content pages
- 内容页数量由 auto_page_planner 自动决定

Only explicit count instructions can override automatic planning.

## Explicit page count phrases

Only the following count as explicit page count instructions:

- 共2页
- 做2页
- 生成6页
- 一共6张
- 第1页到第6页
- 只要2页
- 只做封面和一页内容
- 只做2页极简版

If the user only says:

- 封面页加内容页
- 封面+内容页
- cover page + content pages
- 封面页和内容页

then do not interpret it as 2 pages.

不得理解为2页。

## Output format

```json
{
  "auto_page_count_status": "PASS | WARNING | FAIL",
  "user_page_count_intent": {
    "explicit_total_pages": null,
    "explicit_content_pages": null,
    "has_explicit_page_count": false,
    "raw_page_instruction": "",
    "interpretation": ""
  },
  "source_length_estimate": {
    "chinese_chars": 0,
    "paragraph_count": 0
  },
  "content_density": "low | medium | high | very_high",
  "content_domain": "",
  "factual_risk_level": "low | medium | high",
  "evidence_group_count": 0,
  "claim_count": 0,
  "numeric_claim_count": 0,
  "percentage_claim_count": 0,
  "action_tip_count": 0,
  "definition_count": 0,
  "mechanism_claim_count": 0,
  "study_group_count": 0,
  "has_definition": false,
  "has_background": false,
  "has_multiple_studies": false,
  "has_mechanism": false,
  "has_action_close": false,
  "recommended_total_pages": 0,
  "recommended_content_pages": 0,
  "min_total_pages": 0,
  "max_total_pages": 0,
  "page_role_plan": [],
  "compression_risk": "low | medium | high",
  "split_required": false,
  "split_reason": "",
  "under_page_count_risk": false,
  "over_page_count_risk": false,
  "final_decision_reason": ""
}
```

## Stable planning heuristics

- Low density short input: usually 2–3 pages if not explicitly constrained.
- Medium density input: usually 3–4 pages.
- High density factual content: usually 5–6 pages.
- Very high density long science/health content with multiple studies, multiple numbers, mechanisms, and action tips: usually 6–8 pages or more.
- If has_multiple_studies = true, each major study group should usually get a separate content page.
- If numeric_claim_count >= 4 or percentage_claim_count >= 2, split_required = true.
- If study_group_count >= 2, split_required = true.
- If mechanism_claim_count > 0, reserve one mechanism page when content density allows.
- If action_tip_count > 0 or has_action_close = true, reserve one action or closing page.
- Cover page should not carry dense evidence; it should carry a broad source-supported insight.

## Page role plan rules

page_role_plan must contain exactly recommended_total_pages items:

```json
[
  {"page_id":"P01","page_role":"cover","evidence_group_ids":[],"page_purpose":"broad hook"},
  {"page_id":"P02","page_role":"content","evidence_group_ids":["EG001"],"page_purpose":"evidence group 1"}
]
```

Rules:

- P01 is always cover.
- P02...Pn are content pages, summary pages, mechanism pages, action pages, or closing pages.
- recommended_content_pages = recommended_total_pages - 1.
- page_role_plan length must equal recommended_total_pages.
- Do not let prompt_composer change recommended_total_pages.
- If explicit_total_pages is present but compression_risk is high, status = WARNING and explain under_page_count_risk.

## Failure modes

```text
IF recommended_total_pages < 2:
  FAIL

IF “封面页加内容页” interpreted as exactly 2 pages without explicit count:
  FAIL

IF high density / multiple studies / multiple numbers compressed into 2 pages:
  FAIL

IF page_role_plan length != recommended_total_pages:
  FAIL
```
