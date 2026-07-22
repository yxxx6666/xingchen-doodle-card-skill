# content_fidelity_guard — v0.8.10 Content Fidelity Guard

Purpose:
Block page prompts when the compressed Chinese text changes the factual meaning of the user source.

This guard must run before formal image generation. It accepts only page text that has passed claim_binding_validator.

## Required checks

1. 数字是否来自原文
2. 数字是否绑定正确对象
3. 单位是否保留
4. 时间窗口是否保留
5. 研究对象是否保留
6. 比较组是否保留
7. 结论类型是否保留
8. 相关是否被误写成因果
9. 机制推测是否被误写成确定结论
10. 行动建议是否被夸大
11. 标题钩子是否混合了多个证据线
12. 是否引入了原文没有的新事实
13. 是否为了简短而改变了意思
14. 是否将“可能”“相关”“研究发现”删掉后造成过度承诺
15. 是否把一个研究的数字套到另一个研究的时间单位、样本、人群或结论上

## Output format

```json
{
  "content_fidelity_status": "PASS | WARNING | FAIL",
  "risk_level": "low | medium | high",
  "failed_checks": [],
  "warnings": [],
  "required_rewrites": [],
  "approved_pages": [],
  "blocked_pages": []
}
```

## Hard gates

```text
IF content_fidelity_status = FAIL:
  BLOCK image_gen
  REWRITE page text
  RE-RUN claim_binding_validator
  RE-RUN content_fidelity_guard

IF risk_level = high:
  BLOCK cover numeric claim unless fully anchored

IF observational health/science claim uses causal wording:
  BLOCK image_gen and rewrite with cautious wording

IF any number is unbound:
  BLOCK image_gen

IF a page mixes numbers across different studies/time windows:
  BLOCK image_gen
```

## 内容保真优先级

```text
事实保真 > 证据绑定 > 中文简洁 > 视觉美感 > 标题冲击力
```

This does not replace the existing visual execution priority. Both priority systems are active:

- 视觉执行层：结构正确性 > 可读性 > 美观 > 丰富度
- 内容表达层：事实保真 > 证据绑定 > 中文简洁 > 视觉美感 > 标题冲击力

## Approval rules

- Only approved_pages may move into prompt_composer.
- approved_page_text must be frozen before prompt_composer.
- prompt_composer must use approved_page_text verbatim.
- Any layout shortening or text rewrite invalidates approval and must re-run claim_binding_validator and content_fidelity_guard.
- The guard checks source-to-card fidelity. It does not silently correct source facts with external facts unless the user explicitly asks for verification.

## Common blocks

- unbound number
- misleading cover numeric claim
- observational claim uses causal wording
- percentage/time-window mismatch
- cross-study claim merge
- mechanism certainty overclaim
- deleted qualifier causing overclaim
- invented population or comparison group
