"""database_reference extractor: db lookup failures, duplicate keys."""
from __future__ import annotations

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "database_reference"


def match(block: TimestampedLogBlock) -> bool:
    return "database" in block.source_tag.lower()


def extract(block: TimestampedLogBlock) -> IssueDraft:
    header_lower = block.header_line.lower()
    if "duplicate" in header_lower:
        error_type = "duplicate_key"
    elif "not found" in header_lower or "lookup" in header_lower:
        error_type = "lookup_failed"
    else:
        error_type = "unknown"
    return IssueDraft(
        category=CATEGORY,
        error_type=error_type,
        tags=[],
        engine_source=block.source_tag,
        sample_message=block.header_line,
        primary_file=None,
        primary_line=None,
        referenced_symbols=[],
        referenced_objects=[],
        extra_json={},
        severity="error",
        confidence="high",
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )
