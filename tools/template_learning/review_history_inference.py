"""Trace history inference from retained genuine evidence, without editing artifacts."""
import argparse
import json
from pathlib import Path
import sys


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--without-history-constructions', action='store_true')
    cli.add_argument('--expect-literals', action='store_true')
    cli.add_argument('--inventory-model', type=Path, help='Inventory other adjacent KEY layouts in a retained model.')
    cli.add_argument('--release-file', type=Path, help='Trace an authenticated immutable learner release.')
    args = cli.parse_args()
    release=None
    if args.release_file:
        from template_learning.learner_loader import authenticate
        release=json.loads(args.release_file.read_bytes())
        authenticate(release['folder'],release['manifest_sha256'])
        for name in list(sys.modules):
            if name=='template_learning' or name.startswith('template_learning.'):
                del sys.modules[name]
        sys.path.insert(0,release['folder'])
    # Controlled ablation before importing consumers/caches of these rules.
    from template_learning.owner_rules import OWNER_RULES
    removed = []
    if args.without_history_constructions:
        removed = [d['id'] for d in OWNER_RULES['constructions']
                   if d['id'] in {'character-history-after-death', 'character-history-before-birth'}]
        OWNER_RULES['constructions'][:] = [d for d in OWNER_RULES['constructions'] if d['id'] not in removed]
    from template_learning import clustering as c
    from template_learning.patterns import derive_pattern, inference_units
    from template_learning.records import SequenceRecord
    from template_learning.matching_primitives import display_pattern
    from template_learning.evidence_serialization import write_json
    rows = [r for r in json.loads(args.evidence.read_bytes()) if r['history']]
    records = [SequenceRecord(r['source'], r['text'], tuple(map(tuple, r['pieces'])),
                             context_kind=r['context_kind'], contexts=r['contexts'],
                             continuations=tuple(r['continuations'])) for r in rows]
    hypotheses = []
    parts, failures = derive_pattern(records, records[0], hypotheses=hypotheses)
    review = []
    clusters = c.cluster_source_records(records[0].source_family, records, .72, review=review)
    result = dict(release=release, removed_constructions=removed, messages=len(rows),
                  occurrences=sum(r['occurrences'] for r in rows),
                  initial=dict(display=display_pattern(parts), parts=parts, failures=failures,
                               hypotheses=hypotheses),
                  inputs=[dict(text=r.text, comparison=c.learning_tokens(r),
                               inference=inference_units(r)) for r in records],
                  final=[dict(display=display_pattern(t.parts), members=len(t.records),
                              failures=t.failures, inference_refinements=t.refinements) for t in clusters],
                  review=review)
    if args.inventory_model:
        model=json.loads(args.inventory_model.read_bytes())
        inventory=[]
        for template in model['templates']:
            fields=template['parts']
            for i in range(len(fields)-2):
                left,gap,right=fields[i:i+3]
                if (left.get('type') in {'KEY','OPTIONAL_KEY'}
                        and gap.get('kind')=='literal' and gap['text'].isspace()
                        and right.get('type') in {'KEY','OPTIONAL_KEY'}):
                    inventory.append(dict(template_id=template['template_id'], display=template['display'],
                        slots=[dict(name=p['name'],values=p['observed_values']) for p in (left,right)],
                        alphabetic_values_only=all(v.isalpha() for p in (left,right) for v in p['observed_values'])))
        result['adjacent_key_inventory']=inventory
        result['inventory_model']=str(args.inventory_model)
    if args.expect_literals:
        assert len(clusters) == 2, result['final']
        for cluster in clusters:
            assert not cluster.failures
            assert all(r.text.split(' has history ', 1)[1].split('. File location', 1)[0]
                       in display_pattern(cluster.parts) for r in cluster.records)
    from template_learning.refinement_history import encode_history
    encode_history(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_json(args.output, result)
    print(json.dumps(dict(messages=len(rows), initial=result['initial']['display'],
                          final=[t['display'] for t in result['final']]), ensure_ascii=True))


if __name__ == '__main__':
    main()
