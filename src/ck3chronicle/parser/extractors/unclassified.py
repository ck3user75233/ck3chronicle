"""unclassified extractor: terminal fallback. ``match()`` always True.

This module MUST be last in the EXTRACTORS list. Its ``match()`` is the
unconditional truthy predicate so every block reaches at least one
extractor.
"""
from __future__ import annotations

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "unclassified"


def match(block: TimestampedLogBlock) -> bool:
    return True


def extract(block: TimestampedLogBlock) -> IssueDraft:
    return IssueDraft(
        category=CATEGORY,
        error_type="unknown",
        tags=[],
        engine_source=block.source_tag or "<preamble>",
        sample_message=block.header_line,
        primary_file=None,
        primary_line=None,
        referenced_symbols=[],
        referenced_objects=[],
        extra_json={},
        severity="warning",
        confidence=0.1,
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )
