"""Task 07 checks using complete genuine inputs explicitly provided by the caller.

Set CK3_TASK07_EVIDENCE to a JSON file with capture_directory, manual_error_log,
review_error_log, legacy_storage, output_root. No generated message fixtures.
Outputs stay in a new disposable directory beneath output_root for inspection.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch
import uuid

from ck3chronicle.pipeline import ingestion, review
from ck3chronicle.pipeline.request_handler import HandlerClient
from ck3chronicle.pipeline.database_handler import _Handler
from ck3chronicle.pipeline.capture_access import capture_access
from ck3chronicle.pipeline.catalog import load_selected_classifier
from ck3chronicle.pipeline.contracts import render, render_regions, run_lineage
from ck3chronicle.pipeline.repository import create_database, open_database_readonly, RunWriteError
from ck3chronicle.pipeline.retention import retain_raw_logs, RetentionConfig


def prepare_with_worker(database, **arguments):
    handler = _Handler(database)
    try:
        handler.ready.wait()
        if handler.open_error:
            raise handler.open_error
        return ingestion._ingest(handler.database_call, handler.stopping, **arguments)
    finally:
        handler.close()


@unittest.skipUnless(os.environ.get('CK3_TASK07_EVIDENCE'), 'requires genuine retained CK3 evidence')
class Task07Requirements(unittest.TestCase):
    def test_input_and_coordination_boundaries(self):
        evidence = json.loads(Path(os.environ['CK3_TASK07_EVIDENCE']).read_bytes())
        out = Path(evidence['output_root']).resolve() / uuid.uuid4().hex
        out.mkdir(parents=True)
        pending = out / 'pending'
        pending.mkdir()
        capture = pending / Path(evidence['capture_directory']).name
        shutil.copytree(evidence['capture_directory'], capture)
        database = out / 'storage'
        with create_database(database) as initialized:
            database = initialized.path
        self.addCleanup(HandlerClient(database).shutdown)
        stamp = datetime.fromisoformat(json.loads((capture / 'capture-metadata.json').read_bytes())['captured_at'])
        self.assertFalse(retain_raw_logs(pending, config=RetentionConfig(timedelta(days=60)),
                                        now=stamp + timedelta(days=31)).eligible)
        client = HandlerClient(database)
        with capture_access(capture):
            ref = client.submit('ingest', {'capture_directory': capture})
            self.assertEqual(client.wait(ref, .2).status, 'ENQUEUED')
            with self.assertRaises(TimeoutError):
                client.result(ref, .01)
        self.assertEqual(client.result(ref, 60).status, 'COMPLETED')
        # Validate pair mismatch with a different complete genuine log, no edited messages.
        from ck3chronicle.harvester import hash_file
        from ck3chronicle.pipeline.playsets import PlaysetError
        different = hash_file(Path(evidence['manual_error_log']))
        with self.assertRaises(PlaysetError):
            ingestion._read_playset(capture, json.loads((capture / 'capture-metadata.json').read_bytes()), different)
        # Missing metadata must never acquire a made-up age.
        (capture / 'capture-metadata.json').unlink()
        skipped = retain_raw_logs(pending, preview=False, now=stamp + timedelta(days=90))
        self.assertFalse(skipped.removed)
        self.assertTrue(any('unusable capture time' in s.reason for s in skipped.skipped))
        # Read exact native bytes, but simulate a differing pre-parse hash to verify
        # that no Run is accepted under a hash other than the bytes actually parsed.
        plain = ingestion._protect_manual(Path(evidence['manual_error_log']), pending)
        other_hash = hash_file(Path(evidence['review_error_log']))
        client.shutdown()
        with patch.object(ingestion.harvester, 'hash_file', return_value=other_hash):
            with self.assertRaisesRegex(ingestion.IngestInputError, 'between hashing and parsing'):
                prepare_with_worker(database, capture_directory=plain)
        with open_database_readonly(database) as db:
            self.assertEqual(len(db.list_runs()), 1)

    def test_native_end_to_end(self):
        evidence = json.loads(Path(os.environ['CK3_TASK07_EVIDENCE']).read_bytes())
        out = Path(evidence['output_root']).resolve() / uuid.uuid4().hex
        out.mkdir(parents=True)
        pending = out / 'pending'
        pending.mkdir()
        source = Path(evidence['capture_directory'])
        capture = pending / source.name
        shutil.copytree(source, capture)
        original = {p.name: p.read_bytes() for p in capture.iterdir() if p.is_file()}
        database = out / 'storage'
        with create_database(database) as initialized:
            database = initialized.path
        self.addCleanup(HandlerClient(database).shutdown)
        old, new = '44a0401b8adf0a2953d26705', '68f1ae5db205ab46afef9c4d'
        print('Task 07 evidence:', out, flush=True)

        first = ingestion.ingest(database, capture_directory=capture, package_id=new)
        self.assertEqual(first.status, 'COMPLETED')
        duplicate = ingestion.ingest(database, capture_directory=capture, package_id='missing-package-must-not-load')
        self.assertEqual(duplicate.run_id, first.run_id)
        self.assertEqual(duplicate.status, 'NOT_COMPLETED')

        # Explicit manual input is copied once, with its full native bytes.
        manual = out / 'manual-error.log'
        shutil.copyfile(evidence['manual_error_log'], manual)
        second = ingestion.ingest(database, error_log=manual, captures_root=pending, package_id=old)
        self.assertEqual((second.capture_directory / 'error.log').read_bytes(), manual.read_bytes())
        before = set(pending.iterdir())
        duplicate = ingestion.ingest(database, error_log=manual, captures_root=pending, package_id=new)
        self.assertEqual(duplicate.run_id, second.run_id)
        self.assertEqual(set(pending.iterdir()), before)

        # A third complete genuine log exercises CLI ingestion and native review.
        cmd = [sys.executable, '-B', '-m', 'ck3chronicle.cli', 'ingest', '--database', str(database),
               '--error-log', evidence['review_error_log'], '--captures-root', str(pending), '--package-id', new]
        cli = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(cli.returncode, 0, cli.stderr)
        third = json.loads(cli.stdout)
        self.assertEqual(third['status'], 'COMPLETED')
        repeat = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(repeat.returncode, 1, repeat.stderr)
        self.assertEqual(json.loads(repeat.stdout)['run_id'], third['run_id'])
        self.assertEqual(json.loads(repeat.stdout)['status'], 'NOT_COMPLETED')

        run_ids = [first.run_id, second.run_id, third['run_id']]
        paths = [capture / 'error.log', manual, Path(evidence['review_error_log'])]
        report = {'runs': [], 'output': str(out)}
        rendered_before = {}
        with open_database_readonly(database) as db:
            self.assertEqual(len(db.list_runs()), 3)
            for run_id, path, package_id in zip(run_ids, paths, [new, old, new]):
                run = db.get_run(run_id)
                classifier = load_selected_classifier(package_id=package_id)
                expected_lineage = run_lineage(classifier.package, application_revision=ingestion.application_revision())
                for key, value in expected_lineage.items():
                    self.assertEqual(run['lineage'][key], value)
                self.assertEqual(run['lineage']['model_schema_version'], classifier.package.manifest['model_schema_version'])
                self.assertEqual(run['lineage']['package_schema_version'], classifier.package.manifest['schema_version'])
                self.assertEqual(run['lineage']['database_schema_version'], 3)
                self.assertEqual(run['log_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
                metadata = db.read_review_metadata(run_id)
                manifest = json.loads(db.resolve_review_reference(metadata['manifest_reference']).read_bytes())
                playset = db.read_playset(run_id)
                self.assertEqual(manifest['schema_version'], 3)
                self.assertEqual(manifest['lineage'], run['lineage'])
                self.assertEqual(manifest['playset'], playset)
                self.assertEqual(manifest['counts'], run['counters'])
                if run_id == first.run_id:
                    supplied = json.loads(original['playset.json'])
                    self.assertEqual(playset, dict(supplied, playset_captured=True))
                    self.assertEqual(run['facts'], json.loads(original['capture-metadata.json']))
                else:
                    self.assertFalse(playset['playset_captured'])
                    self.assertEqual(playset['members'], [])
                rows = db.read_diagnostics(run_id)
                self.assertEqual(sum(r['occurrence_count'] for r in rows), run['counters']['eligible_occurrences'])
                for status in ('template', 'provisional'):
                    self.assertEqual(sum(r['occurrence_count'] for r in db.read_diagnostics(run_id, match_status=status)),
                                     run['counters'][status + '_occurrences'])
                self.assertTrue(all(r['error_type'] == 'unknown' for r in rows))
                rendered_before[run_id] = [render(r['definition'], r['values']) for r in rows]
                # Independently reconcile every classification and review emission to native bytes.
                raw = classifier.read_log(path)
                native_records, review_ordinals, record_ordinals = {}, set(), set()
                for result in classifier.classify_raw(raw):
                    diagnostic = getattr(result, 'diagnostic', result)
                    ordinals = diagnostic.provenance['emission_ordinals']
                    if result.disposition == 'record':
                        record_ordinals.update(ordinals)
                        native_records[(tuple(ordinals), diagnostic.provenance.get('message_ordinal'))] = diagnostic.unit
                    else:
                        review_ordinals.update(ordinals)
                for row in rows:
                    unit = native_records[(tuple(row['provenance']['emission_ordinals']),
                                           row['provenance'].get('message_ordinal'))]
                    regions = dict(body=unit['body'], **unit['contexts'],
                                   **{f'continuation:{i}': v for i, v in enumerate(unit['continuations'])})
                    for name, text in render_regions(row['definition'], row['values']):
                        self.assertEqual(text, regions[name]['text'])
                payload = db.resolve_review_reference(metadata['log_reference']).read_bytes()
                self.assertEqual(payload, b''.join(raw.read_bytes(e.span) for e in raw.emissions if e.ordinal in review_ordinals))
                self.assertEqual(record_ordinals | review_ordinals, {e.ordinal for e in raw.emissions})
                report['runs'].append(dict(run_id=run_id, sha256=run['log_sha256'],
                                          lineage=run['lineage'], counters=run['counters']))

        # Failure after review publication must not return success or accept SQL.
        failure_db = out / 'failure-storage'
        with create_database(failure_db) as initialized:
            failure_db = initialized.path
        with patch.object(review, 'verify_published', side_effect=OSError('injected publication verification failure')):
            with self.assertRaises(RunWriteError) as caught:
                prepare_with_worker(failure_db, capture_directory=capture)
        failure = caught.exception
        self.assertIsNotNone(failure.published_run_id)
        from ck3chronicle.pipeline.repository import open_database
        with open_database(failure_db) as db:
            self.assertEqual(db.list_runs(), [])
            self.assertFalse(db.cleanup_unaccepted(failure.published_run_id))  # handler already guarded cleanup
            self.assertEqual(list((db.review_root / '.staging').iterdir()), [])
        self.assertEqual((capture / 'error.log').read_bytes(), original['error.log'])

        # No adoption/deletion of actual schema-1 storage, copied intact.
        legacy = out / 'legacy-storage'
        shutil.copytree(evidence['legacy_storage'], legacy)
        legacy_bytes = (legacy / 'generation.sqlite3').read_bytes()
        with self.assertRaisesRegex(ValueError, 'reset'):
            open_database(legacy / 'generation.sqlite3')
        self.assertEqual((legacy / 'generation.sqlite3').read_bytes(), legacy_bytes)

        # Retention uses elapsed capture time, without changing real metadata.
        timestamp = datetime.fromisoformat(json.loads(original['capture-metadata.json'])['captured_at'])
        young = retain_raw_logs(pending, now=timestamp + timedelta(days=29))
        self.assertNotIn(capture / 'error.log', young.eligible)
        expired = timestamp + timedelta(days=31)
        preview = retain_raw_logs(pending, now=expired)
        self.assertIn(capture / 'error.log', preview.eligible)
        self.assertFalse(preview.removed)
        self.assertTrue((capture / 'error.log').exists())
        with capture_access(capture):
            busy = retain_raw_logs(pending, preview=False, now=expired)
            self.assertNotIn(capture / 'error.log', busy.removed)
            self.assertTrue(any(s.reason == 'capture busy' for s in busy.skipped))
        # Unprocessed/failed capture copies and incomplete staging are separate cases.
        unprocessed = pending / 'unprocessed'
        shutil.copytree(source, unprocessed)
        staging = pending / '.copying-incomplete'
        shutil.copytree(source, staging)
        with patch.object(Path, 'unlink', side_effect=PermissionError('injected file in use')):
            failed_expiry = retain_raw_logs(pending, preview=False, now=expired)
        self.assertTrue(failed_expiry.failures)
        expiry = retain_raw_logs(pending, preview=False, now=expired)
        self.assertIn(capture / 'error.log', expiry.removed)
        self.assertIn(unprocessed / 'error.log', expiry.removed)
        self.assertTrue((staging / 'error.log').exists())
        for name in ('capture-metadata.json', 'playset.json'):
            self.assertEqual((capture / name).read_bytes(), original[name])
        with open_database_readonly(database) as db:
            for run_id in run_ids:
                self.assertEqual([render(r['definition'], r['values']) for r in db.read_diagnostics(run_id)],
                                 rendered_before[run_id])
                self.assertIsNotNone(db.read_playset(run_id))
                self.assertTrue(db.resolve_review_reference(db.read_review_metadata(run_id)['manifest_reference']).exists())
        report['retention'] = dict(eligible=len(preview.eligible), removed=len(expiry.removed),
                                   failures_exercised=len(failed_expiry.failures))
        (out / 'results.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
