"""Task 07D coordination checks; native runs use complete retained CK3 logs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import shutil
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import unittest
from unittest.mock import patch
import uuid

from ck3chronicle.config import WatcherSettings
from ck3chronicle.pipeline import ingestion, review
from ck3chronicle.pipeline.database_handler import _Handler
from ck3chronicle.pipeline.capture_access import capture_access
from ck3chronicle.pipeline.repository import create_database
from ck3chronicle.pipeline.request_handler import (HandlerClient,
    ENQUEUED, COMPLETED, NOT_COMPLETED)
from ck3chronicle.pipeline.retention import retain_raw_logs
from ck3chronicle.watcher_processing import WatcherProcessing


class HandlerRequirements(unittest.TestCase):
    def setUp(self):
        self.root = Path('.codex-tmp/task07d').resolve() / uuid.uuid4().hex
        self.root.mkdir(parents=True)
        with create_database(self.root) as db:
            self.database = db.path
        self.client = HandlerClient(self.database)
        self.addCleanup(self.client.shutdown)

    def query(self, operation, **arguments):
        return self.client.result(self.client.submit(operation, arguments), 30)

    def test_separate_processes_start_one_designated_host_without_watcher(self):
        code = '''import json,sys
from pathlib import Path
from ck3chronicle.pipeline.request_handler import HandlerClient
c=HandlerClient(Path(sys.argv[1]))
r=c.submit('latest_run')
print(json.dumps(dict(host=c._rpc('hello'),state=c.result(r).status,value=c.result(r).value)))
'''
        def child(_):
            process = subprocess.run([sys.executable, '-B', '-c', code, str(self.database)],
                                     capture_output=True, text=True, timeout=30)
            self.assertEqual(process.returncode, 0, process.stderr)
            return json.loads(process.stdout)
        with ThreadPoolExecutor(max_workers=3) as callers:
            replies = list(callers.map(child, range(3)))
        self.assertEqual(len({r['host']['instance'] for r in replies}), 1)
        self.assertEqual(len({r['host']['worker_id'] for r in replies}), 1)
        self.assertNotEqual(replies[0]['host']['pid'], os.getpid())
        self.assertTrue(all(r['state'] == COMPLETED and r['value'] is None for r in replies))
        self.assertEqual(self.query('list_runs').value, [])
        with self.assertRaises(ValueError):
            self.client.submit('execute', {'sql': 'SELECT 1'})
        # Only references/results in memory: initialization's tables are unchanged.
        with sqlite3.connect(self.database) as connection:
            self.assertFalse(any('request' in r[0] or 'queue' in r[0]
                for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")))

    def test_external_sqlite_lock_waits_and_exception_does_not_poison_later_requests(self):
        self.query('latest_run')
        with sqlite3.connect(self.database) as external:
            external.execute('BEGIN EXCLUSIVE')
            first = self.client.submit('latest_run')
            second = self.client.submit('list_runs')
            self.assertEqual(self.client.wait(first, .3).status, ENQUEUED)
            self.assertEqual(self.client.status(second), ENQUEUED)
            with self.assertRaises(TimeoutError):
                self.client.result(first, .01)
            self.assertEqual(self.client.status(first), ENQUEUED)
            external.rollback()
        self.assertEqual(self.client.result(first, 10).status, COMPLETED)
        self.assertEqual(self.client.result(second, 10).value, [])
        failure = self.query('list_runs', limit=-1)
        self.assertEqual(failure.status, NOT_COMPLETED)
        self.assertEqual(failure.exception_class, 'ValueError')
        self.assertIn('pagination', failure.error)
        self.assertEqual(self.query('latest_run').status, COMPLETED)

    def test_graceful_shutdown_discards_waiting_work_and_releases_database(self):
        self.query('latest_run')
        before = self.client._rpc('hello')['instance']
        with sqlite3.connect(self.database) as external:
            external.execute('BEGIN EXCLUSIVE')
            waiting = self.client.submit('latest_run')
            queued = self.client.submit('list_runs')
            self.assertEqual(self.client.wait(waiting, .2).status, ENQUEUED)
            self.client.shutdown()
            external.rollback()
        self.assertEqual(self.client.status(waiting), NOT_COMPLETED)
        self.assertEqual(self.client.status(queued), NOT_COMPLETED)
        self.assertEqual(self.query('latest_run').status, COMPLETED)
        self.assertNotEqual(before, self.client._rpc('hello')['instance'])
        with self.assertRaises(LookupError):
            self.client.status(waiting)

    def test_unavailable_input_is_an_accepted_noncompletion(self):
        outcome = self.query('ingest', capture_directory=str(self.root / 'missing'))
        self.assertEqual(outcome.status, NOT_COMPLETED)
        self.assertIn('completed', outcome.error)
        self.assertEqual(self.query('latest_run').status, COMPLETED)


class NativeHandlerRequirements(HandlerRequirements):
    # Reuse setup/query without re-running the generic tests in this subclass.
    test_separate_processes_start_one_designated_host_without_watcher = None
    test_external_sqlite_lock_waits_and_exception_does_not_poison_later_requests = None
    test_graceful_shutdown_discards_waiting_work_and_releases_database = None
    test_unavailable_input_is_an_accepted_noncompletion = None

    def setUp(self):
        super().setUp()
        evidence = Path(os.environ.get('CK3_TASK07_EVIDENCE', '.codex-tmp/task07/evidence.json'))
        if not evidence.exists():
            self.skipTest('complete genuine CK3 inputs unavailable')
        self.evidence = json.loads(evidence.read_bytes())
        self.pending = self.root / 'pending'
        self.pending.mkdir()
        self.capture = self.pending / 'capture'
        shutil.copytree(self.evidence['capture_directory'], self.capture)

    def test_watcher_api_cli_share_handler_duplicate_and_restart(self):
        events = []
        processor = WatcherProcessing(self.pending,
            WatcherSettings(self.database, retention_enabled=False), lambda e, f: events.append((e, f)))
        try:
            processor.start()
            # API read is accepted while the watcher submits its startup capture.
            self.assertEqual(self.query('latest_run').status, COMPLETED)
        finally:
            processor.close()
        completed = [f for e, f in events if e == 'ingestion_completed']
        self.assertEqual(len(completed), 1, events)
        run_id = completed[0]['run_id']
        before = self.client._rpc('hello')
        cli = subprocess.run([sys.executable, '-B', '-m', 'ck3chronicle.cli', 'ingest',
            '--database', str(self.database), '--capture-directory', str(self.capture),
            '--package-id', 'missing-package-must-not-load'], capture_output=True, text=True, timeout=30)
        self.assertEqual(cli.returncode, 1, cli.stderr)
        duplicate = json.loads(cli.stdout)
        self.assertEqual(duplicate['status'], NOT_COMPLETED)
        self.assertEqual(duplicate['run_id'], run_id)
        self.assertIn('duplicate', duplicate['warnings'][0])
        self.assertEqual(before, self.client._rpc('hello'))
        # Terminate only this disposable host while it has outstanding work.
        with capture_access(self.capture):
            lost = self.client.submit('ingest', {'capture_directory': self.capture})
            self.assertEqual(self.client.wait(lost, .2).status, ENQUEUED)
            os.kill(before['pid'], signal.SIGTERM)
            self.assertEqual(self.client.wait(lost, 5).status, NOT_COMPLETED)
        repeat = ingestion.ingest(self.database, capture_directory=self.capture,
                                  package_id='missing-package-must-not-load')
        self.assertEqual(repeat.status, NOT_COMPLETED)
        self.assertEqual(repeat.run_id, run_id)
        self.assertNotEqual(before['instance'], self.client._rpc('hello')['instance'])
        self.assertEqual(len(self.query('list_runs').value), 1)
        with self.assertRaises(LookupError):
            self.client.status(lost)

    def test_preparation_does_not_occupy_worker_and_retention_respects_active_input(self):
        # Exercise the actual handler infrastructure with a paused native parser;
        # no second service or alternate runtime ingestion implementation.
        handler = _Handler(self.database)
        handler.ready.wait()
        entered, release = threading.Event(), threading.Event()
        original = ingestion.catalog.load_selected_classifier
        def pause(**arguments):
            classifier = original(**arguments)
            entered.set()
            if not release.wait(20):
                raise RuntimeError('test did not release preparation')
            return classifier
        try:
            with patch.object(ingestion.catalog, 'load_selected_classifier', side_effect=pause):
                ref = handler.submit('ingest', {'capture_directory': self.capture})
                self.assertTrue(entered.wait(15))
                read = handler.submit('latest_run', {})
                self.assertEqual(handler.wait(read.__dict__, 3).status, COMPLETED)
                self.assertEqual(handler.wait(ref.__dict__, 0).status, ENQUEUED)
                stamp = datetime.fromisoformat(json.loads((self.capture / 'capture-metadata.json').read_bytes())['captured_at'])
                untouched = self.pending / 'queued'
                shutil.copytree(self.capture, untouched)
                queued = handler.submit('ingest', {'capture_directory': untouched})
                expiry = retain_raw_logs(self.pending, preview=False, now=stamp + timedelta(days=31))
                self.assertNotIn(self.capture / 'error.log', expiry.removed)
                self.assertIn(untouched / 'error.log', expiry.removed)
                release.set()
                self.assertEqual(handler.wait(ref.__dict__, 60).status, COMPLETED)
                self.assertEqual(handler.wait(queued.__dict__, 30).status, NOT_COMPLETED)
        finally:
            release.set()
            handler.close()

    def test_write_contention_keeps_preparation_and_publication_boundary(self):
        handler = _Handler(self.database)
        handler.ready.wait()
        try:
            with patch.object(ingestion.catalog, 'load_selected_classifier',
                              wraps=ingestion.catalog.load_selected_classifier) as load:
                with sqlite3.connect(self.database) as external:
                    external.execute('BEGIN IMMEDIATE')
                    ref = handler.submit('ingest', {'capture_directory': self.capture})
                    deadline = time.monotonic() + 30
                    staging = self.root / 'review' / self.database.stem / '.staging'
                    while not list(staging.iterdir()) and time.monotonic() < deadline:
                        time.sleep(.02)
                    self.assertTrue(list(staging.iterdir()), 'native preparation did not reach the Run writer')
                    self.assertEqual(handler.wait(ref.__dict__, .3).status, ENQUEUED)
                    external.rollback()
                outcome = handler.wait(ref.__dict__, 60)
                self.assertEqual(outcome.status, COMPLETED, outcome)
                self.assertEqual(load.call_count, 1)
                result = outcome.value
                metadata = handler.database_call('read_review_metadata', {'run_id': result.run_id})
                manifest = json.loads((self.root / metadata['manifest_reference']).read_bytes())
                self.assertEqual(manifest['counts'], result.stored.accounting.counts)
                self.assertEqual(manifest['schema_version'], 3)
                self.assertEqual(len(handler.database_call('list_runs', {})), 1)
        finally:
            handler.close()

    def test_shutdown_allows_executing_run_publication_to_complete(self):
        handler = _Handler(self.database)
        handler.ready.wait()
        publishing, release = threading.Event(), threading.Event()
        original = review.verify_published
        def paused(*args):
            original(*args)
            publishing.set()
            if not release.wait(20):
                raise RuntimeError('test did not release publication')
        shutdown = None
        try:
            with patch.object(review, 'verify_published', side_effect=paused):
                ref = handler.submit('ingest', {'capture_directory': self.capture})
                self.assertTrue(publishing.wait(15))
                queued = handler.submit('latest_run', {})
                shutdown = threading.Thread(target=handler.close)
                shutdown.start()
                self.assertTrue(handler.stopping.wait(2))
                self.assertTrue(shutdown.is_alive())
                with self.assertRaises(RuntimeError):
                    handler.submit('latest_run', {})
                release.set()
                shutdown.join(15)
                self.assertFalse(shutdown.is_alive())
                self.assertEqual(handler.wait(ref.__dict__, 0).status, COMPLETED)
                self.assertEqual(handler.wait(queued.__dict__, 0).status, NOT_COMPLETED)
        finally:
            release.set()
            if shutdown is not None:
                shutdown.join()
            else:
                handler.close()


if __name__ == '__main__':
    unittest.main()
