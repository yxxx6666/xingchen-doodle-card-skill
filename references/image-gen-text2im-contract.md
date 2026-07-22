# Codex $imagegen Contract v0.8.10

Use Codex built-in `$imagegen` for every formal page.

- If the tool exposes `aspect_ratio`, request `3:4`.
- If the tool only accepts prompt text, repeat the native 3:4 requirement at the beginning and end of the prompt.
- Never invent `size`, `width` or `height` parameters.
- Never promise fixed output pixels.
- After generation, read the actual width and height and accept only ratio 0.75 within tolerance.
- A ratio failure requires a fresh generation of the same page, not image repair.
