"""Compare fresh/additive assignments on the already-established shared corpus."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.inventory import sha256_file


def read(path):
    return json.loads(path.read_bytes())


def fingerprint(row):
    # Ignore learned assignments but include exact native text, pieces, wrappers,
    # continuations and all occurrence provenance. Order is significant.
    value = {k:row[k] for k in ('source_family','context_kind','native','pieces',
                              'contexts','continuations','native_occurrences')}
    return hashlib.sha256(json.dumps(value,ensure_ascii=True,sort_keys=True,
        separators=(',',':')).encode('ascii')).hexdigest()


def choice(row):
    chosen = row['selected_assignment']
    return dict(template_id=chosen['template_id'] if chosen else None,
                status=chosen['match_status'] if chosen else 'no_match')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('phase', choices=['prepare','compare'])
    cli.add_argument('--fresh-evidence', type=Path, required=True)
    cli.add_argument('--fresh-bundle', type=Path, required=True)
    cli.add_argument('--incremental-bundle', type=Path)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args(); out = args.output
    fresh_native = args.fresh_bundle/'native_evidence.json'
    fresh_manifest = read(args.fresh_bundle/'manifest.json')
    prior = read(args.fresh_evidence/'production-training-ledger.json')
    digest = sha256_file(fresh_native)
    assert digest == fresh_manifest['hashes'][fresh_native.name] == prior['native_evidence_sha256']
    ledger_path = out/'native-comparison-ledger.json'
    if args.phase == 'prepare':
        examples = {}
        for index,(row,count) in enumerate(native_evidence_rows(fresh_native,retain_occurrences=True),1):
            key = row['example_id']; production = prior['examples'][key]
            assert production['occurrences'] == count
            examples[key] = dict(native_sha256=fingerprint(row),occurrences=count,
                                 production=production,fresh=choice(row))
            if index % 20000 == 0:
                print('Authenticated native comparison rows:',index,flush=True)
        assert examples.keys() == prior['examples'].keys()
        write_json(ledger_path,dict(native_evidence_sha256=digest,examples=examples,
                    production_package=prior['package_id'],source_fresh_revision=fresh_manifest['revision_id']))
        return
    ledger = read(ledger_path)
    assert ledger['native_evidence_sha256'] == digest
    incremental = args.incremental_bundle/'native_evidence.json'
    manifest = read(args.incremental_bundle/'manifest.json')
    native_digest = sha256_file(incremental)
    assert native_digest == manifest['hashes'][incremental.name]
    counts = {k:Counter() for k in ('production','fresh','incremental')}
    transitions = {k:Counter() for k in ('production','fresh')}
    edges = {k:{} for k in transitions}; seen = set()
    for index,(row,count) in enumerate(native_evidence_rows(incremental),1):
        key = row['example_id']; before = ledger['examples'][key]
        assert key not in seen; seen.add(key)
        # Shared log hashes are already established. Use the saved contextual
        # message IDs to join outcomes; do not run another input-content audit.
        assert count == before['occurrences'], key
        after = choice(row)
        counts['incremental'][after['status']] += count
        for label in transitions:
            old = before[label]; counts[label][old['status']] += count
            transitions[label][old['status']+' -> '+after['status']] += count
            pair = old['template_id'],after['template_id'],old['status'],after['status']
            edge = edges[label].setdefault(pair,dict(before=pair[0],after=pair[1],before_status=pair[2],
                after_status=pair[3],occurrences=0,messages=0,example=dict(source=row['source_family'],
                    text=row['native'],example_id=key,provenance=row['native_occurrences'][:1])))
            edge['occurrences'] += count; edge['messages'] += 1
        if index % 20000 == 0:
            print('Compared assignment rows:',index,flush=True)
    assert seen == ledger['examples'].keys()
    common = dict(scope='Already-established same 73-log corpus; outcomes joined by saved contextual message IDs and occurrence counts. Training coverage, not independent accuracy.',
        native_evidence_sha256=native_digest,source_candidate_revision=manifest['revision_id'],
        contextual_messages=len(seen),same_contextual_message_ids_and_counts=True)
    for label in transitions:
        name = 'training-corpus-comparison.json' if label=='production' else 'fresh-training-comparison.json'
        write_json(out/name,dict(**common,production_package=ledger['production_package'] if label=='production' else None,
            baseline=label,counts=dict(production=counts[label],candidate=counts['incremental']),
            transitions=transitions[label],edges=list(edges[label].values())))
    write_json(out/'build-history-training-summary.json',dict(**common,counts=counts,transitions=transitions))
    print(json.dumps(dict(counts=counts,transitions=transitions),indent=2))


if __name__ == '__main__':
    main()
