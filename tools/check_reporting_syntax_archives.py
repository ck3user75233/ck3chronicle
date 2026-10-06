"""Receive genuine retained syntax witnesses into isolated, single-Run storage.

Input files are copied unchanged with the normal capture API; source hashes and
timestamps are checked afterward. These Runs never join production history.
Only disposable initialization bypasses HandlerClient, as required by its
bootstrap API. All ingestion and runtime reads use the handler; reports use the
actual root CLI. No synthetic messages, backfilled timestamps or fake playsets.
"""
import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import uuid

from ck3chronicle import harvester
from ck3chronicle.pipeline.repository import create_database
from ck3chronicle.pipeline.request_handler import HandlerClient, COMPLETED
from ck3chronicle.reporting.presets import SYNTAX_ROWS, ASSIGNMENT_REASON, SYNTAX_PACKAGE


def verify(args):
    inputs = json.loads(args.inputs.read_bytes())
    if args.case:
        unknown = set(args.case) - {case['name'] for case in inputs}
        if unknown:
            raise ValueError(f'Unknown archive cases: {sorted(unknown)}')
        inputs = [case for case in inputs if case['name'] in args.case]
    out = args.output_root.resolve() / uuid.uuid4().hex
    out.mkdir(parents=True)
    calls, results, seen = [], [], set()

    def save(path, data):
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    for case in inputs:
        source = Path(case['source']).resolve()
        local = out / case['name']
        local.mkdir()
        before = {'sha256': harvester.hash_file(source), 'mtime_ns': source.stat().st_mtime_ns}
        assert not (source.parent / 'playset.json').exists(), 'Handle any existing playset explicitly; do not discard it'
        capture = harvester.spool_logs(source.parent, local, capture_metadata={
            'trigger': 'retained_log_verification', 'evidence_kind': 'genuine_retained',
            'source_archive': str(source), 'verification_scope': 'Single-Run syntax check; not production chronology'})
        assert harvester.hash_file(capture.dest_dir / 'error.log') == before['sha256']
        with create_database(local / 'storage') as created:
            database = created.path
        client = HandlerClient(database)

        def read(operation, **arguments):
            reply = client.result(client.submit(operation, arguments))
            assert reply.status == COMPLETED, reply
            return reply.value

        def cli(name, query, fmt='json', preset='syntax', expected=0):
            query_path = out / (name + '-query.json')
            save(query_path, query)
            destination = out / (name + ('.txt' if fmt == 'text' else '.' + fmt))
            cmd = [sys.executable, '-I', '-B', '-m', 'ck3chronicle.cli', 'report', run_id,
                   '--database', str(database), '--package-id', SYNTAX_PACKAGE,
                   '--preset', preset, '--query', str(query_path), '--format', fmt, '--output', str(destination)]
            reply = subprocess.run(cmd, encoding='utf-8', capture_output=True, timeout=300)
            calls.append({'command': cmd, 'returncode': reply.returncode, 'stderr': reply.stderr})
            save(out / 'commands.json', calls)
            assert reply.returncode == expected, reply.stderr
            return json.loads(destination.read_bytes()) if fmt == 'json' else destination.read_text(encoding='utf-8')

        try:
            print('Ingesting unchanged retained log:', case['name'], source.stat().st_size, flush=True)
            outcome = read('ingest', capture_directory=capture.dest_dir, package_id=SYNTAX_PACKAGE)
            run_id = outcome['run_id']
            rows = read('read_diagnostics', run_id=run_id)
            playset = read('read_playset', run_id=run_id)
            assert not playset or not playset.get('playset_captured')
            pairs = {(tid, family) for tid, family, _ in SYNTAX_ROWS}
            def syntax(row):
                d = row['definition']
                return ((d['template_id'], d['source_family']) in pairs and (
                    d['template_id'] != '0b2804538785c71278ea37e7' or any(
                        r['name'] == 'body' and b['slot_id'] == 's1' and b['type'] == 'REASON'
                        and b['present'] and b['value'] == ASSIGNMENT_REASON
                        for r in row['values']['regions'] for b in r['bindings'])))
            wanted = [r for r in rows if syntax(r)]
            observed = {r['definition']['template_id'] for r in wanted}
            assert set(case['expected_templates']) <= observed, (case['name'], observed)
            seen.update(observed)
            query = {'purpose': 'Genuine retained-log syntax investigation: ' + case['description'] + '. Single-Run verification; historical playset was not retained.',
                     'analytics': {'history': False}, 'display': {'limit': 100, 'historical_limit': 0}}
            name = 'syntax-archive-' + case['name']
            report = cli(name, query)
            assert report['totals']['occurrences'] == sum(r['occurrence_count'] for r in wanted)
            assert report['totals']['distinct_records'] == len(wanted)
            assert {r['stored_record']['ordinal'] for r in report['records']} == {r['ordinal'] for r in wanted}
            assert {r['stored_record']['match_status'] for r in report['records']} == {r['match_status'] for r in wanted}
            assert not report['coverage']['source'][run_id]['complete']
            assert any('playset' in i['reason'].casefold() for i in report['coverage']['source'][run_id]['issues'])
            for fmt in ('text', 'html'):
                text = cli(name, query, fmt=fmt)
                assert 'Recorded playset is unavailable.' in text
            if case['name'] == 'equals':
                required = deepcopy(query)
                required['purpose'] = 'Genuine archived log with no retained playset: require a game-file association'
                required['scope'] = {'source': {'members': [{'root_ID': 'ROOT_GAME'}]}}
                failed = cli('archive-required-playset', required, expected=3)
                assert failed['status'] == 'source_filter_incomplete'
                assert any('playset' in i['reason'].casefold() for i in failed['partial']['coverage']['issues'])
                cli('archive-required-playset', required, fmt='html', expected=3)
            result = {'name': case['name'], 'source': str(source), 'before': before, 'run_id': run_id,
                      'database': str(database), 'observed_templates': sorted(observed),
                      'syntax_records': len(wanted), 'syntax_occurrences': sum(r['occurrence_count'] for r in wanted),
                      'match_statuses': dict(Counter(r['match_status'] for r in wanted)),
                      'optional_missing_playset_report_completed': True,
                      'scope': 'Fresh single-Run receipt of unchanged genuine retained log; file timestamp retained; no lifecycle or production-history claim.'}
            results.append(result)
            print('Passed:', json.dumps(result), flush=True)
        finally:
            client.shutdown()
            after = {'sha256': harvester.hash_file(source), 'mtime_ns': source.stat().st_mtime_ns}
            assert before == after
            save(local / 'source-integrity.json', {'before': before, 'after': after, 'unchanged': True})
            save(out / 'verification.json', {'status': 'passed' if len(results) == len(inputs) else 'in_progress',
                 'evidence_kind': 'genuine_retained', 'results': results, 'observed_templates': sorted(seen)})
    print('Evidence:', out, flush=True)
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    parser.add_argument('--case', action='append', help='Run only this named input; repeat to select several')
    verify(parser.parse_args())
