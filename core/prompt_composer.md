# prompt_composer — v0.8.10

Purpose: compile one complete image-model prompt for the current authorized page without changing approved text, evidence, page order, series style or filename.

## Required inputs

- `approved_page_text`
- `page_id`, `page_index`, `recommended_total_pages`, `page_role`
- planned `ordered_file_name`
- `series_style_manifest.verbatim_style_block`
- `series_anchor_selector` candidate plan
- `sequential_generation_controller` result
- current available reference state: manifest-only, approved P01, or approved secondary anchor
- `layout_graph`
- `prop_visibility_plan`
- repeated icon/chart dictionary entries used on this page
- selected ratio mode and approved native backend decision

Do not run if content fidelity, viewpoint visibility, style manifest, sequential authorization, page count or filename planning has failed.

## Required prompt structure

```text
OUTPUT FILE NAME: {ordered_file_name}
PAGE: {page_index}/{recommended_total_pages}
ROLE: {page_role}
GENERATION ORDER LOCK: This is the current first incomplete page. Do not generate any other page.

Create one complete 3:4 portrait Xiaohongshu doodle editorial card in a single native image-model content attempt. In default publish mode, use Codex `$imagegen` and require a true 3:4 canvas without promising fixed pixels. Never call 1024x1536 a 3:4 canvas; it is 2:3. Keep a continuous background to all four edges and keep critical text inside the outer 7% safe margin.

APPROVED CHINESE TEXT — reproduce accurately, do not add claims:
{approved_page_text}

SERIES STYLE LOCK — COPY EXACTLY, DO NOT PARAPHRASE:
{verbatim_style_block}

VISUAL REFERENCE STATE:
{reference_state}
For P01, use the immutable manifest only. For later pages, use only already approved earlier pages as references. Never generate or reference a later page early. Reference images control Chinese character skeleton, stroke thickness, rounded terminals, numeral forms, title/body weight relationship, line weight, palette, icon grammar, chart grammar and component shapes. Do not copy reference-page content.

REUSED COMPONENTS ON THIS PAGE:
{canonical_icon_and_chart_descriptions}
Use these exact descriptions. Do not redesign repeated icons or charts.

MAIN SUBJECT AND ACTION:
{content_adaptive_subject}
{one_simple_action}
Use one main subject, one main action and at most 1–2 interaction objects unless the approved content requires otherwise. Do not default every page to a young Chinese woman.

COMPOSITION:
{layout_graph_for_page}
Keep text hierarchy and visual rhythm compatible with the immutable manifest and approved earlier pages while allowing a content-appropriate layout.

PROP TEXT VISIBILITY:
{prop_visibility_plan}
Self-reading props may show only partial, symbolic, illegible or blank text. Only viewer-presentation props may show clear approved text.

TYPOGRAPHY CONSISTENCY HARD RULE:
Use the exact same Chinese visual family as the manifest and approved earlier pages. Cover/page/body levels may differ only in size and weight. Match upright character skeleton, stroke terminals, numeral shapes, punctuation, line spacing and density. Do not switch to brush calligraphy, printed serif/song type, thin script, outlined bubble lettering or a second handwriting family.

ICON AND CHART CONSISTENCY HARD RULE:
Use one stable medium soft-black outline, rounded joins, flat 2D perspective, low-saturation pastel fills and one simple editorial detail band. Match approved earlier pages' chart axes, arrowheads, series colors, labels and markers. No emoji, clip art, gradients, dashboard vector style, 3D or photorealism.

CONTENT FIDELITY:
Use only approved_page_text. Add no new numbers, units, dates, studies, outcomes, certainty, English facts or medical claims.

STRUCTURE:
No extra limbs, disconnected hands, duplicated objects, impossible grip, severe occlusion or text outside the canvas.

ONE-PASS CONTENT RULE:
Generate illustration and Chinese text together with `$imagegen`. No local typography, overlay, redraw, crop, resize, multi-image compositing or fallback renderer. In publish mode the returned image must already have a true 3:4 ratio; in strict mode it must also match the requested pixels. No ratio repair or pixel post-processing is allowed.
```

## Hard locks

```text
prompt plan count = recommended_total_pages
only the current first incomplete page may be dispatched
one prompt = one planned ordered_file_name
verbatim_style_block must match byte-for-byte across prompts
only already approved earlier images may be used as references
repeated icon/chart descriptions must match canonical dictionary entries
prompt_composer may not create, remove, merge, skip or reorder pages
```
