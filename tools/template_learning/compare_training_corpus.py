"""Compare genuine training-message coverage without changing stored Runs."""
import argparse
from collections import Counter
import json
from pathlib import Path

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.inventory import sha256_file
from template_learning.matcher_example import load_verified


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('phase', choices=['production', 'compare'])
    cli.add_argument('--bundle', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--package', type=Path)
    cli.add_argument('--pin')
    cli.add_argument('--production-ledger', type=Path)
    cli.add_argument('--parser-correspondence', type=Path, help='Required combined-package genuine parser correspondence receipt.')
    args = cli.parse_args()
    manifest = json.loads((args.bundle/'manifest.json').read_text())
    path = args.bundle/'native_evidence.json'
    digest = sha256_file(path)
    assert digest == manifest['hashes'][path.name]
    if args.phase == 'production':
        package = load_verified(args.package, args.pin)
        assert package.manifest['parser'] == manifest['parser']
        counts, examples = Counter(), {}
        for index, (row, count) in enumerate(native_evidence_rows(path), 1):
            assert len(row['contexts']) <= 1
            unit = dict(parser=package.manifest['parser'], recovery_status='recovered',
                source_family=row['source_family'], source_tag=row['source_family'],
                context_kind=row['context_kind'],
                body=dict(text=row['native'], pieces=row['pieces']),
                contexts=next(iter(row['contexts'].values()), {}), continuations=row['continuations'])
            selected = package.match(unit)['assignment']
            status = selected['match_status'] if selected else 'no_match'
            examples[row['example_id']] = dict(occurrences=count, status=status,
                template_id=selected['template_id'] if selected else None)
            counts[status] += count
            if index % 10000 == 0:
                print('Production corpus messages:', index, flush=True)
        write_json(args.output, dict(package_id=package.manifest['package_id'], pin=args.pin,
            native_evidence_sha256=digest, counts=counts, examples=examples))
    else:
        prior = json.loads(args.production_ledger.read_text())
        correspondence = None
        if args.parser_correspondence:
            correspondence = json.loads(args.parser_correspondence.read_bytes())
            if not args.package or not args.pin:
                raise ValueError('parser correspondence requires the actual candidate package and external pin')
            candidate = load_verified(args.package,args.pin)
            assert correspondence['status']=='passed'
            assert correspondence['packages']['production']['package_id']==prior['package_id']
            assert correspondence['packages']['production']['manifest_sha256']==prior['pin']
            assert correspondence['packages']['candidate']['parser']==manifest['parser']
            assert correspondence['packages']['candidate']['package_id']==candidate.manifest['package_id']
            assert correspondence['packages']['candidate']['manifest_sha256']==args.pin
            assert candidate.manifest['source_manifest_sha256']==sha256_file(args.bundle/'manifest.json')
            assert set(correspondence['training_hashes'])=={r['sha256'] for r in candidate.data['training_evidence']}
            assert set(correspondence['training_hashes']) <= {r['sha256'] for r in correspondence['logs'] if r['status']=='passed'}
        elif manifest['parser']['version'] != 'ck3-lossless-v1.7':
            raise ValueError('changed parser requires genuine input correspondence receipt')
        # Saved assignments legitimately change after a learner correction.
        # Join the previously established same-corpus evidence by native message
        # identity and occurrence count, not the whole assignment-bearing file.
        counts, transitions, edges, seen = Counter(), Counter(), {}, set()
        for row, count in native_evidence_rows(path):
            key = row['example_id']; seen.add(key)
            old = prior['examples'][key]
            assert old['occurrences'] == count
            chosen = row['selected_assignment']
            status = chosen['match_status'] if chosen else 'no_match'
            identifier = chosen['template_id'] if chosen else None
            counts[status] += count
            transitions[old['status']+' -> '+status] += count
            pair = old['template_id'], identifier, old['status'], status
            edge = edges.setdefault(pair, dict(before=pair[0], after=pair[1],
                before_status=pair[2], after_status=pair[3], occurrences=0, messages=0,
                example=dict(source=row['source_family'], text=row['native'],
                             example_id=key, provenance=row['native_occurrences'])))
            edge['occurrences'] += count
            edge['messages'] += 1
        assert seen == set(prior['examples'])
        write_json(args.output, dict(scope='Complete recovered contextual messages in the exact 73 training logs; training coverage, not independent accuracy.',
            production_package=prior['package_id'], source_candidate_revision=manifest['revision_id'],
            production_ledger_sha256=sha256_file(args.production_ledger),
            native_evidence_sha256=digest, contextual_messages=len(seen),same_contextual_message_ids_and_counts=True,
            parser_correspondence_sha256=sha256_file(args.parser_correspondence) if correspondence else None,
            counts=dict(production=prior['counts'], candidate=counts), transitions=transitions,
            edges=list(edges.values())))
        print(json.dumps(dict(messages=len(seen), counts=counts, transitions=transitions), indent=2))


if __name__ == '__main__':
    main()
