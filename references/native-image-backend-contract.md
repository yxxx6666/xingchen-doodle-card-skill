# Native Image Backend Contract v0.8.10

## Only approved formal backend

Use Codex built-in `$imagegen` directly.

- Do not require `OPENAI_API_KEY`.
- Do not call an external Images API.
- Do not block because the tool lacks `size`.
- If the real tool exposes `aspect_ratio`, set it to `3:4`.
- If it only accepts a prompt, request an exact 3:4 portrait ratio in the prompt and hard-validate the returned file.
- The returned image itself must already be 3:4. No pixel repair is allowed.

## Ratio semantics

- “3:4”, “小红书竖版”, “发布图”: request ratio 3:4.
- “1080×1440 比例”, “1536×2048 比例”: also request ratio 3:4 only.
- Never convert a ratio request into a fixed-pixel requirement.
- If the user explicitly says the final file must equal exact pixel dimensions, disclose that Codex `$imagegen` cannot guarantee exact pixels and ask whether ratio-only output is acceptable.
