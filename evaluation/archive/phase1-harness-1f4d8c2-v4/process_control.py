"""Finite subprocess execution with bounded streams and process-tree cleanup."""
from __future__ import annotations

import ctypes
import hashlib
import os
import signal
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from harness_core import file_identity


STREAM_LIMIT_BYTES = 16 * 1024 * 1024
TERMINATION_GRACE_SECONDS = 10.0


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class _BoundedReader(threading.Thread):
    def __init__(self, stream: Any, destination: Path, limit_bytes: int) -> None:
        super().__init__(daemon=True)
        self.stream = stream
        self.destination = destination
        self.limit_bytes = limit_bytes
        self.total_bytes = 0
        self.captured_bytes = 0
        self.truncated = False
        self.limit_reached = threading.Event()
        self.error: str | None = None

    def run(self) -> None:
        self.destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.destination.open("xb") as output:
                while True:
                    chunk = self.stream.read(64 * 1024)
                    if not chunk:
                        break
                    self.total_bytes += len(chunk)
                    remaining = self.limit_bytes - self.captured_bytes
                    if remaining > 0:
                        kept = chunk[:remaining]
                        output.write(kept)
                        self.captured_bytes += len(kept)
                    if len(chunk) > max(remaining, 0):
                        self.truncated = True
                        self.limit_reached.set()
                output.flush()
                os.fsync(output.fileno())
        except Exception as error:  # preserved as neutral infrastructure evidence
            self.error = f"{type(error).__module__}.{type(error).__qualname__}:{error}"
            self.limit_reached.set()


class _WindowsJob:
    def __init__(self) -> None:
        self.handle: int | None = None
        self.assigned = False
        self.assignment_error: int | None = None
        self.terminate_error: int | None = None
        self.query_error: int | None = None
        if os.name != "nt":
            return

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [
                ("ReadOperationCount", ctypes.c_ulonglong),
                ("WriteOperationCount", ctypes.c_ulonglong),
                ("OtherOperationCount", ctypes.c_ulonglong),
                ("ReadTransferCount", ctypes.c_ulonglong),
                ("WriteTransferCount", ctypes.c_ulonglong),
                ("OtherTransferCount", ctypes.c_ulonglong),
            ]

        class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", ctypes.c_ulong),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", ctypes.c_ulong),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", ctypes.c_ulong),
                ("SchedulingClass", ctypes.c_ulong),
            ]

        class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
                ("IoInfo", IO_COUNTERS),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateJobObjectW.restype = ctypes.c_void_p
        handle = kernel32.CreateJobObjectW(None, None)
        if not handle:
            raise OSError(ctypes.get_last_error(), "CreateJobObjectW failed")
        information = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        information.BasicLimitInformation.LimitFlags = 0x00002000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        ok = kernel32.SetInformationJobObject(
            ctypes.c_void_p(handle),
            9,  # JobObjectExtendedLimitInformation
            ctypes.byref(information),
            ctypes.sizeof(information),
        )
        if not ok:
            error = ctypes.get_last_error()
            kernel32.CloseHandle(ctypes.c_void_p(handle))
            raise OSError(error, "SetInformationJobObject failed")
        self.handle = int(handle)

    def assign(self, process: subprocess.Popen[bytes]) -> None:
        if os.name != "nt":
            self.assigned = True
            return
        assert self.handle is not None
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        ok = kernel32.AssignProcessToJobObject(ctypes.c_void_p(self.handle), ctypes.c_void_p(int(process._handle)))  # type: ignore[attr-defined]
        if not ok:
            self.assignment_error = ctypes.get_last_error()
            raise OSError(self.assignment_error, "AssignProcessToJobObject failed")
        self.assigned = True

    def terminate(self, exit_code: int = 124) -> bool:
        if os.name != "nt":
            return True
        assert self.handle is not None
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        ok = kernel32.TerminateJobObject(ctypes.c_void_p(self.handle), exit_code)
        if not ok:
            self.terminate_error = ctypes.get_last_error()
        return bool(ok)

    def active_process_count(self) -> int | None:
        """Return the kernel's active-process count for this Job Object."""
        if os.name != "nt":
            return None
        assert self.handle is not None

        class JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("TotalUserTime", ctypes.c_longlong),
                ("TotalKernelTime", ctypes.c_longlong),
                ("ThisPeriodTotalUserTime", ctypes.c_longlong),
                ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
                ("TotalPageFaultCount", ctypes.c_ulong),
                ("TotalProcesses", ctypes.c_ulong),
                ("ActiveProcesses", ctypes.c_ulong),
                ("TotalTerminatedProcesses", ctypes.c_ulong),
            ]

        information = JOBOBJECT_BASIC_ACCOUNTING_INFORMATION()
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        ok = kernel32.QueryInformationJobObject(
            ctypes.c_void_p(self.handle),
            1,  # JobObjectBasicAccountingInformation
            ctypes.byref(information),
            ctypes.sizeof(information),
            None,
        )
        if not ok:
            self.query_error = ctypes.get_last_error()
            return None
        return int(information.ActiveProcesses)

    def close(self) -> None:
        if os.name == "nt" and self.handle is not None:
            ctypes.WinDLL("kernel32", use_last_error=True).CloseHandle(ctypes.c_void_p(self.handle))
            self.handle = None


def _windows_process_table() -> dict[int, int]:
    if os.name != "nt":
        return {}

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.c_ulong),
            ("cntUsage", ctypes.c_ulong),
            ("th32ProcessID", ctypes.c_ulong),
            ("th32DefaultHeapID", ctypes.c_size_t),
            ("th32ModuleID", ctypes.c_ulong),
            ("cntThreads", ctypes.c_ulong),
            ("th32ParentProcessID", ctypes.c_ulong),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", ctypes.c_ulong),
            ("szExeFile", ctypes.c_wchar * 260),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateToolhelp32Snapshot.restype = ctypes.c_void_p
    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
    if snapshot == ctypes.c_void_p(-1).value:
        return {}
    table: dict[int, int] = {}
    entry = PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(entry)
    try:
        ok = kernel32.Process32FirstW(ctypes.c_void_p(snapshot), ctypes.byref(entry))
        while ok:
            table[int(entry.th32ProcessID)] = int(entry.th32ParentProcessID)
            ok = kernel32.Process32NextW(ctypes.c_void_p(snapshot), ctypes.byref(entry))
    finally:
        kernel32.CloseHandle(ctypes.c_void_p(snapshot))
    return table


def _descendants(root_pid: int) -> list[int]:
    table = _windows_process_table()
    if not table:
        return []
    found: set[int] = set()
    frontier = {root_pid}
    while frontier:
        children = {pid for pid, parent in table.items() if parent in frontier and pid not in found}
        found.update(children)
        frontier = children
    return sorted(found)


def _pid_state(pid: int) -> str:
    if os.name != "nt":
        try:
            os.kill(pid, 0)
            return "alive"
        except OSError:
            return "absent"
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenProcess.restype = ctypes.c_void_p
    handle = kernel32.OpenProcess(0x00100000 | 0x00000400, False, pid)
    if not handle:
        error = ctypes.get_last_error()
        return "absent" if error == 87 else f"inaccessible:{error}"
    exit_code = ctypes.c_ulong()
    try:
        if not kernel32.GetExitCodeProcess(ctypes.c_void_p(handle), ctypes.byref(exit_code)):
            return "query_failed"
        return "alive" if exit_code.value == 259 else f"exited:{exit_code.value}"
    finally:
        kernel32.CloseHandle(ctypes.c_void_p(handle))


def _resume_suspended_windows_process(process: subprocess.Popen[bytes]) -> dict[str, Any]:
    """Resume the sole initial thread after Job assignment, before user code runs."""
    if os.name != "nt":
        return {"created_suspended": False, "assigned_before_resume": False}

    class THREADENTRY32(ctypes.Structure):
        _fields_ = [
            ("dwSize", ctypes.c_ulong),
            ("cntUsage", ctypes.c_ulong),
            ("th32ThreadID", ctypes.c_ulong),
            ("th32OwnerProcessID", ctypes.c_ulong),
            ("tpBasePri", ctypes.c_long),
            ("tpDeltaPri", ctypes.c_long),
            ("dwFlags", ctypes.c_ulong),
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateToolhelp32Snapshot.restype = ctypes.c_void_p
    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000004, 0)  # TH32CS_SNAPTHREAD
    if snapshot == ctypes.c_void_p(-1).value:
        raise OSError(ctypes.get_last_error(), "thread snapshot failed for suspended process")
    thread_ids: list[int] = []
    entry = THREADENTRY32()
    entry.dwSize = ctypes.sizeof(entry)
    try:
        ok = kernel32.Thread32First(ctypes.c_void_p(snapshot), ctypes.byref(entry))
        while ok:
            if int(entry.th32OwnerProcessID) == process.pid:
                thread_ids.append(int(entry.th32ThreadID))
            ok = kernel32.Thread32Next(ctypes.c_void_p(snapshot), ctypes.byref(entry))
    finally:
        kernel32.CloseHandle(ctypes.c_void_p(snapshot))
    if len(thread_ids) != 1:
        raise RuntimeError(f"suspended process must expose exactly one initial thread: {thread_ids}")
    kernel32.OpenThread.restype = ctypes.c_void_p
    thread_handle = kernel32.OpenThread(0x0002, False, thread_ids[0])  # THREAD_SUSPEND_RESUME
    if not thread_handle:
        raise OSError(ctypes.get_last_error(), "OpenThread failed for suspended process")
    kernel32.ResumeThread.restype = ctypes.c_ulong
    try:
        previous_suspend_count = int(kernel32.ResumeThread(ctypes.c_void_p(thread_handle)))
        if previous_suspend_count == 0xFFFFFFFF:
            raise OSError(ctypes.get_last_error(), "ResumeThread failed")
        if previous_suspend_count != 1:
            raise RuntimeError(f"unexpected initial suspend count: {previous_suspend_count}")
    finally:
        kernel32.CloseHandle(ctypes.c_void_p(thread_handle))
    return {
        "created_suspended": True,
        "assigned_before_resume": True,
        "initial_thread_id": thread_ids[0],
        "resume_previous_suspend_count": previous_suspend_count,
    }


def run_bounded_process(
    command: list[str],
    *,
    timeout_seconds: float,
    stdout_path: Path,
    stderr_path: Path,
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
    stream_limit_bytes: int = STREAM_LIMIT_BYTES,
    sample_callback: Callable[[subprocess.Popen[bytes]], dict[str, Any] | None] | None = None,
) -> dict[str, Any]:
    """Run once, terminate the complete tree at the ceiling, and retain neutral evidence."""
    if not isinstance(timeout_seconds, (int, float)) or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be finite and positive")
    if timeout_seconds == float("inf"):
        raise ValueError("timeout_seconds must be finite")
    if stream_limit_bytes <= 0 or stream_limit_bytes > STREAM_LIMIT_BYTES:
        raise ValueError("invalid stream capture bound")
    if stdout_path == stderr_path:
        raise ValueError("stdout and stderr capture paths must differ")

    started_at = _utc_now()
    started = time.perf_counter()
    creationflags = (subprocess.CREATE_NEW_PROCESS_GROUP | getattr(subprocess, "CREATE_SUSPENDED", 0x00000004)) if os.name == "nt" else 0
    job = _WindowsJob()
    process: subprocess.Popen[bytes] | None = None
    stdout_reader: _BoundedReader | None = None
    stderr_reader: _BoundedReader | None = None
    completed_cleanup = False
    try:
        process = subprocess.Popen(
            command,
            env=env,
            cwd=str(cwd) if cwd is not None else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=creationflags,
            start_new_session=os.name != "nt",
        )
        assert process.stdout is not None and process.stderr is not None
        job.assign(process)
        stdout_reader = _BoundedReader(process.stdout, stdout_path, stream_limit_bytes)
        stderr_reader = _BoundedReader(process.stderr, stderr_path, stream_limit_bytes)
        stdout_reader.start()
        stderr_reader.start()
        launch_containment = _resume_suspended_windows_process(process)

        timed_out = False
        output_limit_exceeded = False
        output_limit_detected_during_monitor = False
        output_limit_detected_after_join = False
        resource_limit_exceeded = False
        resource_limit_evidence: dict[str, Any] | None = None
        sampler_error: str | None = None
        termination_requested = False
        terminate_job_succeeded: bool | None = None
        descendants_before_termination: list[int] = []
        deadline = started + float(timeout_seconds)
        while process.poll() is None:
            if sample_callback is not None:
                try:
                    sample_result = sample_callback(process)
                except Exception as error:
                    sampler_error = f"{type(error).__module__}.{type(error).__qualname__}:{error}"
                    break
                if sample_result is not None:
                    resource_limit_exceeded = True
                    resource_limit_evidence = sample_result
                    break
                if process.poll() is not None:
                    break
            if stdout_reader.limit_reached.is_set() or stderr_reader.limit_reached.is_set():
                output_limit_exceeded = True
                output_limit_detected_during_monitor = True
                break
            remaining = deadline - time.perf_counter()
            if remaining <= 0:
                timed_out = True
                break
            time.sleep(min(0.01, remaining))

        if process.poll() is None:
            termination_requested = True
            descendants_before_termination = _descendants(process.pid)
            if os.name == "nt":
                terminate_job_succeeded = job.terminate(124)
            else:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                    terminate_job_succeeded = True
                except OSError:
                    terminate_job_succeeded = False
            try:
                process.wait(timeout=TERMINATION_GRACE_SECONDS)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=TERMINATION_GRACE_SECONDS)

        root_exit_code = process.wait(timeout=TERMINATION_GRACE_SECONDS)
        # A clean root can still leave descendants. Do not rely on closing the
        # Job handle as implicit evidence: explicitly terminate and observe zero.
        descendants_before_close = sorted(set(descendants_before_termination) | set(_descendants(process.pid)))
        active_processes_before_cleanup = job.active_process_count()
        if os.name == "nt" and active_processes_before_cleanup not in (None, 0):
            termination_requested = True
            terminate_job_succeeded = job.terminate(124)
        active_processes_after_cleanup = job.active_process_count()
        cleanup_deadline = time.perf_counter() + TERMINATION_GRACE_SECONDS
        while os.name == "nt" and active_processes_after_cleanup not in (None, 0) and time.perf_counter() < cleanup_deadline:
            time.sleep(0.01)
            active_processes_after_cleanup = job.active_process_count()
        stdout_reader.join(timeout=TERMINATION_GRACE_SECONDS)
        stderr_reader.join(timeout=TERMINATION_GRACE_SECONDS)
        if stdout_reader.is_alive() or stderr_reader.is_alive():
            raise RuntimeError("bounded stream reader did not terminate")
        # Readers can discover a cap after a fast root has already exited.
        joined_reader_limit = stdout_reader.truncated or stderr_reader.truncated or stdout_reader.limit_reached.is_set() or stderr_reader.limit_reached.is_set()
        output_limit_detected_after_join = joined_reader_limit and not output_limit_detected_during_monitor
        output_limit_exceeded = output_limit_exceeded or joined_reader_limit
        observed_pids = [process.pid, *descendants_before_close]
        states_after = {str(pid): _pid_state(pid) for pid in observed_pids}
        unambiguous_dead_states = all(state == "absent" or state.startswith("exited:") for state in states_after.values())
        job_accounting_proves_empty = os.name != "nt" or active_processes_after_cleanup == 0
        all_terminated = job_accounting_proves_empty and unambiguous_dead_states
        ended = time.perf_counter()
        status = "timed_out" if timed_out else "output_limit_exceeded" if output_limit_exceeded else "resource_limit_exceeded" if resource_limit_exceeded else "sampler_failed" if sampler_error else "completed"
        result = {
        "schema": "ck3chronicle.phase1-bounded-process-observation",
        "schema_version": 1,
        "classification": "neutral_infrastructure_observation_no_harness_verdict",
        "status": status,
        "timed_out": timed_out,
        "output_limit_exceeded": output_limit_exceeded,
        "output_limit_detected_during_monitor": output_limit_detected_during_monitor,
        "output_limit_detected_after_join": output_limit_detected_after_join,
        "resource_limit_exceeded": resource_limit_exceeded,
        "resource_limit_evidence": resource_limit_evidence,
        "sampler_error": sampler_error,
        "timeout_seconds": float(timeout_seconds),
        "elapsed_seconds": ended - started,
        "started_at_utc": started_at,
        "ended_at_utc": _utc_now(),
        "command": command,
        "cwd": str(cwd) if cwd is not None else None,
        "root_pid": process.pid,
        "root_exit_code": root_exit_code,
        "retry_performed": False,
        "process_tree": {
            "platform": os.name,
            **launch_containment,
            "job_object_assigned": job.assigned,
            "job_assignment_error": job.assignment_error,
            "termination_requested": termination_requested,
            "terminate_job_succeeded": terminate_job_succeeded,
            "terminate_job_error": job.terminate_error,
            "job_query_error": job.query_error,
            "job_active_processes_before_cleanup": active_processes_before_cleanup,
            "job_active_processes_after_cleanup": active_processes_after_cleanup,
            "job_accounting_proves_empty": job_accounting_proves_empty,
            "descendant_pids_before_termination_or_close": descendants_before_close,
            "pid_states_after": states_after,
            "pid_states_unambiguously_dead": unambiguous_dead_states,
            "all_observed_processes_terminated": all_terminated,
        },
        "stdout": {
            **file_identity(stdout_path),
            "total_observed_bytes": stdout_reader.total_bytes,
            "captured_bytes": stdout_reader.captured_bytes,
            "truncated": stdout_reader.truncated,
            "reader_error": stdout_reader.error,
        },
        "stderr": {
            **file_identity(stderr_path),
            "total_observed_bytes": stderr_reader.total_bytes,
            "captured_bytes": stderr_reader.captured_bytes,
            "truncated": stderr_reader.truncated,
            "reader_error": stderr_reader.error,
        },
        }
        completed_cleanup = True
        return result
    finally:
        if not completed_cleanup and process is not None:
            try:
                if process.poll() is None:
                    if job.assigned and os.name == "nt":
                        job.terminate(125)
                    elif os.name != "nt":
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                    process.wait(timeout=TERMINATION_GRACE_SECONDS)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass
            for reader in (stdout_reader, stderr_reader):
                if reader is not None and reader.ident is not None:
                    reader.join(timeout=TERMINATION_GRACE_SECONDS)
        job.close()
