# structure_scorer — v0.6.0 Structure Scoring System

v0.6.0 = structure-aware compilation system.

Purpose: score the compiled layout graph and final prompt before / after generation to reduce 三只手、三只脚、断肢、错误连接、多动作崩坏 and scene overload.

## Score range

```text
structure_score: 0-100
SAFE: >=85
WARNING: 70-84
FAIL: <70
```

## Scoring dimensions

### A. Anatomy Integrity（40）

Checks:

- 是否只有1个主角色
- 是否严格2只手
- 是否严格2只脚
- 是否存在隐藏/多余肢体
- all limbs clearly connected to the body
- no third hand, no hidden hand, no hand emerging from desk/clothes/wall/bag/background

Score:

```text
anatomy: 0-40
```

### B. Action Simplicity（20）

Checks:

- 是否只有1个主动作
- 是否动作冲突
- 是否复杂姿态
- no multi-action instruction
- no high dynamic pose

Score:

```text
action: 0-20
```

### C. Scene Complexity（20）

Checks:

- 是否单场景
- props是否过多
- 是否视觉过载
- scene = 1
- props <= 10
- bullets <= 5

Score:

```text
scene: 0-20
```

### D. Interaction Clarity（20）

Checks:

- 手与物体关系是否清晰
- 是否超过2个交互物体
- interaction props <= 2
- each hand has at most one clear target

Score:

```text
interaction: 0-20
```

## Output format

```json
{
  "structure_score": 0,
  "risk_level": "SAFE | WARNING | FAIL",
  "subscores": {
    "anatomy": 0,
    "action": 0,
    "scene": 0,
    "interaction": 0
  },
  "detected_issues": [],
  "repair_required": true
}
```

## Risk rules

- SAFE: structure_score >= 85, repair_required = false
- WARNING: structure_score 70-84, repair_required = true, apply Level 1 repair
- FAIL: structure_score < 70, repair_required = true, apply Level 2 or Level 3 repair

## Non-negotiable priority

```text
结构正确性 > 可读性 > 美观 > 丰富度
```

## v0.6.1 Decision System Upgrade

The scorer is now a decision system, not only a diagnostic checklist.

```text
score >= 85 → allow image_gen
70–84 → repair once
50–69 → layout downgrade
<50 → full simplification
```

The scorer output must be consumed by execution_controller and gate_system.

```text
structure_score → controls execution
```

## v0.6.2 Simulation-aware scoring

The scorer must compare pre-generation simulation and post-generation evaluation.

```json
{
  "pre_gen_score": 0,
  "post_gen_score": 0,
  "delta": "+/-"
}
```

### Scoring interpretation

- pre_gen_score comes from runtime_simulator + prompt analysis.
- post_gen_score comes from actual generated output inspection when available.
- delta measures scoring instability.

If delta is large or post_gen_score < 85, execution_trace must record the failure and repair_policy_matrix must choose a recovery action.

```text
scorer controls execution
```

## simulation-aware scoring

Required fields: pre_gen_score, post_gen_score, delta.
