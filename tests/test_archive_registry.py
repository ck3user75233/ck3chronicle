"""Compatibility tests for archive/registry reconciliation."""
from __future__ import annotations

import shutil
import hashlib
from pathlib import Path

import pytest

from ck3chronicle.archive_registry import reconcile_archives
from ck3chronicle.db import repository
from ck3chronicle.harvester import build_bundle, read_snapshot
from ck3chronicle.ingest import ingest
from ck3chronicle.parser.service import ErrorLogEvidenceError, parse_session


def test_pre_p1_crash_row_is_verified_and_normalized(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "error.log").write_bytes(b"error")
    (source / "game.log").write_bytes(b"game")
    crash_source = source / "crash"
    crash_source.mkdir()
    (crash_source / "dump.txt").write_bytes(b"crash")
    bundle = build_bundle(source)

    archive = tmp_path / "archive"
    legacy_dir = archive / "sessions" / bundle.evidence_bundle_hash
    (legacy_dir / "crash").mkdir(parents=True)
    for log in bundle.log_files:
        shutil.copy2(log, legacy_dir / log.name)
    shutil.copy2(crash_source / "dump.txt", legacy_dir / "crash" / "dump.txt")

    db_path = archive / "ck3chronicle.db"
    conn = repository.open_db(db_path)
    session_id = repository.create_session(
        conn,
        bundle.evidence_bundle_hash,
        log_count=2,
        crash_present=True,
        total_bytes=sum(path.stat().st_size for path in bundle.log_files)
        + (crash_source / "dump.txt").stat().st_size,
    )
    for log in bundle.log_files:
        repository.add_session_file(
            conn,
            session_id,
            log.name,
            bundle.identities[f"log:{log.name}"].sha256,
            log.stat().st_size,
            "log",
        )
    repository.add_session_file(
        conn,
        session_id,
        "dump.txt",
        bundle.identities["crash:dump.txt"].sha256,
        (crash_source / "dump.txt").stat().st_size,
        "crash_artifact",
    )
    conn.execute(
        """
        UPDATE sessions
        SET capture_status='legacy_unverified',
            capture_manifest_version=NULL,
            capture_manifest_sha256=NULL
        WHERE session_id=?
        """,
        (session_id,),
    )
    conn.commit()
    conn.close()

    summary = reconcile_archives(archive, db_path)

    assert summary.errors == ()
    assert summary.adopted_legacy == 1
    read_snapshot(legacy_dir)
    conn = repository.open_db(db_path)
    session = conn.execute(
        "SELECT capture_status, capture_manifest_version FROM sessions WHERE session_id=?",
        (session_id,),
    ).fetchone()
    rows = conn.execute(
        "SELECT rel_path, kind FROM session_files WHERE session_id=? ORDER BY rel_path",
        (session_id,),
    ).fetchall()
    conn.close()
    assert tuple(session) == ("finalized", 1)
    assert ("crash/dump.txt", "crash") in [tuple(row) for row in rows]


def test_parser_rejects_legacy_unverified_session(tmp_path: Path):
    archive = tmp_path / "archive"
    db_path = archive / "ck3chronicle.db"
    conn = repository.open_db(db_path)
    session_id = repository.create_session(
        conn, "a" * 64, log_count=1, crash_present=False, total_bytes=0
    )
    repository.add_session_file(
        conn,
        session_id,
        "error.log",
        hashlib.sha256(b"").hexdigest(),
        0,
        "log",
    )
    conn.execute(
        "UPDATE sessions SET capture_status='legacy_unverified' WHERE session_id=?",
        (session_id,),
    )
    conn.commit()

    with pytest.raises(ErrorLogEvidenceError, match="finalized"):
        parse_session(conn, archive, session_id)
    conn.close()


def test_full_reconcile_rehashes_registered_archive_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    import ck3chronicle.config as config

    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "error.log").write_bytes(b"error")
    (logs / "game.log").write_bytes(b"game")
    archive = tmp_path / "archive"
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", archive)
    captured = ingest(logs_root=logs)
    (captured.archive_dir / "error.log").write_bytes(b"corrupt")

    summary = reconcile_archives(
        archive, archive / "ck3chronicle.db", full_verify=True
    )
    assert any("hash mismatch" in error for error in summary.errors)
