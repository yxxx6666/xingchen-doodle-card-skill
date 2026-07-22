# layout_graph_compiler — v0.6.0 Layout Graph Compiler

Purpose: compile content_graph into a safe visual structure graph before final prompt composition.

## Input

- content_graph
- anatomy_guard
- scene_limiter
- pose_safety

## Output structure

```json
{
  "layout_type": "...",
  "focal_point": "single_main_character",
  "text_structure": {
    "title": "",
    "subtitle": "",
    "bullets": []
  },
  "scene_structure": {
    "main_scene": "",
    "character": "",
    "action": "",
    "props": []
  },
  "composition": {
    "empty_space": "",
    "balance": ""
  }
}
```

## Compiler rules

- layout_graph must have exactly 1 focal_point.
- focal_point must default to `single_main_character`.
- scene_structure.main_scene must be one scene only.
- scene_structure.character must be one main character only.
- scene_structure.action must be one simple main action only.
- props <= 10.
- interaction props <= 2.
- bullets <= 5.
- extra content becomes text bullet or background mark, not another action.

## Why layout graph is core

The layout_graph is the bridge between content and image prompt. It prevents the model from turning every idea into a drawn object, which is a major cause of extra hands, extra feet, and broken anatomy.

## v0.6.1 Controller Role Upgrade

layout_graph = prompt structure controller.

The layout_graph must output and control:

- focal_point（唯一）
- text_structure
- scene_structure
- composition
- props ≤ 10
- interaction props ≤ 2
- layout_type for layout_prompt_mapping

The layout_graph selects the prompt structure through `layout_prompt_mapping.md`.
The prompt_composer must follow the layout_graph and selected template.

## v0.8.10 Viewpoint Visibility Integration

`layout_graph_compiler` must call `viewpoint_visibility_guard` after scene_structure.props are known and before prompt_composer.

The layout graph must include:

```json
{
  "prop_inventory": [],
  "character_gaze_direction": "toward_prop | toward_viewer | down | side | unclear",
  "viewer_camera_angle": "front | side | three_quarter | over_shoulder | top_down | unclear",
  "prop_visibility_plan": [],
  "viewpoint_visibility_status": "PASS | WARNING | FAIL"
}
```

Compiler rules:

- Every paper, phone, tablet, book, notebook, screen, sign, card, manual, or text-bearing prop must receive a prop_role.
- If the character is reading the prop and the prop faces the character, classify it as `self_reading`.
- If a prop is explicitly shown to the viewer, classify it as `viewer_presentation`.
- Decorative context props become `background_prop`.
- Self-reading props must not be assigned clear_readable full body text.
- Required page information must stay in `approved_page_text` unless the prop is viewer_presentation.

If `viewpoint_visibility_status = FAIL`, the layout graph is not safe for prompt composition and must be repaired.
