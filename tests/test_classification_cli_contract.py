"""Functional CLI contracts for classification and human review queues."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.classification.catalog import (
    APPROVED_MODEL_REVISION,
    APPROVED_MODEL_SHA256,
    APPROVED_PROJECTION_CATALOG_REVISION,
    APPROVED_PROJECTION_CATALOG_SHA256,
)
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository

from test_classification_persistence_contract import _session


def test_rclasscli_001_classify_json_is_schema_versioned_and_deterministic(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, _captured, conn, session_id = _session(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    parser = build_parser()

    first_args = parser.parse_args(
        ["classify", "--session", str(session_id), "--json"]
    )
    assert first_args.func(first_args) == 0
    first = json.loads(capsys.readouterr().out)
    assert first == {
        "classification_contract_version": "2.0.1",
        "classification_mutated": True,
        "counts": {
            "full": 4,
            "l1": 1,
            "l1_l2": 0,
            "semantic_occurrences": 5,
            "source_blocks": 3,
            "unknown": 0,
        },
        "model_revision_id": APPROVED_MODEL_REVISION,
        "model_sha256": APPROVED_MODEL_SHA256,
        "mutated": True,
        "run_id": first["run_id"],
        "schema": "ck3chronicle.classification-run",
        "schema_version": 2,
        "semantic_projection": {
            "catalog_revision_id": APPROVED_PROJECTION_CATALOG_REVISION,
            "catalog_sha256": APPROVED_PROJECTION_CATALOG_SHA256,
            "contract_version": "1.0.0",
            "counts": {
                "issue_clusters": first["semantic_projection"]["counts"][
                    "issue_clusters"
                ],
                "multi_issue_blocks": 1,
                "semantic_occurrences": 5,
                "source_blocks": 3,
                "unclassified_occurrences": 1,
            },
            "mutated": True,
            "run_id": first["semantic_projection"]["run_id"],
        },
        "session_id": session_id,
    }

    conn = repository.open_db_readonly(runtime / "ck3chronicle.db")
    try:
        assert repository.get_semantic_projection_run(conn, session_id) is not None
    finally:
        conn.close()

    second_args = parser.parse_args(
        ["classify", "--session", str(session_id), "--json"]
    )
    assert second_args.func(second_args) == 0
    second = json.loads(capsys.readouterr().out)
    assert second["run_id"] == first["run_id"]
    assert second["mutated"] is False
    assert second["classification_mutated"] is False
    assert second["semantic_projection"]["mutated"] is False


def test_rclasscli_004_custom_model_requires_hash_pinned_projection_catalog(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, _captured, conn, session_id = _session(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    parser = build_parser()

    args = parser.parse_args(
        [
            "classify",
            "--session",
            str(session_id),
            "--model",
            "custom-model.json",
            "--model-sha256",
            "0" * 64,
        ]
    )
    assert args.func(args) == 2
    assert "requires a hash-pinned --projection-catalog" in capsys.readouterr().err


def test_rclasscli_002_review_queue_reads_stored_uncertain_rows_only(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, _captured, conn, session_id = _session(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    parser = build_parser()
    classify_args = parser.parse_args(["classify", "--session", str(session_id)])
    assert classify_args.func(classify_args) == 0
    capsys.readouterr()

    queue_args = parser.parse_args(
        ["review-queue", "--session", str(session_id), "--json"]
    )
    assert queue_args.func(queue_args) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["schema"] == "ck3chronicle.classification-review-queue"
    assert payload["schema_version"] == 2
    assert payload["session_id"] == session_id
    assert payload["model_revision_id"] == APPROVED_MODEL_REVISION
    assert payload["returned"] == 1
    assert payload["items"] == [
        {
            "assignment_level": "l1",
            "confidence": payload["items"][0]["confidence"],
            "contract_id": None,
            "first_line": 2,
            "l1_template": (
                "Script system error ! Error : scope : <KEY> . <KEY> trigger"
            ),
            "l2_template": "Entirely novel semantic cause",
            "occurrences": 1,
            "sample": (
                "Script system error! Error: scope:actor.target trigger "
                "[ Entirely novel semantic cause ]"
            ),
            "source_family": "jomini_script_system.cpp",
        }
    ]
    assert 0.0 <= payload["items"][0]["confidence"] <= 1.0


def test_rclasscli_005_full_assignments_can_be_queued_by_confidence(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, _captured, conn, session_id = _session(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    parser = build_parser()
    args = parser.parse_args(["classify", "--session", str(session_id)])
    assert args.func(args) == 0
    capsys.readouterr()

    args = parser.parse_args(
        [
            "review-queue",
            "--session",
            str(session_id),
            "--level",
            "full",
            "--max-confidence",
            "1.0",
            "--json",
        ]
    )
    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema_version"] == 2
    assert payload["level"] == "full"
    assert payload["max_confidence"] == 1.0
    assert payload["returned"] == 2
    assert sum(item["occurrences"] for item in payload["items"]) == 4
    assert all(item["assignment_level"] == "full" for item in payload["items"])
    assert all(item["contract_id"] for item in payload["items"])
    assert all(item["confidence"] <= 1.0 for item in payload["items"])


def test_rclasscli_003_unknown_filter_can_return_an_explicit_empty_queue(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, _captured, conn, session_id = _session(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    parser = build_parser()
    args = parser.parse_args(["classify", "--session", str(session_id)])
    assert args.func(args) == 0
    capsys.readouterr()

    args = parser.parse_args(
        [
            "review-queue",
            "--session",
            str(session_id),
            "--level",
            "unknown",
            "--json",
        ]
    )
    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["returned"] == 0
    assert payload["items"] == []
