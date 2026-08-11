"""Auditable CK3 process lifecycle monitoring and copy-only capture triggers."""
from __future__ import annotations

import ctypes
import json
import os
import platform
import subprocess
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, TextIO, TypeVar

from .harvester import (
    InvalidCaptureInput,
    PendingCapture,
    PendingFileStat,
    UnstableCapture,
    discover_logs,
)

T = TypeVar("T")
EventSink = Callable[[str, dict[str, Any]], None]
RECEIPT_VERSION = 1
EVENT_VERSION = 1


class ProcessProbeError(RuntimeError):
    """The operating system process inventory could not be read safely."""


class WatcherAlreadyRunning(RuntimeError):
    """Another watcher holds the runtime's operating-system lock."""


@dataclass(frozen=True)
class ProcessIdentity:
    """A particular operating-system process, not merely a running Boolean."""

    pid: int
    image_name: str
    started_ns: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "pid": self.pid,
            "image_name": self.image_name,
            "started_ns": self.started_ns,
        }


@dataclass(frozen=True)
class WatchTransition:
    """A state change produced by one process observation."""

    kind: str
    previous: ProcessIdentity | None
    current: ProcessIdentity | None


@dataclass
class WatchState:
    """Track the exact CK3 process identity across observations."""

    initialized: bool = False
    active_process: ProcessIdentity | None = None

    def observe(self, process: ProcessIdentity | None) -> WatchTransition | None:
        if not self.initialized:
            self.initialized = True
            self.active_process = process
            return WatchTransition(
                "initial_running" if process is not None else "initial_absent",
                None,
                process,
            )

        previous = self.active_process
        if previous == process:
            return None
        self.active_process = process
        if previous is None and process is not None:
            return WatchTransition("game_started", None, process)
        if previous is not None and process is None:
            return WatchTransition("game_exited", previous, None)
        return WatchTransition("process_replaced", previous, process)


@dataclass(frozen=True)
class _ProcessEntry:
    pid: int
    image_name: str


def _windows_process_entries() -> tuple[_ProcessEntry, ...]:
    """Enumerate Windows process IDs and executable names with Toolhelp32."""
    from ctypes import wintypes

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.c_size_t),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", wintypes.LONG),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.WCHAR * 260),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    create_snapshot = kernel32.CreateToolhelp32Snapshot
    create_snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    create_snapshot.restype = wintypes.HANDLE
    process_first = kernel32.Process32FirstW
    process_first.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    process_first.restype = wintypes.BOOL
    process_next = kernel32.Process32NextW
    process_next.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    process_next.restype = wintypes.BOOL
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    handle = create_snapshot(0x00000002, 0)  # TH32CS_SNAPPROCESS
    invalid_handle = ctypes.c_void_p(-1).value
    if handle in (None, invalid_handle):
        raise ProcessProbeError(
            f"Windows process snapshot failed: {ctypes.get_last_error()}"
        )
    entries: list[_ProcessEntry] = []
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        if not process_first(handle, ctypes.byref(entry)):
            raise ProcessProbeError(
                f"Windows process enumeration failed: {ctypes.get_last_error()}"
            )
        while True:
            entries.append(_ProcessEntry(int(entry.th32ProcessID), entry.szExeFile))
            if not process_next(handle, ctypes.byref(entry)):
                error = ctypes.get_last_error()
                if error == 18:  # ERROR_NO_MORE_FILES
                    break
                raise ProcessProbeError(
                    f"Windows process enumeration failed: {error}"
                )
    finally:
        close_handle(handle)
    return tuple(entries)


def _windows_process_started_ns(pid: int) -> int | None:
    """Return a Windows process creation timestamp, retaining PID-only fallback."""
    from ctypes import wintypes

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    open_process = kernel32.OpenProcess
    open_process.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    open_process.restype = wintypes.HANDLE
    get_process_times = kernel32.GetProcessTimes
    get_process_times.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
        ctypes.POINTER(wintypes.FILETIME),
    ]
    get_process_times.restype = wintypes.BOOL
    close_handle = kernel32.CloseHandle
    close_handle.argtypes = [wintypes.HANDLE]
    close_handle.restype = wintypes.BOOL

    handle = open_process(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
    if not handle:
        return None
    try:
        creation = wintypes.FILETIME()
        exit_time = wintypes.FILETIME()
        kernel = wintypes.FILETIME()
        user = wintypes.FILETIME()
        if not get_process_times(
            handle,
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel),
            ctypes.byref(user),
        ):
            return None
        ticks = (creation.dwHighDateTime << 32) | creation.dwLowDateTime
        return ticks * 100
    finally:
        close_handle(handle)


def find_process(process_name: str = "ck3.exe") -> ProcessIdentity | None:
    """Return the identity of an exact process name, or ``None`` when absent."""
    system = platform.system()
    wanted = process_name.casefold()
    if system == "Windows":
        matches = [
            entry
            for entry in _windows_process_entries()
            if entry.image_name.casefold() == wanted
        ]
        if not matches:
            return None
        entry = max(matches, key=lambda item: item.pid)
        return ProcessIdentity(
            pid=entry.pid,
            image_name=entry.image_name,
            started_ns=_windows_process_started_ns(entry.pid),
        )
    if system == "Linux":
        proc = Path("/proc")
        for child in sorted(proc.iterdir(), key=lambda path: path.name):
            if not child.name.isdigit():
                continue
            try:
                image_name = (child / "comm").read_text(encoding="utf-8").strip()
                if image_name.casefold() != wanted:
                    continue
                fields = (child / "stat").read_text(encoding="utf-8").split()
                started_ns = int(fields[21]) if len(fields) > 21 else None
                return ProcessIdentity(int(child.name), image_name, started_ns)
            except (OSError, UnicodeError, ValueError):
                continue
        return None
    completed = subprocess.run(
        ["ps", "-A", "-o", "pid=,comm="],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        raise ProcessProbeError(completed.stderr.strip() or "process inventory failed")
    for line in completed.stdout.splitlines():
        fields = line.strip().split(maxsplit=1)
        if len(fields) == 2 and Path(fields[1]).name.casefold() == wanted:
            return ProcessIdentity(int(fields[0]), Path(fields[1]).name)
    return None


def is_process_running(process_name: str = "ck3.exe") -> bool:
    """Compatibility wrapper for one-shot capture safety checks."""
    return find_process(process_name) is not None


def _receipt_path(dest_root: Path) -> Path:
    return Path(dest_root) / "watch" / "last_capture.json"


def write_capture_receipt(
    dest_root: Path,
    pending: PendingCapture,
    *,
    trigger: str,
    process: ProcessIdentity | None = None,
) -> Path:
    """Atomically record which live-log metadata was successfully protected."""
    path = _receipt_path(dest_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": RECEIPT_VERSION,
        "captured_at": pending.captured_at,
        "pending_dir": str(pending.dest_dir),
        "trigger": trigger,
        "process": process.as_dict() if process is not None else None,
        "files": [
            {
                "name": item.name,
                "bytes": item.bytes,
                "source_mtime_ns": item.source_mtime_ns,
            }
            for item in pending.file_stats
        ],
    }
    fd, temporary_name = tempfile.mkstemp(prefix=".last-capture-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, sort_keys=True, separators=(",", ":"))
            stream.write("\n")
            stream.flush()
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return path


def capture_receipt_matches(logs_root: Path, dest_root: Path) -> bool:
    """Compare live file metadata with the last completed copy; read no contents."""
    path = _receipt_path(dest_root)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != RECEIPT_VERSION:
            return False
        expected = {
            item["name"]: (int(item["bytes"]), int(item["source_mtime_ns"]))
            for item in payload["files"]
        }
        actual_files = discover_logs(Path(logs_root))
        actual: dict[str, tuple[int, int]] = {}
        for file_path in actual_files:
            stat = file_path.stat()
            actual[file_path.name] = (stat.st_size, stat.st_mtime_ns)
        return actual == expected and "error.log" in actual
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError):
        return False


def ensure_existing_logs_receipted(logs_root: Path, dest_root: Path) -> bool:
    """Recognize a matching protected pending copy before considering recovery.

    This compatibility seam prevents the first receipt-aware watcher from
    duplicating a copy made by an older or manual copy-only command.
    """
    if capture_receipt_matches(logs_root, dest_root):
        return True
    try:
        live_files = discover_logs(Path(logs_root))
        live_stats = {
            path.name: (path.stat().st_size, path.stat().st_mtime_ns)
            for path in live_files
        }
        if "error.log" not in live_stats:
            return False
        pending_root = Path(dest_root) / "pending"
        candidates = sorted(
            (
                path
                for path in pending_root.iterdir()
                if path.is_dir() and not path.name.startswith(".")
            ),
            key=lambda path: path.name,
            reverse=True,
        )
        for candidate in candidates:
            candidate_files = discover_logs(candidate)
            candidate_stats = {
                path.name: (path.stat().st_size, path.stat().st_mtime_ns)
                for path in candidate_files
            }
            if candidate_stats != live_stats:
                continue
            file_stats = tuple(
                PendingFileStat(name, size, mtime_ns)
                for name, (size, mtime_ns) in candidate_stats.items()
            )
            adopted = PendingCapture(
                dest_dir=candidate,
                captured_at=datetime.fromtimestamp(
                    candidate.stat().st_ctime,
                    tz=timezone.utc,
                ).isoformat(),
                files_copied=len(file_stats),
                file_names=tuple(item.name for item in file_stats),
                file_stats=file_stats,
            )
            write_capture_receipt(
                dest_root,
                adopted,
                trigger="adopted_existing_pending",
            )
            return True
    except (InvalidCaptureInput, OSError):
        return False
    return False


class EventJournal:
    """A per-watcher JSONL journal flushed after every event."""

    def __init__(self, dest_root: Path):
        watch_root = Path(dest_root) / "watch"
        watch_root.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        self.path = watch_root / f"events-{stamp}-{os.getpid()}.jsonl"
        self._stream: TextIO | None = None

    def __enter__(self) -> EventJournal:
        self._stream = self.path.open("x", encoding="utf-8", newline="\n")
        return self

    def emit(self, event: str, fields: dict[str, Any]) -> None:
        if self._stream is None:
            raise RuntimeError("event journal is not open")
        record = {
            "schema_version": EVENT_VERSION,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "watcher_pid": os.getpid(),
            **fields,
        }
        self._stream.write(
            json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
        )
        self._stream.flush()

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self._stream is not None:
            self._stream.close()
            self._stream = None


class WatcherLease:
    """Hold a crash-releasing OS lock so only one watcher can observe a runtime."""

    def __init__(self, dest_root: Path):
        self.path = Path(dest_root) / "watch" / "watcher.lock"
        self._stream = None

    def __enter__(self) -> WatcherLease:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        stream = self.path.open("a+b")
        if stream.seek(0, os.SEEK_END) == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        try:
            if platform.system() == "Windows":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            stream.close()
            raise WatcherAlreadyRunning(
                f"another ck3chronicle watcher already holds {self.path}"
            ) from exc
        self._stream = stream
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self._stream is None:
            return
        try:
            self._stream.seek(0)
            if platform.system() == "Windows":
                import msvcrt

                msvcrt.locking(self._stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self._stream.fileno(), fcntl.LOCK_UN)
        finally:
            self._stream.close()
            self._stream = None


def _process_fields(process: ProcessIdentity | None) -> dict[str, Any]:
    return {"process": process.as_dict() if process is not None else None}


def watch_sessions(
    *,
    logs_root: Path,
    capture: Callable[[str, ProcessIdentity | None], T],
    process_probe: Callable[[], ProcessIdentity | None],
    startup_recovery_needed: Callable[[], bool] = lambda: False,
    event_sink: EventSink | None = None,
    on_capture: Callable[[T, str], None] | None = None,
    on_error: Callable[[Exception, str], None] | None = None,
    poll_seconds: float = 1.0,
    heartbeat_seconds: float = 30.0,
    stop_requested: Callable[[], bool] = lambda: False,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
) -> int:
    """Capture only conditional recovery or an observed CK3 process exit."""
    del logs_root  # retained in the public seam for caller clarity and tests
    if poll_seconds <= 0:
        raise ValueError("poll_seconds must be positive")
    if heartbeat_seconds <= 0:
        raise ValueError("heartbeat_seconds must be positive")

    def emit(event: str, **fields: Any) -> None:
        if event_sink is not None:
            event_sink(event, fields)

    state = WatchState()
    captures = 0
    polls = 0
    last_transition = datetime.now(timezone.utc).isoformat()
    last_heartbeat = monotonic()

    def attempt_capture(trigger: str, process: ProcessIdentity | None) -> None:
        nonlocal captures
        emit("capture_started", trigger=trigger, **_process_fields(process))
        try:
            result = capture(trigger, process)
        except Exception as exc:
            emit(
                "capture_failed",
                trigger=trigger,
                error_type=type(exc).__name__,
                error=str(exc),
                **_process_fields(process),
            )
            if isinstance(exc, (InvalidCaptureInput, UnstableCapture)):
                if on_error is not None:
                    on_error(exc, trigger)
                return
            raise
        captures += 1
        result_path = getattr(result, "dest_dir", None)
        emit(
            "capture_completed",
            trigger=trigger,
            pending_dir=str(result_path) if result_path is not None else None,
            **_process_fields(process),
        )
        if on_capture is not None:
            on_capture(result, trigger)

    try:
        while not stop_requested():
            try:
                observed = process_probe()
            except Exception as exc:
                emit("probe_failed", error_type=type(exc).__name__, error=str(exc))
                raise
            polls += 1
            transition = state.observe(observed)
            if transition is not None:
                last_transition = datetime.now(timezone.utc).isoformat()
                if transition.kind == "initial_absent":
                    emit("watcher_started", state="absent", process=None)
                    if startup_recovery_needed():
                        emit("uncaptured_existing_logs")
                        attempt_capture("startup_recovery", None)
                    else:
                        emit("existing_logs_already_captured")
                elif transition.kind == "initial_running":
                    emit(
                        "watcher_started",
                        state="attached_to_existing_process",
                        **_process_fields(transition.current),
                    )
                elif transition.kind == "game_started":
                    emit("game_started", **_process_fields(transition.current))
                elif transition.kind == "game_exited":
                    emit("game_exited", **_process_fields(transition.previous))
                    attempt_capture("process_exit", transition.previous)
                else:
                    emit(
                        "process_replaced",
                        previous_process=(
                            transition.previous.as_dict()
                            if transition.previous is not None
                            else None
                        ),
                        current_process=(
                            transition.current.as_dict()
                            if transition.current is not None
                            else None
                        ),
                    )

            now = monotonic()
            if now - last_heartbeat >= heartbeat_seconds:
                emit(
                    "heartbeat",
                    state="running" if state.active_process is not None else "absent",
                    polls=polls,
                    last_transition_utc=last_transition,
                    **_process_fields(state.active_process),
                )
                last_heartbeat = now
            if not stop_requested():
                sleep(poll_seconds)
    finally:
        emit(
            "watcher_stopped",
            state="running" if state.active_process is not None else "absent",
            polls=polls,
            **_process_fields(state.active_process),
        )
    return captures
