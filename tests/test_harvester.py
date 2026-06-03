"""Tests for ck3chronicle.harvester."""
from __future__ import annotations

from pathlib import Path

import pytest

from ck3chronicle.harvester import (
    EvidenceBundle,
    SnapshotResult,
    build_bundle,
    discover_logs,
    hash_file,
    snapshot,
)


def test_discover_logs_returns_only_existing(tmp_path: Path):
    (tmp_path / "error.log").write_text("test\n", encoding="utf-8")
    (tmp_path / "game.log").write_text("test\n", encoding="utf-8")
    result = discover_logs(tmp_path)
    names = {p.name for p in result}
    assert "error.log" in names
    assert "game.log" in names
    assert "debug.log" not in names


def test_discover_logs_empty_dir(tmp_path: Path):
    result = discover_logs(tmp_path)
    assert result == []


def test_hash_file_consistent(tmp_path: Path):
    f = tmp_path / "test.txt"
    f.write_text("hello world\n", encoding="utf-8")
    h1 = hash_file(f)
    h2 = hash_file(f)
    assert h1 == h2
    assert len(h1) == 64  # SHA-256 hex digest length


def test_hash_file_different_content(tmp_path: Path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("aaa", encoding="utf-8")
    f2.write_text("bbb", encoding="utf-8")
    assert hash_file(f1) != hash_file(f2)


def test_build_bundle_minimal(fixture_logs_minimal: Path):
    bundle = build_bundle(fixture_logs_minimal)
    assert bundle.log_files
    assert bundle.crash_folder is None
    assert bundle.crash_files == []
    assert len(bundle.evidence_bundle_hash) == 64


def test_build_bundle_with_crash(fixture_logs_with_crash: Path):
    bundle = build_bundle(fixture_logs_with_crash)
    assert bundle.log_files
    assert bundle.crash_folder is not None
    assert bundle.crash_files


def test_snapshot_copies_files(fixture_logs_with_crash: Path, tmp_path: Path):
    bundle = build_bundle(fixture_logs_with_crash)
    result = snapshot(bundle, tmp_path)
    assert not result.was_existing
    assert result.files_copied > 0
    assert result.dest_dir.exists()
    # Log files should be present
    for f in bundle.log_files:
        assert (result.dest_dir / f.name).exists()


def test_snapshot_idempotent(fixture_logs_with_crash: Path, tmp_path: Path):
    bundle = build_bundle(fixture_logs_with_crash)
    r1 = snapshot(bundle, tmp_path)
    r2 = snapshot(bundle, tmp_path)
    assert r1.evidence_bundle_hash == r2.evidence_bundle_hash
    assert r2.was_existing is True
    assert r2.files_copied == 0


def test_bundle_hash_differs_if_content_changes(tmp_path: Path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    (log_dir / "error.log").write_text("content A\n", encoding="utf-8")
    b1 = build_bundle(log_dir)

    (log_dir / "error.log").write_text("content B\n", encoding="utf-8")
    b2 = build_bundle(log_dir)

    assert b1.evidence_bundle_hash != b2.evidence_bundle_hash
