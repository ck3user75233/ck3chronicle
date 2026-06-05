"""gui_interface extractor: gui/, interface/, widget errors."""
from __future__ import annotations

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "gui_interface"

_TAGS = ("gui", "interface", "widget")


def match(block: TimestampedLogBlock) -> bool:
    src = block.source_tag.lower()
    return any(tag in src for tag in _TAGS)


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
