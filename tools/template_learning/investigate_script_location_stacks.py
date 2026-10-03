"""Read complete retained logs through the selected shared package; write ignored evidence.

This is measurement tooling, not a parser, model proposal, or alternate matcher.
The line expression below inventories native Script location tails only. Any
unaccounted tail is reported instead of being silently counted as a valid frame.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

from template_learning.matcher_example import load_verified
from ck3chronicle.pipeline.bindings import bind_captures
from ck3chronicle.pipeline.contracts import materialize_definitions, render


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')


def content_key(unit):
    def region(r):
        return {k: v for k, v in r.items() if k != 'provenance'}
    return digest(json.dumps([
        unit['parser'], unit['source_family'], unit['context_kind'], region(unit['body']),
        {k: region(v) for k, v in unit['contexts'].items()},
        [region(v) for v in unit['continuations']],
    ], sort_keys=True).encode('utf-8', 'surrogateescape'))


FRAME = re.compile(r'file:[ \t]*(?P<file>[^\r\n]+?) (?P<label>near line:|line:) '
                   r'(?P<line>[0-9]+)(?: \((?P<trace>[^\r\n]*)\))?[ \t]*$')


def frames(text):
    marker = 'Script location:'
    if marker not in text:
        return None
    start = text.index(marker) + len(marker)
    tail = text[start:]
    if tail.strip() == 'Unknown':
        return dict(kind='unknown', frames=[])
    found, unparsed, cursor = [], [], start
    for line in tail.splitlines(keepends=True):
        clean = line.strip(' \t\r\n')
        offset = cursor + len(line) - len(line.lstrip(' \t'))
        cursor += len(line)
        if not clean:
            continue
        match = FRAME.fullmatch(clean)
        if match is None:
            unparsed.append(line)
            continue
        fields = {}
        for name in ('file', 'line', 'trace'):
            if match[name] is not None:
                a, b = match.span(name)
                fields[name] = dict(value=match[name], span=[
                    len(text[:offset + a].encode('utf-8', 'surrogateescape')),
                    len(text[:offset + b].encode('utf-8', 'surrogateescape'))])
        found.append(dict(index=len(found), label=match['label'], fields=fields))
    return dict(kind='frames' if not unparsed else 'unparsed', frames=found, unparsed=unparsed)


def values_for(assignment):
    return dict(contract_version='error-contract-v1', template_id=assignment['template_id'],
                regions=[dict(name=r['name'], layout=r['layout'],
                              component_index=r.get('component_index'),
                              bindings=[{k: c[k] for k in ('slot_id', 'type', 'value', 'present')}
                                        for c in r['captures']]) for r in assignment['regions']])


def audit_frames(inventory, assignment):
    if assignment is None:
        return
    captures = assignment['regions'][0]['captures']
    for frame in inventory['frames']:
        for name, field in frame['fields'].items():
            exact = [c for c in captures if c['span'] == field['span']]
            a, b = field['span']
            overlaps = [c for c in captures if c['present'] and c['span'][0] < b and a < c['span'][1]]
            if len(exact) == 1:
                field['binding'] = exact[0]['slot_id']
                field['type'] = exact[0]['type']
                field['accounting'] = 'typed' if exact[0]['type'] == ('PARAM' if name == 'trace' else 'LOCATOR') else 'other_type'
            elif not overlaps:
                field['accounting'] = 'literal'
            else:
                field['accounting'] = 'non_exact_capture'
                field['overlaps'] = overlaps


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--selection', type=Path, required=True)
    cli.add_argument('--inventory', type=Path, required=True)
    cli.add_argument('--task06-inventory', type=Path, required=True)
    cli.add_argument('--date-inventory', type=Path, required=True)
    cli.add_argument('--sample', type=Path, required=True)
    cli.add_argument('--sample-html', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    protected = [args.selection, args.inventory, args.task06_inventory, args.date_inventory,
                 args.sample, args.sample_html]
    selection = json.loads(args.selection.read_text())
    folder = args.selection.parent / selection['artifact_directory']
    protected += list(folder.rglob('*'))
    protected = [p for p in protected if p.is_file()]
    before = {str(p): digest(p.read_bytes()) for p in protected}
    package = load_verified(folder, selection['manifest_sha256'])
    definitions = materialize_definitions(package)
    templates = {t['template_id']: t for t in package.data['templates']}
    inputs = json.loads(args.inventory.read_text())
    assert len(inputs) == len({v['sha256'] for v in inputs})
    task06 = {v['sha256'] for v in json.loads(args.task06_inventory.read_text())}
    dates = {v['sha256'] for v in json.loads(args.date_inventory.read_text())}
    assert task06 | dates <= {v['sha256'] for v in inputs}
    sample = json.loads(args.sample.read_text())['records'][16]
    # Read the saved viewer, including its embedded data; never rerun sampling.
    html = args.sample_html.read_text(encoding='utf-8')
    assert sample['values']['template_id'] in html
    report = dict(selection=selection, inventory=str(args.inventory), logs=[], totals=Counter(),
                  stack_lengths=defaultdict(Counter), task06_stack_lengths=defaultdict(Counter),
                  task06_totals=Counter(), tail_kinds=Counter(), frame_accounting=Counter(),
                  selected_stack_templates=Counter(), saved_sample_verified=False,
                  hashes_before=before, unique_complete_inputs_within_logs=0)
    examples, failures, problems = {}, [], []
    with (args.output / 'stack-ledger.jsonl').open('w', encoding='utf-8') as ledger:
        for number, item in enumerate(inputs, 1):
            raw = package.parse_file(item['path'])
            assert digest(raw.source.data) == item['sha256']
            cursor = 0
            for recovery in raw.iter_recoveries():
                for span in recovery.ordered_spans:
                    assert span.start == cursor
                    cursor = span.end
            assert cursor == len(raw.source.data)
            counts, cache, stack_rows = Counter(), {}, {}
            for unit in package.iter_units(raw):
                if unit['recovery_status'] != 'recovered':
                    counts['unresolved'] += 1
                    problems.append(dict(log=item, provenance=unit['provenance'], kind='unresolved'))
                    continue
                key = content_key(unit)
                fresh = key not in cache
                if fresh:
                    result = package.match(unit)
                    assignment = result['assignment']
                    inv = frames(unit['body']['text'])
                    if inv:
                        audit_frames(inv, assignment)
                    cache[key] = (assignment, inv)
                assignment, inv = cache[key]
                status = assignment['match_status'] if assignment else 'no_match'
                counts[status] += 1
                if not inv and assignment:
                    continue
                row = dict(log_sha256=item['sha256'], path=item['path'], key=key,
                           provenance=unit['provenance'], body_provenance=unit['body']['provenance'],
                           source_family=unit['source_family'], context_kind=unit['context_kind'],
                           native_text=unit['body']['text'], inventory=inv, status=status,
                           assignment=assignment)
                if not assignment and fresh:
                    row['inspection'] = package.match(unit, inspect=True)['inspection']
                    failures.append(row)
                if not inv:
                    continue
                report['tail_kinds'][inv['kind']] += 1
                length = str(len(inv['frames'])) if inv['kind'] == 'frames' else inv['kind']
                report['stack_lengths'][length][status] += 1
                if item['sha256'] in task06:
                    report['task06_stack_lengths'][length][status] += 1
                if fresh:
                    row['occurrences'] = 0
                    stack_rows[key] = row
                    if inv['kind'] == 'unparsed':
                        problems.append(row)
                    if assignment:
                        definition = definitions[assignment['template_id']]
                        assert render(definition, values_for(assignment)) == unit['body']['text']
                        row['template_display'] = templates[assignment['template_id']]['display']
                        row['parts'] = definition['parts']
                        row['parameter_structures'] = definition['parameter_structures']
                    category = length + ':' + status
                    examples.setdefault(category, row)
                    if 'different types (' in row['native_text']:
                        examples.setdefault('comparison:' + length, row)
                stack_rows[key]['occurrences'] += 1
                if assignment:
                    # Bind cached selected spans against every occurrence's own original bytes.
                    assert len(assignment['regions']) == 1
                    bindings = bind_captures(raw.source, unit['body'], assignment['regions'][0]['captures'])
                    report['totals']['stack_bindings_checked'] += len(bindings)
                    report['selected_stack_templates'][assignment['template_id']] += 1
                    for frame in inv['frames']:
                        for field in frame['fields'].values():
                            report['frame_accounting'][field['accounting']] += 1
                    if item['sha256'] == sample['log_sha256'] and unit['body']['text'] == sample['rendered']:
                        assert values_for(assignment) == sample['values']
                        saved_provenance = json.loads(sample['diagnostic']['provenance_json'])
                        if unit['provenance']['emission_ordinals'] == saved_provenance['emission_ordinals']:
                            assert [[b.span.start, b.span.end] for b in bindings] == saved_provenance['regions'][0]['binding_spans']
                            report['saved_sample_verified'] = True
                            examples['saved_sample_17'] = row
            for row in stack_rows.values():
                ledger.write(json.dumps(row, ensure_ascii=True) + '\n')
            report['unique_complete_inputs_within_logs'] += len(cache)
            report['totals'].update(counts)
            if item['sha256'] in task06:
                report['task06_totals'].update(counts)
            assert digest(Path(item['path']).read_bytes()) == item['sha256']
            report['logs'].append(dict(item, bytes=len(raw.source.data), counts=counts,
                                       emissions=len(raw.emissions), unique_inputs=len(cache)))
            write(args.output / 'progress.json', report)
            print(number, len(inputs), item['sha256'], dict(counts), flush=True)
    report['hashes_after'] = {str(p): digest(p.read_bytes()) for p in protected}
    assert report['hashes_after'] == before
    report['tool_sha256'] = digest(Path(__file__).read_bytes())
    write(args.output / 'summary.json', report)
    write(args.output / 'examples.json', examples)
    write(args.output / 'no-match.json', failures)
    write(args.output / 'problems.json', problems)


if __name__ == '__main__':
    main()
