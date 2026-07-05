# Failure Modes and Fixes

## 1. Image feels too full

Symptoms:
- too many objects
- background has many details
- no obvious white area

Fix:
- reduce props to 3-4
- use C01, C02, or C03
- explicitly say: large clean white negative space on the opposite side

## 2. Character is too large or poster-like

Symptoms:
- person fills most of the frame
- looks like a cover model
- composition feels like a poster

Fix:
- place character in a lower corner or one side
- make character small-to-medium scale
- keep opposite side empty

## 3. Looks like anime or manga

Symptoms:
- large shiny eyes
- stylized hair rendering
- dramatic expression
- Japanese/Korean comic feeling

Fix:
- strengthen: clean black ink outline, minimal facial features, restrained doodle character
- add negative: anime style, manga style, Korean comic style, glossy character rendering

## 4. Looks like watercolor

Symptoms:
- soft wash texture
- painterly background
- bleeding colors

Fix:
- strengthen: clean black ink outlines, flat 2D, minimal line art
- add negative: watercolor painting, painterly texture, paper wash

## 5. Looks cinematic or commercial

Symptoms:
- dramatic lighting
- depth of field
- luxury poster mood
- strong shadows

Fix:
- strengthen: flat 2D composition, eye-level view, no dramatic shadows
- add negative: cinematic rendering, realistic lighting, luxury poster design

## 6. Text becomes the main focus

Symptoms:
- English note too large
- looks like a title
- typography dominates the image

Fix:
- say: tiny decorative English note, not the main focus
- no Chinese text
- no large typography

## 7. Props are too complex

Symptoms:
- desk overloaded
- too many icons
- UI screens appear

Fix:
- limit props to 3-6
- remove anything not directly related to the theme
- avoid complex UI and detailed background

## 8. Style becomes childish or low-quality

Symptoms:
- rough child drawing
- over-cute stickers
- messy linework

Fix:
- strengthen: minimalist editorial infographic illustration, clean black ink outline, cute but restrained
- add negative: rough low-quality child drawing, excessive ornament, overly cute decoration

## Output repair rule

When a failure is detected, revise the prompt before generating again.
Do not solve style failures by adding more decorative elements.
Solve them by simplifying.

## v0.5.0 Structure Stability Repair

This is not a feature expansion. It strengthens structure safety for image_gen doodle card prompts.

New priority system:

```text
结构正确性 > 可读性 > 美观 > 丰富度
```

New pipeline layers:

1. anatomy constraints layer
2. scene complexity limiter
3. pose safety layer
4. prompt repair loop
5. mandatory STRUCTURE SAFETY BLOCK in final prompts

Core goal: reduce three hands / three feet / disconnected limbs / hands growing from wrong places / multi-action collapse / scene overload distortion.

The v0.4.2 Execution Lock remains unchanged: the only legal renderer is `image_gen.text2im`. No PIL, Canvas, SVG, HTML, fallback renderer, or post-processing typography layer is allowed.
