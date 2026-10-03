"""Disposable learner experiment on genuine stored Runs and protected logs.

The snapshot phase uses SQLite only for a consistent backup. Stored evidence is
read through HandlerClient. Builds use immutable learner releases and receipts.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import time
import tomllib


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True), encoding='utf-8')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def snapshot(root, output, inventory_path, training_path):
    from ck3chronicle.pipeline.request_handler import HandlerClient, COMPLETED
    output.mkdir(parents=True, exist_ok=False)
    production = {str(p.relative_to(root)): sha(p) for p in
        [root/'models/selection.json', root/'models/catalog.json', root/'learners/catalog.json']}
    save(output/'production-before.json', production)
    source_path = root / tomllib.loads((root/'config.toml').read_text())['watcher']['database']
    database = output/'unchanged.sqlite3'
    source = sqlite3.connect(source_path.resolve().as_uri() + '?mode=ro', uri=True)
    target = sqlite3.connect(database)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()
    before = sha(database)
    inventory = json.loads(inventory_path.read_text())
    by_hash = {row['sha256']: row for row in inventory['inputs']}
    training = json.loads(training_path.read_text())
    for row in training:
        assert sha(Path(row['snapshot'])) == row['sha256']
    save(output/'inputs.json', training)
    client = HandlerClient(database)
    def read(op, **args):
        result = client.result(client.submit(op, args))
        if result.status != COMPLETED:
            raise RuntimeError((op, result.error))
        return result.value
    try:
        runs = read('list_runs')
        save(output/'runs.json', runs)
        linked = []
        for run in runs:
            records = read('read_diagnostics', run_id=run['run_id'])
            save(output/(run['run_id']+'.json'), dict(run=run, records=records,
                review=read('read_review_metadata', run_id=run['run_id'])))
            item = by_hash.get(run['log_sha256'])
            if item:
                assert sha(Path(item['snapshot'])) == run['log_sha256']
            linked.append(dict(run_id=run['run_id'], log_sha256=run['log_sha256'],
                input=item, stored_records=len(records),
                occurrences=sum(r['occurrence_count'] for r in records)))
    finally:
        client.shutdown()  # Only this experiment's disposable backup handler.
    assert sha(database) == before
    save(output/'stored-evidence.json', dict(source_database=str(source_path),
        database=str(database), database_sha256=before, backup_unchanged=True,
        runs=linked, training_hashes=[r['sha256'] for r in training]))
    print(json.dumps(dict(runs=len(runs), linked_runs=sum(r['input'] is not None for r in linked),
        records=sum(r['stored_records'] for r in linked), occurrences=sum(r['occurrences'] for r in linked))))


def build(root, output):
    from template_learning.learner_loader import create_release, launch
    release = create_release(root/'tools/template_learning', output/'learner-releases')
    save(output/'release.json', release)
    folder, pin = Path(release['folder']), release['manifest_sha256']
    arguments = ['--parser-manifest', str(folder/'template_learning/parsers/v1_7/manifest.json'),
                 '--output-dir', str(output/'candidate')]
    for row in json.loads((output/'inputs.json').read_text()):
        arguments.extend(['--log', row['snapshot']])
    start = time.monotonic()
    launch(folder, pin, 'learn', arguments, receipt=str(output/'learn-execution.json'))
    save(output/'build-completion.json', dict(seconds=time.monotonic()-start))
    bundle, = (output/'candidate').glob('*/manifest.json')
    launch(folder, pin, 'publish', ['--bundle', str(bundle.parent), '--output-dir', str(output/'packages')],
           receipt=str(output/'publish-execution.json'))


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('phase', choices=['snapshot', 'build', 'source-probe'])
    cli.add_argument('--root', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--inventory', type=Path)
    cli.add_argument('--training', type=Path)
    cli.add_argument('--native-evidence', type=Path)
    args = cli.parse_args()
    if args.phase == 'snapshot':
        snapshot(args.root.resolve(), args.output.resolve(), args.inventory, args.training)
    elif args.phase=='source-probe':
        from template_learning.evidence_serialization import native_evidence_rows
        from template_learning.records import SequenceRecord
        from template_learning.artifacts import _learn_pool
        from template_learning.matching_validation import _validate_template
        from template_learning.owner_rules import OWNER_RULES
        manifest = json.loads(args.native_evidence.with_name('manifest.json').read_text())
        assert sha(args.native_evidence)==manifest['hashes']['native_evidence.json']
        records=[]
        for row, count in native_evidence_rows(args.native_evidence, retain_occurrences=True):
            if row['source_family']=='jomini_script_system.cpp':
                records.append(SequenceRecord(row['source_family'],row['native'],tuple(map(tuple,row['pieces'])),
                    row['context_kind'], row['contexts'], row['native_occurrences'], tuple(row['continuations'])))
        review=[]
        print('Loaded',len(records),'genuine source records',flush=True)
        templates=_learn_pool('jomini_script_system.cpp',records,.72,review)
        for template in templates:
            _validate_template(template,{d['id']:d for d in OWNER_RULES['constructions']},
                {d['id']:d for d in OWNER_RULES['parameter_structures']},
                {d['id']:d for d in OWNER_RULES['location_label_equivalences']['groups']})
        save(args.output/'source-probe.json',dict(records=len(records),templates=templates,review=review))
        print('Source inference and declaration validation passed:',len(templates),'templates',flush=True)
    else:
        build(args.root.resolve(), args.output.resolve())


if __name__ == '__main__':
    main()
