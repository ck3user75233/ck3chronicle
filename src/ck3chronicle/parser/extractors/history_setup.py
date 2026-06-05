"""history_setup extractor: history/ load errors."""
from __future__ import annotations

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "history_setup"


def match(block: TimestampedLogBlock) -> bool:
    return "history" in block.source_tag.lower()


def extract(block: TimestampedLogBlock) -> IssueDraft:
    return IssueDraft(
        category=CATEGORY,
        error_type="unknown",
        tags=[],
        engine_source=block.source_tag,
        sample_message=block.header_line,
        primary_file=None,
        primary_line=None,
        referenced_symbols=[],
        referenced_objects=[],
        extra_json={},
        severity="error",
        confidence=0.8,
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )
