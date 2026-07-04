# RELEASE REPORT

Skill: `xingchen-doodle-card-skill`

Version: `v0.4.2`

Display name: `涂鸦卡片`

Owner tag: `xingchen`

Release date: 2026-07-02

## 本版目标

v0.4.2 是 **Execution Lock + Single Image Gen Authority** 修复版。

目标：把 `image_gen.text2im` 明确为唯一渲染器，并禁止任何 fallback、本地画字、分离 pipeline、后处理叠字和为了修正中文而绕过 image_gen 的行为。

## 本版完成项

1. 新增 Execution Lock 表述。
2. 新增 Single Image Gen Authority 表述。
3. 更新唯一标准 prompt 模板。
4. 强化 forbidden 行为：PIL / Canvas / SVG / HTML / CSS、fallback renderer、multi-stage composition pipeline、post-processing typography layers。
5. 更新 quick_validate.py 校验 v0.4.2 关键字段。

## Validation results

```text
Validation passed for xingchen-doodle-card-skill v0.4.2
```

## ZIP metadata

- File: `xingchen-doodle-card-skill-v0.4.2.zip`
- Size: recorded in final delivery message and Notion version record after packaging
- SHA256: recorded in final delivery message and Notion version record after packaging

## v0.4.2 Aspect Ratio Lock

- Every output must be native 3:4.
- 2:3 / 4:5 / 9:16 are failed outputs.
- Every final prompt starts with STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.
- Page-by-page verification is required before continuing the carousel.
- Ratio-only retry must preserve content, scene, style, and Chinese text, changing only canvas ratio.

Validation result will be recorded after packaging.
