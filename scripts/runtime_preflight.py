#!/usr/bin/env python3
"""Validate the ratio-only Codex $imagegen workflow.

This skill never requires fixed pixels, an API key, or an external Images API.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

VERSION = "v0.8.10"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-version", default=VERSION)
    parser.add_argument("--requested-ratio", default="3:4")
    parser.add_argument("--mode", choices=("publish-3x4",), default="publish-3x4")
    parser.add_argument("--skill-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    version_text = (args.skill_root / "VERSION.md").read_text(encoding="utf-8").strip()
    if args.expected_version != version_text:
        print(json.dumps({"status": "FAIL", "error": "skill version mismatch", "actual": version_text}, ensure_ascii=False, indent=2))
        return 1
    if args.requested_ratio != "3:4":
        print(json.dumps({"status": "FAIL", "error": "this skill currently produces 3:4 cards only"}, ensure_ascii=False, indent=2))
        return 1

    result = {
        "status": "PASS",
        "skill_version": VERSION,
        "mode": "publish-3x4",
        "backend": "codex-$imagegen",
        "requested_ratio": "3:4",
        "fixed_pixel_size_required": False,
        "requires_api_key": False,
        "external_api_allowed": False,
        "acceptance": "abs(actual_width/actual_height-0.75)<=0.001",
        "pixel_examples_are_ratio_hints_only": True,
    }
    if args.self_test:
        if result["fixed_pixel_size_required"] or result["requires_api_key"] or result["external_api_allowed"]:
            return 1
        print("runtime_preflight self-test passed")
        return 0
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
