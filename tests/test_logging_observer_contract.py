"""Empirical logging-progress observation contracts."""
from __future__ import annotations

from pathlib import Path

from ck3chronicle.cli import build_parser
from ck3chronicle.logging_observer import (
    ExactBoundaryDetector,
    IncrementalTimestampLog,
    LogProgress,
)


def _progress(*, count: int, bytes_: int) -> LogProgress:
    return LogProgress("fixture.log", True, bytes_, 1, count, "12:00:00", bytes_)


def test_rlogobs_001_incremental_reader_counts_only_completed_appended_headers(
    tmp_path: Path,
) -> None:
    """Oracle: appended bytes are read once; an incomplete header waits for newline."""
    path = tmp_path / "error.log"
    first = b"[12:00:00][E][a.cpp:1]: first\ncontinuation\n"
    second = b"[12:00:01][E][b.cpp:2]: second"
    path.write_bytes(first + second)
    tracker = IncrementalTimestampLog(path)

    initial = tracker.poll()
    assert initial.timestamp_headers == 1
    assert initial.last_timestamp == "12:00:00"
    assert initial.bytes_read == len(first + second)

    with path.open("ab") as stream:
        stream.write(b"\n")
    appended = tracker.poll()
    assert appended.timestamp_headers == 2
    assert appended.last_timestamp == "12:00:01"
    assert appended.bytes_read == len(first + second) + 1

    replacement = b"[13:00:00][E][new.cpp:1]: replacement\n"
    path.write_bytes(replacement)
    reset = tracker.poll()
    assert reset.timestamp_headers == 1
    assert reset.last_timestamp == "13:00:00"


def test_rlogobs_002_boundary_requires_stable_error_and_advancing_game_log() -> None:
    """Oracle: process existence alone is insufficient evidence of the boundary."""
    detector = ExactBoundaryDetector(stall_seconds=10.0)
    error = _progress(count=100_000, bytes_=40_000_000)

    assert detector.observe(error, _progress(count=5, bytes_=100), 0.0) is False
    assert detector.observe(error, _progress(count=5, bytes_=100), 20.0) is False
    assert detector.observe(error, _progress(count=6, bytes_=120), 20.0) is True
    assert detector.observe(error, _progress(count=7, bytes_=140), 30.0) is False

    # Any 100,001st header disproves this exact boundary for the observed run.
    assert (
        detector.observe(_progress(count=100_001, bytes_=40_000_100),
                         _progress(count=8, bytes_=160), 40.0)
        is False
    )
    assert detector.boundary_seen_at is None


def test_rlogobs_003_cli_defaults_are_low_frequency_and_separate_from_watch() -> None:
    """Oracle: observation is opt-in and does not alter watcher capture timing."""
    args = build_parser().parse_args(["observe-logging"])
    assert args.command == "observe-logging"
    assert args.poll_seconds == 2.0
    assert args.heartbeat_seconds == 30.0
    assert args.stall_seconds == 60.0

