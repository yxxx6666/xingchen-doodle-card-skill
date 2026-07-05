# anatomy_guard — v0.5.0 Structure Stability Layer

Purpose: reduce three hands / three feet / broken limb connection / wrong-body attachment / multi-action collapse in image_gen doodle cards.

## Structure priority system

All prompt decisions must follow this order:

```text
结构正确性 > 可读性 > 美观 > 丰富度
structure correctness > readability > beauty > richness
```

If richness conflicts with structure, delete richness.

## 角色结构硬限制

- 每个画面默认仅 1 个主角色。
- 禁止默认生成第二角色，除非用户显式要求。
- 每个角色必须严格满足：
  - 2只手
  - 2只脚
  - 所有肢体必须明确连接身体
- 角色不得被拆成多个局部身体。
- 不允许“背景里又出现一个小人”来补充情绪。

## 手部规则（关键）

- 最多 2 只手。
- 禁止出现：
  - 第三只手
  - 隐藏手
  - 从桌子/衣服/墙里伸出的手
  - 与身体连接关系不明确的手
  - 手从错误位置长出
- 每只手必须有明确动作目标。
- 每只手最多交互 1 个物体。
- 如果手部动作难以稳定生成，优先改为：一只手轻轻拿物，另一只手自然放下。

## 脚部规则

- 最多 2 只脚。
- 禁止：
  - 腿数量异常
  - 脚部重复/镜像错误
  - 悬空腿
  - 断腿
  - 腿从错误位置长出
- 如果下半身不重要，使用稳定坐姿或半身构图，但不能用遮挡隐藏多余肢体。

## 动作规则（极其重要）

一个角色只能有一个主动作。

正确动作：
- 拿钥匙
- 坐下阅读
- 挂衣服
- 站立侧身看卡片
- 轻微伸手指向一个对象

错误动作：
- 同时开门 + 拿包 + 回头
- 一边走一边多物体操作
- 双手同时做不同复杂动作
- 身体扭转同时转头、伸手、迈步

## 交互限制

- 每个角色最多交互 1~2 个物体。
- 超过 2 个交互对象时，必须降级为背景物。
- 背景物不得要求角色同时操作。

## 遮挡规则

- 禁止用遮挡“隐藏多余肢体”。
- 所有肢体必须逻辑可解释。
- 宁可简化，不可错误。
- 遮挡只能用于自然空间层次，不能用于掩盖结构不确定。

## Prompt negative constraints

Every final prompt must include:

```text
Anatomy safety: one main character only, exactly two hands, exactly two feet, all limbs clearly connected to the body, no extra hands, no hidden hands, no hands emerging from objects, no extra legs, no floating limbs, one simple main action only.
```

## Cross-layer enforcement keywords

This layer is part of v0.5.0 anatomy constraints layer / scene complexity limiter / pose safety / prompt repair loop. Final prompt must include the STRUCTURE SAFETY BLOCK. It reinforces: 结构正确性 > 可读性 > 美观 > 丰富度; one main character; 2只手 / exactly two hands; 2只脚 / exactly two feet; all limbs clearly connected; no 第三只手; no 隐藏手; no 从桌子/衣服/墙里伸出的手; 一个角色只能有一个主动作 / one simple main action; 1~2 个物体; 坐姿; 站立侧身; 删除非必要物体; 降低动作复杂度.

## v0.6.0 Anatomy scoring additions

### anatomy scoring

Anatomy Integrity contributes 40 points to structure_score.

Checks:

- one main character only
- exactly two hands
- exactly two feet
- all limbs clearly connected
- no hidden or extra limbs

### safe pose list

- seated pose
- side-standing pose
- slight hand extension
- static action

### unsafe pose blacklist

- twisted torso
- crossed-arm complex pose
- running / jumping / dancing
- multi-direction action
- high dynamic pose

### interaction limit

- interaction props <= 2
- each hand has at most one target

## v0.6.1 Anatomy execution gates

- anatomy scoring feeds structure_score.
- safe pose list must be used before IMAGE_GEN_CALL.
- unsafe pose blacklist must block complex body instructions.
- interaction limit rules: interaction props ≤ 2 and each hand has one target at most.
