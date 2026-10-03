"""Watcher caller verification; native processing uses genuine retained inputs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack, redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import shutil
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from ck3chronicle import cli, config, harvester, watcher, watcher_processing
from ck3chronicle.config import WatcherSettings
from ck3chronicle.pipeline.ingestion import ingest
from ck3chronicle.pipeline.request_handler import HandlerClient, RequestResult, RequestRef
from ck3chronicle.pipeline.repository import create_database, open_database_readonly
from ck3chronicle.pipeline.retention import RetentionResult
from ck3chronicle.watcher_processing import WatcherProcessing


class WatcherCallerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.pending = self.root / 'pending'
        self.pending.mkdir()
        self.events = []
        self.emit = lambda event, fields: self.events.append((event, fields))
        self.settings = WatcherSettings(self.root / 'storage', retention_enabled=False)

    def capture(self, name='completed'):
        directory = self.pending / name
        directory.mkdir()
        (directory / 'error.log').write_bytes(b'capture-dispatch-test')
        return SimpleNamespace(dest_dir=directory)

    def success(self):
        return RequestResult('COMPLETED', dict(status='COMPLETED', run_id='accepted', log_sha256='digest',
            warnings=[], capture_directory=None, stored=None))

    def test_ingestion_worker_does_not_block_lifecycle_polls(self):
        entered, release = threading.Event(), threading.Event()
        result = self.capture()
        def blocking_wait(ref, timeout):
            entered.set()
            self.assertTrue(release.wait(5))
            return self.success()
        processor = WatcherProcessing(self.pending, self.settings, self.emit)
        process = watcher.ProcessIdentity(1, 'ck3.exe', 2)
        observations = iter([None, process, None, None])
        polls = 0
        def probe():
            nonlocal polls
            polls += 1
            return next(observations)
        with patch.object(processor.client, 'submit', return_value=RequestRef('handler', 'ref', 'now')), patch.object(processor.client, 'wait', side_effect=blocking_wait):
            try:
                watcher.watch_sessions(logs_root=self.root, capture=lambda *args: result,
                    process_probe=probe, on_capture=processor.on_capture,
                    stop_requested=lambda: polls == 4, sleep=lambda _: None)
                self.assertEqual(polls, 4)
                self.assertTrue(entered.wait(5))
                self.assertNotIn('ingestion_completed', [e for e, _ in self.events])
            finally:
                release.set()
                processor.close()
        self.assertIn('ingestion_completed', [e for e, _ in self.events])

    def test_startup_submits_completed_inputs_and_excludes_staging(self):
        self.capture('20260928-completed')
        self.capture('.copying-unfinished')
        (self.pending / 'expired').mkdir()
        processor = WatcherProcessing(self.pending, self.settings, self.emit)
        with patch.object(processor.client, 'submit', return_value=RequestRef('handler', 'ref', 'now')) as call, patch.object(processor.client, 'wait', return_value=self.success()):
            processor.start()
            processor.close()
        self.assertEqual(call.call_count, 1)
        self.assertEqual(call.call_args.args[1]['capture_directory'].name, '20260928-completed')

    def test_ingestion_failure_does_not_stop_later_capture(self):
        first, second = self.capture('first'), self.capture('second')
        processor = WatcherProcessing(self.pending, self.settings, self.emit)
        with patch.object(processor.client, 'submit', side_effect=[RequestRef('handler', 'one', 'now'), RequestRef('handler', 'two', 'now')]), patch.object(processor.client, 'wait',
                side_effect=[RequestResult('NOT_COMPLETED', error='invalid input', exception_class='ValueError'), self.success()]):
            processor.on_capture(first, 'process_exit')
            processor.on_capture(second, 'process_exit')
            processor.close()
        self.assertIn('ingestion_not_completed', [e for e, _ in self.events])
        self.assertIn('ingestion_completed', [e for e, _ in self.events])
        outcome = next(fields for event, fields in self.events if event == 'ingestion_not_completed')
        self.assertEqual(outcome['exception_class'], 'ValueError')
        self.assertNotIn('error_type', outcome)

    def test_enqueued_work_does_not_block_admission_or_daily_retention(self):
        first, second = self.capture('first'), self.capture('second')
        processor = WatcherProcessing(self.pending, self.settings, self.emit)
        release = threading.Event()
        def outcome(ref, timeout):
            return self.success() if release.is_set() else RequestResult('ENQUEUED')
        with patch.object(processor.client, 'submit', side_effect=[RequestRef('handler', 'one', 'now'), RequestRef('handler', 'two', 'now')]) as submit, patch.object(processor.client, 'wait', side_effect=outcome):
            try:
                processor.on_capture(first, 'process_exit')
                processor.on_capture(second, 'process_exit')
                processor.executor.submit(lambda: None).result(5)
                self.assertEqual(submit.call_count, 2)
                self.assertNotIn('ingestion_completed', [e for e, _ in self.events])
            finally:
                release.set()
                processor.close()

    def test_retention_first_runs_after_a_day_without_captures(self):
        now = [0]
        settings = WatcherSettings(self.root, ingest_enabled=False)
        with patch.object(watcher_processing, 'retain_raw_logs', return_value=RetentionResult(False, (), (), (), ())) as retain:
            processor = WatcherProcessing(self.pending, settings, self.emit, monotonic=lambda: now[0])
            processor.start()
            now[0] = 3600
            processor.tick()
            retain.assert_not_called()
            now[0] = 86400
            processor.tick()
            processor.close()
            retain.assert_called_once()
            self.assertFalse(retain.call_args.kwargs['preview'])
            self.assertEqual(retain.call_args.kwargs['config'].max_age.days, 30)

    def test_journal_serializes_worker_and_polling_events(self):
        with watcher.EventJournal(self.root) as journal:
            with ThreadPoolExecutor(max_workers=2) as pool:
                list(pool.map(lambda n: journal.emit('verification', {'ordinal': n}), range(100)))
            path = journal.path
        lines = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
        self.assertEqual(sorted(item['ordinal'] for item in lines), list(range(100)))

    def test_configuration_has_operational_defaults(self):
        with patch.object(config, 'load_config', return_value={'watcher': {'database': str(self.root / 'database.sqlite3')}}):
            settings = config.watcher_settings()
        self.assertTrue(settings.ingest_enabled)
        self.assertTrue(settings.retention_enabled)
        self.assertEqual(settings.maintenance_hours, 24)
        self.assertEqual(settings.retention_days, 30)


class NativeWatcherIngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        evidence = Path('.codex-tmp/task07/evidence.json')
        if not evidence.is_file():
            raise unittest.SkipTest('genuine Task 07 retained inputs unavailable')
        cls.evidence = json.loads(evidence.read_text(encoding='utf-8'))
        cls.source = Path(cls.evidence['capture_directory'])
        if not (cls.source / 'error.log').is_file():
            raise unittest.SkipTest('genuine retained error log unavailable')

    def run_live_path(self, root, database, *, missing_debug=False):
        logs = root / 'logs'
        logs.mkdir()
        source = Path(self.evidence['manual_error_log']) if missing_debug else self.source / 'error.log'
        shutil.copy2(source, logs / 'error.log')
        if not missing_debug:
            shutil.copy2(self.source / 'debug.log', logs / 'debug.log')
        runtime = root / 'runtime'
        crashes = root / 'crashes'
        crashes.mkdir()
        args = argparse.Namespace(logs=str(logs), once=False, process_name='ck3.exe', poll_seconds=.001, heartbeat_seconds=30)
        process = watcher.ProcessIdentity(999, 'ck3.exe', 123)
        observations = iter([None, process, None, None, None])
        real_watch = watcher.watch_sessions
        polls = 0
        def bounded(**kwargs):
            def sleep(_):
                nonlocal polls
                polls += 1
            return real_watch(**kwargs, sleep=sleep, stop_requested=lambda: polls >= 3)
        stdout, stderr = io.StringIO(), io.StringIO()
        with ExitStack() as stack:
            stack.enter_context(patch.object(config, 'ROOT_CK3CHRONICLE', runtime))
            stack.enter_context(patch.object(config, 'ROOT_CRASHES', crashes))
            stack.enter_context(patch.object(config, 'watcher_settings', return_value=WatcherSettings(database, retention_enabled=False)))
            stack.enter_context(patch.object(watcher, 'find_process', side_effect=lambda _: next(observations)))
            stack.enter_context(patch.object(watcher, 'watch_sessions', side_effect=bounded))
            stack.enter_context(redirect_stdout(stdout))
            stack.enter_context(redirect_stderr(stderr))
            code = cli.cmd_watch(args)
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue(), '')
        self.assertEqual(stderr.getvalue(), '')
        events = [json.loads(line) for p in (runtime / 'watch').glob('events-*.jsonl') for line in p.read_text(encoding='utf-8').splitlines()]
        completed = next(e for e in events if e['event'] == 'ingestion_completed')
        names = [e['event'] for e in events]
        self.assertLess(names.index('pending_capture_published'), names.index('ingestion_submitted'))
        self.assertLess(names.index('capture_completed'), names.index('ingestion_submitted'))
        self.assertNotIn('ingestion_failed', names)
        directory = Path(completed['capture_directory'])
        self.assertFalse(directory.name.startswith('.'))
        if missing_debug:
            self.assertIn('debug_capture_failed', names)
            self.assertFalse((directory / 'playset.json').exists())
        return completed['run_id'], directory

    def test_published_pair_and_error_only_capture_reach_real_sql(self):
        with tempfile.TemporaryDirectory() as temporary, ExitStack() as cleanup:
            root = Path(temporary)
            database = root / 'storage'
            with create_database(database) as initialized:
                database = initialized.path
            cleanup.callback(HandlerClient(database).shutdown)
            for number, missing_debug in enumerate((False, True)):
                fixture = root / str(number)
                fixture.mkdir()
                run_id, directory = self.run_live_path(fixture, database, missing_debug=missing_debug)
                with open_database_readonly(database) as storage:
                    self.assertIsNotNone(storage.get_run(run_id))
                    self.assertEqual(storage.read_playset(run_id)['playset_captured'], not missing_debug)
                    self.assertTrue(storage.read_diagnostics(run_id))
                    reference = storage.read_review_metadata(run_id)['manifest_reference']
                    manifest = json.loads(storage.resolve_review_reference(reference).read_text(encoding='utf-8'))
                    self.assertEqual(manifest['playset'], storage.read_playset(run_id))
                duplicate = ingest(database, capture_directory=directory)
                self.assertEqual(duplicate.status, 'NOT_COMPLETED')
                self.assertEqual(duplicate.run_id, run_id)

    def test_bad_playset_does_not_reject_genuine_error_log(self):
        with tempfile.TemporaryDirectory() as temporary, ExitStack() as cleanup:
            root = Path(temporary)
            capture = root / 'capture'
            shutil.copytree(self.source, capture)
            # Only receiver metadata is deliberately malformed; native log bytes
            # are complete and untouched.
            (capture / 'playset.json').write_text('{broken', encoding='utf-8')
            with create_database(root / 'storage') as initialized:
                database = initialized.path
            cleanup.callback(HandlerClient(database).shutdown)
            result = ingest(database, capture_directory=capture)
            self.assertEqual(result.status, 'COMPLETED')
            self.assertTrue(result.warnings)
            self.assertEqual((capture / 'playset.json').read_text(encoding='utf-8'), '{broken')
            with open_database_readonly(database) as storage:
                self.assertFalse(storage.read_playset(result.run_id)['playset_captured'])


if __name__ == '__main__':
    unittest.main()
