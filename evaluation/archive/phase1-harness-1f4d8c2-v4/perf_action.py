"""Single-process performance action used by the public harness sampler."""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from candidate_runtime import jsonable


def _timed(call):
    cpu_start = time.process_time()
    wall_start = time.perf_counter()
    result = call()
    wall_end = time.perf_counter()
    cpu_end = time.process_time()
    return result, wall_end - wall_start, cpu_end - cpu_start


def _cli_in_process(argv: list[str]) -> dict[str, Any]:
    from ck3chronicle.cli import build_parser
    parser = build_parser(); args = parser.parse_args(argv)
    stdout = io.StringIO(); stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exit_code = int(args.func(args))
    out = stdout.getvalue().encode("utf-8"); err = stderr.getvalue().encode("utf-8")
    return {"argv": argv, "exit_code": exit_code, "stdout_bytes": len(out), "stdout_sha256": hashlib.sha256(out).hexdigest(), "stderr_bytes": len(err), "stderr_sha256": hashlib.sha256(err).hexdigest()}


def execute(request: dict[str, Any]) -> dict[str, Any]:
    action = request["action"]
    if request.get("harness_selftest_sleep_tree"):
        if action != "runtime":
            raise ValueError("sleep-tree fixture is restricted to the PERF-02 runtime action path")
        print("PERF02_TIMEOUT_SELFTEST_PARTIAL_STDOUT", flush=True)
        child = subprocess.Popen([sys.executable, "-B", __file__, "--selftest-descendant", "child"])
        print(json.dumps({"selftest_parent_pid":os.getpid(),"selftest_child_pid":child.pid},sort_keys=True),flush=True)
        time.sleep(float(request.get("sleep_seconds", 120)))
        raise RuntimeError("sleep-tree fixture unexpectedly reached its deadline")
    if action == "lexical":
        from ck3chronicle.parser.log_blocks import iter_log_blocks
        path = Path(request["path"])
        def call():
            digest = hashlib.sha256(); count = 0
            for block in iter_log_blocks(path, log_relpath="error.log", retain_preamble=True):
                digest.update(block.raw_block_sha256.encode("ascii")); digest.update(str(block.raw_byte_length).encode("ascii")); count += 1
            return {"block_count": count, "projection_sha256": digest.hexdigest()}
        result, wall, cpu = _timed(call)
    elif action == "parse":
        from ck3chronicle.db import repository
        from ck3chronicle.parser.service import parse_session
        evidence = Path(request["evidence_root"]); session_id = int(request["session_id"]); conn = repository.open_db(evidence / "ck3chronicle.db")
        try: result, wall, cpu = _timed(lambda: jsonable(parse_session(conn, evidence, session_id)))
        finally: conn.close()
    elif action == "runtime":
        from ck3chronicle.db import repository
        from ck3chronicle.runtime_context import parse_runtime_context
        evidence = Path(request["evidence_root"]); session_id = int(request["session_id"]); conn = repository.open_db(evidence / "ck3chronicle.db")
        try: result, wall, cpu = _timed(lambda: jsonable(parse_runtime_context(conn, evidence, session_id)))
        finally: conn.close()
    elif action == "report_function":
        from ck3chronicle.db import repository
        from ck3chronicle.reporting import build_session_report
        evidence = Path(request["evidence_root"]); session_id = int(request["session_id"]); conn = repository.open_db_readonly(evidence / "ck3chronicle.db")
        try:
            result, wall, cpu = _timed(lambda: build_session_report(conn, session_id, observed_run_id=request.get("run_id")))
            result = {"report_sha256": hashlib.sha256(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(), "schema": result.get("schema"), "schema_version": result.get("schema_version")}
        finally: conn.close()
    elif action == "report_cli":
        result, wall, cpu = _timed(lambda: _cli_in_process(list(request["argv"])))
    elif action == "pipeline":
        from ck3chronicle.classification.catalog import load_approved_classifier
        from ck3chronicle.harvester import spool_logs
        from ck3chronicle.processing import process_pending
        from ck3chronicle.watcher import write_capture_receipt
        source = Path(request["source_logs"]); evidence = Path(request["evidence_root"]); target = Path(request["copy_target"])
        def call():
            shutil.copytree(source, target)
            pending = spool_logs(target, evidence)
            write_capture_receipt(evidence, pending, trigger="phase1_perf_pipeline", observed_started_at="2026-08-16T00:00:00+00:00", observed_ended_at="2026-08-16T00:10:00+00:00", termination_kind="normal")
            return jsonable(process_pending(evidence, load_approved_classifier()))
        result, wall, cpu = _timed(call)
    else:
        raise KeyError(action)
    return {"action": action, "wall_seconds": wall, "child_cpu_seconds": cpu, "logical_result": result}


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--request"); parser.add_argument("--selftest-descendant",choices=("child","grandchild")); parser.add_argument("--selftest-immediate-orphan",action="store_true"); parser.add_argument("--selftest-fast-output-bytes",type=int); args = parser.parse_args()
    if args.selftest_immediate_orphan:
        child=subprocess.Popen([sys.executable,"-B",__file__,"--selftest-descendant","child"])
        print(json.dumps({"selftest_immediate_parent_pid":os.getpid(),"selftest_child_pid":child.pid},sort_keys=True),flush=True)
        return 0
    if args.selftest_fast_output_bytes is not None:
        if args.selftest_fast_output_bytes<=0:
            parser.error("--selftest-fast-output-bytes must be positive")
        sys.stdout.buffer.write(b"F"*args.selftest_fast_output_bytes); sys.stdout.buffer.flush()
        return 0
    if args.selftest_descendant:
        if args.selftest_descendant=="child":
            grandchild=subprocess.Popen([sys.executable,"-B",__file__,"--selftest-descendant","grandchild"])
            print(json.dumps({"selftest_child_pid":os.getpid(),"selftest_grandchild_pid":grandchild.pid},sort_keys=True),flush=True)
        else:
            print(json.dumps({"selftest_grandchild_pid":os.getpid()},sort_keys=True),flush=True)
        time.sleep(120)
        return 0
    if not args.request:
        parser.error("--request is required")
    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    print(json.dumps(execute(request), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
