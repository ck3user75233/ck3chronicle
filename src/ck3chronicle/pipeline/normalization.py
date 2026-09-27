"""Literal matching view with native correspondence and whitespace boundaries.

No sentence recognition, slot inference, masks, or literal rewriting occurs
here. Slots are assigned only by the supplied template during matching.
"""
from __future__ import annotations

import re

from .diagnostics import _diagnostic_text
from .domain import MatchingToken, NormalizedValue, NormalizedView, RecoveredDiagnostic

NORMALIZER_REVISION = "ck3-native-literal-view-v2"

# Punctuation remains matchable literally or as part of a candidate slot.
# Word runs include Unicode and numbers; no key alphabet is inferred here.
TOKEN_RE = re.compile(r"\w+|[^\w\s]")


def tokenize(text: str) -> tuple[str, ...]:
    """Tokenize literal text without interpreting its content."""
    return tuple(TOKEN_RE.findall(text))


def normalize_for_match(diagnostic: RecoveredDiagnostic) -> NormalizedView:
    """Retain every non-whitespace character and its original byte origins.

    Recovery owns native framing and child boundaries. Whitespace is excluded
    from tokens, but adjacency is retained for single-string KEY slots and
    original spans retain the exact whitespace inside multi-word captures.
    """
    text = _diagnostic_text(diagnostic)
    tokens = []
    previous_end = None
    for match in TOKEN_RE.finditer(text.text):
        piece = text.cut(*match.span())
        tokens.append(MatchingToken(piece.text, piece.native_origins(),
                                    joined_to_previous=match.start() == previous_end))
        previous_end = match.end()
    values = tuple(NormalizedValue(value, None) for value in diagnostic.values)
    return NormalizedView(diagnostic, NORMALIZER_REVISION, tuple(tokens), values)
