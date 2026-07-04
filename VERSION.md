# Version

Current version: **v0.4.2**

Skill name: `xingchen-doodle-card-skill`

Release type: Execution Lock + Single Image Gen Authority patch

Release date: 2026-07-02

## Version scope

v0.4.2 strengthens v0.4.0 with an explicit Execution Lock and Single Image Gen Authority. It makes `image_gen.text2im` the only legal renderer and prohibits fallback renderer, local text rendering, separated illustration/text pipelines, post-processing typography layers, and bypassing image_gen to fix Chinese text.

Display name: **涂鸦卡片**
Owner tag: **xingchen**

## v0.4.2 scope

Adds Aspect Ratio Lock + Page-by-Page Verification. Every image must be native 3:4. 2:3, 4:5, 9:16, square, A4, and long poster outputs are failed outputs.
