"""Compare real source searches with independent PowerShell tree measurements.

Retained SQLite is backed up read-only; runtime reads and root-CLI reports use
only its disposable copy through HandlerClient. Installed sources are read-only.
No generated source trees, synthetic histories, mocks or injected failures.
"""
import argparse
from html import escape
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET

from ck3chronicle.pipeline.request_handler import HandlerClient, COMPLETED
from ck3chronicle.reporting import DiagnosticAnalysis, SourceSearch
from ck3chronicle.reporting.presentation import _page, _el, _table


TREE_COUNT = r'''
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$selection = [Console]::In.ReadToEnd() | ConvertFrom-Json
$treeRoot = Get-Item -LiteralPath $selection.root -Force
$treeItems = @(Get-ChildItem -LiteralPath $treeRoot.FullName -Force -Recurse -ErrorAction Stop)
$treeLinks = @($treeItems | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint })
@{
  files = @($treeItems | Where-Object { -not $_.PSIsContainer } | ForEach-Object { $_.FullName })
  folders = @($treeRoot.FullName) + @($treeItems | Where-Object { $_.PSIsContainer } | ForEach-Object { $_.FullName })
  reparse_points = @($treeLinks | ForEach-Object { $_.FullName })
} | ConvertTo-Json -Depth 4 -Compress
'''


def physical(path):
    return os.path.normcase(os.path.abspath(path))


def main(args):
    out = args.output_root.resolve() / uuid.uuid4().hex
    out.mkdir(parents=True)
    database = out / 'genuine.sqlite3'
    with sqlite3.connect(args.source_database.resolve().as_uri() + '?mode=ro', uri=True) as source:
        with sqlite3.connect(database) as target:
            source.backup(target)
    client = HandlerClient(database)
    comparisons, measurements, calls, expected_cache = [], {}, [], {}

    def save(name, data):
        (out / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    def read(op, **kwargs):
        reply = client.result(client.submit(op, kwargs))
        assert reply.status == COMPLETED, reply
        return reply.value

    def expected(root, directories, recursive):
        key = (physical(root), tuple(directories), recursive)
        if key in expected_cache:
            return expected_cache[key]
        tree = measurements[physical(root)]
        starts = [Path(root) / directory for directory in directories]
        files = {p for p in tree['files'] if any(
            Path(p).is_relative_to(start) if recursive else Path(p).parent == start for start in starts)}
        folders = {p for p in tree['folders'] if any(
            Path(p).is_relative_to(start) if recursive else Path(p) == start for start in starts)}
        expected_cache[key] = files, folders
        return files, folders

    def check_counts(name, coverage):
        files, folders = set(), set()
        for scope in coverage['search_scopes']:
            wanted_files, wanted_folders = expected(scope['root'], scope['directories'], scope['recursive'])
            assert scope['complete'], scope
            assert scope['files_searched'] == len(wanted_files), (name, scope, len(wanted_files))
            assert scope['folders_searched'] == len(wanted_folders), (name, scope, len(wanted_folders))
            files.update(wanted_files)
            folders.update(wanted_folders)
        counts = coverage['search_counts']
        assert counts['files_searched'] == len(files), (name, counts, len(files))
        assert counts['folders_searched'] == len(folders), (name, counts, len(folders))
        assert coverage['complete'], (name, coverage['issues'])
        comparisons.append({'name': name, 'expected_files': len(files), 'reported_files': counts['files_searched'],
            'expected_folders': len(folders), 'reported_folders': counts['folders_searched'],
            'status': 'passed', 'scopes': coverage['search_scopes']})
        save('comparisons-in-progress.json', comparisons)
        return files

    try:
        run = read('get_run', run_id=args.run_id)
        playset = read('read_playset', run_id=args.run_id)
        members = [m for m in playset['members'] if m['load_order'] in args.member_order]
        assert len(members) == len(args.member_order), 'Requested member not present in recorded playset'
        for member in members:
            root = member['path']
            reply = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', TREE_COUNT],
                input=json.dumps({'root': root}), capture_output=True, encoding='utf-8', timeout=240)
            assert reply.returncode == 0, reply.stderr
            independent = json.loads(reply.stdout)
            assert not independent['reparse_points'], 'Reparse-point traversal requires a separate comparison'
            tree = {kind: {physical(p) for p in independent[kind]} for kind in ('files', 'folders')}
            measurements[physical(root)] = tree
            save(f'root-{member["load_order"]}-independent.json', independent)
            print('Independent root count:', member['name'] or member['root_ID'], len(tree['files']),
                  'files;', len(tree['folders']), 'folders including root', flush=True)
            search = SourceSearch()

            def check(name, selector, service=search, exact_files=None):
                result = service.search({'roots': [root], **selector})
                visited = check_counts(f'{member["load_order"]}: {name}', result['coverage'])
                actual = {physical(f['physical_path']) for f in result['files']}
                assert actual == (visited if exact_files is None else exact_files), name
                assert result['coverage']['search_counts']['matching_files'] == len(actual)
                return result

            full = check('whole root, recursive, cold', {'recursive': True})
            again = check('whole root, recursive, cached', {'recursive': True})
            assert again['coverage']['search_scopes'][0]['cache'] == 'exact_scope'
            assert again['coverage']['search_counts'] == full['coverage']['search_counts']
            for name, selector in (
                ('root only', {'recursive': False}),
                ('common recursive', {'directories': ['common'], 'recursive': True}),
                ('common without recursion', {'directories': ['common'], 'recursive': False}),
                ('overlapping directory scopes', {'directories': ['common', 'common/on_action'], 'recursive': True}),
            ):
                cached = check(name + ', from cached root', selector)
                cold = check(name + ', cold', selector, SourceSearch())
                assert cached['coverage']['search_counts'] == cold['coverage']['search_counts']
                assert cached['coverage']['search_scopes'][0]['cache'] == 'whole_root_subset'
            nested = next(p for p in sorted(tree['files']) if Path(p).is_relative_to(Path(root) / 'common')
                          and Path(p).suffix == '.txt' and Path(p).parent != Path(root) / 'common')
            relative = Path(nested).relative_to(root).as_posix()
            for label, service in (('cached', search), ('cold', SourceSearch())):
                check('exact path narrows to parent, ' + label, {'files': [relative]}, service, {nested})
            by_name = {p for p in tree['files'] if Path(p).name == Path(nested).name}
            check('filename-only search traverses the root', {'filename': {'exact': [Path(nested).name]}},
                  SourceSearch(), by_name)
            duplicate = search.search({'roots': [root, root], 'recursive': True})
            check_counts(f'{member["load_order"]}: repeated root associations', duplicate['coverage'])
            assert len(duplicate['files']) == 2 * len(tree['files'])
            assert duplicate['coverage']['search_counts']['matching_files'] == len(tree['files'])

        # A real root-CLI report uses a known path, so its actual lookup should
        # enumerate only common/on_action in the selected recorded mod root.
        member = next(m for m in members if m['load_order'] == 114)
        query = {'purpose': 'Validate source-search file and folder counts for a recorded script path',
                 'scope': {'source': {'members': [{'load_order': 114}],
                    'files': ['common/on_action/sea_minority_on_actions.txt']}},
                 'analytics': {'history': False}, 'display': {'limit': 20}}
        save('recursion-scoped-report-query.json', query)
        for fmt in ('json', 'text', 'html'):
            destination = out / ('recursion-scoped-report.' + ('txt' if fmt == 'text' else fmt))
            command = [sys.executable, '-I', '-B', '-m', 'ck3chronicle.cli', 'report', args.run_id,
                '--database', str(database), '--package-id', run['lineage']['package_id'], '--preset', 'frequent',
                '--query', str(out / 'recursion-scoped-report-query.json'), '--format', fmt, '--output', str(destination)]
            reply = subprocess.run(command, capture_output=True, encoding='utf-8', timeout=240)
            calls.append({'command': command, 'returncode': reply.returncode, 'stderr': reply.stderr,
                          'attachments': [{'label': 'Independent recursion measurements and comparison',
                                           'path': str(out / 'recursion-verification.html')}]})
            save('commands.json', calls)
            assert reply.returncode == 0, reply.stderr
            if fmt == 'json':
                report = json.loads(destination.read_bytes())
                coverage = report['coverage']['source'][args.run_id]
                check_counts('Root CLI: recorded file in selected mod', coverage)
                assert coverage['search_scopes'][0]['directories'] == ['common/on_action']
                assert not coverage['search_scopes'][0]['recursive']
                assert report['totals']['distinct_records'] > 0
            else:
                text = destination.read_bytes().decode('utf-8')
                assert 'Files checked (names/paths)' in text
                assert 'Folders checked' in text
                assert 'common/on_action' in text
                for entry in report['records']:
                    assert (escape(entry['message'], quote=False) if fmt == 'html' else entry['message']) in text
        # Existing stored-only filtering must keep reporting zero filesystem work.
        stored = DiagnosticAnalysis(client, source_resolver=SourceSearch(client)).investigate(args.run_id,
            package_id=run['lineage']['package_id'], query={'scope': {'source': {'files': query['scope']['source']['files']}},
                                                         'analytics': {'history': False}})
        assert stored.coverage['source'][args.run_id]['search_counts']['files_searched'] == 0
        assert stored.coverage['source'][args.run_id]['search_counts']['folders_searched'] == 0
        assert stored.totals['distinct_records'] == report['totals']['distinct_records']

        save('verification.json', {'status': 'passed', 'evidence_kind': 'genuine', 'comparisons': comparisons,
             'report_totals': report['totals'], 'sql_only_filesystem_counts': 0,
             'independent_method': 'PowerShell Get-ChildItem -LiteralPath -Force -Recurse; exact file sets compared as well as counts',
             'limitations': 'Read-only current trees; reparse points and unavailable traversals not represented. Counts are measurements, not acceptance thresholds.'})
        page = ET.Element('main')
        _el(page, 'h1', 'Does source search descend into the right folders?')
        _el(page, 'p', 'This check independently counted real files and folders using PowerShell, then compared SourceSearch on the same trees. '
            'A recursive search should agree with the full tree. Turning recursion off should inspect only the starting folder. '
            'Directory and exact-file scopes should inspect only their allowed folders. Cached and fresh searches should return the same file sets and counts.')
        _el(page, 'h2', 'Actual result')
        _el(page, 'p', f'All {len(comparisons)} scope/count comparisons passed, including exact returned-file sets for standalone searches. '
            'The root CLI also exported matching JSON, text and HTML counts. Stored-path-only library filtering performed zero filesystem work.')
        _el(page, 'p', 'Folders include each starting directory and empty folders. Files checked means names/paths considered before filters, '
            'not file contents read. Repeated roots retain separate candidate associations but totals count each physical path once.')
        _table(page, ['Case', 'Independent files', 'Search files', 'Independent folders', 'Search folders', 'Result'], [
            [v['name'], v['expected_files'], v['reported_files'], v['expected_folders'], v['reported_folders'], v['status']] for v in comparisons])
        _el(page, 'h2', 'Measured roots')
        _table(page, ['Recorded member', 'Root', 'Files recursively', 'Folders including root'], [
            [m['name'] or m['root_ID'], m['path'], len(measurements[physical(m['path'])]['files']),
             len(measurements[physical(m['path'])]['folders'])] for m in members])
        _el(page, 'p', 'No source file, production database or active package was changed. Unavailable traversals and reparse points remain unverified.')
        (out / 'recursion-verification.html').write_text(_page('Source recursion verification', page), encoding='utf-8')
        print('Verified:', out, len(comparisons), 'comparisons', flush=True)
    finally:
        client.shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-database', type=Path, required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    parser.add_argument('--member-order', type=int, action='append', default=None)
    args = parser.parse_args()
    args.member_order = args.member_order or [0, 114]
    main(args)
