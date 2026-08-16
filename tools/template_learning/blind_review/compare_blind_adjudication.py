"""Compare frozen learner assignments with completed independent adjudication."""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "local-data" / "blind_adjudication"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(sample: dict, linkage: dict, adjudication: dict) -> None:
    expected = [row["blind_id"] for row in sample["samples"]]
    linked = [row["blind_id"] for row in linkage["rows"]]
    actual = [row["blind_id"] for row in adjudication["annotations"]]
    if len(expected) != 96 or len(set(expected)) != 96:
        raise ValueError("blind sample must contain 96 unique IDs")
    if set(linked) != set(expected) or len(linked) != len(expected):
        raise ValueError("private linkage does not exactly account for blind sample")
    if set(actual) != set(expected) or len(actual) != len(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        duplicates = sorted(key for key, count in collections.Counter(actual).items() if count > 1)
        raise ValueError(f"adjudication accounting failure missing={missing} extra={extra} duplicates={duplicates}")
    required = {
        "blind_id",
        "template_group_id",
        "semantic_template",
        "category",
        "error_type",
        "severity",
        "confidence",
        "slot_notes",
        "rationale",
    }
    for row in adjudication["annotations"]:
        absent = required - set(row)
        if absent:
            raise ValueError(f"{row.get('blind_id')} missing fields {sorted(absent)}")
        if not str(row["template_group_id"]).strip() or not str(row["semantic_template"]).strip():
            raise ValueError(f"{row['blind_id']} has empty template judgment")


def pair_results(rows: list[dict], prefix: str, expected_same: bool) -> list[dict]:
    grouped: dict[str, list[dict]] = collections.defaultdict(list)
    for row in rows:
        pair_id = row["linkage"].get("pair_id", "")
        if pair_id.startswith(prefix):
            grouped[pair_id].append(row)
    results: list[dict] = []
    for pair_id, members in sorted(grouped.items()):
        if len(members) != 2:
            raise ValueError(f"pair {pair_id} has {len(members)} rows")
        adjudicator_same = members[0]["adjudication"]["template_group_id"] == members[1]["adjudication"]["template_group_id"]
        correct = adjudicator_same == expected_same
        results.append(
            {
                "pair_id": pair_id,
                "expected_relationship": "same" if expected_same else "different",
                "adjudicator_relationship": "same" if adjudicator_same else "different",
                "learner_correct": correct,
                "source_family": members[0]["sample"]["source_family"],
                "learner_cluster_ids": [member["linkage"].get("cluster_id", "") for member in members],
                "adjudicated_group_ids": [member["adjudication"]["template_group_id"] for member in members],
                "messages": [member["sample"]["message"] for member in members],
                "adjudicated_templates": [member["adjudication"]["semantic_template"] for member in members],
            }
        )
    return results


def main() -> int:
    sample_path = ROOT / "BLIND_SAMPLE.json"
    linkage_path = ROOT / "PRIVATE_LINKAGE.json"
    adjudication_path = ROOT / "INDEPENDENT_ADJUDICATION.json"
    manifest = load(ROOT / "SAMPLE_MANIFEST.json")
    if sha256(sample_path) != manifest["sample_sha256"]:
        raise ValueError("blind sample hash changed")
    if sha256(linkage_path) != manifest["linkage_sha256"]:
        raise ValueError("private linkage hash changed")

    sample = load(sample_path)
    linkage = load(linkage_path)
    adjudication = load(adjudication_path)
    validate(sample, linkage, adjudication)

    sample_by_id = {row["blind_id"]: row for row in sample["samples"]}
    link_by_id = {row["blind_id"]: row for row in linkage["rows"]}
    adjudication_by_id = {row["blind_id"]: row for row in adjudication["annotations"]}
    joined = [
        {
            "sample": sample_by_id[blind_id],
            "linkage": link_by_id[blind_id],
            "adjudication": adjudication_by_id[blind_id],
        }
        for blind_id in sorted(sample_by_id)
    ]

    within = pair_results(joined, "within-", expected_same=True)
    split = pair_results(joined, "split-", expected_same=False)
    false_merges = [row for row in within if not row["learner_correct"]]
    false_splits = [row for row in split if not row["learner_correct"]]

    label_rows = [
        row
        for row in joined
        if row["linkage"].get("assignment") == "assigned"
        and row["linkage"].get("frozen_label")
    ]
    label_exact = [
        row
        for row in label_rows
        if tuple(row["linkage"]["frozen_label"])
        == (row["adjudication"]["category"], row["adjudication"]["error_type"])
    ]
    category_exact = [
        row
        for row in label_rows
        if row["linkage"]["frozen_label"][0] == row["adjudication"]["category"]
    ]
    label_occurrences = sum(row["sample"]["occurrences_in_session"] for row in label_rows)
    label_exact_occurrences = sum(row["sample"]["occurrences_in_session"] for row in label_exact)

    assigned = [row for row in joined if row["linkage"].get("assignment") == "assigned"]
    cluster_groups: dict[str, list[str]] = collections.defaultdict(list)
    for row in assigned:
        cluster_groups[row["linkage"]["cluster_id"]].append(row["adjudication"]["template_group_id"])
    template_pure_samples = sum(collections.Counter(groups).most_common(1)[0][1] for groups in cluster_groups.values())
    impure_clusters = [
        {
            "cluster_id": cluster_id,
            "sample_count": len(groups),
            "adjudicated_groups": [
                {"template_group_id": group, "count": count}
                for group, count in collections.Counter(groups).most_common()
            ],
        }
        for cluster_id, groups in cluster_groups.items()
        if len(set(groups)) > 1
    ]

    reviewer_groups: dict[str, set[str]] = collections.defaultdict(set)
    reviewer_group_samples: dict[str, int] = collections.Counter()
    for row in assigned:
        group = row["adjudication"]["template_group_id"]
        reviewer_groups[group].add(row["linkage"]["cluster_id"])
        reviewer_group_samples[group] += 1
    fragmented_groups = [
        {
            "template_group_id": group,
            "sample_count": reviewer_group_samples[group],
            "learner_cluster_ids": sorted(cluster_ids),
        }
        for group, cluster_ids in reviewer_groups.items()
        if len(cluster_ids) > 1
    ]

    metrics = {
        "blind_samples": len(joined),
        "learner_assigned_samples": len(assigned),
        "learner_unknown_samples": len(joined) - len(assigned),
        "targeted_same_template_pairs": len(within),
        "targeted_false_merges": len(false_merges),
        "targeted_same_template_pair_accuracy": (len(within) - len(false_merges)) / len(within),
        "targeted_different_template_pairs": len(split),
        "targeted_false_splits": len(false_splits),
        "targeted_different_template_pair_accuracy": (len(split) - len(false_splits)) / len(split),
        "assigned_template_group_purity": template_pure_samples / len(assigned) if assigned else 0.0,
        "impure_sampled_learner_clusters": len(impure_clusters),
        "fragmented_adjudicated_groups": len(fragmented_groups),
        "independently_labelable_assignments": len(label_rows),
        "category_exact_samples": len(category_exact),
        "category_exact_rate": len(category_exact) / len(label_rows) if label_rows else None,
        "category_type_exact_samples": len(label_exact),
        "category_type_exact_rate": len(label_exact) / len(label_rows) if label_rows else None,
        "category_type_exact_occurrences": label_exact_occurrences,
        "label_evaluable_occurrences": label_occurrences,
        "category_type_exact_occurrence_weighted_rate": label_exact_occurrences / label_occurrences if label_occurrences else None,
    }
    result = {
        "schema": "ck3chronicle.blind-template-comparison",
        "schema_version": 1,
        "status": "complete",
        "provenance": {
            "sample_sha256": sha256(sample_path),
            "linkage_sha256": sha256(linkage_path),
            "adjudication_sha256": sha256(adjudication_path),
        },
        "metrics": metrics,
        "false_merges": false_merges,
        "false_splits": false_splits,
        "impure_clusters": impure_clusters,
        "fragmented_groups": fragmented_groups,
        "label_mismatches": [
            {
                "blind_id": row["sample"]["blind_id"],
                "source_family": row["sample"]["source_family"],
                "message": row["sample"]["message"],
                "frozen_learner_label": row["linkage"]["frozen_label"],
                "independent_label": [row["adjudication"]["category"], row["adjudication"]["error_type"]],
                "independent_template": row["adjudication"]["semantic_template"],
                "rationale": row["adjudication"]["rationale"],
            }
            for row in label_rows
            if row not in label_exact
        ],
    }
    output_json = ROOT / "BLIND_COMPARISON.json"
    output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Independent blind template audit",
        "",
        f"- Blind patterns adjudicated: **{metrics['blind_samples']}**",
        f"- Learner assigned / unknown in sample: **{metrics['learner_assigned_samples']} / {metrics['learner_unknown_samples']}**",
        f"- Targeted false merges: **{metrics['targeted_false_merges']}/{metrics['targeted_same_template_pairs']}**",
        f"- Targeted false splits: **{metrics['targeted_false_splits']}/{metrics['targeted_different_template_pairs']}**",
        f"- Blind template-group purity among assigned sampled rows: **{metrics['assigned_template_group_purity']:.2%}**",
        f"- Independently label-evaluable assignments: **{metrics['independently_labelable_assignments']}**",
        f"- Category exact: **{metrics['category_exact_samples']}/{metrics['independently_labelable_assignments']} ({metrics['category_exact_rate']:.2%})**",
        f"- Category + type exact: **{metrics['category_type_exact_samples']}/{metrics['independently_labelable_assignments']} ({metrics['category_type_exact_rate']:.2%})**",
        f"- Category + type exact, occurrence-weighted: **{metrics['category_type_exact_occurrence_weighted_rate']:.2%}**",
        "",
        "The 96-row sample is deliberately stratified toward difficult boundaries and",
        "candidate merge/split errors; it is not a prevalence-weighted random sample.",
        "Occurrence-weighted semantic agreement is reported separately and should not",
        "replace the sample-level result.",
        "",
        "## False merges",
        "",
    ]
    if not false_merges:
        lines.append("None in the 16 targeted same-cluster pairs.")
    for row in false_merges:
        lines.extend([f"### `{row['pair_id']}` Ã¢â‚¬â€ `{row['source_family']}`", ""])
        for message, template in zip(row["messages"], row["adjudicated_templates"]):
            lines.append(f"- `{message[:500]}`")
            lines.append(f"  - Independent template: `{template}`")
        lines.append("")
    lines.extend(["## False splits", ""])
    if not false_splits:
        lines.append("None in the 8 targeted cross-cluster pairs.")
    for row in false_splits:
        lines.extend([f"### `{row['pair_id']}` Ã¢â‚¬â€ `{row['source_family']}`", ""])
        for message, template in zip(row["messages"], row["adjudicated_templates"]):
            lines.append(f"- `{message[:500]}`")
            lines.append(f"  - Independent template: `{template}`")
        lines.append("")
    lines.extend(["## Semantic-label mismatches", ""])
    if not result["label_mismatches"]:
        lines.append("None among independently label-evaluable assignments.")
    for row in result["label_mismatches"]:
        lines.extend(
            [
                f"### `{row['blind_id']}` Ã¢â‚¬â€ `{row['source_family']}`",
                "",
                f"- Frozen cluster label: `{row['frozen_learner_label'][0]}/{row['frozen_learner_label'][1]}`",
                f"- Independent label: `{row['independent_label'][0]}/{row['independent_label'][1]}`",
                f"- Message: `{row['message'][:600]}`",
                f"- Rationale: {row['rationale']}",
                "",
            ]
        )
    (ROOT / "BLIND_AUDIT_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
