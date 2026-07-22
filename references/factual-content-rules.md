# Factual Content Rules v0.8.10

These rules activate the Content Fidelity Layer for factual, scientific, health, financial, legal, safety, and data-driven inputs.

## When to activate factual guard

When input contains any of the following, content_fidelity_guard must activate:

- 研究
- 荟萃分析
- 系统综述
- 样本量
- 随访
- 风险
- 死亡率
- 心血管
- 癌症
- 糖尿病
- WHO
- 百分比
- 置信区间
- 可穿戴设备
- 传感器
- 相关
- 可能
- 证据
- 数据
- 法律
- 金融
- 投资
- 医疗
- 疾病
- 药物
- 治疗
- 安全性

## General factual rules

- Prefer source-grounded wording over catchy wording.
- Do not invent numbers.
- Do not invent time windows.
- Do not invent populations.
- Do not invent mechanisms.
- Do not invent certainty.
- If the source says “可能”, keep “可能”.
- If the source says “相关”, keep “相关”.
- If the source says “观察性研究”, do not write causal certainty.
- If the source says “研究人员认为”, write “可能” or “研究者认为”.
- If the source says “与……相关”, do not write “一定会降低”.
- For high-stakes content, shorter text must not be less accurate.

## Cover page rules

- Cover can be catchy, but cannot be less accurate than the source.
- Cover should avoid exact percentages unless the evidence anchor is clear.
- If the source contains multiple studies, cover should use qualitative promise.
- Headline claims are low-trust unless supported by body evidence.
- If uncertain, soften or omit the number.
- numbers must keep their source anchor.
- do not merge numbers across studies/time windows.

Safe cover patterns:

- “每天几分钟，也可能有收益”
- “从不动到动，收益最大”
- “短促运动，也算数”
- “别等完美计划”

Risky cover patterns:

- “几分钟降低31%死亡风险”
- “每天2分钟防心脏病”
- “所有人都适用”
- “一定有效”
- “比健身房更有用”

## Scientific wording preferences

Recommended:

- “研究发现”
- “与……相关”
- “可能”
- “风险更低相关”
- “相关下降”
- “在该研究中”
- “与完全不运动相比”
- “较……人群”

Avoid unless source supports:

- “一定”
- “保证”
- “直接导致”
- “治愈”
- “防止”
- “逆转”
- “所有人”
- “只要……就能……”

## Core semantic reminders

- Content Fidelity Layer protects source-to-card meaning.
- evidence ledger comes before page planning.
- claim binding comes before final text approval.
- content_fidelity_guard blocks unsafe prompts.
- correlation is not causation.
- unbound number must block image_gen.
- misleading cover numeric claim must be rewritten.
- observational claim uses causal wording = fail unless source supports causation.
