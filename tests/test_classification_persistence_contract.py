"""Fresh takeover contracts for versioned, atomic classification storage."""

from __future__ import annotations

from pathlib import Path
import sqlite3

import pytest

from ck3chronicle.classification import Classifier, load_model
from ck3chronicle.classification.catalog import (
    APPROVED_MODEL_SHA256,
    approved_model_path,
)
from ck3chronicle.classification.service import (
    ClassificationPreconditionError,
    classify_session,
)
from ck3chronicle.db import repository
from ck3chronicle.harvester import MANIFEST_VERSION, finalize_pending, spool_logs
from ck3chronicle.parser.service import parse_session

from foundation_oracle import SIX_LOG_BYTES, write_logs


MODEL_SHA256 = APPROVED_MODEL_SHA256
MODEL_PATH = approved_model_path()

CLASSIFICATION_ERROR_LOG = (
    b"[12:00:00][E][pdx_localize.cpp:1]: Duplicate localization key. Key "
    b"'Carthage' is defined in both 'localization/english/a.yml' and "
    b"'mod/loc/b.yml'.\n"
    b"[12:00:01][E][jomini_script_system.cpp:2]: Script system error! Error: "
    b"scope:actor.target trigger [ Entirely novel semantic cause ]\n"
    b"[12:00:02][E][pdx_persistent_reader.cpp:3]: Error: \""
    b"Unknown trigger: first_key, near line: 10 "
    b"Unknown trigger: second_key, near line: 20 "
    b"Unknown trigger: third_key, near line: 30"
    b"\" in file: events/example.txt line: 40\n"
)


def _classifier() -> Classifier:
    return Classifier(load_model(MODEL_PATH, expected_sha256=MODEL_SHA256))


def _session(tmp_path: Path, *, parse: bool = True):
    logs = tmp_path / "live-logs"
    runtime = tmp_path / "runtime"
    files = dict(SIX_LOG_BYTES)
    files["error.log"] = CLASSIFICATION_ERROR_LOG
    write_logs(logs, files)
    captured = finalize_pending(spool_logs(logs, runtime), runtime)
    conn = repository.open_db(runtime / "ck3chronicle.db")
    session_id, _ = repository.register_finalized_session(
        conn,
        evidence_bundle_hash=captured.evidence_bundle_hash,
        captured_at="2026-08-13T00:00:00+00:00",
        manifest_version=MANIFEST_VERSION,
        manifest_sha256=captured.manifest_sha256,
        evidence_completeness="complete",
        files=captured.files,
    )
    if parse:
        parse_session(conn, runtime, session_id)
    return runtime, captured, conn, session_id


def test_rclassdb_001_one_row_per_semantic_unit_with_exact_provenance(
    tmp_path: Path,
) -> None:
    """Oracle: three source blocks contain five independently countable units."""
    _runtime, _captured, conn, session_id = _session(tmp_path)

    result = classify_session(conn, session_id, _classifier())

    assert result.mutated is True
    assert result.counts == {
        "source_blocks": 3,
        "semantic_occurrences": 5,
        "full": 4,
        "l1_l2": 0,
        "l1": 1,
        "unknown": 0,
    }
    rows = conn.execute(
        """
        SELECT sb.start_line, ca.unit_ordinal, cp.source_family,
               cp.assignment_level, cp.contract_id, cp.semantic_text
        FROM classification_assignments ca
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        JOIN source_blocks sb
          ON sb.source_block_pk = ca.source_block_pk
        WHERE ca.session_id = ?
        ORDER BY sb.start_line, ca.unit_ordinal
        """,
        (session_id,),
    ).fetchall()
    assert [tuple(row[:5]) for row in rows] == [
        (1, 0, "pdx_localize.cpp", "full", "514c7f0349cf61eb"),
        (2, 0, "jomini_script_system.cpp", "l1", None),
        (3, 0, "pdx_persistent_reader.cpp", "full", "21b477c6e94b1681"),
        (3, 1, "pdx_persistent_reader.cpp", "full", "21b477c6e94b1681"),
        (3, 2, "pdx_persistent_reader.cpp", "full", "21b477c6e94b1681"),
    ]
    assert [row[5] for row in rows[2:]] == ["Unknown trigger: <KEY>"] * 3
    assert conn.execute(
        "SELECT COUNT(*) FROM classification_contracts WHERE model_sha256 = ?",
        (MODEL_SHA256,),
    ).fetchone()[0] == len(_classifier().model.clusters)
    # The three persistent-reader units are independently addressable but have
    # one exact derived payload. Together with the other two blocks this yields
    # three dictionary rows for five assignment rows.
    assert conn.execute(
        "SELECT COUNT(*) FROM classification_payloads WHERE model_sha256 = ?",
        (MODEL_SHA256,),
    ).fetchone()[0] == 3
    assert set(
        row[1]
        for row in conn.execute("PRAGMA table_info(classification_assignments)")
    ) == {
        "classification_assignment_id",
        "run_id",
        "session_id",
        "source_block_pk",
        "unit_ordinal",
        "payload_pk",
    }
    conn.close()


def test_rclassdb_002_classification_reads_database_not_archived_log(
    tmp_path: Path,
) -> None:
    """Oracle: after canonical parse, derived classification needs no log reopen."""
    _runtime, captured, conn, session_id = _session(tmp_path)
    (captured.dest_dir / "error.log").unlink()

    result = classify_session(conn, session_id, _classifier())

    assert result.counts["semantic_occurrences"] == 5
    conn.close()


def test_rclassdb_003_same_model_is_idempotent(tmp_path: Path) -> None:
    """Oracle: rerunning an unchanged model returns the same visible run."""
    _runtime, _captured, conn, session_id = _session(tmp_path)
    first = classify_session(conn, session_id, _classifier())
    second = classify_session(conn, session_id, _classifier())

    assert second.mutated is False
    assert second.run_id == first.run_id
    assert conn.execute(
        "SELECT COUNT(*) FROM classification_runs WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 1
    assert conn.execute(
        "SELECT COUNT(*) FROM classification_assignments WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 5
    conn.close()


def test_rclassdb_004_failed_reclassification_preserves_prior_run(
    tmp_path: Path,
) -> None:
    """Oracle: a database fault after one insert cannot expose a partial run."""
    _runtime, _captured, conn, session_id = _session(tmp_path)
    first = classify_session(conn, session_id, _classifier())
    conn.execute(
        """
        CREATE TRIGGER fail_second_classification
        BEFORE INSERT ON classification_assignments
        WHEN NEW.unit_ordinal = 1
        BEGIN
            SELECT RAISE(ABORT, 'injected classification failure');
        END
        """
    )
    conn.commit()

    with pytest.raises(sqlite3.IntegrityError, match="injected classification failure"):
        classify_session(conn, session_id, _classifier(), reclassify=True)

    visible = conn.execute(
        "SELECT run_id FROM classification_runs WHERE session_id = ?",
        (session_id,),
    ).fetchall()
    assert [row[0] for row in visible] == [first.run_id]
    assert conn.execute(
        "SELECT COUNT(*) FROM classification_assignments WHERE run_id = ?",
        (first.run_id,),
    ).fetchone()[0] == 5
    conn.close()


def test_rclassdb_005_unparsed_session_is_rejected_without_rows(tmp_path: Path) -> None:
    """Oracle: classifiers derive only from the accepted canonical block store."""
    _runtime, _captured, conn, session_id = _session(tmp_path, parse=False)

    with pytest.raises(ClassificationPreconditionError, match="parsed"):
        classify_session(conn, session_id, _classifier())

    assert conn.execute("SELECT COUNT(*) FROM classification_runs").fetchone()[0] == 0
    conn.close()


def test_rclassdb_006_stale_inference_contract_is_replaced_automatically(
    tmp_path: Path,
) -> None:
    """Same model bytes cannot make pre-PostValidate results look current."""
    _runtime, _captured, conn, session_id = _session(tmp_path)
    first = classify_session(conn, session_id, _classifier())
    conn.execute(
        """
        UPDATE classification_runs
        SET classification_contract_version = '2.0.0'
        WHERE run_id = ?
        """,
        (first.run_id,),
    )
    conn.commit()

    second = classify_session(conn, session_id, _classifier())

    assert second.mutated is True
    assert second.run_id != first.run_id
    assert second.classification_contract_version == "2.0.1"
    assert conn.execute(
        "SELECT COUNT(*) FROM classification_runs WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 1
    conn.close()


def test_rclassdb_007_successful_reparse_invalidates_derived_classification(
    tmp_path: Path,
) -> None:
    """A new canonical projection cannot retain assignments to old block IDs."""
    runtime, _captured, conn, session_id = _session(tmp_path)
    classify_session(conn, session_id, _classifier())

    parse_session(conn, runtime, session_id, reparse=True)

    assert conn.execute(
        "SELECT COUNT(*) FROM classification_runs WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 0
    assert conn.execute(
        "SELECT COUNT(*) FROM classification_assignments WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 0
    conn.close()
