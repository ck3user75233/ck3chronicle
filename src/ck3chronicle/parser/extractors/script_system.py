"""script_system extractor: blocks emitted by script_system.cpp.

Emits (category, error_type) pairs:
- ("script_system", "syntax_error")
- ("script_system", "unknown")
"""
from __future__ import annotations

import re

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "script_system"

_FILE_LINE_RE = re.compile(r'"([^"]+)"\s+near\s+line\s+(\d+)', re.IGNORECASE)


def match(block: TimestampedLogBlock) -> bool:
    return "script_system" in block.source_tag.lower()


def extract(block: TimestampedLogBlock) -> IssueDraft:
    header = block.header_line
    primary_file: str | None = None
    primary_line: int | None = None
    m = _FILE_LINE_RE.search(header)
    if m:
        primary_file = m.group(1)
        try:
            primary_line = int(m.group(2))
        except ValueError:
            primary_line = None

    referenced_objects: list[str] = []
    # Call-stack / continuation tokens go into referenced_objects so cluster
    # views can surface them without polluting the symbol-name registry.
    for cont in block.continuation_lines:
        token = cont.strip()
        if token:
            referenced_objects.append(token)

    return IssueDraft(
        category=CATEGORY,
        error_type="syntax_error",
        tags=[],
        engine_source=block.source_tag,
        sample_message=header,
        primary_file=primary_file,
        primary_line=primary_line,
        referenced_symbols=[],
        referenced_objects=sorted(set(referenced_objects)),
        extra_json={},
        severity="error",
        confidence="high",
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )
