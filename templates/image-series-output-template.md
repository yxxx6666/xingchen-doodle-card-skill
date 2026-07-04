# Image Series Output Template v0.4.2

```text
【图片组概览】
共 X 张：
01 封面｜……
02 内容页｜……

【Aspect Ratio Lock】
所有页面必须是原生 3:4。每页生成后先检查实际比例，确认 3:4 后才继续下一页。2:3 / 4:5 / 9:16 不是小偏差，是失败输出。

【Single Image Gen Authority】
唯一允许路径：image_gen.text2im。每张图单次完整生成。禁止 fallback renderer、本地画字、后处理叠字、插画与文字分离 pipeline。

【第 1 张｜封面】
A. 风格定义：hand-drawn doodle illustration, minimalist ink line art, imperfect sketch lines, soft pastel accents, large white negative space
B. 场景描述：……
C. 构图规则：vertical 3:4 composition, subject placed bottom-left or side, large empty space for typography, editorial magazine layout feel
D. 中文文字：Title / Subtitle / Optional points
E. 英文辅助：……
F. image_gen.text2im prompt：
STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.
Create one complete image on a native 3:4 vertical canvas.
Target canvas: 1080×1440 Xiaohongshu-style card, or any exact 3:4 equivalent.
Do not use 2:3, 4:5, 9:16, square, A4, landscape, or long poster format.

A hand-drawn doodle editorial illustration.
...

【Execution Lock 自检】
- 是否只使用 image_gen.text2im：是
- 是否单次完整生成：是
- 是否实际比例为 3:4：是
- 是否不是 2:3 / 4:5 / 9:16：是
- 是否无 fallback renderer：是
- 是否无本地画字：是
- 是否无 PIL / Canvas / SVG / HTML / CSS 文字渲染：是
- 是否无插画与文字分离 pipeline：是
- 是否无后处理叠字：是
- 是否没有为了修正中文而绕过 image_gen：是
- 是否插画 + 中文一次生成完成：是
- 是否风格一致性优先于中文完美性：是
```
