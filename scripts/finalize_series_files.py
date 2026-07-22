#!/usr/bin/env python3
"""Revalidate, order, copy/move and zip a 3:4 image series without editing pixels."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from PIL import Image

from validate_native_3x4 import inspect_image

SAFE_NAME = re.compile(r"^(\d{2})-(cover|content|action|closing|summary)-[a-z0-9]+(?:-[a-z0-9]+)*\.(png|jpg|jpeg|webp)$", re.I)


def load_entries(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    if (data.get("validation_mode") or "publish-3x4") != "publish-3x4":
        raise ValueError("only publish-3x4 ratio validation is supported")
    if data.get("fixed_pixel_size_required") not in (None, False):
        raise ValueError("fixed pixel size must not be required")
    entries = data.get("pages") or data.get("files")
    if not isinstance(entries, list) or not entries:
        raise ValueError("manifest must contain a non-empty pages or files list")
    return data, entries


def validate_entries(entries: list[dict[str, Any]], source_dir: Path) -> list[dict[str, Any]]:
    validated: list[dict[str, Any]] = []
    names: list[str] = []
    sources: list[str] = []
    for index, item in enumerate(entries, start=1):
        name = item.get("ordered_file_name") or item.get("final_name")
        source = item.get("source_file")
        if not isinstance(name, str) or not isinstance(source, str):
            raise ValueError("entry missing ordered_file_name or source_file")
        match = SAFE_NAME.fullmatch(name)
        if not match:
            raise ValueError(f"unsafe or invalid ordered_file_name: {name}")
        if int(match.group(1)) != index:
            raise ValueError(f"prefix sequence error: expected {index:02d}, got {match.group(1)}")
        if index == 1 and "-cover-" not in name.lower():
            raise ValueError("first file must be cover")
        if item.get("status") not in (None, "COMPLETE"):
            raise ValueError(f"{item.get('page_id', index)} is not COMPLETE")
        path = source_dir / source
        if not path.is_file():
            raise FileNotFoundError(f"source file not found: {path}")
        actual = inspect_image(path, requested_ratio=item.get("requested_ratio", "3:4"))
        if not actual["passed"]:
            raise ValueError(
                f"3:4 validation failed for {source}: {actual['actual_width']}x{actual['actual_height']} "
                f"ratio={actual['actual_ratio']}"
            )
        if item.get("sha256") and item["sha256"] != actual["sha256"]:
            raise ValueError(f"sha256 mismatch for {source}")
        if item.get("actual_width") is not None and item["actual_width"] != actual["actual_width"]:
            raise ValueError(f"recorded width mismatch for {source}")
        if item.get("actual_height") is not None and item["actual_height"] != actual["actual_height"]:
            raise ValueError(f"recorded height mismatch for {source}")
        names.append(name.lower())
        sources.append(source)
        validated.append({
            "page_id": item.get("page_id", f"P{index:02d}"),
            "source_file": source,
            "ordered_file_name": name,
            "source_path": str(path),
            **actual,
        })
    if len(set(names)) != len(names):
        raise ValueError("duplicate ordered_file_name values")
    if len(set(sources)) != len(sources):
        raise ValueError("duplicate source_file values")
    return validated


def finalize(
    manifest: Path,
    source_dir: Path,
    output_dir: Path,
    file_mode: str,
    zip_path: Path | None,
) -> dict[str, Any]:
    _, entries = load_entries(manifest)
    validated = validate_entries(entries, source_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    finalized = []
    for item in validated:
        source = Path(item["source_path"])
        target = output_dir / item["ordered_file_name"]
        target.unlink(missing_ok=True)
        if file_mode == "move":
            shutil.move(str(source), str(target))
        else:
            shutil.copy2(source, target)
        target_check = inspect_image(target, requested_ratio="3:4")
        if not target_check["passed"] or target_check["sha256"] != item["sha256"]:
            target.unlink(missing_ok=True)
            raise RuntimeError(f"destination revalidation failed for {target.name}")
        finalized.append({
            "page_id": item["page_id"],
            "ordered_file_name": target.name,
            "path": str(target),
            "actual_width": target_check["actual_width"],
            "actual_height": target_check["actual_height"],
            "actual_ratio": target_check["actual_ratio"],
            "sha256": target_check["sha256"],
        })
    if zip_path:
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        zip_path.unlink(missing_ok=True)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for item in finalized:
                archive.write(item["path"], arcname=item["ordered_file_name"])
        with zipfile.ZipFile(zip_path, "r") as archive:
            expected_names = [item["ordered_file_name"] for item in finalized]
            if archive.namelist() != expected_names:
                raise RuntimeError("ZIP order verification failed")
    return {
        "status": "PASS",
        "validation_mode": "publish-3x4",
        "fixed_pixel_size_required": False,
        "files": finalized,
        "zip": str(zip_path) if zip_path else None,
    }


def self_test() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        src = root / "src"
        out = root / "out"
        src.mkdir()
        Image.new("RGB", (1086, 1448), "white").save(src / "a.png")
        Image.new("RGB", (1536, 2048), "white").save(src / "b.png")
        rows = []
        for page_id, source, final in [
            ("P01", "a.png", "01-cover-test.png"),
            ("P02", "b.png", "02-content-test.png"),
        ]:
            check = inspect_image(src / source)
            rows.append({
                "page_id": page_id,
                "source_file": source,
                "ordered_file_name": final,
                "status": "COMPLETE",
                "requested_ratio": "3:4",
                "actual_width": check["actual_width"],
                "actual_height": check["actual_height"],
                "sha256": check["sha256"],
            })
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps({"validation_mode": "publish-3x4", "fixed_pixel_size_required": False, "pages": rows}), encoding="utf-8")
        result = finalize(manifest, src, out, "copy", root / "series.zip")
        if len(result["files"]) != 2:
            return 1
        bad = root / "bad"
        bad.mkdir()
        Image.new("RGB", (1024, 1536), "white").save(bad / "a.png")
        Image.new("RGB", (1080, 1440), "white").save(bad / "b.png")
        try:
            validate_entries(rows, bad)
            return 1
        except ValueError:
            pass
    print("finalize_series_files self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--source-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--validation-mode", choices=("publish-3x4",), default="publish-3x4")
    parser.add_argument("--mode", dest="file_mode", choices=("copy", "move"), default="copy")
    parser.add_argument("--zip", dest="zip_path", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.manifest or not args.source_dir or not args.output_dir:
        parser.error("--manifest, --source-dir and --output-dir are required")
    try:
        result = finalize(args.manifest, args.source_dir, args.output_dir, args.file_mode, args.zip_path)
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
