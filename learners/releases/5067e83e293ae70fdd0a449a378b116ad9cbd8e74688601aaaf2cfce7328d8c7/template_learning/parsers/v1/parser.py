"""Lossless CK3 framing and lexical boundaries; no learned semantics.

This file is the complete versioned implementation. Keep it self-contained.
Native offsets are absolute half-open byte intervals. Text uses UTF-8 with
surrogateescape so even undecodable bytes round-trip without replacement loss.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
import re
import unicodedata

VERSION = "ck3-lossless-v1.6"
_HEADER = re.compile(br"^\[(\d{2}:\d{2}:\d{2})\]\[([^\]\r\n]+)\]\[([^\]\r\n]+)\]:", re.MULTILINE)
_SOURCE_LINE = re.compile(r":\d+$")
_BOM = b"\xef\xbb\xbf"
# Owner-approved exact lexical exception. It is not a path rule or a substring
# replacement; the independently versioned artifact owns its implementation.
ATOMIC_LEXEMES = frozenset({"Div/0"})
# Each separator is emitted individually wherever it occurs. These rules apply
# to raw characters, not filename/slot recognition. @ and _ are not separators.
ALWAYS_SEPARATORS = frozenset(':/\\{}[]()"=;|')
_NON_ASCII = re.compile(r"[^\x00-\x7f]")


@lru_cache(maxsize=64)
def _scanner(unicode_punctuation: str):
    """Compile the same token rules with native Unicode boundary punctuation.

    Unicode P* categories supply the existing non-ASCII punctuation convention.
    ASCII edge rules retain dots, signs, @, _ and ! inside continuous strings;
    leading ! is filename content, while a trailing ! is sentence punctuation.
    """
    separators = re.escape("".join(sorted(ALWAYS_SEPARATORS)))
    leading = re.escape("',<>" + unicode_punctuation)
    trailing = re.escape("',.!?<>" + unicode_punctuation)
    end = rf"(?:$|[\s{separators}])"
    # Div/0 is an exact atom, never a substring of a symbol or path. A slash
    # or backslash immediately on either side prevents the atomic exception.
    atom_boundary = re.escape("".join(sorted(ALWAYS_SEPARATORS - {'/', '\\'})))
    atom_end = rf"(?:$|[\s{atom_boundary}])"
    atoms = "|".join(re.escape(value) for value in sorted(ATOMIC_LEXEMES))
    return re.compile("|".join((
        rf"(?<![^\s{atom_boundary}{leading}])(?:{atoms})(?={atom_end}|[{trailing}]+(?={atom_end}))",
        rf"(?<![^\s{separators}])\.{{1,2}}(?={end})",
        rf"(?<![^\s{separators}])[{leading}]|[{trailing}](?=[{trailing}]*{end})",
        rf"[{separators}]",
        r"\s+",
        rf"[^\s{separators}]+?(?=[{trailing}]*{end})",
    )))


@dataclass(frozen=True)
class Span:
    start: int
    end: int

    def __post_init__(self):
        if not 0 <= self.start <= self.end:
            raise ValueError("invalid byte span")

    def contains(self, other) -> bool:
        return self.start <= other.start <= other.end <= self.end


@dataclass(frozen=True)
class Source:
    name: str
    data: bytes

    def read_bytes(self, span: Span) -> bytes:
        if not 0 <= span.start <= span.end <= len(self.data):
            raise ValueError("range outside original input")
        return self.data[span.start:span.end]

    def read_text(self, span: Span) -> str:
        return self.read_bytes(span).decode("utf-8", "surrogateescape")


@dataclass(frozen=True)
class Piece:
    span: Span
    text: str
    kind: str  # token or gap; never a semantic slot type


def lexical_pieces(source: Source, span: Span) -> tuple[Piece, ...]:
    """Scan exact token/gap ranges; always-separators never join other text."""
    text = source.read_text(span)
    unicode_punctuation = "".join(sorted({m.group() for m in _NON_ASCII.finditer(text)
        if unicodedata.category(m.group()).startswith("P")}))
    offset = span.start
    char_offset = 0
    pieces = []
    for match in _scanner(unicode_punctuation).finditer(text):
        if match.start() != char_offset:
            raise ValueError("lexer omitted native characters")
        value = match.group()
        end = offset + len(value.encode("utf-8", "surrogateescape"))
        pieces.append(Piece(Span(offset, end), value, "gap" if value.isspace() else "token"))
        offset, char_offset = end, match.end()
    if char_offset != len(text) or offset != span.end:
        raise ValueError("lexer did not cover the complete native range")
    return tuple(pieces)


@dataclass(frozen=True)
class Emission:
    original: Source
    span: Span
    header_span: Span
    body_span: Span
    ordinal: int
    start_line: int
    end_line: int
    timestamp: str
    level: str
    source_tag: str
    source_family: str

    @property
    def identity(self):
        return self.original.name, self.ordinal

    def native_bytes(self) -> bytes:
        return self.original.read_bytes(self.span)

    @property
    def decoded_text(self) -> str:
        return self.original.read_text(self.span)

    @property
    def body_text(self) -> str:
        return self.original.read_text(self.body_span)

    @property
    def pieces(self) -> tuple[Piece, ...]:
        return lexical_pieces(self.original, self.body_span)

    @property
    def tokens(self) -> tuple[Piece, ...]:
        return tuple(piece for piece in self.pieces if piece.kind == "token")

    def select_messages(self, ranges: tuple[tuple[int, int], ...]):
        return select_messages(self, tuple(Span(start, end) for start, end in ranges))

    @property
    def recovery(self) -> Recovery:
        return recover_messages(self)


@dataclass(frozen=True)
class MessageSelection:
    """Original message range, with references to its emission and shared context.

    Manual range selection establishes positions only. Recovery.status records
    whether the parser established the message boundaries automatically.
    """
    parent: Emission
    span: Span
    ordinal: int
    shared_spans: tuple[Span, ...]

    @property
    def text(self) -> str:
        return self.parent.original.read_text(self.span)

    @property
    def pieces(self) -> tuple[Piece, ...]:
        return lexical_pieces(self.parent.original, self.span)

    @property
    def tokens(self) -> tuple[Piece, ...]:
        return tuple(piece for piece in self.pieces if piece.kind == "token")

    def native_bytes(self) -> bytes:
        return self.parent.original.read_bytes(self.span)


def select_messages(emission: Emission, spans: tuple[Span, ...]) -> tuple[MessageSelection, ...]:
    """Bind already established message boundaries; complement remains shared.

    The caller (learning research or model-directed refinement) supplies ordered,
    disjoint body ranges. This function validates ranges, not their semantics.
    It never reports an unsplit emission as a confirmed individual message.
    """
    cursor = emission.span.start
    shared = []
    for span in spans:
        if (span.start == span.end or not emission.body_span.contains(span)
                or span.start < cursor):
            raise ValueError("message ranges must be nonempty, ordered and inside the body")
        if cursor < span.start:
            shared.append(Span(cursor, span.start))
        cursor = span.end
    if cursor < emission.span.end:
        shared.append(Span(cursor, emission.span.end))
    shared_spans = tuple(shared)
    return tuple(MessageSelection(emission, span, ordinal, shared_spans)
                 for ordinal, span in enumerate(spans))


@dataclass(frozen=True)
class Recovery:
    """A byte partition and an explicit boundary-recovery outcome.

    All messages share the same context tuple; no native text is copied here.
    Shared ranges include framing and separating whitespace, not just semantic
    context. Unresolved content is never presented as a confirmed single error.
    Structure names describe syntax, not error types, slots or L1/L2 meaning.
    """
    parent: Emission
    status: str  # recovered or unresolved
    structure: str | None
    messages: tuple[MessageSelection, ...]
    shared_spans: tuple[Span, ...]
    unresolved_spans: tuple[Span, ...]
    reason: str | None = None

    @property
    def ordered_spans(self) -> tuple[Span, ...]:
        """Each original byte exactly once, in emission order."""
        return tuple(sorted((*self.shared_spans, *self.unresolved_spans,
                             *(message.span for message in self.messages)),
                            key=lambda span: span.start))


_WRAPPER_START = re.compile(br'[ \t\r\n]*Error[ \t]*:[ \t]*"')
_WRAPPER = re.compile(
    br'[ \t\r\n]*Error[ \t]*:[ \t]*"(?P<inner>[^\"]*)"'
    br'[ \t]+in[ \t]+file[ \t]*:[ \t]*"[^"\r\n]*"'
    br'[ \t]+near[ \t]+line[ \t]*:[ \t]*[0-9]+[ \t\r\n]*')
_NEAR_LINE = re.compile(br',[ \t]+near[ \t]+line[ \t]*:[ \t]*[0-9]+')
_LOCATED_ENTRY = re.compile(
    br'[^\r\n]+,[ \t]+near[ \t]+line[ \t]*:[ \t]*[0-9]+'
    br'(?:[ \t]+\(expanded[ \t]+from[ \t]+file[ \t]*:[^\r\n]*'
    br'[ \t]+line[ \t]*:[ \t]*[0-9]+\))?[ \t]*')
_SCRIPT_START = re.compile(br'Script system error!(?:[ \t]+\([^\r\n]*\))?')
_FILE_LOCATION = re.compile(br'file:[ \t]*[^\r\n]*[ \t]+line:[ \t]*[0-9]+(?:[ \t]+[^\r\n]*)?')


def _single_structure(emission: Emission, body: bytes) -> str | None:
    """Recognize evidenced single-message envelopes without dividing reasons.

    Structural envelopes are source-independent where their syntax identifies
    them. A few content-only forms need source applicability as well. Unknown
    multiline forms do not pass merely because no repeated wrapper was found.
    """
    lines = [line.strip(b" \t\r") for line in body.split(b"\n")
             if line.strip(b" \t\r")]
    if not lines:
        return None
    first, tail = lines[0], lines[1:]
    if _SCRIPT_START.fullmatch(first):
        errors = [i for i, line in enumerate(lines) if line.startswith(b"Error:")]
        locations = [i for i, line in enumerate(lines) if line.startswith(b"Script location:")]
        if errors != [1] or len(locations) != 1 or locations[0] <= 1:
            return None
        location = locations[0]
        # The Error field may be plain text or a multiline failure/reason.
        # Its envelope, not brackets or a presumed L1/L2 formulation, establishes
        # one message. Never balance arbitrary CK3 keys or quoted prose here.
        if not b" ".join(lines[1:location]).removeprefix(b"Error:").strip():
            return None
        where = lines[location].removeprefix(b"Script location:").strip(b" \t")
        if where != b"Unknown" and not _FILE_LOCATION.fullmatch(where):
            return None
        if not all(_FILE_LOCATION.fullmatch(line) for line in lines[location + 1:]):
            return None
        return "script-error"
    if len(lines) == 1:
        return "single-line"
    if tail[0] == b"Stack trace:" and len(tail) > 1:
        if all(_FILE_LOCATION.fullmatch(line) for line in tail[1:]):
            return "message-with-stack-trace"
    if len(tail) == 1 and tail[0].startswith(b"From:"):
        where = tail[0].removeprefix(b"From:").strip(b" \t")
        if len(where) > 1 and where[:1] == where[-1:] == b"'" and _FILE_LOCATION.fullmatch(where[1:-1]):
            return "message-with-from-location"
    if (first.endswith(b"for scope:") and len(tail) == 2
            and tail[0].startswith(b"Root:") and tail[1] == b"Saved event targets:"):
        return "message-with-scope-context"
    if (emission.source_family == "jomini_effect_impl.cpp" and len(tail) == 2
            and tail[0].startswith(b"Cheater:") and tail[1].startswith(b"With:")):
        return "message-with-participants"
    if (emission.source_family in {"faction.cpp", "character_commands.cpp"}
            and len(tail) == 1 and tail[0].startswith((b"\x15", b"\x16"))):
        return "message-with-formatted-reason"
    quoted = {
        "pdx_data_localize.cpp": b"Data error in loc string '",
        "pdx_text_formatter.cpp": b"Unknown formatting tag '",
    }
    prefix = quoted.get(emission.source_family)
    if prefix and body.strip(b" \t\r\n").startswith(prefix) and lines[-1].endswith(b"'"):
        return "message-with-quoted-multiline-value"
    return None


def recover_messages(emission: Emission) -> Recovery:
    """Recover independent messages using native framing, never model meaning."""
    body = emission.original.read_bytes(emission.body_span)

    def unresolved(reason):
        return Recovery(emission, "unresolved", None, (), (emission.header_span,),
                        (emission.body_span,), reason)

    def recovered(structure, spans):
        messages = select_messages(emission, tuple(spans))
        return Recovery(emission, "recovered", structure, messages,
                        messages[0].shared_spans, ())

    # A wrapper candidate must establish its complete syntax even on one line.
    # Repeated error wording, source filenames and slot knowledge are irrelevant.
    if _WRAPPER_START.match(body):
        wrapper = _WRAPPER.fullmatch(body)
        if wrapper is None:
            return unresolved("quoted error wrapper has unsupported or ambiguous framing")
        inner = wrapper.group("inner")
        offset = emission.body_span.start + wrapper.start("inner")
        spans = []
        for line in inner.split(b"\n"):
            content = line[:-1] if line.endswith(b"\r") else line
            if not _LOCATED_ENTRY.fullmatch(content) or len(_NEAR_LINE.findall(content)) != 1:
                return unresolved("wrapper entry does not establish one complete located message")
            spans.append(Span(offset, offset + len(content)))
            offset += len(line) + 1
        return recovered("located-message-wrapper", spans)

    structure = _single_structure(emission, body)
    if structure is not None:
        return recovered(structure, (emission.body_span,))
    return unresolved("no supported individual-message structure established")


@dataclass(frozen=True)
class RawParse:
    source: Source
    parser_reference: dict
    emissions: tuple[Emission, ...]

    def read_bytes(self, span: Span) -> bytes:
        return self.source.read_bytes(span)

    def read_text(self, span: Span) -> str:
        return self.source.read_text(span)

    def bytes_between(self, start: int, end: int) -> bytes:
        return self.read_bytes(Span(start, end))

    def text_between(self, start: int, end: int) -> str:
        return self.read_text(Span(start, end))

    def debug_document(self) -> dict:
        """Optional inspectable snapshot, containing its original bytes once."""
        def bounds(span):
            return [span.start, span.end]
        def recovery_document(emission):
            recovery = emission.recovery
            return {
                "status": recovery.status, "structure": recovery.structure,
                "reason": recovery.reason,
                "shared_spans": [bounds(span) for span in recovery.shared_spans],
                "unresolved_spans": [bounds(span) for span in recovery.unresolved_spans],
                "messages": [{"ordinal": message.ordinal, "span": bounds(message.span)}
                             for message in recovery.messages],
            }
        return {
            "format": "ck3-raw-parse-v1",
            "parser": self.parser_reference,
            "source_name": self.source.name,
            "original_base64": base64.b64encode(self.source.data).decode("ascii"),
            "emissions": [{
                "ordinal": e.ordinal, "span": bounds(e.span),
                "header_span": bounds(e.header_span), "body_span": bounds(e.body_span),
                "start_line": e.start_line, "end_line": e.end_line,
                "timestamp": e.timestamp, "level": e.level,
                "source_tag": e.source_tag, "source_family": e.source_family,
                "pieces": [{"span": bounds(p.span), "text": p.text, "kind": p.kind}
                           for p in e.pieces],
                "recovery": recovery_document(e),
            } for e in self.emissions],
        }

    def save_debug(self, path: Path | str) -> None:
        # ensure_ascii also preserves surrogateescape characters in JSON.
        Path(path).write_text(json.dumps(self.debug_document(), ensure_ascii=True,
                                        indent=2) + "\n", encoding="utf-8")


def parse_bytes(data: bytes, *, source_name: str, parser_reference: dict) -> RawParse:
    if not isinstance(data, bytes):
        raise TypeError("raw parsing requires bytes")
    source = Source(source_name, data)
    # A byte-order mark belongs to the first emission, never to its body.
    origin = len(_BOM) if data.startswith(_BOM) else 0
    matches = list(_HEADER.finditer(data[origin:]))
    if data and (not matches or matches[0].start() != 0):
        raise ValueError("input does not begin with a native CK3 header")
    emissions = []
    line = 1
    for ordinal, match in enumerate(matches):
        start = 0 if ordinal == 0 else match.start() + origin
        end = matches[ordinal + 1].start() + origin if ordinal + 1 < len(matches) else len(data)
        body_start = match.end() + origin
        segment = data[start:end]
        newline_count = segment.count(b"\n")
        end_line = line + newline_count - int(segment.endswith(b"\n"))
        timestamp, level, tag = (group.decode("utf-8", "surrogateescape") for group in match.groups())
        emissions.append(Emission(source, Span(start, end), Span(start, body_start),
                                  Span(body_start, end), ordinal, line, end_line,
                                  timestamp, level, tag, _SOURCE_LINE.sub("", tag)))
        line += newline_count
    return RawParse(source, dict(parser_reference), tuple(emissions))


def load_debug(path: Path, parser_reference: dict) -> RawParse:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("format") != "ck3-raw-parse-v1" or document.get("parser") != parser_reference:
        raise ValueError("debug output does not belong to the selected parser")
    result = parse_bytes(base64.b64decode(document["original_base64"], validate=True),
                         source_name=document["source_name"], parser_reference=parser_reference)
    if result.debug_document() != document:
        raise ValueError("debug output disagrees with its original bytes and selected parser")
    return result
