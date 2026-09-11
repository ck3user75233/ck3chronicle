"""script_hygiene extractor: deprecated effects / unused vars."""
from __future__ import annotations

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "script_hygiene"


def match(block: TimestampedLogBlock) -> bool:
    return "script_hygiene" in block.source_tag.lower()


def extract(block: TimestampedLogBlock) -> IssueDraft:
    header_lower = block.header_line.lower()
    if "deprecated" in header_lower:
        error_type = "deprecated_effect"
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
        severity="warning",
        confidence="medium",
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )
