"""event_system extractor: event ID resolution / scope errors.

Match logic looks for ``event`` (substring) in the source tag. The
acceptance-test ``unknown_subsystem.cpp:999`` source_tag does not
contain the substring ``event`` so the unclassified fallback wins for
AT-7.
"""
from __future__ import annotations

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "event_system"


def match(block: TimestampedLogBlock) -> bool:
    return "event" in block.source_tag.lower()


def extract(block: TimestampedLogBlock) -> IssueDraft:
    return IssueDraft(
        category=CATEGORY,
        error_type="unresolved_event_id",
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
