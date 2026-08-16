"""Fresh reboot acceptance tests for pending finalization and registration."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from ck3chronicle import harvester
from ck3chronicle.archive_registry import reconcile_archives
from ck3chronicle.db import repository
from ck3chronicle.harvester import (
    ArchiveIntegrityError,
    MANIFEST_VERSION,
    finalize_pending,
    spool_logs,
    validate_snapshot,
)

from foundation_oracle import (
    SIX_LOG_BUNDLE_SHA256,
    SIX_LOG_BYTES,
    SIX_LOG_SHA256,
    write_logs,
)


def _finalized(tmp_path: Path):
    logs = tmp_path / "live-logs"
    runtime = tmp_path / "runtime"
    write_logs(logs)
    pending = spool_logs(logs, runtime, abort_if=lambda: False)
    return runtime, finalize_pending(pending, runtime)


def test_rarch_001_finalization_matches_independent_six_file_oracle(
    tmp_path: Path,
) -> None:
    """Oracle: literal bytes produce the precomputed hashes and bundle identity."""
    runtime, result = _finalized(tmp_path)

    assert result.evidence_bundle_hash == SIX_LOG_BUNDLE_SHA256
    assert result.dest_dir == runtime / "sessions" / SIX_LOG_BUNDLE_SHA256
    assert result.was_existing is False
    assert {item.identity_path: item.sha256 for item in result.files} == SIX_LOG_SHA256
    assert {item.identity_path: item.bytes for item in result.files} == {
        name: len(data) for name, data in SIX_LOG_BYTES.items()
    }
    for name, expected in SIX_LOG_BYTES.items():
        assert (result.dest_dir / name).read_bytes() == expected

    manifest = json.loads((result.dest_dir / "manifest.json").read_text("utf-8"))
    assert manifest["manifest_version"] == 1
    assert manifest["capture_status"] == "finalized"
    assert manifest["evidence_bundle_hash"] == SIX_LOG_BUNDLE_SHA256
    assert manifest["principal_logs"] == {
        "debug.log": "present",
        "error.log": "present",
        "game.log": "present",
    }


def test_rarch_002_finalization_hashes_each_protected_file_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Oracle: six files require six content reads for SHA-256, not repeated scans."""
    logs = tmp_path / "live-logs"
    runtime = tmp_path / "runtime"
    write_logs(logs)
    pending = spool_logs(logs, runtime, abort_if=lambda: False)
    original = harvester.hash_file
    calls: list[str] = []

    def counted(path: Path) -> str:
        calls.append(path.name)
        return original(path)

    monkeypatch.setattr(harvester, "hash_file", counted)
    finalize_pending(pending, runtime)

    assert calls == list(SIX_LOG_BYTES)


def test_rarch_003_identical_pending_content_reuses_one_archive(tmp_path: Path) -> None:
    """Oracle: identical evidence has one archive identity and no duplicate copy."""
    logs = tmp_path / "live-logs"
    runtime = tmp_path / "runtime"
    write_logs(logs)

    first = finalize_pending(spool_logs(logs, runtime), runtime)
    second = finalize_pending(spool_logs(logs, runtime), runtime)

    assert first.dest_dir == second.dest_dir
    assert second.was_existing is True
    assert [path.name for path in (runtime / "sessions").iterdir()] == [
        SIX_LOG_BUNDLE_SHA256
    ]
    assert list((runtime / "pending").iterdir()) == []


def test_rarch_004_registration_rolls_back_session_and_files_together(
    tmp_path: Path,
) -> None:
    """Oracle: a file-row failure leaves neither a session nor a partial manifest."""
    runtime, result = _finalized(tmp_path)
    conn = repository.open_db(runtime / "ck3chronicle.db")
    conn.execute(
        """
        CREATE TRIGGER reboot_reject_session_file
        BEFORE INSERT ON session_files
        BEGIN
            SELECT RAISE(ABORT, 'reboot injected file failure');
        END
        """
    )
    conn.commit()

    with pytest.raises(Exception, match="reboot injected file failure"):
        repository.register_finalized_session(
            conn,
            evidence_bundle_hash=result.evidence_bundle_hash,
            captured_at="2026-08-13T00:00:00+00:00",
            manifest_version=MANIFEST_VERSION,
            manifest_sha256=result.manifest_sha256,
            evidence_completeness="complete",
            files=result.files,
        )

    assert conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM session_files").fetchone()[0] == 0
    conn.close()


def test_rarch_005_changed_archived_byte_is_detected(tmp_path: Path) -> None:
    """Oracle: manifest validation fails after any retained artifact is altered."""
    _runtime, result = _finalized(tmp_path)
    game_log = result.dest_dir / "game.log"
    game_log.write_bytes(game_log.read_bytes() + b"changed")

    with pytest.raises(ArchiveIntegrityError):
        validate_snapshot(result.dest_dir)


def test_rarch_006_strict_reconcile_does_not_downgrade_sqlite_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    runtime, _result = _finalized(tmp_path)

    def database_failure(*_args, **_kwargs):
        raise sqlite3.OperationalError("injected registry failure")

    monkeypatch.setattr(
        repository,
        "register_finalized_session",
        database_failure,
    )
    with pytest.raises(sqlite3.OperationalError, match="injected registry failure"):
        reconcile_archives(
            runtime,
            runtime / "ck3chronicle.db",
            strict_integrity=True,
        )
