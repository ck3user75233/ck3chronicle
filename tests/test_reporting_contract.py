"""Fresh functional contracts for database-only executive reports."""

from __future__ import annotations

from ck3chronicle.classification import classify_session
from ck3chronicle.db import repository
from ck3chronicle.reporting import build_session_report, latest_session_id

from test_classification_persistence_contract import _classifier, _session


def test_rreport_001_executive_report_uses_stored_classification_rows(
    tmp_path,
) -> None:
    runtime, captured, conn, session_id = _session(tmp_path)
    classify_session(conn, session_id, _classifier())
    # A report is a database projection. The archive is not consulted again.
    (captured.dest_dir / "error.log").unlink()

    report = build_session_report(conn, session_id, limit=10)

    assert report["schema"] == "ck3chronicle.session-report"
    assert report["schema_version"] == 4
    assert report["session"]["session_id"] == session_id
    assert report["session"]["captured_at"] == "2026-08-13T00:00:00+00:00"
    assert report["parse"]["source_blocks"] == 3
    assert report["classification"]["model_revision_id"] == "93196794a7e0115d"
    assert report["classification"]["counts"] == {
        "full": 4,
        "l1_l2": 0,
        "l1": 1,
        "unknown": 0,
    }
    assert report["classification"]["semantic_occurrences"] == 5
    assert report["classification"]["full_rate"] == 0.8
    assert report["classification"]["l1_or_better_rate"] == 1.0
    assert report["classification"]["review_required"] == 1

    assert report["source_summary"] == [
        {"source_family": "pdx_persistent_reader.cpp", "occurrences": 3},
        {"source_family": "jomini_script_system.cpp", "occurrences": 1},
        {"source_family": "pdx_localize.cpp", "occurrences": 1},
    ]
    assert report["top_patterns"][0] == {
        "assignment_level": "full",
        "contract_id": "21b477c6e94b1681",
        "source_family": "pdx_persistent_reader.cpp",
        "occurrences": 3,
        "first_line": 3,
        "template": "Unknown trigger : <KEY>",
        "sample": "Unknown trigger: <KEY>",
    }
    assert report["review_queue"] == [
        {
            "assignment_level": "l1",
            "source_family": "jomini_script_system.cpp",
            "occurrences": 1,
            "first_line": 2,
            "l1_template": (
                "Script system error ! Error : scope : <KEY> . <KEY> trigger"
            ),
            "l2_template": "Entirely novel semantic cause",
            "sample": (
                "Script system error! Error: scope:actor.target trigger "
                "[ Entirely novel semantic cause ]"
            ),
        }
    ]
    conn.close()


def test_rreport_002_latest_uses_capture_chronology_not_session_id(tmp_path) -> None:
    _runtime, _captured, conn, first_id = _session(tmp_path)
    classify_session(conn, first_id, _classifier())
    conn.execute(
        "UPDATE sessions SET created_at = ? WHERE session_id = ?",
        ("2026-08-13T10:00:00+00:00", first_id),
    )
    newer_id = conn.execute(
        """
        INSERT INTO sessions (
            evidence_bundle_hash, created_at, log_count, crash_present,
            total_bytes, capture_status, capture_manifest_version,
            capture_manifest_sha256, evidence_completeness, parse_status,
            parser_contract_version, parse_source_blocks, parse_preamble_blocks,
            parse_issue_occurrences, parse_issue_clusters,
            parse_unclassified_occurrences, parse_multi_issue_blocks,
            parse_silently_dropped_blocks
        ) VALUES (?, ?, 1, 0, 0, 'finalized', 1, ?, 'complete', 'succeeded',
                  '1.0.0', 0, 0, 0, 0, 0, 0, 0)
        """,
        ("f" * 64, "2026-08-13T09:00:00+00:00", "e" * 64),
    ).lastrowid
    conn.execute(
        """
        INSERT INTO classification_runs (
            session_id, model_sha256, classification_contract_version,
            classified_at, source_block_count, semantic_occurrence_count,
            full_count, l1_l2_count, l1_count, unknown_count
        ) VALUES (?, ?, '1.0.0', ?, 0, 0, 0, 0, 0, 0)
        """,
        (newer_id, _classifier().model.sha256, "2026-08-13T11:00:00+00:00"),
    )
    conn.commit()

    # The larger ID was registered later but represents an older capture.
    assert newer_id > first_id
    assert latest_session_id(conn) == first_id
    assert [row["session_id"] for row in repository.list_sessions(conn, 2)] == [
        first_id,
        newer_id,
    ]
    conn.close()
