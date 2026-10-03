"""Dedicated handler executable: python -m ck3chronicle.pipeline.database_handler DB.

One preparation thread and one serial database worker. Only the latter opens
SQLite. The pipe listener is exclusive for the canonical database path.
"""
from collections import OrderedDict
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timezone
from multiprocessing.connection import Listener
from queue import Queue
import os
from pathlib import Path
import sqlite3
import sys
import threading
import time
import uuid

from ..runtime_logging import (configure_runtime_logging, close_runtime_logging,
                               context_fields, event, get_logger, log_context)

from .domain import RunAccounting, ReviewMetadata, RunResult
from .repository import DuplicateRunError, RunWriteError, open_database
from .request_handler import (COMPLETED, ENQUEUED, NOT_COMPLETED, OPERATIONS,
                              RequestRef, RequestResult, _address, _receive, _send)

logger = get_logger('handler')
worker_logger = get_logger('database_worker')
preparation_logger = get_logger('preparation')


def _contention(exc):
    while exc is not None:
        if isinstance(exc, sqlite3.Error):
            if getattr(exc, 'sqlite_errorcode', 0) & 255 in (sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED):
                return True
        exc = exc.__cause__
    return False


def _failed(exc):
    details = {key: str(value) for key in ('capture_directory', 'published_run_id', 'staging_reference')
               if (value := getattr(exc, key, None)) is not None}
    if getattr(exc, 'warnings', ()):
        details['warnings'] = list(exc.warnings)
    return RequestResult(NOT_COMPLETED, error=str(exc), exception_class=type(exc).__name__, details=details)


class _Request:
    def __init__(self, instance, operation):
        self.ref = RequestRef(instance, uuid.uuid4().hex, datetime.now(timezone.utc).isoformat())
        self.operation = operation
        self.started = time.monotonic()
        self.outcome = RequestResult(ENQUEUED)
        self.done = threading.Event()


class _Handler:
    """Infrastructure implementation; never constructed by runtime callers."""
    def __init__(self, database):
        self.database = database
        self.instance = uuid.uuid4().hex
        self.log_fields = dict(database=str(database), handler_instance=self.instance)
        event(logger, 'handler_started', **self.log_fields)
        self.requests = {}
        self.terminals = OrderedDict()
        self.lock = threading.Lock()
        self.stopping = threading.Event()
        self.ready = threading.Event()
        self.open_error = None
        self.queue = Queue()
        self.preparation = ThreadPoolExecutor(max_workers=1, thread_name_prefix='ingest-preparation')
        self.worker = threading.Thread(target=self._database_worker, name='database-worker')
        self.worker.start()

    def _finish(self, request, outcome):
        with self.lock:
            if request.done.is_set():
                return
            request.outcome = outcome
            value = outcome.value
            run_id = value.get('run_id') if isinstance(value, dict) else getattr(value, 'run_id', None)
            fields = dict(self._request_fields(request), status=outcome.status,
                          elapsed_seconds=time.monotonic() - request.started)
            if run_id is not None:
                fields['run_id'] = run_id
            directory = getattr(value, 'capture_directory', None) or (outcome.details or {}).get('capture_directory')
            if directory is not None:
                fields['capture_directory'] = str(directory)
            if outcome.error:
                fields.update(error=outcome.error, exception_class=outcome.exception_class)
            if getattr(value, 'warnings', ()):
                fields['warnings'] = value.warnings
            event(logger, 'request_completed' if outcome.status == COMPLETED else 'request_not_completed',
                  level='ERROR' if outcome.error else 'INFO', **fields)
            self.terminals[request.ref.request_id] = None
            if len(self.terminals) > 256:
                oldest, _ = self.terminals.popitem(last=False)
                del self.requests[oldest]
            # Existing waiters hold the request object independently of lookup.
            request.done.set()

    def _request_fields(self, request):
        return dict(self.log_fields, request_id=request.ref.request_id,
                    enqueued_at=request.ref.enqueued_at, operation=request.operation)

    def _retry(self, callback, *, wait_state=None, **fields):
        owns_wait = wait_state is None
        waiting = [None] if owns_wait else wait_state
        while True:
            try:
                value = callback()
                if owns_wait and waiting[0] is not None:
                    event(worker_logger, 'database_wait_resumed',
                          elapsed_seconds=time.monotonic() - waiting[0], **fields)
                return value
            except Exception as exc:
                if not _contention(exc):
                    raise
                if waiting[0] is None:
                    waiting[0] = time.monotonic()
                    event(worker_logger, 'database_wait_started', **fields)
                if self.stopping.wait(.05):
                    raise

    def _open_database(self, fields, *, wait_state=None, reopening=False):
        storage = self._retry(lambda: open_database(self.database), wait_state=wait_state, **fields)
        storage.connection.execute('PRAGMA busy_timeout=100')
        event(worker_logger, 'database_opened', level='DEBUG' if reopening else 'INFO', **fields)
        return storage

    def _close_database(self, storage, fields, *, reopening=False):
        storage.close()
        event(worker_logger, 'database_closed', level='DEBUG' if reopening else 'INFO', **fields)

    def _database_worker(self):
        storage = None
        try:
            try:
                storage = self._open_database(dict(self.log_fields, operation='open_database'))
                # Short SQLite waits, followed by internal retries of the complete
                # operation. Preparation is retained while the final write waits.
                event(logger, 'handler_ready', **self.log_fields)
            except Exception as exc:
                event(worker_logger, 'database_open_failed', level='ERROR', exc_info=True, **self.log_fields)
                self.open_error = exc
                return
            finally:
                self.ready.set()
            while True:
                item = self.queue.get()
                if item is None:
                    break
                operation, arguments, future, context, queued = item
                fields = dict(context, **self.log_fields, operation=operation)
                started = time.monotonic()
                waiting = [None]
                event(worker_logger, 'database_operation_started',
                      queue_wait_seconds=started - queued, **fields)
                value = None
                try:
                    if self.stopping.is_set():
                        raise RuntimeError('handler shut down before operation completed')
                    if storage is None:
                        storage = self._open_database(fields)
                    while True:
                        try:
                            value = (storage.metadata if operation == 'metadata'
                                     else getattr(storage, operation)(**arguments))
                            break
                        except RunWriteError as exc:
                            # A commit error is not permission to replay. Reopen
                            # and consult accepted hashes before cleanup or retry.
                            if _contention(exc) and waiting[0] is None:
                                waiting[0] = time.monotonic()
                                event(worker_logger, 'database_wait_started', **fields)
                            elif not _contention(exc):
                                event(worker_logger, 'database_write_uncertain', level='WARNING',
                                      exc_info=True, **fields)
                            self._close_database(storage, fields, reopening=True)
                            storage = None
                            storage = self._open_database(fields, wait_state=waiting, reopening=True)
                            existing = self._retry(lambda: storage.find_run_by_log_hash(arguments['log_sha256']), wait_state=waiting, **fields)
                            if existing:
                                if existing['run_id'] != exc.published_run_id:
                                    raise DuplicateRunError(existing['run_id']) from exc
                                metadata = self._retry(lambda: storage.read_review_metadata(existing['run_id']), wait_state=waiting, **fields)
                                metadata.pop('run_id')
                                value = RunResult(existing['run_id'], storage.metadata['database_id'],
                                    existing['log_sha256'], RunAccounting(existing['counters']), ReviewMetadata(**metadata))
                                break
                            if exc.published_run_id:
                                self._retry(lambda: storage.cleanup_unaccepted(exc.published_run_id), wait_state=waiting, **fields)
                            if not _contention(exc) or self.stopping.wait(.05):
                                raise
                        except Exception as exc:
                            if not _contention(exc):
                                raise
                            if waiting[0] is None:
                                waiting[0] = time.monotonic()
                                event(worker_logger, 'database_wait_started', **fields)
                            if self.stopping.wait(.05):
                                raise
                    if waiting[0] is not None:
                        event(worker_logger, 'database_wait_resumed',
                              elapsed_seconds=time.monotonic() - waiting[0], **fields)
                    run_id = value.get('run_id') if isinstance(value, dict) else getattr(value, 'run_id', None)
                    event(worker_logger, 'database_operation_completed',
                          elapsed_seconds=time.monotonic() - started,
                          **dict(fields, **({'run_id': run_id} if run_id is not None else {})))
                    future.set_result(value)
                except Exception as exc:
                    event(worker_logger, 'database_operation_not_completed',
                          level='INFO' if isinstance(exc, DuplicateRunError) else 'ERROR',
                          exc_info=not isinstance(exc, DuplicateRunError), error=str(exc),
                          elapsed_seconds=time.monotonic() - started, **fields)
                    future.set_exception(exc)
                finally:
                    # Never retain prepared raw/classifier objects while idle.
                    del item, arguments, future, value
        finally:
            if storage is not None:
                self._close_database(storage, self.log_fields)

    def database_call(self, operation, arguments):
        future = Future()
        with self.lock:
            if self.stopping.is_set():
                raise RuntimeError('handler shut down before operation completed')
            self.queue.put((operation, arguments, future, context_fields(), time.monotonic()))
        return future.result()

    def _prepare(self, request, arguments):
        from .ingestion import _ingest
        try:
            if self.stopping.is_set():
                raise RuntimeError('handler shut down before preparation')
            with log_context(**self._request_fields(request)):
                event(preparation_logger, 'preparation_started',
                      **{key: str(arguments[key]) for key in ('capture_directory', 'error_log') if arguments.get(key)},
                      queue_wait_seconds=time.monotonic() - request.started)
                value = _ingest(self.database_call, self.stopping, **arguments)
            self._finish(request, RequestResult(value.status, value))
        except Exception as exc:
            event(preparation_logger, 'preparation_not_completed', level='ERROR', exc_info=True,
                  **self._request_fields(request))
            self._finish(request, _failed(exc))

    def submit(self, operation, arguments):
        if operation not in OPERATIONS or not isinstance(arguments, dict):
            raise ValueError('defined operation and arguments object required')
        with self.lock:
            if self.stopping.is_set():
                raise RuntimeError('handler is shutting down')
            request = _Request(self.instance, operation)
            self.requests[request.ref.request_id] = request
            event(logger, 'request_accepted', **self._request_fields(request))
            if operation == 'ingest':
                self.preparation.submit(self._prepare, request, arguments)
            else:
                future = Future()
                def finish(done):
                    try:
                        self._finish(request, RequestResult(COMPLETED, done.result()))
                    except Exception as exc:
                        self._finish(request, _failed(exc))
                future.add_done_callback(finish)
                self.queue.put((operation, arguments, future, self._request_fields(request), time.monotonic()))
            return request.ref

    def wait(self, ref, timeout):
        with self.lock:
            request = self.requests.get(ref['request_id']) if ref['instance'] == self.instance else None
        if request is None:
            raise LookupError('request result is no longer retained by this handler')
        request.done.wait(timeout)
        return request.outcome

    def close(self):
        with self.lock:
            if self.stopping.is_set():
                return
            self.stopping.set()
            event(logger, 'handler_shutdown_started', **self.log_fields)
            self.queue.put(None)
        # The active DB operation finishes its publication/transaction boundary.
        # Queued DB work is rejected; preparation releases its capture lock.
        self.worker.join()
        self.preparation.shutdown(wait=True)
        for request in tuple(self.requests.values()):
            if not request.done.is_set():
                self._finish(request, RequestResult(NOT_COMPLETED, error='handler shut down'))
        event(logger, 'handler_stopped', **self.log_fields)


def serve(database):
    # AF_PIPE uses FILE_FLAG_FIRST_PIPE_INSTANCE. Bind BEFORE opening SQLite.
    # Even a direct second module launch cannot open a second runtime connection.
    with Listener(_address(database), family='AF_PIPE') as listener:
        # Bind before configuring a rotating file: a direct second launch must
        # never share the live owner's output, even during bootstrap.
        output = configure_runtime_logging(database=database)
        try:
            _serve_connected(database, listener)
        except Exception:
            event(logger, 'handler_failed', level='ERROR', exc_info=True, database=str(database))
            raise SystemExit(1)
        finally:
            close_runtime_logging(output)


def _serve_connected(database, listener):
    handler = _Handler(Path(database).resolve())
    exit_requested = threading.Event()
    shutdown_lock = threading.Lock()

    def handle(connection):
        shutdown_completed = False
        with connection:
            try:
                message = _receive(connection)
                command = message['command']
                handler.ready.wait()
                if handler.open_error is not None:
                    raise handler.open_error
                if command == 'hello':
                    if handler.stopping.is_set():
                        raise RuntimeError('handler is shutting down')
                    reply = dict(instance=handler.instance, pid=os.getpid(),
                                 worker_id=handler.worker.ident)
                elif command == 'submit':
                    reply = handler.submit(message['operation'], message['arguments'])
                elif command == 'wait':
                    try:
                        reply = handler.wait(message['ref'], message['timeout'])
                    except LookupError as exc:
                        reply = dict(result_unavailable=str(exc))
                elif command == 'shutdown':
                    with shutdown_lock:
                        handler.close()
                    shutdown_completed = True
                    reply = {}
                else:
                    raise ValueError('unsupported handler command')
                _send(connection, reply)
            except (EOFError, BrokenPipeError):
                pass  # client departure does not cancel accepted work
            except Exception as exc:
                try:
                    _send(connection, dict(admission_error=f'{type(exc).__name__}: {exc}'))
                except (OSError, EOFError):
                    pass
            finally:
                if handler.open_error is not None or shutdown_completed:
                    exit_requested.set()

    def accept():
        while not exit_requested.is_set():
            try:
                connection = listener.accept()
            except OSError:
                return
            threading.Thread(target=handle, args=(connection,), daemon=True).start()

    threading.Thread(target=accept, name='database-pipe', daemon=True).start()
    try:
        exit_requested.wait()
    finally:
        with shutdown_lock:
            if not handler.stopping.is_set():
                handler.close()


if __name__ == '__main__':
    # Pre-configuration exceptions reach the launcher's bootstrap stderr file.
    serve(Path(sys.argv[1]).resolve())
