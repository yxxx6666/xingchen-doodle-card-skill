# Version

Current version: **v0.6.2**

Skill name: `xingchen-doodle-card-skill`

Release type: Production-grade Observable AI Visual Compilation Pipeline

Release date: 2026-07-05

## Version scope

v0.6.2 upgrades v0.6.1 into a production-grade deterministic AI pipeline.

This is not a style expansion. It adds runtime simulation, encoding safety, and execution traceability.

The only legal rendering path remains `image_gen.text2im`.

Display name: **涂鸦卡片**
Owner tag: **xingchen**

## Core principle

结构正确性 > 可读性 > 美观 > 丰富度

## Final production chain

```text
encoding safety before pipeline
simulation before generation
execution trace after generation
scorer controls execution
controller is single source of truth
image_gen only allowed if ALL checks pass
```
