"""Implementation regressions for run identity and crash-source provenance."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from ck3chronicle.db import repository
from ck3chronicle.cli import _print_executive_report
from ck3chronicle.database_audit import audit_database
from ck3chronicle.harvester import (
    ArchiveIntegrityError,
    PRINCIPAL_LOG_NAMES,
    spool_logs,
)
from ck3chronicle.processing import process_pending
from ck3chronicle.reporting import build_session_report, latest_session_id
from ck3chronicle.run_registry import reconcile_run_receipts
from ck3chronicle.run_receipts import RunReceiptError, finalized_receipts
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


def test_rrun_000_finalized_receipt_symlinks_are_rejected(
    tmp_path, monkeypatch
) -> None:
    directory = tmp_path / "run_receipts" / "finalized"
    directory.mkdir(parents=True)
    receipt = directory / "capture.json"
    receipt.write_text("{}\n", encoding="utf-8")
    original = Path.is_symlink

    def pretend_receipt_is_symlink(path):
        return path == receipt or original(path)

    monkeypatch.setattr(Path, "is_symlink", pretend_receipt_is_symlink)
    with pytest.raises(RunReceiptError, match="symlink"):
        finalized_receipts(tmp_path)


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


def test_rrun_002_crash_logs_are_attributed_without_duplicate_copy(
    tmp_path, capsys
) -> None:
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
    exception_bytes = b"Unhandled exception: 0xC0000005\n"
    exception_source = crash_folder / "exception.txt"
    exception_source.write_bytes(exception_bytes)
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
    protected_exception = (
        runtime / "crash_evidence" / pending.dest_dir.name / "exception.txt"
    )
    assert protected_exception.read_bytes() == exception_bytes
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
        assert run["crash_exception_status"] == "captured"
        assert run["crash_exception_source_rel_path"] == "exception.txt"
        assert run["crash_exception_retained_path"] == (
            f"crash_evidence/{pending.dest_dir.name}/exception.txt"
        )
        assert run["crash_exception_sha256"] == hashlib.sha256(
            exception_bytes
        ).hexdigest()
        assert run["crash_exception_bytes"] == len(exception_bytes)
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
        assert report["run"]["crash"]["exception"]["status"] == "captured"
        assert report["run"]["crash"]["exception"]["retained_path"] == (
            f"crash_evidence/{pending.dest_dir.name}/exception.txt"
        )
        _print_executive_report(report)
        assert "Crash exception: captured; retained=crash_evidence/" in (
            capsys.readouterr().out
        )
    finally:
        conn.close()

    retained_files = sorted(
        path.relative_to(runtime).as_posix()
        for path in (runtime / "crash_evidence").rglob("*")
        if path.is_file()
    )
    assert retained_files == [
        f"crash_evidence/{pending.dest_dir.name}/exception.txt"
    ]
    assert audit_database(runtime)["status"] == "pass"
    protected_exception.write_bytes(b"corrupt\n")
    corrupt_audit = audit_database(runtime)
    assert corrupt_audit["status"] == "fail"
    assert any(
        item["code"] == "DB-RUN-004" for item in corrupt_audit["findings"]
    )


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


def test_rrun_006_crash_without_exception_is_explicitly_absent(tmp_path) -> None:
    game_root = tmp_path / "game-user-root"
    logs = game_root / "logs"
    crashes = game_root / "crashes"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    crashes.mkdir(parents=True)
    baseline = scan_crash_inventory(crashes)
    crash_folder = crashes / "ck3_20260814_030405"
    (crash_folder / "logs").mkdir(parents=True)
    termination, crash = infer_termination_from_crashes(
        baseline, scan_crash_inventory(crashes)
    )

    pending = spool_logs(logs, runtime)
    write_capture_receipt(
        runtime,
        pending,
        trigger="process_exit",
        process=ProcessIdentity(606, "ck3.exe", 60600),
        termination_kind=termination,
        crash=crash,
    )
    assert not (runtime / "crash_evidence").exists()
    processed = process_pending(runtime, _classifier())
    assert processed.reconciliation_errors == ()

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        run = repository.get_run_by_capture_id(conn, pending.dest_dir.name)
        assert run["termination_kind"] == "crash"
        assert run["crash_exception_status"] == "absent"
        report = build_session_report(conn, int(run["session_id"]))
        assert report["run"]["crash"]["exception"]["status"] == "absent"
        assert report["run"]["crash"]["exception"]["retained_path"] is None
    finally:
        conn.close()


def test_rrun_007_stale_crash_folder_is_not_associated_or_copied(tmp_path) -> None:
    game_root = tmp_path / "game-user-root"
    logs = game_root / "logs"
    crashes = game_root / "crashes"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    stale = crashes / "ck3_20260813_010203"
    stale.mkdir(parents=True)
    (stale / "exception.txt").write_bytes(b"old crash\n")
    baseline = scan_crash_inventory(crashes)
    termination, crash = infer_termination_from_crashes(
        baseline, scan_crash_inventory(crashes)
    )
    assert termination == "normal"
    assert crash is None

    pending = spool_logs(logs, runtime)
    write_capture_receipt(
        runtime,
        pending,
        trigger="process_exit",
        process=ProcessIdentity(707, "ck3.exe", 70700),
        termination_kind=termination,
        crash=crash,
    )
    assert not (runtime / "crash_evidence").exists()
    processed = process_pending(runtime, _classifier())
    assert processed.reconciliation_errors == ()

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        run = repository.get_run_by_capture_id(conn, pending.dest_dir.name)
        assert run["termination_kind"] == "normal"
        assert run["crash_exception_status"] == "not_applicable"
    finally:
        conn.close()


def test_rrun_008_v1_crash_receipt_remains_truthfully_unavailable(tmp_path) -> None:
    game_root = tmp_path / "game-user-root"
    logs = game_root / "logs"
    crashes = game_root / "crashes"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    crashes.mkdir(parents=True)
    baseline = scan_crash_inventory(crashes)
    crash_folder = crashes / "ck3_20260814_040506"
    crash_folder.mkdir()
    (crash_folder / "exception.txt").write_bytes(b"historical exception\n")
    termination, crash = infer_termination_from_crashes(
        baseline, scan_crash_inventory(crashes)
    )

    pending = spool_logs(logs, runtime)
    write_capture_receipt(
        runtime,
        pending,
        trigger="process_exit",
        process=ProcessIdentity(808, "ck3.exe", 80800),
        termination_kind=termination,
        crash=crash,
    )
    process_pending(runtime, _classifier())

    db_path = runtime / "ck3chronicle.db"
    conn = repository.open_db(db_path)
    try:
        conn.execute(
            "DELETE FROM capture_observations WHERE capture_id = ?",
            (pending.dest_dir.name,),
        )
        conn.commit()
    finally:
        conn.close()

    receipt_path = (
        runtime / "run_receipts" / "finalized" / f"{pending.dest_dir.name}.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["schema_version"] = 1
    receipt.pop("crash_exception")
    receipt_path.write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    summary = reconcile_run_receipts(runtime, db_path)
    assert summary.errors == ()
    assert summary.registered == 1
    conn = repository.open_db(db_path)
    try:
        run = repository.get_run_by_capture_id(conn, pending.dest_dir.name)
        assert run["termination_kind"] == "crash"
        assert run["crash_exception_status"] == "unavailable"
        assert run["crash_exception_source_rel_path"] == "exception.txt"
        assert run["crash_exception_retained_path"] is None
    finally:
        conn.close()


def test_rrun_009_corrupt_protected_exception_is_a_hard_integrity_failure(
    tmp_path
) -> None:
    game_root = tmp_path / "game-user-root"
    logs = game_root / "logs"
    crashes = game_root / "crashes"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    crashes.mkdir(parents=True)
    baseline = scan_crash_inventory(crashes)
    crash_folder = crashes / "ck3_20260814_050607"
    crash_folder.mkdir()
    (crash_folder / "exception.txt").write_bytes(b"original exception\n")
    termination, crash = infer_termination_from_crashes(
        baseline, scan_crash_inventory(crashes)
    )
    pending = spool_logs(logs, runtime)
    write_capture_receipt(
        runtime,
        pending,
        trigger="process_exit",
        process=ProcessIdentity(909, "ck3.exe", 90900),
        termination_kind=termination,
        crash=crash,
    )
    process_pending(runtime, _classifier())

    protected = runtime / "crash_evidence" / pending.dest_dir.name / "exception.txt"
    protected.write_bytes(b"corrupt exception\n")

    with pytest.raises(
        ArchiveIntegrityError,
        match="captured crash exception fails integrity verification",
    ):
        process_pending(runtime, _classifier())


def test_rrun_010_unbound_legacy_run_is_upgraded_from_immutable_receipt(
    tmp_path
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    pending = _capture(runtime, logs, process_pid=100)
    process_pending(runtime, _classifier())
    db_path = runtime / "ck3chronicle.db"

    conn = repository.open_db(db_path)
    try:
        conn.execute(
            """
            UPDATE capture_observations
            SET receipt_sha256 = NULL, process_pid = NULL,
                trigger = 'legacy_import'
            WHERE capture_id = ?
            """,
            (pending.dest_dir.name,),
        )
        conn.commit()
    finally:
        conn.close()

    summary = reconcile_run_receipts(runtime, db_path, strict_integrity=True)
    assert summary.already_registered == 1
    assert summary.errors == ()
    conn = repository.open_db(db_path)
    try:
        row = repository.get_run_by_capture_id(conn, pending.dest_dir.name)
        assert row["receipt_sha256"] is not None
        assert row["process_pid"] == 100
        assert row["trigger"] == "process_exit"
    finally:
        conn.close()


def test_rrun_011_bound_run_projection_mismatch_is_rejected(tmp_path) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    pending = _capture(runtime, logs, process_pid=100)
    process_pending(runtime, _classifier())
    db_path = runtime / "ck3chronicle.db"

    conn = repository.open_db(db_path)
    try:
        conn.execute(
            "UPDATE capture_observations SET trigger = 'tampered' "
            "WHERE capture_id = ?",
            (pending.dest_dir.name,),
        )
        conn.commit()
    finally:
        conn.close()

    with pytest.raises(
        ArchiveIntegrityError,
        match="run receipt projection disagrees with indexed run",
    ):
        reconcile_run_receipts(runtime, db_path, strict_integrity=True)
