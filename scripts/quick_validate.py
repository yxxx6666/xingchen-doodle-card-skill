#!/usr/bin/env python3
"""Validate the v0.8.10 ratio-only Codex imagegen skill."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v0.8.10"
REQUIRED = [
    "SKILL.md", "README.md", "VERSION.md", "CHANGELOG.md", "RELEASE_REPORT.md", "agents/openai.yaml",
    "core/auto_page_planner.md", "core/page_content_allocator.md", "core/content_fidelity_guard.md",
    "core/series_style_manifest.md", "core/series_consistency_gate.md", "core/sequential_generation_controller.md",
    "core/timeout_recovery_controller.md", "core/aspect_ratio_gate.md", "core/output_file_namer.md",
    "references/typography-consistency-rules.md", "references/icon-consistency-rules.md",
    "references/chart-consistency-rules.md", "references/aspect-ratio-lock.md",
    "references/native-image-backend-contract.md", "references/image-gen-text2im-contract.md",
    "references/validation-rules.md", "templates/series-progress-manifest-template.md",
    "templates/image-gen-card-prompt-template.md", "templates/compact-timeout-retry-prompt-template.md",
    "scripts/runtime_preflight.py", "scripts/validate_native_3x4.py", "scripts/finalize_series_files.py",
    "scripts/validate_series_progress.py", "scripts/series_progress_controller.py",
    "tests/test_native_3x4_pipeline.py",
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing file: {rel}")
    for obsolete in ["scripts/enforce_3x4.py", "scripts/generate_native_3x4.py", "tests/mock_image_api_server.py"]:
        if (ROOT / obsolete).exists():
            errors.append(f"obsolete file must not exist: {obsolete}")
    for rel in ("SKILL.md", "README.md", "VERSION.md", "RELEASE_REPORT.md", "agents/openai.yaml"):
        if VERSION not in (ROOT / rel).read_text(encoding="utf-8"):
            errors.append(f"{rel} missing {VERSION}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if len(skill.splitlines()) > 500:
        errors.append("SKILL.md must remain below 500 lines")
    required_links = [
        "core/auto_page_planner.md", "core/page_content_allocator.md", "core/series_style_manifest.md",
        "core/sequential_generation_controller.md", "core/timeout_recovery_controller.md",
        "core/aspect_ratio_gate.md", "core/output_file_namer.md", "core/prompt_composer.md",
        "references/typography-consistency-rules.md", "references/icon-consistency-rules.md",
        "references/chart-consistency-rules.md", "references/aspect-ratio-lock.md",
        "references/native-image-backend-contract.md", "references/image-gen-text2im-contract.md",
        "templates/image-gen-card-prompt-template.md", "templates/series-progress-manifest-template.md",
    ]
    for rel in required_links:
        if f"]({rel})" not in skill:
            errors.append(f"SKILL.md missing direct link: {rel}")

    required_phrases = [
        "只认比例，不认固定像素", "Codex 自带的 `$imagegen`", "1086×1448", "1024×1536",
        "不得切换外部 API", "PAUSED_TIMEOUT", "每次请求最多携带一张",
    ]
    for phrase in required_phrases:
        if phrase not in skill:
            errors.append(f"SKILL.md missing ratio-only rule: {phrase}")

    active_roots = [ROOT / "SKILL.md", ROOT / "core", ROOT / "references", ROOT / "scripts", ROOT / "templates", ROOT / "agents", ROOT / "tests"]
    forbidden = ["strict" + "-size", "generate_native" + "_3x4"]
    for target in active_roots:
        paths = [target] if target.is_file() else [p for p in target.rglob("*") if p.is_file()]
        paths = [p for p in paths if p.name != "quick_validate.py"]
        for path in paths:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for token in forbidden:
                if token in text:
                    errors.append(f"forbidden fixed-pixel token in {path.relative_to(ROOT)}: {token}")

    production_scripts = [ROOT / "scripts/finalize_series_files.py", ROOT / "scripts/validate_native_3x4.py"]
    for path in production_scripts:
        text = path.read_text(encoding="utf-8")
        for operation in [".crop(", ".resize(", ".paste(", "ImageDraw", "draw.text", "ImageFont"]:
            if operation in text:
                errors.append(f"forbidden production pixel operation in {path.name}: {operation}")

    commands = [
        [sys.executable, str(ROOT / "scripts/runtime_preflight.py"), "--self-test"],
        [sys.executable, str(ROOT / "scripts/validate_native_3x4.py"), "--self-test"],
        [sys.executable, str(ROOT / "scripts/finalize_series_files.py"), "--self-test"],
        [sys.executable, str(ROOT / "scripts/validate_series_progress.py"), "--self-test"],
        [sys.executable, str(ROOT / "scripts/series_progress_controller.py"), "self-test"],
        [sys.executable, str(ROOT / "tests/test_native_3x4_pipeline.py")],
    ]
    test_results = []
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        test_results.append({"command": command[-1], "returncode": result.returncode, "stdout": result.stdout.strip()})
        if result.returncode != 0:
            errors.append(f"test failed: {' '.join(command)}\n{result.stdout}\n{result.stderr}")

    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors, "tests": test_results}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({
        "status": "PASS",
        "version": VERSION,
        "file_count": sum(1 for p in ROOT.rglob("*") if p.is_file()),
        "tests": test_results,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
