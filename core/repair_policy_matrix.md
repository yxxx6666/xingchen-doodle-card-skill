# repair_policy_matrix — v0.6.0 Repair Policy Matrix

Purpose: map structure_score and detected_issues to deterministic repair actions.

## Risk levels

```text
SAFE >= 85: no repair
WARNING 70-84: Level 1 repair
FAIL < 70: Level 2 or Level 3 repair
```

## Anatomy problems

If detected_issues include anatomy risk:

- 删除多余动作
- 改为单动作
- 改为坐姿/侧身
- 减少props
- force exactly two hands and exactly two feet
- all limbs clearly connected

## Scene overload

If detected_issues include scene overload:

- props <= 8
- 删除非核心元素
- 单场景化
- extra information becomes text bullet or split card

## Action complexity

If detected_issues include action conflict:

- 多动作 → 单动作
- 双手操作 → 单手
- high dynamic pose → seated / side-standing / static pose

## Repair levels

### Level 1：轻修复

- 文案压缩
- 删除装饰物
- keep same concept
- keep same scene

### Level 2：结构修复

- 单动作
- 单场景
- 降低姿态复杂度
- props <= 8
- interaction props <= 1-2

### Level 3：安全降级

- 仅标题 + 单角色 + 3要点
- simple seated or side-standing pose
- one hand lightly interacting with one object
- all other props become background marks

## Output repair instruction

```json
{
  "repair_level": "Level 1 | Level 2 | Level 3",
  "repair_actions": [],
  "regenerate_required": true
}
```

## v0.6.1 Executable Policy Upgrade

The repair_policy_matrix is now an executable strategy table.

```text
Anatomy failure → reduce actions → reduce props → seated pose
Scene overload → limit props ≤ 8 → single scene
Action complexity → single action only
```

Repair loop must be driven by structure_score and gate_system:

- 70–84: repair once
- 50–69: layout downgrade
- <50: full simplification

## v0.6.2 Simulation-aware repair

repair now depends on:

- simulation result
- execution trace
- scorer delta

### Repair inputs

- runtime_simulator.simulated_score
- runtime_simulator.predicted_issues
- execution_trace.repair_triggered
- execution_trace.downgrade_triggered
- structure_scorer.pre_gen_score
- structure_scorer.post_gen_score
- structure_scorer.delta

### Repair rule

If simulated_score < 85, do not call image_gen. Repair the prompt/layout first.
If scorer delta shows instability, simplify layout and reduce props.
If execution_trace shows repeated repair, downgrade to minimal safe output.
