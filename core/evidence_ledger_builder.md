# evidence_ledger_builder — v0.8.10 Evidence Ledger Builder

Purpose:
Extract an evidence ledger from the raw user source before any visual page planning. The ledger prevents high-impact numbers, study claims, time units, populations, comparison groups, and qualifiers from being detached from their original source anchors.

This module is part of the Content Fidelity Layer. It is a source-to-card fidelity module, not an external fact-checker.

## Output format

```json
{
  "source_summary": "",
  "content_domain": "health | science | finance | legal | education | lifestyle | general",
  "factual_risk_level": "low | medium | high",
  "claim_inventory": [
    {
      "claim_id": "C001",
      "source_text": "",
      "claim_type": "numeric | correlational | causal | mechanism | recommendation | action_tip | definition | opinion",
      "number": "",
      "unit": "",
      "time_window": "",
      "population": "",
      "comparison_group": "",
      "outcome": "",
      "study_or_context": "",
      "study_type": "",
      "qualifier": "",
      "certainty": "high | medium | low",
      "allowed_wording": [],
      "forbidden_wording": [],
      "can_appear_on_cover": false,
      "notes": ""
    }
  ],
  "headline_claims": [],
  "body_supported_claims": [],
  "headline_body_tension": [],
  "evidence_conflicts": [],
  "prohibited_merges": []
}
```

## Source anchor rules

- Every number must have a source anchor.
- A source anchor includes: number, unit, time window, population, comparison group, outcome, and source sentence.
- Do not extract a percentage without its outcome.
- Do not extract a time expression without its time window.
- Do not extract a recommendation without its target population.
- Headline claims are low-trust unless they are supported by body evidence.
- If the headline combines two evidence lines but the body separates them, keep the body evidence separated.
- If the body evidence is vague, mark certainty as medium or low.
- If a number cannot be safely anchored, downgrade it to qualitative wording or omit it.
- The ledger must preserve source wording, but it must not allow misleading recombination.
- For health/science content, observational evidence must use cautious wording such as “相关”“可能”“研究发现”“与……更低相关”.
- Do not turn association into direct causation unless the source explicitly supports causal language.
- Do not silently correct the user’s source with external facts. This Skill checks source-to-card fidelity, not external truth, unless the user explicitly asks for verification.

## Claim inventory extraction protocol

1. Identify content_domain first. Health, science, finance, legal, medical, risk, investment, safety, or disease content is high-stakes by default.
2. Split the source into independent evidence lines.
3. Assign one claim_id to each independent claim.
4. Bind every percentage, sample size, year, duration, frequency, or comparison result to its source_text.
5. Record whether the claim is numeric, correlational, causal, mechanism, recommendation, action_tip, definition, or opinion.
6. Record qualifier exactly when the source uses terms like “可能”, “相关”, “研究发现”, “研究人员认为”, “与……相关”, “约”, “平均”, “随访”.
7. Put weak headline-only claims into headline_claims and body-supported claims into body_supported_claims.
8. Put any headline/body mismatch into headline_body_tension.
9. Put dangerous combinations into prohibited_merges.

## prohibited_merges rules

Examples of prohibited merges:

- Do not merge a weekly exercise claim with a daily short-burst activity claim unless the same source sentence supports both.
- Do not attach a percentage from one study to the time window from another study.
- Do not attach a risk-reduction number to a different disease outcome.
- Do not attach a study result from one population to another population.
- Do not merge “few minutes” with “31%” only because both are catchy.
- Do not merge self-reported exercise studies with wearable-device studies unless the page explicitly distinguishes them.
- Do not merge “WHO recommendation” with “daily 3–4 minutes” unless the source says so.

## Health/science default wording

Allowed wording examples:

- “研究发现”
- “与……相关”
- “可能”
- “风险更低相关”
- “相关下降”
- “在该研究中”
- “与完全不运动相比”

Forbidden wording examples unless the source explicitly supports causality:

- “一定”
- “保证”
- “直接导致”
- “治愈”
- “预防所有风险”
- “只要……就能……”

## Failure behavior

If a claim cannot be anchored safely:

```text
DO NOT use the number.
SOFTEN the sentence.
OMIT the percentage if needed.
PRESERVE the evidence group boundary.
```
