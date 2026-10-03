"""Source-mtime provenance using genuine retained logs and disposable storage.

CK3_TASK07_EVIDENCE supplies capture_directory (a genuine log pair/playset) and
output_root. Retained sources are read-only; altered timestamps use fresh copies.
"""
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch
import uuid

from ck3chronicle import harvester
from ck3chronicle.pipeline.repository import create_database, open_database_readonly
from ck3chronicle.pipeline.request_handler import HandlerClient
from ck3chronicle.playset import PlaysetMember


@unittest.skipUnless(os.environ.get('CK3_TASK07_EVIDENCE'), 'requires genuine retained CK3 evidence')
class CaptureSourceMtimeRequirements(unittest.TestCase):
    def setUp(self):
        evidence = json.loads(Path(os.environ['CK3_TASK07_EVIDENCE']).read_bytes())
        self.source = Path(evidence['capture_directory'])
        self.out = Path(evidence['output_root']).resolve() / uuid.uuid4().hex
        self.out.mkdir(parents=True)

    def assert_source_timestamp(self, value, mtime_ns):
        # Decode the ISO timestamp to exact epoch nanoseconds independently of
        # production formatting; datetime alone would discard the last 3 digits.
        self.assertTrue(value.endswith('+00:00'))
        whole, fraction = value.removesuffix('+00:00').split('.')
        delta = datetime.fromisoformat(whole).replace(tzinfo=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)
        self.assertEqual((delta.days * 86400 + delta.seconds) * 1_000_000_000
                         + int(fraction.ljust(9, '0')), mtime_ns)
        self.assertEqual(datetime.fromisoformat(value).utcoffset(), timedelta(0))

    def test_native_publication_and_sql_facts_preserve_source_timestamp(self):
        source_file = self.source / 'error.log'
        source_before = source_file.stat()
        digest = harvester.hash_file(source_file)
        supplied = json.loads((self.source / harvester.CAPTURE_METADATA_NAME).read_bytes())
        playset = json.loads((self.source / 'playset.json').read_bytes())
        staging_metadata = []

        def before_publication(directory, capture_id, captured_at):
            self.assertTrue(directory.name.startswith('.copying-'))
            self.assertFalse((directory.parent / capture_id).exists())
            staging_metadata.append((directory / harvester.CAPTURE_METADATA_NAME).read_bytes())
            harvester.write_playset_template(directory, captured_at=captured_at,
                members=tuple(PlaysetMember(**m) for m in playset['members']))

        capture = harvester.spool_logs(self.source, self.out, capture_metadata=supplied,
                                      include_debug=True, on_logs_copied=before_publication)
        metadata_bytes = (capture.dest_dir / harvester.CAPTURE_METADATA_NAME).read_bytes()
        self.assertEqual(staging_metadata, [metadata_bytes])
        metadata = json.loads(metadata_bytes)
        value = metadata['error_log_source_modified_at']
        self.assert_source_timestamp(value, source_before.st_mtime_ns)
        for key in supplied.keys() - {'schema_version', 'capture_id', 'captured_at',
                                      'crash_exception', 'error_log_source_modified_at'}:
            self.assertEqual(metadata[key], supplied[key])
        self.assertEqual(capture.file_stats[0].source_mtime_ns, source_before.st_mtime_ns)
        self.assertEqual(harvester.hash_file(capture.dest_dir / 'error.log'), digest)
        with create_database(self.out / 'storage') as db:
            database = db.path
        client = HandlerClient(database)
        self.addCleanup(client.shutdown)
        outcome = client.result(client.submit('ingest', {'capture_directory': capture.dest_dir}), 60)
        self.assertEqual(outcome.status, 'COMPLETED', outcome)
        with open_database_readonly(database) as db:
            run = db.latest_run()
            facts_json = db.connection.execute('SELECT facts_json FROM runs WHERE run_id=?',
                                              (run['run_id'],)).fetchone()[0]
            self.assertEqual(json.loads(facts_json), metadata)
            self.assertEqual(db.read_playset(run['run_id'])['members'], playset['members'])
            duplicate = client.result(client.submit('ingest', {'capture_directory': capture.dest_dir}), 60)
            self.assertEqual(duplicate.status, 'NOT_COMPLETED')
            self.assertEqual(len(db.list_runs()), 1)
            self.assertEqual(db.get_run(run['run_id'])['facts'], metadata)
        self.assertEqual(source_file.stat().st_mtime_ns, source_before.st_mtime_ns)
        self.assertEqual(harvester.hash_file(source_file), digest)
        (self.out / 'result.json').write_text(json.dumps(dict(
            source=str(source_file), source_mtime_ns=source_before.st_mtime_ns,
            error_log_source_modified_at=value, capture=str(capture.dest_dir),
            database=str(database), run_id=run['run_id'], log_sha256=digest,
            published_metadata_equals_staging=True, sql_facts_equal_metadata=True,
            duplicate_preserves_facts=True), indent=2) + '\n', encoding='utf-8')
        print('Source mtime evidence:', self.out, flush=True)

    def test_destination_timestamp_cannot_supply_source_fact(self):
        source_file = self.source / 'error.log'
        source_ns = source_file.stat().st_mtime_ns
        exact_copy = harvester._copy_exact

        def different_destination_time(src, dst):
            exact_copy(src, dst)
            os.utime(dst, ns=(source_ns - 10_000_000_000, source_ns - 10_000_000_000))

        with patch.object(harvester, '_copy_exact', side_effect=different_destination_time):
            capture = harvester.spool_logs(self.source, self.out)
        metadata = json.loads((capture.dest_dir / harvester.CAPTURE_METADATA_NAME).read_bytes())
        self.assertNotEqual((capture.dest_dir / 'error.log').stat().st_mtime_ns, source_ns)
        self.assert_source_timestamp(metadata['error_log_source_modified_at'], source_ns)
        self.assertEqual(capture.file_stats[0].source_mtime_ns, source_ns)

    def test_source_mtime_change_rejects_publication(self):
        logs = self.out / 'logs'
        logs.mkdir()
        shutil.copy2(self.source / 'error.log', logs / 'error.log')
        exact_copy = harvester._copy_exact

        def change_source_time(src, dst):
            exact_copy(src, dst)
            stat = src.stat()
            os.utime(src, ns=(stat.st_atime_ns, stat.st_mtime_ns + 10_000_000_000))

        with patch.object(harvester, '_copy_exact', side_effect=change_source_time):
            with self.assertRaises(harvester.UnstableCapture):
                harvester.spool_logs(logs, self.out)
        self.assertTrue(all(p.name.startswith('.copying-') for p in (self.out / 'pending').iterdir()))
        self.assertFalse(list((self.out / 'pending').glob('*/capture-metadata.json')))
