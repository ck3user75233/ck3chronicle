"""Tests for the foreground CK3 capture watcher."""
from __future__ import annotations

from pathlib import Path
import pytest

import ck3chronicle.watcher as watcher
from ck3chronicle.harvester import UnstableCapture
from ck3chronicle.watcher import WatchState, wait_for_stable_evidence, watch_sessions


def _logs(root: Path) -> Path:
    root.mkdir()
    (root / "error.log").write_bytes(b"error")
    (root / "debug.log").write_bytes(b"debug")
    (root / "game.log").write_bytes(b"game")
    return root


def test_watch_state_captures_existing_then_only_running_to_absent_transition():
    state = WatchState()
    observations = [False, False, True, True, False, False]
    assert [state.observe(value) for value in observations] == [
        "startup_existing",
        None,
        None,
        None,
        "process_exit",
        None,
    ]


def test_watch_state_started_during_game_does_not_capture_mid_session():
    state = WatchState()
    assert state.observe(True) is None
    assert state.observe(True) is None
    assert state.observe(False) == "process_exit"


def test_stability_gate_requires_unchanged_inventory(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    now = 0.0

    def monotonic() -> float:
        return now

    def sleep(seconds: float) -> None:
        nonlocal now
        now += seconds

    fingerprint = wait_for_stable_evidence(
        logs,
        stable_seconds=1.0,
        poll_seconds=0.25,
        timeout_seconds=3.0,
        monotonic=monotonic,
        sleep=sleep,
    )
    assert {name for name, _, _ in fingerprint} == {
        "error.log",
        "debug.log",
        "game.log",
    }
    assert now >= 1.0


def test_stability_gate_rejects_continuously_changing_log(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    now = 0.0

    def monotonic() -> float:
        return now

    def sleep(seconds: float) -> None:
        nonlocal now
        now += seconds
        with (logs / "error.log").open("ab") as stream:
            stream.write(b"x")

    with pytest.raises(UnstableCapture, match="did not settle"):
        wait_for_stable_evidence(
            logs,
            stable_seconds=1.0,
            poll_seconds=0.25,
            timeout_seconds=1.0,
            monotonic=monotonic,
            sleep=sleep,
        )


def test_stability_gate_aborts_if_ck3_restarts(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    probes = iter([False, True])
    with pytest.raises(UnstableCapture, match="restarted"):
        wait_for_stable_evidence(
            logs,
            stable_seconds=1.0,
            poll_seconds=0.01,
            timeout_seconds=1.0,
            abort_if=lambda: next(probes),
            sleep=lambda seconds: None,
        )


class _SequenceProbe:
    def __init__(self, values: list[bool]):
        self.values = values
        self.index = 0

    def __call__(self) -> bool:
        value = self.values[self.index]
        self.index += 1
        return value

    def done(self) -> bool:
        return self.index >= len(self.values)


def test_watcher_does_not_repeat_capture_on_absent_polls(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    probe = _SequenceProbe([False, False, False, False, False, False])
    triggers: list[str] = []
    count = watch_sessions(
        logs_root=logs,
        capture=lambda trigger: "captured",
        process_probe=probe,
        on_capture=lambda result, trigger: triggers.append(trigger),
        poll_seconds=0.01,
        stable_seconds=0,
        stop_requested=probe.done,
        sleep=lambda seconds: None,
    )
    assert count == 1
    assert triggers == ["startup_existing"]


def test_watcher_captures_once_after_game_exit(tmp_path: Path):
    logs = _logs(tmp_path / "logs")
    probe = _SequenceProbe([True, True, False, False, False, False])
    triggers: list[str] = []
    count = watch_sessions(
        logs_root=logs,
        capture=lambda trigger: "captured",
        process_probe=probe,
        on_capture=lambda result, trigger: triggers.append(trigger),
        poll_seconds=0.01,
        stable_seconds=0,
        stop_requested=probe.done,
        sleep=lambda seconds: None,
    )
    assert count == 1
    assert triggers == ["process_exit"]


def test_windows_process_probe_uses_exact_image_name(monkeypatch):
    monkeypatch.setattr(watcher.platform, "system", lambda: "Windows")
    monkeypatch.setattr(
        watcher,
        "_windows_process_names",
        lambda: ("ck3-helper.exe", "ck3.exe"),
    )
    assert watcher.is_process_running("ck3.exe") is True
    assert watcher.is_process_running("other.exe") is False
