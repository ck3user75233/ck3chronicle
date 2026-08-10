"""Foreground CK3 process watcher for automatic finalized evidence capture."""
from __future__ import annotations

import ctypes
import platform
import sqlite3
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypeVar

from .harvester import CaptureError, InvalidCaptureInput, LOG_NAMES, UnstableCapture

T = TypeVar("T")


class ProcessProbeError(RuntimeError):
    """The operating system process inventory could not be read safely."""


@dataclass
class WatchState:
    """Translate process observations into one-shot capture triggers."""

    previous_running: bool | None = None

    def observe(self, running: bool) -> str | None:
        if self.previous_running is None:
            self.previous_running = running
            return None if running else "startup_existing"
        previous = self.previous_running
        self.previous_running = running
        if previous and not running:
            return "process_exit"
        return None


def evidence_fingerprint(logs_root: Path) -> tuple[tuple[str, int, int], ...]:
    """Return the approved live file set's name/size/high-resolution mtime."""
    records: list[tuple[str, int, int]] = []
    for name in LOG_NAMES:
        path = logs_root / name
        if path.exists():
            if path.is_symlink() or not path.is_file():
                raise InvalidCaptureInput(f"evidence source is not a regular file: {name}")
            stat = path.stat()
            records.append((name, stat.st_size, stat.st_mtime_ns))
    if not any(name == "error.log" for name, _, _ in records):
        raise InvalidCaptureInput("mandatory error.log is missing")
    return tuple(records)


def wait_for_stable_evidence(
    logs_root: Path,
    *,
    stable_seconds: float = 2.0,
    poll_seconds: float = 0.5,
    timeout_seconds: float = 30.0,
    monotonic: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
    abort_if: Callable[[], bool] | None = None,
) -> tuple[tuple[str, int, int], ...]:
    """Wait until the complete approved log inventory remains unchanged."""
    if stable_seconds < 0 or poll_seconds <= 0 or timeout_seconds <= 0:
        raise ValueError("watch timing values must be positive")
    deadline = monotonic() + timeout_seconds
    previous: tuple[tuple[str, int, int], ...] | None = None
    unchanged_since: float | None = None
    while True:
        if abort_if is not None and abort_if():
            raise UnstableCapture("CK3 restarted before evidence capture settled")
        now = monotonic()
        current = evidence_fingerprint(logs_root)
        if current == previous:
            if unchanged_since is not None and now - unchanged_since >= stable_seconds:
                return current
        else:
            previous = current
            unchanged_since = now
        if now >= deadline:
            raise UnstableCapture("evidence did not settle before capture timeout")
        sleep(min(poll_seconds, max(0.0, deadline - now)))


def _windows_process_names() -> tuple[str, ...]:
    """Enumerate executable names with Toolhelp32; raise instead of guessing."""
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
    names: list[str] = []
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        if not process_first(handle, ctypes.byref(entry)):
            raise ProcessProbeError(
                f"Windows process enumeration failed: {ctypes.get_last_error()}"
            )
        while True:
            names.append(entry.szExeFile)
            if not process_next(handle, ctypes.byref(entry)):
                error = ctypes.get_last_error()
                if error == 18:  # ERROR_NO_MORE_FILES
                    break
                raise ProcessProbeError(
                    f"Windows process enumeration failed: {error}"
                )
    finally:
        close_handle(handle)
    return tuple(names)


def is_process_running(process_name: str = "ck3.exe") -> bool:
    """Return whether an exact process name is running, without dependencies."""
    system = platform.system()
    wanted = process_name.casefold()
    if system == "Windows":
        return any(name.casefold() == wanted for name in _windows_process_names())
    if system == "Linux":
        proc = Path("/proc")
        for child in proc.iterdir():
            if child.name.isdigit():
                try:
                    if (child / "comm").read_text(encoding="utf-8").strip().casefold() == wanted:
                        return True
                except (OSError, UnicodeError):
                    continue
        return False
    completed = subprocess.run(
        ["ps", "-A", "-o", "comm="],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return any(line.strip().casefold() == wanted for line in completed.stdout.splitlines())


def watch_sessions(
    *,
    logs_root: Path,
    capture: Callable[[str], T],
    process_probe: Callable[[], bool],
    on_capture: Callable[[T, str], None] | None = None,
    on_error: Callable[[Exception, str], None] | None = None,
    poll_seconds: float = 1.0,
    stable_seconds: float = 2.0,
    timeout_seconds: float = 30.0,
    stop_requested: Callable[[], bool] = lambda: False,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    """Capture existing logs once, then each observed CK3 process exit."""
    if poll_seconds <= 0:
        raise ValueError("poll_seconds must be positive")
    state = WatchState()
    captures = 0
    pending_trigger: str | None = None
    while not stop_requested():
        running = process_probe()
        trigger = state.observe(running)
        if trigger is not None:
            pending_trigger = trigger
        if pending_trigger is not None and not running:
            try:
                wait_for_stable_evidence(
                    logs_root,
                    stable_seconds=stable_seconds,
                    poll_seconds=min(poll_seconds, 0.5),
                    timeout_seconds=timeout_seconds,
                    sleep=sleep,
                    abort_if=process_probe,
                )
                result = capture(pending_trigger)
                captures += 1
                if on_capture is not None:
                    on_capture(result, pending_trigger)
                pending_trigger = None
            except Exception as exc:
                if not isinstance(exc, (InvalidCaptureInput, UnstableCapture)):
                    raise
                if on_error is not None:
                    on_error(exc, pending_trigger)
                # Missing mandatory input will not become valid without a new
                # run. Instability is retried while the process stays absent.
                if isinstance(exc, InvalidCaptureInput):
                    pending_trigger = None
        if not stop_requested():
            sleep(poll_seconds)
    return captures
