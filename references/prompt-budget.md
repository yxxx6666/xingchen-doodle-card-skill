# Prompt Budget v0.8.10

Keep each page prompt explicit but compact. Prioritize filename, exact approved Chinese text, 3:4 request, layout, one main subject/action, style lock, and concise negative constraints.

## Timeout prevention

- Attach at most one approved reference image to a `$imagegen` request.
- Use the textual `verbatim_style_block` for all other series consistency information.
- Do not repeat the same constraints multiple times beyond the opening and final 3:4 reminder.
- Avoid long workflow explanations inside the image prompt.
- Split dense content during planning instead of overloading a page.

## Retry prompt

After one service timeout, use the compact retry template. Preserve exact Chinese text, facts, filename, layout intent and style lock. Remove only nonessential decoration and duplicated prose. A timeout retry must not silently drop required content.
