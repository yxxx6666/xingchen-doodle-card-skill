# content_graph_builder — v0.8.10 Content Graph Builder

Purpose: convert user content into a compact content graph before visual prompting. In v0.8.10, content_graph_builder must consume evidence_ledger, not only raw user text. This prevents raw long content from directly becoming overloaded scenes and prevents evidence lines from being merged into misleading card text.

## Output format

```json
{
  "topic": "",
  "core_message": "",
  "content_type": "",
  "content_domain": "",
  "factual_risk_level": "low | medium | high",
  "key_points": [],
  "evidence_anchors": [],
  "claim_intent": [],
  "visual_candidates": [],
  "must_visualize": [],
  "must_not_visualize": [],
  "prohibited_merges": [],
  "recommended_layout": ""
}
```

## Rules

- content_graph_builder must consume evidence_ledger, not only raw user text.
- key_points <= 5 whenever possible.
- key_points must preserve claim boundaries.
- If a key point contains a number, it must include evidence_anchors.
- If a key point is qualitative, it may be anchor-free only when it does not imply a numerical result.
- Do not make visual page points by merging unrelated claim_ids.
- If key_points > 5, split cards or group visually.
- must_visualize contains only what must become a visible scene object.
- must_not_visualize should include abstract or unsupported concepts.
- must_not_visualize contains abstract concepts, extra props, secondary examples, and anything likely to overload the scene.
- prohibited_merges must be copied from evidence_ledger when relevant.
- If source contains multiple studies, each study should usually become a separate page or separate bullet group.
- recommended_layout must preserve the existing 3:4 doodle editorial card positioning.

## Content graph quality gate

A valid content_graph must have:

- one topic
- one core_message
- one content_type
- content_domain
- factual_risk_level
- 0-5 key_points
- evidence_anchors for every numerical point
- prohibited_merges when source has multiple evidence lines
- a clear recommended_layout

The content_graph is input to layout_graph_compiler.

## Fidelity principle

```text
facts before hooks
claim boundaries before page titles
evidence groups before visual composition
```
