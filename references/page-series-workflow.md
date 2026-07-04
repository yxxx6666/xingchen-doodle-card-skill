# Page Series Workflow

## Purpose

Convert a pasted Chinese content block into a cover plus content-page image prompt series.

Each page is a complete image_gen prompt.
No local rendering or post-processing is allowed.

## Workflow

### 1. Content distillation

Read the pasted content and extract:

- central topic
- main conflict or insight
- 3–6 key points
- emotional direction
- audience-facing value

### 2. Page count decision

Use `references/page-count-rules.md`.
Default: 1 cover + 3–6 content pages.

### 3. Page planning

Create a page list:

```text
01 Cover — central promise / core insight
02 Content — point 1
03 Content — point 2
04 Content — point 3
...
```

### 4. Per-page text compression

For every page, create:

- Chinese title
- Chinese body text

Both must be short enough for image_gen.

### 5. Per-page visual design

For every page, choose:

- scene
- young Chinese woman action anchor
- props
- composition pattern
- text placement area
- optional English note

### 6. Per-page prompt writing

Every prompt must contain:

A. Visual description  
B. Composition description  
C. Chinese title  
D. Chinese body text  
E. image_gen-only clause  
F. avoid list

### 7. Closed-loop self-check

Before final answer, verify:

- no local rendering method is suggested
- no text overlay workflow is suggested
- title and body are included verbatim in each page prompt
- illustration and text are generated in the same image_gen pass
