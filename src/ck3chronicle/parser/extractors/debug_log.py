"""debug_log extractor family: blocks originating from debug.log.

Handles the two dominant high-volume patterns that previously fell to
``unclassified`` from debug.log:

1. ``pdx_localize.cpp`` — duplicate / multi-file localization key warnings.
   Patterns::

       "Localization key 'KEY' is present in both 'FILE1' and 'FILE2'"
       "Duplicate localization key 'KEY' in file 'FILE'"

2. ``gamedatabase.h`` / ``gamedatabase.cpp`` — database object override
   notifications.  Patterns::

       "[Type TypeName] is being overridden in mod_a, using mod_b instead"
       "Overriding [Trait foo_bar] in [mod A] with [mod B]"

Extractors template out the volatile parts (key names → ``'<KEY>'``,
quoted file paths → ``"<FILE>"``, bracketed objects → ``[<OBJECT>]``) so
repeated occurrences of the same pattern share a signature.
"""
from __future__ import annotations

import re

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

# ── Source-tag matchers ───────────────────────────────────────────────────

def match(block: TimestampedLogBlock) -> bool:
    src = block.source_tag.lower()
    return "pdx_locali" in src or "gamedatabase" in src


# ── Volatile token patterns ───────────────────────────────────────────────

_LOC_KEY_RE = re.compile(r"'([A-Z][A-Z0-9_]{2,})'")
_QUOTED_FILE_RE = re.compile(r'"[^"\n]+"')
_BRACKET_OBJECT_RE = re.compile(r"\[[^\]\n]{1,80}\]")


# ── Dispatch ─────────────────────────────────────────────────────────────

def extract(block: TimestampedLogBlock) -> IssueDraft:
    src = block.source_tag.lower()
    if "pdx_locali" in src:
        return _extract_pdx_localize(block)
    return _extract_gamedatabase(block)


# ── pdx_localize.cpp ─────────────────────────────────────────────────────

def _extract_pdx_localize(block: TimestampedLogBlock) -> IssueDraft:
    header = block.header_line
    keys: list[str] = sorted(set(_LOC_KEY_RE.findall(header)))
    # Template: replace key literals and file paths
    templated = _LOC_KEY_RE.sub("'<KEY>'", header)
    templated = _QUOTED_FILE_RE.sub('"<FILE>"', templated)

    header_lower = header.lower()
    if "duplicate" in header_lower or "multiple" in header_lower or "present in both" in header_lower:
        error_type = "duplicate_key"
    elif "not found" in header_lower:
        error_type = "missing_key"
    else:
        error_type = "unknown"

    return IssueDraft(
        category="localization",
        error_type=error_type,
        tags=["debug_log"],
        engine_source=block.source_tag,
        sample_message=templated,
        primary_file=None,
        primary_line=None,
        referenced_symbols=keys,
        referenced_objects=[],
        extra_json={},
        severity="warning",
        confidence="high",
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )


# ── gamedatabase.h ───────────────────────────────────────────────────────

def _extract_gamedatabase(block: TimestampedLogBlock) -> IssueDraft:
    header = block.header_line
    # Preserve bracketed object names as referenced_objects
    objects: list[str] = sorted(set(_BRACKET_OBJECT_RE.findall(header)))
    # Template out brackets and quoted paths
    templated = _BRACKET_OBJECT_RE.sub("[<OBJECT>]", header)
    templated = _QUOTED_FILE_RE.sub('"<FILE>"', templated)

    header_lower = header.lower()
    if "overrid" in header_lower:  # covers: override, overriding, overridden
        error_type = "database_override"
    elif "duplicate" in header_lower:
        error_type = "duplicate_key"
    else:
        error_type = "unknown"

    return IssueDraft(
        category="database_reference",
        error_type=error_type,
        tags=["debug_log"],
        engine_source=block.source_tag,
        sample_message=templated,
        primary_file=None,
        primary_line=None,
        referenced_symbols=[],
        referenced_objects=objects,
        extra_json={},
        severity="warning",
        confidence="high",
        raw_block=block.raw_block,
        log_relpath=block.log_relpath,
        line_number=block.line_number,
    )
