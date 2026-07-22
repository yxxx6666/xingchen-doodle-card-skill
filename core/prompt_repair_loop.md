# prompt_repair_loop — v0.5.0 Failure Repair Loop

Purpose: automatically repair risky prompts before a formal image-model request is dispatched.

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

Repair loop only rewrites the prompt. It does not enable general PIL rendering, Canvas, SVG, HTML, post-processing typography, or any fallback renderer. Ratio repair is forbidden. The default legal renderer is Codex `$imagegen`; no external image API helper is allowed.

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


## v0.8.10 Content Fidelity Repair Invalidation Rule

If repair or downgrade changes Chinese page text:

```text
approved_page_text becomes invalid
RE-RUN claim_binding_validator
RE-RUN content_fidelity_guard
BLOCK image_gen until both pass
```

This rule applies to all repair levels and all downgrade strategies. Repair may simplify visual structure, but it must not silently rewrite approved Chinese claims after approval.

No renderer fallback is allowed. The default legal renderer is Codex `$imagegen`; no external image API helper is allowed.


## v0.8.10 Page Count Repair Rule

If repair or downgrade changes Chinese page text:

```text
approved_page_text becomes invalid
RE-RUN claim_binding_validator
RE-RUN content_fidelity_guard
BLOCK image_gen until both pass
```

If repair or downgrade changes page count, page role plan, or claim allocation:

```text
RE-RUN auto_page_planner
RE-RUN page_content_allocator
RE-RUN claim_binding_validator
RE-RUN content_fidelity_guard
RE-RUN output_file_namer
BLOCK image_gen until all pass
```

Repair may simplify visual structure, but it must not silently reduce auto_page_planner.recommended_total_pages.
No renderer fallback is allowed. The default legal renderer is Codex `$imagegen`; no external image API helper is allowed.
