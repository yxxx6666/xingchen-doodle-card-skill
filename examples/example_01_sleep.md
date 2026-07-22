# Example - 睡前手机偷走睡意

## native image-model prompt

```text
STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.
Create one complete image on a native 3:4 vertical canvas.
Target canvas: 1080×1440 Xiaohongshu-style card, or any exact 3:4 equivalent.
Do not use 2:3, 4:5, 9:16, square, A4, landscape, or long poster format.

A hand-drawn doodle editorial illustration.

Scene: an office worker puts a phone on a small bedside table in a quiet night routine.
Style: minimalist ink doodle, imperfect sketch lines, soft pastel accents, large white negative space.

Composition: vertical 3:4, subject placed bottom-left or side, with large empty space reserved for text.

Chinese text integrated into image:
Title: "睡前手机偷走睡意"
Subtitle: "大脑还在兴奋，睡意就被推远"
Optional points:
- 放下屏幕
- 留给睡眠

Mood: calm, warm, educational, reflective.

Avoid:
- any external text rendering
- post-processing typography layers
- PIL/Canvas/SVG/HTML rendering
- CSS text systems
- multi-stage composition pipeline
- fallback renderer
```

## Execution Lock 自检

- 是否只使用 Codex `$imagegen` 原生生成并验证真实 3:4 比例：是
- 是否单次完整生成：是
- 比例检查：有尺寸时精确验证；无尺寸时仅做视觉检查
- 是否不是 2:3 / 4:5 / 9:16：是
- 是否无 fallback renderer：是
- 是否无本地画字：是
- 是否无 PIL / Canvas / SVG / HTML / CSS 文字渲染：是
- 是否无插画与文字分离 pipeline：是
- 是否无后处理叠字：是
- 是否没有为了修正中文而绕过 image_gen：是
- 是否插画 + 中文一次生成完成：是
- 是否风格一致性优先于中文完美性：是
