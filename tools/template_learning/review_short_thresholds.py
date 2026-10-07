"""Isolated short-form discovery experiment on retained genuine learner evidence.

This is not a published model or a replacement production-coverage comparison.
Only comparable() is varied; inference, ordering, boundaries and guards remain
those of the identified learner. Runtime matching does not use this threshold.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from template_learning import clustering
from template_learning.records import SequenceRecord, identity
from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.learner_loader import implementation_identity
from template_learning.matching_primitives import display_pattern
from template_learning.matching_defaults import match_pattern


def record(row):
    return SequenceRecord(row['source_family'], row['native'], tuple(map(tuple, row['pieces'])),
        row['context_kind'], row['contexts'], row['native_occurrences'], tuple(row['continuations']))


def length(tokens):
    return sum(t[0] != 'quoted-value' for t in tokens)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase', choices=['extract', 'run'])
    p.add_argument('--bundle', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--application-source', type=Path, required=True)
    p.add_argument('--policy', choices=['fixed', 'gentle', 'lower'], default='fixed')
    a = p.parse_args(); a.output.mkdir(parents=True, exist_ok=True)
    implementation = implementation_identity(Path(__file__).parent, application_source=a.application_source)
    if a.phase == 'extract':
        seen = set(); counts = Counter(); kept = 0
        with (a.output/'short-records.jsonl').open('w', encoding='utf-8') as f:
            for i, (row, occurrences) in enumerate(native_evidence_rows(a.bundle/'native_evidence.json'), 1):
                counts['contextual_rows'] += 1; counts['occurrences'] += occurrences
                r = record(row); tokens = clustering.learning_tokens(r)
                # Include the existing <=2-unit cases too: their later inferred
                # fields can affect regrouping. Never invent shorter messages.
                if length(tokens) <= 8:
                    counts['short_contextual_rows'] += 1
                    counts['short_occurrences'] += occurrences
                    key = identity(r.key)
                    if key not in seen:
                        seen.add(key); kept += 1
                        f.write(json.dumps(dict(row=row, count=occurrences, tokens=tokens), ensure_ascii=True)+'\n')
                if i % 10000 == 0:
                    print('Scanned', i, 'short underlying messages', kept, flush=True)
        write_json(a.output/'scope.json', dict(implementation=implementation, counts=counts,
            underlying_short_messages=kept, bundle=str(a.bundle.resolve()),
            native_evidence_sha256=json.loads((a.bundle/'manifest.json').read_bytes())['hashes']['native_evidence.json'],
            scope='All <=8 non-quoted-value comparison-unit messages from the retained 73-log evidence; initial discovery plus all refinement stages. Not an incremental model build.',
            occurrence_note='One native provenance witness per underlying message; repetition counts are not used by clustering/inference. No support-status or runtime-coverage claim.'))
        return
    scope = json.loads((a.output/'scope.json').read_bytes())
    assert implementation == scope['implementation'], 'learner changed after extraction'
    pools = defaultdict(list)
    with (a.output/'short-records.jsonl').open(encoding='utf-8') as f:
        for line in f:
            r = record(json.loads(line)['row']); pools[r.source_family].append(r)
    original = clustering.comparable
    curves = dict(gentle={3:.68, 4:.69, 5:.70, 6:.71}, lower={3:.60, 4:.63, 5:.66, 6:.69})
    calls = Counter(); newly_admitted = {}; templates = []; reviews = []
    potential_sources = defaultdict(set)
    baseline = json.loads((a.output/'fixed.json').read_bytes()) if a.policy!='fixed' else None
    active_source = None
    def varied(left, right, threshold):
        n = max(length(left), length(right))
        target = min(threshold, curves.get(a.policy, {}).get(n, threshold))
        before = original(left, right, threshold)
        after = original(left, right, target)
        if a.policy=='fixed':
            for name, curve in curves.items():
                if original(left,right,min(threshold,curve.get(n,threshold))) != before:
                    potential_sources[name].add(active_source)
        calls['all'] += 1
        if after and not before:
            calls['new_admissions'] += 1
            key = identity((left, right))
            newly_admitted[key] = dict(left=left, right=right, score=clustering.sequence_similarity(left,right), threshold=target)
        return after
    clustering.comparable = varied
    try:
        for source, records in sorted(pools.items()):
            if baseline is not None and source not in baseline['potential_sources'].get(a.policy,[]):
                templates.extend(t for t in baseline['templates'] if t['source']==source)
                reviews.extend(r for r in baseline['review'] if r.get('source')==source)
                continue
            active_source = source
            print(a.policy, source, len(records), 'messages', flush=True)
            review = []
            clusters = clustering.cluster_source_records(source, records, .72, review=review)
            for c in clusters:
                assert not c.failures, (source,c.failures)
                for r in c.records:
                    assert match_pattern(c.parts, r.text, pieces=r.pieces) is not None, r.key
                templates.append(dict(template_id=c.template_id, source=source, display=display_pattern(c.parts),
                    members=sorted(identity(r.key) for r in c.records),
                    slots=[dict(name=p['name'], type=p['type'], values=p['observed_values']) for p in c.parts if p['kind']=='slot'],
                    examples=[dict(text=r.text, record_id=identity(r.key)) for r in c.records[:3]]))
            reviews.extend(review)
    finally:
        clustering.comparable = original
    write_json(a.output/(a.policy+'.json'), dict(policy=a.policy, thresholds=curves.get(a.policy, {}),
        default_threshold=.72, calls=calls, newly_admitted=list(newly_admitted.values()),
        templates=templates, review=reviews, potential_sources={k:sorted(v) for k,v in potential_sources.items()},
        reused_sources=sorted(set(pools)-set(baseline['potential_sources'].get(a.policy,[]))) if baseline else [],
        learner_identity=implementation['sha256']))
    print('DONE', a.policy, len(templates), 'templates', dict(calls), flush=True)


if __name__ == '__main__':
    main()
