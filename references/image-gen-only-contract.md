# Image Generation Only Contract v0.8.10

The only approved formal image backend is Codex built-in `$imagegen`.

- Generate the complete card in one model image attempt.
- Request a native 3:4 portrait ratio.
- Do not require or promise fixed output pixels.
- Do not use external Images API, HTML, SVG, Canvas, PIL rendering, overlays, crop, resize, padding or compositing.
- Read-only dimension and hash inspection is allowed.
- Reject and regenerate any returned file whose actual ratio is not 3:4.
