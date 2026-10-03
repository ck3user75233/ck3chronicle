"""Run with python -I -S: no installed ck3chronicle/learner package required."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path


def load_verified(folder, manifest_sha256):
    folder = Path(folder).resolve()
    payload = (folder / 'manifest.json').read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest_sha256:
        raise ValueError('externally supplied manifest digest disagrees')
    manifest = json.loads(payload)
    path = folder / 'matcher_loader.py'
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest['hashes']['matcher_loader.py']:
        raise ValueError('bootstrap digest disagrees')
    spec = importlib.util.spec_from_file_location('verified_matcher_bootstrap', path)
    module = importlib.util.module_from_spec(spec)
    # Execute the already verified bytes, without a second file read for exec.
    exec(compile(payload, str(path), 'exec'), module.__dict__)
    return module.load_package(folder, expected_manifest_sha256=manifest_sha256)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--package', type=Path, required=True)
    cli.add_argument('--manifest-sha256', required=True)
    cli.add_argument('--log', type=Path, required=True)
    args = cli.parse_args()
    package = load_verified(args.package, args.manifest_sha256)
    raw = package.parse_file(args.log)
    counts = Counter()
    example = None
    for unit in package.iter_units(raw):
        if unit['recovery_status'] != 'recovered':
            counts['unresolved'] += 1
            continue
        result = package.match(unit)
        chosen = result['assignment']
        counts[chosen['match_status'] if chosen else 'no_match'] += 1
        if example is None or (unit['continuations'] and not example['has_components']):
            example = dict(has_components=bool(unit['continuations']), result=result)
    print(json.dumps(dict(log_sha256=hashlib.sha256(raw.source.data).hexdigest(),
                          counts=counts, example=example), indent=2))


if __name__ == '__main__':
    main()
