"""Strict native CK3 lexing and byte-correspondent decoded text.

The caller supplies a protected input and its provenance. No Run is created.
Unrecognized leading bytes raise explicitly: they cannot be represented as a
recognized Emission. Malformed header-like lines after a header are continuations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import BinaryIO, Iterator

from .domain import ByteSpan, Emission, EvidenceSpan, OriginalAccess, SourceProvenance

PARSER_REVISION = "ck3-native-emissions-v1"
_HEADER_RE = re.compile(br"^\[(\d{2}:\d{2}:\d{2})\]\[([^\]\r\n]+)\]\[([^\]\r\n]+)\]:")
_SOURCE_LINE_SUFFIX_RE = re.compile(r":\d+$")
_UTF8_BOM = b"\xef\xbb\xbf"


class EmissionError(ValueError):
    """Input bytes cannot be accounted for as native emissions."""


def _parse_header(raw: bytes) -> tuple[str, str, str] | None:
    match = _HEADER_RE.match(raw)
    if match is None:
        return None
    try:
        return tuple(group.decode("utf-8", "strict") for group in match.groups())
    except UnicodeDecodeError:
        return None


def iter_emissions(
    stream: BinaryIO, *, provenance: SourceProvenance, original: OriginalAccess
) -> Iterator[Emission]:
    """Read a binary stream from byte zero; original must access that same input.

    Neither resource is closed here. Provenance validation/hash calculation is
    input-owner work. Empty input yields nothing; any preamble raises. Original
    access must remain available for subsequent recovery and native review.
    """
    if stream.tell() != 0:
        raise EmissionError("emission stream must start at byte zero")
    lines: list[bytes] = []
    start = offset = ordinal = 0
    start_line = last_line = 1
    parsed: tuple[str, str, str] | None = None

    def make(end_line: int) -> Emission:
        assert parsed is not None
        timestamp, level, source = parsed
        raw = b"".join(lines)
        return Emission(
            provenance, original, ByteSpan(start, start + len(raw)),
            ByteSpan(start, start + len(lines[0])), ordinal, start_line,
            end_line, timestamp, source, _SOURCE_LINE_SUFFIX_RE.sub("", source),
            level, raw.decode("utf-8", "replace"), PARSER_REVISION,
        )

    for line_number, raw_line in enumerate(stream, 1):
        if not isinstance(raw_line, bytes):
            raise TypeError("emission stream must be binary")
        last_line = line_number
        header = raw_line[3:] if offset == 0 and raw_line.startswith(_UTF8_BOM) else raw_line
        next_header = _parse_header(header)
        if next_header is not None:
            if lines:
                yield make(line_number - 1)
                ordinal += 1
            start, start_line, parsed = offset, line_number, next_header
            lines = [raw_line]
        elif lines:
            lines.append(raw_line)
        else:
            raise EmissionError(f"unrecognized preamble at bytes {offset}:{offset + len(raw_line)}")
        offset += len(raw_line)
    if lines:
        yield make(last_line)


def _coalesce(origins) -> tuple[EvidenceSpan, ...]:
    result: list[EvidenceSpan] = []
    seen = set()
    for origin in origins:
        if origin in seen:
            continue
        seen.add(origin)
        if result and result[-1].scope == origin.scope and result[-1].span.end == origin.span.start:
            result[-1] = EvidenceSpan(ByteSpan(result[-1].span.start, origin.span.end), origin.scope)
        else:
            result.append(origin)
    return tuple(result)


@dataclass(frozen=True)
class _Text:
    """Transient character correspondence; marks track values through edits."""

    text: str
    origins: tuple[tuple[EvidenceSpan, ...], ...]
    marks: tuple[frozenset[int], ...]
    anchor: EvidenceSpan

    def cut(self, start: int, end: int | None = None) -> _Text:
        end = len(self.text) if end is None else end
        anchor = self.origins[start][0] if start < len(self.text) else self.anchor
        if start == len(self.text) and self.origins:
            last = self.origins[-1][-1]
            anchor = EvidenceSpan(ByteSpan(last.span.end, last.span.end), last.scope)
        return _Text(self.text[start:end], self.origins[start:end], self.marks[start:end], anchor)

    def native_origins(self) -> tuple[EvidenceSpan, ...]:
        return _coalesce(o for origins in self.origins for o in origins) or (
            EvidenceSpan(ByteSpan(self.anchor.span.start, self.anchor.span.start), self.anchor.scope),
        )

    def literal(self, text: str) -> _Text:
        anchor = EvidenceSpan(ByteSpan(self.anchor.span.start, self.anchor.span.start), self.anchor.scope)
        return _Text(text, ((anchor,),) * len(text), (frozenset(),) * len(text), anchor)

    def join(self, parts) -> _Text:
        parts = tuple(parts)
        return _Text("".join(p.text for p in parts), tuple(o for p in parts for o in p.origins),
                     tuple(m for p in parts for m in p.marks), self.anchor)

    def strip(self, chars: str | None = None) -> _Text:
        start = len(self.text) - len(self.text.lstrip(chars))
        end = len(self.text.rstrip(chars))
        return self.cut(start, max(start, end))

    def sub(self, pattern: re.Pattern[str], replacement, count: int = 0) -> _Text:
        parts = []
        end = 0
        for index, match in enumerate(pattern.finditer(self.text)):
            if count and index >= count:
                break
            parts.extend((self.cut(end, match.start()), replacement(self, match)))
            end = match.end()
        parts.append(self.cut(end))
        return self.join(parts)


def _decode_text(raw: bytes, start: int, scope="child") -> _Text:
    # Strict decoding of at most one code point exposes precisely the bytes
    # consumed by each replacement. Re-encoding U+FFFD cannot recover these.
    chars: list[str] = []
    origins: list[tuple[EvidenceSpan, ...]] = []
    index = 0
    while index < len(raw):
        byte = raw[index]
        width = 2 if 0xC2 <= byte <= 0xDF else 3 if 0xE0 <= byte <= 0xEF else 4 if 0xF0 <= byte <= 0xF4 else 1
        chunk = raw[index:index + width]
        try:
            char = chunk.decode("utf-8", "strict")
            consumed = len(chunk)
        except UnicodeDecodeError as error:
            char, consumed = "\ufffd", error.end
        chars.append(char)
        origins.append((EvidenceSpan(ByteSpan(start + index, start + index + consumed), scope),))
        index += consumed
    anchor = EvidenceSpan(ByteSpan(start, start), scope)
    return _Text("".join(chars), tuple(origins), (frozenset(),) * len(chars), anchor)


def _collapse(text: _Text) -> _Text:
    return text.sub(re.compile(r"\s+"), lambda t, m: _Text(
        " ", (t.cut(*m.span()).native_origins(),), (frozenset(),), t.cut(m.start()).anchor
    )).strip()


def _message(emission: Emission) -> _Text:
    raw = emission.native_bytes()
    view = raw[3:] if emission.span.start == 0 and raw.startswith(_UTF8_BOM) else raw
    header = _HEADER_RE.match(view)
    if header is None or _parse_header(view) is None:
        raise EmissionError("original emission header no longer agrees with recognized input")
    start = len(raw) - len(view) + header.end()
    return _collapse(_decode_text(raw[start:], emission.span.start + start))
