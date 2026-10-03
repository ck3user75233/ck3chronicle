"""Re-evaluate the frozen blind sample against the corrected v4 model."""
from __future__ import annotations

import collections
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import evaluate_unseen_session as unseen
import learn_error_templates as learner
from ck3chronicle.parser.log_blocks import iter_log_blocks


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BLIND = ROOT / "local-data" / "blind_adjudication"
HOLDOUT = ROOT / "local-data" / "holdout" / "error.log"
MODEL = ROOT.parents[1] / "models" / "93196794a7e0115d" / "empirical_template_model.json"
LABELS = ROOT / "local-data" / "review" / "sample_assignments.csv"

# These four pairs were split only because the blind adjudicator treated one
# repeated clause versus two repeated clauses as different templates.  The
# user subsequently ruled that repetition count is occurrence cardinality.
USER_APPROVED_SAME_PAIR_OVERRIDES = {
    "split-05",
    "split-06",
    "split-07",
    "split-08",
}

# Independent-adjudication groups covered by the user's explicit parameter
# rules.  This mapping is confined to evaluation of the frozen sample; it is
# not used by the learner to assign clusters.
USER_POLICY_EQUIVALENCE_GROUPS = (
    ("ITG-004", "ITG-005", "ITG-028", "ITG-033"),  # failed key reference
    ("ITG-007", "ITG-014", "ITG-036"),  # unknown trigger repetition
    ("ITG-018", "ITG-024", "ITG-034"),  # optional Historical ID key
)

# The paired sample was designed to challenge suspected splits/merges, not to
# supply negative controls after the user's rulings.  Preserve explicit
# semantic-separation gates with independently selected blind rows.
NEGATIVE_CONTROLS = (
    ("negative-undefined-vs-unset", "U12-017-90cac25c", "U12-009-c9c4bcd7"),
    ("negative-never-set-vs-never-used", "U12-002-2507272a", "U12-087-0c863d7f"),
    ("negative-trigger-vs-key-reference", "U12-057-54968b6f", "U12-004-7917e369"),
    ("negative-missing-vs-duplicate-loc", "U12-006-41cc89b3", "U12-030-6e1f4a77"),
)


class Groups:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, value: str) -> str:
        self.parent.setdefault(value, value)
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, left: str, right: str) -> None:
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_messages() -> dict[str, list[str]]:
    by_source: dict[str, list[str]] = collections.defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for block in iter_log_blocks(HOLDOUT, log_relpath="error.log"):
        if block.timestamp is None:
            continue
        message = learner.block_message(block)
        key = (block.source_family, message)
        if message and key not in seen:
            seen.add(key)
            by_source[block.source_family].append(message)
    return dict(by_source)


def resolve_full_message(source: str, sample_message: str, messages: dict[str, list[str]]) -> str:
    exact = [message for message in messages.get(source, []) if message == sample_message]
    if exact:
        return exact[0]
    prefixed = [message for message in messages.get(source, []) if message.startswith(sample_message)]
    if prefixed:
        return min(prefixed, key=len)
    reverse = [message for message in messages.get(source, []) if sample_message.startswith(message)]
    if reverse:
        return max(reverse, key=len)
    raise ValueError(f"cannot resolve blind message {source}: {sample_message[:120]}")


def cluster_labels() -> dict[str, tuple[str, str]]:
    distributions: dict[str, set[tuple[str, str]]] = collections.defaultdict(set)
    with LABELS.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["cluster_id"]:
                distributions[row["cluster_id"]].add((row["category"], row["error_type"]))
    return {
        cluster_id: next(iter(labels))
        for cluster_id, labels in distributions.items()
        if len(labels) == 1
    }


def main() -> int:
    model = load(MODEL)
    clusters_by_source, model_by_id = unseen.reconstruct_model(model)
    threshold = float(model["algorithm"]["cluster_threshold"])
    sample = load(BLIND / "BLIND_SAMPLE.json")
    linkage = load(BLIND / "PRIVATE_LINKAGE.json")
    adjudication = load(BLIND / "INDEPENDENT_ADJUDICATION.json")
    sample_by_id = {row["blind_id"]: row for row in sample["samples"]}
    link_by_id = {row["blind_id"]: row for row in linkage["rows"]}
    adjud_by_id = {row["blind_id"]: row for row in adjudication["annotations"]}
    if set(sample_by_id) != set(link_by_id) or set(sample_by_id) != set(adjud_by_id):
        raise ValueError("blind artifacts do not account for identical IDs")

    messages = source_messages()
    rows: list[dict] = []
    for blind_id in sorted(sample_by_id):
        blind = sample_by_id[blind_id]
        full = resolve_full_message(blind["source_family"], blind["message"], messages)
        units = learner.semantic_units(blind["source_family"], full)
        assignments: list[dict] = []
        for unit in units:
            cluster = learner.best_cluster(
                clusters_by_source,
                blind["source_family"],
                learner.tokenize(unit),
                learner.diagnostic_lead(unit),
                threshold,
            )
            assignments.append(
                {
                    "unit": unit,
                    "cluster_id": cluster.cluster_id if cluster else None,
                    "template": model_by_id[cluster.cluster_id]["template"] if cluster else None,
                }
            )
        cluster_ids = sorted({item["cluster_id"] for item in assignments if item["cluster_id"]})
        rows.append(
            {
                "blind_id": blind_id,
                "sample": blind,
                "linkage": link_by_id[blind_id],
                "adjudication": adjud_by_id[blind_id],
                "full_message": full,
                "semantic_units": assignments,
                "v4_cluster_ids": cluster_ids,
                "v4_assignment": (
                    "assigned" if len(cluster_ids) == 1 and all(item["cluster_id"] for item in assignments)
                    else "unknown" if not cluster_ids
                    else "multi_or_partial"
                ),
            }
        )

    by_id = {row["blind_id"]: row for row in rows}
    pair_members: dict[str, list[dict]] = collections.defaultdict(list)
    for row in rows:
        pair_id = row["linkage"].get("pair_id", "")
        if pair_id:
            pair_members[pair_id].append(row)

    policy_groups = Groups()
    for equivalence_group in USER_POLICY_EQUIVALENCE_GROUPS:
        for member in equivalence_group[1:]:
            policy_groups.union(equivalence_group[0], member)
    pair_results: list[dict] = []
    for pair_id, members in sorted(pair_members.items()):
        if len(members) != 2:
            raise ValueError(f"{pair_id} has {len(members)} members")
        left_group = members[0]["adjudication"]["template_group_id"]
        right_group = members[1]["adjudication"]["template_group_id"]
        if pair_id.startswith("within-"):
            # User-ratified contract: repetition cardinality and optional
            # identity metadata never create a different base template.
            expected_same = True
            policy_groups.union(left_group, right_group)
        else:
            expected_same = (
                left_group == right_group
                or pair_id in USER_APPROVED_SAME_PAIR_OVERRIDES
            )
            if expected_same:
                policy_groups.union(left_group, right_group)
        left_clusters, right_clusters = members[0]["v4_cluster_ids"], members[1]["v4_cluster_ids"]
        observed_same = (
            len(left_clusters) == 1
            and len(right_clusters) == 1
            and left_clusters[0] == right_clusters[0]
        )
        correct = observed_same if expected_same else (
            len(left_clusters) == 1
            and len(right_clusters) == 1
            and left_clusters[0] != right_clusters[0]
        )
        pair_results.append(
            {
                "pair_id": pair_id,
                "expected_relationship": "same" if expected_same else "different",
                "v4_relationship": "same" if observed_same else "different_or_unassigned",
                "correct": correct,
                "source_family": members[0]["sample"]["source_family"],
                "v4_cluster_ids": [left_clusters, right_clusters],
                "v4_templates": [
                    [item["template"] for item in member["semantic_units"]]
                    for member in members
                ],
                "messages": [member["sample"]["message"] for member in members],
            }
        )

    for pair_id, left_id, right_id in NEGATIVE_CONTROLS:
        members = [by_id[left_id], by_id[right_id]]
        left_clusters, right_clusters = members[0]["v4_cluster_ids"], members[1]["v4_cluster_ids"]
        observed_different = (
            len(left_clusters) == 1
            and len(right_clusters) == 1
            and left_clusters[0] != right_clusters[0]
        )
        pair_results.append(
            {
                "pair_id": pair_id,
                "expected_relationship": "different",
                "v4_relationship": "different" if observed_different else "same_or_unassigned",
                "correct": observed_different,
                "source_family": [
                    members[0]["sample"]["source_family"],
                    members[1]["sample"]["source_family"],
                ],
                "v4_cluster_ids": [left_clusters, right_clusters],
                "v4_templates": [
                    [item["template"] for item in member["semantic_units"]]
                    for member in members
                ],
                "messages": [member["sample"]["message"] for member in members],
            }
        )

    assigned_rows = [row for row in rows if row["v4_assignment"] == "assigned"]
    by_cluster: dict[str, list[str]] = collections.defaultdict(list)
    for row in assigned_rows:
        group = policy_groups.find(row["adjudication"]["template_group_id"])
        by_cluster[row["v4_cluster_ids"][0]].append(group)
    pure = sum(collections.Counter(groups).most_common(1)[0][1] for groups in by_cluster.values())
    impure = [
        {
            "cluster_id": cluster_id,
            "distribution": dict(collections.Counter(groups)),
            "template": model_by_id[cluster_id]["template"],
        }
        for cluster_id, groups in by_cluster.items()
        if len(set(groups)) > 1
    ]

    labels = cluster_labels()
    label_rows = [
        row for row in assigned_rows if row["v4_cluster_ids"][0] in labels
    ]
    category_exact = [
        row
        for row in label_rows
        if labels[row["v4_cluster_ids"][0]][0] == row["adjudication"]["category"]
    ]
    type_exact = [
        row
        for row in label_rows
        if labels[row["v4_cluster_ids"][0]]
        == (row["adjudication"]["category"], row["adjudication"]["error_type"])
    ]
    same_pairs = [row for row in pair_results if row["expected_relationship"] == "same"]
    different_pairs = [row for row in pair_results if row["expected_relationship"] == "different"]
    result = {
        "schema": "ck3chronicle.postfix-blind-sample-evaluation",
        "schema_version": 1,
        "status": "complete_development_retest_not_new_holdout",
        "model_sha256": unseen.sha256_file(MODEL),
        "holdout_sha256": unseen.sha256_file(HOLDOUT),
        "metrics": {
            "blind_rows": len(rows),
            "assigned_rows": len(assigned_rows),
            "unknown_rows": sum(row["v4_assignment"] == "unknown" for row in rows),
            "multi_or_partial_rows": sum(row["v4_assignment"] == "multi_or_partial" for row in rows),
            "policy_adjusted_template_purity": pure / len(assigned_rows) if assigned_rows else 0.0,
            "impure_v4_clusters": len(impure),
            "expected_same_pairs": len(same_pairs),
            "correct_same_pairs": sum(row["correct"] for row in same_pairs),
            "expected_different_pairs": len(different_pairs),
            "correct_different_pairs": sum(row["correct"] for row in different_pairs),
            "all_pair_gates_correct": all(row["correct"] for row in pair_results),
            "label_evaluable_rows": len(label_rows),
            "category_exact_rows": len(category_exact),
            "category_type_exact_rows": len(type_exact),
            "category_exact_rate": len(category_exact) / len(label_rows) if label_rows else None,
            "category_type_exact_rate": len(type_exact) / len(label_rows) if label_rows else None,
        },
        "pair_results": pair_results,
        "pair_failures": [row for row in pair_results if not row["correct"]],
        "semantic_label_mismatches": [
            {
                "blind_id": row["blind_id"],
                "source_family": row["sample"]["source_family"],
                "message": row["sample"]["message"],
                "expected": {
                    "category": row["adjudication"]["category"],
                    "error_type": row["adjudication"]["error_type"],
                },
                "predicted": {
                    "category": labels[row["v4_cluster_ids"][0]][0],
                    "error_type": labels[row["v4_cluster_ids"][0]][1],
                },
            }
            for row in label_rows
            if labels[row["v4_cluster_ids"][0]]
            != (row["adjudication"]["category"], row["adjudication"]["error_type"])
        ],
        "impure_clusters": impure,
        "unassigned_rows": [
            {
                "blind_id": row["blind_id"],
                "source_family": row["sample"]["source_family"],
                "message": row["sample"]["message"],
                "prior_stratum": row["linkage"]["selection_stratum"],
            }
            for row in rows
            if row["v4_assignment"] != "assigned"
        ],
    }
    output = HERE / "POST_FIX_V4_BLIND_RETEST.json"
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    metrics = result["metrics"]
    lines = [
        "# Post-fix v4 retest of the frozen 96-pattern audit",
        "",
        "This is a development retest, not a new untouched holdout.",
        "",
        f"- Assigned / unknown / multi-partial: **{metrics['assigned_rows']} / {metrics['unknown_rows']} / {metrics['multi_or_partial_rows']}**",
        f"- Policy-adjusted template purity: **{metrics['policy_adjusted_template_purity']:.2%}**",
        f"- Expected-same pair gates: **{metrics['correct_same_pairs']}/{metrics['expected_same_pairs']}**",
        f"- Expected-different pair gates: **{metrics['correct_different_pairs']}/{metrics['expected_different_pairs']}**",
        f"- All pair gates correct: **{metrics['all_pair_gates_correct']}**",
        f"- Category exact: **{metrics['category_exact_rows']}/{metrics['label_evaluable_rows']} ({metrics['category_exact_rate']:.2%})**",
        f"- Category + type exact: **{metrics['category_type_exact_rows']}/{metrics['label_evaluable_rows']} ({metrics['category_type_exact_rate']:.2%})**",
        "",
        "## Pair failures",
        "",
    ]
    if not result["pair_failures"]:
        lines.append("None.")
    for failure in result["pair_failures"]:
        lines.extend(
            [
                f"### `{failure['pair_id']}` Ã¢â‚¬â€ expected {failure['expected_relationship']}",
                "",
                f"- V4 relationship: {failure['v4_relationship']}",
                f"- Cluster IDs: `{failure['v4_cluster_ids']}`",
                "",
            ]
        )
    (HERE / "POST_FIX_V4_BLIND_RETEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
