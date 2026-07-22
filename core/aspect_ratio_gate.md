# aspect_ratio_gate — v0.8.10

Purpose: validate the actual pixel ratio returned by Codex `$imagegen`. This gate never repairs images and never enforces fixed pixels.

## Single mode: publish-3x4

```text
$imagegen request
→ read returned file dimensions
→ ratio validation
→ hash and log
→ accept or discard and regenerate same page
```

Hard pass:

```text
abs(actual_width / actual_height - 0.75) <= 0.001
```

Examples:

- `1086x1448`: PASS.
- `1080x1440`: PASS.
- `1536x2048`: PASS.
- `768x1024`: PASS.
- `1024x1536`: FAIL because it is 2:3.

No fixed pixel size is required or compared.

## Ratio interpretation

A pair such as `1536x2048` may be used as a ratio example. It does not create an exact-pixel requirement. If the user explicitly demands exact output pixels, explain that Codex `$imagegen` cannot guarantee them and ask to proceed with ratio-only output.

## Forbidden

- padding or canvas enlargement;
- crop;
- resize or stretch;
- redraw, inpainting or outpainting to change ratio;
- local typography or overlays;
- accepting by visual guess without reading real dimensions;
- switching to an external API to enforce pixels.

## Command

```bash
python scripts/validate_native_3x4.py IMAGE_PATH --requested-ratio 3:4
```

Failure action: discard or quarantine the returned file and regenerate the same page from scratch. Never advance to the next page.
