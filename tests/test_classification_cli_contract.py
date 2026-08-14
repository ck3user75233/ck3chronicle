"""Functional CLI contracts for classification and human review queues."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.cli import build_parser

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
        "classification_contract_version": "2.0.0",
        "counts": {
            "full": 4,
            "l1": 1,
            "l1_l2": 0,
            "semantic_occurrences": 5,
            "source_blocks": 3,
            "unknown": 0,
        },
        "model_revision_id": "93196794a7e0115d",
        "model_sha256": (
            "3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3"
        ),
        "mutated": True,
        "run_id": first["run_id"],
        "schema": "ck3chronicle.classification-run",
        "schema_version": 1,
        "session_id": session_id,
    }

    second_args = parser.parse_args(
        ["classify", "--session", str(session_id), "--json"]
    )
    assert second_args.func(second_args) == 0
    second = json.loads(capsys.readouterr().out)
    assert second["run_id"] == first["run_id"]
    assert second["mutated"] is False


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
    assert payload["schema_version"] == 1
    assert payload["session_id"] == session_id
    assert payload["model_revision_id"] == "93196794a7e0115d"
    assert payload["returned"] == 1
    assert payload["items"] == [
        {
            "assignment_level": "l1",
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
