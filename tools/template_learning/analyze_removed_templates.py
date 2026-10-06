"""Trace removed templates through genuine selected matches and exact capture spans.

This is review tooling, not an alternate matcher. Both immutable packages replay
one saved genuine witness for every observed predecessor/successor/scope edge.
Coverage counts are complete; capture-difference observations are witness-based.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.inventory import sha256_file
from template_learning.matcher_example import load_verified
from template_learning.verify_location_candidate import stored_unit


def read(path):
    return json.loads(path.read_bytes())


def raw(text):
    return text.encode('utf-8', 'surrogateescape')


def native_regions(unit):
    return {'body': unit['body']['text'],
            **{k: v['text'] for k, v in unit['contexts'].items()},
            **{'continuation:'+str(i): v['text'] for i, v in enumerate(unit['continuations'])}}


def capture_map(assignment, texts):
    result = {}
    for region in assignment['regions']:
        name = region['name']; data = raw(texts[name])
        labels = ['literal'] * len(data)
        locations = [False] * len(data)
        occupied = set()
        for cap in region['captures']:
            if not cap['present']:
                continue
            a, b = cap['span']
            assert data[a:b] == raw(cap['value']), (name, cap)
            assert not occupied.intersection(range(a, b))
            occupied.update(range(a, b))
            labels[a:b] = [cap['type']] * (b-a)
            location = cap['type'] == 'LOCATOR' or cap['slot_id'].startswith('locations_')
            locations[a:b] = [location] * (b-a)
        result[name] = (labels, locations)
    assert set(result) == set(texts)
    return result


def changes(before, after, texts):
    old, new = capture_map(before, texts), capture_map(after, texts)
    diffs = []
    for name, text in texts.items():
        data = raw(text); a, al = old[name]; b, bl = new[name]
        start = 0
        while start < len(data):
            stop = start + 1
            tag = (a[start], b[start], al[start] or bl[start])
            while stop < len(data) and (a[stop], b[stop], al[stop] or bl[stop]) == tag:
                stop += 1
            if tag[0] != tag[1]:
                value = data[start:stop].decode('utf-8', 'surrogateescape')
                diffs.append(dict(region=name, span=[start, stop], before=tag[0], after=tag[1],
                    location=tag[2], text=value, words=re.findall(r'\w+', value)))
            start = stop
    return diffs


def classify(diffs, repeated):
    diagnostic = [d for d in diffs if d['words'] and not d['location']]
    broader = any(d['before'] == 'literal' for d in diagnostic)
    narrower = any(d['after'] == 'literal' for d in diagnostic)
    if broader and narrower:
        return 'both_broader_and_narrower'
    if broader:
        return 'literal_words_become_slots'
    if narrower:
        return 'slot_words_become_literals'
    if diagnostic:
        return 'slot_types_change'
    if repeated or any(d['location'] for d in diffs):
        return 'location_change_without_diagnostic_word_retyping'
    return 'no_diagnostic_word_retyping'


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence', type=Path, required=True)
    cli.add_argument('--bundle', type=Path, required=True)
    cli.add_argument('--production', type=Path, required=True)
    cli.add_argument('--candidate', type=Path, required=True)
    args = cli.parse_args(); out = args.evidence
    comparison = read(out/'comparison.json'); training = read(out/'training-corpus-comparison.json')
    packages = dict(production=load_verified(args.production, comparison['production']['manifest_sha256']),
                    candidate=load_verified(args.candidate, comparison['candidate']['pin']))
    templates = {label: {t['template_id']: t for t in p.data['templates']} for label, p in packages.items()}
    removed = set(comparison['removed'])
    assert removed == templates['production'].keys() - templates['candidate'].keys()
    rows = []
    needed = defaultdict(list)
    for scope, edges in [('training', training['edges']), ('stored_runs', comparison['edges'])]:
        for edge in edges:
            if edge['before'] not in removed:
                continue
            row = dict(scope=scope, before=edge['before'], after=edge['after'],
                       before_status=edge['before_status'], after_status=edge['after_status'],
                       messages=edge.get('messages', edge.get('distinct_messages')),
                       occurrences=edge['occurrences'])
            key = edge['example']['example_id'] if scope == 'training' else edge['example_key']
            row['witness_key'] = key
            rows.append(row); needed[(scope, key)].append(row)

    def evaluate(unit, targets, provenance):
        results = {label: p.match(unit)['assignment'] for label, p in packages.items()}
        old, new = results['production'], results['candidate']
        texts = native_regions(unit)
        for row in targets:
            assert old['template_id'] == row['before'] and old['match_status'] == row['before_status']
            assert (new['template_id'] if new else None) == row['after']
            assert (new['match_status'] if new else 'no_match') == row['after_status']
            row['source'] = unit['source_family']
            row['provenance'] = provenance
            row['native_regions'] = texts
            row['patterns'] = {label: templates[label][a['template_id']]['display'] if a else None
                               for label, a in results.items()}
            row['captures'] = {label: [{k: r[k] for k in ('name', 'captures', 'layout')} for r in a['regions']]
                               if a else None for label, a in results.items()}
            repeated = bool(new and any(part['kind'] == 'repeat' for part in templates['candidate'][row['after']]['parts']))
            row['repeated_location_tail'] = repeated
            row['changes'] = changes(old, new, texts) if new else []
            row['theme'] = classify(row['changes'], repeated) if new else 'no_complete_match'
            row['same_display'] = row['patterns']['production'] == row['patterns']['candidate']

    native = args.bundle/'native_evidence.json'
    digest = sha256_file(native)
    assert digest == training['native_evidence_sha256'] == read(args.bundle/'manifest.json')['hashes'][native.name]
    pending = {key for scope, key in needed if scope == 'training'}
    for index, (row, count) in enumerate(native_evidence_rows(native), 1):
        key = row['example_id']
        if key in pending:
            unit = dict(parser=packages['candidate'].manifest['parser'], recovery_status='recovered',
                source_family=row['source_family'], source_tag=row['source_family'], context_kind=row['context_kind'],
                body=dict(text=row['native'], pieces=row['pieces']),
                contexts=next(iter(row['contexts'].values()), {}), continuations=row['continuations'])
            evaluate(unit, needed[('training', key)], row['native_occurrences'])
            pending.remove(key)
        if index % 10000 == 0:
            print('Streamed', index, 'genuine messages; training witnesses remaining', len(pending), flush=True)
        if not pending:
            break
    assert not pending
    messages = {r['key']: r for r in read(out/'messages.json')}
    snapshot = Path(read(out/'stored-evidence.json').get('snapshot_directory', out))
    runs = {}
    for (scope, key), targets in needed.items():
        if scope != 'stored_runs':
            continue
        message = messages[key]
        ref = next(r for r in message['references'] if r['kind'] == 'stored')
        run = ref['run_id']
        if run not in runs:
            runs[run] = {r['ordinal']: r for r in read(snapshot/(run+'.json'))['records']}
        unit = stored_unit(packages['candidate'], runs[run][ref['ordinal']])
        assert native_regions(unit) == dict(message['native_regions'])
        evaluate(unit, targets, [ref])
    print('Replayed witnesses:', len(rows), flush=True)

    by_old, by_new = defaultdict(list), defaultdict(set)
    for row in rows:
        by_old[row['before']].append(row)
        if row['after']:
            by_new[row['after']].add(row['before'])
    outgoing = {i: sorted({r['after'] for r in v if r['after']}) for i, v in by_old.items()}
    theme_sets = defaultdict(set)
    for row in rows:
        theme_sets[row['theme']].add(row['before'])
    summary = dict(inventory=comparison['inventory'], removed=len(removed), observed_removed=len(by_old),
        unobserved_removed=sorted(removed-by_old.keys()),
        unique_pairs=len({(r['before'], r['after']) for r in rows}), replayed_witnesses=len(rows),
        destination_templates=len(by_new),
        removed_by_source=Counter(templates['production'][i]['source_family'] for i in removed),
        overlapping_theme_counts={k: len(v) for k, v in theme_sets.items()},
        outgoing_destination_counts=Counter(len(v) for v in outgoing.values()),
        many_to_one_destinations=sum(len(v)>1 for v in by_new.values()),
        removed_with_many_to_one_destination=len(set().union(*(v for v in by_new.values() if len(v)>1))),
        no_production_or_candidate_mutations=True)
    write_json(out/'removed-template-analysis.json', dict(summary=summary,
        method='Complete saved coverage crosswalk across 73 training logs and 20 stored Runs; one exact public-matcher witness per edge per scope. Capture changes are measured on witnesses, not every message. Counts from overlapping scopes are kept separate. A successor means observed selected assignment, not ancestry or semantic equivalence.',
        packages=dict(production=comparison['production'], candidate=comparison['candidate']),
        native_evidence_sha256=digest, templates=templates,
        incoming={k: sorted(v) for k, v in by_new.items()}, outgoing=outgoing, witnesses=rows))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
