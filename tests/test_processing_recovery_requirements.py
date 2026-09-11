"""Checks derived from the approved ingestion-recovery requirements."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from ck3chronicle.archive_registry import register_archive
from ck3chronicle.classification.catalog import load_approved_semantic_runtime
from ck3chronicle.db import repository
from ck3chronicle.harvester import (
    MANIFEST_NAME,
    ArchiveIntegrityError,
    finalize_pending,
    spool_logs,
)
from ck3chronicle.processing import (
    ProcessingJournal,
    ProcessorAlreadyRunning,
    ProcessorLease,
    plan_pending_capture,
    plan_selected_sessions,
    process_pending,
)


class ProcessingRecoveryRequirements(unittest.TestCase):
    def test_one_database_identity_is_the_run_id(self) -> None:
        """One accepted capture has one Run ID and one keyed metadata row."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            runtime = root / "runtime"
            logs.mkdir()
            (logs / "error.log").write_text(
                "[00:00:01][pdx.cpp:1]: one\n",
                encoding="utf-8",
            )
            pending = spool_logs(
                logs,
                runtime,
                capture_metadata={
                    "trigger": "manual_capture",
                    "termination_kind": "unknown",
                },
            )
            archive = finalize_pending(pending, runtime)
            registration = register_archive(
                runtime,
                runtime / "ck3chronicle.db",
                archive.evidence_bundle_hash,
            )

            conn = repository.open_db_readonly(runtime / "ck3chronicle.db")
            try:
                tables = {
                    str(row[0])
                    for row in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    ).fetchall()
                }
                metadata = repository.get_run(conn, registration.session_id)
            finally:
                conn.close()

            self.assertEqual(registration.run_id, registration.session_id)
            self.assertIsNotNone(metadata)
            assert metadata is not None
            self.assertEqual(int(metadata["session_id"]), registration.session_id)
            self.assertIsNone(metadata["observed_started_at"])
            self.assertIsNone(metadata["observed_ended_at"])
            self.assertIn("run_metadata", tables)
            self.assertNotIn("capture_observations", tables)
            self.assertNotIn("run_file_origins", tables)

    def test_readonly_open_never_performs_an_implicit_migration(self) -> None:
        """A read command must not turn into an unapproved production write."""
        with tempfile.TemporaryDirectory() as temporary:
            db_path = Path(temporary) / "legacy.db"
            conn = sqlite3.connect(db_path)
            conn.execute("CREATE TABLE marker (value TEXT NOT NULL)")
            conn.execute("INSERT INTO marker VALUES ('unchanged')")
            conn.commit()
            conn.close()
            before = hashlib.sha256(db_path.read_bytes()).hexdigest()

            with self.assertRaises(repository.DatabaseMigrationRequired):
                repository.open_db_readonly(db_path)

            self.assertEqual(hashlib.sha256(db_path.read_bytes()).hexdigest(), before)

    def test_wide_pending_pipeline_is_disabled_before_runtime_mutation(self) -> None:
        """No internal default may revive the former all-pending/all-history sweep."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            marker = root / "pending" / "leave-me" / "error.log"
            marker.parent.mkdir(parents=True)
            marker.write_text("protected\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "wide pending"):
                process_pending(root, object())  # type: ignore[arg-type]

            self.assertTrue(marker.is_file())
            self.assertFalse((root / "ck3chronicle.db").exists())

    def test_pending_plan_is_read_only_and_names_exactly_one_capture(self) -> None:
        """Planning one pending item must not mutate it, its peer, or SQLite."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            runtime = root / "runtime"
            logs.mkdir()
            db_path = runtime / "ck3chronicle.db"
            conn = repository.open_db(db_path)
            conn.close()
            (logs / "error.log").write_text(
                "[00:00:01][pdx.cpp:1]: selected\n",
                encoding="utf-8",
            )
            selected = spool_logs(
                logs,
                runtime,
                capture_metadata={
                    "trigger": "process_exit",
                    "termination_kind": "normal",
                },
            )
            (logs / "error.log").write_text(
                "[00:00:02][pdx.cpp:2]: unselected\n",
                encoding="utf-8",
            )
            unselected = spool_logs(
                logs,
                runtime,
                capture_metadata={
                    "trigger": "process_exit",
                    "termination_kind": "normal",
                },
            )
            database_before = hashlib.sha256(db_path.read_bytes()).hexdigest()
            classifier, projection_catalog = load_approved_semantic_runtime()

            plan = plan_pending_capture(
                runtime,
                classifier,
                projection_catalog,
                selected.dest_dir.name,
            )

            self.assertEqual(plan.pending_name, selected.dest_dir.name)
            self.assertEqual(
                plan.as_dict()["bounds"],
                {"pending_captures": 1, "historical_sessions": 0},
            )
            self.assertTrue(selected.dest_dir.is_dir())
            self.assertTrue(unselected.dest_dir.is_dir())
            self.assertFalse((selected.dest_dir / MANIFEST_NAME).exists())
            self.assertFalse((unselected.dest_dir / MANIFEST_NAME).exists())
            self.assertEqual(
                hashlib.sha256(db_path.read_bytes()).hexdigest(),
                database_before,
            )

    def test_replacement_foreign_keys_have_leading_column_indexes(self) -> None:
        """Replacing parse/projection parents must not scan entire child tables."""
        with tempfile.TemporaryDirectory() as temporary:
            conn = repository.open_db(Path(temporary) / "ck3chronicle.db")
            try:
                expected = {
                    "classification_assignments": (
                        "source_block_pk",
                        "idx_classification_assignments_source_block",
                    ),
                    "issue_occurrences": (
                        "source_block_pk",
                        "idx_issue_occurrences_source_block",
                    ),
                    "issues": (
                        "semantic_projection_run_id",
                        "idx_issues_semantic_projection_run",
                    ),
                }
                projection_occurrence = (
                    "issue_occurrences",
                    "semantic_projection_run_id",
                    "idx_issue_occurrences_semantic_projection_run",
                )
                for table, (column, index_name) in expected.items():
                    indexes = {
                        str(row[1])
                        for row in conn.execute(
                            f"PRAGMA index_list({table})"
                        ).fetchall()
                    }
                    self.assertIn(index_name, indexes)
                    plan = [
                        str(row[3])
                        for row in conn.execute(
                            "EXPLAIN QUERY PLAN "
                            f"SELECT rowid FROM {table} WHERE {column} = ?",
                            (1,),
                        ).fetchall()
                    ]
                    self.assertTrue(
                        any(
                            "SEARCH" in detail and index_name in detail
                            for detail in plan
                        ),
                        msg=f"foreign-key lookup plan for {table}: {plan}",
                    )
                table, column, index_name = projection_occurrence
                plan = [
                    str(row[3])
                    for row in conn.execute(
                        "EXPLAIN QUERY PLAN "
                        f"SELECT rowid FROM {table} WHERE {column} = ?",
                        (1,),
                    ).fetchall()
                ]
                self.assertTrue(
                    any(
                        "SEARCH" in detail and index_name in detail
                        for detail in plan
                    ),
                    msg=f"foreign-key lookup plan for {table}: {plan}",
                )
                projection_join_plan = [
                    str(row[3])
                    for row in conn.execute(
                        """
                        EXPLAIN QUERY PLAN
                        SELECT i.issue_id
                        FROM issues i
                        LEFT JOIN issue_occurrences io
                          ON io.session_id = i.session_id
                         AND io.signature = i.signature
                         AND io.semantic_projection_run_id =
                             i.semantic_projection_run_id
                        WHERE i.session_id = ?
                          AND i.semantic_projection_run_id = ?
                        GROUP BY i.issue_id, i.occurrence_count
                        """,
                        (1, 1),
                    ).fetchall()
                ]
                self.assertTrue(
                    any(
                        "SEARCH io" in detail
                        and "idx_issue_occurrences_projection_signature" in detail
                        for detail in projection_join_plan
                    ),
                    msg=f"projection cluster validation plan: {projection_join_plan}",
                )
                projection_block_plan = [
                    str(row[3])
                    for row in conn.execute(
                        """
                        EXPLAIN QUERY PLAN
                        SELECT sb.source_block_pk
                        FROM source_blocks sb
                        LEFT JOIN issue_occurrences io
                          ON io.session_id = sb.session_id
                         AND io.source_block_pk = sb.source_block_pk
                         AND io.semantic_projection_run_id = ?
                        WHERE sb.session_id = ?
                        GROUP BY sb.source_block_pk, sb.issue_count
                        """,
                        (1, 1),
                    ).fetchall()
                ]
                self.assertTrue(
                    any(
                        "SEARCH io" in detail
                        and "idx_issue_occurrences_projection_source" in detail
                        for detail in projection_block_plan
                    ),
                    msg=f"projection block validation plan: {projection_block_plan}",
                )
            finally:
                conn.close()

    def test_backfill_plan_verifies_one_selected_archive_and_excludes_pending(self) -> None:
        """Historical planning must bind one DB row to its intact archive."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            runtime = root / "runtime"
            logs.mkdir()
            db_path = runtime / "ck3chronicle.db"
            conn = repository.open_db(db_path)
            conn.close()
            (logs / "error.log").write_text(
                "[00:00:01][pdx.cpp:1]: selected\n",
                encoding="utf-8",
            )
            pending = spool_logs(
                logs,
                runtime,
                capture_metadata={
                    "trigger": "process_exit",
                    "termination_kind": "normal",
                },
            )
            archive = finalize_pending(pending, runtime)
            registration = register_archive(
                runtime,
                db_path,
                archive.evidence_bundle_hash,
            )
            classifier, projection_catalog = load_approved_semantic_runtime()
            database_before = hashlib.sha256(db_path.read_bytes()).hexdigest()

            plan = plan_selected_sessions(
                runtime,
                classifier,
                projection_catalog,
                (registration.session_id,),
            )

            payload = plan.as_dict()
            self.assertEqual(
                payload["bounds"],
                {"pending_captures": 0, "historical_sessions": 1},
            )
            self.assertEqual(payload["scope"]["pending_finalization"], "disabled")
            self.assertTrue(payload["sessions"][0]["archive"]["verified"])
            self.assertEqual(
                hashlib.sha256(db_path.read_bytes()).hexdigest(),
                database_before,
            )

            (archive.dest_dir / "error.log").write_text(
                "changed after registration\n",
                encoding="utf-8",
            )
            with self.assertRaises(ArchiveIntegrityError):
                plan_selected_sessions(
                    runtime,
                    classifier,
                    projection_catalog,
                    (registration.session_id,),
                )

    def test_processing_journal_is_visible_before_pipeline_completion(self) -> None:
        """An operator must see the current stage while work is still running."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with ProcessingJournal(root) as journal:
                journal.emit(
                    "stage_started",
                    {"stage": "classification_prepare", "session_id": 14},
                )
                records = [
                    json.loads(line)
                    for line in journal.path.read_text(encoding="utf-8").splitlines()
                ]
                status = json.loads(
                    journal.status_path.read_text(encoding="utf-8")
                )
                journal_io = journal.io_summary()

                self.assertEqual(records[-1]["event"], "stage_started")
                self.assertEqual(
                    records[-1]["fields"]["stage"], "classification_prepare"
                )
                self.assertEqual(status, records[-1])
                self.assertEqual(journal_io["events_emitted"], 1)
                self.assertGreaterEqual(
                    journal_io["emit_total_ms"],
                    journal_io["append_fsync_ms"],
                )
                self.assertEqual(journal_io["status_replace_failures"], 0)
                self.assertIsNone(journal_io["status_replace_last_error"])

    def test_second_processor_cannot_acquire_the_same_runtime(self) -> None:
        """One runtime database may have only one active processor."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with ProcessorLease(root):
                with self.assertRaises(ProcessorAlreadyRunning):
                    with ProcessorLease(root):
                        self.fail("second processor unexpectedly acquired the lease")


if __name__ == "__main__":
    unittest.main()
