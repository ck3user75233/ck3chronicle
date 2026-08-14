"""Fresh reboot acceptance tests for lifecycle-triggered copy protection."""
from __future__ import annotations

from collections import deque
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from ck3chronicle import harvester
from ck3chronicle.harvester import UnstableCapture, spool_logs
from ck3chronicle.watcher import EventJournal, ProcessIdentity, watch_sessions

from foundation_oracle import SIX_LOG_BYTES, write_logs


def test_rcap_001_requires_an_observed_start_and_exit_before_copy() -> None:
    """Oracle: absent -> running -> absent produces exactly one exit copy."""
    game = ProcessIdentity(pid=41234, image_name="ck3.exe", started_ns=9001)
    observations = deque([None, game, game, None])
    captures: list[tuple[str, ProcessIdentity | None]] = []
    events: list[tuple[str, dict]] = []

    def capture(trigger: str, process: ProcessIdentity | None):
        captures.append((trigger, process))
        return SimpleNamespace(dest_dir=Path("protected-pending"))

    count = watch_sessions(
        logs_root=Path("not-read-by-the-state-machine"),
        capture=capture,
        process_probe=observations.popleft,
        startup_recovery_needed=lambda: False,
        event_sink=lambda event, fields: events.append((event, fields)),
        stop_requested=lambda: not observations,
        sleep=lambda _seconds: None,
        monotonic=iter([0.0, 1.0, 2.0, 3.0, 4.0]).__next__,
        heartbeat_seconds=100.0,
    )

    assert count == 1
    assert captures == [("process_exit", game)]
    assert [event for event, _ in events] == [
        "watcher_started",
        "existing_logs_already_captured",
        "game_started",
        "game_exited",
        "capture_started",
        "capture_completed",
        "watcher_stopped",
    ]


def test_rcap_002_heartbeat_observes_state_without_copying() -> None:
    """Oracle: an absent process can produce heartbeats but zero copy calls."""
    polls = 0
    captures: list[str] = []
    events: list[tuple[str, dict]] = []

    def probe():
        nonlocal polls
        polls += 1
        return None

    watch_sessions(
        logs_root=Path("not-read-by-the-state-machine"),
        capture=lambda trigger, _process: captures.append(trigger),
        process_probe=probe,
        startup_recovery_needed=lambda: False,
        event_sink=lambda event, fields: events.append((event, fields)),
        stop_requested=lambda: polls >= 3,
        sleep=lambda _seconds: None,
        monotonic=iter([0.0, 31.0, 62.0, 93.0]).__next__,
        heartbeat_seconds=30.0,
    )

    assert captures == []
    heartbeats = [fields for event, fields in events if event == "heartbeat"]
    assert len(heartbeats) == 3
    assert all(item["state"] == "absent" for item in heartbeats)


def test_rcap_003_spool_copies_each_approved_log_exactly_without_hashing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Oracle: copy-first protection preserves exact bytes and does no hashing."""
    logs = tmp_path / "live-logs"
    runtime = tmp_path / "runtime"
    write_logs(logs)

    def forbidden_hash(_path: Path) -> str:
        raise AssertionError("copy-first capture must not hash")

    monkeypatch.setattr(harvester, "hash_file", forbidden_hash)
    pending = spool_logs(logs, runtime, abort_if=lambda: False)

    assert pending.file_names == tuple(SIX_LOG_BYTES)
    assert pending.files_copied == 6
    assert not pending.dest_dir.name.startswith(".")
    assert not (pending.dest_dir / "manifest.json").exists()
    assert not (runtime / "ck3chronicle.db").exists()
    assert {
        path.name: path.read_bytes()
        for path in pending.dest_dir.iterdir()
        if path.is_file()
    } == SIX_LOG_BYTES


def test_rcap_004_restart_during_copy_never_publishes_completed_pending(
    tmp_path: Path,
) -> None:
    """Oracle: a relaunch detected after copying leaves no ready pending bundle."""
    logs = tmp_path / "live-logs"
    runtime = tmp_path / "runtime"
    write_logs(logs)
    checks = iter([False, True])

    with pytest.raises(UnstableCapture):
        spool_logs(logs, runtime, abort_if=checks.__next__)

    pending_root = runtime / "pending"
    visible = [path for path in pending_root.iterdir() if not path.name.startswith(".")]
    assert visible == []


def test_rcap_005_heartbeat_is_current_state_not_unbounded_history(
    tmp_path: Path,
) -> None:
    """Oracle: lifecycle is append-only; repeated health replaces one snapshot."""
    with EventJournal(tmp_path) as journal:
        journal.emit("watcher_started", {"state": "absent"})
        journal.emit("heartbeat", {"state": "absent", "polls": 10})
        journal.emit("heartbeat", {"state": "running", "polls": 20})
        heartbeat = json.loads(journal.heartbeat_path.read_text(encoding="utf-8"))
        assert heartbeat["event"] == "heartbeat"
        assert heartbeat["state"] == "running"
        assert heartbeat["polls"] == 20
        journal.emit("game_started", {"process": {"pid": 42}})

    events = [
        json.loads(line)
        for line in journal.path.read_text(encoding="utf-8").splitlines()
    ]
    assert [item["event"] for item in events] == ["watcher_started", "game_started"]
    assert not journal.heartbeat_path.exists()
