"""localization extractor: blocks emitted by localization.cpp.

Lifts the concrete localization key into ``referenced_symbols`` and
replaces it with ``<KEY>`` in ``sample_message`` so the cluster row's
``message_template`` is key-agnostic while occurrence rows preserve the
concrete value.
"""
from __future__ import annotations

import re

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "localization"

# UPPER_SNAKE quoted keys (single quotes) — the canonical CK3 localization
# error shape: "Localization key 'FOO_BAR' not found".
_LOC_KEY_RE = re.compile(r"'([A-Z][A-Z0-9_]{1,})'")


def match(block: TimestampedLogBlock) -> bool:
    return "localization" in block.source_tag.lower()


def extract(block: TimestampedLogBlock) -> IssueDraft:
    header = block.header_line
    keys: list[str] = sorted(set(_LOC_KEY_RE.findall(header)))
    templated = _LOC_KEY_RE.sub("'<KEY>'", header)

    error_type = "missing_key" if "not found" in header.lower() else "unknown"

    return IssueDraft(
        category=CATEGORY,
        error_type=error_type,
        tags=[],
        engine_source=block.source_tag,
        sample_message=templated,
        primary_file=None,
        primary_line=None,
        referenced_symbols=keys,
        referenced_objects=[],
        extra_json={},
        severity="error",
        confidence="high",
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )
