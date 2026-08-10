"""Acceptance tests for finalized, content-addressed evidence capture."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

import ck3chronicle.harvester as harvester
from ck3chronicle.harvester import (
    ArchiveIntegrityError,
    InvalidCaptureInput,
    UnstableCapture,
    build_bundle,
    discover_logs,
    hash_file,
    snapshot,
    validate_snapshot,
)


def _complete_logs(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "error.log").write_bytes(b"error\x00\r\nsecond\n")
    (root / "debug.log").write_bytes(b"debug\r\n")
    (root / "game.log").write_bytes(b"game\n")
    return root


def _independent_bundle_hash(root: Path, names: list[str]) -> str:
    records = []
    for name in names:
        digest = hashlib.sha256((root / name).read_bytes()).hexdigest()
        records.append(f"log:{name}:{digest}")
    canonical = "\n".join(sorted(records)).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _final_dirs(archive: Path) -> list[Path]:
    sessions = archive / "sessions"
    if not sessions.exists():
        return []
    return [path for path in sessions.iterdir() if path.name != ".staging"]


def test_discover_logs_returns_only_existing(tmp_path: Path):
    (tmp_path / "error.log").write_text("test\n", encoding="utf-8")
    (tmp_path / "game.log").write_text("test\n", encoding="utf-8")
    names = {path.name for path in discover_logs(tmp_path)}
    assert names == {"error.log", "game.log"}


def test_missing_error_log_is_invalid_input(tmp_path: Path):
    (tmp_path / "debug.log").write_bytes(b"debug")
    with pytest.raises(InvalidCaptureInput, match="error.log"):
        build_bundle(tmp_path)


def test_zero_byte_error_log_is_valid_evidence(tmp_path: Path):
    (tmp_path / "error.log").write_bytes(b"")
    bundle = build_bundle(tmp_path)
    assert bundle.identities["log:error.log"].bytes == 0
    assert bundle.identities["log:error.log"].sha256 == hashlib.sha256(b"").hexdigest()


def test_hash_file_uses_exact_bytes(tmp_path: Path):
    path = tmp_path / "mixed.bin"
    path.write_bytes(b"a\r\nb\n\x00")
    assert hash_file(path) == hashlib.sha256(b"a\r\nb\n\x00").hexdigest()


def test_p1_cap_01_staged_bytes_hashes_sizes_and_manifest_match(tmp_path: Path):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    bundle = build_bundle(logs)
    expected_hash = _independent_bundle_hash(
        logs, ["error.log", "debug.log", "game.log"]
    )

    result = snapshot(bundle, archive)

    assert result.evidence_bundle_hash == expected_hash
    assert result.dest_dir.name == expected_hash
    assert result.files_copied == 3
    assert result.missing_principal_logs == ()
    for name in ("error.log", "debug.log", "game.log"):
        assert (result.dest_dir / name).read_bytes() == (logs / name).read_bytes()
    manifest = json.loads((result.dest_dir / "manifest.json").read_text("utf-8"))
    assert manifest["capture_status"] == "finalized"
    assert manifest["evidence_completeness"] == "complete"
    assert manifest["principal_logs"] == {
        "debug.log": "present",
        "error.log": "present",
        "game.log": "present",
    }
    validate_snapshot(result.dest_dir, expected_hash=expected_hash)


def test_p1_cap_02_identical_capture_is_idempotent_even_if_mtime_changes(
    tmp_path: Path,
):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    first = snapshot(build_bundle(logs), archive)
    original_manifest = (first.dest_dir / "manifest.json").read_bytes()
    for path in logs.iterdir():
        path.touch()

    second = snapshot(build_bundle(logs), archive)

    assert second.evidence_bundle_hash == first.evidence_bundle_hash
    assert second.was_existing is True
    assert second.files_copied == 0
    assert (second.dest_dir / "manifest.json").read_bytes() == original_manifest
    assert len(_final_dirs(archive)) == 1


def test_p1_cap_03_one_changed_byte_changes_file_and_bundle_hash(tmp_path: Path):
    logs = _complete_logs(tmp_path / "logs")
    first = build_bundle(logs)
    old_file_hash = first.identities["log:error.log"].sha256
    content = bytearray((logs / "error.log").read_bytes())
    content[-1] ^= 1
    (logs / "error.log").write_bytes(content)

    second = build_bundle(logs)

    assert second.identities["log:error.log"].sha256 != old_file_hash
    assert second.evidence_bundle_hash != first.evidence_bundle_hash


def test_p1_cap_04_source_mutation_during_copy_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    bundle = build_bundle(logs)
    real_copy = harvester._copy_exact
    mutated = False

    def copy_then_mutate(src: Path, dst: Path) -> None:
        nonlocal mutated
        real_copy(src, dst)
        if src.name == "error.log" and not mutated:
            mutated = True
            with src.open("ab") as stream:
                stream.write(b"changed")

    monkeypatch.setattr(harvester, "_copy_exact", copy_then_mutate)
    with pytest.raises(UnstableCapture, match="during copy"):
        snapshot(bundle, archive)

    assert _final_dirs(archive) == []
    assert list((archive / "sessions" / ".staging").iterdir()) == []


def test_p1_cap_05_copy_failure_leaves_no_finalized_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"

    def fail_copy(src: Path, dst: Path) -> None:
        raise OSError("injected copy failure")

    monkeypatch.setattr(harvester, "_copy_exact", fail_copy)
    with pytest.raises(OSError, match="injected"):
        snapshot(build_bundle(logs), archive)

    assert _final_dirs(archive) == []
    assert list((archive / "sessions" / ".staging").iterdir()) == []


def test_p1_cap_05_promotion_failure_leaves_no_finalized_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"

    def fail_promotion(source: Path, destination: Path) -> None:
        raise OSError("injected promotion failure")

    monkeypatch.setattr(harvester.os, "rename", fail_promotion)
    with pytest.raises(OSError, match="promotion"):
        snapshot(build_bundle(logs), archive)
    assert _final_dirs(archive) == []
    assert list((archive / "sessions" / ".staging").iterdir()) == []


def test_failed_post_promotion_verification_removes_new_bundle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"

    def fail_validation(directory: Path, *, expected_hash: str | None = None):
        raise ArchiveIntegrityError("injected verification failure")

    monkeypatch.setattr(harvester, "validate_snapshot", fail_validation)
    with pytest.raises(ArchiveIntegrityError, match="injected"):
        snapshot(build_bundle(logs), archive)
    assert _final_dirs(archive) == []


def test_partial_same_hash_destination_is_never_accepted(tmp_path: Path):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    bundle = build_bundle(logs)
    partial = archive / "sessions" / bundle.evidence_bundle_hash
    partial.mkdir(parents=True)
    (partial / "error.log").write_bytes(b"partial")

    with pytest.raises(ArchiveIntegrityError, match="legacy archive"):
        snapshot(bundle, archive)


def test_corrupt_existing_archive_is_never_a_duplicate(tmp_path: Path):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    first = snapshot(build_bundle(logs), archive)
    (first.dest_dir / "error.log").write_bytes(b"same size? no")

    with pytest.raises(ArchiveIntegrityError, match="hash mismatch"):
        snapshot(build_bundle(logs), archive)


def test_unlisted_file_invalidates_finalized_archive(tmp_path: Path):
    logs = _complete_logs(tmp_path / "logs")
    result = snapshot(build_bundle(logs), tmp_path / "archive")
    (result.dest_dir / "unlisted.log").write_bytes(b"not in manifest")
    with pytest.raises(ArchiveIntegrityError, match="unlisted"):
        validate_snapshot(result.dest_dir)


def test_missing_debug_is_explicit_partial_evidence(tmp_path: Path):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "error.log").write_bytes(b"")
    (logs / "game.log").write_bytes(b"game")
    result = snapshot(build_bundle(logs), tmp_path / "archive")
    manifest = json.loads((result.dest_dir / "manifest.json").read_text("utf-8"))

    assert result.missing_principal_logs == ("debug.log",)
    assert manifest["evidence_completeness"] == "partial"
    assert manifest["principal_logs"]["debug.log"] == "missing"


def test_manifestless_v1_archive_is_verified_and_adopted_in_place(tmp_path: Path):
    logs = _complete_logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    bundle = build_bundle(logs)
    legacy = archive / "sessions" / bundle.evidence_bundle_hash
    legacy.mkdir(parents=True)
    for source in bundle.log_files:
        shutil.copy2(source, legacy / source.name)

    result = snapshot(bundle, archive)

    assert result.was_existing is True
    assert result.dest_dir == legacy
    assert (legacy / "manifest.json").is_file()
    validate_snapshot(legacy, expected_hash=bundle.evidence_bundle_hash)


def test_late_byte_change_in_large_log_changes_identity(tmp_path: Path):
    logs = _complete_logs(tmp_path / "logs")
    large = bytearray(b"x" * (4 * 1024 * 1024))
    (logs / "error.log").write_bytes(large)
    first = build_bundle(logs).evidence_bundle_hash
    large[-1] = ord("y")
    (logs / "error.log").write_bytes(large)
    assert build_bundle(logs).evidence_bundle_hash != first
