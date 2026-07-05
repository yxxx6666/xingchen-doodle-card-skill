# prompt_repair_loop — v0.5.0 Failure Repair Loop

Purpose: automatically repair risky prompts before image_gen.text2im is called.

## Trigger risks

If the prompt contains any of the following risks, repair must run:

- 多手风险
- 多脚风险
- 多动作风险
- 场景过载
- 结构不清晰
- 多角色默认出现
- 手部交互对象过多
- 身体扭转或高动态姿态

## Repair strategy priority

1. 删除非必要物体
2. 降低动作复杂度
3. 将双手动作改为单手
4. 改为坐姿/静态姿态
5. 减少场景元素
6. 强制重新生成 prompt

## Repair output requirement

A repaired prompt must explicitly state:

```text
Repaired for structure stability: one main character, one simple action, at most two interaction objects, safe seated or side-standing pose, simple scene, exact two hands and two feet, all limbs connected.
```

## No renderer fallback

Repair loop only rewrites the prompt. It does not enable PIL, Canvas, SVG, HTML, post-processing typography, or any fallback renderer.
The only legal renderer remains image_gen.text2im.

## Cross-layer enforcement keywords

This layer is part of v0.5.0 anatomy constraints layer / scene complexity limiter / pose safety / prompt repair loop. Final prompt must include the STRUCTURE SAFETY BLOCK. It reinforces: 结构正确性 > 可读性 > 美观 > 丰富度; one main character; 2只手 / exactly two hands; 2只脚 / exactly two feet; all limbs clearly connected; no 第三只手; no 隐藏手; no 从桌子/衣服/墙里伸出的手; 一个角色只能有一个主动作 / one simple main action; 1~2 个物体; 坐姿; 站立侧身; 删除非必要物体; 降低动作复杂度.

## v0.6.0 Three-level repair loop

The repair loop now uses structure_score and risk_level.

### Level 1：轻修复

- 文案压缩
- 删除装饰物
- keep same layout_graph

### Level 2：结构修复

- 单动作
- 单场景
- 降低姿态复杂度
- props <= 8
- interaction props <= 2

### Level 3：安全降级

- 仅标题 + 单角色 + 3要点
- one safe seated or side-standing pose
- one interaction object max
- max_attempts = 3

The repair loop is scoring-based: structure_score below 85 triggers repair.
