"""Independent migration contract for the normalized evidence index."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3

import pytest

from ck3chronicle.db import repository
from ck3chronicle import config
from ck3chronicle.cli import build_parser


MODEL_HASH = "a" * 64
RAW = "[12:00:00][E][same.cpp:1]: Repeated diagnostic\n"
RAW_HASH = hashlib.sha256(RAW.encode("utf-8")).hexdigest()


def _legacy_database(path: Path) -> None:
    """Create two exact occurrences using the immediately preceding schema."""
    conn = repository.open_db(path)
    conn.execute(
        """
        INSERT INTO sessions (
            evidence_bundle_hash, created_at, log_count, crash_present,
            total_bytes, capture_status, capture_manifest_version,
            capture_manifest_sha256, evidence_completeness, parse_status,
            parser_contract_version, parse_source_blocks, parse_preamble_blocks,
            parse_issue_occurrences, parse_issue_clusters,
            parse_unclassified_occurrences, parse_multi_issue_blocks,
            parse_silently_dropped_blocks
        ) VALUES (?, ?, 1, 0, ?, 'finalized', 1, ?, 'complete', 'succeeded',
                  'legacy', 2, 0, 2, 1, 2, 0, 0)
        """,
        ("b" * 64, "2026-08-14T00:00:00+00:00", len(RAW) * 2, "c" * 64),
    )
    conn.execute(
        """
        INSERT INTO classification_models (
            model_sha256, revision_id, schema_version, normalizer_version,
            clusterer_version, threshold, cluster_count, registered_at
        ) VALUES (?, 'legacy-model', 1, 'n', 'c', 1.0, 1, ?)
        """,
        (MODEL_HASH, datetime.now(timezone.utc).isoformat()),
    )
    conn.execute(
        """
        INSERT INTO classification_runs (
            session_id, model_sha256, classification_contract_version,
            classified_at, source_block_count, semantic_occurrence_count,
            full_count, l1_l2_count, l1_count, unknown_count
        ) VALUES (1, ?, 'legacy', ?, 2, 2, 2, 0, 0, 0)
        """,
        (MODEL_HASH, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.executescript(
        """
        DROP TABLE classification_assignments;
        DROP TABLE issue_occurrences;
        DROP TABLE source_blocks;

        CREATE TABLE source_blocks (
            session_id INTEGER NOT NULL,
            source_block_id TEXT NOT NULL,
            log_relpath TEXT NOT NULL,
            start_line INTEGER NOT NULL,
            end_line INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            source_tag TEXT NOT NULL,
            source_family TEXT NOT NULL,
            raw_block_sha256 TEXT NOT NULL,
            raw_byte_length INTEGER NOT NULL,
            raw_block TEXT NOT NULL,
            issue_count INTEGER NOT NULL,
            PRIMARY KEY (session_id, source_block_id)
        );
        CREATE TABLE issue_occurrences (
            issue_occurrence_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            signature TEXT NOT NULL,
            source_block_id TEXT NOT NULL,
            issue_ordinal INTEGER NOT NULL,
            log_relpath TEXT NOT NULL,
            line_number INTEGER NOT NULL,
            raw_block TEXT NOT NULL,
            occurrence_count INTEGER NOT NULL,
            referenced_symbols_json TEXT NOT NULL,
            extra_json TEXT NOT NULL,
            log_type TEXT NOT NULL
        );
        CREATE TABLE classification_assignments (
            classification_assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            session_id INTEGER NOT NULL,
            source_block_id TEXT NOT NULL,
            unit_ordinal INTEGER NOT NULL,
            source_family TEXT NOT NULL,
            assignment_level TEXT NOT NULL,
            contract_id TEXT,
            confidence REAL NOT NULL,
            semantic_text TEXT NOT NULL,
            location_evidence TEXT,
            normalized_tokens_json TEXT NOT NULL,
            l1_template TEXT,
            l2_template TEXT,
            structured_slots_json TEXT NOT NULL
        );
        """
    )
    for ordinal, line in enumerate((1, 2), start=1):
        block_id = f"block-{ordinal}"
        conn.execute(
            """
            INSERT INTO source_blocks VALUES (
                1, ?, 'error.log', ?, ?, '12:00:00', 'E', 'same.cpp:1',
                'same.cpp', ?, ?, ?, 1
            )
            """,
            (block_id, line, line, RAW_HASH, len(RAW.encode("utf-8")), RAW),
        )
        conn.execute(
            """
            INSERT INTO issue_occurrences (
                session_id, signature, source_block_id, issue_ordinal,
                log_relpath, line_number, raw_block, occurrence_count,
                referenced_symbols_json, extra_json, log_type
            ) VALUES (1, 'sig', ?, 0, 'error.log', ?, ?, 1, '[]', '{}', 'error')
            """,
            (block_id, line, RAW),
        )
        conn.execute(
            """
            INSERT INTO classification_assignments (
                run_id, session_id, source_block_id, unit_ordinal,
                source_family, assignment_level, contract_id, confidence,
                semantic_text, location_evidence, normalized_tokens_json,
                l1_template, l2_template, structured_slots_json
            ) VALUES (1, 1, ?, 0, 'same.cpp', 'full', '1234567890abcdef',
                      1.0, 'Repeated diagnostic', NULL,
                      '["Repeated","diagnostic"]', NULL, NULL, '[]')
            """,
            (block_id,),
        )
    conn.commit()
    conn.close()


def test_rstorage_001_legacy_rows_migrate_to_lossless_dictionaries(
    tmp_path: Path,
) -> None:
    """Oracle: two occurrences survive while each repeated payload is stored once."""
    db = tmp_path / "legacy.db"
    _legacy_database(db)

    conn = repository.open_db(db)

    assert conn.execute("SELECT COUNT(*) FROM source_blocks").fetchone()[0] == 2
    assert conn.execute("SELECT COUNT(*) FROM issue_occurrences").fetchone()[0] == 2
    assert conn.execute(
        "SELECT COUNT(*) FROM classification_assignments"
    ).fetchone()[0] == 2
    assert conn.execute("SELECT COUNT(*) FROM raw_block_contents").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM classification_payloads").fetchone()[0] == 1
    assert conn.execute(
        """
        SELECT COUNT(*)
        FROM source_blocks sb
        JOIN raw_block_contents rb
          ON rb.raw_block_pk = sb.raw_block_pk
        WHERE rb.raw_block = ? AND rb.raw_byte_length = ?
        """,
        (RAW, len(RAW.encode("utf-8"))),
    ).fetchone()[0] == 2
    assert conn.execute(
        """
        SELECT COUNT(*)
        FROM classification_assignments ca
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        WHERE cp.semantic_text = 'Repeated diagnostic'
          AND cp.contract_id = '1234567890abcdef'
        """
    ).fetchone()[0] == 2
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert "raw_block" not in {
        row[1] for row in conn.execute("PRAGMA table_info(source_blocks)")
    }
    assert "source_family" not in {
        row[1]
        for row in conn.execute("PRAGMA table_info(classification_assignments)")
    }
    conn.close()


def test_rstorage_002_compact_command_reports_verified_post_vacuum_state(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    """Oracle: maintenance output reports the retained independent row counts."""
    root = tmp_path / "runtime"
    root.mkdir()
    db = root / "ck3chronicle.db"
    _legacy_database(db)
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", root)
    args = build_parser().parse_args(["compact-db", "--json"])

    assert args.func(args) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["schema"] == "ck3chronicle.database-compaction"
    assert result["schema_version"] == 1
    assert result["quick_check"] == "ok"
    assert result["foreign_key_errors"] == 0
    assert result["bytes_after"] == db.stat().st_size
    assert result["counts"] == {
        "source_blocks": 2,
        "raw_block_contents": 1,
        "issue_occurrences": 2,
        "classification_assignments": 2,
        "classification_payloads": 1,
    }


def test_rstorage_003_conflicting_hash_content_rolls_back_legacy_schema(
    tmp_path: Path,
) -> None:
    """Mutation: a forged raw-hash collision must not expose a partial migration."""
    db = tmp_path / "collision.db"
    _legacy_database(db)
    conn = sqlite3.connect(db)
    conn.execute(
        "UPDATE source_blocks SET raw_block = ? WHERE source_block_id = 'block-2'",
        ("[12:00:00][E][same.cpp:1]: Different diagnostic\n",),
    )
    conn.commit()
    conn.close()

    with pytest.raises(sqlite3.DatabaseError, match="conflicting stored content"):
        repository.open_db(db)

    conn = sqlite3.connect(db)
    assert "raw_block" in {
        row[1] for row in conn.execute("PRAGMA table_info(source_blocks)")
    }
    assert "source_block_id" in {
        row[1] for row in conn.execute("PRAGMA table_info(source_blocks)")
    }
    assert conn.execute("SELECT COUNT(*) FROM source_blocks").fetchone()[0] == 2
    conn.close()
