#!/usr/bin/env python3
"""Validate cover-first progress metadata for ratio-only 3:4 generation."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

VERSION = "v0.8.10"
ALLOWED_STATUSES = {
    "PLANNED", "WAITING_IMAGEGEN", "SERVICE_TIMEOUT", "PAUSED_TIMEOUT", "GENERATED",
    "RATIO_FAILED", "RATIO_PASS", "CONSISTENCY_PASS", "CONTENT_FAILED", "COMPLETE",
}
FINAL_STATUS = "COMPLETE"


def validate_manifest(data: dict) -> tuple[list[str], str | None]:
    errors: list[str] = []
    if data.get("version") != VERSION:
        errors.append(f"version must be {VERSION}")
    mode = data.get("validation_mode") or "publish-3x4"
    if mode != "publish-3x4":
        errors.append("validation_mode must be publish-3x4")
    if data.get("requested_ratio") != "3:4":
        errors.append("requested_ratio must be 3:4")
    if data.get("fixed_pixel_size_required") not in (None, False):
        errors.append("fixed_pixel_size_required must be false")
    if data.get("requested_size") not in (None, ""):
        errors.append("requested_size must not be used")
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        return errors + ["pages must be a non-empty list"], None
    total = data.get("total_pages")
    if total != len(pages):
        errors.append("total_pages must equal pages length")
    expected_order = [f"P{i:02d}" for i in range(1, len(pages) + 1)]
    if data.get("generation_order") != expected_order:
        errors.append("generation_order must be P01,P02,...")
    if data.get("delivery_order") != expected_order:
        errors.append("delivery_order must be P01,P02,...")

    first_incomplete: str | None = None
    seen_incomplete = False
    for index, page in enumerate(pages, start=1):
        page_id = f"P{index:02d}"
        status = page.get("status")
        if page.get("page_id") != page_id or page.get("page_index") != index:
            errors.append(f"{page_id} id/index mismatch")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{page_id} invalid status: {status}")
        filename = page.get("ordered_file_name", "")
        if not re.match(rf"^{index:02d}-(cover|content|action|summary|closing)-.+\.png$", filename):
            errors.append(f"{page_id} ordered_file_name invalid")
        if status != FINAL_STATUS and first_incomplete is None:
            first_incomplete = page_id
            seen_incomplete = True
        elif seen_incomplete and status != "PLANNED":
            errors.append(f"{page_id} progressed while an earlier page is incomplete")
        if not isinstance(page.get("service_dispatch_count", 0), int) or not 0 <= page.get("service_dispatch_count", 0) <= 4:
            errors.append(f"{page_id} service_dispatch_count must be 0..4")
        if not isinstance(page.get("content_attempt_count", 0), int) or not 0 <= page.get("content_attempt_count", 0) <= 3:
            errors.append(f"{page_id} content_attempt_count must be 0..3")
        if page.get("requested_size") not in (None, ""):
            errors.append(f"{page_id} requested_size must not be used")
        if page.get("exact_size_passed") not in (None, ""):
            errors.append(f"{page_id} exact_size_passed must not be used")
        if status == FINAL_STATUS:
            width, height = page.get("actual_width"), page.get("actual_height")
            if not isinstance(width, int) or not isinstance(height, int) or height <= 0:
                errors.append(f"{page_id} actual dimensions required")
            elif abs(width / height - 0.75) > 0.001:
                errors.append(f"{page_id} actual ratio must be 3:4")
            if page.get("ratio_passed") is not True:
                errors.append(f"{page_id} ratio_passed=true required")
            if not isinstance(page.get("sha256"), str) or len(page.get("sha256", "")) != 64:
                errors.append(f"{page_id} sha256 required")
    if data.get("first_incomplete_page_id") != first_incomplete:
        errors.append(f"first_incomplete_page_id must be {first_incomplete!r}")
    return errors, first_incomplete


def self_test() -> int:
    base = {
        "version": VERSION,
        "validation_mode": "publish-3x4",
        "requested_ratio": "3:4",
        "fixed_pixel_size_required": False,
        "total_pages": 2,
        "generation_order": ["P01", "P02"],
        "delivery_order": ["P01", "P02"],
        "first_incomplete_page_id": "P02",
        "pages": [
            {"page_id": "P01", "page_index": 1, "ordered_file_name": "01-cover-test.png", "status": "COMPLETE", "service_dispatch_count": 1, "content_attempt_count": 1, "actual_width": 1086, "actual_height": 1448, "ratio_passed": True, "sha256": "a" * 64},
            {"page_id": "P02", "page_index": 2, "ordered_file_name": "02-content-test.png", "status": "PLANNED", "service_dispatch_count": 0, "content_attempt_count": 0},
        ],
    }
    errors, first = validate_manifest(base)
    if errors or first != "P02":
        return 1
    base["pages"][0]["actual_width"] = 1024
    base["pages"][0]["actual_height"] = 1536
    errors, _ = validate_manifest(base)
    if not errors:
        return 1
    print("validate_series_progress self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.manifest:
        parser.error("manifest is required")
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        errors, first = validate_manifest(data)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    result = {"status": "PASS" if not errors else "FAIL", "first_incomplete_page_id": first, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
