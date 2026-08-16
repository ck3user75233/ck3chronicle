"""Project immutable run receipts and crash-source provenance into SQLite."""
from __future__ import annotations

import os
import shutil
import sqlite3
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .db import repository
from .harvester import ArchiveIntegrityError, PRINCIPAL_LOG_NAMES, hash_file
from .run_receipts import (
    CRASH_EXCEPTION_NAME,
    RunReceiptError,
    SUPPORTED_RUN_RECEIPT_VERSIONS,
    finalized_receipts,
    receipt_sha256,
)


@dataclass(frozen=True)
class RunReconciliationSummary:
    scanned: int
    registered: int
    already_registered: int
    errors: tuple[str, ...]


SQLITE_INTEGER_MAX = (1 << 63) - 1


def _required_text(payload: dict[str, Any], name: str) -> str:
    value = payload.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"run receipt has invalid {name}")
    return value


def _optional_text(
    payload: dict[str, Any], name: str, *, context: str = "run receipt"
) -> str | None:
    value = payload.get(name)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} has invalid {name}")
    return value


def _optional_integer(
    payload: dict[str, Any], name: str, *, context: str = "run receipt"
) -> int | None:
    value = payload.get(name)
    if value is None:
        return None
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value < 0
        or value > SQLITE_INTEGER_MAX
    ):
        raise ValueError(f"{context} has invalid {name}")
    return value


def _optional_object(payload: dict[str, Any], name: str) -> dict[str, Any] | None:
    value = payload.get(name)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"run receipt has invalid {name}")
    return value


def _exception_projection(
    payload: dict[str, Any],
    root: Path,
    *,
    capture_id: str,
    termination_kind: str,
) -> dict[str, Any]:
    """Validate one protected exception descriptor without reading CK3 live data."""
    version = payload.get("schema_version")
    if isinstance(version, bool) or not isinstance(version, int):
        raise ValueError("run receipt has invalid schema_version")
    if version == 1:
        return {
            "status": (
                "not_applicable" if termination_kind == "normal" else "unavailable"
            ),
            "source_rel_path": (
                CRASH_EXCEPTION_NAME if termination_kind == "crash" else None
            ),
            "retained_path": None,
            "sha256": None,
            "bytes": None,
            "source_mtime_ns": None,
        }

    descriptor = payload.get("crash_exception")
    if not isinstance(descriptor, dict):
        raise ValueError("run receipt has no crash exception descriptor")
    status = descriptor.get("status")
    if status not in {"captured", "absent", "unavailable", "not_applicable"}:
        raise ValueError("run receipt has invalid crash exception status")
    if termination_kind == "crash" and status == "not_applicable":
        raise ValueError("crash run marks exception evidence not applicable")
    if termination_kind == "normal" and status != "not_applicable":
        raise ValueError("normal run has contradictory crash exception status")

    source_rel_path = descriptor.get("source_rel_path")
    retained_path = descriptor.get("retained_path")
    sha256 = descriptor.get("sha256")
    bytes_ = descriptor.get("bytes")
    source_mtime_ns = descriptor.get("source_mtime_ns")
    if source_rel_path != CRASH_EXCEPTION_NAME:
        raise ValueError("crash exception source path is invalid")
    if status == "captured":
        expected = (
            Path("crash_evidence") / capture_id / CRASH_EXCEPTION_NAME
        ).as_posix()
        if source_rel_path != CRASH_EXCEPTION_NAME or retained_path != expected:
            raise ValueError("crash exception path is not bound to this run")
        if (
            not isinstance(sha256, str)
            or len(sha256) != 64
            or sha256 != sha256.lower()
            or any(character not in "0123456789abcdef" for character in sha256)
        ):
            raise ValueError("crash exception hash is invalid")
        if (
            isinstance(bytes_, bool)
            or not isinstance(bytes_, int)
            or bytes_ < 0
            or bytes_ > SQLITE_INTEGER_MAX
        ):
            raise ValueError("crash exception byte count is invalid")
        if (
            isinstance(source_mtime_ns, bool)
            or not isinstance(source_mtime_ns, int)
            or source_mtime_ns < 0
            or source_mtime_ns > SQLITE_INTEGER_MAX
        ):
            raise ValueError("crash exception source timestamp is invalid")
        retained = Path(root) / Path(retained_path)
        if retained.is_symlink() or not retained.is_file():
            raise ValueError("captured crash exception is missing")
        if retained.stat().st_size != bytes_ or hash_file(retained) != sha256:
            raise ValueError("captured crash exception fails integrity verification")
    elif any(
        value is not None
        for value in (retained_path, sha256, bytes_, source_mtime_ns)
    ):
        raise ValueError("uncaptured crash exception has retained metadata")

    return {
        "status": status,
        "source_rel_path": source_rel_path,
        "retained_path": retained_path,
        "sha256": sha256,
        "bytes": bytes_,
        "source_mtime_ns": source_mtime_ns,
    }


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
    root: Path,
    db_path: Path,
    *,
    strict_integrity: bool = False,
) -> RunReconciliationSummary:
    """Rebuild the run index from finalized receipt files idempotently."""
    evidence_root = Path(root)
    try:
        receipts = finalized_receipts(evidence_root)
    except (
        OSError,
        UnicodeError,
        ValueError,
        TypeError,
        RunReceiptError,
    ) as exc:
        if strict_integrity:
            raise ArchiveIntegrityError(
                f"invalid finalized run receipt: {exc}"
            ) from exc
        return RunReconciliationSummary(
            scanned=0,
            registered=0,
            already_registered=0,
            errors=(str(exc),),
        )
    registered = 0
    existing = 0
    errors: list[str] = []
    conn = repository.open_db(db_path)
    try:
        receipt_ids = {path.stem for path, _payload in receipts}
        indexed_receipts = conn.execute(
            """
            SELECT capture_id
            FROM capture_observations
            WHERE receipt_sha256 IS NOT NULL
            ORDER BY capture_id
            """
        ).fetchall()
        for row in indexed_receipts:
            capture_id = str(row["capture_id"])
            if capture_id not in receipt_ids:
                message = f"{capture_id}: indexed run is missing its finalized receipt"
                if strict_integrity:
                    raise ArchiveIntegrityError(message)
                errors.append(message)
        for path, payload in receipts:
            capture_id = path.stem
            try:
                if payload.get("schema") != "ck3chronicle.finalized-run-receipt":
                    raise ValueError("unexpected run receipt schema")
                schema_version = payload.get("schema_version")
                if (
                    isinstance(schema_version, bool)
                    or not isinstance(schema_version, int)
                    or schema_version not in SUPPORTED_RUN_RECEIPT_VERSIONS
                ):
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
                process = _optional_object(payload, "process") or {}
                crash = _optional_object(payload, "crash")
                process_name = _optional_text(
                    process, "image_name", context="run receipt process"
                )
                process_pid = _optional_integer(
                    process, "pid", context="run receipt process"
                )
                process_started_ns = _optional_integer(
                    process, "started_ns", context="run receipt process"
                )
                observed_started_at = _optional_text(payload, "observed_started_at")
                observed_ended_at = _optional_text(payload, "observed_ended_at")
                crash_folder_name = (
                    _optional_text(crash, "folder_name", context="run receipt crash")
                    if crash is not None
                    else None
                )
                crash_folder_path = (
                    _optional_text(crash, "folder_path", context="run receipt crash")
                    if crash is not None
                    else None
                )
                crash_detected_at = (
                    _optional_text(crash, "detected_at", context="run receipt crash")
                    if crash is not None
                    else None
                )
                crash_association_method = (
                    _optional_text(
                        crash, "association_method", context="run receipt crash"
                    )
                    if crash is not None
                    else None
                )
                crash_association_confidence = (
                    _optional_text(crash, "confidence", context="run receipt crash")
                    if crash is not None
                    else None
                )
                termination_kind = str(payload.get("termination_kind", "unknown"))
                if termination_kind not in {"normal", "crash", "unknown"}:
                    raise ValueError("run receipt has invalid termination_kind")
                exception = _exception_projection(
                    payload,
                    evidence_root,
                    capture_id=capture_id,
                    termination_kind=termination_kind,
                )
                observation_id, was_existing = repository.register_run(
                    conn,
                    session_id=int(session["session_id"]),
                    capture_id=capture_id,
                    trigger=_required_text(payload, "trigger"),
                    process_name=process_name,
                    observed_at=_required_text(payload, "captured_at"),
                    observed_started_at=observed_started_at,
                    observed_ended_at=observed_ended_at,
                    process_pid=process_pid,
                    process_started_ns=process_started_ns,
                    termination_kind=termination_kind,
                    crash_folder_name=crash_folder_name,
                    crash_folder_path=crash_folder_path,
                    crash_detected_at=crash_detected_at,
                    crash_association_method=crash_association_method,
                    crash_association_confidence=crash_association_confidence,
                    crash_exception_status=exception["status"],
                    crash_exception_source_rel_path=exception["source_rel_path"],
                    crash_exception_retained_path=exception["retained_path"],
                    crash_exception_sha256=exception["sha256"],
                    crash_exception_bytes=exception["bytes"],
                    crash_exception_source_mtime_ns=exception[
                        "source_mtime_ns"
                    ],
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
            except sqlite3.Error:
                raise
            except (
                OSError,
                UnicodeError,
                ValueError,
                TypeError,
                RunReceiptError,
            ) as exc:
                if strict_integrity:
                    raise ArchiveIntegrityError(
                        f"{path.name}: {exc}"
                    ) from exc
                errors.append(f"{path.name}: {exc}")
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
