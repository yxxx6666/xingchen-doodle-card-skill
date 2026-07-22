#!/usr/bin/env python3
"""Atomic progress/checkpoint controller for sequential Codex $imagegen runs."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

VERSION = "v0.8.10"
ACTIVE = "WAITING_IMAGEGEN"
FINAL = "COMPLETE"
RETRYABLE = {"PLANNED", "SERVICE_TIMEOUT", "PAUSED_TIMEOUT", "RATIO_FAILED", "CONTENT_FAILED"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_time(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def append_log(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": now_iso(), **event}, ensure_ascii=False) + "\n")


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != VERSION:
        raise ValueError(f"manifest version must be {VERSION}")
    if not isinstance(data.get("pages"), list) or not data["pages"]:
        raise ValueError("manifest pages missing")
    return data


def page_by_id(data: dict, page_id: str) -> dict:
    for page in data["pages"]:
        if page.get("page_id") == page_id:
            return page
    raise ValueError(f"page not found: {page_id}")


def first_incomplete(data: dict) -> str | None:
    for page in data["pages"]:
        if page.get("status") != FINAL:
            return page.get("page_id")
    return None


def refresh(data: dict) -> None:
    data["first_incomplete_page_id"] = first_incomplete(data)
    data["resume_from_page_id"] = data["first_incomplete_page_id"]
    data["updated_at"] = now_iso()


def enforce_current(data: dict, page_id: str) -> dict:
    current = first_incomplete(data)
    if current != page_id:
        raise ValueError(f"only first incomplete page may run: expected {current}, got {page_id}")
    return page_by_id(data, page_id)


def cmd_begin(args) -> dict:
    data = load(args.manifest)
    page = enforce_current(data, args.page_id)
    if page.get("status") not in RETRYABLE:
        raise ValueError(f"page status cannot begin: {page.get('status')}")
    total = int(page.get("service_dispatch_count", 0))
    if total >= args.max_service_dispatches:
        page["status"] = "PAUSED_TIMEOUT"
        page["last_error_type"] = "SERVICE_RETRY_EXHAUSTED"
        refresh(data); atomic_write(args.manifest, data)
        raise ValueError("maximum cumulative service dispatches reached")
    window_id = args.execution_window_id or str(uuid.uuid4())
    if page.get("execution_window_id") != window_id:
        page["execution_window_id"] = window_id
        page["window_dispatch_count"] = 0
    window_count = int(page.get("window_dispatch_count", 0))
    if window_count >= args.max_window_dispatches:
        page["status"] = "PAUSED_TIMEOUT"
        refresh(data); atomic_write(args.manifest, data)
        raise ValueError("maximum immediate dispatches for this execution window reached")
    page["service_dispatch_count"] = total + 1
    page["window_dispatch_count"] = window_count + 1
    page["status"] = ACTIVE
    page["attempt_id"] = str(uuid.uuid4())
    page["dispatch_started_at"] = now_iso()
    page["last_error"] = None
    page["last_error_type"] = None
    refresh(data); atomic_write(args.manifest, data)
    append_log(args.log_jsonl, {"event":"dispatch_started","page_id":args.page_id,"attempt_id":page["attempt_id"],"service_dispatch_count":page["service_dispatch_count"],"window_dispatch_count":page["window_dispatch_count"]})
    return {"status":"PASS","action":"BEGIN","page_id":args.page_id,"attempt_id":page["attempt_id"],"service_dispatch_count":page["service_dispatch_count"],"window_dispatch_count":page["window_dispatch_count"]}


def cmd_timeout(args) -> dict:
    data = load(args.manifest)
    page = enforce_current(data, args.page_id)
    if page.get("status") != ACTIVE:
        raise ValueError(f"timeout requires {ACTIVE}, got {page.get('status')}")
    window_count = int(page.get("window_dispatch_count", 0))
    total = int(page.get("service_dispatch_count", 0))
    can_retry_now = window_count < args.max_window_dispatches and total < args.max_service_dispatches
    page["status"] = "SERVICE_TIMEOUT" if can_retry_now else "PAUSED_TIMEOUT"
    page["last_error_type"] = "SERVICE_TIMEOUT"
    page["last_error"] = args.error
    page["last_timeout_at"] = now_iso()
    page["attempt_id"] = None
    refresh(data); atomic_write(args.manifest, data)
    append_log(args.log_jsonl, {"event":"service_timeout","page_id":args.page_id,"next_status":page["status"],"service_dispatch_count":total,"window_dispatch_count":window_count,"error":args.error})
    return {"status":"PASS","action":"TIMEOUT","page_id":args.page_id,"page_status":page["status"],"retry_immediately":can_retry_now,"resume_from_page_id":data["resume_from_page_id"]}


def cmd_returned(args) -> dict:
    data = load(args.manifest)
    page = enforce_current(data, args.page_id)
    if page.get("status") != ACTIVE:
        raise ValueError(f"returned requires {ACTIVE}, got {page.get('status')}")
    page["status"] = "GENERATED"
    page["source_file"] = args.source_file
    page["returned_at"] = now_iso()
    page["attempt_id"] = None
    refresh(data); atomic_write(args.manifest, data)
    append_log(args.log_jsonl, {"event":"image_returned","page_id":args.page_id,"source_file":args.source_file})
    return {"status":"PASS","action":"RETURNED","page_id":args.page_id,"source_file":args.source_file}


def cmd_fail(args) -> dict:
    data = load(args.manifest)
    page = enforce_current(data, args.page_id)
    count = int(page.get("content_attempt_count", 0)) + 1
    page["content_attempt_count"] = count
    page["status"] = "RATIO_FAILED" if args.failure_type == "ratio" else "CONTENT_FAILED"
    page["last_error_type"] = "RATIO_FAILURE" if args.failure_type == "ratio" else "CONTENT_FAILURE"
    page["last_error"] = args.error
    page["source_file"] = None
    refresh(data); atomic_write(args.manifest, data)
    append_log(args.log_jsonl, {"event":"returned_image_failed","page_id":args.page_id,"failure_type":args.failure_type,"content_attempt_count":count,"error":args.error})
    return {"status":"PASS","action":"FAIL","page_id":args.page_id,"content_attempt_count":count,"can_retry":count < args.max_content_attempts}


def cmd_complete(args) -> dict:
    data = load(args.manifest)
    page = enforce_current(data, args.page_id)
    page.update({"status":"COMPLETE","source_file":args.source_file,"actual_width":args.actual_width,"actual_height":args.actual_height,"actual_ratio":round(args.actual_width/args.actual_height,6),"ratio_passed":True,"sha256":args.sha256,"completed_at":now_iso(),"last_error":None,"last_error_type":None})
    refresh(data); atomic_write(args.manifest, data)
    append_log(args.log_jsonl, {"event":"page_complete","page_id":args.page_id,"source_file":args.source_file,"actual_width":args.actual_width,"actual_height":args.actual_height,"ratio":round(args.actual_width/args.actual_height,6)})
    return {"status":"PASS","action":"COMPLETE","page_id":args.page_id,"next_page_id":data["first_incomplete_page_id"]}


def cmd_recover(args) -> dict:
    data = load(args.manifest)
    recovered=[]
    now=datetime.now(timezone.utc)
    for page in data["pages"]:
        if page.get("status") != ACTIVE:
            continue
        started=parse_time(page.get("dispatch_started_at"))
        age=(now-started).total_seconds() if started else None
        stale=args.force_after_reconnect or age is None or age >= args.stale_after
        if stale:
            page["status"]="SERVICE_TIMEOUT"
            page["last_error_type"]="SESSION_INTERRUPTED" if args.force_after_reconnect else "STALE_IMAGEGEN_REQUEST"
            page["last_error"]="live image request state was not preserved; re-dispatch same page"
            page["attempt_id"]=None
            page["last_timeout_at"]=now_iso()
            recovered.append(page.get("page_id"))
    refresh(data); atomic_write(args.manifest,data)
    for pid in recovered:
        append_log(args.log_jsonl,{"event":"stale_request_recovered","page_id":pid,"force_after_reconnect":args.force_after_reconnect})
    return {"status":"PASS","action":"RECOVER","recovered_pages":recovered,"resume_from_page_id":data["resume_from_page_id"]}


def cmd_status(args) -> dict:
    data=load(args.manifest); refresh(data)
    return {"status":"PASS","action":"STATUS","version":data.get("version"),"first_incomplete_page_id":data.get("first_incomplete_page_id"),"resume_from_page_id":data.get("resume_from_page_id"),"pages":[{"page_id":p.get("page_id"),"status":p.get("status"),"service_dispatch_count":p.get("service_dispatch_count",0),"content_attempt_count":p.get("content_attempt_count",0)} for p in data["pages"]]}


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); manifest=td/'progress.json'; log=td/'log.jsonl'
        data={"version":VERSION,"validation_mode":"publish-3x4","requested_ratio":"3:4","fixed_pixel_size_required":False,"total_pages":4,"generation_order":["P01","P02","P03","P04"],"delivery_order":["P01","P02","P03","P04"],"first_incomplete_page_id":"P03","resume_from_page_id":"P03","pages":[
            {"page_id":"P01","page_index":1,"ordered_file_name":"01-cover-t.png","status":"COMPLETE"},
            {"page_id":"P02","page_index":2,"ordered_file_name":"02-content-t.png","status":"COMPLETE"},
            {"page_id":"P03","page_index":3,"ordered_file_name":"03-content-t.png","status":"PLANNED","service_dispatch_count":0,"content_attempt_count":0},
            {"page_id":"P04","page_index":4,"ordered_file_name":"04-content-t.png","status":"PLANNED","service_dispatch_count":0,"content_attempt_count":0}]}
        atomic_write(manifest,data)
        class A: pass
        a=A(); a.manifest=manifest; a.page_id='P03'; a.execution_window_id='w1'; a.max_service_dispatches=4; a.max_window_dispatches=2; a.log_jsonl=log
        cmd_begin(a)
        a.error='request timed out'; cmd_timeout(a)
        cmd_begin(a)
        cmd_timeout(a)
        state=load(manifest)
        p=page_by_id(state,'P03')
        if p['status']!='PAUSED_TIMEOUT' or p['service_dispatch_count']!=2 or p.get('content_attempt_count',0)!=0: return 1
        # new execution window resumes P03
        a.execution_window_id='w2'; cmd_begin(a)
        # simulate reconnect and recover
        r=A(); r.manifest=manifest; r.force_after_reconnect=True; r.stale_after=300; r.log_jsonl=log
        cmd_recover(r)
        state=load(manifest)
        if page_by_id(state,'P03')['status']!='SERVICE_TIMEOUT' or state['first_incomplete_page_id']!='P03': return 1
        print('series_progress_controller self-test passed')
        return 0


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('command', choices=('begin','timeout','returned','fail','complete','recover','status','self-test'))
    p.add_argument('--manifest', type=Path)
    p.add_argument('--page-id')
    p.add_argument('--execution-window-id')
    p.add_argument('--max-service-dispatches', type=int, default=4)
    p.add_argument('--max-window-dispatches', type=int, default=2)
    p.add_argument('--max-content-attempts', type=int, default=3)
    p.add_argument('--error', default='')
    p.add_argument('--failure-type', choices=('ratio','content'), default='content')
    p.add_argument('--source-file')
    p.add_argument('--actual-width', type=int)
    p.add_argument('--actual-height', type=int)
    p.add_argument('--sha256')
    p.add_argument('--stale-after', type=int, default=300)
    p.add_argument('--force-after-reconnect', action='store_true')
    p.add_argument('--log-jsonl', type=Path)
    args=p.parse_args()
    if args.command=='self-test': return self_test()
    if not args.manifest: p.error('--manifest is required')
    if args.log_jsonl is None: args.log_jsonl=args.manifest.with_name('generation-log.jsonl')
    if args.command in {'begin','timeout','returned','fail','complete'} and not args.page_id: p.error('--page-id is required')
    if args.command=='returned' and not args.source_file: p.error('--source-file is required')
    if args.command=='complete' and (not args.source_file or args.actual_width is None or args.actual_height is None or not args.sha256): p.error('complete requires --source-file --actual-width --actual-height --sha256')
    try:
        fn={'begin':cmd_begin,'timeout':cmd_timeout,'returned':cmd_returned,'fail':cmd_fail,'complete':cmd_complete,'recover':cmd_recover,'status':cmd_status}[args.command]
        result=fn(args)
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except Exception as exc:
        print(json.dumps({'status':'FAIL','command':args.command,'error':str(exc)},ensure_ascii=False,indent=2)); return 1

if __name__=='__main__': raise SystemExit(main())
