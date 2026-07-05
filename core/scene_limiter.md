# scene_limiter — v0.5.0 Scene Complexity Limiter

Purpose: prevent scene overload from causing body distortion and unreadable doodle cards.

## Scene limits

- 单画面最多 1 个主场景。
- 静态物体最多 6~12 个。
- 主角色最多 1 个。
- 主要交互对象最多 1~2 个。
- 禁止信息过载。
- 多信息必须拆卡片，而不是塞进一张图。

## Information density rule

If information > 5 points:

```text
must visually group information
must not draw everything into the same physical space
must split into multiple cards when grouping is not enough
```

## Object role rules

Objects must be classified as:

1. main interaction object
2. supporting scene object
3. background object

Only the main interaction object can be touched by the character.
Supporting/background objects must not create additional actions.

## Simplification rule

If a scene includes too many props, simplify in this order:

1. remove decorative props
2. merge similar props
3. keep only one interaction object
4. convert extras to simple background marks
5. split into another card

## Cross-layer enforcement keywords

This layer is part of v0.5.0 anatomy constraints layer / scene complexity limiter / pose safety / prompt repair loop. Final prompt must include the STRUCTURE SAFETY BLOCK. It reinforces: 结构正确性 > 可读性 > 美观 > 丰富度; one main character; 2只手 / exactly two hands; 2只脚 / exactly two feet; all limbs clearly connected; no 第三只手; no 隐藏手; no 从桌子/衣服/墙里伸出的手; 一个角色只能有一个主动作 / one simple main action; 1~2 个物体; 坐姿; 站立侧身; 删除非必要物体; 降低动作复杂度.



## Explicit density trigger

如果 信息 > 5 个要点，必须视觉分组；如果仍然过载，必须拆卡片。

## v0.6.0 Scene limiter hard caps

- scene = 1
- props <= 10
- interaction props <= 2
- bullets <= 5

If the content exceeds these caps, use content_graph_builder and layout_graph_compiler to split, group, or demote details.

## v0.6.1 Hard scene limits

```text
scene = 1
props ≤ 10
interaction props ≤ 2
bullets ≤ 5
```

If any hard limit fails, gate_system must block image_gen and send the pipeline to REPAIR or DOWNGRADE.
