"""Add a completed comparison's additional logs to an isolated cumulative build.

Uses validated registry evidence and the owning model builder. Does not mutate
registry roles or the selected production/research revision.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

from template_learning import artifacts
from template_learning.incremental_template_registry import combine_training_records, load_registry
from template_learning.inspect_candidate_revision import compact_review, row_key
from template_learning.parsers import load_parser, reference_from_manifest


def inspect(registry_root, comparison, parser_manifest, output):
    started = time.monotonic()
    baseline_summary = json.loads((comparison / "summary.json").read_text(encoding="utf-8"))
    baseline, bundled_parser = artifacts.load_bundle(Path(baseline_summary["bundle"]))
    parser = load_parser(reference_from_manifest(parser_manifest))
    if (parser.reference.version, parser.reference.sha256) != (bundled_parser.reference.version, bundled_parser.reference.sha256):
        raise ValueError("cumulative build requires the comparison's exact parser version and bytes")
    registry_bytes = (registry_root / "registry.json").read_bytes()
    registry = load_registry(registry_root)
    additions = baseline_summary["additional_logs"]
    selected = set(baseline["evidence"]) | set(additions["evidence"])
    assert len(selected) == len(baseline["evidence"]) + additions["logs"]
    entries = [registry["evidence"][sha] for sha in sorted(selected)]
    print(f"Building cumulative evidence: {len(baseline['evidence'])} + {additions['logs']} = {len(entries)} logs", flush=True)
    grouped, stats = combine_training_records(registry_root, entries, parser=parser)
    before = Counter(baseline["summary"]["training_outcomes"])
    before.update(additions["after"]["counts"])
    exceptions = {}
    for filename in ("training-review.json", "additional-review.json"):
        for row in json.loads((comparison / filename).read_text(encoding="utf-8")):
            key = (row["source_family"], row["native"], tuple(row["context_ids"]))
            if key in exceptions and exceptions[key] != row["outcome"]:
                raise ValueError("inconsistent saved outcomes for one candidate")
            exceptions[key] = row["outcome"]
    model, evidence = artifacts.build_model(grouped, stats, parser=parser,
        threshold=baseline["algorithm"]["cluster_threshold"])
    transitions, reconciled = Counter(), Counter()
    for row in evidence["records"]:
        previous = exceptions.get(row_key(row))
        if previous is None:
            previous = "full"
        count = len(row["native_occurrences"])
        reconciled[previous] += count
        transitions[(previous, row["outcome"])] += count
    assert reconciled == +before, (reconciled, before)
    output.mkdir(parents=True, exist_ok=True)
    (output / "training-review.json").write_bytes(artifacts.canonical_bytes(compact_review(evidence["records"], model)))
    bundle = artifacts.write_bundle(output / "revisions", model, evidence, parser=parser,
        build_command=[sys.executable, "-m", "template_learning.inspect_accumulated_corpus", *sys.argv[1:]])
    assert (registry_root / "registry.json").read_bytes() == registry_bytes
    result = dict(revision_id=model["revision_id"], bundle=str(bundle.resolve()),
        previous_revision=baseline["revision_id"], added_logs=additions["logs"], before=dict(before),
        after=model["summary"], registry_unchanged=True,
        transitions=[dict(before=a, after=b, occurrences=n) for (a,b),n in sorted(transitions.items())],
        scope="Cumulative in-corpus learning after adding the 25 native logs; not unseen-log accuracy",
        elapsed_seconds=round(time.monotonic()-started, 1))
    (output / "summary.json").write_bytes(artifacts.canonical_bytes(result))
    print(json.dumps(result), flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--registry", type=Path, required=True)
    p.add_argument("--comparison", type=Path, required=True)
    p.add_argument("--parser-manifest", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    inspect(args.registry, args.comparison, args.parser_manifest, args.output)


if __name__ == "__main__":
    main()
