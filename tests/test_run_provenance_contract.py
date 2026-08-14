"""Implementation regressions for run identity and crash-source provenance."""
from __future__ import annotations

import shutil

from ck3chronicle.db import repository
from ck3chronicle.database_audit import audit_database
from ck3chronicle.harvester import PRINCIPAL_LOG_NAMES, spool_logs
from ck3chronicle.processing import process_pending
from ck3chronicle.reporting import build_session_report, latest_session_id
from ck3chronicle.session_intelligence import compare_latest
from ck3chronicle.watcher import (
    ProcessIdentity,
    infer_termination_from_crashes,
    scan_crash_inventory,
    write_capture_receipt,
)

from foundation_oracle import SIX_LOG_BYTES, write_logs
from test_classification_persistence_contract import _classifier


def _capture(runtime, logs, *, process_pid: int):
    minute = process_pid // 100
    pending = spool_logs(logs, runtime)
    write_capture_receipt(
        runtime,
        pending,
        trigger="process_exit",
        process=ProcessIdentity(process_pid, "ck3.exe", process_pid * 100),
        observed_started_at=f"2026-08-14T00:{minute:02d}:00+00:00",
        observed_ended_at=f"2026-08-14T01:{minute:02d}:00+00:00",
        termination_kind="normal",
    )
    return pending


def test_rrun_001_identical_evidence_retains_two_distinct_runs(tmp_path) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)

    first_pending = _capture(runtime, logs, process_pid=101)
    first = process_pending(runtime, _classifier())
    second_pending = _capture(runtime, logs, process_pid=202)
    second = process_pending(runtime, _classifier())

    assert first.registered_archives == 1
    assert first.registered_runs == 1
    assert second.registered_archives == 0
    assert second.registered_runs == 1
    assert first_pending.dest_dir.name != second_pending.dest_dir.name

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        assert conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 1
        runs = conn.execute(
            """
            SELECT capture_id, session_id, process_pid
            FROM capture_observations
            WHERE trigger = 'process_exit'
            ORDER BY observed_ended_at
            """
        ).fetchall()
        assert [row["capture_id"] for row in runs] == [
            first_pending.dest_dir.name,
            second_pending.dest_dir.name,
        ]
        assert len({int(row["session_id"]) for row in runs}) == 1
        assert [int(row["process_pid"]) for row in runs] == [101, 202]
        report = build_session_report(conn, int(runs[-1]["session_id"]))
        assert report["run"]["capture_id"] == second_pending.dest_dir.name
    finally:
        conn.close()


def test_rrun_002_crash_logs_are_attributed_without_duplicate_copy(tmp_path) -> None:
    game_root = tmp_path / "game-user-root"
    logs = game_root / "logs"
    crashes = game_root / "crashes"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    crashes.mkdir(parents=True)
    baseline = scan_crash_inventory(crashes)

    crash_folder = crashes / "ck3_20260814_010203"
    crash_logs = crash_folder / "logs"
    crash_logs.mkdir(parents=True)
    for name in PRINCIPAL_LOG_NAMES:
        shutil.copyfile(logs / name, crash_logs / name)
    termination, crash = infer_termination_from_crashes(
        baseline, scan_crash_inventory(crashes)
    )
    assert termination == "crash"
    assert crash is not None

    pending = spool_logs(logs, runtime)
    write_capture_receipt(
        runtime,
        pending,
        trigger="process_exit",
        process=ProcessIdentity(303, "ck3.exe", 30300),
        observed_started_at="2026-08-14T01:00:00+00:00",
        observed_ended_at="2026-08-14T01:05:00+00:00",
        termination_kind=termination,
        crash=crash,
    )
    processed = process_pending(runtime, _classifier())
    assert processed.reconciliation_errors == ()
    # Exact crash-source hashes are a durable projection. Later processing
    # must not re-read a crash folder that was already reconciled.
    shutil.rmtree(crash_folder)
    repeated = process_pending(runtime, _classifier())
    assert repeated.registered_runs == 0
    assert repeated.reconciliation_errors == ()

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        run = conn.execute(
            "SELECT * FROM capture_observations WHERE capture_id = ?",
            (pending.dest_dir.name,),
        ).fetchone()
        assert run["termination_kind"] == "crash"
        assert run["crash_folder_name"] == crash_folder.name
        origins = repository.get_run_file_origins(
            conn, int(run["observation_id"])
        )
        by_name = {row["rel_path"]: row for row in origins}
        for name in PRINCIPAL_LOG_NAMES:
            assert by_name[name]["origin_kind"] == "live_after_crash"
            assert by_name[name]["crash_equivalence"] == "exact"
            assert by_name[name]["preserved_crash_rel_path"] is None
        report = build_session_report(conn, int(run["session_id"]))
        assert report["run"]["termination_kind"] == "crash"
        assert report["run"]["crash"]["folder_name"] == crash_folder.name
    finally:
        conn.close()

    assert not (runtime / "crash_evidence").exists()


def test_rrun_003_different_crash_log_is_preserved_and_linked(tmp_path) -> None:
    game_root = tmp_path / "game-user-root"
    logs = game_root / "logs"
    crashes = game_root / "crashes"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    crashes.mkdir(parents=True)
    baseline = scan_crash_inventory(crashes)
    crash_folder = crashes / "ck3_20260814_020304"
    crash_logs = crash_folder / "logs"
    crash_logs.mkdir(parents=True)
    for name in PRINCIPAL_LOG_NAMES:
        shutil.copyfile(logs / name, crash_logs / name)
    crash_error = SIX_LOG_BYTES["error.log"] + b"crash-only-tail\n"
    (crash_logs / "error.log").write_bytes(crash_error)
    termination, crash = infer_termination_from_crashes(
        baseline, scan_crash_inventory(crashes)
    )

    pending = spool_logs(logs, runtime)
    write_capture_receipt(
        runtime,
        pending,
        trigger="process_exit",
        process=ProcessIdentity(404, "ck3.exe", 40400),
        termination_kind=termination,
        crash=crash,
    )
    processed = process_pending(runtime, _classifier())
    assert processed.reconciliation_errors == ()

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        run = repository.get_run_by_capture_id(conn, pending.dest_dir.name)
        origins = repository.get_run_file_origins(
            conn, int(run["observation_id"])
        )
        error_origin = next(row for row in origins if row["rel_path"] == "error.log")
        assert error_origin["crash_equivalence"] == "different"
        retained = runtime / error_origin["preserved_crash_rel_path"]
        assert retained.read_bytes() == crash_error
    finally:
        conn.close()


def test_rrun_004_audit_rejects_missing_receipt_file_origin(tmp_path) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    pending = _capture(runtime, logs, process_pid=505)
    process_pending(runtime, _classifier())

    conn = repository.open_db(runtime / "ck3chronicle.db")
    run = repository.get_run_by_capture_id(conn, pending.dest_dir.name)
    conn.execute(
        """
        DELETE FROM run_file_origins
        WHERE run_file_origin_id = (
            SELECT MIN(run_file_origin_id)
            FROM run_file_origins
            WHERE observation_id = ?
        )
        """,
        (run["observation_id"],),
    )
    conn.commit()
    conn.close()

    audit = audit_database(runtime)
    assert audit["status"] == "fail"
    assert any(item["code"] == "DB-RUN-002" for item in audit["findings"])


def test_rrun_005_latest_and_previous_follow_a_b_a_run_chronology(tmp_path) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    first_a = _capture(runtime, logs, process_pid=101)
    first_result = process_pending(runtime, _classifier())
    first_a_session = first_result.latest_report["session"]["session_id"]

    variant = dict(SIX_LOG_BYTES)
    variant["error.log"] = SIX_LOG_BYTES["error.log"].replace(
        b"Error one", b"Error two"
    )
    write_logs(logs, variant)
    middle_b = _capture(runtime, logs, process_pid=202)
    middle_result = process_pending(runtime, _classifier())
    middle_b_session = middle_result.latest_report["session"]["session_id"]
    assert middle_b_session != first_a_session

    write_logs(logs, SIX_LOG_BYTES)
    latest_a = _capture(runtime, logs, process_pid=303)
    latest_result = process_pending(runtime, _classifier())
    assert latest_result.latest_report["session"]["session_id"] == first_a_session

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        assert latest_session_id(conn) == first_a_session
        comparison = compare_latest(conn)
        assert comparison["schema_version"] == 2
        assert comparison["previous_session"]["session_id"] == middle_b_session
        assert comparison["previous_session"]["capture_id"] == middle_b.dest_dir.name
        assert comparison["current_session"]["session_id"] == first_a_session
        assert comparison["current_session"]["capture_id"] == latest_a.dest_dir.name
        assert comparison["current_session"]["capture_id"] != first_a.dest_dir.name
    finally:
        conn.close()
