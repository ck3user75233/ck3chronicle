"""Guardrails for incremental empirical-template evidence and revisions."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "template_learning"
    / "incremental_template_registry.py"
)
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("incremental_template_registry", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
registry = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = registry
SPEC.loader.exec_module(registry)


def protected_log(runtime: Path, name: str, content: bytes) -> Path:
    path = runtime / "pending" / name / "error.log"
    path.parent.mkdir(parents=True)
    path.write_bytes(content)
    return path


def feature(item):
    label = item.path.read_text(encoding="utf-8").strip()
    return {
        "schema": registry.FEATURE_SCHEMA,
        "schema_version": registry.FEATURE_SCHEMA_VERSION,
        "normalizer_version": registry.learner.NORMALIZER_VERSION,
        "evidence_sha256": item.sha256,
        "bytes": item.bytes,
        "timestamped_blocks": 1,
        "eligible_occurrences": 1,
        "records": [
            {
                "source_family": "fixture.cpp",
                "tokens": ["Diagnostic", label],
                "semantic_lead": ["diagnostic", label.casefold()],
                "occurrences": 1,
                "examples": [f"Diagnostic {label}"],
                "location_evidence_examples": [],
                "structured_slot_examples": [],
            }
        ],
    }


def test_unchanged_protected_path_is_not_rehashed_or_reparsed(tmp_path):
    runtime, state = tmp_path / "runtime", tmp_path / "state"
    protected_log(runtime, "one", b"alpha")
    calls = {"hash": 0, "feature": 0}

    def hasher(path):
        calls["hash"] += 1
        return registry.learner.sha256_file(path)

    def builder(item):
        calls["feature"] += 1
        return feature(item)

    first = registry.sync_registry(runtime, state, hasher=hasher, feature_builder=builder)
    second = registry.sync_registry(runtime, state, hasher=hasher, feature_builder=builder)
    assert first["paths_hashed"] == first["new_feature_caches"] == 1
    assert second["paths_hashed"] == second["new_feature_caches"] == 0
    assert calls == {"hash": 1, "feature": 1}


def test_duplicate_content_is_one_evidence_parse_with_two_observations(tmp_path):
    runtime, state = tmp_path / "runtime", tmp_path / "state"
    protected_log(runtime, "one", b"alpha")
    calls = {"feature": 0}

    def builder(item):
        calls["feature"] += 1
        return feature(item)

    registry.sync_registry(runtime, state, feature_builder=builder)
    protected_log(runtime, "duplicate", b"alpha")
    result = registry.sync_registry(runtime, state, feature_builder=builder)
    saved = registry.load_registry(state)
    assert result["new_evidence"] == result["new_feature_caches"] == 0
    assert result["duplicate_observations"] == 1
    assert calls["feature"] == 1
    assert len(saved["evidence"]) == 1
    assert len(next(iter(saved["evidence"].values()))["observed_paths"]) == 2


def test_changed_protected_path_creates_new_candidate_evidence(tmp_path):
    runtime, state = tmp_path / "runtime", tmp_path / "state"
    path = protected_log(runtime, "one", b"alpha")
    registry.sync_registry(runtime, state, feature_builder=feature)
    path.write_bytes(b"beta-longer")
    result = registry.sync_registry(runtime, state, feature_builder=feature)
    saved = registry.load_registry(state)
    assert result["new_evidence"] == result["new_feature_caches"] == 1
    assert len(saved["evidence"]) == 2
    assert {row["role"] for row in saved["evidence"].values()} == {"candidate"}


def test_holdout_never_enters_training_and_revisions_are_idempotent(tmp_path):
    runtime, state = tmp_path / "runtime", tmp_path / "state"
    first = protected_log(runtime, "one", b"alpha")
    second = protected_log(runtime, "two", b"beta")
    registry.sync_registry(runtime, state, feature_builder=feature)
    first_sha = hashlib.sha256(first.read_bytes()).hexdigest()
    second_sha = hashlib.sha256(second.read_bytes()).hexdigest()
    registry.set_role(state, first_sha, "training")
    registry.set_role(state, second_sha, "holdout")

    revision_one = registry.build_revision(state, tmp_path / "missing-oracle")
    repeated = registry.build_revision(state, tmp_path / "missing-oracle")
    model_one = json.loads(Path(revision_one["model_path"]).read_text(encoding="utf-8"))
    saved = registry.load_registry(state)
    assert repeated["revision_id"] == revision_one["revision_id"]
    assert len(saved["revisions"]) == 1
    assert set(model_one["evidence"]) == {first_sha}
    assert model_one["excluded_evidence"] == [
        {"bytes": 4, "role": "holdout", "sha256": second_sha}
    ]

    registry.set_role(state, second_sha, "training")
    revision_two = registry.build_revision(state, tmp_path / "missing-oracle")
    model_two = json.loads(Path(revision_two["model_path"]).read_text(encoding="utf-8"))
    saved = registry.load_registry(state)
    assert revision_two["revision_id"] != revision_one["revision_id"]
    assert len(saved["revisions"]) == 2
    assert set(model_two["evidence"]) == {first_sha, second_sha}


def test_failed_feature_parse_does_not_publish_registry(tmp_path):
    runtime, state = tmp_path / "runtime", tmp_path / "state"
    protected_log(runtime, "one", b"alpha")

    def fail(_item):
        raise RuntimeError("injected parse failure")

    try:
        registry.sync_registry(runtime, state, feature_builder=fail)
    except RuntimeError as error:
        assert "injected" in str(error)
    else:
        raise AssertionError("failure injection did not fail")
    assert not (state / "registry.json").exists()
    result = registry.sync_registry(runtime, state, feature_builder=feature)
    assert result["new_feature_caches"] == 1


def test_corrupt_feature_cache_is_rejected(tmp_path):
    runtime, state = tmp_path / "runtime", tmp_path / "state"
    path = protected_log(runtime, "one", b"alpha")
    registry.sync_registry(runtime, state, feature_builder=feature)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    cache_path = registry.feature_cache_path(state, digest)
    cache_path.write_text("{}\n", encoding="utf-8")
    try:
        registry.sync_registry(runtime, state, feature_builder=feature)
    except ValueError as error:
        assert "hash mismatch" in str(error)
    else:
        raise AssertionError("corrupt cache was accepted")
