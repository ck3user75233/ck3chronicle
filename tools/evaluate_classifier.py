"""Read-only coverage measurement for a protected CK3 error.log.

This utility never mutates the log, model, archive, or database. Its output is
telemetry, not a semantic-accuracy oracle.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from ck3chronicle.classification import Classifier, load_model
from ck3chronicle.parser.log_blocks import iter_log_blocks


def evaluate(classifier: Classifier, error_log: Path) -> dict[str, object]:
    assignments: Counter[str] = Counter()
    unknown_sources: Counter[str] = Counter()
    contract_counts: Counter[str] = Counter()
    unknown_examples: list[dict[str, str]] = []
    source_blocks = 0
    occurrences = 0

    for block in iter_log_blocks(error_log, log_relpath="error.log"):
        if block.timestamp is None:
            continue
        source_blocks += 1
        results = classifier.classify_block(block.source_family, block.raw_block)
        for result in results:
            occurrences += 1
            assignments[result.assignment_level] += 1
            if result.contract_id is not None:
                contract_counts[result.contract_id] += 1
            if result.assignment_level == "unknown":
                unknown_sources[result.source_family] += 1
                if len(unknown_examples) < 30:
                    unknown_examples.append(
                        {
                            "source_family": result.source_family,
                            "semantic_text": result.semantic_text[:500],
                        }
                    )

    assigned = occurrences - assignments["unknown"]
    l1_or_better = assigned
    return {
        "schema": "ck3chronicle.classifier-coverage",
        "schema_version": 1,
        "input": str(error_log),
        "model_revision": classifier.model.revision_id,
        "model_sha256": classifier.model.sha256,
        "source_blocks": source_blocks,
        "semantic_occurrences": occurrences,
        "assignments": dict(sorted(assignments.items())),
        "full_rate": assignments["full"] / occurrences if occurrences else 1.0,
        "l1_or_better_rate": l1_or_better / occurrences if occurrences else 1.0,
        "unknown_sources": unknown_sources.most_common(20),
        "unknown_examples": unknown_examples,
        "top_contracts": contract_counts.most_common(20),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("error_log", type=Path)
    parser.add_argument("model", type=Path)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    classifier = Classifier(load_model(args.model, expected_sha256=args.sha256))
    result = evaluate(classifier, args.error_log)
    if args.compact:
        result = {
            key: result[key]
            for key in (
                "input",
                "source_blocks",
                "semantic_occurrences",
                "assignments",
                "full_rate",
                "l1_or_better_rate",
                "unknown_sources",
            )
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
