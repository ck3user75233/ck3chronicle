"""Neutral candidate invocation and observation helpers.

The module imports no candidate package at module import time.  Each public
function imports only after the caller has established the isolated profile.
"""
from __future__ import annotations

import base64
import contextlib
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import sqlite3
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from harness_core import canonical_json_bytes, file_identity, sha256_file, write_canonical_json
from process_control import run_bounded_process
from timeouts import PRODUCT_SUBPROCESS_DEFAULT_SECONDS


HEADER = re.compile(
    rb"^\[(?P<timestamp>\d{2}:\d{2}:\d{2})\]\[(?P<level>[^\]\r\n]+)\]\[(?P<tag>[^\]\r\n]+)\]:"
)


def jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, bytes):
        return {"base64": base64.b64encode(value).decode("ascii"), "bytes": len(value), "sha256": hashlib.sha256(value).hexdigest()}
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def isolated_cli_environment(candidate_root: Path, evidence_root: Path, extra_pythonpath: Path | None = None) -> dict[str, str]:
    if evidence_root.name != "ck3chronicle":
        raise ValueError("evidence root must be named ck3chronicle for isolated default config")
    profile = evidence_root.parent.parent / "profile"
    profile.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["LOCALAPPDATA"] = str(evidence_root.parent)
    env["USERPROFILE"] = str(profile)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    paths = [str(candidate_root / "src")]
    if extra_pythonpath is not None:
        paths.insert(0, str(extra_pythonpath))
    existing = env.get("PYTHONPATH")
    if existing:
        paths.append(existing)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def invoke_cli(
    *,
    candidate_root: Path,
    python_executable: Path,
    evidence_root: Path,
    argv: list[str],
    declared_root: Path,
    transcript_id: str,
    extra_pythonpath: Path | None = None,
    timeout_seconds: float | None = None,
) -> dict[str, Any]:
    env = isolated_cli_environment(candidate_root, evidence_root, extra_pythonpath)
    command = [str(python_executable), "-B", "-m", "ck3chronicle.cli", *argv]
    transcript_root = declared_root / "transcripts"
    transcript_root.mkdir(parents=True, exist_ok=True)
    stdout_path = transcript_root / f"{transcript_id}.stdout.bin"
    stderr_path = transcript_root / f"{transcript_id}.stderr.bin"
    ceiling = float(timeout_seconds or os.environ.get("CK3CHRONICLE_PHASE1_PRODUCT_SUBPROCESS_TIMEOUT_SECONDS", PRODUCT_SUBPROCESS_DEFAULT_SECONDS))
    process = run_bounded_process(
        command,
        timeout_seconds=ceiling,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        env=env,
    )
    if process["sampler_error"] or not process["process_tree"]["all_observed_processes_terminated"]:
        raise RuntimeError("bounded product subprocess cleanup could not be proven")
    stdout = stdout_path.read_bytes()
    metadata = {
        "transcript_id": transcript_id,
        "argv": argv,
        "exit_code": process["root_exit_code"],
        "timed_out": process["timed_out"],
        "output_limit_exceeded": process["output_limit_exceeded"],
        "resource_limit_exceeded": process["resource_limit_exceeded"],
        "sampler_error": process["sampler_error"],
        "timeout_seconds": ceiling,
        "bounded_process": process,
        "stdout": file_identity(stdout_path, declared_root),
        "stderr": file_identity(stderr_path, declared_root),
        "stdout_json": None,
    }
    if stdout:
        try:
            metadata["stdout_json"] = json.loads(stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
    write_canonical_json(transcript_root / f"{transcript_id}.json", metadata)
    return metadata


def direct_capture_process(
    *,
    logs_root: Path,
    evidence_root: Path,
    termination_kind: str = "normal",
    observed_started_at: str | None = None,
    observed_ended_at: str | None = None,
    crash: dict[str, Any] | None = None,
    process_now: bool = True,
) -> dict[str, Any]:
    from ck3chronicle.classification.catalog import load_approved_classifier
    from ck3chronicle.harvester import spool_logs
    from ck3chronicle.processing import process_pending
    from ck3chronicle.watcher import write_capture_receipt

    pending = spool_logs(logs_root, evidence_root)
    receipt = write_capture_receipt(
        evidence_root,
        pending,
        trigger="phase1_public_runner",
        observed_started_at=observed_started_at,
        observed_ended_at=observed_ended_at,
        termination_kind=termination_kind,
        crash=crash,
    )
    result = process_pending(evidence_root, load_approved_classifier()) if process_now else None
    return {"pending": jsonable(pending), "receipt_path": str(receipt), "processing": jsonable(result)}


def finalize_and_register_without_derivation(logs_root: Path, evidence_root: Path, *, receipt: bool = True) -> dict[str, Any]:
    from ck3chronicle.archive_registry import reconcile_archives
    from ck3chronicle.harvester import finalize_pending_captures, spool_logs
    from ck3chronicle.run_registry import reconcile_run_receipts
    from ck3chronicle.watcher import write_capture_receipt

    pending = spool_logs(logs_root, evidence_root)
    receipt_path = None
    if receipt:
        receipt_path = write_capture_receipt(
            evidence_root,
            pending,
            trigger="phase1_public_runner",
            observed_started_at="2026-08-16T00:00:00+00:00",
            observed_ended_at="2026-08-16T00:01:00+00:00",
            termination_kind="normal",
        )
    snapshots = finalize_pending_captures(evidence_root)
    archive = reconcile_archives(evidence_root, evidence_root / "ck3chronicle.db", strict_integrity=True)
    runs = reconcile_run_receipts(evidence_root, evidence_root / "ck3chronicle.db", strict_integrity=True) if receipt else None
    return {"pending": jsonable(pending), "receipt_path": str(receipt_path) if receipt_path else None, "snapshots": jsonable(snapshots), "archive_reconciliation": jsonable(archive), "run_reconciliation": jsonable(runs)}


def _line_spans(data: bytes) -> list[tuple[int, int, int, bytes]]:
    result: list[tuple[int, int, int, bytes]] = []
    byte_offset = 0
    line_number = 1
    for line in data.splitlines(keepends=True):
        end = byte_offset + len(line)
        result.append((line_number, byte_offset, end, line))
        byte_offset = end
        line_number += 1
    if byte_offset < len(data):
        result.append((line_number, byte_offset, len(data), data[byte_offset:]))
    return result


def independent_lexical_scan(path: Path, export_path: Path | None = None) -> dict[str, Any]:
    data = path.read_bytes()
    lines = _line_spans(data)
    starts: list[tuple[int, int, re.Match[bytes]]] = []
    for line_number, start, _end, line in lines:
        candidate = line[3:] if start == 0 and line.startswith(b"\xef\xbb\xbf") else line
        match = HEADER.match(candidate)
        if match:
            starts.append((line_number, start, match))
    records: list[dict[str, Any]] = []
    first_header_byte = starts[0][1] if starts else len(data)
    if first_header_byte:
        raw = data[:first_header_byte]
        end_line = max(1, starts[0][0] - 1) if starts else max(1, len(lines))
        records.append({"block_index": 0, "kind": "preamble", "start_line": 1, "end_line": end_line, "start_byte": 0, "end_byte": first_header_byte, "raw_byte_length": len(raw), "raw_block_sha256": hashlib.sha256(raw).hexdigest()})
    for ordinal, (line_number, start, match) in enumerate(starts, start=1):
        end = starts[ordinal][1] if ordinal < len(starts) else len(data)
        end_line = starts[ordinal][0] - 1 if ordinal < len(starts) else max(line_number, len(lines))
        raw = data[start:end]
        tag = match.group("tag").decode("utf-8", "replace")
        records.append({
            "block_index": ordinal,
            "kind": "timestamped",
            "start_line": line_number,
            "end_line": end_line,
            "start_byte": start,
            "end_byte": end,
            "timestamp": match.group("timestamp").decode("ascii"),
            "level": match.group("level").decode("utf-8", "replace"),
            "source_tag": tag,
            "source_family": tag.split(":", 1)[0],
            "raw_byte_length": len(raw),
            "raw_block_sha256": hashlib.sha256(raw).hexdigest(),
        })
    if export_path is not None:
        export_path.parent.mkdir(parents=True, exist_ok=True)
        with gzip.GzipFile(filename=str(export_path), mode="wb", compresslevel=9, mtime=0) as stream:
            for record in records:
                stream.write(canonical_json_bytes(record))
    reconstruction = hashlib.sha256()
    for record in records:
        reconstruction.update(data[int(record["start_byte"]) : int(record["end_byte"])])
    return {
        "path_identity": file_identity(path),
        "timestamped_blocks": len(starts),
        "preamble_blocks": int(first_header_byte > 0),
        "record_count": len(records),
        "reconstruction_sha256": reconstruction.hexdigest(),
        "records_sha256": hashlib.sha256(b"".join(canonical_json_bytes(item) for item in records)).hexdigest(),
        "records": records if export_path is None else None,
        "export": file_identity(export_path) if export_path is not None else None,
    }


def product_lexical_scan(path: Path, export_path: Path | None = None) -> dict[str, Any]:
    from ck3chronicle.parser.log_blocks import iter_log_blocks

    records: list[dict[str, Any]] = []
    reconstruction = hashlib.sha256()
    stream = gzip.GzipFile(filename=str(export_path), mode="wb", compresslevel=9, mtime=0) if export_path else None
    try:
        for ordinal, block in enumerate(iter_log_blocks(path, log_relpath="error.log", retain_preamble=True)):
            raw_bytes = block.raw_block.encode("utf-8", "surrogatepass")
            reconstruction.update(raw_bytes)
            row = {
                "block_index": ordinal,
                "timestamp": block.timestamp,
                "level": block.level,
                "source_tag": block.source_tag,
                "source_family": block.source_family,
                "header_line": block.header_line,
                "continuation_lines": list(block.continuation_lines),
                "log_relpath": block.log_relpath,
                "line_number": block.line_number,
                "end_line": block.end_line,
                "raw_block_sha256": block.raw_block_sha256,
                "raw_byte_length": block.raw_byte_length,
                "source_block_id": block.source_block_id,
                "raw_block_utf8_sha256": hashlib.sha256(raw_bytes).hexdigest(),
            }
            records.append(row)
            if stream:
                stream.write(canonical_json_bytes(row))
    finally:
        if stream:
            stream.close()
    return {
        "block_count": len(records),
        "records_sha256": hashlib.sha256(b"".join(canonical_json_bytes(item) for item in records)).hexdigest(),
        "reconstruction_sha256": reconstruction.hexdigest(),
        "records": records if export_path is None else None,
        "export": file_identity(export_path) if export_path else None,
    }


def table_projection(db_path: Path, *, samples_per_table: int = 12) -> dict[str, Any]:
    if not db_path.is_file():
        return {"database_present": False}
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    tables: dict[str, Any] = {}
    try:
        names = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        for name in names:
            columns = [row[1] for row in conn.execute(f'PRAGMA table_info("{name}")')]
            count = int(conn.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0])
            hasher = hashlib.sha256()
            first: list[dict[str, Any]] = []
            last: list[dict[str, Any]] = []
            for index, row in enumerate(conn.execute(f'SELECT * FROM "{name}" ORDER BY rowid')):
                item: dict[str, Any] = {}
                for column in columns:
                    value = row[column]
                    if name == "raw_block_contents" and column == "raw_block":
                        raw = str(value).encode("utf-8", "surrogatepass")
                        value = {"utf8_bytes": len(raw), "utf8_sha256": hashlib.sha256(raw).hexdigest()}
                    item[column] = value
                hasher.update(canonical_json_bytes(item))
                if index < samples_per_table:
                    first.append(item)
                last.append(item)
                if len(last) > samples_per_table:
                    last.pop(0)
            tables[name] = {"row_count": count, "projection_sha256": hasher.hexdigest(), "first_rows": first, "last_rows": last}
    finally:
        conn.close()
    return {"database_present": True, "database": file_identity(db_path), "tables": tables}


def canonical_distribution_export(db_path: Path, destination: Path) -> dict[str, Any]:
    conn = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    queries = {
        "totals": "SELECT session_id, parse_source_blocks, parse_issue_occurrences, parse_issue_clusters, parse_unclassified_occurrences, parse_multi_issue_blocks, parse_silently_dropped_blocks FROM sessions ORDER BY session_id",
        "per_block": "SELECT sb.session_id, sb.start_line, sb.end_line, rb.raw_block_sha256, rb.raw_byte_length, sb.issue_count, COUNT(io.issue_occurrence_id) AS linked_occurrences FROM source_blocks sb JOIN raw_block_contents rb ON rb.raw_block_pk=sb.raw_block_pk LEFT JOIN issue_occurrences io ON io.source_block_pk=sb.source_block_pk GROUP BY sb.source_block_pk ORDER BY sb.session_id,sb.start_line",
        "per_signature": "SELECT i.session_id, i.signature, i.category, i.error_type, i.occurrence_count, COUNT(io.issue_occurrence_id) AS linked_occurrences FROM issues i LEFT JOIN issue_occurrences io ON io.session_id=i.session_id AND io.signature=i.signature GROUP BY i.issue_id ORDER BY i.session_id,i.signature",
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    hasher = hashlib.sha256()
    with gzip.GzipFile(filename=str(destination), mode="wb", compresslevel=9, mtime=0) as stream:
        for section, query in queries.items():
            count = 0
            for row in conn.execute(query):
                item = {"section": section, **dict(row)}
                payload = canonical_json_bytes(item)
                stream.write(payload); hasher.update(payload); count += 1
            counts[section] = count
    conn.close()
    return {"counts": counts, "projection_sha256": hasher.hexdigest(), "artifact": file_identity(destination)}


def invoke_direct_with_capture(function, *args, **kwargs) -> dict[str, Any]:
    stdout = io.StringIO(); stderr = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = function(*args, **kwargs)
        return {"status": "returned", "result": jsonable(result), "stdout_utf8": stdout.getvalue(), "stderr_utf8": stderr.getvalue()}
    except Exception as exc:
        return {"status": "raised", "exception_type": f"{type(exc).__module__}.{type(exc).__qualname__}", "message": str(exc), "stdout_utf8": stdout.getvalue(), "stderr_utf8": stderr.getvalue()}


def chronological_times() -> list[tuple[str, str]]:
    return [
        ("2026-08-16T01:00:00+00:00", "2026-08-16T01:10:00+00:00"),
        ("2026-08-16T02:00:00+00:00", "2026-08-16T02:10:00+00:00"),
        ("2026-08-16T03:00:00+00:00", "2026-08-16T03:10:00+00:00"),
        ("2026-08-16T04:00:00+00:00", "2026-08-16T04:10:00+00:00"),
    ]
