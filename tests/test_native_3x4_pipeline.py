#!/usr/bin/env python3
"""Ratio-only pipeline regression test for v0.8.10."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([PYTHON, *args], capture_output=True, text=True)


def main() -> int:
    preflight = run(str(ROOT / "scripts/runtime_preflight.py"), "--expected-version", "v0.8.10", "--requested-ratio", "3:4")
    if preflight.returncode != 0:
        print(preflight.stdout, preflight.stderr)
        return 1
    p = json.loads(preflight.stdout)
    if p["backend"] != "codex-$imagegen" or p["fixed_pixel_size_required"] is not False or p["requires_api_key"] is not False:
        return 1

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        src = td / "src"
        out = td / "out"
        src.mkdir()
        Image.new("RGB", (1086, 1448), "white").save(src / "p1.png")
        Image.new("RGB", (1536, 2048), "white").save(src / "p2.png")
        Image.new("RGB", (1024, 1536), "white").save(src / "bad.png")

        good = run(
            str(ROOT / "scripts/validate_native_3x4.py"),
            "--requested-ratio", "3:4", "--json", str(src / "p1.png"), str(src / "p2.png"),
        )
        if good.returncode != 0:
            print(good.stdout, good.stderr)
            return 1
        good_data = json.loads(good.stdout)
        if not good_data["all_passed"]:
            return 1

        bad = run(
            str(ROOT / "scripts/validate_native_3x4.py"),
            "--requested-ratio", "3:4", "--json", str(src / "bad.png"),
        )
        if bad.returncode == 0:
            return 1

        pages = []
        for index, source, final in [
            (1, "p1.png", "01-cover-test-topic.png"),
            (2, "p2.png", "02-content-test-topic.png"),
        ]:
            row = json.loads(run(
                str(ROOT / "scripts/validate_native_3x4.py"),
                "--json", str(src / source),
            ).stdout)["images"][0]
            pages.append({
                "page_id": f"P{index:02d}",
                "page_index": index,
                "source_file": source,
                "ordered_file_name": final,
                "status": "COMPLETE",
                "requested_ratio": "3:4",
                "actual_width": row["actual_width"],
                "actual_height": row["actual_height"],
                "ratio_passed": True,
                "sha256": row["sha256"],
                "service_dispatch_count": 1,
                "content_attempt_count": 1,
            })
        manifest = td / "manifest.json"
        manifest.write_text(json.dumps({
            "version": "v0.8.10",
            "validation_mode": "publish-3x4",
            "requested_ratio": "3:4",
            "fixed_pixel_size_required": False,
            "total_pages": 2,
            "generation_order": ["P01", "P02"],
            "delivery_order": ["P01", "P02"],
            "first_incomplete_page_id": None,
            "pages": pages,
        }), encoding="utf-8")

        progress = run(str(ROOT / "scripts/validate_series_progress.py"), str(manifest))
        if progress.returncode != 0:
            print(progress.stdout, progress.stderr)
            return 1

        final = run(
            str(ROOT / "scripts/finalize_series_files.py"),
            "--manifest", str(manifest),
            "--source-dir", str(src),
            "--output-dir", str(out),
            "--validation-mode", "publish-3x4",
            "--zip", str(td / "series.zip"),
        )
        if final.returncode != 0:
            print(final.stdout, final.stderr)
            return 1
        result = json.loads(final.stdout)
        if [f["ordered_file_name"] for f in result["files"]] != ["01-cover-test-topic.png", "02-content-test-topic.png"]:
            return 1

    print("ratio-only native 3:4 pipeline test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
