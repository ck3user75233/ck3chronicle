"""Persistence contracts for the hash-bound canonical semantic projection."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sqlite3

import pytest

from ck3chronicle.classification.inference import Classifier
from ck3chronicle.classification.model import load_model
from ck3chronicle.classification.projection_catalog import load_projection_catalog
from ck3chronicle.classification.service import classify_session
from ck3chronicle.db import repository
from ck3chronicle.harvester import MANIFEST_VERSION, finalize_pending, spool_logs
from ck3chronicle.parser.service import parse_session
from ck3chronicle.semantic_projection_service import (
    StoredClassificationError,
    project_classification_run,
)

from foundation_oracle import SIX_LOG_BYTES, write_logs
from test_semantic_projection_contract import (
    MODEL_REVISION,
    SOURCE_FAMILY,
    _write_catalog,
    _write_model,
)


INVENTED_ERROR_LOG = (
    b"[12:34:56][E][invented_semantics.cpp:73]: Widget symbol "
    b"'azure_widget' cannot be resolved\n"
    b"Script location: file: common/invented/azure_widget.txt line: 81 "
    b"(invented:setup)\n"
    b"[12:35:57][W][invented_semantics.cpp:73]: Widget symbol "
    b"'vermilion_widget' cannot be resolved\n"
    b"Script location: file: events/invented/vermilion_widget.txt line: 907 "
    b"(invented:setup)\n"
)


def _runtime(tmp_path: Path):
    model_path = tmp_path / "invented-model.json"
    model_sha256 = _write_model(model_path)
    model = load_model(model_path, expected_sha256=model_sha256)
    catalog_path = tmp_path / "invented-catalog.json"
    catalog_sha256 = _write_catalog(catalog_path, model_sha256)
    catalog = load_projection_catalog(
        catalog_path,
        expected_sha256=catalog_sha256,
        model=model,
    )

    logs = tmp_path / "live-logs"
    runtime = tmp_path / "runtime"
    files = dict(SIX_LOG_BYTES)
    files["error.log"] = INVENTED_ERROR_LOG
    write_logs(logs, files)
    captured = finalize_pending(spool_logs(logs, runtime), runtime)
    conn = repository.open_db(runtime / "ck3chronicle.db")
    session_id, _existing = repository.register_finalized_session(
        conn,
        evidence_bundle_hash=captured.evidence_bundle_hash,
        captured_at="2026-08-16T00:00:00+00:00",
        manifest_version=MANIFEST_VERSION,
        manifest_sha256=captured.manifest_sha256,
        evidence_completeness="complete",
        files=captured.files,
    )
    parse_session(conn, runtime, session_id)
    classification = classify_session(conn, session_id, Classifier(model))
    return conn, session_id, classification, catalog, catalog_path


def _source_snapshot(conn: sqlite3.Connection, session_id: int) -> tuple[tuple, ...]:
    return tuple(
        tuple(row)
        for row in conn.execute(
            """
            SELECT sb.source_block_pk, sb.raw_block_pk, sb.start_line, sb.end_line,
                   sb.timestamp, sb.level, sb.source_tag, sb.source_family,
                   rb.raw_block_sha256, rb.raw_byte_length, rb.raw_block,
                   sb.issue_count
            FROM source_blocks sb
            JOIN raw_block_contents rb ON rb.raw_block_pk = sb.raw_block_pk
            WHERE sb.session_id = ? ORDER BY sb.start_line
            """,
            (session_id,),
        ).fetchall()
    )


def _projection_snapshot(conn: sqlite3.Connection, session_id: int) -> tuple:
    lineage = tuple(
        tuple(row)
        for row in conn.execute(
            """
            SELECT projection_run_id, classification_run_id,
                   projection_catalog_sha256, projection_catalog_revision_id,
                   projection_contract_version, source_block_count,
                   semantic_occurrence_count, issue_cluster_count,
                   unclassified_occurrence_count, multi_issue_block_count
            FROM semantic_projection_runs WHERE session_id = ?
            """,
            (session_id,),
        ).fetchall()
    )
    issues = tuple(
        tuple(row)
        for row in conn.execute(
            """
            SELECT issue_id, signature, category, error_type, severity,
                   confidence, occurrence_count, semantic_projection_run_id
            FROM issues WHERE session_id = ? ORDER BY issue_id
            """,
            (session_id,),
        ).fetchall()
    )
    occurrences = tuple(
        tuple(row)
        for row in conn.execute(
            """
            SELECT issue_occurrence_id, signature, source_block_pk,
                   issue_ordinal, primary_file, primary_line,
                   referenced_symbols_json, referenced_objects_json,
                   semantic_projection_run_id
            FROM issue_occurrences WHERE session_id = ?
            ORDER BY source_block_pk, issue_ordinal
            """,
            (session_id,),
        ).fetchall()
    )
    return lineage, issues, occurrences


def test_projection_replaces_canonical_rows_with_occurrence_specific_evidence(
    tmp_path: Path,
) -> None:
    conn, session_id, classification, catalog, _path = _runtime(tmp_path)
    source_before = _source_snapshot(conn, session_id)

    result = project_classification_run(conn, session_id, catalog)

    assert result.mutated is True
    assert result.classification_run_id == classification.run_id
    assert result.model_revision_id == MODEL_REVISION
    assert result.counts == {
        "source_blocks": 2,
        "semantic_occurrences": 2,
        "issue_clusters": 1,
        "unclassified_occurrences": 0,
        "multi_issue_blocks": 0,
    }
    lineage = conn.execute(
        "SELECT * FROM semantic_projection_runs WHERE session_id = ?",
        (session_id,),
    ).fetchone()
    assert lineage["model_sha256"] == catalog.model_sha256
    assert lineage["projection_catalog_sha256"] == catalog.sha256
    assert lineage["projection_catalog_revision_id"] == catalog.revision_id
    assert lineage["projection_catalog_schema_version"] == catalog.schema_version
    cluster = conn.execute(
        """
        SELECT category, error_type, occurrence_count, severity, confidence
        FROM issues WHERE session_id = ?
        """,
        (session_id,),
    ).fetchone()
    assert tuple(cluster) == (
        "symbol_resolution", "undefined_symbol", 2, "error", "high"
    )
    occurrences = conn.execute(
        """
        SELECT primary_file, primary_line, referenced_symbols_json,
               referenced_objects_json
        FROM issue_occurrences WHERE session_id = ? ORDER BY line_number
        """,
        (session_id,),
    ).fetchall()
    assert [tuple(row) for row in occurrences] == [
        (
            "common/invented/azure_widget.txt",
            81,
            '["azure_widget"]',
            "[]",
        ),
        (
            "events/invented/vermilion_widget.txt",
            907,
            '["vermilion_widget"]',
            "[]",
        ),
    ]
    source_after = _source_snapshot(conn, session_id)
    assert tuple(row[:-1] for row in source_after) == tuple(
        row[:-1] for row in source_before
    )
    assert [row[-1] for row in source_after] == [1, 1]
    repository.validate_semantic_projection(conn, result.projection_run_id)
    conn.close()


def test_same_lineage_is_read_only_and_catalog_change_reprojects(
    tmp_path: Path,
) -> None:
    conn, session_id, _classification, catalog, catalog_path = _runtime(tmp_path)
    first = project_classification_run(conn, session_id, catalog)
    changes_before = conn.total_changes

    same = project_classification_run(conn, session_id, catalog)

    assert same.mutated is False
    assert same.projection_run_id == first.projection_run_id
    assert conn.total_changes == changes_before

    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    raw["revision_id"] = "invented-projection-catalog-v2"
    catalog_path.write_text(
        json.dumps(raw, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
        encoding="utf-8",
    )
    second_hash = hashlib.sha256(catalog_path.read_bytes()).hexdigest()
    second_catalog = load_projection_catalog(
        catalog_path,
        expected_sha256=second_hash,
        model=load_model(
            tmp_path / "invented-model.json",
            expected_sha256=catalog.model_sha256,
        ),
    )

    second = project_classification_run(conn, session_id, second_catalog)

    assert second.mutated is True
    assert second.projection_run_id != first.projection_run_id
    assert conn.execute(
        "SELECT COUNT(*) FROM semantic_projection_runs WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 1
    assert conn.execute(
        "SELECT COUNT(*) FROM issue_occurrences WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 2
    conn.close()


def test_failed_reprojection_restores_prior_lineage_and_canonical_rows(
    tmp_path: Path,
) -> None:
    conn, session_id, _classification, catalog, _path = _runtime(tmp_path)
    project_classification_run(conn, session_id, catalog)
    before = _projection_snapshot(conn, session_id)
    conn.execute(
        """
        CREATE TEMP TRIGGER fail_second_projected_occurrence
        BEFORE INSERT ON issue_occurrences
        WHEN NEW.line_number = 3
        BEGIN
            SELECT RAISE(ABORT, 'injected semantic projection failure');
        END
        """
    )

    with pytest.raises(sqlite3.IntegrityError, match="projection failure"):
        project_classification_run(conn, session_id, catalog, reproject=True)

    assert _projection_snapshot(conn, session_id) == before
    conn.close()


def test_postvalidation_rejects_wrong_distribution_and_rolls_back(
    tmp_path: Path,
) -> None:
    conn, session_id, _classification, catalog, _path = _runtime(tmp_path)
    project_classification_run(conn, session_id, catalog)
    before = _projection_snapshot(conn, session_id)
    conn.execute(
        """
        CREATE TEMP TRIGGER corrupt_projected_signature
        AFTER INSERT ON issue_occurrences
        WHEN NEW.line_number = 3
        BEGIN
            UPDATE issue_occurrences
            SET signature = 'orphaned-signature'
            WHERE session_id = NEW.session_id AND line_number = 1;
        END
        """
    )

    with pytest.raises(ValueError, match="projection distribution disagrees"):
        project_classification_run(conn, session_id, catalog, reproject=True)

    assert _projection_snapshot(conn, session_id) == before
    conn.close()


def test_malformed_stored_payload_cannot_replace_prior_projection(
    tmp_path: Path,
) -> None:
    conn, session_id, classification, catalog, _path = _runtime(tmp_path)
    project_classification_run(conn, session_id, catalog)
    before = _projection_snapshot(conn, session_id)
    conn.execute(
        """
        UPDATE classification_payloads
        SET structured_slots_json = '{'
        WHERE payload_pk = (
            SELECT payload_pk FROM classification_assignments
            WHERE run_id = ? ORDER BY classification_assignment_id LIMIT 1
        )
        """,
        (classification.run_id,),
    )
    conn.commit()

    with pytest.raises(StoredClassificationError, match="not valid JSON"):
        project_classification_run(conn, session_id, catalog, reproject=True)

    assert _projection_snapshot(conn, session_id) == before
    conn.close()


def test_replacing_classification_invalidates_projection_not_source_blocks(
    tmp_path: Path,
) -> None:
    conn, session_id, classification, catalog, _path = _runtime(tmp_path)
    project_classification_run(conn, session_id, catalog)
    source_before = _source_snapshot(conn, session_id)
    model_path = tmp_path / "invented-model.json"
    model = load_model(model_path, expected_sha256=catalog.model_sha256)

    replaced = classify_session(
        conn, session_id, Classifier(model), reclassify=True
    )

    assert replaced.run_id != classification.run_id
    assert conn.execute(
        "SELECT COUNT(*) FROM semantic_projection_runs WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 0
    assert conn.execute(
        "SELECT COUNT(*) FROM issues WHERE session_id = ?", (session_id,)
    ).fetchone()[0] == 0
    assert conn.execute(
        "SELECT COUNT(*) FROM issue_occurrences WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0] == 0
    session = repository.get_session(conn, session_id)
    assert (
        session["parse_issue_occurrences"],
        session["parse_issue_clusters"],
        session["parse_unclassified_occurrences"],
        session["parse_multi_issue_blocks"],
    ) == (0, 0, 0, 0)
    assert _source_snapshot(conn, session_id) == source_before
    conn.close()


def test_failed_classification_replacement_restores_projection_cascade(
    tmp_path: Path,
) -> None:
    conn, session_id, classification, catalog, _path = _runtime(tmp_path)
    project_classification_run(conn, session_id, catalog)
    source_before = _source_snapshot(conn, session_id)
    projection_before = _projection_snapshot(conn, session_id)
    model = load_model(
        tmp_path / "invented-model.json", expected_sha256=catalog.model_sha256
    )
    conn.execute(
        """
        CREATE TEMP TRIGGER fail_replacement_assignment
        BEFORE INSERT ON classification_assignments
        BEGIN
            SELECT RAISE(ABORT, 'injected classification replacement failure');
        END
        """
    )

    with pytest.raises(sqlite3.IntegrityError, match="replacement failure"):
        classify_session(conn, session_id, Classifier(model), reclassify=True)

    assert repository.get_classification_run(
        conn, session_id, catalog.model_sha256
    )["run_id"] == classification.run_id
    assert _projection_snapshot(conn, session_id) == projection_before
    assert _source_snapshot(conn, session_id) == source_before
    conn.close()
