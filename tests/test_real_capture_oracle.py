"""Opt-in P1 capture gates against the restricted frozen real-session corpus."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from ck3chronicle.harvester import LOG_NAMES, build_bundle, snapshot, validate_snapshot


ORACLE_BUNDLE_HASH = "63e97b752bb362308f09baa019515fdb84fe05f5e39dcc84089ae499474180f1"
ORACLE_TOTAL_BYTES = 34_265_910
ORACLE_HASHES = {
    "database_conflicts.log": "a08557563f353b539297da8727d7f547cdfdcd5a88f22b4e9217d0793328f1b4",
    "debug.log": "b8c6b4f3fc55c66c1b9b5c45323d80a4bee3c0ec928579f27ca5db54699f8862",
    "error.log": "675216ebb2dbcd8b24bc0bb15474616826c923781be463ea22a9a5da1042b2bf",
    "game.log": "2bdbf581a79791a815642d52ade7c34fdf67c1b293f1e8913958ce51f8072077",
    "setup.log": "d25ca3a8b8d997ec4e8a93a68f56f2612539fc7b4757a9309ce0c7ca96c3c545",
    "text.log": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}


def _oracle_root() -> Path:
    value = os.environ.get("CK3CHRONICLE_CAPTURE_ORACLE")
    if not value:
        pytest.skip("restricted real capture oracle not configured")
    root = Path(value)
    if not root.is_dir():
        pytest.skip("configured real capture oracle is unavailable")
    return root


def test_p1_cap_01_real_six_file_oracle_exact_bytes(tmp_path: Path):
    root = _oracle_root()
    bundle = build_bundle(root)
    result = snapshot(bundle, tmp_path / "archive")

    assert result.evidence_bundle_hash == ORACLE_BUNDLE_HASH
    assert len(result.files) == 6
    assert sum(item.bytes for item in result.files) == ORACLE_TOTAL_BYTES
    assert {
        item.identity_path: item.sha256 for item in result.files if item.kind == "log"
    } == ORACLE_HASHES
    validate_snapshot(result.dest_dir, expected_hash=ORACLE_BUNDLE_HASH)


def test_p1_cap_03_each_real_file_mutation_changes_bundle_identity(tmp_path: Path):
    root = _oracle_root()
    baseline = build_bundle(root)
    assert baseline.evidence_bundle_hash == ORACLE_BUNDLE_HASH

    for name in LOG_NAMES:
        mutated_root = tmp_path / name.removesuffix(".log")
        shutil.copytree(root, mutated_root)
        path = mutated_root / name
        data = bytearray(path.read_bytes())
        if data:
            data[-1] ^= 1
        else:
            data.append(1)
        path.write_bytes(data)
        mutated = build_bundle(mutated_root)
        assert mutated.identities[f"log:{name}"].sha256 != ORACLE_HASHES[name]
        assert mutated.evidence_bundle_hash != ORACLE_BUNDLE_HASH
