"""Oracle-side P1-PAR-01 scorer; deliberately imports no ck3chronicle code."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


SCHEMA = "ck3chronicle.phase1.lexical-score"
SCHEMA_VERSION = 1
FIELDS = (
    "index",
    "start_line",
    "end_line",
    "line_count",
    "timestamp",
    "level",
    "source_tag",
    "source_family",
    "raw_sha256",
    "byte_count",
)


def _source_block_id(entry: dict[str, object]) -> str:
    identity = (
        b"error.log\0"
        + str(entry["start_line"]).encode("ascii")
        + b"\0"
        + str(entry["raw_sha256"]).encode("ascii")
    )
    return hashlib.sha256(identity).hexdigest()


def score(result: dict[str, object], oracle: dict[str, object]) -> dict[str, object]:
    discrepancies: list[dict[str, object]] = []

    def mismatch(kind: str, **fields: object) -> None:
        if len(discrepancies) < 20:
            discrepancies.append({"kind": kind, **fields})

    result_blocks = list(result.get("blocks", []))
    oracle_blocks = list(oracle.get("blocks", []))
    if result.get("input", {}).get("sha256") != oracle["source"]["sha256"]:
        mismatch("input_sha256")
    if result.get("input", {}).get("byte_count") != oracle["source"]["byte_count"]:
        mismatch("input_byte_count")
    if len(result_blocks) != len(oracle_blocks):
        mismatch("block_count", actual=len(result_blocks), expected=len(oracle_blocks))

    field_mismatch_counts: dict[str, int] = {}
    compared = min(len(result_blocks), len(oracle_blocks))
    for index in range(compared):
        actual = result_blocks[index]
        expected = oracle_blocks[index]
        bad_fields: list[str] = []
        for field in FIELDS:
            if actual.get(field) != expected.get(field):
                field_mismatch_counts[field] = field_mismatch_counts.get(field, 0) + 1
                bad_fields.append(field)
        if actual.get("source_block_id") != _source_block_id(expected):
            field_mismatch_counts["source_block_id"] = (
                field_mismatch_counts.get("source_block_id", 0) + 1
            )
            bad_fields.append("source_block_id")
        if bad_fields:
            mismatch(
                "block_fields",
                block_index=index + 1,
                fields=sorted(bad_fields),
            )

    summary = result.get("summary", {})
    expected_summary = oracle["summary"]
    summary_pairs = {
        "timestamped_block_count": expected_summary["block_count"],
        "timestamped_block_bytes": expected_summary["block_byte_count"],
        "preamble_bytes": expected_summary["preamble_byte_count"],
    }
    for field, expected in summary_pairs.items():
        if summary.get(field) != expected:
            mismatch("summary", field=field, actual=summary.get(field), expected=expected)

    passed = not discrepancies and not field_mismatch_counts
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "gate_component": "P1-PAR-01-LEXICAL",
        "status": "pass" if passed else "fail",
        "candidate_commit": result.get("candidate_commit"),
        "input_sha256": result.get("input", {}).get("sha256"),
        "blocks_compared": compared,
        "field_mismatch_counts": dict(sorted(field_mismatch_counts.items())),
        "discrepant_records_reported": len(discrepancies),
        "field_mismatch_total": sum(field_mismatch_counts.values()),
        "first_discrepancies": discrepancies,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.result.read_text(encoding="utf-8"))
    oracle = json.loads(args.oracle.read_text(encoding="utf-8"))
    payload = score(result, oracle)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    raise SystemExit(0 if payload["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
