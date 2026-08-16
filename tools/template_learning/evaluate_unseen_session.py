"""Evaluate one protected error.log against a frozen empirical model.

This is inference-only.  It never updates the model and reports unmatched
patterns explicitly rather than assigning them to the nearest weak match.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

import learn_error_templates as learner
from ck3chronicle.parser.log_blocks import iter_log_blocks


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reconstruct_model(model: dict) -> tuple[dict[str, list[learner.TemplateCluster]], dict[str, dict]]:
    by_source: dict[str, list[learner.TemplateCluster]] = collections.defaultdict(list)
    by_id: dict[str, dict] = {}
    for item in model["clusters"]:
        medoid = learner.SequenceRecord(
            source_family=item["source_family"],
            tokens=learner.tokenize(item["medoid"]),
            semantic_lead=tuple(item["semantic_lead"]),
            occurrences=item["support_occurrences"],
            evidence_ids=set(item["support_evidence_ids"]),
            examples=list(item["examples"]),
        )
        cluster = learner.TemplateCluster(
            source_family=item["source_family"],
            cluster_number=0,
            records=[medoid],
            medoid=medoid,
            template_tokens=tuple(item["template_tokens"]),
            support_occurrences=item["support_occurrences"],
            support_evidence=set(item["support_evidence_ids"]),
        )
        if cluster.cluster_id != item["cluster_id"]:
            raise ValueError(f"cluster reconstruction mismatch: {item['cluster_id']}")
        by_source[item["source_family"]].append(cluster)
        by_id[item["cluster_id"]] = item
    return dict(by_source), by_id


def inference_records(log_path: Path) -> tuple[dict[tuple[str, tuple[str, ...]], dict], int]:
    records: dict[tuple[str, tuple[str, ...]], dict] = {}
    timestamped_blocks = 0
    for block in iter_log_blocks(log_path, log_relpath="error.log"):
        if block.timestamp is None:
            continue
        timestamped_blocks += 1
        message = learner.block_message(block)
        for unit in learner.semantic_units(block.source_family, message):
            tokens = learner.tokenize(unit)
            if not unit or not tokens:
                continue
            key = (block.source_family, tokens)
            record = records.get(key)
            if record is None:
                record = {
                    "source_family": block.source_family,
                    "tokens": tokens,
                    "semantic_lead": learner.diagnostic_lead(unit),
                    "occurrences": 0,
                    "example": unit[:1000],
                }
                records[key] = record
            record["occurrences"] += 1
    return records, timestamped_blocks


def evaluate(log_path: Path, model_path: Path) -> tuple[dict, list[dict], list[dict]]:
    model = json.loads(model_path.read_text(encoding="utf-8"))
    by_source, by_id = reconstruct_model(model)
    records, timestamped_blocks = inference_records(log_path)
    threshold = float(model["algorithm"]["cluster_threshold"])

    counts = collections.Counter()
    matched = collections.Counter()
    unknown_rows: list[dict] = []
    assigned_rows: list[dict] = []
    locator_failures: list[dict] = []
    for record in records.values():
        occurrences = int(record["occurrences"])
        counts["eligible_occurrences"] += occurrences
        counts["distinct_sequences"] += 1
        layered = learner.best_layered_cluster(
            by_source,
            record["source_family"],
            record["tokens"],
            record["semantic_lead"],
            threshold,
        )
        cluster = layered.cluster
        layers = learner.script_system_layer_tokens(record["tokens"])
        if cluster is None and not layered.outer_known:
            unknown_kind = "known_source_new_pattern" if record["source_family"] in by_source else "new_source_family"
            counts[f"{unknown_kind}_occurrences"] += occurrences
            counts[f"{unknown_kind}_sequences"] += 1
            unknown_rows.append(
                {
                    "unknown_kind": unknown_kind,
                    "source_family": record["source_family"],
                    "semantic_lead": " ".join(record["semantic_lead"]),
                    "occurrences": occurrences,
                    "message": record["example"],
                    "l1_outer_template": "",
                    "l2_reason_template": "",
                    "review_decision": "",
                    "reviewer_notes": "",
                }
            )
            continue

        counts["l1_or_full_assigned_occurrences"] += occurrences
        counts["l1_or_full_assigned_sequences"] += 1
        if cluster is None:
            assert layered.outer_contract is not None and layers is not None
            outer_template = " ".join(layered.outer_contract)
            reason_cluster_layers = (
                learner.script_system_layer_tokens(layered.reason_cluster.template_tokens)
                if layered.reason_cluster is not None
                else None
            )
            reason_tokens = (
                reason_cluster_layers[1]
                if reason_cluster_layers is not None
                else layers[1]
            )
            reason_template = " ".join(reason_tokens)
            if layered.reason_cluster is not None:
                counts["l1_l2_composed_occurrences"] += occurrences
                counts["l1_l2_composed_sequences"] += 1
                counts["l2_resolved_occurrences"] += occurrences
                counts["l2_resolved_sequences"] += 1
                contract_id = learner.layered_contract_id(
                    record["source_family"], layered.outer_contract, reason_tokens
                )
                rendered_template = outer_template + " [ " + reason_template + " ]"
            else:
                counts["l1_assigned_l2_unresolved_occurrences"] += occurrences
                counts["l1_assigned_l2_unresolved_sequences"] += 1
                contract_id = ""
                rendered_template = outer_template + " [ <UNRESOLVED_REASON> ]"
                unknown_rows.append(
                    {
                        "unknown_kind": "known_l1_new_l2_reason",
                        "source_family": record["source_family"],
                        "semantic_lead": " ".join(record["semantic_lead"]),
                        "occurrences": occurrences,
                        "message": record["example"],
                        "l1_outer_template": outer_template,
                        "l2_reason_template": reason_template,
                        "review_decision": "",
                        "reviewer_notes": "",
                    }
                )
            assigned_rows.append(
                {
                    "assignment_level": layered.assignment_level,
                    "cluster_id": contract_id,
                    "source_family": record["source_family"],
                    "occurrences": occurrences,
                    "l1_outer_template": outer_template,
                    "l2_reason_template": reason_template,
                    "template": rendered_template,
                    "message": record["example"],
                }
            )
        else:
            counts["assigned_occurrences"] += occurrences
            counts["assigned_sequences"] += 1
            counts["full_contract_assigned_occurrences"] += occurrences
            counts["full_contract_assigned_sequences"] += 1
            if layered.outer_contract is not None:
                counts["l2_resolved_occurrences"] += occurrences
                counts["l2_resolved_sequences"] += 1
            matched[cluster.cluster_id] += occurrences
            layer_contracts = by_id[cluster.cluster_id].get("layer_contracts") or {}
            assigned_rows.append(
                {
                    "assignment_level": layered.assignment_level,
                    "cluster_id": cluster.cluster_id,
                    "source_family": record["source_family"],
                    "occurrences": occurrences,
                    "l1_outer_template": layer_contracts.get("l1_outer_template", ""),
                    "l2_reason_template": layer_contracts.get("l2_reason_template", ""),
                    "template": by_id[cluster.cluster_id]["template"],
                    "message": record["example"],
                }
            )

        mutated_message = learner.mutate_locators(record["example"])
        mutated = learner.best_layered_cluster(
            by_source,
            record["source_family"],
            learner.tokenize(mutated_message),
            learner.diagnostic_lead(mutated_message),
            threshold,
        )
        counts["locator_tested_sequences"] += 1
        counts["locator_tested_occurrences"] += occurrences
        if (
            cluster is not None
            and mutated.cluster is not None
            and mutated.cluster.cluster_id == cluster.cluster_id
        ) or (
            cluster is None
            and mutated.cluster is None
            and mutated.outer_known
            and mutated.outer_contract == layered.outer_contract
            and (
                (layered.reason_cluster is None and mutated.reason_cluster is None)
                or (
                    layered.reason_cluster is not None
                    and mutated.reason_cluster is not None
                    and mutated.reason_cluster.cluster_id
                    == layered.reason_cluster.cluster_id
                )
            )
        ):
            counts["locator_stable_sequences"] += 1
            counts["locator_stable_occurrences"] += occurrences
        else:
            locator_failures.append(
                {
                    "source_family": record["source_family"],
                    "cluster_id": cluster.cluster_id if cluster else None,
                    "mutated_cluster_id": (
                        mutated.cluster.cluster_id if mutated.cluster else None
                    ),
                    "occurrences": occurrences,
                    "message": record["example"],
                }
            )

    eligible = counts["eligible_occurrences"]
    distinct = counts["distinct_sequences"]
    summary = {
        "schema": "ck3chronicle.empirical-template-unseen-inference",
        "schema_version": 2,
        "status": "first_inference_frozen_model_no_tuning",
        "holdout": {
            "path": str(log_path),
            "bytes": log_path.stat().st_size,
            "sha256": sha256_file(log_path),
            "timestamped_blocks": timestamped_blocks,
        },
        "model": {
            "path": str(model_path),
            "sha256": sha256_file(model_path),
            "cluster_threshold": threshold,
            "candidate_templates": len(model["clusters"]),
            "training_distinct_error_logs": model["summary"]["distinct_error_logs"],
        },
        "counts": dict(counts),
        "metrics": {
            "occurrence_assignment_rate": counts["assigned_occurrences"] / eligible if eligible else 0.0,
            "distinct_sequence_assignment_rate": counts["assigned_sequences"] / distinct if distinct else 0.0,
            "l1_or_full_occurrence_assignment_rate": counts["l1_or_full_assigned_occurrences"] / eligible if eligible else 0.0,
            "l1_or_full_distinct_sequence_assignment_rate": counts["l1_or_full_assigned_sequences"] / distinct if distinct else 0.0,
            "l2_known_occurrence_rate_within_layered_assignments": counts["l2_resolved_occurrences"] / (counts["l2_resolved_occurrences"] + counts["l1_assigned_l2_unresolved_occurrences"]) if (counts["l2_resolved_occurrences"] + counts["l1_assigned_l2_unresolved_occurrences"]) else 0.0,
            "locator_stability_by_sequence": counts["locator_stable_sequences"] / counts["locator_tested_sequences"] if counts["locator_tested_sequences"] else 0.0,
            "locator_stability_by_occurrence": counts["locator_stable_occurrences"] / counts["locator_tested_occurrences"] if counts["locator_tested_occurrences"] else 0.0,
            "matched_template_count": len(matched),
        },
        "top_assigned_templates": [
            {
                "cluster_id": cluster_id,
                "source_family": by_id[cluster_id]["source_family"],
                "occurrences": occurrences,
                "template": by_id[cluster_id]["template"],
            }
            for cluster_id, occurrences in matched.most_common(30)
        ],
        "locator_mutation_failures": sorted(locator_failures, key=lambda row: -row["occurrences"]),
        "interpretation": [
            "Full assignment is structural similarity to a frozen reason-specific template, not semantic-label accuracy.",
            "Independently known exact L1 envelopes and learned L2 reasons may compose without claiming their precise pairing was previously observed.",
            "A novel bracket reason can receive L1-only assignment while remaining explicitly unresolved.",
            "Unknown L2 reasons and wholly unknown patterns were not force-fit to the nearest cluster.",
            "Purity and semantic accuracy require independent adjudication of a sample from this session.",
        ],
    }
    return summary, sorted(unknown_rows, key=lambda row: (-row["occurrences"], row["source_family"], row["message"])), sorted(assigned_rows, key=lambda row: (-row["occurrences"], row["cluster_id"], row["message"]))


def write_csv(path: Path, rows: list[dict], fallback_fields: list[str]) -> None:
    fields = list(fallback_fields)
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, summary: dict, unknowns: list[dict]) -> None:
    counts = summary["counts"]
    metrics = summary["metrics"]
    untouched = summary["status"] == "first_inference_frozen_model_no_tuning"
    lines = [
        (
            "# First inference on untouched CK3 session"
            if untouched
            else "# Post-fix development retest on previously inspected CK3 session"
        ),
        "",
        f"- Holdout SHA-256: `{summary['holdout']['sha256']}`",
        f"- Frozen model SHA-256: `{summary['model']['sha256']}`",
        f"- Timestamped blocks: **{summary['holdout']['timestamped_blocks']:,}**",
        f"- Full L2/non-layered occurrence assignment: **{counts.get('assigned_occurrences', 0):,}/{counts.get('eligible_occurrences', 0):,} ({metrics['occurrence_assignment_rate']:.2%})**",
        f"- Full L2/non-layered distinct-sequence assignment: **{counts.get('assigned_sequences', 0):,}/{counts.get('distinct_sequences', 0):,} ({metrics['distinct_sequence_assignment_rate']:.2%})**",
        f"- L1-or-full occurrence assignment: **{counts.get('l1_or_full_assigned_occurrences', 0):,}/{counts.get('eligible_occurrences', 0):,} ({metrics['l1_or_full_occurrence_assignment_rate']:.2%})**",
        f"- L1-or-full distinct-sequence assignment: **{counts.get('l1_or_full_assigned_sequences', 0):,}/{counts.get('distinct_sequences', 0):,} ({metrics['l1_or_full_distinct_sequence_assignment_rate']:.2%})**",
        f"- Independently composed known L1 + known L2: **{counts.get('l1_l2_composed_sequences', 0):,} sequences / {counts.get('l1_l2_composed_occurrences', 0):,} occurrences**",
        f"- Known L1 / unresolved L2: **{counts.get('l1_assigned_l2_unresolved_sequences', 0):,} sequences / {counts.get('l1_assigned_l2_unresolved_occurrences', 0):,} occurrences**",
        f"- Known-source new patterns: **{counts.get('known_source_new_pattern_sequences', 0):,} sequences / {counts.get('known_source_new_pattern_occurrences', 0):,} occurrences**",
        f"- Entirely new source families: **{counts.get('new_source_family_sequences', 0):,} sequences / {counts.get('new_source_family_occurrences', 0):,} occurrences**",
        f"- Frozen templates exercised: **{metrics['matched_template_count']}**",
        f"- Locator stability: **{counts.get('locator_stable_sequences', 0):,}/{counts.get('locator_tested_sequences', 0):,} sequences ({metrics['locator_stability_by_sequence']:.2%})**",
        "",
        "These are coverage and invariance results, not semantic accuracy.",
        (
            "No model rule was changed after the session was captured and unknowns were not force-fit."
            if untouched
            else "This session was previously inspected during tuning; these numbers are not a new holdout claim."
        ),
        "",
        "## Top assigned templates",
        "",
        "| Occurrences | Source | Frozen template |",
        "|---:|---|---|",
    ]
    for item in summary["top_assigned_templates"][:15]:
        template = item["template"].replace("|", "\\|")
        if len(template) > 240:
            template = template[:239] + "Ã¢â‚¬Â¦"
        lines.append(f"| {item['occurrences']:,} | `{item['source_family']}` | {template} |")
    lines.extend(
        [
            "",
            "## Highest-volume unresolved patterns",
            "",
            "| Occurrences | Kind | Source | Message |",
            "|---:|---|---|---|",
        ]
    )
    for item in unknowns[:25]:
        message = item["message"].replace("|", "\\|")
        if len(message) > 260:
            message = message[:259] + "Ã¢â‚¬Â¦"
        lines.append(f"| {item['occurrences']:,} | {item['unknown_kind']} | `{item['source_family']}` | {message} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--status",
        default="first_inference_frozen_model_no_tuning",
        help="Evidence-status label written into JSON and used to label the Markdown report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary, unknowns, assigned = evaluate(args.log, args.model)
    summary["status"] = args.status
    summary["evaluator_sha256"] = sha256_file(Path(__file__).resolve())
    (args.output_dir / "FIRST_INFERENCE.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_csv(
        args.output_dir / "unknown_patterns.csv",
        unknowns,
        ["unknown_kind", "source_family", "semantic_lead", "occurrences", "message", "l1_outer_template", "l2_reason_template", "review_decision", "reviewer_notes"],
    )
    write_csv(
        args.output_dir / "assigned_sequences.csv",
        assigned,
        ["assignment_level", "cluster_id", "source_family", "occurrences", "l1_outer_template", "l2_reason_template", "template", "message"],
    )
    write_markdown(args.output_dir / "FIRST_INFERENCE.md", summary, unknowns)
    print(json.dumps(summary, indent=2)[:12000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
