"""Normalize an IssueDraft: mask volatile tokens, compute signature.

Signature formula (deterministic across processes and platforms):

    sig_input = (
        category + "\\n" +
        error_type + "\\n" +
        ",".join(sorted(tags)) + "\\n" +
        message_template
    )
    signature = hashlib.sha256(sig_input.encode("utf-8")).hexdigest()[:16]

Volatile masking is whitelist-only. Per-category extractors are expected
to template their own semantic placeholders into ``sample_message``
(e.g. ``<KEY>`` for localization keys); generic masking here only
handles infrastructure-volatile tokens (Windows paths, "near line N",
hex addresses, "at position N", date tokens).
"""
from __future__ import annotations

import hashlib
import re

from ck3chronicle.models.issue import IssueDraft, NormalizedIssue


# Order matters: more specific patterns first.
_WINDOWS_PATH_RE = re.compile(r"[A-Za-z]:\\[^\s\"']+")
_NEAR_LINE_RE = re.compile(r"\b(?:near|at)\s+line\s+\d+", re.IGNORECASE)
_LINE_COLON_RE = re.compile(r"\bline:\s*\d+\b", re.IGNORECASE)
_AT_POS_RE = re.compile(r"\bat\s+position\s+\d+", re.IGNORECASE)
_HEX_ADDR_RE = re.compile(r"0x[0-9A-Fa-f]+")
_DATE_TOKEN_RE = re.compile(r"\b\d{4}\.\d+\.\d+\b")
_ARGS_REF_RE = re.compile(r"\bargs#\d+\b")
_UNQUOTED_RELPATH_RE = re.compile(r"\b(?:common|events|history|localization|map_data|gfx|gui|interface|mod)/[^\s,;:]+")
# Real CK3 headers include timestamp/level/source and should not affect signatures.
_LOG_HEADER_RE = re.compile(r"^\[\d{2}:\d{2}:\d{2}\](?:\[[A-Z]\])?\[[^\]]+\]:\s*")
# Mask quoted relative asset/script paths such as "common/traits/00_traits.txt".
_QUOTED_RELPATH_RE = re.compile(r'"(?![A-Za-z]:)[^"\n]*(?:/|\\\\)[^"\n]*"')


def _mask_generic(text: str) -> str:
    """Apply whitelist-only volatile masking to *text*."""
    text = _LOG_HEADER_RE.sub("", text, count=1)
    text = _QUOTED_RELPATH_RE.sub('"<FILE>"', text)
    text = _WINDOWS_PATH_RE.sub("<TOKEN>", text)
    text = _UNQUOTED_RELPATH_RE.sub("<FILE>", text)
    text = _NEAR_LINE_RE.sub("<TOKEN>", text)
    text = _LINE_COLON_RE.sub("line:<N>", text)
    text = _AT_POS_RE.sub("<TOKEN>", text)
    text = _HEX_ADDR_RE.sub("<TOKEN>", text)
    text = _DATE_TOKEN_RE.sub("<TOKEN>", text)
    text = _ARGS_REF_RE.sub("args#<N>", text)
    return text


def normalize(draft: IssueDraft) -> NormalizedIssue:
    """Mask volatile tokens in ``draft.sample_message`` and compute signature."""
    text = draft.sample_message
    referenced_symbols = list(draft.referenced_symbols)

    # Category-specific templating happens inside the extractor by setting
    # sample_message with <KEY>/<TRAIT>/... already in place. Generic
    # volatile masking only handles infrastructure tokens here.
    text = _mask_generic(text)

    tags_sorted = sorted(draft.tags)
    # Keep signature focused on issue semantics, not file location.
    sig_input = (
        draft.category + "\n" +
        draft.error_type + "\n" +
        ",".join(tags_sorted) + "\n" +
        text
    )
    signature = hashlib.sha256(sig_input.encode("utf-8")).hexdigest()[:16]

    return NormalizedIssue(
        signature=signature,
        message_template=text,
        category=draft.category,
        error_type=draft.error_type,
        tags=list(tags_sorted),
        engine_source=draft.engine_source,
        sample_message=draft.sample_message,
        primary_file=draft.primary_file,
        primary_line=draft.primary_line,
        referenced_symbols=referenced_symbols,
        referenced_objects=list(draft.referenced_objects),
        extra_json=dict(draft.extra_json),
        severity=draft.severity,
        confidence=draft.confidence,
        raw_block=draft.raw_block,
        log_relpath=draft.log_relpath,
        line_number=draft.line_number,
    )
