# pose_safety — v0.5.0 Pose Safety System

Purpose: choose poses that image_gen can render reliably in cute hand-drawn doodle style.

## Safe pose priority

Prefer:

1. 站立侧身
2. 坐姿
3. 轻微伸手
4. 静态动作
5. 半身安静构图

## Forbidden / high-risk poses

Avoid:

- 大幅扭转身体
- 双臂交叉复杂动作
- 多方向同时动作
- 高动态姿态
- 跑跳、摔倒、旋转、舞蹈动作
- 一边走一边操作多个物体
- 身体朝一个方向、头和手朝多个方向

## Safe default pose

When uncertain, use:

```text
one young Chinese woman in a simple seated or side-standing pose, one calm main action, one hand lightly interacting with one object, the other hand naturally relaxed, both feet visible or logically placed, all limbs clearly connected.
```

## Pose downgrade rule

If the requested scene contains risky action, downgrade:

- running → standing side view
- carrying many items → holding one object
- opening door + looking back + holding bag → standing beside door holding one key
- pointing + writing + holding phone → lightly pointing at one note

## Cross-layer enforcement keywords

This layer is part of v0.5.0 anatomy constraints layer / scene complexity limiter / pose safety / prompt repair loop. Final prompt must include the STRUCTURE SAFETY BLOCK. It reinforces: 结构正确性 > 可读性 > 美观 > 丰富度; one main character; 2只手 / exactly two hands; 2只脚 / exactly two feet; all limbs clearly connected; no 第三只手; no 隐藏手; no 从桌子/衣服/墙里伸出的手; 一个角色只能有一个主动作 / one simple main action; 1~2 个物体; 坐姿; 站立侧身; 删除非必要物体; 降低动作复杂度.

