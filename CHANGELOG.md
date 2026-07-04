# Changelog

## v0.4.2 - 2026-07-03

### Rename patch

- Renamed public display name to 涂鸦卡片.
- Renamed package / Skill ID to `xingchen-doodle-card-skill`.
- Kept Execution Lock + Single Image Gen Authority rules unchanged.

## v0.4.2 - 2026-07-02

Execution Lock + Single Image Gen Authority patch.

### Added

- Explicit Execution Lock.
- Explicit Single Image Gen Authority.
- Prohibition against bypassing image_gen to fix Chinese text.
- Standard prompt updated to use `imperfect sketch lines` and `with large empty space reserved for text`.
- Avoid list updated to include CSS text systems and multi-stage composition pipeline.

### Kept

- `image_gen.text2im` remains the only legal visual generation path.
- No fallback renderer.
- No local deterministic Chinese layout.
- No post-processing typography layers.
