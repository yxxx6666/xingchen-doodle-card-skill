#!/usr/bin/env python3
"""Read-only native 3:4 validation for Codex $imagegen outputs.

Any native pixel dimensions are accepted when the actual ratio is 3:4.
No exact pixel comparison is performed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

TOLERANCE = 0.001


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_image(
    path: Path,
    mode: str = "publish-3x4",
    requested_ratio: str = "3:4",
    **_ignored: Any,
) -> dict[str, Any]:
    if mode != "publish-3x4":
        raise ValueError("fixed-pixel validation modes are not supported")
    if requested_ratio != "3:4":
        raise ValueError("this validator accepts requested_ratio=3:4 only")
    with Image.open(path) as image:
        width, height = image.size
        image.verify()
    if height <= 0:
        raise ValueError("invalid image height")
    ratio = width / height
    ratio_passed = abs(ratio - 0.75) <= TOLERANCE
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "file": str(path),
        "validation_mode": "publish-3x4",
        "requested_ratio": requested_ratio,
        "fixed_pixel_size_required": False,
        "actual_width": width,
        "actual_height": height,
        "actual_ratio": round(ratio, 9),
        "ratio_passed": ratio_passed,
        "passed": ratio_passed,
        "sha256": sha256_file(path),
    }


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def self_test() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        cases = {
            "codex-native.png": ((1086, 1448), True),
            "standard.png": ((1080, 1440), True),
            "large.png": ((1536, 2048), True),
            "small.png": ((768, 1024), True),
            "bad.png": ((1024, 1536), False),
        }
        for name, (size, expected) in cases.items():
            path = root / name
            Image.new("RGB", size, "white").save(path)
            if inspect_image(path)["passed"] is not expected:
                return 1
    print("validate_native_3x4 self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="*")
    parser.add_argument("--mode", choices=("publish-3x4",), default="publish-3x4")
    parser.add_argument("--requested-ratio", default="3:4")
    parser.add_argument("--log-jsonl", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.images:
        parser.error("at least one image is required")
    try:
        rows = [inspect_image(Path(image), args.mode, args.requested_ratio) for image in args.images]
        if args.log_jsonl:
            for row in rows:
                append_jsonl(args.log_jsonl, row)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    payload = {"images": rows, "all_passed": all(row["passed"] for row in rows)}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print(
                f"{'PASS' if row['passed'] else 'FAIL'} | {row['file']} | "
                f"actual={row['actual_width']}x{row['actual_height']} | ratio={row['actual_ratio']} | sha256={row['sha256']}"
            )
    return 0 if payload["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
