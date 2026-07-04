#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

SKILL_NAME = "xingchen-doodle-card-skill"
DISPLAY_NAME = "涂鸦卡片"
VERSION = "v0.4.2"
ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md", "README.md", "VERSION.md", "CHANGELOG.md", "RELEASE_REPORT.md", "agents/openai.yaml",
    "references/image-gen-text2im-contract.md", "references/aspect-ratio-lock.md", "references/chinese-text-in-image-rules.md", "references/prompt-budget.md", "references/validation-rules.md",
    "styles/chinese-doodle-editorial-style-lock.md", "templates/image-gen-card-prompt-template.md", "templates/image-series-output-template.md", "templates/image_prompt_template.md", "templates/compact-final-prompt-template.md",
    "tests/test_cases.json", "tests/style_checklist.md", "scripts/quick_validate.py",
]
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf"}

REQUIRED_KEYWORDS = [
    "image_gen.text2im", "Execution Lock", "Single Image Gen Authority", "Aspect Ratio Lock", "STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.",
    "native 3:4", "1080×1440", "1536×2048", "width / height = 0.75", "0.745", "0.755",
    "2:3", "4:5", "9:16", "A4", "long poster", "not a minor deviation", "Page-by-page verification",
    "A hand-drawn doodle editorial illustration.",
    "Style: minimalist ink doodle, imperfect sketch lines, soft pastel accents, large white negative space.",
    "Composition: exact 3:4 portrait card", "Chinese text integrated into image:", "Title:", "Subtitle:", "Optional points:",
    "Mood: calm, warm, educational, reflective.", "any external text rendering", "post-processing typography layers",
    "PIL/Canvas/SVG/HTML rendering", "CSS text systems", "multi-stage composition pipeline", "fallback renderer",
]
FORBIDDEN_IMPORT_PATTERNS = [r"from\s+PIL\s+import", r"import\s+PIL", r"import\s+canvas", r"from\s+canvas\s+import", r"import\s+cairo", r"from\s+cairo\s+import"]
errors=[]

if ROOT.name != SKILL_NAME:
    errors.append(f"Root directory name should be {SKILL_NAME}, got {ROOT.name}")

for rel in REQUIRED_FILES:
    if not (ROOT/rel).exists():
        errors.append(f"Missing file: {rel}")

for rel in ["SKILL.md", "README.md", "VERSION.md", "agents/openai.yaml"]:
    p=ROOT/rel
    if p.exists() and DISPLAY_NAME not in p.read_text(encoding="utf-8"):
        errors.append(f"{rel} missing display name: {DISPLAY_NAME}")

for p in ROOT.rglob('*'):
    if not p.is_file():
        continue
    rel=str(p.relative_to(ROOT))
    if any(part in {'.git','__MACOSX','__pycache__'} for part in p.parts):
        continue
    if p.suffix.lower() in BINARY_SUFFIXES:
        continue
    try:
        txt=p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        errors.append(f"File is not UTF-8: {rel}")
        continue
    if p.suffix in {'.py','.js','.ts','.mjs'}:
        for pat in FORBIDDEN_IMPORT_PATTERNS:
            if re.search(pat, txt):
                errors.append(f"Forbidden local rendering import in {rel}: {pat}")

for rel in ["SKILL.md","README.md","VERSION.md","CHANGELOG.md","RELEASE_REPORT.md"]:
    p=ROOT/rel
    if p.exists() and VERSION not in p.read_text(encoding='utf-8'):
        errors.append(f"{rel} missing version {VERSION}")

for rel in ["SKILL.md","README.md","templates/image-gen-card-prompt-template.md","templates/image_prompt_template.md","templates/compact-final-prompt-template.md","references/image-gen-text2im-contract.md","references/aspect-ratio-lock.md","styles/chinese-doodle-editorial-style-lock.md"]:
    p=ROOT/rel
    if p.exists():
        txt=p.read_text(encoding='utf-8')
        for kw in REQUIRED_KEYWORDS:
            if kw not in txt:
                errors.append(f"{rel} missing required v0.4.2 keyword: {kw}")

for rel in ["examples/example_01_sleep.md","examples/example_02_reading.md","examples/example_03_ai_anxiety.md","examples/example_04_rainy_day.md","examples/example_05_work_life.md"]:
    p=ROOT/rel
    if p.exists():
        txt=p.read_text(encoding='utf-8')
        for kw in ["STRICT EXACT 3:4 PORTRAIT IMAGE ONLY.", "1080×1440", "2:3", "4:5", "9:16", "是否实际比例为 3:4：是"]:
            if kw not in txt:
                errors.append(f"{rel} missing example keyword: {kw}")

json_path=ROOT/'tests/test_cases.json'
if json_path.exists():
    try:
        data=json.loads(json_path.read_text(encoding='utf-8'))
        if not isinstance(data, list) or len(data)<8:
            errors.append('tests/test_cases.json must contain at least 8 cases')
    except Exception as e:
        errors.append(f'tests/test_cases.json invalid: {e}')

if errors:
    print('Validation failed:')
    for e in errors:
        print('-', e)
    sys.exit(1)
print(f"Validation passed for {SKILL_NAME} {VERSION}")
