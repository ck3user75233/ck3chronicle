"""Owner-authorized two-emission fixture: only file-valued LOCATORs change.

Retained input is read-only. All generated files/storage are disposable. The
normal capture/playset writer, authenticated parser, handler ingest and root CLI
are exercised; there are no mocked clients or invented database records. This is
synthetic source-path verification, not genuine Run-history acceptance.
"""
import argparse
from copy import deepcopy
from html import escape
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from ck3chronicle import harvester
from ck3chronicle.pipeline.catalog import load_selected_classifier
from ck3chronicle.pipeline.contracts import render
from ck3chronicle.pipeline.repository import create_database
from ck3chronicle.pipeline.request_handler import HandlerClient, COMPLETED
from ck3chronicle.playset import PlaysetMember
from ck3chronicle.reporting import exact_identity


def verify(args):
    scratch = Path(__file__).resolve().parents[1] / '.codex-tmp'
    if not args.source_database.resolve().is_relative_to(scratch):
        raise ValueError('source database must be a disposable snapshot under .codex-tmp; its handler is stopped after verification')
    out = args.output_root.resolve() / uuid.uuid4().hex
    out.mkdir(parents=True)
    inputs = out / 'input'
    inputs.mkdir()
    originals = out / 'original-emissions'
    originals.mkdir()
    source = args.capture.resolve()
    source_client = HandlerClient(args.source_database)
    fixture_client = None
    calls, checks = [], []

    def save(name, value):
        (out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

    def read(client, operation, **arguments):
        reply = client.result(client.submit(operation, arguments))
        assert reply.status == COMPLETED, reply
        return reply.value

    before = {name: {'sha256': harvester.hash_file(source / name),
                     'mtime_ns': (source / name).stat().st_mtime_ns}
              for name in ('error.log', 'debug.log', 'playset.json', 'capture-metadata.json')}
    try:
        run = read(source_client, 'get_run', run_id=args.source_run)
        assert run['log_sha256'] == before['error.log']['sha256']
        playset = read(source_client, 'read_playset', run_id=args.source_run)
        original_playset = json.loads((source / 'playset.json').read_bytes())
        assert playset['members'] == original_playset['members']
        assert playset['debug_log_sha256'] == before['debug.log']['sha256']
        records = read(source_client, 'read_diagnostics', run_id=args.source_run)
        package = run['lineage']['package_id']
        classifier = load_selected_classifier(package_id=package)
        raw = classifier.read_log(source / 'error.log')
        targets = [
            (b'Error: scope:secondary_actor trigger [ Failed context switch ]',
             b'common/character_interactions/zzz_vassal_interactions.txt', 104),
            (b'Error: culture trigger [ Failed context switch ]',
             b'common/on_action/sea_minority_on_actions.txt', 141),
        ]
        fixture_bytes, provenance, expected_records = [], [], []
        for number, (marker, old_path, line) in enumerate(targets, 1):
            emission = next(e for e in raw.emissions
                            if marker in raw.read_bytes(e.span)
                            and old_path + b' line: ' + str(line).encode() in raw.read_bytes(e.span))
            original = raw.read_bytes(emission.span)
            assert original.count(old_path) == 1
            relative = Path(old_path.decode()).parent.as_posix() + '/__08b_nonexistent_' + out.name[:8] + f'_{number}.txt'
            new_path = relative.encode('utf-8')
            assert all(not (Path(m['path']) / relative).exists() for m in playset['members'] if m['path'])
            changed = original.replace(old_path, new_path, 1)
            assert changed.replace(new_path, old_path, 1) == original
            (originals / f'{number}.log').write_bytes(original)
            (originals / f'{number}-modified.log').write_bytes(changed)
            fixture_bytes.append(changed)
            record = next(r for r in records if marker.decode() in render(r['definition'], r['values'])
                          and old_path.decode() + ' line: ' + str(line) in render(r['definition'], r['values']))
            expected = deepcopy(record)
            changed_bindings = 0
            for region in expected['values']['regions']:
                for binding in region['bindings']:
                    if binding['type'] == 'LOCATOR' and binding['present'] and binding['value'] == old_path.decode():
                        binding['value'] = relative
                        changed_bindings += 1
            assert changed_bindings == 1
            expected_records.append(expected)
            provenance.append({'entry': number, 'original_span': [emission.span.start, emission.span.end],
                               'original_path': old_path.decode(), 'fixture_path': relative,
                               'line_unchanged': line, 'only_path_bytes_changed': True,
                               'template_id': record['definition']['template_id']})
        (inputs / 'error.log').write_bytes(b''.join(fixture_bytes))
        shutil.copy2(source / 'debug.log', inputs / 'debug.log')
        parsed = classifier.read_log(inputs / 'error.log')
        assert len(parsed.emissions) == 2
        del raw, parsed, classifier

        def write_playset(directory, capture_id, captured_at):
            harvester.write_playset_template(directory, captured_at=captured_at,
                members=tuple(PlaysetMember(**m) for m in playset['members']))

        capture = harvester.spool_logs(inputs, out, include_debug=True, on_logs_copied=write_playset,
            capture_metadata={'trigger': 'synthetic_reporting_fixture', 'evidence_kind': 'synthetic',
                'source_run_id': args.source_run, 'fixture_description': 'Two genuine emissions; only file LOCATOR paths changed.'})
        fixture_playset = json.loads((capture.dest_dir / 'playset.json').read_bytes())
        assert fixture_playset['members'] == playset['members']
        assert fixture_playset['error_log_sha256'] == harvester.hash_file(inputs / 'error.log')
        assert fixture_playset['debug_log_sha256'] == before['debug.log']['sha256']
        storage = out / 'storage'
        # Explicit disposable bootstrap only. All ingest and runtime reads below
        # use HandlerClient; no repository queries or direct SQL are used.
        with create_database(storage) as created:
            database = created.path
        fixture_client = HandlerClient(database)
        ingested = read(fixture_client, 'ingest', capture_directory=capture.dest_dir, package_id=package)
        selected = ingested['run_id']
        stored = read(fixture_client, 'read_diagnostics', run_id=selected)
        assert len(stored) == 2 and all(r['occurrence_count'] == 1 for r in stored)
        assert {json.dumps(exact_identity(r), sort_keys=True) for r in stored} == {
            json.dumps(exact_identity(r), sort_keys=True) for r in expected_records}
        assert read(fixture_client, 'read_playset', run_id=selected)['members'] == playset['members']
        save('fixture.json', {'evidence_kind': 'synthetic', 'source_run_id': args.source_run,
            'source_capture': str(source), 'package_id': package, 'database': str(database),
            'run_id': selected, 'capture': str(capture.dest_dir), 'entries': provenance,
            'playset_members': len(playset['members']), 'playset_members_unchanged': True,
            'playset_hashes_rebuilt_by_normal_writer': True,
            'scope': 'Missing diagnostic file paths in an otherwise readable genuine playset. No missing root, failed-read or historical chronology claim.'})
        print('Fixture:', out, 'Run:', selected, flush=True)

        def cli(name, query, preset='frequent', fmt='json', verbose=False, expected=0):
            qpath = out / (name + '-query.json')
            save(qpath.name, query)
            destination = out / (name + ('.txt' if fmt == 'text' else '.' + fmt))
            command = [sys.executable, '-I', '-B', '-m', 'ck3chronicle.cli', 'report', selected,
                       '--database', str(database), '--package-id', package, '--preset', preset,
                       '--query', str(qpath), '--format', fmt, '--output', str(destination)]
            if verbose:
                command.append('--verbose')
            reply = subprocess.run(command, capture_output=True, encoding='utf-8', timeout=180)
            call = {'command': command, 'returncode': reply.returncode, 'stderr': reply.stderr}
            if name in {'synthetic-missing-files', 'synthetic-unresolved-paths'}:
                call['attachments'] = [
                    {'label': label, 'path': str(path)} for label, path in (
                        ('Two-entry synthetic error.log', capture.dest_dir / 'error.log'),
                        ('Recorded playset members with fixture log hashes', capture.dest_dir / 'playset.json'),
                        ('Exact original-to-fixture changes', out / 'fixture.json'),
                        ('Original first emission', originals / '1.log'),
                        ('Original second emission', originals / '2.log'),
                        ('Executed verification results', out / 'verification.json'))]
            calls.append(call)
            save('commands.json', calls)
            assert reply.returncode == expected, reply.stderr
            result = destination.read_bytes().decode('utf-8')
            print('CLI completed:', name, fmt, flush=True)
            return json.loads(result) if fmt == 'json' else result

        base_query = {'purpose': 'Synthetic fixture: two genuine emissions with only file LOCATOR paths changed to nonexistent files',
                      'analytics': {'history': False}, 'display': {'limit': 10, 'historical_limit': 0}}
        result = cli('synthetic-missing-files', base_query, verbose=True)
        assert result['totals']['distinct_records'] == 2 and result['totals']['occurrences'] == 2
        coverage = result['coverage']['source'][selected]
        assert coverage['complete'] and not coverage['issues'] and coverage['reference_count'] == 2
        assert len(coverage['roots']) == len(playset['members'])
        assert all(r['available'] for r in coverage['roots'])
        assert all(r['reference_details'] and not r['candidates'] for r in result['records'])
        for fmt in ('text', 'html'):
            rendered = cli('synthetic-missing-files', base_query, fmt=fmt, verbose=True)
            assert 'File not found' in rendered
            for entry in result['records']:
                assert (escape(entry['message'], quote=False) if fmt == 'html' else entry['message']) in rendered
        checks.append({'name': 'optional_context', 'status': 'passed', 'diagnostics': 2, 'occurrences': 2,
                       'candidate_files': 0, 'complete_search': True, 'formats': ['json', 'text', 'html']})
        hotspots = cli('synthetic-missing-hotspots', base_query, preset='hotspots')
        assert hotspots['totals'] == result['totals']
        assert len(hotspots['rollups']['referenced_files']['buckets']) == 2
        assert not hotspots['rollups']['candidate_files']['buckets']
        cli('synthetic-missing-hotspots', base_query, preset='hotspots', fmt='html')
        checks.append({'name': 'hotspots_keep_unresolved_paths', 'status': 'passed', 'diagnostics': 2})
        query = deepcopy(base_query)
        paths = [e['fixture_path'] for e in provenance]
        query['scope'] = {'source': {'relative_path': {'exact': paths}}}
        filtered = cli('synthetic-find-missing-files', query)
        assert filtered['status'] == 'completed' and filtered['totals'] == result['totals']
        assert filtered['coverage']['source'][selected]['complete']
        cli('synthetic-find-missing-files', query, fmt='html')
        checks.append({'name': 'relative_path_filter', 'status': 'passed', 'matches': 2, 'complete_search': True})
        query['scope']['source'] = {'files': paths}
        selected_paths = cli('synthetic-required-missing-files', query)
        assert selected_paths['status'] == 'completed' and selected_paths['totals'] == result['totals']
        assert not selected_paths['coverage']['source'][selected]['issues']
        cli('synthetic-required-missing-files', query, fmt='html')
        checks.append({'name': 'explicit_file_paths', 'status': 'passed', 'matches': 2,
                       'interpretation': 'Match recorded file paths even when the files do not exist on disk.'})
        query['scope']['source'] = {'referenced_paths': [provenance[0]['fixture_path']]}
        reference = cli('synthetic-stored-missing-reference', query)
        assert reference['totals']['distinct_records'] == 1 and reference['totals']['occurrences'] == 1
        assert not reference['records'][0]['candidates']
        cli('synthetic-stored-missing-reference', query, fmt='html')
        checks.append({'name': 'stored_reference_filter', 'status': 'passed', 'matches': 1})
        for name, selection, expected_count in (
            ('synthetic-unmentioned-file', {'files': [paths[0] + '.unmentioned']}, 0),
            ('synthetic-directory', {'directories': [str(Path(paths[0]).parent)], 'recursive': False}, 1),
            ('synthetic-absolute-file', {'files': [str(Path(playset['members'][0]['path']) / paths[0])]}, 1),
            ('synthetic-member-missing-files', {'files': paths, 'members': [{'load_order': 115}]}, 0),
        ):
            query['scope']['source'] = selection
            checked = cli(name, query)
            assert checked['status'] == 'completed' and checked['totals']['distinct_records'] == expected_count
            assert not checked['coverage']['source'][selected]['issues']
            cli(name, query, fmt='html')
            checks.append({'name': name, 'status': 'passed', 'matches': expected_count})
        for name, selection, expected_count in (
            ('synthetic-unresolved-paths', {'resolution': 'unresolved'}, 2),
            ('synthetic-resolved-paths', {'resolution': 'resolved'}, 0),
            ('synthetic-unresolved-directory', {'resolution': 'unresolved', 'directories': ['common/on_action']}, 1),
            ('synthetic-unresolved-member', {'resolution': 'unresolved', 'members': [{'load_order': 115}]}, 2),
            ('synthetic-unresolved-content', {'resolution': 'unresolved', 'content': {'contains': 'culture'}}, 0),
        ):
            query['scope']['source'] = selection
            query['purpose'] = 'Synthetic fixture: select messages by current path resolution, separately from ordinary path matching'
            checked = cli(name, query)
            assert checked['status'] == 'completed' and checked['totals']['distinct_records'] == expected_count
            assert checked['coverage']['source'][selected]['complete']
            for record in checked['records']:
                assert record['reference_resolution']
                assert all(r['status'] == 'unresolved' and not r['candidate_ids'] for r in record['reference_resolution'])
            for fmt in (('html', 'text') if name == 'synthetic-unresolved-paths' else ('html',)):
                rendered = cli(name, query, fmt=fmt)
                if expected_count:
                    assert 'File not found' in rendered
                for record in checked['records']:
                    assert (escape(record['message'], quote=False) if fmt == 'html' else record['message']) in rendered
            checks.append({'name': name, 'status': 'passed', 'matches': expected_count})
        save('verification.json', {'status': 'passed', 'evidence_kind': 'synthetic', 'checks': checks,
             'only_two_locator_paths_changed': True, 'normal_playset_integrity': True})
        print(json.dumps(checks, indent=2), flush=True)
    finally:
        if fixture_client:
            fixture_client.shutdown()
        # Source database is an explicitly supplied disposable snapshot.
        source_client.shutdown()
        after = {name: {'sha256': harvester.hash_file(source / name),
                        'mtime_ns': (source / name).stat().st_mtime_ns} for name in before}
        save('source-integrity.json', {'before': before, 'after': after, 'unchanged': before == after})
        assert before == after, 'Retained source changed during verification'
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-database', type=Path, required=True, help='Disposable unchanged source snapshot; its handler is stopped after the check')
    parser.add_argument('--source-run', required=True)
    parser.add_argument('--capture', type=Path, required=True, help='Genuine retained paired capture; read-only')
    parser.add_argument('--output-root', type=Path, required=True)
    print('Verified:', verify(parser.parse_args()), flush=True)
