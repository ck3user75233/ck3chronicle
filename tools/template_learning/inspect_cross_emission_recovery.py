"""Verify the new parser against complete native inputs and a prior native census.

No training, log mutation, model promotion or database access. Output is external
review evidence. The prior census supplies independently established block ranges.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile

from template_learning.parsers import load_parser, reference_from_manifest


def span(value):
    return [value.start, value.end]


def signature(recovery):
    return (recovery.status, recovery.structure, recovery.reason,
            [span(m.span) for m in recovery.messages],
            [span(s) for s in recovery.shared_spans],
            [span(s) for s in recovery.unresolved_spans])


def inspect(inputs, census, old_manifest, new_manifest, output):
    expected = json.loads(census.read_text(encoding='utf-8'))
    old = load_parser(reference_from_manifest(old_manifest))
    new = load_parser(reference_from_manifest(new_manifest))
    declaration = json.loads(new_manifest.with_name('recovery_rules.json').read_text(encoding='utf-8'))
    assert new.implementation.CROSS_EMISSION_RULES == declaration
    counts = Counter()
    title_counts = Counter()
    files, cases = [], []
    seen_bodies = set()
    for number, record in enumerate(expected['files'], 1):
        path = inputs / record['path']
        data = path.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        assert sha == record['sha256'], path
        before = old.parse_bytes(data, source_name=str(path.resolve()))
        after = new.parse_bytes(data, source_name=str(path.resolve()))
        assert len(before.emissions) == len(after.emissions)
        expected_cases = {c['opening']['ordinal']: c for c in expected['cases'] if c['log'] == sha}
        found = set()
        cursor = 0
        rebuilt = hashlib.sha256()
        local = Counter()
        for a, b in zip(before.emissions, after.emissions):
            assert (span(a.span), span(a.header_span), span(a.body_span), a.source_tag,
                    a.source_family, a.timestamp, a.level, a.start_line, a.end_line) == (
                    span(b.span), span(b.header_span), span(b.body_span), b.source_tag,
                    b.source_family, b.timestamp, b.level, b.start_line, b.end_line)
            body = after.read_bytes(b.body_span)
            digest = hashlib.sha256(body).digest()
            if digest not in seen_bodies:
                seen_bodies.add(digest)
                pa, pb = a.pieces, b.pieces
                assert [(p.kind, p.text, span(p.span)) for p in pa] == [(p.kind, p.text, span(p.span)) for p in pb]
                assert b''.join(after.read_bytes(p.span) for p in pb) == body
        for recovery in after.iter_recoveries():
            for s in recovery.ordered_spans:
                assert s.start == cursor
                rebuilt.update(after.read_bytes(s))
                cursor = s.end
            local['messages'] += len(recovery.messages)
            local['unresolved'] += recovery.status != 'recovered'
            if recovery.continuation_parents:
                expected_case = expected_cases[recovery.parent.ordinal]
                found.add(recovery.parent.ordinal)
                assert recovery.status == 'recovered' and recovery.reason is None
                assert len(recovery.messages) == 1
                message = recovery.messages[0]
                assert span(message.span) == expected_case['opening']['body_span']
                assert len(message.continuations) == len(expected_case['entries'])
                assert [e.ordinal for e in recovery.parents] == [expected_case['opening']['ordinal']] + [
                    e['emission']['ordinal'] for e in expected_case['entries']]
                values = []
                for entry, witness in zip(message.continuations, expected_case['entries']):
                    assert span(entry.message.span) == witness['emission']['body_span']
                    assert span(entry.prefix_span) == witness['reference']['span']
                    assert span(entry.value_span) == witness['title_span']
                    value = after.read_text(entry.value_span)
                    assert value == witness['title']
                    assert after.read_text(entry.prefix_span) == expected_case['reference']['text']
                    values.append(dict(value=value, span=span(entry.value_span)))
                title_counts[len(values)] += 1
                local['groups'] += 1
                local['supporting_entries'] += len(values)
                cases.append(dict(sha256=sha, opening_line=recovery.parent.start_line,
                    emission_ordinals=[e.ordinal for e in recovery.parents], values=values))
            else:
                original = before.emissions[recovery.parent.ordinal].recovery
                assert signature(recovery) == signature(original), (path, recovery.parent.start_line)
                local['unchanged_local_recoveries'] += 1
        assert found == set(expected_cases)
        assert cursor == len(data) and rebuilt.hexdigest() == sha
        old_count = sum(len(e.recovery.messages) for e in before.emissions)
        assert old_count - local['messages'] == local['supporting_entries']
        local['old_messages'] = old_count
        local['emissions'] = len(after.emissions)
        counts.update(local)
        files.append(dict(path=str(path), sha256=sha, **local))
        print(f'{number}/{len(expected["files"])} complete logs: {counts["groups"]} groups, '
              f'{counts["supporting_entries"]} supporting entries', flush=True)

    # Exercise actual consumer boundaries on both complete affected logs.
    from ck3chronicle.pipeline.raw_input import iter_diagnostics
    from ck3chronicle.pipeline.bindings import bind_captures
    from ck3chronicle.pipeline.domain import ByteSpan, Capture
    from template_learning.inventory import ProtectedLog
    from template_learning.incremental_template_registry import feature_from_log, validate_feature
    consumer_results = []
    for name in sorted({c['path'] for c in expected['cases']}):
        path = inputs / name
        raw = new.parse_file(path)
        sha = hashlib.sha256(raw.source.data).hexdigest()
        wanted = [c for c in expected['cases'] if c['log'] == sha]
        openings = {c['opening']['ordinal'] for c in wanted}
        supporting = {e['emission']['ordinal'] for c in wanted for e in c['entries']}
        emitted = set()
        grouped = []
        for diagnostic in iter_diagnostics(raw):
            emitted.add(diagnostic.emission_ordinal)
            if getattr(diagnostic, 'continuations', ()):
                grouped.append(diagnostic)
                for i, entry in enumerate(diagnostic.continuations):
                    value = raw.read_text(entry.value_span)
                    relative = ByteSpan(entry.value_span.start-entry.body.span.start,
                                        entry.value_span.end-entry.body.span.start)
                    # The binding mechanics are exercised using the observed range;
                    # this is not a model match or parser-assigned PARAM type.
                    bound = bind_captures(raw, entry.body, (Capture('title', 'PARAM', value, relative),),
                        template_id='native-range-verification', region_name=f'continuations[{i}]')
                    assert bound[0].span == entry.value_span
        assert {d.emission_ordinal for d in grouped} == openings
        assert not emitted & supporting
        stat = path.stat()
        evidence = ProtectedLog(sha, 'protected', path, sha, stat.st_size, stat.st_mtime_ns)
        feature = feature_from_log(evidence, parser=new)
        validate_feature(feature, sha, parser=new)
        deferred = [r for r in feature['evidence_stats']['unresolved_emissions'] if r.get('recovery_status') == 'recovered']
        assert {r['emission_ordinal'] for r in deferred} == openings
        assert sum(len(r['components'])-1 for r in deferred) == len(supporting)
        learnt_ordinals = {o['emission_ordinal'] for r in feature['records'] for o in r['native_occurrences']}
        assert not learnt_ordinals & (openings | supporting)
        for r in deferred:
            assert r['text'].encode('utf-8','surrogateescape') == raw.bytes_between(*r['span'])
            for component in r['components']:
                assert component['text'].encode('utf-8','surrogateescape') == raw.bytes_between(*component['span'])
        # Serialize/reload one complete affected input, including the log stream.
        if not consumer_results:
            with tempfile.TemporaryDirectory(dir=output) as folder:
                debug = Path(folder) / 'raw.json'
                raw.save_debug(debug)
                replay = new.load_debug(debug)
                assert [(signature(r), [e.ordinal for e in r.parents]) for r in replay.iter_recoveries()] == [
                    (signature(r), [e.ordinal for e in r.parents]) for r in raw.iter_recoveries()]
        consumer_results.append(dict(path=str(path), pipeline_groups=len(grouped),
            learner_deferred_groups=len(deferred), title_capture_ranges=len(supporting),
            feature_roundtrip='passed', duplicate_entry_diagnostics=0))
        print(f'Consumer replay passed: {name}', flush=True)
    result = dict(old_parser=old.reference.to_dict(), new_parser=new.reference.to_dict(),
        counts=dict(counts), titles_per_group=dict(title_counts), files=files, cases=cases,
        distinct_body_lexical_comparisons=len(seen_bodies), consumers=consumer_results,
        exact_complete_input_reconstruction=True, debug_reload=True,
        limitations=['No native absent/mismatched/truncated title lists occur in this corpus.',
                    'Grouped model inference/classification remains a separate learner contract; groups are retained for review.'])
    (output / 'verification.json').write_text(json.dumps(result, indent=2, ensure_ascii=True)+'\n', encoding='utf-8')
    return result


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--inputs', type=Path, required=True)
    cli.add_argument('--census', type=Path, required=True)
    cli.add_argument('--old-manifest', type=Path, required=True)
    cli.add_argument('--new-manifest', type=Path, required=True)
    cli.add_argument('--output-dir', type=Path, required=True)
    args = cli.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = inspect(args.inputs, args.census, args.old_manifest, args.new_manifest, args.output_dir)
    print(json.dumps(result['counts'], indent=2))


if __name__ == '__main__':
    main()
