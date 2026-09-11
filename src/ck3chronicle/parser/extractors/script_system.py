"""script_system extractor: blocks emitted by script_system.cpp.

Emits ``(category, error_type)`` pairs using fine-grained error types
derived from the heritage taxonomy in
``error analysis prototype/parse_script_errors.py`` (§5.3 heritage asset).

Heritage error_type values (24 specific + 1 default):
  failed_context_switch, wrong_scope, scope_type_mismatch, null_scope_object,
  unset_scope, null_fetch, invalid_comparison, variable_scope_error,
  no_capital, invalid_legitimacy, asset_visual_error, unknown_loc_key,
  postvalidate_false, else_not_after_if, more_than_one_effect,
  unknown_effect, unknown_trigger, unknown_modifier, unknown_value,
  unknown_token, duplicate_definition, type_mismatch, undefined_symbol,
  out_of_range, syntax_error (default)
"""
from __future__ import annotations

import re

from ck3chronicle.models.issue import IssueDraft
from ck3chronicle.parser.log_blocks import TimestampedLogBlock

CATEGORY = "script_system"

_FILE_LINE_RE = re.compile(r'"([^"]+)"\s+near\s+line\s+(\d+)', re.IGNORECASE)

# ── Heritage taxonomy patterns (order: most specific first) ───────────────
# Sourced from error analysis prototype/parse_script_errors.py CLUSTERS list.
_HERITAGE_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("failed_context_switch",  re.compile(r"Failed context switch", re.I)),
    ("wrong_scope",            re.compile(r"Wrong scope for (?:trigger|effect|modifier)", re.I)),
    ("scope_type_mismatch",    re.compile(r"did not get a matching scope type|expected .{0,60} but got", re.I)),
    ("null_scope_object",      re.compile(r"Scoped object.{0,60}is not valid|\bwas null\b|character was null", re.I)),
    ("unset_scope",            re.compile(r"returned an unset scope|Failed to fetch (?:key|variable) for", re.I)),
    ("null_fetch",             re.compile(r"Fetched null|returned null", re.I)),
    ("invalid_comparison",     re.compile(r"Invalid (?:left|right) side during comparison", re.I)),
    ("variable_scope_error",   re.compile(r"Variable not of the .value. scope type|This scope doesn.t support variables|does not have variables", re.I)),
    ("no_capital",             re.compile(r"has no capital|Character with no location", re.I)),
    ("invalid_legitimacy",     re.compile(r"doesn.t have valid legitimacy type", re.I)),
    ("asset_visual_error",     re.compile(r"Couldn.t determine .asset. visual type", re.I)),
    ("unknown_loc_key",        re.compile(r"Unknown loc key", re.I)),
    ("postvalidate_false",     re.compile(r"PostValidate.{0,60}returned false|postvalidate", re.I)),
    ("else_not_after_if",      re.compile(r"else.{0,20}not.{0,20}if|else_if.{0,5}not", re.I)),
    ("more_than_one_effect",   re.compile(r"more than one.{0,20}effect|multiple effect", re.I)),
    ("unknown_effect",         re.compile(r"unknown effect", re.I)),
    ("unknown_trigger",        re.compile(r"unknown trigger", re.I)),
    ("unknown_modifier",       re.compile(r"unknown modifier", re.I)),
    ("unknown_value",          re.compile(r"unknown value|invalid value", re.I)),
    ("unknown_token",          re.compile(r"unexpected token|unexpected symbol", re.I)),
    ("duplicate_definition",   re.compile(r"duplicate|already defined|redefinition", re.I)),
    ("type_mismatch",          re.compile(r"type mismatch|wrong type", re.I)),
    ("undefined_symbol",       re.compile(r"undefined|not defined|could not find", re.I)),
    ("out_of_range",           re.compile(r"out of range", re.I)),
]


def _classify_error_type(text: str) -> str:
    """Return the most specific matching heritage error_type, or 'syntax_error'."""
    for label, pat in _HERITAGE_PATTERNS:
        if pat.search(text):
            return label
    return "syntax_error"


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
    for cont in block.continuation_lines:
        token = cont.strip()
        if token:
            referenced_objects.append(token)

    error_type = _classify_error_type(header)

    return IssueDraft(
        category=CATEGORY,
        error_type=error_type,
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
