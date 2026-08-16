"""Mine underscore-suffix symbol shapes as QC evidence, never template rules.

Support is measured by distinct values, structural template contexts, protected
training logs, and source families.  Raw occurrence counts are reported only
as volume: repetition of one error does not increase QC confidence.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evaluate_unseen_session as unseen
import learn_error_templates as learner


UNDERSCORE_IDENTIFIER_RE = re.compile(
    r"^[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+$"
)
KNOWN_QC_SUFFIXES = frozenset({"effect", "trigger"})


def locator_context(tokens: tuple[str, ...], index: int) -> bool:
    """Exclude values already occurring in file/callsite evidence."""
    if tokens[index] == learner.LOCATOR:
        return True
    # A CK3 scripted callsite commonly follows a masked path as:
    # `<LOCATOR> ( some_effect [ args#... ] )`.  The symbol-looking callsite is
    # still locator evidence, not a semantic slot value.
    left = tokens[max(0, index - 8) : index]
    if learner.LOCATOR in left:
        locator_position = len(left) - 1 - left[::-1].index(learner.LOCATOR)
        after_locator = left[locator_position + 1 :]
        if "(" in after_locator and ")" not in after_locator:
            return True
    # Retain this conservative fallback for unmasked `file:` fragments.
    nearby = tuple(token.casefold() for token in tokens[max(0, index - 4) : index])
    return "file" in nearby and (":" in nearby or "at" in nearby)


def add_example(bucket: dict, value: str, cluster_id: str, source: str, context: str) -> None:
    example = {
        "value": value,
        "cluster_id": cluster_id,
        "source_family": source,
        "context": context,
    }
    if example not in bucket["examples"] and len(bucket["examples"]) < 8:
        bucket["examples"].append(example)


def mine(state_root: Path) -> tuple[list[dict], dict]:
    registry = json.loads((state_root / "registry.json").read_text(encoding="utf-8"))
    revision_id = registry["current_revision"]
    if not revision_id:
        raise ValueError("registry has no current model revision")
    model_path = state_root / "revisions" / revision_id / "empirical_template_model.json"
    model = json.loads(model_path.read_text(encoding="utf-8"))
    by_source, by_id = unseen.reconstruct_model(model)
    threshold = float(model["algorithm"]["cluster_threshold"])

    suffixes: dict[str, dict] = {}
    excluded_locator_values: set[str] = set()
    assigned_records = 0
    unassigned_records = 0
    for entry in sorted(registry["evidence"].values(), key=lambda item: item["sha256"]):
        if entry["role"] != "training":
            continue
        cache = entry["feature_caches"][learner.NORMALIZER_VERSION]
        feature = json.loads((state_root / cache["path"]).read_text(encoding="utf-8"))
        evidence_sha = entry["sha256"]
        for record in feature["records"]:
            tokens = tuple(record["tokens"])
            cluster = learner.best_cluster(
                by_source,
                record["source_family"],
                tokens,
                tuple(record["semantic_lead"]),
                threshold,
            )
            if cluster is None:
                unassigned_records += 1
                continue
            assigned_records += 1
            cluster_item = by_id[cluster.cluster_id]
            literal_tokens = set(cluster_item["template_tokens"])
            for index, token in enumerate(tokens):
                bare = token.lstrip("@")
                if not UNDERSCORE_IDENTIFIER_RE.fullmatch(bare):
                    continue
                suffix = bare.rsplit("_", 1)[1].casefold()
                if not suffix.isalpha():
                    continue
                if locator_context(tokens, index):
                    excluded_locator_values.add(bare)
                    continue
                bucket = suffixes.setdefault(
                    suffix,
                    {
                        "values": set(),
                        "template_ids": set(),
                        "evidence_sha256": set(),
                        "source_families": set(),
                        "abstracted_values": set(),
                        "retained_literal_values": set(),
                        "raw_occurrences": 0,
                        "examples": [],
                    },
                )
                bucket["values"].add(bare)
                bucket["template_ids"].add(cluster.cluster_id)
                bucket["evidence_sha256"].add(evidence_sha)
                bucket["source_families"].add(record["source_family"])
                if token in literal_tokens:
                    bucket["retained_literal_values"].add(bare)
                else:
                    bucket["abstracted_values"].add(bare)
                bucket["raw_occurrences"] += int(record["occurrences"])
                context = " ".join(tokens[max(0, index - 6) : index + 7])
                add_example(bucket, bare, cluster.cluster_id, record["source_family"], context)

    rows: list[dict] = []
    for suffix, bucket in suffixes.items():
        distinct_values = len(bucket["values"])
        distinct_templates = len(bucket["template_ids"])
        distinct_logs = len(bucket["evidence_sha256"])
        distinct_sources = len(bucket["source_families"])
        if suffix in KNOWN_QC_SUFFIXES:
            review_status = "known_symbol_suffix"
        elif distinct_values >= 3 and distinct_templates >= 2 and distinct_logs >= 2:
            review_status = "candidate_suffix_review"
        else:
            review_status = "insufficient_distinct_support"
        rows.append(
            {
                "suffix": suffix,
                "review_status": review_status,
                "distinct_values": distinct_values,
                "distinct_templates": distinct_templates,
                "distinct_training_logs": distinct_logs,
                "distinct_source_families": distinct_sources,
                "abstracted_values": len(bucket["abstracted_values"]),
                "retained_literal_values": len(bucket["retained_literal_values"]),
                "raw_occurrences_descriptive_only": bucket["raw_occurrences"],
                "example_values": sorted(bucket["values"])[:12],
                "examples": bucket["examples"],
            }
        )
    rows.sort(
        key=lambda row: (
            row["review_status"] == "insufficient_distinct_support",
            -row["distinct_training_logs"],
            -row["distinct_templates"],
            -row["distinct_values"],
            row["suffix"],
        )
    )
    summary = {
        "schema": "ck3chronicle.symbol-suffix-qc-inventory",
        "schema_version": 1,
        "status": "qc_candidates_only_not_template_rules",
        "model_revision": revision_id,
        "training_evidence_hashes": sorted(
            row["sha256"] for row in registry["evidence"].values() if row["role"] == "training"
        ),
        "support_policy": {
            "confidence_dimensions": [
                "distinct_values",
                "distinct_templates",
                "distinct_training_logs",
                "distinct_source_families",
            ],
            "raw_occurrences_used_for_confidence": False,
            "locator_values_excluded": True,
        },
        "assigned_feature_records": assigned_records,
        "unassigned_feature_records": unassigned_records,
        "suffixes": len(rows),
        "known_suffixes": sorted(KNOWN_QC_SUFFIXES),
        "candidate_suffixes": sum(
            row["review_status"] == "candidate_suffix_review" for row in rows
        ),
        "excluded_locator_like_values": len(excluded_locator_values),
    }
    return rows, summary


def write_outputs(rows: list[dict], summary: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {**summary, "rows": rows}
    (output_dir / "symbol_suffix_inventory.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    fields = [
        "suffix",
        "review_status",
        "distinct_values",
        "distinct_templates",
        "distinct_training_logs",
        "distinct_source_families",
        "abstracted_values",
        "retained_literal_values",
        "raw_occurrences_descriptive_only",
        "example_values",
        "human_decision",
        "reviewer_notes",
    ]
    with (output_dir / "symbol_suffix_inventory.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **{field: row.get(field, "") for field in fields},
                    "example_values": " | ".join(row["example_values"]),
                }
            )
    review = [row for row in rows if row["review_status"] != "insufficient_distinct_support"]
    lines = [
        "# CK3 underscore-suffix QC inventory",
        "",
        "These are QC candidates, not template-discovery or taxonomy rules.",
        "Raw occurrence volume is descriptive only; repeated copies of one error",
        "do not increase confidence.",
        "",
        f"- Model revision: `{summary['model_revision']}`",
        f"- Training logs: **{len(summary['training_evidence_hashes'])}**",
        f"- Suffixes observed: **{summary['suffixes']}**",
        f"- Review candidates beyond known `_effect`/`_trigger`: **{summary['candidate_suffixes']}**",
        f"- Locator/callsite-looking values excluded: **{summary['excluded_locator_like_values']}**",
        "",
        "## Review inventory",
        "",
        "| Suffix | Status | Values | Templates | Logs | Sources | Examples |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in review:
        examples = ", ".join(f"`{value}`" for value in row["example_values"][:5])
        lines.append(
            f"| `_{row['suffix']}` | {row['review_status']} | {row['distinct_values']} | "
            f"{row['distinct_templates']} | {row['distinct_training_logs']} | "
            f"{row['distinct_source_families']} | {examples} |"
        )
    (output_dir / "SYMBOL_SUFFIX_QC_REVIEW.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows, summary = mine(args.state_root)
    write_outputs(rows, summary, args.output_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
