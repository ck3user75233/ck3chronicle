"""Fresh complete-native-log replay for the shared matcher extraction.

Baseline must be run before changing matcher mechanics. Evidence stays ignored.
"""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path
import pickle

from template_learning.inventory import ProtectedLog, sha256_file
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.records import collect_records
from template_learning.research_matching import evaluate_records


def without_layout_indices(value):
    """Only expected extraction delta: identifying the chosen component layout."""
    if isinstance(value, dict):
        return {k: without_layout_indices(v) for k, v in value.items() if k != 'layout_index'}
    if isinstance(value, (list, tuple)):
        return type(value)(without_layout_indices(v) for v in value)
    return value


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--release', type=Path, required=True)
    cli.add_argument('--inventory', type=Path, required=True)
    cli.add_argument('--additional-log', type=Path, action='append', default=[])
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--baseline', action='store_true')
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((args.release / 'manifest.json').read_text())
    for name, digest in manifest['hashes'].items():
        assert sha256_file(args.release / name) == digest, name
    model = json.loads((args.release / 'empirical_template_model.json').read_text())
    parser = load_parser(reference_from_manifest(args.release / 'parser-manifest.json'))
    logs = json.loads(args.inventory.read_text())['logs']
    logs = [*logs, *[dict(path=str(p.resolve()), sha256=sha256_file(p),
                         cohort='additional') for p in args.additional_log]]
    assert {e['sha256'] for e in model['training_evidence']} <= {e['sha256'] for e in logs}
    report = dict(manifest_sha256=sha256_file(args.release / 'manifest.json'),
                  selection_sha256=sha256_file(Path('models/selection.json')),
                  logs=[], unavailable=[], counts=Counter())
    for item in {e['sha256']: e for e in logs}.values():
        path = Path(item['path'])
        if not path.is_file():
            report['unavailable'].append(item)
            continue
        stat = path.stat()
        evidence = ProtectedLog(item['sha256'], item['cohort'], path,
                                item['sha256'], stat.st_size, stat.st_mtime_ns)
        grouped, stats = collect_records([evidence], parser=parser)
        summary, rows, unresolved = evaluate_records(model, grouped, stats)
        saved = args.output / (item['sha256'] + '.pickle.gz')
        # Store complete fresh native inputs and every alternative, not a cache
        # used in place of reparsing during the after comparison.
        if args.baseline:
            if saved.exists():
                raise ValueError('baseline already exists: ' + str(saved))
            with gzip.open(saved, 'wb') as stream:
                pickle.dump((summary, rows, unresolved), stream)
        else:
            with gzip.open(saved, 'rb') as stream:
                expected = pickle.load(stream)
            assert without_layout_indices((summary, rows, unresolved)) == expected, path
        assert sha256_file(path) == item['sha256']
        report['logs'].append(dict(**item, bytes=stat.st_size, summary=summary,
                                  contextual_rows=len(rows)))
        report['counts'].update(summary['counts'])
        print(item['sha256'], summary['counts'], len(rows), flush=True)
        (args.output / ('baseline.json' if args.baseline else 'after.json')).write_text(
            json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
