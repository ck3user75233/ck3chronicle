"""Build a WIP production-catalog conversion audit from public evidence only.

The generated product-shaped catalog includes learned template tokens but never
sample identities, raw identities, concrete slot values, or source messages.
Selectors are retained only when they reproduce every public row for a contract.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "evaluation-results" / "semantic-projection"
SAMPLE_PATH = REPO / "reference-data" / "SEMANTIC_CALIBRATION_SAMPLE_CANDIDATE.json"
ORACLE_PATH = REPO / "reference-data" / "SEMANTIC_LABELS_ADJUDICATED.json"
PROJECTION_SCHEMA_SOURCE = REPO / "src" / "ck3chronicle" / "classification" / "projection_catalog.py"
PROJECTION_RUNTIME_SOURCE = REPO / "src" / "ck3chronicle" / "semantic_projection.py"

sys.path.insert(0, str(REPO / "src"))

from ck3chronicle.classification.catalog import (  # noqa: E402
    APPROVED_MODEL_REVISION,
    APPROVED_MODEL_SHA256,
    load_approved_classifier,
)
from ck3chronicle.classification.normalize import (  # noqa: E402
    KEY,
    LOCATOR,
    OPTIONAL_KEY,
    PUNCTUATION,
    TOKEN_RE,
    TYPE,
)
from ck3chronicle.classification.projection_catalog import (  # noqa: E402
    load_projection_catalog,
)
from ck3chronicle.parser.log_blocks import TimestampedLogBlock  # noqa: E402
from ck3chronicle.semantic_projection import (  # noqa: E402
    analyze_complete_message,
    project_issue,
)


PLACEHOLDERS = frozenset({KEY, OPTIONAL_KEY, LOCATOR, TYPE, "<VALUE>", "<PARAM>"})
FIELD_TARGET = {
    "referenced_symbols": "referenced_symbol",
    "referenced_objects": "referenced_object",
}


@dataclass(frozen=True)
class SlotIdentity:
    role: str
    ordinal: int

    def as_projection(self, target: str) -> dict[str, Any]:
        return {"role": self.role, "ordinal": self.ordinal, "target": target}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_lf(path: Path, value: Any) -> None:
    """Write canonical UTF-8/LF JSON so Git and runtime hash identical bytes."""
    path.write_bytes(
        (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )


def normalized_path(value: str | None) -> str | None:
    return value.replace("\\", "/") if value is not None else None


def make_block(sample: dict[str, Any]) -> TimestampedLogBlock:
    lines = sample["raw_block_utf8"].splitlines()
    return TimestampedLogBlock(
        timestamp=sample["timestamp"],
        level=sample["level"],
        source_tag=sample["source_tag"],
        source_family=sample["source_family"],
        header_line=lines[0] if lines else "",
        continuation_lines=lines[1:],
        raw_block=sample["raw_block_utf8"],
        log_relpath="logs/error.log",
        line_number=sample["start_line"],
        end_line=sample["end_line"],
    )


def product_slots(result: Any) -> dict[SlotIdentity, str | None]:
    ordinals: dict[str, int] = {}
    slots: dict[SlotIdentity, str | None] = {}
    for raw in result.structured_slots:
        role_value = raw.get("role")
        if not isinstance(role_value, str) or not role_value:
            continue
        role = role_value.casefold()
        ordinal = ordinals.get(role, 0) + 1
        ordinals[role] = ordinal
        value = raw.get("value")
        if raw.get("present") is not True or not isinstance(value, str):
            normalized = None
        else:
            normalized = value.strip()
            if normalized in PLACEHOLDERS:
                normalized = None
        slots[SlotIdentity(role, ordinal)] = normalized
    return slots


def predicted_values(
    slots: dict[SlotIdentity, str | None], selectors: Iterable[SlotIdentity]
) -> list[str]:
    values = [slots.get(selector) for selector in selectors]
    return sorted({value for value in values if value is not None})


def exact_slot_selector(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    candidates = sorted(
        {
            identity
            for row in rows
            for identity, value in row["slots"].items()
            if value is not None and identity.role != "locator"
        },
        key=lambda item: (item.role, item.ordinal),
    )
    targets = [sorted(set(row["issue"][field])) for row in rows]
    if all(not target for target in targets):
        return {"status": "not_required", "selectors": [], "candidate_sets": 1}

    valid: list[tuple[SlotIdentity, ...]] = []
    for size in range(len(candidates) + 1):
        for selected in combinations(candidates, size):
            if all(
                predicted_values(row["slots"], selected) == target
                for row, target in zip(rows, targets)
            ):
                valid.append(selected)
        if valid:
            break
    if len(valid) == 1:
        return {
            "status": "safe_exact",
            "selectors": [
                identity.as_projection(FIELD_TARGET[field]) for identity in valid[0]
            ],
            "candidate_sets": 1,
        }
    if len(valid) > 1:
        return {
            "status": "ambiguous_exact",
            "selectors": [],
            "candidate_sets": len(valid),
        }
    return {"status": "unprojected_role_gap", "selectors": [], "candidate_sets": 0}


def _template_alignment(
    candidate: tuple[str, ...], template: tuple[str, ...]
) -> list[int] | None:
    """Map candidate token indexes to template indexes for one exact contract."""
    slot_tokens = PLACEHOLDERS

    @lru_cache(maxsize=None)
    def match(template_index: int, candidate_index: int):
        if template_index == len(template):
            return [([], [])] if candidate_index == len(candidate) else []
        expected = template[template_index]
        if expected not in slot_tokens:
            if candidate_index >= len(candidate) or candidate[candidate_index] != expected:
                return []
            return [
                ([template_index, *mapping], spans)
                for mapping, spans in match(template_index + 1, candidate_index + 1)
            ][:2]
        if expected == LOCATOR:
            if candidate_index >= len(candidate) or candidate[candidate_index] != LOCATOR:
                return []
            return [
                ([template_index, *mapping], [(template_index, candidate_index, candidate_index + 1), *spans])
                for mapping, spans in match(template_index + 1, candidate_index + 1)
            ][:2]
        solutions = []
        if expected == OPTIONAL_KEY:
            for mapping, spans in match(template_index + 1, candidate_index):
                solutions.append((mapping, [(template_index, candidate_index, candidate_index), *spans]))
                if len(solutions) == 2:
                    return solutions
        if candidate_index < len(candidate) and candidate[candidate_index] == expected:
            ends = [candidate_index + 1]
        else:
            ends = [
                end
                for end in range(candidate_index + 1, len(candidate) + 1)
                if not any(token in slot_tokens for token in candidate[candidate_index:end])
            ]
        for end in ends:
            for mapping, spans in match(template_index + 1, end):
                solutions.append(
                    (
                        [*[template_index] * (end - candidate_index), *mapping],
                        [(template_index, candidate_index, end), *spans],
                    )
                )
                if len(solutions) == 2:
                    return solutions
        return solutions

    solutions = match(0, 0)
    if len(solutions) != 1:
        return None
    mapping = solutions[0][0]
    return mapping if len(mapping) == len(candidate) else None


def exact_template_capture_specs(
    rows: list[dict[str, Any]], field: str, template_tokens: list[str]
) -> dict[str, Any]:
    """Find stable learned-template spans that cover every target value."""
    template = tuple(template_tokens)
    expected_spans: set[tuple[int, int]] | None = None
    for row in rows:
        candidate = tuple(row["result"].normalized_tokens)
        mapping = _template_alignment(candidate, template)
        if mapping is None:
            return {"status": "unavailable", "spans": []}
        row_spans: set[tuple[int, int]] = set()
        for target in row["issue"][field]:
            target_tokens = tuple(TOKEN_RE.findall(target))
            if not target_tokens:
                return {"status": "unavailable", "spans": []}
            occurrences = [
                (start, start + len(target_tokens))
                for start in range(len(candidate) - len(target_tokens) + 1)
                if candidate[start : start + len(target_tokens)] == target_tokens
            ]
            mapped_spans = {
                (min(mapping[start:end]), max(mapping[start:end]) + 1)
                for start, end in occurrences
            }
            if len(mapped_spans) != 1:
                return {
                    "status": "ambiguous" if mapped_spans else "unavailable",
                    "spans": [],
                }
            row_spans.update(mapped_spans)
        if expected_spans is None:
            expected_spans = row_spans
        elif row_spans != expected_spans:
            return {"status": "inconsistent", "spans": []}
    spans = sorted(expected_spans or set())
    if not spans:
        return {"status": "unavailable", "spans": []}
    return {
        "status": "safe_exact",
        "spans": [
            {
                "start_ordinal": start + 1,
                "end_ordinal_exclusive": end + 1,
                "target": FIELD_TARGET[field],
                "join_policy": "preserve_original_token_adjacency",
            }
            for start, end in spans
        ],
    }


def locator_prediction(row: dict[str, Any], ordinal: int) -> tuple[str | None, int | None]:
    locators = row["evidence"].locators
    if ordinal < 1 or ordinal > len(locators):
        return None, None
    locator = locators[ordinal - 1]
    return normalized_path(locator.path), locator.line


def exact_locator_reference_selector(
    rows: list[dict[str, Any]], field: str
) -> dict[str, Any]:
    maximum = max((len(row["evidence"].locators) for row in rows), default=0)
    candidates = list(range(1, maximum + 1))
    targets = [sorted(set(row["issue"][field])) for row in rows]
    valid: list[tuple[int, ...]] = []
    for size in range(len(candidates) + 1):
        for selected in combinations(candidates, size):
            predictions = []
            for row in rows:
                paths = [
                    normalized_path(row["evidence"].locators[ordinal - 1].path)
                    for ordinal in selected
                    if ordinal <= len(row["evidence"].locators)
                ]
                predictions.append(sorted(set(paths)))
            if predictions == targets:
                valid.append(selected)
        if valid:
            break
    if len(valid) == 1:
        return {
            "status": "safe_exact",
            "locator_ordinals": list(valid[0]),
            "target": FIELD_TARGET[field],
        }
    return {
        "status": "ambiguous" if valid else "unavailable",
        "locator_ordinals": [],
        "target": FIELD_TARGET[field],
    }


def exact_locator_selector(rows: list[dict[str, Any]]) -> dict[str, Any]:
    targets = [
        (normalized_path(row["issue"]["primary_file"]), row["issue"]["primary_line"])
        for row in rows
    ]
    if all(target == (None, None) for target in targets):
        return {
            "status": "not_required",
            "primary_locator_ordinal": None,
            "candidate_ordinals": [],
            "best_file_rows": len(rows),
            "best_line_rows": len(rows),
            "best_pair_rows": len(rows),
        }
    maximum = max((len(row["evidence"].locators) for row in rows), default=0)
    ordinals = list(range(1, maximum + 1))
    valid = [
        ordinal
        for ordinal in ordinals
        if all(locator_prediction(row, ordinal) == target for row, target in zip(rows, targets))
    ]
    scores: list[tuple[int, int, int, int]] = []
    for ordinal in ordinals:
        file_rows = 0
        line_rows = 0
        pair_rows = 0
        for row, target in zip(rows, targets):
            predicted = locator_prediction(row, ordinal)
            file_rows += predicted[0] == target[0]
            line_rows += predicted[1] == target[1]
            pair_rows += predicted == target
        scores.append((pair_rows, file_rows, line_rows, ordinal))
    best = max(scores, default=(0, 0, 0, 0))
    if len(valid) == 1:
        status = "safe_exact"
        selected: int | None = valid[0]
    elif len(valid) > 1:
        status = "ambiguous_exact"
        selected = None
    else:
        status = "unprojected_role_gap"
        selected = None
    return {
        "status": status,
        "primary_locator_ordinal": selected,
        "candidate_ordinals": valid,
        "best_file_rows": best[1],
        "best_line_rows": best[2],
        "best_pair_rows": best[0],
    }


def projection_tuple(annotation: dict[str, Any]) -> tuple[str, str, str, str]:
    issue = annotation["issues"][0]
    return (
        annotation["accounting"],
        issue["category"],
        issue["error_type"],
        issue["confidence"],
    )


def model_identity(result: Any, clusters: dict[str, Any]) -> dict[str, Any]:
    cluster = clusters.get(result.contract_id)
    if cluster is not None:
        return {
            "contract_kind": "model_full",
            "template_tokens": list(cluster.template_tokens),
        }
    if result.assignment_level != "l1_l2" or result.l1_template is None or result.l2_template is None:
        raise RuntimeError("stable contract does not join to a full or composed model identity")
    outer = tuple(result.l1_template.split())
    reason = tuple(result.l2_template.split())
    outer_clusters = [
        cluster
        for cluster in clusters.values()
        if cluster.source_family.casefold() == result.source_family.casefold()
        and cluster.layers is not None
        and cluster.layers.l1_outer_tokens == outer
    ]
    reason_clusters = [
        cluster
        for cluster in clusters.values()
        if cluster.source_family.casefold() == result.source_family.casefold()
        and cluster.layers is not None
        and cluster.layers.l2_reason_tokens == reason
    ]
    if not outer_clusters or not reason_clusters:
        raise RuntimeError(
            "composed contract does not join to learned layers: "
            f"source={result.source_family!r} outer={outer!r} reason={reason!r}"
        )
    return {
        "contract_kind": "composed_l1_l2",
        "template_tokens": [*outer, "[", *reason, "]"],
        "l1_outer_tokens": list(outer),
        "l2_reason_tokens": list(reason),
        "learned_l1_source_cluster_ids": sorted(
            cluster.cluster_id for cluster in outer_clusters
        ),
        "learned_l2_source_cluster_ids": sorted(
            cluster.cluster_id for cluster in reason_clusters
        ),
    }


def inferred_gap_pattern(
    rows: list[dict[str, Any]], field: str, slot_result: dict[str, Any]
) -> str | None:
    if slot_result["status"] in {"safe_exact", "not_required"}:
        return None
    if not any(row["issue"][field] for row in rows):
        return None
    if all(
        normalized_path(target)
        in {normalized_path(locator.path) for locator in row["evidence"].locators}
        for row in rows
        for target in row["issue"][field]
    ):
        return "bind_locator_ordinal_to_reference_role"
    if all(
        any(
            part
            and part in re.sub(r"\s+", "", target).casefold()
            for part in (
                re.sub(r"\s+", "", value).casefold()
                for value in row["slots"].values()
                if value is not None
            )
        )
        for row in rows
        for target in row["issue"][field]
    ):
        return "compose_contract_bound_generic_slots"
    if all(
        target in row["evidence"].complete_message
        for row in rows
        for target in row["issue"][field]
    ):
        return "replay_exact_template_over_complete_message_with_typed_capture"
    return "add_family_specific_complete_block_role_extractor"


def primary_locator_gap(contract_id: str) -> tuple[str, dict[str, Any]]:
    if contract_id == "861fe418198a1e67":
        return (
            "file_label_opaque_source_with_line",
            {
                "file_capture": "single_nonwhitespace_value_after_contract_file_label",
                "line_capture": "following_line_value",
                "pairing": "same_contract_clause",
            },
        )
    if contract_id == "f36af685a32c501a":
        return (
            "pre_path_line_column_pair",
            {
                "file_capture": "path_after_contract_in_relation",
                "line_capture": "preceding_line_value",
                "ignored_parameter": "intervening_column_value",
                "pairing": "same_contract_clause",
            },
        )
    return (
        "typed_complete_block_locator_pairing",
        {"pairing": "reviewed_contract_clause"},
    )


def specialized_reference_gap(
    contract_id: str, field: str
) -> tuple[str, dict[str, Any]] | None:
    if field == "referenced_symbols" and contract_id in {
        "93f10d4591275681",
        "df20426245cc1682",
    }:
        return (
            "compose_slot_and_key_path_roles",
            {
                "outputs": [
                    {"role": "key", "ordinal": 1},
                    {
                        "compose": [
                            {"role": "key", "ordinal": 2},
                            {"template_punctuation": "."},
                            {"role": "key", "ordinal": 3},
                        ]
                    },
                ],
                "deduplicate": True,
                "order": "lexical",
            },
        )
    if field == "referenced_symbols" and contract_id == "c6a2f80945571e9f":
        return (
            "assert_equivalent_slot_values_then_select",
            {
                "equivalent_candidates": [
                    {"role": "key", "ordinal": 1},
                    {"role": "key", "ordinal": 2},
                ],
                "on_disagreement": "leave_unprojected_and_record_role_conflict",
                "select_after_agreement": {"role": "key", "ordinal": 1},
            },
        )
    if field == "referenced_objects" and contract_id == "364d3f870373ddc8":
        return (
            "event_uri_and_key_object_roles",
            {
                "outputs": [
                    {"capture": "event_uri_payload", "retain_leading_slash": True},
                    {"role": "key", "ordinal": 1},
                ],
                "event_uri_is_filesystem_locator": False,
                "deduplicate": True,
                "order": "lexical",
            },
        )
    if field == "referenced_symbols" and contract_id == "4b8494e68dfd6f25":
        return (
            "contract_quoted_argument_roles",
            {
                "quoted_argument_ordinals": [1, 2],
                "roles": ["symbol.reference", "symbol.reference"],
                "deduplicate": True,
                "order": "lexical",
            },
        )
    if field == "referenced_symbols" and contract_id in {
        "00a0add0c4063a3a",
        "33824ae4410d9837",
        "acdf70f87cbadc47",
        "fda2ffa9dc25c8df",
    }:
        return (
            "preserve_script_outer_expression_sidecar",
            {
                "capture": "outer_expression_before_trigger_or_effect_role",
                "normalization": "preserve_ck3_key_path_adjacency",
                "role": "symbol.reference",
            },
        )
    if field == "referenced_symbols" and contract_id == "21b477c6e94b1681":
        return (
            "preserve_persistent_clause_key_sidecar",
            {
                "capture": "key_consumed_by_reviewed_persistent_clause_normalizer",
                "role": "symbol.reference",
            },
        )
    if field == "referenced_symbols" and contract_id == "fef0093771afc804":
        return (
            "preserve_structured_normalizer_capture",
            {
                "capture": "key_consumed_by_reviewed_structured_normalizer",
                "role": "symbol.reference",
            },
        )
    return None


def reference_projection_plan(entry: dict[str, Any]) -> list[dict[str, Any]]:
    """Compile reviewed role gaps into schema-v2 contract-bound captures."""
    contract_id = entry["contract_id"]
    references: list[dict[str, Any]] = []

    # These mixed captures cannot be represented as a single v1 slot selector.
    if contract_id == "93b0680d3e83c199":
        return [
            {
                "capture": "script_outer_expression",
                "target": "referenced_symbol",
            },
            {
                "capture": "slot_set",
                "target": "referenced_object",
                "role": "key",
                "ordinals": [3, 6, 9],
            },
        ]
    if contract_id == "9ac0cbcd6c4780f7":
        return [
            {
                "capture": "locator",
                "target": "referenced_object",
                "ordinal": 1,
            },
            {
                "capture": "slot",
                "target": "referenced_object",
                "role": "key",
                "ordinal": 1,
            },
        ]
    if contract_id == "96f429d690d07a4f":
        return [
            {
                "capture": "template_span",
                "target": "referenced_symbol",
                "start_ordinal": ordinal,
                "end_ordinal_exclusive": ordinal + 1,
            }
            for ordinal in (5, 7)
        ]
    if contract_id == "d22c7d583900a720":
        return [
            {
                "capture": "template_span",
                "target": "referenced_symbol",
                "start_ordinal": 13,
                "end_ordinal_exclusive": 14,
            }
        ]
    if contract_id == "eac6101b42e4af8a":
        return [
            {"capture": "unexpected_token", "target": "referenced_symbol"}
        ]
    if contract_id == "d3b8882494c388d8":
        return [
            {"capture": "unknown_arguments", "target": "referenced_symbol"}
        ]

    for gap in entry["projection_gaps"]:
        target = FIELD_TARGET.get(gap["field"])
        if target is None:
            continue
        pattern = gap["pattern"]
        detail = gap.get("detail", {})
        if pattern == "capture_learned_template_span":
            for span in detail.get("spans", []):
                references.append(
                    {
                        "capture": "template_span",
                        "target": target,
                        "start_ordinal": span["start_ordinal"],
                        "end_ordinal_exclusive": span["end_ordinal_exclusive"],
                    }
                )
        elif pattern == "bind_locator_ordinal_to_reference_role":
            for ordinal in detail.get("locator_ordinals", []):
                references.append(
                    {"capture": "locator", "target": target, "ordinal": ordinal}
                )
        elif pattern == "preserve_script_outer_expression_sidecar":
            references.append(
                {"capture": "script_outer_expression", "target": target}
            )
        elif pattern == "preserve_persistent_clause_key_sidecar":
            references.append({"capture": "persistent_key", "target": target})
        elif pattern == "event_uri_and_key_object_roles":
            references.extend(
                (
                    {"capture": "event_uri", "target": target},
                    {
                        "capture": "slot",
                        "target": target,
                        "role": "key",
                        "ordinal": 1,
                    },
                )
            )
        elif pattern == "contract_quoted_argument_roles":
            references.extend(
                {
                    "capture": "quoted_argument",
                    "target": target,
                    "ordinal": ordinal,
                }
                for ordinal in detail["quoted_argument_ordinals"]
            )
        elif pattern == "compose_slot_and_key_path_roles":
            for output in detail["outputs"]:
                if "role" in output:
                    references.append(
                        {
                            "capture": "slot",
                            "target": target,
                            "role": output["role"],
                            "ordinal": output["ordinal"],
                        }
                    )
                    continue
                parts = []
                for part in output["compose"]:
                    if "template_punctuation" in part:
                        parts.append({"literal": part["template_punctuation"]})
                    else:
                        parts.append(
                            {"role": part["role"], "ordinal": part["ordinal"]}
                        )
                references.append(
                    {
                        "capture": "slot_composition",
                        "target": target,
                        "parts": parts,
                    }
                )
        elif pattern == "assert_equivalent_slot_values_then_select":
            references.append(
                {
                    "capture": "equivalent_slots",
                    "target": target,
                    "role": detail["select_after_agreement"]["role"],
                    "ordinals": [
                        item["ordinal"] for item in detail["equivalent_candidates"]
                    ],
                }
            )
    return references


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    global SAMPLE_PATH, ORACLE_PATH, OUT
    args = parse_args()
    SAMPLE_PATH = args.candidate.resolve()
    ORACLE_PATH = args.oracle.resolve()
    OUT = args.output_dir.resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    samples = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))["samples"]
    annotations = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))["annotations"]
    by_id = {row["sample_id"]: row for row in annotations}
    classifier = load_approved_classifier()
    clusters = {cluster.cluster_id: cluster for cluster in classifier.model.clusters}
    rows_by_contract: dict[str, list[dict[str, Any]]] = defaultdict(list)
    unresolved_rows: list[dict[str, Any]] = []

    for sample in samples:
        annotation = by_id[sample["sample_id"]]
        results = classifier.classify_block(sample["source_family"], sample["raw_block_utf8"])
        if len(results) != 1:
            raise RuntimeError("public semantic row did not produce one classification unit")
        result = results[0]
        if result.contract_id is None or result.assignment_level not in {"full", "l1_l2"}:
            issue = annotation["issues"][0]
            unresolved_rows.append(
                {
                    "sample_id": sample["sample_id"],
                    "source_family": sample["source_family"],
                    "message": sample["header_message"],
                    "assignment_level": result.assignment_level,
                    "normalized_tokens": list(result.normalized_tokens),
                    "l1_template": result.l1_template,
                    "l2_template": result.l2_template,
                    "accounting": annotation["accounting"],
                    "category": issue["category"],
                    "error_type": issue["error_type"],
                }
            )
            continue
        block = make_block(sample)
        rows_by_contract[result.contract_id].append(
            {
                "sample_id": sample["sample_id"],
                "message": sample["header_message"],
                "result": result,
                "annotation": annotation,
                "issue": annotation["issues"][0],
                "slots": product_slots(result),
                "evidence": analyze_complete_message(result, block),
            }
        )

    audited_projections: list[dict[str, Any]] = []
    gap_groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    coverage = {
        "primary_locator": Counter(),
        "referenced_symbols": Counter(),
        "referenced_objects": Counter(),
    }
    field_exact_rows = Counter()
    safe_catalog_exact_rows = Counter()
    field_total_rows = Counter()

    for contract_id, rows in sorted(rows_by_contract.items()):
        targets = {projection_tuple(row["annotation"]) for row in rows}
        sources = {row["result"].source_family for row in rows}
        levels = {row["result"].assignment_level for row in rows}
        if len(targets) != 1 or len(sources) != 1:
            raise RuntimeError("stable contract has conflicting semantic authority")
        accounting, category, error_type, confidence = next(iter(targets))
        source = next(iter(sources))
        identity = model_identity(rows[0]["result"], clusters)
        locator = exact_locator_selector(rows)
        symbols = exact_slot_selector(rows, "referenced_symbols")
        objects = exact_slot_selector(rows, "referenced_objects")

        symbol_identities = {
            (item["role"], item["ordinal"])
            for item in symbols["selectors"]
        }
        object_identities = {
            (item["role"], item["ordinal"])
            for item in objects["selectors"]
        }
        cross_target = symbol_identities & object_identities
        if cross_target:
            symbols = {"status": "cross_target_conflict", "selectors": [], "candidate_sets": 0}
            objects = {"status": "cross_target_conflict", "selectors": [], "candidate_sets": 0}

        coverage["primary_locator"][locator["status"]] += 1
        coverage["referenced_symbols"][symbols["status"]] += 1
        coverage["referenced_objects"][objects["status"]] += 1
        field_total_rows["primary_file"] += len(rows)
        field_total_rows["primary_line"] += len(rows)
        field_total_rows["referenced_symbols"] += len(rows)
        field_total_rows["referenced_objects"] += len(rows)
        field_exact_rows["primary_file"] += locator["best_file_rows"]
        field_exact_rows["primary_line"] += locator["best_line_rows"]
        if locator["status"] in {"safe_exact", "not_required"}:
            safe_catalog_exact_rows["primary_file"] += len(rows)
            safe_catalog_exact_rows["primary_line"] += len(rows)
        else:
            safe_catalog_exact_rows["primary_file"] += sum(
                row["issue"]["primary_file"] is None for row in rows
            )
            safe_catalog_exact_rows["primary_line"] += sum(
                row["issue"]["primary_line"] is None for row in rows
            )
        if symbols["status"] in {"safe_exact", "not_required"}:
            field_exact_rows["referenced_symbols"] += len(rows)
            safe_catalog_exact_rows["referenced_symbols"] += len(rows)
        else:
            unprojected_exact = sum(
                not row["issue"]["referenced_symbols"] for row in rows
            )
            field_exact_rows["referenced_symbols"] += unprojected_exact
            safe_catalog_exact_rows["referenced_symbols"] += unprojected_exact
        if objects["status"] in {"safe_exact", "not_required"}:
            field_exact_rows["referenced_objects"] += len(rows)
            safe_catalog_exact_rows["referenced_objects"] += len(rows)
        else:
            unprojected_exact = sum(
                not row["issue"]["referenced_objects"] for row in rows
            )
            field_exact_rows["referenced_objects"] += unprojected_exact
            safe_catalog_exact_rows["referenced_objects"] += unprojected_exact

        projection_gaps: list[dict[str, Any]] = []
        if locator["status"] not in {"safe_exact", "not_required"}:
            pattern, detail = primary_locator_gap(contract_id)
            projection_gaps.append(
                {"field": "primary_locator", "pattern": pattern, "detail": detail}
            )
            gap_groups[(source, "primary_locator", pattern)].append(contract_id)
        for field, audit in (
            ("referenced_symbols", symbols),
            ("referenced_objects", objects),
        ):
            pattern = None
            detail: dict[str, Any] | None = None
            if audit["status"] not in {"safe_exact", "not_required"}:
                specialized = specialized_reference_gap(contract_id, field)
                if specialized is not None:
                    pattern, detail = specialized
                else:
                    locator_reference = exact_locator_reference_selector(rows, field)
                    if locator_reference["status"] == "safe_exact":
                        pattern = "bind_locator_ordinal_to_reference_role"
                        detail = locator_reference
                    else:
                        template_capture = exact_template_capture_specs(
                            rows, field, identity["template_tokens"]
                        )
                        if template_capture["status"] == "safe_exact":
                            pattern = "capture_learned_template_span"
                            detail = template_capture
            if pattern is None:
                pattern = inferred_gap_pattern(rows, field, audit)
            if pattern is not None:
                gap = {"field": field, "pattern": pattern}
                if detail is not None:
                    gap["detail"] = detail
                projection_gaps.append(gap)
                gap_groups[(source, field, pattern)].append(contract_id)

        slot_projections = [*symbols["selectors"], *objects["selectors"]]
        entry = {
            "contract_id": contract_id,
            "source_family": source,
            **identity,
            "accounting": accounting,
            "category": category,
            "error_type": error_type,
            "tags": [],
            "confidence_by_assignment": {level: confidence for level in sorted(levels)},
            "primary_locator_ordinal": locator["primary_locator_ordinal"],
            "slot_projections": slot_projections,
            "reference_projections": [],
            "projection_gaps": projection_gaps,
            "audit": {
                "primary_locator": locator,
                "referenced_symbols": symbols,
                "referenced_objects": objects,
                "development_rows": (
                    [
                        {
                            "sample_id": row["sample_id"],
                            "message": row["message"],
                            "primary_file": row["issue"]["primary_file"],
                            "primary_line": row["issue"]["primary_line"],
                            "referenced_symbols": row["issue"]["referenced_symbols"],
                            "referenced_objects": row["issue"]["referenced_objects"],
                            "slots": [
                                {
                                    "role": identity.role,
                                    "ordinal": identity.ordinal,
                                    "value": value,
                                }
                                for identity, value in sorted(
                                    row["slots"].items(),
                                    key=lambda item: (item[0].role, item[0].ordinal),
                                )
                            ],
                        }
                        for row in rows
                    ]
                    if projection_gaps
                    else []
                ),
            },
        }
        audited_projections.append(entry)

    for entry in audited_projections:
        entry["reference_projections"] = reference_projection_plan(entry)

    gap_patterns = [
        {
            "source_family": source,
            "target_field": field,
            "proposed_pattern": pattern,
            "contract_ids": sorted(contract_ids),
        }
        for (source, field, pattern), contract_ids in sorted(gap_groups.items())
    ]

    audited_full_ids = {
        entry["contract_id"]
        for entry in audited_projections
        if entry["contract_kind"] == "model_full"
    }
    default_projections = [
        {
            "contract_id": cluster.cluster_id,
            "source_family": cluster.source_family,
            "contract_kind": "model_full",
            "template_tokens": list(cluster.template_tokens),
            "accounting": "preserved_unclassified",
            "category": "unclassified",
            "error_type": "unknown",
            "tags": [],
            "confidence_by_assignment": {"full": "low"},
            "primary_locator_ordinal": None,
            "slot_projections": [],
            "reference_projections": [],
            "projection_gaps": [],
            "projection_authority": "default_preserved_unclassified",
        }
        for cluster in sorted(classifier.model.clusters, key=lambda item: item.cluster_id)
        if cluster.cluster_id not in audited_full_ids
    ]
    for entry in audited_projections:
        entry["projection_authority"] = "public_semantic_review"
    projections = sorted(
        [*audited_projections, *default_projections],
        key=lambda entry: (entry["contract_id"], entry["contract_kind"]),
    )
    direct_full = sum(entry["contract_kind"] == "model_full" for entry in audited_projections)
    composed = len(audited_projections) - direct_full
    preserved = sum(
        entry["accounting"] == "preserved_unclassified"
        for entry in audited_projections
    )
    document = {
        "schema": "ck3chronicle-semantic-projection-catalog",
        "schema_version": 1,
        "status": "wip_conversion_audit_not_product_not_evaluator",
        "revision_id": "public-semantic-252-conversion-draft-v2",
        "model_revision_id": APPROVED_MODEL_REVISION,
        "model_sha256": APPROVED_MODEL_SHA256,
        "authority": {
            "sample_artifact_sha256": sha256(SAMPLE_PATH),
            "oracle_artifact_sha256": sha256(ORACLE_PATH),
            "projection_schema_source_sha256": sha256(PROJECTION_SCHEMA_SOURCE),
            "projection_runtime_source_sha256": sha256(PROJECTION_RUNTIME_SOURCE),
        },
        "summary": {
            "public_rows": len(samples),
            "unresolved_rows": len(unresolved_rows),
            "stable_contract_rows": sum(len(rows) for rows in rows_by_contract.values()),
            "stable_contracts": len(audited_projections),
            "direct_full_model_contracts": direct_full,
            "composed_l1_l2_contracts": composed,
            "preserved_unclassified_contracts": preserved,
            "approved_model_clusters": len(classifier.model.clusters),
            "default_preserved_unclassified_model_contracts": len(default_projections),
            "total_catalog_projections": len(projections),
            "semantic_projection_conflicts": 0,
            "contract_field_status": {
                field: dict(sorted(statuses.items()))
                for field, statuses in coverage.items()
            },
            "row_field_best_exact": {
                field: {
                    "exact_rows": field_exact_rows[field],
                    "total_rows": field_total_rows[field],
                }
                for field in (
                    "primary_file",
                    "primary_line",
                    "referenced_symbols",
                    "referenced_objects",
                )
            },
            "row_field_safe_catalog_exact": {
                field: {
                    "exact_rows": safe_catalog_exact_rows[field],
                    "total_rows": field_total_rows[field],
                }
                for field in (
                    "primary_file",
                    "primary_line",
                    "referenced_symbols",
                    "referenced_objects",
                )
            },
            "selector_conflicts": {
                "primary_locator_ambiguous_exact_contracts": coverage[
                    "primary_locator"
                ]["ambiguous_exact"],
                "referenced_symbols_ambiguous_exact_contracts": coverage[
                    "referenced_symbols"
                ]["ambiguous_exact"],
                "referenced_objects_ambiguous_exact_contracts": coverage[
                    "referenced_objects"
                ]["ambiguous_exact"],
                "cross_target_conflicts": sum(
                    statuses["cross_target_conflict"] for statuses in coverage.values()
                ),
            },
            "role_gap_groups": len(gap_patterns),
        },
        "required_schema_corrections": [
            {
                "id": "composed-contract-identity",
                "change": "validate composed_l1_l2 identity from source plus exact learned L1 and L2 token arrays",
            },
            {
                "id": "explicit-unprojected-fields",
                "change": "distinguish an audited empty projection from an unresolved role gap",
            },
            {
                "id": "typed-reference-evidence",
                "change": "support contract-bound complete-message captures, slot composition, and locator-to-reference bindings",
            },
        ],
        "role_extraction_pattern_definitions": {
            "capture_learned_template_span": (
                "Replay the exact learned template over the complete message while "
                "retaining original token spans; capture the audited 1-based template "
                "span and preserve original token adjacency."
            ),
            "bind_locator_ordinal_to_reference_role": (
                "Reuse complete-block locator extraction, select the audited 1-based "
                "locator ordinal, and project its path to the stated reference role."
            ),
            "compose_contract_bound_generic_slots": (
                "Compose only the contract-listed generic slot ordinals using punctuation "
                "already present between them in the learned template."
            ),
            "compose_slot_and_key_path_roles": (
                "Project the listed direct slot and reconstruct the second CK3 key path "
                "from listed key slots plus learned template punctuation."
            ),
            "assert_equivalent_slot_values_then_select": (
                "Require the listed redundant captures to agree before selecting one; "
                "a disagreement is a role conflict and remains unprojected."
            ),
            "event_uri_and_key_object_roles": (
                "Capture the non-filesystem event URI payload and the listed key slot as "
                "two objects; the URI prefix is syntax and the leading slash is retained."
            ),
            "contract_quoted_argument_roles": (
                "Capture the listed quote-delimited argument ordinals after exact contract "
                "selection and assign only their reviewed roles."
            ),
            "preserve_script_outer_expression_sidecar": (
                "Retain the concrete outer CK3 expression before structured script-system "
                "normalization replaces it with a key placeholder."
            ),
            "preserve_persistent_clause_key_sidecar": (
                "Retain the concrete key consumed by the reviewed persistent-clause "
                "normalizer before replacement with a placeholder."
            ),
            "preserve_structured_normalizer_capture": (
                "Retain the concrete value consumed by an approved structured normalizer "
                "as typed sidecar evidence."
            ),
            "replay_exact_template_over_complete_message_with_typed_capture": (
                "Run contract matching before lossy structured normalization and retain "
                "the raw span consumed by each typed placeholder as sidecar evidence."
            ),
            "add_family_specific_complete_block_role_extractor": (
                "Add one source-guarded, contract-ordered complete-block evidence rule; "
                "the rule may assign roles but may not discover contract identity."
            ),
            "file_label_opaque_source_with_line": (
                "For the audited contract, accept a non-path opaque source after the file "
                "label and pair it with the following line value."
            ),
            "pre_path_line_column_pair": (
                "For the audited contract, pair the path following the relation with the "
                "preceding line value while retaining the intervening column as a parameter."
            ),
            "typed_complete_block_locator_pairing": (
                "Bind a primary file and line as one reviewed complete-block clause."
            ),
        },
        "projections": projections,
        "role_gap_patterns": gap_patterns,
        "unresolved_rows": unresolved_rows,
    }
    output = OUT / "semantic-projection-catalog.product-shaped.audit.json"
    write_json_lf(output, document)

    compatible_fields = (
        "contract_id",
        "contract_kind",
        "source_family",
        "accounting",
        "category",
        "error_type",
        "tags",
        "confidence_by_assignment",
        "primary_locator_ordinal",
        "slot_projections",
        "reference_projections",
    )
    compatible_projections = []
    for entry in projections:
        compatible = {field: entry[field] for field in compatible_fields}
        if entry["contract_kind"] == "composed_l1_l2":
            compatible["l1_outer_tokens"] = entry["l1_outer_tokens"]
            compatible["l2_reason_tokens"] = entry["l2_reason_tokens"]
        compatible_projections.append(compatible)
    compatible_document = {
        "schema": "ck3chronicle-semantic-projection-catalog",
        "schema_version": 2,
        "revision_id": "public-semantic-252-contract-evidence-v3",
        "model_revision_id": APPROVED_MODEL_REVISION,
        "model_sha256": APPROVED_MODEL_SHA256,
        "projections": compatible_projections,
    }
    compatible_path = OUT / "semantic-projection-catalog.current-schema.json"
    write_json_lf(compatible_path, compatible_document)
    compatible_hash = sha256(compatible_path)
    loaded = load_projection_catalog(
        compatible_path,
        expected_sha256=compatible_hash,
        model=classifier.model,
    )
    if len(loaded.projections) != len(compatible_projections):
        raise RuntimeError("current-schema subset did not round-trip")

    annotation_by_id = {row["sample_id"]: row for row in annotations}
    mismatch_counts: Counter[str] = Counter()
    mismatch_rows: list[dict[str, Any]] = []
    for sample in samples:
        expected_annotation = annotation_by_id[sample["sample_id"]]
        expected = expected_annotation["issues"][0]
        results = classifier.classify_block(
            sample["source_family"], sample["raw_block_utf8"]
        )
        if len(results) != 1:
            raise RuntimeError("public semantic row did not produce one projection unit")
        result = results[0]
        projected = project_issue(result, make_block(sample), loaded)
        semantic_projection = loaded.projection_for(result.contract_id or "")
        actual = {
            "accounting": (
                semantic_projection.accounting
                if semantic_projection is not None
                else "preserved_unclassified"
            ),
            "category": projected.category,
            "error_type": projected.error_type,
            "severity": projected.severity,
            "confidence": projected.confidence,
            "primary_file": projected.primary_file,
            "primary_line": projected.primary_line,
            "referenced_symbols": sorted(projected.referenced_symbols),
            "referenced_objects": sorted(projected.referenced_objects),
        }
        wanted = {
            "accounting": expected_annotation["accounting"],
            "category": expected["category"],
            "error_type": expected["error_type"],
            "severity": expected["severity"],
            "confidence": expected["confidence"],
            "primary_file": expected["primary_file"],
            "primary_line": expected["primary_line"],
            "referenced_symbols": sorted(expected["referenced_symbols"]),
            "referenced_objects": sorted(expected["referenced_objects"]),
        }
        mismatches = sorted(field for field in wanted if wanted[field] != actual[field])
        mismatch_counts.update(mismatches)
        if mismatches:
            mismatch_rows.append(
                {
                    "sample_id": sample["sample_id"],
                    "contract_id": result.contract_id,
                    "source_family": sample["source_family"],
                    "mismatches": mismatches,
                    "expected": wanted,
                    "actual": actual,
                }
            )
    calibration = {
        "schema": "ck3chronicle-semantic-projection-public-calibration",
        "schema_version": 1,
        "status": "development_authority_not_holdout",
        "candidate_sha256": sha256(SAMPLE_PATH),
        "oracle_sha256": sha256(ORACLE_PATH),
        "model_revision_id": APPROVED_MODEL_REVISION,
        "model_sha256": APPROVED_MODEL_SHA256,
        "catalog_revision_id": loaded.revision_id,
        "catalog_sha256": compatible_hash,
        "rows": len(samples),
        "exact_rows": len(samples) - len(mismatch_rows),
        "mismatch_rows": len(mismatch_rows),
        "field_mismatch_counts": dict(sorted(mismatch_counts.items())),
        "mismatches": mismatch_rows,
    }
    write_json_lf(OUT / "semantic-projection-public-calibration.json", calibration)


if __name__ == "__main__":
    main()
