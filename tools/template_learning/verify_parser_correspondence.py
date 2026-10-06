"""Compare real authenticated package parsers on an explicit genuine log inventory."""
import argparse
from concurrent.futures import ProcessPoolExecutor
from dataclasses import fields, is_dataclass
import hashlib
from itertools import zip_longest
import json
from pathlib import Path
import time

from template_learning.matcher_example import load_verified

_PACKAGES = None


def load_comparison(config):
    global _PACKAGES
    _PACKAGES = {k: load_verified(Path(path), pin) for k, (path, pin) in config.items()}


def compare_log(item):
    digest, name = item
    packages = _PACKAGES
    started = time.monotonic()
    path = Path(name).resolve(); data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, path
    raw = {k: p.parse_file(path) for k, p in packages.items()}
    a, b = raw.values()
    assert a.source.data == b.source.data == data
    assert len(a.emissions) == len(b.emissions)
    assert b''.join(e.native_bytes() for e in a.emissions) == data
    assert b''.join(e.native_bytes() for e in b.emissions) == data
    for x, y in zip(a.emissions, b.emissions):
        assert primitive(x) == primitive(y)
        assert x.decoded_text == y.decoded_text and x.body_text == y.body_text
        assert primitive(x.pieces) == primitive(y.pieces)
        assert primitive(x.recovery) == primitive(y.recovery)
    recoveries = 0
    for x, y in zip_longest(a.iter_recoveries(), b.iter_recoveries()):
        assert x is not None and y is not None and primitive(x) == primitive(y)
        recoveries += 1
    units = 0
    for x, y in zip_longest(packages['production'].iter_units(a), packages['candidate'].iter_units(b)):
        assert x is not None and y is not None
        corresponding_units(dict(production=x, candidate=y))
        units += 1
    return dict(path=str(path), sha256=digest, bytes=len(data), emissions=len(a.emissions),
                recoveries=recoveries, native_units=units, status='passed',
                seconds=round(time.monotonic()-started, 3))


def primitive(value):
    if isinstance(value, bytes):
        return {'bytes': len(value), 'sha256': hashlib.sha256(value).hexdigest()}
    if is_dataclass(value):
        if type(value).__name__ == 'Source':
            return {'source_name': value.name}
        return {f.name: primitive(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, (tuple, list)):
        return [primitive(v) for v in value]
    if isinstance(value, dict):
        return {k: primitive(v) for k, v in value.items()}
    return value


def corresponding_units(units):
    """Require equal native input, retaining each package's actual parser identity."""
    values = [primitive({k: v for k, v in unit.items() if k != 'parser'})
              for unit in units.values()]
    assert all(value == values[0] for value in values[1:]), 'native parser inputs differ'


def evidence_unit(package, unit):
    """Re-lex retained genuine regions before using this package's parser identity."""
    for region in [unit['body'], *unit['contexts'].values(), *unit['continuations']]:
        raw = region['text'].encode('utf-8', 'surrogateescape')
        source = package.parser.Source('retained-genuine-region', raw)
        pieces = [(p.kind, p.text) for p in package.parser.lexical_pieces(
            source, package.parser.Span(0, len(raw)))]
        assert pieces == list(map(tuple, region['pieces'])), 'retained lexical evidence differs'
        assert source.read_text(package.parser.Span(0, len(raw))) == region['text']
    return dict(unit, parser=package.manifest['parser'])


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--production', type=Path, required=True)
    cli.add_argument('--production-pin', required=True)
    cli.add_argument('--candidate', type=Path, required=True)
    cli.add_argument('--candidate-pin', required=True)
    cli.add_argument('--basis', type=Path, required=True)
    cli.add_argument('--additional-receipt', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--workers', type=int, default=1)
    args = cli.parse_args()
    config = dict(production=(str(args.production.resolve()), args.production_pin),
                  candidate=(str(args.candidate.resolve()), args.candidate_pin))
    load_comparison(config)
    packages = _PACKAGES
    basis = json.loads(args.basis.read_bytes())
    logs = {r['sha256']: r['snapshot'] for r in basis['inputs']}
    for row in json.loads(args.additional_receipt.read_bytes())['logs']:
        logs.setdefault(row['sha256'], row['path'])
    report = dict(status='running', packages={k: dict(package_id=p.manifest['package_id'],
        manifest_sha256=p.manifest_sha256, parser=p.manifest['parser']) for k, p in packages.items()},
        basis_sha256=hashlib.sha256(args.basis.read_bytes()).hexdigest(),
        training_hashes=sorted(r['sha256'] for r in basis['inputs']), logs=[])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    def save():
        args.output.write_text(json.dumps(report, ensure_ascii=True, indent=2)+'\n', encoding='utf-8')
    with ProcessPoolExecutor(max_workers=args.workers, initializer=load_comparison, initargs=(config,)) as pool:
        for row in pool.map(compare_log, logs.items()):
            report['logs'].append(row)
            save(); print(len(report['logs']), row['sha256'], row['emissions'], row['native_units'], flush=True)
    report['status'] = 'passed'
    report['comparison'] = 'Exact bytes, framing, decoded text, token spans, local/cross-emission recovery and native units; only actual parser reference differs.'
    save()


if __name__ == '__main__':
    main()
