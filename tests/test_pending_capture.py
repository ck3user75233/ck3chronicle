"""Acceptance tests for immediate copy-first CK3 session protection."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

import ck3chronicle.harvester as harvester
from ck3chronicle.harvester import (
    UnstableCapture,
    finalize_pending,
    finalize_pending_captures,
    spool_logs,
)


def _logs(root: Path) -> Path:
    root.mkdir()
    (root / "error.log").write_bytes(b"error evidence")
    (root / "debug.log").write_bytes(b"debug evidence")
    (root / "game.log").write_bytes(b"game evidence")
    return root


def test_spool_copies_priority_logs_without_hashing_or_sqlite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    logs = _logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    copied: list[str] = []
    real_copy2 = shutil.copy2

    def copy2(source: Path, target: Path):
        copied.append(Path(source).name)
        return real_copy2(source, target)

    monkeypatch.setattr(harvester.shutil, "copy2", copy2)
    monkeypatch.setattr(
        harvester,
        "hash_file",
        lambda path: pytest.fail(f"urgent spool hashed {path}"),
    )

    pending = spool_logs(logs, archive, abort_if=lambda: False)

    assert copied == ["error.log", "debug.log", "game.log"]
    assert pending.file_names == tuple(copied)
    assert pending.dest_dir.parent == archive / "pending"
    assert not pending.dest_dir.name.startswith(".")
    assert not (archive / "sessions").exists()
    assert not (archive / "ck3chronicle.db").exists()
    for name in copied:
        assert (pending.dest_dir / name).read_bytes() == (logs / name).read_bytes()


def test_restart_during_copy_leaves_only_incomplete_copying_directory(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    probes = iter([False, True])

    with pytest.raises(UnstableCapture, match="restarted"):
        spool_logs(logs, archive, abort_if=lambda: next(probes))

    entries = list((archive / "pending").iterdir())
    assert len(entries) == 1
    assert entries[0].name.startswith(".copying-")
    assert finalize_pending_captures(archive) == ()
    assert not (archive / "sessions").exists()


def test_deferred_finalize_hashes_only_private_copies(tmp_path: Path, monkeypatch):
    logs = _logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    pending = spool_logs(logs, archive, abort_if=lambda: False)
    real_hash = harvester.hash_file
    hashed: list[Path] = []

    def hash_private(path: Path) -> str:
        path = Path(path)
        hashed.append(path)
        assert pending.dest_dir in path.parents
        assert logs not in path.parents
        return real_hash(path)

    monkeypatch.setattr(harvester, "hash_file", hash_private)
    result = finalize_pending(pending.dest_dir, archive)

    assert {path.name for path in hashed} == {
        "error.log",
        "debug.log",
        "game.log",
    }
    assert result.dest_dir.parent == archive / "sessions"
    assert result.dest_dir.name == result.evidence_bundle_hash
    assert (result.dest_dir / "manifest.json").is_file()
    assert not pending.dest_dir.exists()
    assert not (archive / "ck3chronicle.db").exists()


def test_duplicate_pending_copy_reuses_one_final_archive(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    first_pending = spool_logs(logs, archive, abort_if=lambda: False)
    second_pending = spool_logs(logs, archive, abort_if=lambda: False)

    first = finalize_pending(first_pending, archive)
    second = finalize_pending(second_pending.dest_dir, archive)

    assert first.was_existing is False
    assert second.was_existing is True
    assert first.evidence_bundle_hash == second.evidence_bundle_hash
    finalized = [
        path
        for path in (archive / "sessions").iterdir()
        if path.name != ".staging"
    ]
    assert finalized == [first.dest_dir]
    assert not second_pending.dest_dir.exists()


def test_complete_pending_copy_survives_until_explicit_finalization(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    pending = spool_logs(logs, archive, abort_if=lambda: False)

    recovered = finalize_pending_captures(archive)

    assert len(recovered) == 1
    assert recovered[0].files_copied == 3
    assert not pending.dest_dir.exists()
