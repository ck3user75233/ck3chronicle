"""asset_graphics extractor: texture/model/dds/shader load failures."""
from __future__ import annotations

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "asset_graphics"

_TAGS = ("texture", "model", "shader", "dds", "asset")


def match(block: TimestampedLogBlock) -> bool:
    src = block.source_tag.lower()
    return any(tag in src for tag in _TAGS)


def extract(block: TimestampedLogBlock) -> IssueDraft:
    error_type = "texture_load_failed" if "texture" in block.source_tag.lower() else "asset_load_failed"
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
        confidence="medium",
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )
