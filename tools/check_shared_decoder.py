"""Compare decoder/search/parser hookups on supplied genuine evidence only.

No fixtures, source edits, production activation or model publication. Outputs
belong in ignored storage. --baseline-source is a pre-change SourceSearch copy.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import types

from ck3chronicle.decoder import Decoder, normalize_newlines, physical_lines
from ck3chronicle.pipeline.catalog import load_selected_package
from ck3chronicle.pipeline.request_handler import HandlerClient


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2), encoding='utf-8')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--sample-survey', type=Path, required=True)
    cli.add_argument('--baseline-source', type=Path, required=True)
    cli.add_argument('--candidate-source', type=Path, required=True, help='Disposable candidate SourceSearch copy; never patches the installed caller.')
    cli.add_argument('--logs-manifest', type=Path, required=True)
    cli.add_argument('--database', type=Path, required=True, help='Existing disposable genuine-data database only.')
    cli.add_argument('--run', required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    baseline = types.ModuleType('ck3chronicle.reporting._source_before_decoder')
    baseline.__package__ = 'ck3chronicle.reporting'
    exec(compile(args.baseline_source.read_bytes(), str(args.baseline_source), 'exec'), baseline.__dict__)
    candidate = types.ModuleType('ck3chronicle.reporting._source_decoder_candidate')
    candidate.__package__ = 'ck3chronicle.reporting'
    exec(compile(args.candidate_source.read_bytes(), str(args.candidate_source), 'exec'), candidate.__dict__)
    SourceSearch = candidate.SourceSearch
    old = baseline.SourceSearch(scratch_directory=args.output)
    new = SourceSearch(scratch_directory=args.output)
    files = json.loads(args.sample_survey.read_bytes())['files']
    summary = {'sample_files': len(files), 'statuses': Counter(), 'newline_styles': Counter(),
               'source_text_equal': 0, 'parser_logs': [], 'search_comparisons': []}
    rows, readable, ambiguous = [], [], []
    for file in files:
        path = Path(file['path'])
        raw = path.read_bytes()
        check(hashlib.sha256(raw).hexdigest() == file['sha256'], f'Genuine sample changed: {path}')
        result = new.decoder.read(path)
        summary['statuses'][result.status] += 1
        if result.method != 'detected' and result.text is not None:
            check(result.text == raw.decode('utf-8-sig', errors='strict'), f'UTF-8 text differs: {path}')
            check(result.working_text == normalize_newlines(raw.decode('utf-8-sig')), f'Working text differs: {path}')
            summary['source_text_equal'] += 1
            summary['newline_styles'][result.newlines['style']] += 1
            readable.append({'physical_path': str(path)})
        else:
            ambiguous.append(file)
        rows.append({'path': str(path), **result.metadata()})
    save(args.output / 'sample-decoding.json', rows)
    print('Sample decode comparison:', dict(summary['statuses']), flush=True)

    # Same genuine files and literal/grouped predicates through both rg paths.
    expressions = [{'contains': 'culture'}, {'contains': 'NAME', 'case_sensitive': True},
                   {'and': [{'contains': 'culture'}, {'not_contains': 'faith'}]},
                   {'or': [{'contains': 'faith'}, {'contains': 'religion'}]}]
    for expression in expressions:
        previous, previous_issues = old._content(readable, expression)
        current, current_issues = new._content(readable, expression)
        check(not previous_issues and not current_issues, 'Search unexpectedly incomplete on readable sample.')
        check(previous == current, f'Search parity failed: {expression}')
        summary['search_comparisons'].append({'expression': expression, 'matching_files': len(current), 'equal': True})
        print('Search comparison:', expression, len(current), flush=True)
    for path, lines in current.items():
        if lines:
            target = lines[0]['line']
            excerpt = new.excerpts_for({path: {target}})[path, target]
            check(next(row['text'] for row in excerpt['lines'] if row['target']) == lines[0]['text'], 'Search/excerpt line disagreement.')
    all_paths = {row['physical_path']: {1} for row in readable}
    a, b = old.excerpts_for(all_paths), new.excerpts_for(all_paths)
    check(a == {k: {x: y for x, y in v.items() if x != 'decoding'} for k, v in b.items()}, 'Excerpt parity failed.')
    summary['excerpt_files_equal'] = len(a)
    # A real adjacent-line query expressed in both newline conventions.
    multiline = next(row for row in rows if row['newlines'] and row['newlines']['style'] == 'CRLF')
    path = multiline['path']
    text = new.decoder.read(path).working_text
    literal = '\n'.join(physical_lines(text)[:2])
    check('\n' in literal, 'Selected genuine file has no adjacent lines.')
    a, issues = new._content([{'physical_path': path}], {'contains': literal})
    b, other = new._content([{'physical_path': path}], {'contains': literal.replace('\n', '\r\n')})
    check(a == b and path in a and not issues and not other, 'CRLF/LF query normalization failed.')
    summary['multiline_query_equal'] = True
    for file in ambiguous:
        path = file['path']
        check(new.decoder.read(path).status == 'undetermined', 'Expected low-confidence detection failure.')
        matched, issues = new._content([{'physical_path': path}], {'not_contains': 'culture'})
        check(not matched and issues and issues[0]['content_searched'] is False, 'Ambiguous input became an invented negative match.')
        supplied = Decoder(encoding='cp1252')
        result = supplied.read(path)
        check(result.text == Path(path).read_bytes().decode('cp1252'), 'Explicit interpretation differs.')
        overridden = SourceSearch(decoder=supplied, scratch_directory=args.output)
        target = next((i, line) for i, line in enumerate(physical_lines(result.text), 1)
                      if any(ord(c) > 127 for c in line))
        matched, issues = overridden._content([{'physical_path': path}], {'contains': target[1], 'case_sensitive': True})
        excerpt = overridden.excerpts_for({path: {target[0]}})[path, target[0]]
        check(not issues and path in matched and any(line['text'] == target[1] for line in matched[path]), 'Override search failed.')
        check(next(line['text'] for line in excerpt['lines'] if line['target']) == target[1], 'Override excerpt differs.')
    summary['explicit_override_cases'] = len(ambiguous)
    check(all('--encoding' in row['options'] and 'none' in row['options'] for row in new.metrics['ripgrep_invocations']), 'rg chooses decoding independently.')
    check(not list(args.output.glob('ck3-source-*')), 'Temporary search input leaked.')

    # Public search and investigation callers use genuine stored playset/records.
    package = load_selected_package()
    client = HandlerClient(args.database)
    try:
        from ck3chronicle.reporting.analysis import DiagnosticAnalysis
        before, after = baseline.SourceSearch(client, scratch_directory=args.output), SourceSearch(client, scratch_directory=args.output)
        selection = {'files': ['common/on_action/sea_minority_on_actions.txt'],
                     'content': {'contains': 'do_culture_faith_migration'}}
        previous, current = before.search(selection, run_id=args.run), after.search(selection, run_id=args.run)
        check(previous['files'] == [{k: v for k, v in c.items() if k != 'decoding'} for c in current['files']], 'Public source search changed matched associations/lines.')
        check(previous['coverage']['complete'] and current['coverage']['complete'], 'Public search incomplete.')
        query = {'scope': {'source': selection}, 'analytics': {'history': False, 'include_absent': False},
                 'display': {'limit': 2, 'historical_limit': 0}}
        previous = DiagnosticAnalysis(client, source_resolver=before).investigate(args.run, package_id=package.manifest['package_id'], query=query)
        current = DiagnosticAnalysis(client, source_resolver=after).investigate(args.run, package_id=package.manifest['package_id'], query=query)
        check(previous.totals == current.totals, 'Investigation totals differ.')
        def without_decoding(value):
            if isinstance(value, dict):
                return {k: without_decoding(v) for k, v in value.items() if k != 'decoding'}
            return [without_decoding(v) for v in value] if isinstance(value, list) else value
        check(without_decoding(previous.records) == without_decoding(current.records), 'Investigation records differ.')
        summary['public_search_files'] = len(after.search(selection, run_id=args.run)['files'])
        summary['investigation_totals'] = current.totals
    finally:
        client.shutdown()
    print('Source search, excerpts and public investigation comparisons passed.', flush=True)

    # Same API, using the UTF-8 encoding already declared by the parser.
    logs = sorted({f['sha256']: f for f in json.loads(args.logs_manifest.read_bytes())['files'] if f['bytes']}.values(), key=lambda f: f['bytes'])
    selected = [logs[i] for i in (len(logs) // 4, len(logs) // 2, 3 * len(logs) // 4)]
    for file in selected:
        path = Path(file['path'])
        raw = path.read_bytes()
        check(hashlib.sha256(raw).hexdigest() == file['sha256'], f'Genuine log changed: {path}')
        decoder = Decoder(encoding='utf-8')
        decoded = decoder.decode(raw)
        check(decoded.raw == raw and raw[decoded.bom_bytes:] == decoded.text.encode('utf-8'), 'Whole-log byte reconstruction failed.')
        previous = package.parse_file(path)
        # Compare interpretation without modifying parser input/results or
        # substituting a source object. Actual decoder-call integration is pending.
        native_text = previous.text_between(decoded.bom_bytes, len(raw))
        check(decoded.text == native_text, 'Decoder/native-parser text differs.')
        check(b''.join(e.native_bytes() for e in previous.emissions) == raw, 'Emission reconstruction failed.')
        summary['parser_logs'].append({'path': str(path), 'sha256': file['sha256'], 'bytes': len(raw),
                                       'emissions': len(previous.emissions),
                                       'decoded_text_equal_to_unmodified_parser': True,
                                       'decoder_call_integration': 'pending'})
        print('Decoder/native-parser text comparison passed:', len(previous.emissions), 'emissions', flush=True)
    # Genuine isolated invalid bytes must retain the existing processing text.
    invalid = []
    missing, changed = [], []
    for file in logs:
        try:
            raw = Path(file['path']).read_bytes()
        except OSError:
            missing.append(file['path'])
            continue
        if hashlib.sha256(raw).hexdigest() != file['sha256']:
            changed.append(file['path'])
            continue
        try:
            raw.decode('utf-8-sig', errors='strict')
        except UnicodeError as exc:
            decoded = Decoder(encoding='utf-8').decode(raw)
            previous = package.parse_file(file['path'])
            check(b''.join(e.native_bytes() for e in previous.emissions) == raw, 'Original parser lost malformed-byte evidence.')
            same_text = decoded.text == previous.text_between(decoded.bom_bytes, len(raw))
            check(decoded.text is not None and decoded.text.encode('utf-8', 'surrogateescape') == raw,
                  'Shared decoder lost original log bytes.')
            invalid.append({'path': file['path'], 'sha256': file['sha256'], 'byte_error': str(exc),
                            'decoder': decoded.metadata(), 'decoded_text_equal_to_unmodified_parser': same_text,
                            'original_parser_bytes_preserved': True})
    summary['genuine_non_utf8_log_checks'] = invalid
    summary['log_paths_unavailable'] = missing
    summary['log_paths_changed'] = changed
    summary['package_id'] = package.manifest['package_id']
    summary['unverified'] = ['UTF-16/32 and East Asian genuine files absent from sample',
                             'Double/conflicting/displaced BOM and BOM-mojibake positive cases absent',
                             'Lone-CR genuine files absent; mixed CRLF/LF observed in one log', 'Concurrent modification cases not injected',
                             'Live ingestion activation and future package upgrade not performed']
    # A rejected genuine log accepted by the existing parser is a regression,
    # not a successful ambiguity-handling case. Persist evidence before failing.
    differences = [row for row in invalid if not row['decoded_text_equal_to_unmodified_parser']]
    summary['parser_text_compatibility'] = 'failed' if differences else 'passed_on_checked_inputs'
    summary['decoder_call_integration'] = 'Separate disposable-parser experiment; not exercised by this tool.'
    save(args.output / 'verification.json', summary)
    print(json.dumps(summary, indent=2))
    check(not differences, f'Decoder/parser compatibility failed for {len(differences)} genuine log(s); see verification.json.')


if __name__ == '__main__':
    main()
