"""Inspect native path ranges and captures from a slash-separated parser bundle."""
import argparse
from collections import Counter
import json
from pathlib import Path

from template_learning.artifacts import load_bundle
from template_learning.inspect_incremental_learning import native_evidence_rows
from template_learning.literal_guidance import guided_piece_indices
from template_learning.patterns import path_piece_ranges, location_piece_ranges, literal_anchor_indices, filename_sequence
from template_learning.records import SequenceRecord
from template_learning.parsers import load_parser, reference_from_manifest


def native_key(row):
    # Context IDs include raw pieces and therefore change across parser versions.
    return (row['source_family'], row['native'], tuple(sorted(
        tuple(sorted((name, value['text']) for name, value in context.items()))
        for context in row['contexts'].values())))


def inspect(bundle, output, baseline=None):
    model, _ = load_bundle(bundle)
    parser = load_parser(reference_from_manifest(bundle / 'parser-manifest.json')).implementation
    counts, examples, failures = Counter(), [], []
    previous_paths = {}
    if baseline:
        load_bundle(baseline)
        for row, _ in native_evidence_rows(baseline / 'native_evidence.json'):
            matches = row['matches']
            previous_paths[native_key(row)] = {
                tuple(c['span']) for m in matches for c in m['captures']
                if c['type'] == 'LOCATOR' and c['value'] and '/' in c['value']}
    for row, occurrences in native_evidence_rows(bundle / 'native_evidence.json'):
        pieces = tuple(tuple(p) for p in row['pieces'])
        source = parser.Source('saved native message verification', row['native'].encode('utf-8', 'surrogateescape'))
        actual = tuple((p.kind, p.text) for p in parser.lexical_pieces(source, parser.Span(0, len(source.data))))
        if actual != pieces:
            raise ValueError('Saved native pieces disagree with the selected parser artifact.')
        counts['evidence_rows'] += 1
        counts['message_occurrences'] += occurrences
        offsets = [0]
        for _, text in pieces:
            offsets.append(offsets[-1] + len(text.encode('utf-8', 'surrogateescape')))
        locations = set(location_piece_ranges(pieces))
        if baseline:
            expected = previous_paths.pop(native_key(row))
            actual = {(offsets[a], offsets[b]) for a, b in locations}
            counts['previous_path_ranges_checked'] += len(expected)
            if expected - actual:
                failures.append(dict(source=row['source_family'], native=row['native'],
                    missing_previous_ranges=sorted(expected - actual), occurrences=occurrences))
        record = SequenceRecord(row['source_family'], row['native'], pieces)
        anchors = set(literal_anchor_indices(record))
        guides = set(guided_piece_indices(pieces))
        matches = [('message', m) for m in row['matches']]
        for a, b in path_piece_ranges(pieces):
            counts['adjacent_slash_sequences'] += occurrences
            if not any(x <= a and b <= y for x, y in locations):
                counts['sequences_not_recognized_as_locations'] += occurrences
        for a, b in sorted(locations):
            is_path = any(t == '/' for _, t in pieces[a:b]) or filename_sequence(pieces[a:b])
            counts['recognized_location_occurrences'] += occurrences
            if is_path:
                counts['recognized_path_occurrences'] += occurrences
            indices = set(range(a, b))
            assert not indices & anchors
            if is_path and indices & guides:
                counts['paths_containing_default_words'] += occurrences
            span = [offsets[a], offsets[b]]
            value = ''.join(t for _, t in pieces[a:b])
            captures = []
            for region, match in matches:
                region_span = [0, offsets[-1]]
                if not (region_span[0] <= span[0] and span[1] <= region_span[1]):
                    continue
                exact = [c for c in match['captures'] if c['type'] == 'LOCATOR' and c['span'] == span and c['value'] == value]
                if not exact:
                    failures.append(dict(source=row['source_family'], native=row['native'], span=span,
                        template_id=match['template_id'], occurrences=occurrences))
                captures.extend(exact)
                counts['checked_candidate_location_captures'] += 1
                if is_path:
                    counts['checked_candidate_path_captures'] += 1
            if len(examples) < 25:
                examples.append(dict(source=row['source_family'], native=row['native'], pieces=pieces,
                    location_piece_range=[a, b], span=span, value=value, captures=captures,
                    first_occurrence=row['native_occurrences'][0]))
    if baseline and previous_paths:
        raise ValueError('Baseline and new bundle do not contain the same native messages/contexts.')
    result = dict(revision=model['revision_id'], parser=model['parser'], counts=counts,
        failures=failures, examples=examples,
        scope='All saved native rows and every matching candidate location capture; filename and line fields retain original pieces, never directory-name rules.')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=True, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(counts=counts, failures=len(failures))))
    if failures:
        raise SystemExit('Native candidate path-capture failures require inspection.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--baseline-bundle', type=Path)
    a = p.parse_args()
    inspect(a.bundle, a.output, a.baseline_bundle)
