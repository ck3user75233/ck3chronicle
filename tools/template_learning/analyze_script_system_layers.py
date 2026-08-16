"""Measure the empirical outer-envelope / bracket-reason structure.

Read-only analysis over the immutable incremental registry feature caches.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-root", type=Path, required=True)
    return parser.parse_args()


def joined(tokens: list[str] | tuple[str, ...]) -> str:
    return " ".join(token for token in tokens if token.strip())


def main() -> int:
    args = parse_args()
    registry = json.loads((args.state_root / "registry.json").read_text(encoding="utf-8"))
    normalizer = registry["normalizer_version"]

    totals = collections.Counter()
    outer_occurrences = collections.Counter()
    reason_occurrences = collections.Counter()
    outer_evidence: dict[str, set[str]] = collections.defaultdict(set)
    reason_evidence: dict[str, set[str]] = collections.defaultdict(set)
    outer_reasons: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    reason_outers: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    role_totals = collections.Counter()

    for evidence_sha, evidence in registry["evidence"].items():
        cache_meta = evidence["feature_caches"][normalizer]
        cache = json.loads((args.state_root / cache_meta["path"]).read_text(encoding="utf-8"))
        role = evidence["role"]
        for record in cache["records"]:
            if record["source_family"].casefold() != "jomini_script_system.cpp":
                continue
            occurrences = int(record["occurrences"])
            tokens = list(record["tokens"])
            totals[f"{role}_script_occurrences"] += occurrences
            totals[f"{role}_script_sequences"] += 1
            try:
                open_index = tokens.index("[")
                close_index = len(tokens) - 1 - tokens[::-1].index("]")
            except ValueError:
                totals[f"{role}_non_bracketed_occurrences"] += occurrences
                totals[f"{role}_non_bracketed_sequences"] += 1
                continue
            if open_index == 0 or tokens[open_index - 1].casefold() not in {"trigger", "effect"}:
                totals[f"{role}_non_role_bracketed_occurrences"] += occurrences
                totals[f"{role}_non_role_bracketed_sequences"] += 1
                continue
            outer = joined(tokens[:open_index])
            reason = joined(tokens[open_index + 1 : close_index])
            role_word = tokens[open_index - 1].casefold()
            totals[f"{role}_role_envelope_occurrences"] += occurrences
            totals[f"{role}_role_envelope_sequences"] += 1
            role_totals[(role, role_word)] += occurrences
            outer_occurrences[outer] += occurrences
            reason_occurrences[reason] += occurrences
            outer_evidence[outer].add(evidence_sha)
            reason_evidence[reason].add(evidence_sha)
            outer_reasons[outer][reason] += occurrences
            reason_outers[reason][outer] += occurrences

    scope_outer = "Script system error ! Error : scope : <KEY> trigger"
    scoped_reason_prefix = "Scoped object of type"
    scope_reasons = outer_reasons.get(scope_outer, collections.Counter())
    scoped_reason_outers = collections.Counter()
    for reason, outers in reason_outers.items():
        if reason.casefold().startswith(scoped_reason_prefix.casefold()):
            scoped_reason_outers.update(outers)

    result = {
        "normalizer_version": normalizer,
        "totals": dict(totals),
        "role_occurrences": {
            f"{role}:{role_word}": occurrences
            for (role, role_word), occurrences in sorted(role_totals.items())
        },
        "distinct_outer_contracts": len(outer_occurrences),
        "distinct_reason_contracts_before_l2_slot_normalization": len(reason_occurrences),
        "outer_contracts_with_multiple_reasons": sum(
            1 for reasons in outer_reasons.values() if len(reasons) > 1
        ),
        "reason_contracts_seen_under_multiple_outers": sum(
            1 for outers in reason_outers.values() if len(outers) > 1
        ),
        "top_outer_contracts_by_reason_diversity": [
            {
                "outer": outer,
                "reason_count": len(reasons),
                "occurrences": outer_occurrences[outer],
                "evidence_logs": len(outer_evidence[outer]),
            }
            for outer, reasons in sorted(
                outer_reasons.items(),
                key=lambda item: (-len(item[1]), -outer_occurrences[item[0]], item[0]),
            )[:20]
        ],
        "scope_key_trigger_outer": {
            "outer": scope_outer,
            "occurrences": outer_occurrences[scope_outer],
            "evidence_logs": len(outer_evidence[scope_outer]),
            "distinct_reasons": len(scope_reasons),
            "top_reasons": [
                {
                    "reason": reason,
                    "occurrences": occurrences,
                    "evidence_logs": len(reason_evidence[reason]),
                }
                for reason, occurrences in scope_reasons.most_common(20)
            ],
        },
        "scoped_object_reason_across_outers": [
            {"outer": outer, "occurrences": occurrences}
            for outer, occurrences in scoped_reason_outers.most_common(20)
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
