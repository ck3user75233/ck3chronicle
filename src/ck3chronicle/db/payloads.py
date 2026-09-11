"""Deterministic identity for losslessly deduplicated classifier payloads."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Sequence


PAYLOAD_COLUMNS: tuple[str, ...] = (
    "model_sha256",
    "source_family",
    "assignment_level",
    "contract_id",
    "confidence",
    "semantic_text",
    "location_evidence",
    "normalized_tokens_json",
    "l1_template",
    "l2_template",
    "structured_slots_json",
)


def payload_sha256(values: Sequence[Any]) -> str:
    """Hash one exact persisted payload using an unambiguous JSON encoding."""
    if len(values) != len(PAYLOAD_COLUMNS):
        raise ValueError("classification payload has the wrong field count")
    encoded = json.dumps(
        list(values),
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

