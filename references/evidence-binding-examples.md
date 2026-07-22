# Evidence Binding Examples v0.8.10

## Example: prohibited merge

Source line A: “低于 WHO 建议标准的人死亡风险下降31%。”
Source line B: “每天3–4分钟短时高强度活动与死亡风险下降相关。”

FAIL:

- “每周几分钟，死亡风险下降31%”

Reason: the percentage and time window belong to different source anchors.

PASS:

- “低于建议标准：死亡风险↓31%”
- “每天3–4分钟：与死亡风险下降相关”

## Example: association vs causation

Source: “A 与 B 风险下降相关。”

PASS:

- “A 与 B 风险更低相关”

FAIL:

- “A 会直接降低 B 风险”

## Example: mechanism uncertainty

Source: “研究人员认为，可能通过改善代谢发挥作用。”

PASS:

- “可能改善代谢”

FAIL:

- “通过改善代谢发挥作用”
