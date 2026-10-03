"""Summarize the native stack investigation and inspect saved review evidence read-only."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace

from ck3chronicle.pipeline.contracts import render
from template_learning.matcher_example import load_verified


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', '\\n').replace('\r', '\\r')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--results', type=Path, required=True)
    cli.add_argument('--selection', type=Path, required=True)
    cli.add_argument('--task06', type=Path, required=True)
    cli.add_argument('--sample', type=Path, required=True)
    cli.add_argument('--sample-html', type=Path, required=True)
    args = cli.parse_args()
    summary = read(args.results / 'summary.json')
    selection = read(args.selection)
    model = read(args.selection.parent / selection['artifact_directory'] / 'empirical_template_model.json')
    sample = read(args.sample)
    html = args.sample_html.read_text(encoding='utf-8')
    embedded = re.search(r'<script[^>]*id="sql-sample-data"[^>]*>(.*?)</script>', html, re.S)
    assert embedded and json.loads(embedded[1]) == sample
    sample17 = sample['records'][16]
    assert render(json.loads(sample17['definition']['definition_json']), sample17['values']) == sample17['rendered']
    stats = dict(stack_rows_within_logs=0, distinct_complete_stack_inputs=0,
                 frames=0, frames_with_trace=0, frames_without_trace=0,
                 selected_frames=0, input_bytes=0, raw_script_markers=0,
                 lengths={}, review=[], html_sample_equal=True, saved_definition_render_equal=True)
    seen, selected, examples = set(), Counter(), read(args.results / 'examples.json')
    chosen = {'saved_sample_17': examples['saved_sample_17']}
    wanted = {'f0cd72fd7357b2cfc5c275ad': 'four_frame_trigger',
              'b93cd68fb7b8374d173b423e': 'one_frame_comparison',
              'bd05cdbc8471ae8529ae1bc0': 'four_frame_comparison'}
    lengths = defaultdict(lambda: dict(rows=0, distinct=set(), occurrences=0, frames=0))
    maximum = 0
    with (args.results / 'stack-ledger.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            row = json.loads(line)
            stats['stack_rows_within_logs'] += 1
            seen.add(row['key'])
            inv = row['inventory']
            n = len(inv['frames'])
            name = str(n) if inv['kind'] == 'frames' else inv['kind']
            lengths[name]['rows'] += 1
            lengths[name]['distinct'].add(row['key'])
            lengths[name]['occurrences'] += row['occurrences']
            lengths[name]['frames'] += n * row['occurrences']
            stats['frames'] += n * row['occurrences']
            for frame in inv['frames']:
                if 'trace' in frame['fields']:
                    stats['frames_with_trace'] += row['occurrences']
                else:
                    stats['frames_without_trace'] += row['occurrences']
                    chosen.setdefault('location_without_parenthetical', row)
            if row['assignment']:
                tid = row['assignment']['template_id']
                selected[tid] += row['occurrences']
                stats['selected_frames'] += n * row['occurrences']
                if tid in wanted:
                    chosen.setdefault(wanted[tid], row)
                if n == 15 and row['assignment']['selection']['template_tie']:
                    chosen.setdefault('fifteen_frame_tie', row)
                if n == 3 and row['status'] == 'provisional' and row['occurrences'] > 1000:
                    chosen.setdefault('frequent_three_frame_provisional', row)
            if n > maximum:
                maximum = n
                chosen['longest_stack'] = row
    chosen['fifteen_frame_provisional'] = examples['15:provisional']
    chosen['unknown_literal'] = examples['unknown:provisional']
    # Inspect an existing short definition against an unchanged genuine longer
    # unit. The body-only probe is explicitly not a public/eligible assignment.
    package = load_verified(args.selection.parent / selection['artifact_directory'],
                            selection['manifest_sha256'])
    longer = chosen['four_frame_trigger']
    raw = package.parse_file(longer['path'])
    assert sha(raw.source.data) == longer['log_sha256']
    recovery = next(r for r in raw.iter_recoveries()
                    if [e.ordinal for e in r.parents] == longer['provenance']['emission_ordinals'])
    for unit in package.iter_units(raw):
        if unit['provenance']['emission_ordinals'] != longer['provenance']['emission_ordinals']:
            continue
        assert unit['body']['text'] == longer['native_text']
        record = SimpleNamespace(source_family=unit['source_family'], context_kind=unit['context_kind'],
                                 text=unit['body']['text'], pieces=tuple(map(tuple, unit['body']['pieces'])),
                                 contexts={}, continuations=unit['continuations'])
        short = package.matcher.by_id['0b2804538785c71278ea37e7']
        correct = package.matcher.by_id[longer['assignment']['template_id']]
        rules = package.matcher.rules
        stats['cross_length_probe'] = dict(
            log_sha256=longer['log_sha256'], provenance=longer['provenance'],
            recovery=dict(status=recovery.status, structure=recovery.structure,
                          message_spans=[[m.span.start, m.span.end] for m in recovery.messages]),
            one_frame_template_id=short['template_id'], four_frame_template_id=correct['template_id'],
            one_frame_applicable=rules.applies_to_record(short, record),
            four_frame_applicable=rules.applies_to_record(correct, record),
            one_frame_complete_match=rules.match_record(short, record),
            body_only_not_an_assignment=rules.analyze_match_pattern(short['parts'], record.text,
                                                                  pieces=record.pieces),
            public_assignment=package.match(unit)['assignment'])
        assert not stats['cross_length_probe']['one_frame_applicable']
        assert stats['cross_length_probe']['four_frame_applicable']
        assert stats['cross_length_probe']['one_frame_complete_match'] is None
        assert stats['cross_length_probe']['public_assignment']['template_id'] == correct['template_id']
        break
    assert 'cross_length_probe' in stats
    stats['distinct_complete_stack_inputs'] = len(seen)
    stats['lengths'] = {k: dict(v, distinct=len(v['distinct'])) for k, v in lengths.items()}
    stats['selected_definitions'] = len(selected)
    script_templates = [t for t in model['templates'] if 'Script location:' in t['display']]
    stats['published_script_definitions'] = len(script_templates)
    stats['published_head_display_groups'] = len({t['display'].split('Script location:')[0] for t in script_templates})
    paths = {v['sha256']: Path(v['path']) for v in summary['logs']}
    for path in paths.values():
        data = path.read_bytes()
        stats['input_bytes'] += len(data)
        stats['raw_script_markers'] += data.count(b'Script location:')
    assert stats['raw_script_markers'] == sum(summary['tail_kinds'].values())
    failures = read(args.results / 'no-match.json')
    fresh = {(f['log_sha256'], tuple(f['provenance']['emission_ordinals'])): f for f in failures}
    matched_failures = set()
    for manifest_path in sorted((args.task06 / 'generation-a' / 'review').rglob('review-manifest.json')):
        manifest = read(manifest_path)
        shard_path = manifest_path.parent / manifest['log_file']
        shard = shard_path.read_bytes()
        assert sha(shard) == manifest['log_sha256']
        native = paths[manifest['input_log_sha256']].read_bytes()
        assert sha(native) == manifest['input_log_sha256']
        for emission in manifest['emissions']:
            a, b = emission['original_span']
            c, d = emission['shard_span']
            assert native[a:b] == shard[c:d]
            key = (manifest['input_log_sha256'], (emission['ordinal'],))
            assert key in fresh
            matched_failures.add(key)
        stats['review'].append(dict(run_id=manifest['run_id'], manifest=str(manifest_path),
                                   shard=str(shard_path), sha256=sha(shard), bytes=len(shard),
                                   emissions=len(manifest['emissions']), native_bytes_equal=True))
    assert matched_failures == set(fresh)
    for index, row in enumerate(failures, 1):
        chosen['no_match_' + str(index)] = row
    (args.results / 'supplement.json').write_text(json.dumps(stats, indent=2) + '\n', encoding='utf-8')
    (args.results / 'chosen-examples.json').write_text(json.dumps(chosen, indent=2) + '\n', encoding='utf-8')
    lines = ['# Native Script location examples', '',
             'Generated from complete-log shared-matcher replay. Visual code blocks display native bodies; '
             '`chosen-examples.json` retains exact escaped text, parts, byte spans and original provenance. '
             'All frame tables follow native order. Slot spans below are body-relative UTF-8 bytes.', '']
    for name, row in chosen.items():
        lines += ['## ' + name, '',
                  'Input SHA-256: `' + row['log_sha256'] + '`. Emission ordinal(s): `' +
                  str(row['provenance']['emission_ordinals']) + '`. Body span: `' +
                  str(row['body_provenance']['span']) + '`.', '',
                  'Native body:', '', '```text', row['native_text'], '```', '',
                  'Exact escaped body:', '', '```json', json.dumps(row['native_text'], ensure_ascii=True), '```', '']
        assignment = row['assignment']
        if assignment:
            lines += ['Selected `' + assignment['template_id'] + '`; **' + row['status'] +
                      '**, record eligible. Selection: `' + assignment['selection']['reason'] + '`.', '',
                      'Published parts, shown with slot names:', '', '```text']
            display = ''.join(p['text'] if p['kind'] == 'literal' and 'alternatives' not in p else
                              '{' + '|'.join(p['alternatives']) + '}' if p['kind'] == 'literal' else
                              '<' + p['type'] + ':' + p['name'] + '>' for p in row['parts'])
            lines += [display, '```', '', 'Ordered bindings:', '',
                      '| Slot | Type | Exact value | Relative byte span |', '|---|---|---|---|']
            for capture in assignment['regions'][0]['captures']:
                lines.append('| ' + ' | '.join(cell(capture[k]) for k in ('slot_id', 'type', 'value', 'span')) + ' |')
            lines += ['', 'Literal choices: `' + str(assignment['regions'][0]['layout'].get('literal_choices', [])) + '`.', '']
        else:
            lines += ['**no_match**; no selected template, parts or bindings. Native review; '
                      'byte-equality checks against the existing Task 06 shard are in `supplement.json`.', '']
        if row['inventory'] and row['inventory']['frames']:
            lines += ['Every location entry:', '', '| Index | File binding | Line binding | Trace binding |', '|---|---|---|---|']
            for frame in row['inventory']['frames']:
                lines.append('| ' + str(frame['index']) + ' | ' + ' | '.join(
                    cell(frame['fields'][key].get('binding', frame['fields'][key]['accounting']))
                    if key in frame['fields'] else 'not present in native frame'
                    for key in ('file', 'line', 'trace')) + ' |')
            lines += ['']
    (args.results / 'NATIVE_EXAMPLES.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()
