# content_graph_builder — v0.6.0 Content Graph Builder

Purpose: convert user content into a compact content graph before visual prompting. This prevents raw long content from directly becoming overloaded scenes.

## Output format

```json
{
  "topic": "",
  "core_message": "",
  "content_type": "",
  "key_points": [],
  "visual_candidates": [],
  "must_visualize": [],
  "must_not_visualize": [],
  "recommended_layout": ""
}
```

## Rules

- key_points <= 5 whenever possible.
- If key_points > 5, split cards or group visually.
- must_visualize contains only what must become a visible scene object.
- must_not_visualize contains abstract concepts, extra props, secondary examples, and anything likely to overload the scene.
- recommended_layout must preserve the existing 3:4 doodle editorial card positioning.

## Content graph quality gate

A valid content_graph must have:

- one topic
- one core_message
- one content_type
- 0-5 key_points
- a clear recommended_layout

The content_graph is input to layout_graph_compiler.
