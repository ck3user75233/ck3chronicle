"""Measure serialization allocations using a saved genuine research model."""
import argparse
import gc
import json
from pathlib import Path
import time
import tracemalloc

from template_learning.evidence_serialization import write_json, json_identity
from template_learning.inventory import sha256_file


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    manifest = json.loads((args.bundle/'manifest.json').read_text())
    source = args.bundle/'empirical_template_model.json'
    assert sha256_file(source) == manifest['hashes'][source.name]
    with source.open(encoding='utf-8') as stream:
        model = json.load(stream)
    args.output.mkdir(parents=True, exist_ok=False)
    result = dict(source=str(source.resolve()), source_bytes=source.stat().st_size,
        source_revision=model['revision_id'],
        scope='Additional Python allocations after loading the genuine model; excludes inference and initial model loading.')

    def measure(name, operation):
        gc.collect()
        tracemalloc.start()
        started = time.monotonic()
        value = operation()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        result[name] = dict(seconds=time.monotonic()-started,
                            retained_allocations=current, peak_allocations=peak)
        print(name, json.dumps(result[name]), flush=True)
        return value

    digest = measure('write_json', lambda: write_json(args.output/source.name, model))
    assert digest == manifest['hashes'][source.name]
    revision = measure('revision_hash', lambda: json_identity({k: v for k, v in model.items() if k != 'revision_id'}))
    assert revision[:24] == model['revision_id']
    result.update(serialized_bytes_identical=True, revision_hash_identical=True)
    write_json(args.output/'measurement.json', result)


if __name__ == '__main__':
    main()
