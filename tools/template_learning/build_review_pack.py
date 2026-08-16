"""Build a human-reviewable evidence pack for the WIP template learner.

The pack is deliberately separate from production ck3chronicle.  It maps the
frozen 252-sample semantic oracle onto a frozen empirical model and emits both
short Markdown views and complete editable CSV queues.
"""
from __future__ import annotations

import argparse
import base64
import collections
import csv
import json
import re
from pathlib import Path

import learn_error_templates as learner
from ck3chronicle.parser.log_blocks import TimestampedLogBlock


PLACEHOLDER_RE = re.compile(r"<(?P<role>LOCATOR|KEY|VALUE|PARAM|ALT:[^>]+)>")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_cell(value: object, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "Ã¢â‚¬Â¦"
    return text.replace("|", "\\|")


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def reconstruct_clusters(model: dict) -> tuple[dict[str, list[learner.TemplateCluster]], dict[str, dict]]:
    by_source: dict[str, list[learner.TemplateCluster]] = collections.defaultdict(list)
    by_id: dict[str, dict] = {}
    for item in model["clusters"]:
        medoid_text = item["medoid"]
        medoid = learner.SequenceRecord(
            source_family=item["source_family"],
            tokens=learner.tokenize(medoid_text),
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


def sample_message(sample: dict) -> str:
    raw = base64.b64decode(sample["raw_block_base64"])
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    block = TimestampedLogBlock(
        timestamp=sample["timestamp"],
        level=sample["level"],
        source_tag=sample["source_tag"],
        source_family=sample["source_family"],
        header_line=lines[0] if lines else "",
        continuation_lines=lines[1:],
        raw_block=text,
        line_number=sample["start_line"],
        end_line=sample["end_line"],
    )
    return learner.block_message(block)


def map_samples(
    model: dict,
    candidate: dict,
    oracle: dict,
    clusters_by_source: dict[str, list[learner.TemplateCluster]],
    cluster_model: dict[str, dict],
) -> list[dict]:
    samples = {item["sample_id"]: item for item in candidate["samples"]}
    rows: list[dict] = []
    threshold = float(model["algorithm"]["cluster_threshold"])
    for annotation in oracle["annotations"]:
        sample = samples[annotation["sample_id"]]
        message = sample_message(sample)
        units = learner.semantic_units(sample["source_family"], message)
        unit = units[0] if units else message
        match = learner.best_cluster(
            clusters_by_source,
            sample["source_family"],
            learner.tokenize(unit),
            learner.diagnostic_lead(unit),
            threshold,
        )
        issue = annotation["issues"][0]
        cluster_id = match.cluster_id if match else ""
        cluster = cluster_model.get(cluster_id, {})
        rows.append(
            {
                "sample_id": sample["sample_id"],
                "manifest_block_index": sample["manifest_block_index"],
                "source_family": sample["source_family"],
                "accounting": annotation["accounting"],
                "category": issue["category"],
                "error_type": issue["error_type"],
                "assignment": "assigned" if match else "unknown",
                "cluster_id": cluster_id,
                "template": cluster.get("template", ""),
                "message": message,
                "evidence": annotation.get("evidence") or "",
                "uncertainty": annotation.get("uncertainty") or "",
                "adjudication_rationale": annotation.get("adjudication", {}).get("rationale", ""),
            }
        )
    return rows


def cluster_rows(sample_rows: list[dict], cluster_model: dict[str, dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = collections.defaultdict(list)
    for row in sample_rows:
        if row["cluster_id"]:
            grouped[row["cluster_id"]].append(row)

    result: list[dict] = []
    for cluster_id, samples in grouped.items():
        model = cluster_model[cluster_id]
        labels = collections.Counter((row["category"], row["error_type"]) for row in samples)
        label_text = "; ".join(
            f"{category}/{error_type} ({count})"
            for (category, error_type), count in labels.most_common()
        )
        flags: list[str] = []
        template = model["template"]
        if len(labels) > 1:
            flags.append("MIXED_LABELS")
        if len(samples) == 1:
            flags.append("SINGLE_ORACLE_SAMPLE")
        if model["support_evidence_count"] == 1:
            flags.append("ONE_TRAINING_SESSION")
        if len(model["template_tokens"]) > 80:
            flags.append("VERY_LONG_TEMPLATE")
        if "<PARAM>" in template:
            flags.append("AMBIGUOUS_PARAM")
        if "<ALT:" in template:
            flags.append("SEMANTIC_ALTERNATIVE")
        if samples[0]["accounting"] == "preserved_unclassified":
            flags.append("TAXONOMY_UNKNOWN")
        result.append(
            {
                "review_priority": 1 if any(flag in flags for flag in ("MIXED_LABELS", "VERY_LONG_TEMPLATE", "AMBIGUOUS_PARAM", "TAXONOMY_UNKNOWN")) else 2 if "SINGLE_ORACLE_SAMPLE" in flags else 3,
                "cluster_id": cluster_id,
                "source_family": model["source_family"],
                "oracle_sample_count": len(samples),
                "oracle_labels": label_text,
                "training_occurrences": model["support_occurrences"],
                "training_sessions": model["support_evidence_count"],
                "training_unique_sequences": model["unique_sequences"],
                "template": template,
                "example_1": samples[0]["message"],
                "example_2": samples[1]["message"] if len(samples) > 1 else (model["examples"][1] if len(model["examples"]) > 1 else ""),
                "flags": ";".join(flags),
                "template_identity_decision": "",
                "slot_decision_notes": "",
                "reviewer_notes": "",
            }
        )
    return sorted(
        result,
        key=lambda row: (
            row["review_priority"],
            -row["oracle_sample_count"],
            -row["training_occurrences"],
            row["source_family"],
        ),
    )


def slot_rows(clusters: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for cluster in clusters:
        matches = list(PLACEHOLDER_RE.finditer(cluster["template"]))
        for number, match in enumerate(matches, start=1):
            role = match.group("role")
            if role.startswith("ALT:"):
                suggested = "semantic_alternative"
            else:
                suggested = role.casefold()
            rows.append(
                {
                    "cluster_id": cluster["cluster_id"],
                    "source_family": cluster["source_family"],
                    "slot_number": number,
                    "left_context": cluster["template"][max(0, match.start() - 100) : match.start()],
                    "slot": match.group(0),
                    "right_context": cluster["template"][match.end() : match.end() + 100],
                    "suggested_role": suggested,
                    "oracle_labels": cluster["oracle_labels"],
                    "training_occurrences": cluster["training_occurrences"],
                    "example_1": cluster["example_1"],
                    "decision": "",
                    "replacement_role": "",
                    "reviewer_notes": "",
                }
            )
    role_rank = {"param": 0, "semantic_alternative": 1, "key": 2, "value": 3, "locator": 4}
    return sorted(
        rows,
        key=lambda row: (
            role_rank.get(row["suggested_role"], 5),
            -int(row["training_occurrences"]),
            row["cluster_id"],
            row["slot_number"],
        ),
    )


def write_executive_summary(
    path: Path,
    model: dict,
    sample_rows: list[dict],
    clusters: list[dict],
) -> None:
    assigned = [row for row in sample_rows if row["assignment"] == "assigned"]
    unknowns = [row for row in sample_rows if row["assignment"] == "unknown"]
    touched = {row["cluster_id"] for row in assigned}
    cluster_sizes = collections.Counter(row["cluster_id"] for row in assigned)
    shared_samples = sum(size for size in cluster_sizes.values() if size > 1)
    singleton_samples = sum(size for size in cluster_sizes.values() if size == 1)
    categories: dict[str, list[dict]] = collections.defaultdict(list)
    for row in sample_rows:
        categories[row["category"]].append(row)

    lines = [
        "# Executive review Ã¢â‚¬â€ empirical CK3 error templates",
        "",
        "## Decision summary",
        "",
        "The promising result is **structural grouping**, not end-to-end parser accuracy.",
        "The older 98.81% figure came from training on all archived sessions, including",
        "the frozen reference session. The stricter session-excluded v3 calibration is",
        f"**{len(assigned)}/252 assigned ({len(assigned)/252:.2%})**, with **{len(unknowns)} explicit unknowns**",
        f"and **{model['evaluation']['weighted_label_purity']:.2%} category/type purity among assigned samples**.",
        "The learner has not independently named those categories/types; human labels are",
        "used only afterward to test whether each cluster mixed unlike diagnostics.",
        "",
        "For comparison, the current production extractor is only **43/252 (17.06%)**",
        "exact across all normative fields and **89/252 (35.32%)** exact on category+type.",
        "",
        "## Purity sanity check",
        "",
        f"- Frozen samples assigned: **{len(assigned)}**",
        f"- Empirical clusters touched by those samples: **{len(touched)}**",
        f"- Samples sharing a cluster with another oracle sample: **{shared_samples}**",
        f"- Samples alone in their oracle-touched cluster: **{singleton_samples}**",
        f"- Mixed-label clusters: **{model['evaluation']['mixed_cluster_count']}**",
        "",
        "Singletons are not evidence of bad grouping, but they contribute trivially to",
        "purity. This is why false-split and slot-role review remain mandatory.",
        "",
        "## Category coverage",
        "",
        "| Category | Oracle samples | Assigned | Unknown | Touched clusters |",
        "|---|---:|---:|---:|---:|",
    ]
    for category in sorted(categories):
        rows = categories[category]
        category_assigned = [row for row in rows if row["assignment"] == "assigned"]
        lines.append(
            f"| {category} | {len(rows)} | {len(category_assigned)} | {len(rows)-len(category_assigned)} | {len({row['cluster_id'] for row in category_assigned})} |"
        )

    representative: list[dict] = []
    seen_categories: set[str] = set()
    for cluster in sorted(clusters, key=lambda row: (-row["oracle_sample_count"], -row["training_occurrences"])):
        category = cluster["oracle_labels"].split("/", 1)[0]
        if category not in seen_categories:
            representative.append(cluster)
            seen_categories.add(category)
        if len(representative) >= 12:
            break
    lines.extend(
        [
            "",
            "## Representative learned clusters",
            "",
            "| Source | Frozen label | Template | Training support |",
            "|---|---|---|---:|",
        ]
    )
    for row in representative:
        lines.append(
            f"| {markdown_cell(row['source_family'], 40)} | {markdown_cell(row['oracle_labels'], 55)} | {markdown_cell(row['template'], 220)} | {row['training_occurrences']:,} |"
        )

    lines.extend(
        [
            "",
            "## Recommended review order",
            "",
            "1. Review `UNKNOWN_QUEUE.md` (23 samples). Decide whether each is a novel",
            "   template, a normalization miss, or intentionally unknown taxonomy.",
            "2. Review priority 1 rows in `cluster_review.csv`: long templates, `<PARAM>`",
            "   slots, taxonomy unknowns, and any future mixed clusters.",
            "3. Review `slot_role_review.csv`, starting with `param`, then",
            "   `semantic_alternative`, then `key`. Enter `accept` or `change` and a",
            "   replacement role; do not edit the evidence columns.",
            "4. Sample one cluster per category in `CLUSTER_EXAMPLES.md` and verify that",
            "   source prefix plus ordered semantic wordingÃ¢â‚¬â€not the key/locatorÃ¢â‚¬â€defines it.",
            "5. Only after those decisions, freeze an untouched newly captured session and",
            "   measure assignment, false merges, false splits, and revision churn.",
            "",
            "## What approval would mean",
            "",
            "Approval of a row means the displayed messages belong to one template and its",
            "placeholder roles are plausible. It does **not** yet approve production parser",
            "promotion, severity, attribution, or automatic taxonomy changes.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_unknown_queue(path: Path, unknowns: list[dict]) -> None:
    lines = [
        "# Unknown assignment queue",
        "",
        "These frozen samples did not match any cluster learned from the other five",
        "distinct archived sessions. Unknown is a safe outcome, not automatically a defect.",
        "",
    ]
    for number, row in enumerate(unknowns, start=1):
        lines.extend(
            [
                f"## {number}. `{row['sample_id']}` Ã¢â‚¬â€ `{row['source_family']}`",
                "",
                f"- Frozen judgment: `{row['category']}/{row['error_type']}`",
                f"- Message: `{markdown_cell(row['message'], 600)}`",
                f"- Evidence: {markdown_cell(row['evidence'], 400)}",
                f"- Oracle uncertainty: {markdown_cell(row['uncertainty'] or 'none', 400)}",
                "- Reviewer decision: `[ ] novel template  [ ] normalization miss  [ ] intentionally unknown  [ ] investigate`",
                "- Notes:",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_cluster_examples(path: Path, clusters: list[dict]) -> None:
    lines = [
        "# Frozen-sample cluster examples",
        "",
        "Only clusters touched by the 252 frozen samples appear here. Complete editable",
        "fields and risk flags are in `cluster_review.csv`.",
        "",
    ]
    for row in clusters:
        lines.extend(
            [
                f"## `{row['cluster_id']}` Ã¢â‚¬â€ `{row['source_family']}`",
                "",
                f"- Frozen labels: {row['oracle_labels']}",
                f"- Frozen samples: {row['oracle_sample_count']}; training occurrences: {row['training_occurrences']:,}; training sessions: {row['training_sessions']}",
                f"- Flags: `{row['flags'] or 'none'}`",
                f"- Template: `{markdown_cell(row['template'], 1000)}`",
                f"- Example 1: `{markdown_cell(row['example_1'], 1000)}`",
                f"- Example 2: `{markdown_cell(row['example_2'] or 'none', 1000)}`",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--oracle-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    model = load_json(args.model)
    candidate = load_json(args.oracle_root / "SEMANTIC_CALIBRATION_SAMPLE_CANDIDATE.json")
    oracle = load_json(args.oracle_root / "SEMANTIC_LABELS_ADJUDICATED.json")
    by_source, cluster_model = reconstruct_clusters(model)
    samples = map_samples(model, candidate, oracle, by_source, cluster_model)
    clusters = cluster_rows(samples, cluster_model)
    slots = slot_rows(clusters)
    unknowns = [row for row in samples if row["assignment"] == "unknown"]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_executive_summary(args.output_dir / "EXECUTIVE_SUMMARY.md", model, samples, clusters)
    write_unknown_queue(args.output_dir / "UNKNOWN_QUEUE.md", unknowns)
    write_cluster_examples(args.output_dir / "CLUSTER_EXAMPLES.md", clusters)
    write_csv(
        args.output_dir / "sample_assignments.csv",
        samples,
        list(samples[0]),
    )
    write_csv(
        args.output_dir / "cluster_review.csv",
        clusters,
        list(clusters[0]),
    )
    write_csv(
        args.output_dir / "slot_role_review.csv",
        slots,
        list(slots[0]),
    )
    manifest = {
        "schema": "ck3chronicle.template-review-pack",
        "schema_version": 1,
        "model": str(args.model),
        "model_evidence_sha256": model["excluded_evidence"][0]["sha256"],
        "samples": len(samples),
        "assigned": len(samples) - len(unknowns),
        "unknown": len(unknowns),
        "oracle_touched_clusters": len(clusters),
        "slot_decisions": len(slots),
        "status": "human_review_required",
    }
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
