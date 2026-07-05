# layout_prompt_mapping — v0.6.1 Layout → Prompt Mapping

layout_graph is not only a structure; it is a prompt selector.

## Required mapping

```text
title_scene_bullets → template_A
single_scene_editorial → template_B
list_scene_hybrid → template_C
title_object_ring → template_D
```

## Template roles

### template_A — title_scene_bullets

Use for one title, one simple scene, 3-5 bullets, one main character.

### template_B — single_scene_editorial

Use for one editorial illustration with large empty space and one main action.

### template_C — list_scene_hybrid

Use for list-like content where text is primary and props are secondary.

### template_D — title_object_ring

Use for abstract topics where a central title/object ring is safer than drawing many actions.

## Rules

- layout_type must choose exactly one template.
- layout_graph → controls prompt.
- prompt_composer must use selected template and must not invent a different layout.
- If layout_type is unknown, force template_A or downgrade to template_D.
