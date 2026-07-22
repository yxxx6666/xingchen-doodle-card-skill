---
name: xingchen-doodle-card-skill
description: use this skill when users provide chinese articles, notes, educational copy, science or health content and want finished xiaohongshu-style 3:4 hand-drawn doodle image cards. automatically plan pages, preserve factual meaning, lock one typography/icon/chart system, generate strictly from the cover in numeric order with Codex built-in $imagegen, validate the actual returned aspect ratio, discard non-3:4 results without post-processing, checkpoint each page, recover from service timeouts, and package only continuous ordered files. treat every ratio request as an aspect-ratio requirement, never as a fixed-pixel requirement.
---

# xingchen doodle card

Version: v0.8.10  
Display name: 涂鸦卡片  
Skill ID: `xingchen-doodle-card-skill`

## 目标

把用户提供的中文内容整理成可直接发布的 3:4 小红书涂鸦插画卡片。自动决定页数，并让整组页面在事实、中文字形、数字字形、图标、图表、配色、组件、生成顺序和文件顺序上保持一致。

正式图片只使用 Codex 自带的 `$imagegen` 直接生成，不检查、不要求 `OPENAI_API_KEY`，不调用外部 Images API。每张图必须由图像模型一次性原生生成插画与中文文字。禁止补边、裁切、缩放、拉伸、扩图、重绘、局部补字、Canvas、SVG、HTML/CSS、PIL 排版、第三方排版器、分层合成或任何像素后处理。读取真实宽高和文件哈希不属于图像修改。

## 比例语义：只认比例，不认固定像素

`3:4`、`9:16`、`1:1` 等表达只代表画面宽高比，不代表某一组固定像素。

本技能只有一种正式比例模式：`publish-3x4`。

- 用户说“3:4”“3:4 竖版”“小红书比例”“1080×1440 比例”“1536×2048 比例”时，只提取宽高比 `3:4`。
- 不把任何比例自动改写为固定像素要求。
- 不因为用户举出一组 3:4 数字，就要求最终文件必须等于这组数字。
- `1086×1448`、`1080×1440`、`1536×2048` 都是合格 3:4。
- `1024×1536` 是 2:3，不合格。
- 如果用户明确要求“最终实际像素必须严格等于某组宽高”，说明 Codex `$imagegen` 不能保证固定像素；不得切换外部 API，也不得假装能保证。先请求用户接受“原生 3:4 比例、不固定像素”。

## 核心优先级

```text
事实保真 > 中文准确 > 严格顺序 > 原生3:4比例 > 系列一致性 > 结构可读 > 视角真实
```

## 全局流程

```text
input
→ interpret_aspect_ratio_only
→ encoding_guard
→ evidence_ledger_builder
→ content_graph_builder
→ auto_page_planner
→ page_content_allocator
→ claim_binding_validator
→ content_fidelity_guard
→ viewpoint_visibility_guard
→ series_style_manifest
→ output_file_namer.plan
→ runtime_preflight
→ sequential_generation_controller
→ prompt_composer(current page)
→ $imagegen(current page)
→ actual_pixel_ratio_gate
→ series_consistency_gate
→ progress_checkpoint
→ repeat next numeric page
→ output_file_namer.verify
→ final_revalidation
→ finalize_series_files
```

不得绕过严格顺序、实际像素比例校验、系列一致性或最终重新验图。

## 1. 内容解析与事实保真

处理健康、科学、法律、金融或带数据内容时，读取：

- [证据台账](core/evidence_ledger_builder.md)
- [事实保真规则](references/factual-content-rules.md)
- [证据绑定示例](references/evidence-binding-examples.md)
- [内容保真守卫](core/content_fidelity_guard.md)

每个数字保留数字、单位、时间窗口、人群、比较组、结果和原句来源。不得跨研究拼接，不得把相关性改写成因果。

## 2. 自动分页

读取：

- [自动分页器](core/auto_page_planner.md)
- [分页规则](references/page-count-rules.md)
- [页面内容分配器](core/page_content_allocator.md)

默认 `P01=cover`，`P02...Pn=content`。只有用户明确指定页数时才锁定总页数。

## 3. 文字、图标与图表一致性

生成前读取：

- [系列样式清单](core/series_style_manifest.md)
- [系列样式模板](templates/series-style-manifest-template.md)
- [文字一致性规则](references/typography-consistency-rules.md)
- [图标一致性规则](references/icon-consistency-rules.md)
- [图表一致性规则](references/chart-consistency-rules.md)
- [统一画风](styles/chinese-doodle-editorial-style-lock.md)

冻结一个 `verbatim_style_block`，逐页原样复制。整组最多一个中文字形体系、三个文字层级、一个数字与标点体系、一套图标语法和一套图表语法。

## 4. 严格顺序与断点续跑

读取：

- [严格顺序控制器](core/sequential_generation_controller.md)
- [超时恢复控制器](core/timeout_recovery_controller.md)
- [进度清单模板](templates/series-progress-manifest-template.md)
- [超时紧凑重试模板](templates/compact-timeout-retry-prompt-template.md)

```text
generation_order = delivery_order = P01,P02,P03,...Pn
```

- 第一张必须是封面。
- 当前页未通过，不启动下一页。
- 禁止并行生成多页。
- 每页通过后立即写入断点清单。
- 恢复时从第一张未完成页继续。
- 进度必须落盘为原子 JSON 清单。
- 每次新会话先恢复 stale `WAITING_IMAGEGEN` 状态。

## 5. 运行前预检

读取：

- [图像后端契约](references/native-image-backend-contract.md)
- [3:4 比例锁](references/aspect-ratio-lock.md)

运行：

```bash
python scripts/runtime_preflight.py \
  --expected-version v0.8.10 \
  --requested-ratio 3:4
```

预检必须直接选择 Codex `$imagegen`，并明确：

- `fixed_pixel_size_required = false`
- `requires_api_key = false`
- 验收依据是返回文件的真实宽高比，而不是某组固定像素。

## 6. 提示词与 `$imagegen` 调用

读取：

- [视角可见性守卫](core/viewpoint_visibility_guard.md)
- [布局图编译器](core/layout_graph_compiler.md)
- [提示词编译器](core/prompt_composer.md)
- [标准提示词模板](templates/image-gen-card-prompt-template.md)
- [内置 imagegen 契约](references/image-gen-text2im-contract.md)

正式图片必须使用 Codex 自带 `$imagegen`。提示词首段和末段都写清：

```text
画布必须是原生 3:4 竖版，不是 2:3、4:5、9:16、A4 或长海报；不要求固定像素尺寸。
```

如果 `$imagegen` 实际暴露 `aspect_ratio`，传入 `3:4`；如果只接受 prompt，则不得虚构 `size`、`width` 或 `height` 参数。生成后读取真实像素硬校验。

## 7. 实际像素比例硬门

读取：

- [比例硬门](core/aspect_ratio_gate.md)
- [最终验收规则](references/validation-rules.md)

```bash
python scripts/validate_native_3x4.py GENERATED_IMAGE.png \
  --requested-ratio 3:4 \
  --log-jsonl generation-log.jsonl
```

唯一比例通过条件：

```text
abs(actual_width / actual_height - 0.75) <= 0.001
```

不校验固定像素，不比较“请求宽高”和“实际宽高”。若不通过：删除或隔离本次结果，使用同一文字、同一样式锁和同一文件名从头重生成当前页。不得修图。

## 8. 文件名预规划

读取 [文件命名器](core/output_file_namer.md)。生成前完成唯一文件名规划：

```text
01-cover-{topic-slug}.png
02-content-{topic-slug}.png
03-content-{topic-slug}.png
04-action-{topic-slug}.png
```

重试与续跑不得改变文件名。

## 9. 系列一致性验收

读取：

- [系列一致性门](core/series_consistency_gate.md)
- [整组一致性规则](references/group-consistency-rules.md)

明显字体、数字、图标、图表、纸色、线宽或组件漂移均判失败，只重新生成当前页。

## 10. 最终重新验图与打包

```bash
python scripts/finalize_series_files.py \
  --manifest SERIES_PROGRESS.json \
  --source-dir GENERATED_IMAGES \
  --output-dir FINAL_IMAGES \
  --validation-mode publish-3x4 \
  --zip FINAL_SERIES.zip
```

最终器必须重新打开每张源图和目标图，重新读取宽高、比例和 SHA-256；不得相信旧的 `ratio_passed=true`。最终器只复制或移动文件及写 ZIP，不改变像素。

## 11. 超时、会话重连与断点恢复

`request timed out` 表示本次 `$imagegen` 调用没有在工具或会话期限内返回图片。没有运行时证据时不得武断归因。

执行硬规则：

- 调用前先用 `scripts/series_progress_controller.py begin` 原子写入 `WAITING_IMAGEGEN`。
- 每次请求最多携带一张已通过的参考图。
- 首次服务超时不消耗内容尝试，只重试当前页一次。
- 同一执行窗口第二次超时后写入 `PAUSED_TIMEOUT` 并停止。
- 用户说“继续”时，从磁盘读取清单，只恢复 `resume_from_page_id`。
- 会话重连导致旧请求状态丢失时，运行 `recover --force-after-reconnect`。
- 图片返回但比例、中文、结构或一致性失败，才消耗内容尝试；最多 3 次。
- 当前页未 `COMPLETE` 前，下一页不得启动。

首次超时后的重试使用 [紧凑超时重试模板](templates/compact-timeout-retry-prompt-template.md)，保持文字、事实、文件名和样式锁不变，只移除重复说明与非必要装饰。

## 最终交付

只交付事实、中文、结构、视角、真实 3:4 比例、系列一致性、生成顺序和文件顺序全部通过的图片。最终文件可以是任何原生像素尺寸，只要真实比例为 3:4。绝不把比例要求升级成固定像素要求。
