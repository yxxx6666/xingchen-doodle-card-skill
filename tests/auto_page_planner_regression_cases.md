# Auto Page Planner Regression Cases v0.8.0

## Case 1: “封面页加内容页” is not 2 pages

Input instruction: “封面页加内容页”
Content: long health/science article with multiple studies, multiple numbers, mechanisms, and action tips.

Expected:

- has_explicit_page_count = false
- recommended_total_pages >= 5
- split_required = true
- page_role_plan length = recommended_total_pages

Must avoid:

- interpreting “封面页加内容页” as exactly 2 pages
- compressing multiple studies into one content page

## Case 2: explicit 2 pages

Input instruction: “只做2页极简版”

Expected:

- has_explicit_page_count = true
- explicit_total_pages = 2
- if content_density = high, under_page_count_risk = true and status = WARNING

## Case 3: output file names

Expected output file names:

- 01-cover-topic.png
- 02-content-topic.png
- 03-content-topic.png

named_file_count must equal recommended_total_pages.
