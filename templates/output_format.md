# Output Format

v0.3.0 output is a cover plus content-page image_gen prompt series.

Every page must include A-D:

A. 视觉描述（插画）  
B. 构图描述（留白/位置）  
C. 中文标题（必须原样写入 image_gen prompt）  
D. 中文正文（必须原样写入 image_gen prompt）

Use `templates/image-series-output-template.md` as the canonical output format.

## Required final self-check

```text
【闭环自检】
- 是否完全由 image_gen 生成整张图：是
- 是否禁止本地绘图 / 排版 / 后期叠字：是
- 是否每页中文标题原样进入 prompt：是
- 是否每页中文正文原样进入 prompt：是
- 是否插画 + 场景 + 文字同一次生成：是
- 是否 3:4 竖版：是
- 是否大面积留白：是
```
