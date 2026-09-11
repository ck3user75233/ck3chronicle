"""Freeze a deterministic, blinded sample for independent template review."""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import evaluate_unseen_session as unseen
import learn_error_templates as learner


ROOT = Path(__file__).resolve().parent.parent
HOLDOUT = ROOT / "local-data" / "holdout" / "error.log"
MODEL_PATH = ROOT.parents[1] / "models" / "93196794a7e0115d" / "empirical_template_model.json"
ORACLE_ASSIGNMENTS = ROOT / "local-data" / "review" / "sample_assignments.csv"
OUTPUT = ROOT / "evaluation-results" / "blind_adjudication"
HOLDOUT_SHA256 = "eb2f32b800364c6eceacbdb993d0164e8959cafc18cd6a9869912bd2d444e34a"


def stable_key(*values: object) -> str:
    material = "\0".join(str(value) for value in values)
    return hashlib.sha256((HOLDOUT_SHA256 + "\0" + material).encode()).hexdigest()


def model_label_map() -> dict[str, tuple[str, str]]:
    import csv

    labels: dict[str, set[tuple[str, str]]] = collections.defaultdict(set)
    with ORACLE_ASSIGNMENTS.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if row["cluster_id"]:
                labels[row["cluster_id"]].add((row["category"], row["error_type"]))
    return {
        cluster_id: next(iter(values))
        for cluster_id, values in labels.items()
        if len(values) == 1
    }


def ranked_matches(record: dict, clusters_by_source: dict[str, list[learner.TemplateCluster]]) -> list[tuple[float, learner.TemplateCluster]]:
    ranked: list[tuple[float, learner.TemplateCluster]] = []
    for cluster in clusters_by_source.get(record["source_family"], []):
        assert cluster.medoid is not None
        if cluster.medoid.semantic_lead != record["semantic_lead"]:
            continue
        if not learner.has_ordered_anchor_overlap(cluster.medoid.tokens, record["tokens"]):
            continue
        score = learner.sequence_similarity(cluster.medoid.tokens, record["tokens"])
        ranked.append((score, cluster))
    return sorted(ranked, key=lambda item: (-item[0], item[1].cluster_id))


def select_with_source_cap(candidates: list[dict], count: int, cap: int, already: set[str]) -> list[dict]:
    selected: list[dict] = []
    by_source = collections.Counter()
    for item in candidates:
        if item["sequence_id"] in already or by_source[item["source_family"]] >= cap:
            continue
        selected.append(item)
        already.add(item["sequence_id"])
        by_source[item["source_family"]] += 1
        if len(selected) == count:
            break
    if len(selected) < count:
        for item in candidates:
            if item["sequence_id"] in already:
                continue
            selected.append(item)
            already.add(item["sequence_id"])
            if len(selected) == count:
                break
    return selected


def main() -> int:
    if unseen.sha256_file(HOLDOUT) != HOLDOUT_SHA256:
        raise ValueError("holdout hash changed")
    model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    clusters_by_source, cluster_model = unseen.reconstruct_model(model)
    records, timestamped = unseen.inference_records(HOLDOUT)
    threshold = float(model["algorithm"]["cluster_threshold"])
    frozen_labels = model_label_map()

    rows: list[dict] = []
    for record in records.values():
        ranked = ranked_matches(record, clusters_by_source)
        assigned = ranked and ranked[0][0] >= threshold
        cluster_id = ranked[0][1].cluster_id if assigned else ""
        score = ranked[0][0] if ranked else 0.0
        second_score = ranked[1][0] if len(ranked) > 1 else 0.0
        sequence_material = record["source_family"] + "\0" + " ".join(record["tokens"])
        sequence_id = hashlib.sha256(sequence_material.encode()).hexdigest()[:20]
        rows.append(
            {
                "sequence_id": sequence_id,
                "source_family": record["source_family"],
                "semantic_lead": list(record["semantic_lead"]),
                "tokens": list(record["tokens"]),
                "occurrences": int(record["occurrences"]),
                "message": record["example"],
                "assignment": "assigned" if assigned else "unknown",
                "cluster_id": cluster_id,
                "score": score,
                "margin": score - second_score,
                "frozen_label": list(frozen_labels[cluster_id]) if cluster_id in frozen_labels else None,
            }
        )

    assigned_rows = [row for row in rows if row["assignment"] == "assigned"]
    unknown_rows = [row for row in rows if row["assignment"] == "unknown"]
    by_cluster: dict[str, list[dict]] = collections.defaultdict(list)
    for row in assigned_rows:
        by_cluster[row["cluster_id"]].append(row)

    selected: list[dict] = []
    selected_ids: set[str] = set()

    pair_candidates = [
        (sum(row["occurrences"] for row in members), cluster_id, members)
        for cluster_id, members in by_cluster.items()
        if len(members) >= 2
    ]
    pair_candidates.sort(key=lambda item: (-item[0], stable_key("within", item[1])))
    pair_source_counts = collections.Counter()
    pair_clusters = 0
    for _, cluster_id, members in pair_candidates:
        source = members[0]["source_family"]
        if pair_source_counts[source] >= 5:
            continue
        ordered = sorted(members, key=lambda row: (-row["occurrences"], row["score"], stable_key(row["sequence_id"])))
        choices = [ordered[0], min(ordered[1:], key=lambda row: (row["score"], stable_key(row["sequence_id"])))]
        if any(row["sequence_id"] in selected_ids for row in choices):
            continue
        for row in choices:
            copy = dict(row)
            copy["selection_stratum"] = "within_cluster_pair"
            copy["pair_id"] = f"within-{cluster_id}"
            selected.append(copy)
            selected_ids.add(row["sequence_id"])
        pair_source_counts[source] += 1
        pair_clusters += 1
        if pair_clusters == 16:
            break
    if pair_clusters < 16:
        raise ValueError(f"insufficient within-cluster pairs: {pair_clusters}")

    # Candidate false splits: different frozen clusters, same source and lead,
    # with high direct sequence similarity. The adjudicator sees no pair data.
    split_pairs: list[tuple[float, dict, dict]] = []
    grouped: dict[tuple[str, tuple[str, ...]], list[dict]] = collections.defaultdict(list)
    for row in assigned_rows:
        grouped[(row["source_family"], tuple(row["semantic_lead"]))].append(row)
    for group in grouped.values():
        available = sorted(group, key=lambda row: (-row["occurrences"], row["sequence_id"]))[:80]
        for left_index, left in enumerate(available):
            for right in available[left_index + 1 :]:
                if left["cluster_id"] == right["cluster_id"]:
                    continue
                similarity = learner.sequence_similarity(left["tokens"], right["tokens"])
                if similarity >= 0.62:
                    split_pairs.append((similarity, left, right))
    split_pairs.sort(key=lambda item: (-item[0], stable_key("split", item[1]["sequence_id"], item[2]["sequence_id"])))
    split_source_counts = collections.Counter()
    split_count = 0
    for similarity, left, right in split_pairs:
        source = left["source_family"]
        if split_source_counts[source] >= 4 or left["sequence_id"] in selected_ids or right["sequence_id"] in selected_ids:
            continue
        pair_id = f"split-{split_count + 1:02d}"
        for row in (left, right):
            copy = dict(row)
            copy["selection_stratum"] = "cross_cluster_pair"
            copy["pair_id"] = pair_id
            copy["pair_similarity"] = similarity
            selected.append(copy)
            selected_ids.add(row["sequence_id"])
        split_source_counts[source] += 1
        split_count += 1
        if split_count == 8:
            break
    if split_count < 8:
        raise ValueError(f"insufficient cross-cluster pairs: {split_count}")

    boundary_candidates = sorted(
        assigned_rows,
        key=lambda row: (row["score"], row["margin"], stable_key("boundary", row["sequence_id"])),
    )
    for row in select_with_source_cap(boundary_candidates, 16, 6, selected_ids):
        copy = dict(row)
        copy["selection_stratum"] = "assignment_boundary"
        copy["pair_id"] = ""
        selected.append(copy)

    breadth_candidates = sorted(
        assigned_rows,
        key=lambda row: (row["source_family"], stable_key("breadth", row["sequence_id"])),
    )
    for row in select_with_source_cap(breadth_candidates, 16, 2, selected_ids):
        copy = dict(row)
        copy["selection_stratum"] = "source_breadth"
        copy["pair_id"] = ""
        selected.append(copy)

    known_unknown = sorted(
        [row for row in unknown_rows if row["source_family"] in clusters_by_source],
        key=lambda row: (-row["occurrences"], stable_key("known-unknown", row["sequence_id"])),
    )
    new_source = sorted(
        [row for row in unknown_rows if row["source_family"] not in clusters_by_source],
        key=lambda row: (row["source_family"], -row["occurrences"], stable_key("new-source", row["sequence_id"])),
    )
    unknown_selection = select_with_source_cap(known_unknown, 8, 5, selected_ids)
    unknown_selection += select_with_source_cap(new_source, 8, 4, selected_ids)
    for row in unknown_selection:
        copy = dict(row)
        copy["selection_stratum"] = "unknown_pattern"
        copy["pair_id"] = ""
        selected.append(copy)

    if len(selected) != 96 or len(selected_ids) != 96:
        raise ValueError(f"expected 96 unique rows, got {len(selected)}/{len(selected_ids)}")

    linkage: list[dict] = []
    blind_rows: list[dict] = []
    shuffled = sorted(selected, key=lambda row: stable_key("shuffle", row["sequence_id"]))
    for index, row in enumerate(shuffled, start=1):
        blind_id = f"U12-{index:03d}-{stable_key('blind', row['sequence_id'])[:8]}"
        blind_rows.append(
            {
                "blind_id": blind_id,
                "source_family": row["source_family"],
                "message": row["message"],
                "occurrences_in_session": row["occurrences"],
            }
        )
        private = dict(row)
        private["blind_id"] = blind_id
        private.pop("tokens", None)
        private.pop("message", None)
        linkage.append(private)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    blind_payload = {
        "schema": "ck3chronicle.blind-template-adjudication-sample",
        "schema_version": 1,
        "status": "frozen",
        "holdout_sha256": HOLDOUT_SHA256,
        "selection_seed": HOLDOUT_SHA256,
        "sample_count": len(blind_rows),
        "authorized_adjudicator_inputs": [
            "BLIND_SAMPLE.json",
            "ADJUDICATION_INSTRUCTIONS.md",
            "SEMANTIC_LABELING_GUIDE.md",
        ],
        "samples": blind_rows,
    }
    (OUTPUT / "BLIND_SAMPLE.json").write_text(
        json.dumps(blind_payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUTPUT / "PRIVATE_LINKAGE.json").write_text(
        json.dumps(
            {
                "schema": "ck3chronicle.blind-template-private-linkage",
                "schema_version": 1,
                "holdout_sha256": HOLDOUT_SHA256,
                "timestamped_blocks": timestamped,
                "model_sha256": unseen.sha256_file(MODEL_PATH),
                "rows": linkage,
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    instructions = """# Independent blind adjudication instructions

Review only `BLIND_SAMPLE.json`, this file, and `SEMANTIC_LABELING_GUIDE.md`.
Do not read learner code, models, inference reports, private linkage, production
parser outputs, prior review packs, or the original error.log.

For every blind sample, independently record:

- `blind_id`;
- `template_group_id`: your own stable identifier shared by messages having
  exactly the same source-qualified ordered semantic template;
- `semantic_template`: retain ordered semantic content and replace timestamps,
  locators/line numbers, keys, numeric instance values, and names with explicit
  `<LOCATOR>`, `<KEY>`, `<VALUE>`, or `<PARAM>` slots;
- `category`, `error_type`, `severity`, and `confidence` under the supplied guide;
- `slot_notes` explaining ambiguous key-versus-semantic decisions;
- `rationale` in one concise sentence.

Rules:

1. Source family plus ordered semantic phrase defines template identity.
2. Timestamp, key values, locator values, and line numbers never change identity.
3. Changing semantic words or their order can change identity even when the
   source family is the same.
4. Do not force an unsupported diagnostic into a registered category/type;
   preserve `unclassified/unknown` where warranted.
5. Do not infer template grouping from occurrence counts.

Write `INDEPENDENT_ADJUDICATION.json` using schema
`ck3chronicle.independent-template-adjudication`, version 1, with one object per
sample under `annotations`. Account for all 96 unique blind IDs. Do not include
any discussion of the hidden learner assignment because it is not an authorized
input.
"""
    (OUTPUT / "ADJUDICATION_INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")
    guide = ROOT.parent / "codex_reboot" / "phase0" / "SEMANTIC_LABELING_GUIDE.md"
    (OUTPUT / "SEMANTIC_LABELING_GUIDE.md").write_bytes(guide.read_bytes())
    manifest = {
        "sample_sha256": unseen.sha256_file(OUTPUT / "BLIND_SAMPLE.json"),
        "linkage_sha256": unseen.sha256_file(OUTPUT / "PRIVATE_LINKAGE.json"),
        "instructions_sha256": unseen.sha256_file(OUTPUT / "ADJUDICATION_INSTRUCTIONS.md"),
        "guide_sha256": unseen.sha256_file(OUTPUT / "SEMANTIC_LABELING_GUIDE.md"),
        "sample_count": 96,
        "selection_strata": dict(collections.Counter(row["selection_stratum"] for row in selected)),
        "status": "frozen_before_independent_adjudication",
    }
    (OUTPUT / "SAMPLE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
