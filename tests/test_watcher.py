"""Tests for auditable, process-identity CK3 lifecycle monitoring."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import ck3chronicle.watcher as watcher
from ck3chronicle.harvester import spool_logs
from ck3chronicle.watcher import (
    EventJournal,
    ProcessIdentity,
    WatcherAlreadyRunning,
    WatcherLease,
    WatchState,
    capture_receipt_matches,
    ensure_existing_logs_receipted,
    watch_sessions,
    write_capture_receipt,
)


CK3_A = ProcessIdentity(pid=101, image_name="ck3.exe", started_ns=1_000)
CK3_B = ProcessIdentity(pid=202, image_name="ck3.exe", started_ns=2_000)


def _logs(root: Path) -> Path:
    root.mkdir()
    (root / "error.log").write_bytes(b"error")
    (root / "debug.log").write_bytes(b"debug")
    (root / "game.log").write_bytes(b"game")
    return root


class _SequenceProbe:
    def __init__(self, values: list[ProcessIdentity | None]):
        self.values = values
        self.index = 0

    def __call__(self) -> ProcessIdentity | None:
        value = self.values[self.index]
        self.index += 1
        return value

    def done(self) -> bool:
        return self.index >= len(self.values)


class _Clock:
    def __init__(self):
        self.value = 0.0

    def __call__(self) -> float:
        self.value += 1.0
        return self.value


def _run(
    tmp_path: Path,
    observations: list[ProcessIdentity | None],
    *,
    recover: bool = False,
):
    logs = _logs(tmp_path / "logs")
    probe = _SequenceProbe(observations)
    events: list[tuple[str, dict]] = []
    triggers: list[str] = []
    count = watch_sessions(
        logs_root=logs,
        capture=lambda trigger, process: triggers.append(trigger) or "captured",
        process_probe=probe,
        startup_recovery_needed=lambda: recover,
        event_sink=lambda event, fields: events.append((event, fields)),
        poll_seconds=0.01,
        heartbeat_seconds=2.0,
        stop_requested=probe.done,
        sleep=lambda seconds: None,
        monotonic=_Clock(),
    )
    return count, triggers, events


def test_watch_state_records_identity_transitions_without_startup_trigger():
    state = WatchState()

    assert state.observe(None).kind == "initial_absent"
    assert state.observe(None) is None
    assert state.observe(CK3_A).kind == "game_started"
    assert state.observe(CK3_A) is None
    exit_transition = state.observe(None)
    assert exit_transition.kind == "game_exited"
    assert exit_transition.previous == CK3_A


def test_absent_heartbeats_do_not_copy_when_last_capture_matches(tmp_path: Path):
    count, triggers, events = _run(tmp_path, [None] * 6)

    assert count == 0
    assert triggers == []
    assert [event for event, _ in events[:2]] == [
        "watcher_started",
        "existing_logs_already_captured",
    ]
    assert any(event == "heartbeat" for event, _ in events)
    assert not any(event.startswith("capture_") for event, _ in events)


def test_unmatched_existing_logs_are_recovered_once_not_each_poll(tmp_path: Path):
    count, triggers, events = _run(tmp_path, [None] * 6, recover=True)

    assert count == 1
    assert triggers == ["startup_recovery"]
    assert [event for event, _ in events].count("capture_started") == 1
    assert [event for event, _ in events].count("capture_completed") == 1


def test_full_absent_running_absent_cycle_copies_exactly_once(tmp_path: Path):
    count, triggers, events = _run(
        tmp_path,
        [None, None, CK3_A, CK3_A, None, None],
    )

    names = [event for event, _ in events]
    assert count == 1
    assert triggers == ["process_exit"]
    assert names.index("game_started") < names.index("game_exited")
    assert names.index("game_exited") < names.index("capture_started")
    assert names.index("capture_started") < names.index("capture_completed")


def test_started_during_game_is_labeled_attached_then_captures_exit(tmp_path: Path):
    count, triggers, events = _run(tmp_path, [CK3_A, CK3_A, None, None])

    assert count == 1
    assert triggers == ["process_exit"]
    started = events[0]
    assert started[0] == "watcher_started"
    assert started[1]["state"] == "attached_to_existing_process"
    assert started[1]["process"]["pid"] == CK3_A.pid


def test_process_replacement_is_visible_and_never_copies_while_running(
    tmp_path: Path,
):
    count, triggers, events = _run(tmp_path, [CK3_A, CK3_B, CK3_B, None])

    replacement = next(fields for event, fields in events if event == "process_replaced")
    assert replacement["previous_process"]["pid"] == CK3_A.pid
    assert replacement["current_process"]["pid"] == CK3_B.pid
    assert count == 1
    assert triggers == ["process_exit"]


def test_running_heartbeat_names_process_and_never_attempts_capture(tmp_path: Path):
    count, triggers, events = _run(tmp_path, [CK3_A] * 6)

    heartbeats = [fields for event, fields in events if event == "heartbeat"]
    assert heartbeats
    assert all(item["state"] == "running" for item in heartbeats)
    assert all(item["process"]["pid"] == CK3_A.pid for item in heartbeats)
    assert count == 0
    assert triggers == []


def test_capture_receipt_matches_metadata_without_reading_log_contents(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    pending = spool_logs(logs, archive, abort_if=lambda: False)

    receipt = write_capture_receipt(
        archive,
        pending,
        trigger="process_exit",
        process=CK3_A,
    )

    assert receipt.is_file()
    assert json.loads(receipt.read_text(encoding="utf-8"))["process"]["pid"] == 101
    assert capture_receipt_matches(logs, archive) is True
    (logs / "error.log").write_bytes(b"changed error")
    assert capture_receipt_matches(logs, archive) is False


def test_matching_pre_receipt_pending_copy_is_adopted_without_another_copy(
    tmp_path: Path,
):
    logs = _logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    pending = spool_logs(logs, archive, abort_if=lambda: False)

    assert not (archive / "watch" / "last_capture.json").exists()
    assert ensure_existing_logs_receipted(logs, archive) is True
    assert (archive / "watch" / "last_capture.json").is_file()
    assert capture_receipt_matches(logs, archive) is True
    assert list((archive / "pending").iterdir()) == [pending.dest_dir]


def test_event_journal_is_machine_readable_and_flushed_immediately(tmp_path: Path):
    with EventJournal(tmp_path) as journal:
        journal.emit("watcher_started", {"state": "absent"})
        lines = journal.path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["schema_version"] == 1
    assert record["event"] == "watcher_started"
    assert record["state"] == "absent"
    assert record["watcher_pid"] > 0


def test_observed_lifecycle_writes_journal_pending_copy_and_process_receipt(
    tmp_path: Path,
):
    logs = _logs(tmp_path / "logs")
    archive = tmp_path / "archive"
    probe = _SequenceProbe([None, CK3_A, CK3_A, None])

    def capture(trigger: str, process: ProcessIdentity | None):
        pending = spool_logs(logs, archive, abort_if=lambda: False)
        write_capture_receipt(
            archive,
            pending,
            trigger=trigger,
            process=process,
        )
        return pending

    with EventJournal(archive) as journal:
        count = watch_sessions(
            logs_root=logs,
            capture=capture,
            process_probe=probe,
            startup_recovery_needed=lambda: False,
            event_sink=journal.emit,
            poll_seconds=0.01,
            heartbeat_seconds=60.0,
            stop_requested=probe.done,
            sleep=lambda seconds: None,
        )
        records = [
            json.loads(line)
            for line in journal.path.read_text(encoding="utf-8").splitlines()
        ]

    assert count == 1
    assert [record["event"] for record in records] == [
        "watcher_started",
        "existing_logs_already_captured",
        "game_started",
        "game_exited",
        "capture_started",
        "capture_completed",
        "watcher_stopped",
    ]
    pending_dirs = list((archive / "pending").iterdir())
    assert len(pending_dirs) == 1
    assert not (archive / "sessions").exists()
    assert not (archive / "ck3chronicle.db").exists()
    receipt = json.loads(
        (archive / "watch" / "last_capture.json").read_text(encoding="utf-8")
    )
    assert receipt["trigger"] == "process_exit"
    assert receipt["process"]["pid"] == CK3_A.pid


def test_watcher_lease_prevents_two_watchers_for_one_runtime(tmp_path: Path):
    with WatcherLease(tmp_path):
        with pytest.raises(WatcherAlreadyRunning):
            with WatcherLease(tmp_path):
                pass

    with WatcherLease(tmp_path):
        pass


def test_windows_process_probe_uses_exact_image_and_process_identity(monkeypatch):
    monkeypatch.setattr(watcher.platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        watcher,
        "_windows_process_entries",
        lambda: (
            watcher._ProcessEntry(10, "ck3-helper.exe"),
            watcher._ProcessEntry(20, "ck3.exe"),
        ),
    )
    monkeypatch.setattr(watcher, "_windows_process_started_ns", lambda pid: 1234)

    assert watcher.find_process("ck3.exe") == ProcessIdentity(20, "ck3.exe", 1234)
    assert watcher.find_process("other.exe") is None
    assert watcher.is_process_running("ck3.exe") is True
