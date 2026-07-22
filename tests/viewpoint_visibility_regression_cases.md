# Viewpoint Visibility Regression Cases — v0.8.10

These cases verify Viewpoint Visibility Rule, Prop Text Visibility Lock, and Readable Surface Perspective Guard.

| Case | Input visual idea | Expected role | Expected text visibility | Expected gate behavior |
|---|---|---|---|---|
| A01 self-reading paper | Young woman reads a paper angled toward herself | self_reading | symbolic_only / illegible / blank | PASS only if no full readable body text on paper |
| A02 impossible paper readability | Young woman reads paper facing herself, viewer can read all body text | self_reading | clear_readable | FAIL → BLOCK image_gen → repair |
| B01 self-reading phone | Young woman looks at phone screen from side view | self_reading | symbolic_only / illegible / screen glow | PASS |
| B02 impossible phone readability | Side-view phone screen contains full readable paragraph | self_reading | clear_readable | FAIL → BLOCK image_gen → repair |
| C01 notebook top-down | Young woman looks down at notebook | self_reading | partial / symbolic_only | PASS |
| C02 viewer-facing card | Character presents a card to viewer | viewer_presentation | clear_readable allowed | PASS if front-facing |
| C03 background book | Book lies on desk as decoration | background_prop | symbolic_only / blank | PASS |
| C04 unclear orientation | Prop orientation unclear but prompt requires clear readable text | unclear | clear_readable | WARNING or FAIL → clarify role |
| C05 over-shoulder partial | Viewer sees over character shoulder while character reads | self_reading | partial only | WARNING allowed if not full body text |
| C06 required text on prop | User comprehension depends on self-reading prop text | self_reading | clear_readable requested | FAIL → move text to independent card text area |

## Required assertions

- `viewpoint_visibility_status = FAIL` blocks formal image generation.
- `readability_misuse_detected = true` whenever self_reading + not viewer_facing + clear_readable appears.
- `requires_prompt_constraint = true` whenever a text-bearing prop appears in the layout graph.
- `prompt_composer` must explicitly state the prop text visibility handling for self-reading, viewer_presentation, and background_prop.
- `structure_scorer` must penalize viewpoint conflicts even when anatomy is correct.
- `runtime_simulator` must predict impossible readable surface perspective before generation.
- `execution_trace` must record prop_visibility_plan and visibility_conflicts.

## Negative prompt examples

- Do not show full readable body text on paper when the character is reading it privately.
- Do not make a side-view phone screen readable like a front-facing sign.
- Do not place the card’s main bullet text on a notebook page that faces the character.

## Positive prompt examples

- The character quietly reads a paper angled toward themselves; the paper surface has only tiny symbolic unreadable marks; all readable Chinese content is in the independent card text area.
- The character presents a front-facing card toward the viewer; only approved_page_text appears on that viewer-facing card.

## Module assertion

These cases must be evaluated by `viewpoint_visibility_guard` and must produce a `prop_visibility_plan` containing `self_reading`, `viewer_presentation`, and `background_prop` decisions when relevant.
