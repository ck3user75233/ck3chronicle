"""Clients of the designated local database handler (Windows named pipe).

Only JSON data crosses the pipe. Request references and results live in memory;
connecting to a replacement handler never resubmits an earlier request.
"""
from contextlib import contextmanager
from dataclasses import asdict, dataclass, is_dataclass
import hashlib
import json
from multiprocessing.connection import Client
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

from ..runtime_logging import open_bootstrap_log, bootstrap_log_path

ENQUEUED = 'ENQUEUED'
COMPLETED = 'COMPLETED'
NOT_COMPLETED = 'NOT_COMPLETED'

# Complete, defined repository operations. No SQL, connection or cursor API.
READ_OPERATIONS = frozenset({
    'metadata', 'find_run_by_log_hash', 'get_run', 'list_runs', 'latest_run',
    'read_diagnostics', 'read_playset', 'read_review_metadata',
    'resolve_review_reference',
})
OPERATIONS = READ_OPERATIONS | {'ingest'}


@dataclass(frozen=True)
class RequestRef:
    instance: str
    request_id: str
    enqueued_at: str


@dataclass(frozen=True)
class RequestResult:
    status: str
    value: object = None
    error: str | None = None
    exception_class: str | None = None
    details: dict | None = None


def _json_default(value):
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value):
        return asdict(value)
    raise TypeError(f'not JSON request data: {type(value).__name__}')


def _send(connection, value):
    connection.send_bytes(json.dumps(value, default=_json_default).encode('utf-8'))


def _receive(connection):
    return json.loads(connection.recv_bytes())


def _identity(database):
    if os.name != 'nt':
        raise OSError('the shared database handler requires Windows named pipes')
    path = os.path.normcase(str(Path(database).resolve()))
    return hashlib.sha256(path.encode('utf-8')).hexdigest()


def _address(database):
    return r'\\.\pipe\ck3chronicle-database-' + _identity(database)


@contextmanager
def _startup_lock(database):
    """Serialize launch checks only; callers never host the handler or SQLite."""
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
    kernel.CreateMutexW.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.ReleaseMutex.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.CreateMutexW(None, False, 'Local\\ck3chronicle-start-' + _identity(database))
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        acquired = kernel.WaitForSingleObject(handle, 0xFFFFFFFF)
        if acquired not in (0, 0x80):  # acquired or abandoned by an exited launcher
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            yield
        finally:
            kernel.ReleaseMutex(handle)
    finally:
        kernel.CloseHandle(handle)


class HandlerClient:
    """A lightweight client, never an owner of database resources.

    submit starts the dedicated host if absent and returns after acceptance.
    wait returns a RequestResult; result raises TimeoutError only for a caller
    timeout, otherwise returns the same terminal envelope, including failures.
    Lookup of an unavailable/evicted result raises LookupError, not a request state.
    """
    def __init__(self, database: Path):
        self.database = Path(database).resolve()
        self.address = _address(self.database)

    def _rpc(self, command, **arguments):
        with Client(self.address, family='AF_PIPE') as connection:
            _send(connection, dict(command=command, **arguments))
            reply = _receive(connection)
        if 'admission_error' in reply:
            raise RuntimeError(reply['admission_error'])
        if 'result_unavailable' in reply:
            raise LookupError(reply['result_unavailable'])
        return reply

    def _ensure_started(self):
        with _startup_lock(self.database):
            try:
                return self._rpc('hello')
            except (OSError, EOFError):
                pass
            # The same module hosts every instance. The launching caller does no
            # preparation or database work and is free to exit after admission.
            with open_bootstrap_log(self.database) as bootstrap:
                process = subprocess.Popen(
                    [sys.executable, '-B', '-m', 'ck3chronicle.pipeline.database_handler',
                     str(self.database)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=bootstrap, creationflags=subprocess.CREATE_NO_WINDOW)
            # Reap the launcher handle if this client remains alive. This does
            # not tie the dedicated process lifetime to the launching client.
            threading.Thread(target=process.wait, name='handler-launcher', daemon=True).start()
            deadline = time.monotonic() + 30
            while True:
                try:
                    return self._rpc('hello')
                except (OSError, EOFError):
                    if process.poll() is not None:
                        raise RuntimeError(f'database handler could not start for {self.database}; '
                                           f'see {bootstrap_log_path(self.database)}')
                    if time.monotonic() >= deadline:
                        raise TimeoutError('database handler startup did not respond')
                    time.sleep(.05)

    def submit(self, operation: str, arguments: dict | None = None) -> RequestRef:
        if operation not in OPERATIONS:
            raise ValueError(f'unsupported database operation: {operation}')
        arguments = dict(arguments or {})
        if operation == 'ingest':
            for key in ('capture_directory', 'error_log', 'captures_root'):
                if arguments.get(key) is not None:
                    arguments[key] = str(Path(arguments[key]).absolute())
        self._ensure_started()
        return RequestRef(**self._rpc('submit', operation=operation, arguments=arguments))

    def wait(self, ref: RequestRef, timeout: float | None = None) -> RequestResult:
        if timeout is not None and timeout < 0:
            raise ValueError('timeout must be nonnegative')
        try:
            return RequestResult(**self._rpc('wait', ref=ref, timeout=timeout))
        except (OSError, EOFError) as exc:
            return RequestResult(NOT_COMPLETED, error=f'handler terminated or unavailable: {exc}',
                                 exception_class=type(exc).__name__)

    def status(self, ref: RequestRef) -> str:
        return self.wait(ref, timeout=0).status

    def result(self, ref: RequestRef, timeout: float | None = None) -> RequestResult:
        outcome = self.wait(ref, timeout)
        if outcome.status == ENQUEUED:
            raise TimeoutError('request remains ENQUEUED')
        return outcome

    def shutdown(self):
        """Explicit infrastructure shutdown; closing an ordinary client does not stop it."""
        with _startup_lock(self.database):
            try:
                self._rpc('shutdown')
            except (OSError, EOFError):
                return
            # Wait for the listener to close before another caller may launch.
            while True:
                try:
                    self._rpc('hello')
                except (OSError, EOFError):
                    return
                except RuntimeError:
                    pass
                time.sleep(.02)
