"""Project immutable run receipts and crash-source provenance into SQLite."""
from __future__ import annotations

import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .db import repository
from .harvester import PRINCIPAL_LOG_NAMES, hash_file
from .run_receipts import (
    RUN_RECEIPT_VERSION,
    finalized_receipts,
    receipt_sha256,
)


@dataclass(frozen=True)
class RunReconciliationSummary:
    scanned: int
    registered: int
    already_registered: int
    errors: tuple[str, ...]


def _required_text(payload: dict[str, Any], name: str) -> str:
    value = payload.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"run receipt has invalid {name}")
    return value


def _preserve_different_crash_file(
    root: Path,
    capture_id: str,
    rel_path: str,
    source: Path,
    expected_sha256: str,
) -> str:
    destination = Path(root) / "crash_evidence" / capture_id / rel_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file():
        if hash_file(destination) != expected_sha256:
            raise ValueError("preserved crash evidence hash conflict")
        return destination.relative_to(root).as_posix()

    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}-", dir=destination.parent
    )
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        if hash_file(temporary) != expected_sha256:
            raise ValueError("crash log changed while being preserved")
        os.replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination.relative_to(root).as_posix()


def _file_origins(
    conn,
    root: Path,
    *,
    observation_id: int,
    session_id: int,
    capture_id: str,
    termination_kind: str,
    crash: dict[str, Any] | None,
) -> None:
    files = conn.execute(
        """
        SELECT session_file_id, rel_path, sha256
        FROM session_files
        WHERE session_id = ?
        ORDER BY rel_path
        """,
        (session_id,),
    ).fetchall()
    if termination_kind == "crash":
        origin_kind = "live_after_crash"
    elif termination_kind == "normal":
        origin_kind = "live_normal"
    else:
        origin_kind = "live_unknown"

    crash_folder = None
    if isinstance(crash, dict) and isinstance(crash.get("folder_path"), str):
        crash_folder = Path(crash["folder_path"])
    origins: list[dict[str, Any]] = []
    for row in files:
        rel_path = str(row["rel_path"]).replace("\\", "/")
        item: dict[str, Any] = {
            "session_file_id": int(row["session_file_id"]),
            "origin_kind": origin_kind,
            "crash_rel_path": None,
            "crash_sha256": None,
            "crash_equivalence": (
                "unavailable"
                if termination_kind == "crash" and rel_path in PRINCIPAL_LOG_NAMES
                else "not_applicable"
            ),
            "preserved_crash_rel_path": None,
        }
        if (
            termination_kind == "crash"
            and rel_path in PRINCIPAL_LOG_NAMES
            and crash_folder is not None
        ):
            candidate = crash_folder / "logs" / rel_path
            item["crash_rel_path"] = f"logs/{rel_path}"
            if candidate.is_file() and not candidate.is_symlink():
                crash_sha256 = hash_file(candidate)
                item["crash_sha256"] = crash_sha256
                if crash_sha256 == row["sha256"]:
                    item["crash_equivalence"] = "exact"
                else:
                    item["crash_equivalence"] = "different"
                    item["preserved_crash_rel_path"] = (
                        _preserve_different_crash_file(
                            root,
                            capture_id,
                            rel_path,
                            candidate,
                            crash_sha256,
                        )
                    )
        origins.append(item)
    repository.replace_run_file_origins(conn, observation_id, origins)


def reconcile_run_receipts(
    root: Path, db_path: Path
) -> RunReconciliationSummary:
    """Rebuild the run index from finalized receipt files idempotently."""
    evidence_root = Path(root)
    receipts = finalized_receipts(evidence_root)
    registered = 0
    existing = 0
    errors: list[str] = []
    conn = repository.open_db(db_path)
    try:
        for path, payload in receipts:
            capture_id = path.stem
            try:
                if payload.get("schema") != "ck3chronicle.finalized-run-receipt":
                    raise ValueError("unexpected run receipt schema")
                if payload.get("schema_version") != RUN_RECEIPT_VERSION:
                    raise ValueError("unsupported run receipt version")
                if payload.get("status") != "finalized":
                    raise ValueError("run receipt is not finalized")
                if _required_text(payload, "capture_id") != capture_id:
                    raise ValueError("run receipt filename disagrees with capture_id")
                bundle_hash = _required_text(payload, "evidence_bundle_hash")
                session = repository.get_session_by_hash(conn, bundle_hash)
                if session is None or session["capture_status"] != "finalized":
                    raise ValueError("run receipt evidence bundle is not registered")
                if session["capture_manifest_sha256"] != _required_text(
                    payload, "manifest_sha256"
                ):
                    raise ValueError("run receipt manifest hash disagrees")
                process = payload.get("process")
                process = process if isinstance(process, dict) else {}
                crash = payload.get("crash")
                crash = crash if isinstance(crash, dict) else None
                termination_kind = str(payload.get("termination_kind", "unknown"))
                observation_id, was_existing = repository.register_run(
                    conn,
                    session_id=int(session["session_id"]),
                    capture_id=capture_id,
                    trigger=_required_text(payload, "trigger"),
                    process_name=process.get("image_name"),
                    observed_at=_required_text(payload, "captured_at"),
                    observed_started_at=payload.get("observed_started_at"),
                    observed_ended_at=payload.get("observed_ended_at"),
                    process_pid=process.get("pid"),
                    process_started_ns=process.get("started_ns"),
                    termination_kind=termination_kind,
                    crash_folder_name=(crash or {}).get("folder_name"),
                    crash_folder_path=(crash or {}).get("folder_path"),
                    crash_detected_at=(crash or {}).get("detected_at"),
                    crash_association_method=(crash or {}).get("association_method"),
                    crash_association_confidence=(crash or {}).get("confidence"),
                    receipt_sha256=receipt_sha256(path),
                )
                stored_origins = repository.get_run_file_origins(
                    conn, observation_id
                )
                session_file_count = int(
                    conn.execute(
                        "SELECT COUNT(*) FROM session_files WHERE session_id = ?",
                        (session["session_id"],),
                    ).fetchone()[0]
                )
                unresolved_crash_origin = any(
                    row["rel_path"] in PRINCIPAL_LOG_NAMES
                    and row["crash_equivalence"] == "unavailable"
                    for row in stored_origins
                )
                if (
                    len(stored_origins) != session_file_count
                    or unresolved_crash_origin
                ):
                    _file_origins(
                        conn,
                        evidence_root,
                        observation_id=observation_id,
                        session_id=int(session["session_id"]),
                        capture_id=capture_id,
                        termination_kind=termination_kind,
                        crash=crash,
                    )
                existing += int(was_existing)
                registered += int(not was_existing)
            except Exception as exc:
                errors.append(f"{path.name}: {exc}")
    finally:
        conn.close()
    return RunReconciliationSummary(
        scanned=len(receipts),
        registered=registered,
        already_registered=existing,
        errors=tuple(errors),
    )
