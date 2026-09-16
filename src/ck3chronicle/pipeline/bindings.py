"""Native locator extraction and binding of already-validated positions.

No semantic projection, template alignment or whole-message rematching occurs
here. Grammar forms describe evidence syntax only, never diagnostic categories.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, replace
from typing import Iterable

from .domain import (ByteSpan, EvidenceSpan, LearnedVariable, NormalizedValue, NormalizedView, OccurrenceBinding,
                     OccurrenceValue, RecoveredDiagnostic, TokenSpan)
from .emissions import _Text, _collapse, _decode_text

_PATH_EXTENSIONS = (
    "txt|yml|yaml|gui|dds|asset|mesh|mod|json|wav|ogg|bank|png|tga"
)
_RELATIVE_ROOTS = (
    "mod|common|events|history|localization|gfx|gui|interface|map_data|"
    "game|dlc|music|sound|launcher|workshop"
)
_PATH_VALUE = (
    rf"(?:[A-Za-z]:[\\/][^\s\]\[\(\),;]+|"
    rf"(?:{_RELATIVE_ROOTS})[\\/][^\s\]\[\(\),;]+|"
    rf"[^\s\]\[\(\),;:'\"]+\.(?:{_PATH_EXTENSIONS}))"
)
_QUOTED_PATH_VALUE = rf"(?P<quote>['\"])(?P<quoted>{_PATH_VALUE})(?P=quote)"
_PATH_CAPTURE = rf"(?:{_QUOTED_PATH_VALUE}|(?P<plain>{_PATH_VALUE}))"

_FILE_LABEL_RE = re.compile(
    rf"\b(?:at\s+)?file\s*:\s*(?P<value>{_PATH_CAPTURE})"
    rf"(?:\s+(?:near\s+)?line\s*:?\s*(?P<line>\d+))?",
    re.IGNORECASE,
)
_QUOTED_NEAR_LINE_RE = re.compile(
    rf"(?P<value>{_QUOTED_PATH_VALUE})\s+near\s+line\s*:?\s*(?P<line>\d+)",
    re.IGNORECASE,
)
_PATH_LINE_RE = re.compile(
    rf"(?P<value>{_PATH_CAPTURE}):(?P<line>\d+)\b",
    re.IGNORECASE,
)
_LINE_COLUMN_IN_PATH_RE = re.compile(
    rf"\b(?:at\s+)?line\s*:?\s*(?P<line>\d+)\s+and\s+column\s*:?\s*\d+"
    rf"\s+in\s+(?P<value>{_PATH_CAPTURE})",
    re.IGNORECASE,
)
_OPAQUE_FILE_LABEL_RE = re.compile(
    r"\b(?:Near\s+)?file\s*:\s*(?P<value>[A-Za-z_][A-Za-z0-9_#@.-]*)"
    r"\s+(?:near\s+)?line\s*:?\s*(?P<line>\d+)",
    re.IGNORECASE,
)
_BARE_PATH_RE = re.compile(rf"(?P<value>{_PATH_CAPTURE})", re.IGNORECASE)
_EVENT_URI_RE = re.compile(r"\[\s*event\s*:\s*(?P<value>/[^\]]+)\]", re.IGNORECASE)


@dataclass(frozen=True)
class LocatorEvidence:
    """Original spelling/spans, with event_uri distinct from filesystem forms."""

    value: OccurrenceValue
    line_value: OccurrenceValue | None
    form: str

    @property
    def line(self) -> int | None:
        return int(self.line_value.text) if self.line_value is not None else None


def _path_span(match: re.Match[str]) -> tuple[int, int]:
    for group in ("quoted", "plain"):
        if match.groupdict().get(group) is not None:
            return match.span(group)
    start, end = match.span("value")
    raw = match.group("value")
    left = len(raw) - len(raw.lstrip())
    right = len(raw.rstrip())
    raw = raw.strip()
    if len(raw) > 1 and raw[0] == raw[-1] and raw[0] in "'\"":
        left += 1
        right -= 1
    return start + left, start + right


def _overlaps(span: tuple[int, int], occupied: list[tuple[int, int]]) -> bool:
    return any(span[0] < other[1] and other[0] < span[1] for other in occupied)


def _extract_locators(text: _Text, original) -> tuple[LocatorEvidence, ...]:
    def value(span):
        origins = text.cut(*span).native_origins()
        chunks = []
        for origin in origins:
            raw = original.read_bytes(origin.span)
            if len(raw) != origin.span.end - origin.span.start:
                raise ValueError("incomplete original locator read")
            chunks.append(raw)
        return OccurrenceValue(b"".join(chunks).decode("utf-8", "replace"), origins)

    matches = []
    occupied = []
    for match in _EVENT_URI_RE.finditer(text.text):
        occupied.append(match.span())
        matches.append((match.start(), match.end(), LocatorEvidence(value(match.span("value")), None, "event_uri")))
    patterns = (
        ("file_line", _FILE_LABEL_RE),
        ("quoted_near_line", _QUOTED_NEAR_LINE_RE),
        ("path_line", _PATH_LINE_RE),
        ("line_column_in_path", _LINE_COLUMN_IN_PATH_RE),
        ("opaque_file_line", _OPAQUE_FILE_LABEL_RE),
        ("path", _BARE_PATH_RE),
    )
    for form, pattern in patterns:
        for match in pattern.finditer(text.text):
            if _overlaps(match.span(), occupied):
                continue
            line = value(match.span("line")) if match.groupdict().get("line") is not None else None
            matches.append((match.start(), match.end(), LocatorEvidence(value(_path_span(match)), line, form)))
            occupied.append(match.span())
    return tuple(item[2] for item in sorted(matches, key=lambda item: item[:2]))


def extract_locators(diagnostic: RecoveredDiagnostic) -> tuple[LocatorEvidence, ...]:
    """Extract from this child and its envelope only, never from a sibling."""
    result = []
    spans = [(span, "child") for span in diagnostic.local_spans]
    spans.extend((span, "shared_envelope") for span in diagnostic.shared_spans)
    for span, scope in sorted(spans, key=lambda item: item[0].start):
        raw = diagnostic.parent.original.read_bytes(span)
        if len(raw) != span.end - span.start:
            raise ValueError("incomplete original locator evidence read")
        result.extend(_extract_locators(_collapse(_decode_text(raw, span.start, scope)), diagnostic.parent.original))
    return tuple(result)


@dataclass(frozen=True)
class ValidatedPosition:
    """Matcher-supplied template variable and occurrence map position.

    token_span indexes this view (not the learned template). value_index selects
    the exact entry in view.values, including when several values share a
    collapsed locator token. The matcher owns learned/typed validation.
    """

    variable: LearnedVariable
    token_span: TokenSpan
    value_index: int


def bind_original_values(
    view: NormalizedView, positions: Iterable[ValidatedPosition]
) -> tuple[OccurrenceBinding, ...]:
    """Resolve explicit validated positions without reading or searching text.

    Missing, out-of-range, duplicate or mismatched map positions fail explicitly.
    A removed locator has no template position and cannot be bound this way.
    """
    result = []
    seen = set()
    for position in positions:
        if position.variable in seen:
            raise ValueError("duplicate learned variable binding")
        if not 0 <= position.value_index < len(view.values):
            raise ValueError("validated value index is outside the original-value map")
        value = view.values[position.value_index]
        if value.token_span is None or value.token_span != position.token_span:
            raise ValueError("validated token position disagrees with preserved value")
        seen.add(position.variable)
        result.append(OccurrenceBinding(position.variable, value))
    return tuple(result)


def bind_matched_spans(
    view: NormalizedView, matches: Iterable[tuple[LearnedVariable, TokenSpan]]
) -> tuple[NormalizedView, tuple[OccurrenceBinding, ...]]:
    """Bridge matcher spans to the existing explicit value-index interface.

    Learned variables can cover multiple tokens; coalesced locator tokens can
    also cover several original values. Preserve those interval values in a
    new immutable view before binding. Compose only supplied token origins,
    never normalize or search raw text. Interior whitespace/punctuation is
    included only within one already-owned child/shared evidence span.
    """
    values = list(view.values)
    positions = []
    for variable, span in matches:
        if not 0 <= span.start < span.end <= len(view.tokens):
            raise ValueError("matched variable must occupy normalized tokens")
        origins = sorted(set(o for token in view.tokens[span.start:span.end]
                             for o in token.origins),
                         key=lambda o: (o.span.start, o.span.end, o.scope))
        nonempty = [o for o in origins if o.span.start < o.span.end]
        origins = nonempty or origins
        merged = []
        for origin in origins:
            owned = (view.diagnostic.local_spans if origin.scope == "child"
                     else view.diagnostic.shared_spans)
            if not any(s.contains(origin.span) for s in owned):
                raise ValueError("token origin is outside diagnostic evidence")
            if merged and merged[-1].scope == origin.scope:
                envelope = ByteSpan(merged[-1].span.start,
                                    max(merged[-1].span.end, origin.span.end))
                if any(s.contains(envelope) for s in owned):
                    merged[-1] = EvidenceSpan(envelope, origin.scope)
                    continue
            merged.append(origin)
        exact_origins = tuple(merged)
        index = next((i for i, value in enumerate(values)
                      if value.token_span == span and value.value.origins == exact_origins), None)
        if index is None:
            chunks = []
            for origin in exact_origins:
                raw = view.diagnostic.parent.original.read_bytes(origin.span)
                if len(raw) != origin.span.end - origin.span.start:
                    raise ValueError("incomplete original matched span read")
                chunks.append(raw)
            value = OccurrenceValue(b"".join(chunks).decode("utf-8", "replace"), exact_origins)
            index = len(values)
            values.append(NormalizedValue(value, span))
        positions.append(ValidatedPosition(variable, span, index))
    bound_view = replace(view, values=tuple(values))
    return bound_view, bind_original_values(bound_view, positions)
