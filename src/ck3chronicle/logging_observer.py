"""Low-I/O empirical observation of CK3 error/game log progress."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import time
from typing import Callable

from .watcher import ProcessIdentity


_TIMESTAMP_HEADER = re.compile(br"^\[(\d{2}:\d{2}:\d{2})\]")
OBSERVATION_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class LogProgress:
    path: str
    exists: bool
    bytes: int
    mtime_ns: int | None
    timestamp_headers: int
    last_timestamp: str | None
    bytes_read: int


class IncrementalTimestampLog:
    """Count timestamp headers while reading each observed byte at most once."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._offset = 0
        self._carry = b""
        self._timestamp_headers = 0
        self._last_timestamp: str | None = None
        self._bytes_read = 0
        self._mtime_ns: int | None = None

    def _consume(self, data: bytes) -> None:
        combined = self._carry + data
        lines = combined.splitlines(keepends=True)
        self._carry = b""
        if lines and not lines[-1].endswith((b"\n", b"\r")):
            self._carry = lines.pop()
        for line in lines:
            match = _TIMESTAMP_HEADER.match(line)
            if match is None:
                continue
            self._timestamp_headers += 1
            self._last_timestamp = match.group(1).decode("ascii")

    def poll(self) -> LogProgress:
        try:
            stat = self.path.stat()
        except FileNotFoundError:
            self._offset = 0
            self._carry = b""
            self._timestamp_headers = 0
            self._last_timestamp = None
            self._mtime_ns = None
            return LogProgress(str(self.path), False, 0, None, 0, None, self._bytes_read)
        if stat.st_size < self._offset:
            self._offset = 0
            self._carry = b""
            self._timestamp_headers = 0
            self._last_timestamp = None
        if stat.st_size > self._offset:
            with self.path.open("rb") as stream:
                stream.seek(self._offset)
                data = stream.read(stat.st_size - self._offset)
            self._offset += len(data)
            self._bytes_read += len(data)
            self._consume(data)
        self._mtime_ns = stat.st_mtime_ns
        return LogProgress(
            str(self.path),
            True,
            stat.st_size,
            stat.st_mtime_ns,
            self._timestamp_headers,
            self._last_timestamp,
            self._bytes_read,
        )


@dataclass
class ExactBoundaryDetector:
    """Detect a stable 100,000 error boundary while game logging advances."""

    stall_seconds: float
    boundary_seen_at: float | None = None
    boundary_error_bytes: int | None = None
    boundary_game_bytes: int | None = None
    emitted: bool = False

    def observe(self, error: LogProgress, game: LogProgress, now: float) -> bool:
        if error.timestamp_headers != 100_000:
            self.boundary_seen_at = None
            self.boundary_error_bytes = None
            self.boundary_game_bytes = None
            self.emitted = False
            return False
        if self.boundary_error_bytes != error.bytes:
            self.boundary_seen_at = now
            self.boundary_error_bytes = error.bytes
            self.boundary_game_bytes = game.bytes
            return False
        if self.emitted or self.boundary_seen_at is None:
            return False
        game_advanced = game.bytes > int(self.boundary_game_bytes or 0)
        if game_advanced and now - self.boundary_seen_at >= self.stall_seconds:
            self.emitted = True
            return True
        return False


def observe_logging_progress(
    *,
    logs_root: Path,
    runtime_root: Path,
    process_probe: Callable[[], ProcessIdentity | None],
    poll_seconds: float = 2.0,
    heartbeat_seconds: float = 30.0,
    stall_seconds: float = 60.0,
    stop_requested: Callable[[], bool] = lambda: False,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
) -> tuple[Path, bool]:
    """Observe one absent/running/absent lifecycle and journal bounded progress."""
    if min(poll_seconds, heartbeat_seconds, stall_seconds) <= 0:
        raise ValueError("observer timing values must be positive")
    journal_root = Path(runtime_root) / "watch"
    journal_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    journal_path = journal_root / f"log-progress-{stamp}-{os.getpid()}.jsonl"
    error_log = IncrementalTimestampLog(Path(logs_root) / "error.log")
    game_log = IncrementalTimestampLog(Path(logs_root) / "game.log")
    detector = ExactBoundaryDetector(stall_seconds)
    active: ProcessIdentity | None = None
    last_heartbeat = monotonic()
    boundary_observed = False

    with journal_path.open("x", encoding="utf-8", newline="\n") as journal:
        def emit(event: str, **fields: object) -> None:
            record = {
                "schema_version": OBSERVATION_SCHEMA_VERSION,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "event": event,
                **fields,
            }
            journal.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
            journal.write("\n")
            journal.flush()

        emit("observer_started", state="awaiting_ck3")
        while not stop_requested():
            process = process_probe()
            if active is None:
                if process is None:
                    sleep(poll_seconds)
                    continue
                active = process
                emit("game_started", process=active.as_dict())
                error_log.poll()
                game_log.poll()
                last_heartbeat = monotonic()
            elif process != active:
                emit(
                    "game_exited" if process is None else "process_replaced",
                    process=active.as_dict(),
                    replacement=process.as_dict() if process is not None else None,
                )
                break

            now = monotonic()
            error = error_log.poll()
            game = game_log.poll()
            if detector.observe(error, game, now):
                boundary_observed = True
                emit(
                    "exact_100000_error_boundary_with_game_progress",
                    process=active.as_dict(),
                    error=error.__dict__,
                    game=game.__dict__,
                    stall_seconds=stall_seconds,
                )
            if now - last_heartbeat >= heartbeat_seconds:
                emit(
                    "heartbeat",
                    state="running",
                    process=active.as_dict(),
                    error=error.__dict__,
                    game=game.__dict__,
                    exact_boundary_observed=boundary_observed,
                )
                last_heartbeat = now
            sleep(poll_seconds)
        emit("observer_stopped", exact_boundary_observed=boundary_observed)
    return journal_path, boundary_observed
