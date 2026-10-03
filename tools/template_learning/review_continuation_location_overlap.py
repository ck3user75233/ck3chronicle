"""Audit existing recovery boundaries against location markers in genuine logs.

Read-only research using the verified package parser, without new recovery rules.
Counts recovery units, messages, and original emissions separately.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from template_learning.inventory_location_markers import MARKER, SENTINEL
from template_learning.matcher_example import load_verified


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--inventory', type=Path, required=True)
    cli.add_argument('--package', type=Path, required=True)
    cli.add_argument('--manifest-sha256', required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    inventory = json.loads(args.inventory.read_text(encoding='utf-8'))
    package = load_verified(args.package, args.manifest_sha256)
    current = Path(__file__).parent / 'parsers' / 'v1_7' / 'parser.py'
    assert current.read_bytes() == (args.package / 'parser.py').read_bytes()
    rules = json.loads(Path(__file__).with_name('owner_rules.json').read_text(encoding='utf-8'))
    recorded_rules = json.loads((args.package / 'owner_rules.json').read_text(encoding='utf-8'))
    assert rules['continuation_structures'] == recorded_rules['continuation_structures']
    totals, structures, examples, logs, cross_groups = Counter(), {}, {}, [], []
    for number, item in enumerate(inventory['inputs'], 1):
        raw = package.parse_file(item['snapshot'])
        assert hashlib.sha256(raw.source.data).hexdigest() == item['sha256']
        totals['emissions'] += len(raw.emissions)
        cursor = 0
        for recovery in raw.iter_recoveries():
            parents = recovery.parents
            assert [e.ordinal for e in parents] == list(range(cursor, cursor + len(parents)))
            cursor += len(parents)
            key = recovery.structure or 'unresolved'
            row = structures.setdefault(key, dict(units=0, emissions=0, messages=0,
                attached_entries=0, marker_units=0, markers=Counter(), unavailable=Counter(),
                message_counts=Counter(), entry_counts=Counter(), sources=Counter()))
            row['units'] += 1
            row['emissions'] += len(parents)
            row['messages'] += len(recovery.messages)
            row['message_counts'][len(recovery.messages)] += 1
            entries = sum(len(m.continuations) for m in recovery.messages)
            row['attached_entries'] += entries
            row['entry_counts'][entries] += 1
            row['sources'][recovery.parent.source_tag] += 1
            hits = []
            for parent in parents:
                body = raw.read_bytes(parent.body_span)
                for match in MARKER.finditer(body):
                    label = match.group().rstrip(b' \t').decode('ascii')
                    row['markers'][label] += 1
                    tail = body[match.end():].split(b'\n', 1)[0].rstrip(b'\r')
                    if SENTINEL.match(tail):
                        row['unavailable'][label + ' ' + tail.decode('utf-8', 'surrogateescape')] += 1
                    hits.append(dict(emission_ordinal=parent.ordinal, marker=label,
                        span=[parent.body_span.start + match.start(), parent.body_span.start + match.end()]))
            row['marker_units'] += bool(hits)
            example_key = key + ('/markers' if hits else '/no-markers')
            if example_key not in examples or entries:
                example = dict(log_sha256=item['sha256'], path=item['snapshot'],
                    structure=recovery.structure, status=recovery.status, reason=recovery.reason,
                    original_emissions=[dict(ordinal=e.ordinal, source=e.source_tag,
                        span=[e.span.start, e.span.end], text=e.decoded_text) for e in parents],
                    messages=[dict(text=m.text, continuations=[e.message.text for e in m.continuations])
                              for m in recovery.messages], marker_mentions=hits)
                examples.setdefault(example_key, example)
                if entries:
                    cross_groups.append(example)
            totals['recovery_units'] += 1
            totals['messages'] += len(recovery.messages)
        assert cursor == len(raw.emissions)
        logs.append(dict(sha256=item['sha256'], emissions=len(raw.emissions)))
        if number % 10 == 0:
            print(number, 'logs checked;', totals['recovery_units'], 'recovery units', flush=True)
    result = dict(package=str(args.package), manifest_sha256=args.manifest_sha256,
        parser_sha256=hashlib.sha256(current.read_bytes()).hexdigest(),
        current_parser_identical=True, current_continuation_declarations_identical=True,
        cross_emission_rule=package.parser.CROSS_EMISSION_RULES,
        learner_continuation_declarations=rules['continuation_structures'],
        totals=totals, structures=structures, examples=examples,
        cross_emission_groups=cross_groups, logs=logs,
        limitations=['Marker mentions are inventory probes, not slot assignments.',
                    'Observed counts do not establish future exhaustiveness.',
                    'No parser, learner, matcher, model, source log or stored Run was changed.'])
    args.output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(dict(totals=totals, structures=structures)), flush=True)


if __name__ == '__main__':
    main()
