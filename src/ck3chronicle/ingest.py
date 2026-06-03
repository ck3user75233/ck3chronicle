"""Ingest pipeline: build evidence bundle, dedupe, persist."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import config
from .harvester import build_bundle, hash_file, snapshot
from .db import repository


@dataclass
class IngestResult:
    session_id: int
    evidence_bundle_hash: str
    was_duplicate: bool
    forced_duplicate_of: int | None = None
    log_count: int = 0
    crash_count: int = 0
    total_files: int = 0


def _db_path() -> Path:
    return config.ROOT_CK3CHRONICLE / "ck3chronicle.db"


def ingest(logs_root: Path | None = None, force: bool = False) -> IngestResult:
    """Ingest a CK3 evidence bundle into the session registry.

    Args:
        logs_root: Path to CK3 logs folder.  Defaults to config.ROOT_LOGS.
        force: Re-ingest even if the bundle hash already exists, creating a
               second session row with forced_duplicate_of set.

    Returns:
        IngestResult with session_id and metadata.
    """
    root = logs_root if logs_root is not None else config.ROOT_LOGS
    bundle = build_bundle(root)

    db_path = _db_path()
    conn = repository.open_db(db_path)

    existing = repository.get_session_by_hash(conn, bundle.evidence_bundle_hash)
    if existing and not force:
        conn.close()
        return IngestResult(
            session_id=existing["session_id"],
            evidence_bundle_hash=bundle.evidence_bundle_hash,
            was_duplicate=True,
            log_count=existing["log_count"],
            crash_count=int(existing["crash_present"]),
            total_files=existing["log_count"] + int(existing["crash_present"]),
        )

    # Snapshot to durable storage (idempotent)
    snapshot(bundle, config.ROOT_CK3CHRONICLE)

    total_bytes = sum(f.stat().st_size for f in bundle.log_files)
    total_bytes += sum(f.stat().st_size for f in bundle.crash_files)
    crash_present = len(bundle.crash_files) > 0
    crash_count = len(bundle.crash_files)

    # For forced duplicates: generate a unique hash so the UNIQUE constraint holds
    forced_duplicate_of: int | None = None
    hash_to_use = bundle.evidence_bundle_hash
    if existing and force:
        forced_duplicate_of = existing["session_id"]
        hash_to_use = hashlib.sha256(
            f"{bundle.evidence_bundle_hash}:forced:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()

    session_id = repository.create_session(
        conn=conn,
        evidence_bundle_hash=hash_to_use,
        log_count=len(bundle.log_files),
        crash_present=crash_present,
        total_bytes=total_bytes,
        forced_duplicate_of=forced_duplicate_of,
    )

    for src in bundle.log_files:
        repository.add_session_file(
            conn,
            session_id=session_id,
            rel_path=src.name,
            sha256=hash_file(src),
            bytes_=src.stat().st_size,
            kind="log",
        )
    if bundle.crash_folder and bundle.crash_files:
        for src in bundle.crash_files:
            rel = str(src.relative_to(bundle.crash_folder))
            repository.add_session_file(
                conn,
                session_id=session_id,
                rel_path=rel,
                sha256=hash_file(src),
                bytes_=src.stat().st_size,
                kind="crash_artifact",
            )

    conn.close()
    total_files = len(bundle.log_files) + len(bundle.crash_files)
    return IngestResult(
        session_id=session_id,
        evidence_bundle_hash=hash_to_use,
        was_duplicate=False,
        forced_duplicate_of=forced_duplicate_of,
        log_count=len(bundle.log_files),
        crash_count=crash_count,
        total_files=total_files,
    )
