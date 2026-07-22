# Viewpoint Visibility Rules — v0.8.10

This reference defines the Viewpoint Visibility Rule, Prop Text Visibility Lock, and Readable Surface Perspective Guard for Xiaohongshu 3:4 hand-drawn doodle cards.

## Core rule

Readable text on a prop must match real-world orientation. If the character is reading the prop and the prop faces the character, the viewer cannot also read the prop’s full front-facing body text from a side, three-quarter, or unclear angle.

## Three prop roles

### self-reading prop

The character reads the object privately. The object can be paper, book, notebook, phone, tablet, computer screen, card, manual, sign, or similar.

Allowed:

- blank / near blank surface
- symbolic strokes
- partial marks
- illegible tiny lines
- soft screen glow without readable paragraphs

Not allowed:

- full body text clearly readable by viewer
- phone or tablet screen readable from side angle
- book or notebook text perfectly facing viewer while character looks down

### viewer-facing presentation prop

The character intentionally shows the prop to the viewer.

Allowed:

- clear readable approved text
- medium/high text density if front-facing and large enough

Required:

- front-facing surface
- action/gaze supports presentation
- no contradiction between viewer camera angle and prop surface

### background prop

The prop decorates the scene and does not carry required information.

Allowed:

- symbolic_only
- illegible
- blank
- minimal decorative marks

## Readability handling

If text is required for user comprehension, it must be placed in the independent card text area unless the prop is explicitly viewer-facing presentation.

The prompt_composer must never use a self-reading paper, book, phone, tablet, notebook, or screen as the main body text carrier.

## Failure modes

- person reads a paper angled toward themselves, but the viewer sees a full paragraph on the paper
- person looks at a phone, but the viewer can read the full screen from three-quarter side view
- person looks down at a notebook, but the notebook text is perfectly upright to the viewer
- scene says self-reading, prompt says clear readable prop text
- prop orientation is unclear but prompt demands clear readable text

## Repair choices

1. Downgrade prop text to symbolic_only / illegible / blank.
2. Move real information to title/subtitle/bullets.
3. Change prop role to viewer_presentation with a front-facing display.
4. Use partial over-shoulder readability only when the camera relation supports it.
5. Remove the prop if repeated conflicts remain.

## Acceptance

A v0.8.10 prompt passes only if:

- every text-bearing prop has a prop_role
- character gaze and prop orientation do not conflict
- self-reading props never carry full readable body text
- viewer-facing presentation props are clearly front-facing
- background props do not carry required facts
- the required page message remains in approved_page_text unless presentation is explicit
