# viewpoint_visibility_guard — v0.8.10 Viewpoint Visibility Guard

Purpose:
Ensure that readable text on props follows real-world viewpoint logic. If a character is reading an object oriented toward themselves, the viewer must not be able to clearly read the object’s front-facing text from an implausible angle.

## 核心目的

- 保证“文字道具”的可见性符合真实视角逻辑。
- 防止“角色自己在看，但观众却替他看清”的错误。
- 区分道具是否是：
  1. self-reading prop
  2. viewer-facing presentation prop
  3. background prop
- 决定该道具上的文字应该：
  - clear readable
  - partially visible
  - symbolic only
  - illegible
  - blank / near blank

## 适用对象

- 纸张
- 文件
- 报纸
- 便签
- 书本
- 笔记本
- 手机
- 平板
- 电脑屏幕
- 手册
- 卡片
- 宣传页
- 板子
- 任何带文字的手持/桌面道具

## 输入

- page visual intent
- layout graph
- prop inventory
- character pose
- character gaze direction
- prop orientation
- viewer camera angle
- whether prop is informational or decorative
- whether readable text is required for user comprehension

## 输出格式

```json
{
  "viewpoint_visibility_status": "PASS | WARNING | FAIL",
  "prop_visibility_plan": [
    {
      "prop_id": "",
      "prop_type": "paper | phone | tablet | book | notebook | screen | sign | other",
      "prop_role": "self_reading | viewer_presentation | background_prop",
      "held_by_character": true,
      "character_is_reading": true,
      "viewer_facing": false,
      "camera_relation": "front | side | three_quarter | over_shoulder | top_down | unclear",
      "text_visibility": "clear_readable | partial | symbolic_only | illegible | blank",
      "allowed_text_density": "none | minimal | low | medium | high",
      "must_not_show_full_body_text": true,
      "recommended_handling": "",
      "reason": ""
    }
  ],
  "visibility_conflicts": [],
  "readability_misuse_detected": false,
  "requires_prompt_constraint": false,
  "final_decision_reason": ""
}
```

## Prop role definitions

### 1. self_reading

A character is reading or looking at the object, and the readable surface is oriented toward the character.

Rules:

- `viewer_facing` must be false unless the composition is explicitly over-the-shoulder with only partial view.
- `text_visibility` must be `partial`, `symbolic_only`, `illegible`, or `blank`.
- `allowed_text_density` must be `none`, `minimal`, or `low`.
- `must_not_show_full_body_text` must be true.
- The card’s real message must be placed in the independent title/subtitle/bullet text area, not on the self-reading prop.

Allowed visual treatment:

- blank / near blank paper
- short symbolic strokes
- tiny unreadable lines
- partial angled marks
- screen glow with no readable paragraphs
- book pages with texture-like line marks only

Forbidden:

- complete front-facing paragraphs visible to viewer
- full phone / tablet screen content readable from side view
- book or notebook text perfectly aligned to viewer while the character is looking down
- using self-reading prop as the main text area

### 2. viewer_presentation

The character intentionally presents a paper, card, sign, phone, tablet, or board to the viewer.

Rules:

- `viewer_facing` must be true.
- Character gaze/action must support presentation, not private reading.
- `text_visibility` may be `clear_readable`.
- `allowed_text_density` may be `medium` or `high` only if the object is large enough and front-facing.
- The prop can contain selected approved_page_text, but still must not add new claims.

Required prompt wording:

- “the character presents the prop toward the viewer”
- “front-facing display surface”
- “readable text is on the viewer-facing display only”

### 3. background_prop

The object exists as decoration or context and is not the main carrier of text.

Rules:

- `text_visibility` should be `symbolic_only`, `illegible`, or `blank`.
- `allowed_text_density` should be `none`, `minimal`, or `low`.
- Background text must not carry required facts.
- Decorative English or pseudo text must not introduce factual claims.

## Decision matrix

| Character reading? | Viewer-facing? | Camera relation | Prop role | Allowed text visibility | Decision |
|---|---|---|---|---|---|
| yes | no | side / three_quarter | self_reading | symbolic_only / illegible / blank | PASS |
| yes | no | side / three_quarter | self_reading | clear_readable | FAIL |
| yes | unclear | unclear | self_reading | clear_readable | WARNING or FAIL |
| no | true | front | viewer_presentation | clear_readable | PASS |
| no | false | background | background_prop | symbolic_only / illegible / blank | PASS |
| yes | true | over_shoulder | self_reading | partial only | WARNING |

## Mandatory gates

```text
IF prop_role = self_reading
AND character_is_reading = true
AND viewer_facing = false
AND text_visibility = clear_readable:
  viewpoint_visibility_status = FAIL
  readability_misuse_detected = true
  BLOCK image_gen
  FORCE repair loop
```

```text
IF readable text is required for user comprehension
AND prop_role != viewer_presentation:
  move required text to independent card text area
  set prop text_visibility = symbolic_only or illegible
  requires_prompt_constraint = true
```

```text
IF prop_orientation, character gaze, and viewer camera angle conflict:
  viewpoint_visibility_status = FAIL
  BLOCK image_gen
  repair by choosing either self_reading with unreadable prop text OR viewer_presentation with front-facing prop
```

## Integration requirements

- `layout_graph_compiler` must build `prop_visibility_plan` before prompt composition.
- `runtime_simulator` must predict viewpoint visibility risk before any `image_gen.text2im` call.
- `structure_scorer` must include viewpoint realism and readable-surface perspective checks.
- `prompt_composer` must include explicit prop text visibility constraints whenever text-bearing props are present.
- `execution_trace` must record `viewpoint_visibility_guard_result`, `prop_visibility_plan`, conflicts, and repair decisions.
- `gate_system` and `execution_controller` must block image generation when `viewpoint_visibility_status = FAIL`.

## Repair actions

Priority order:

1. Keep scene and action, downgrade prop text to symbolic_only / illegible / blank.
2. Move required information from prop surface to independent card text area.
3. Change composition to clear viewer_presentation if the prop must carry readable text.
4. Use over-the-shoulder only for partial, not full, readable text.
5. Remove the text-bearing prop if it creates repeated conflicts.

## Non-negotiable principle

```text
视角真实性 > 道具文字可读性
```

A self-reading prop may look meaningful, but it must not become a physically impossible front-facing text panel.
