"""Bounded 07D result retention and its API/caller behavior; no CK3 fixtures."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack, redirect_stdout
from dataclasses import asdict
import io
import json
from pathlib import Path
import sqlite3
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import uuid

from ck3chronicle import cli
from ck3chronicle.config import WatcherSettings
from ck3chronicle.pipeline.capture_access import capture_access
from ck3chronicle.pipeline.database_handler import _Handler
from ck3chronicle.pipeline.ingestion import ingest_result
from ck3chronicle.pipeline.repository import create_database
from ck3chronicle.pipeline.request_handler import (
    HandlerClient, RequestRef, RequestResult, ENQUEUED, COMPLETED, NOT_COMPLETED,
)
from ck3chronicle.watcher_processing import WatcherProcessing


class HandlerHardeningRequirements(unittest.TestCase):
    def setUp(self):
        self.root = Path('.codex-tmp/task07d-hardening').resolve() / uuid.uuid4().hex
        self.root.mkdir(parents=True)
        with create_database(self.root) as db:
            self.database = db.path
        self.client = HandlerClient(self.database)
        self.addCleanup(self.client.shutdown)

    def local_handler(self):
        handler = _Handler(self.database)
        self.addCleanup(handler.close)
        self.assertTrue(handler.ready.wait(10))
        self.assertIsNone(handler.open_error)
        return handler

    def test_only_terminal_requests_count_and_eviction_uses_completion_order(self):
        handler = self.local_handler()
        capture = self.root / 'capture'
        capture.mkdir()
        with capture_access(capture):
            # These are the earliest accepted requests, but cannot yet finish.
            unfinished = [handler.submit('ingest', {'capture_directory': capture}) for _ in range(2)]
            self.assertEqual(handler.wait(asdict(unfinished[0]), .1).status, ENQUEUED)
            terminals = []
            for number in range(256):
                operation, arguments = ('list_runs', {'limit': -1}) if number == 0 else ('latest_run', {})
                ref = handler.submit(operation, arguments)
                outcome = handler.wait(asdict(ref), 5)
                self.assertEqual(outcome.status, NOT_COMPLETED if number == 0 else COMPLETED)
                terminals.append(ref)
            self.assertEqual(len(handler.terminals), 256)
            self.assertEqual(len(handler.requests), 258)
            # Reading an older result does not promote it in completion order.
            self.assertEqual(handler.wait(asdict(terminals[0]), 0).status, NOT_COMPLETED)
            newest = handler.submit('latest_run', {})
            self.assertEqual(handler.wait(asdict(newest), 5).status, COMPLETED)
            with self.assertRaisesRegex(LookupError, 'no longer retained'):
                handler.wait(asdict(terminals[0]), 0)
            self.assertEqual(handler.wait(asdict(terminals[1]), 0).status, COMPLETED)
            self.assertEqual(len(handler.terminals), 256)
            self.assertEqual(len(handler.requests), 258)
            for ref in unfinished:
                self.assertEqual(handler.wait(asdict(ref), 0).status, ENQUEUED)
        # No log was fabricated: after lock release, ordinary missing-input
        # failures finish both requests and also enter the terminal bound.
        for ref in unfinished:
            self.assertEqual(handler.wait(asdict(ref), 5).status, NOT_COMPLETED)
        self.assertEqual(len(handler.requests), 256)

    def test_waiter_holds_result_after_lookup_cache_eviction(self):
        handler = self.local_handler()
        entered, deliver = threading.Event(), threading.Event()
        with sqlite3.connect(self.database) as external, ExitStack() as cleanup:
            external.execute('BEGIN EXCLUSIVE')
            ref = handler.submit('latest_run', {})
            request = handler.requests[ref.request_id]
            original_wait = request.done.wait
            def delayed_return(timeout):
                entered.set()
                completed = original_wait(timeout)
                if not deliver.wait(15):
                    raise TimeoutError('test did not allow delivery')
                return completed
            pool = cleanup.enter_context(ThreadPoolExecutor(max_workers=1))
            cleanup.callback(deliver.set)
            cleanup.enter_context(patch.object(request.done, 'wait', side_effect=delayed_return))
            waiter = pool.submit(handler.wait, asdict(ref), 10)
            self.assertTrue(entered.wait(5))
            external.rollback()
            for _ in range(256):
                newer = handler.submit('latest_run', {})
                self.assertEqual(handler.wait(asdict(newer), 5).status, COMPLETED)
            with self.assertRaises(LookupError):
                handler.wait(asdict(ref), 0)
            deliver.set()
            result = waiter.result(5)
            self.assertEqual(result.status, COMPLETED)
            self.assertIsNone(result.value)

    def test_transport_maps_eviction_to_lookuperror_for_all_lookup_methods(self):
        oldest = self.client.submit('latest_run')
        self.assertEqual(self.client.result(oldest, 10).status, COMPLETED)
        for _ in range(256):
            ref = self.client.submit('latest_run')
            self.assertEqual(self.client.result(ref, 5).status, COMPLETED)
        for method in (self.client.status, self.client.wait, self.client.result):
            with self.subTest(method=method.__name__):
                with self.assertRaisesRegex(LookupError, 'no longer retained'):
                    method(oldest)
        self.assertEqual(self.client.status(ref), COMPLETED)

    def test_cleanup_is_rejected_at_client_and_server_admission(self):
        with self.assertRaises(ValueError):
            self.client.submit('cleanup_unaccepted', {'run_id': '20260930-ABC123'})
        self.client.result(self.client.submit('latest_run'), 10)
        # A caller bypassing local validation is still rejected by the host.
        with self.assertRaisesRegex(RuntimeError, 'defined operation'):
            self.client._rpc('submit', operation='cleanup_unaccepted', arguments={'run_id': '20260930-ABC123'})
        self.assertEqual(self.client.result(self.client.submit('latest_run'), 5).status, COMPLETED)

    def test_exception_class_survives_transport_ingestion_and_cli(self):
        outcome = self.client.result(self.client.submit('ingest', {}), 10)
        self.assertEqual(outcome.status, NOT_COMPLETED)
        self.assertEqual(outcome.exception_class, 'IngestInputError')
        self.assertNotIn('error_type', asdict(outcome))
        result = ingest_result(outcome)
        self.assertEqual(result.exception_class, 'IngestInputError')
        self.assertNotIn('error_type', asdict(result))
        output = io.StringIO()
        with redirect_stdout(output):
            code = cli.cmd_ingest(SimpleNamespace(database=self.database, capture_directory=None,
                                                  error_log=None, captures_root=None, package_id=None))
        self.assertEqual(code, 1)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload['exception_class'], 'IngestInputError')
        self.assertNotIn('error_type', payload)
        self.assertIn('error', payload)
        self.assertIn('details', payload)

    def test_watcher_reports_unavailable_without_outcome_or_retry(self):
        pending = self.root / 'pending'
        pending.mkdir()
        directory = pending / 'capture'
        directory.mkdir()
        events = []
        ref = RequestRef('test-instance', 'test-request', '2026-09-30T00:00:00+00:00')
        processor = WatcherProcessing(pending, WatcherSettings(self.database, retention_enabled=False),
                                      lambda event, fields: events.append((event, fields)))
        with patch.object(processor.client, 'submit', return_value=ref) as submit, patch.object(
                processor.client, 'wait', side_effect=LookupError('request result is no longer retained by this handler')):
            try:
                processor.on_capture(SimpleNamespace(dest_dir=directory), 'process_exit')
            finally:
                processor.close()
            self.assertFalse(processor._pending)
            self.assertNotIn(directory, processor._scheduled)
            self.assertNotIn(directory, processor._retry)
            processor._maintain()
            self.assertEqual(submit.call_count, 1)
        outcomes = [(name, fields) for name, fields in events if name == 'ingestion_outcome_unavailable']
        self.assertEqual(len(outcomes), 1, events)
        self.assertNotIn('status', outcomes[0][1])
        self.assertEqual(outcomes[0][1]['request_id'], ref.request_id)
        self.assertFalse({'ingestion_completed', 'ingestion_not_completed', 'ingestion_failed',
                          'watcher_processing_failed'} & {name for name, _ in events})


if __name__ == '__main__':
    unittest.main()
