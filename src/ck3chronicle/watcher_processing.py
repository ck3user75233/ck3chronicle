"""Watcher calls to the pipeline, kept off the CK3 lifecycle polling thread.

The local dispatcher only admits requests and runs daily retention. Ingestion
preparation and database work belong to the dedicated shared handler.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pathlib import Path
import threading
import time

from .config import WatcherSettings
from .pipeline.ingestion import ingest_result
from .pipeline.request_handler import ENQUEUED, COMPLETED, HandlerClient
from .pipeline.retention import RetentionConfig, retain_raw_logs


class WatcherProcessing:
    """Nonblocking handler client, outcome delivery and daily raw maintenance."""

    def __init__(self, pending_root: Path, settings: WatcherSettings, emit, *, monotonic=time.monotonic):
        self.pending_root = pending_root
        self.settings = settings
        self.emit = emit
        self.clock = monotonic
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='watcher-submit')
        self._scheduled = set()
        self._lock = threading.Lock()
        self._retry = set()
        self.client = HandlerClient(settings.database)
        self._pending = {}
        self._closing = threading.Event()
        self._monitor = threading.Thread(target=self._monitor_results, name='watcher-results')
        self._monitor.start()
        self._maintenance = None
        self._next_maintenance = self.clock() + settings.maintenance_hours * 3600

    def _dispatch(self, operation, *args):
        def run():
            try:
                operation(*args)
            except Exception as exc:
                self.emit('watcher_processing_failed', {
                    'operation': operation.__name__, 'error_type': type(exc).__name__,
                    'error': str(exc),
                })
        return self.executor.submit(run)

    def start(self):
        self.emit('watcher_processing_configured', {
            'database': str(self.settings.database),
            'ingest_enabled': self.settings.ingest_enabled,
            'retention_enabled': self.settings.retention_enabled,
            'maintenance_hours': self.settings.maintenance_hours,
            'retention_days': self.settings.retention_days,
        })
        if self.settings.ingest_enabled:
            self._dispatch(self._startup)

    def _startup(self):
        if not self.pending_root.exists():
            return
        # Watcher capture names start with UTC capture time. Legacy inputs are
        # still handed to ingest for validation; no file time is invented.
        for directory in sorted(self.pending_root.iterdir()):
            try:
                if (directory.name.startswith('.') or directory.is_symlink()
                        or not directory.is_dir() or not (directory / 'error.log').is_file()):
                    continue
                self._ingest(directory, 'startup')
            except OSError as exc:
                self.emit('ingestion_input_unavailable', {'capture_directory': str(directory), 'error': str(exc)})

    def on_capture(self, result, trigger):
        """Called only with a published PendingCapture, never a staging path."""
        if not self.settings.ingest_enabled:
            return
        directory = result.dest_dir
        if directory.name.startswith('.'):
            raise ValueError('ingestion submission requires a published capture')
        with self._lock:
            if directory in self._scheduled:
                return
            self._scheduled.add(directory)
        self.emit('ingestion_submitted', {'capture_directory': str(directory), 'trigger': trigger})
        self._dispatch(self._submitted_ingest, directory, trigger)

    def _submitted_ingest(self, directory, trigger):
        self._ingest(directory, trigger)

    def _ingest(self, directory, trigger):
        context = {'capture_directory': str(directory), 'trigger': trigger,
                   'database': str(self.settings.database)}
        self.emit('ingestion_requested', context)
        try:
            ref = self.client.submit('ingest', {'capture_directory': directory})
        except Exception as exc:
            with self._lock:
                self._retry.add(directory)
                self._scheduled.discard(directory)
            self.emit('ingestion_failed', {**context, 'error_type': type(exc).__name__, 'error': str(exc)})
            return
        context.update(request_id=ref.request_id, handler_instance=ref.instance,
                       enqueued_at=ref.enqueued_at, operation='ingest')
        self.emit('ingestion_accepted', context)
        with self._lock:
            self._pending[ref] = context
            self._retry.discard(directory)

    def _monitor_results(self):
        while True:
            with self._lock:
                pending = tuple(self._pending.items())
            if self._closing.is_set() and not pending:
                return
            for ref, context in pending:
                try:
                    try:
                        outcome = self.client.wait(ref, timeout=0)
                    except LookupError as exc:
                        directory = Path(context['capture_directory'])
                        with self._lock:
                            self._pending.pop(ref, None)
                            self._scheduled.discard(directory)
                            self._retry.discard(directory)
                        self.emit('ingestion_outcome_unavailable', {
                            **context, 'message': str(exc),
                            'request_id': ref.request_id, 'handler_instance': ref.instance,
                        })
                        continue
                    if outcome.status == ENQUEUED:
                        continue
                    result = ingest_result(outcome)
                    directory = Path(context['capture_directory'])
                    with self._lock:
                        self._pending.pop(ref)
                        self._scheduled.discard(directory)
                        if result.error:
                            self._retry.add(directory)
                        else:
                            self._retry.discard(directory)
                    for warning in result.warnings:
                        self.emit('ingestion_warning', {**context, 'message': warning, 'run_id': result.run_id})
                    self.emit('ingestion_completed' if result.status == COMPLETED else 'ingestion_not_completed', {
                        **context, 'status': result.status, 'run_id': result.run_id,
                        'error_log_sha256': result.log_sha256, 'error': result.error,
                        'exception_class': result.exception_class,
                    })
                except Exception as exc:
                    with self._lock:
                        self._pending.pop(ref, None)
                        self._scheduled.discard(Path(context['capture_directory']))
                        self._retry.add(Path(context['capture_directory']))
                    self.emit('watcher_processing_failed', {**context, 'error': str(exc)})
            time.sleep(.1)

    def tick(self):
        """Nonblocking due check, also called when CK3 is idle."""
        if self.clock() < self._next_maintenance:
            return
        if self._maintenance is not None and not self._maintenance.done():
            return
        self._next_maintenance = self.clock() + self.settings.maintenance_hours * 3600
        self._maintenance = self._dispatch(self._maintain)

    def _maintain(self):
        if self.settings.retention_enabled and self.pending_root.exists():
            try:
                result = retain_raw_logs(
                    self.pending_root,
                    config=RetentionConfig(max_age=timedelta(days=self.settings.retention_days)),
                    preview=False,
                )
                self.emit('retention_completed', {
                    'eligible': [str(path) for path in result.eligible],
                    'removed': [str(path) for path in result.removed],
                    'skipped_count': len(result.skipped),
                    'problems': [
                        {'path': str(item.path), 'reason': item.reason}
                        for item in (*result.skipped, *result.failures)
                        if item.reason not in ('absent', 'not expired')
                    ],
                })
            except Exception as exc:
                self.emit('retention_failed', {'error_type': type(exc).__name__, 'error': str(exc)})
        if self.settings.ingest_enabled:
            with self._lock:
                retry = tuple(self._retry)
            for directory in retry:
                if (directory / 'error.log').is_file():
                    self._ingest(directory, 'maintenance')
                else:
                    with self._lock:
                        self._retry.discard(directory)
                    self.emit('ingestion_input_unavailable', {
                        'capture_directory': str(directory), 'error': 'retained error.log is no longer present',
                    })

    def close(self):
        # Keep the journal and runtime lease alive until submitted calls finish.
        self.executor.shutdown(wait=True)
        self._closing.set()
        self._monitor.join()
