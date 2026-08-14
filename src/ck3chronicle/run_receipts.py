"""Durable, rebuildable run receipts kept outside evidence bundles.

Evidence archives are content-addressed and may be shared by several CK3
runs.  A run receipt is therefore an independent immutable record.  The
protected receipt is written immediately after copy-first capture; finalizing
adds the evidence-bundle identity before the pending directory is moved or
discarded.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


RUN_RECEIPT_VERSION = 1


class RunReceiptError(RuntimeError):
    """A durable run receipt is absent, malformed, or contradictory."""


def _canonical_bytes(payload: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def _receipt_root(root: Path) -> Path:
    return Path(root) / "run_receipts"


def protected_receipt_path(root: Path, capture_id: str) -> Path:
    return _receipt_root(root) / "protected" / f"{capture_id}.json"


def finalized_receipt_path(root: Path, capture_id: str) -> Path:
    return _receipt_root(root) / "finalized" / f"{capture_id}.json"


def _validate_capture_id(capture_id: str) -> str:
    value = str(capture_id).strip()
    if not value or value in {".", ".."} or Path(value).name != value:
        raise RunReceiptError("run receipt has an unsafe capture_id")
    return value


def _publish_immutable(path: Path, payload: Mapping[str, Any]) -> Path:
    """Publish canonical JSON exactly once and reject conflicting reuse."""
    data = _canonical_bytes(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise RunReceiptError(f"run receipt identity conflict: {path.name}")
        return path

    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            # A hard-link publish cannot replace a concurrent winner.
            os.link(temporary, path)
        except FileExistsError:
            if path.read_bytes() != data:
                raise RunReceiptError(
                    f"run receipt identity conflict: {path.name}"
                )
        return path
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def publish_protected_receipt(
    root: Path,
    *,
    capture_id: str,
    captured_at: str,
    pending_dir: Path,
    trigger: str,
    process: Mapping[str, Any] | None,
    observed_started_at: str | None = None,
    observed_ended_at: str | None = None,
    termination_kind: str = "unknown",
    crash: Mapping[str, Any] | None = None,
) -> Path:
    """Record one protected copy without hashing or touching SQLite."""
    safe_id = _validate_capture_id(capture_id)
    if termination_kind not in {"normal", "crash", "unknown"}:
        raise RunReceiptError("invalid run termination kind")
    payload = {
        "schema": "ck3chronicle.protected-run-receipt",
        "schema_version": RUN_RECEIPT_VERSION,
        "capture_id": safe_id,
        "status": "protected",
        "captured_at": captured_at,
        "pending_name": Path(pending_dir).name,
        "trigger": trigger,
        "process": dict(process) if process is not None else None,
        "observed_started_at": observed_started_at,
        "observed_ended_at": observed_ended_at or captured_at,
        "termination_kind": termination_kind,
        "crash": dict(crash) if crash is not None else None,
    }
    return _publish_immutable(protected_receipt_path(root, safe_id), payload)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RunReceiptError(f"cannot read run receipt: {path}") from exc
    if not isinstance(payload, dict):
        raise RunReceiptError(f"run receipt is not an object: {path}")
    return payload


def _legacy_last_capture(root: Path, pending_name: str) -> dict[str, Any] | None:
    path = Path(root) / "watch" / "last_capture.json"
    if not path.is_file():
        return None
    payload = _load_json(path)
    pending_dir = payload.get("pending_dir")
    if not isinstance(pending_dir, str) or Path(pending_dir).name != pending_name:
        return None
    return {
        "schema": "ck3chronicle.protected-run-receipt",
        "schema_version": RUN_RECEIPT_VERSION,
        "capture_id": pending_name,
        "status": "protected",
        "captured_at": payload.get("captured_at"),
        "pending_name": pending_name,
        "trigger": payload.get("trigger", "legacy_receipt"),
        "process": payload.get("process"),
        "observed_started_at": None,
        "observed_ended_at": payload.get("captured_at"),
        "termination_kind": "unknown",
        "crash": None,
    }


def finalize_run_receipt(
    root: Path,
    *,
    pending_name: str,
    evidence_bundle_hash: str,
    manifest_sha256: str,
    captured_at: str,
) -> Path:
    """Bind one run to evidence before its pending copy is moved or removed."""
    capture_id = _validate_capture_id(pending_name)
    protected_path = protected_receipt_path(root, capture_id)
    if protected_path.is_file():
        protected = _load_json(protected_path)
    else:
        protected = _legacy_last_capture(root, pending_name) or {
            "schema": "ck3chronicle.protected-run-receipt",
            "schema_version": RUN_RECEIPT_VERSION,
            "capture_id": capture_id,
            "status": "protected",
            "captured_at": captured_at,
            "pending_name": pending_name,
            "trigger": "unattributed_pending",
            "process": None,
            "observed_started_at": None,
            "observed_ended_at": captured_at,
            "termination_kind": "unknown",
            "crash": None,
        }
        _publish_immutable(protected_path, protected)

    if protected.get("capture_id") != capture_id:
        raise RunReceiptError("protected receipt capture_id disagrees")
    if protected.get("pending_name") != pending_name:
        raise RunReceiptError("protected receipt pending directory disagrees")
    finalized = {
        **protected,
        "schema": "ck3chronicle.finalized-run-receipt",
        "status": "finalized",
        "evidence_bundle_hash": evidence_bundle_hash,
        "manifest_sha256": manifest_sha256,
    }
    return _publish_immutable(finalized_receipt_path(root, capture_id), finalized)


def finalized_receipts(root: Path) -> tuple[tuple[Path, dict[str, Any]], ...]:
    directory = _receipt_root(root) / "finalized"
    if not directory.is_dir():
        return ()
    return tuple(
        (path, _load_json(path))
        for path in sorted(directory.glob("*.json"), key=lambda item: item.name)
        if path.is_file()
    )


def receipt_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

