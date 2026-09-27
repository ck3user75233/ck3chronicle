"""Native byte correspondence and v3 matching results.

The selected-parser path uses NativeDiagnostic and NativeClassification. Earlier
framing/view types remain solely for the learner's historical parser comparison;
they are not consumed by the selected model reader, classifier or bindings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class ByteSpan:
    """Absolute [start, end) byte boundaries in the protected log."""

    start: int
    end: int

    def __post_init__(self) -> None:
        if not 0 <= self.start <= self.end:
            raise ValueError("invalid byte span")

    def contains(self, other: ByteSpan) -> bool:
        return self.start <= other.start <= other.end <= self.end


@dataclass(frozen=True)
class TokenSpan:
    """[start, end) indices in NormalizedView.tokens; may be empty."""

    start: int
    end: int

    def __post_init__(self) -> None:
        if not 0 <= self.start <= self.end:
            raise ValueError("invalid token span")


class OriginalAccess(Protocol):
    """Read-only access supplied by the input owner, valid during processing.

    Implementations return exactly the requested original bytes or raise;
    they never re-encode decoded text or silently return a short read.
    """

    def read_bytes(self, span: ByteSpan) -> bytes: ...


@dataclass(frozen=True)
class SourceProvenance:
    """Supplied protected-input facts, independent of a successful Run ID."""

    evidence_id: str
    log_relpath: str
    sha256: str


@dataclass(frozen=True)
class Emission:
    """One recognized header and its continuations in original order.

    ordinal is zero-based within this input; line numbers are one-based and
    inclusive. header_span includes the native header's line ending, if any.
    decoded_text contains the unmasked emission, possibly replacement-decoded.
    provenance plus ordinal identifies the emission without hashing text.
    """

    provenance: SourceProvenance
    original: OriginalAccess
    span: ByteSpan
    header_span: ByteSpan
    ordinal: int
    start_line: int
    end_line: int
    timestamp: str
    source_tag: str
    source_family: str
    level: str | None
    decoded_text: str
    parser_revision: str

    def __post_init__(self) -> None:
        if self.ordinal < 0 or not 1 <= self.start_line <= self.end_line:
            raise ValueError("invalid emission order or line boundaries")
        if self.header_span.start != self.span.start or not self.span.contains(self.header_span):
            raise ValueError("header must begin and lie within the emission")

    @property
    def identity(self) -> tuple[str, int]:
        return self.provenance.evidence_id, self.ordinal

    def native_bytes(self) -> bytes:
        data = self.original.read_bytes(self.span)
        if len(data) != self.span.end - self.span.start:
            raise ValueError("original access returned an incomplete emission")
        return data


EvidenceScope = Literal["child", "shared_envelope"]


@dataclass(frozen=True)
class EvidenceSpan:
    """Original bytes belonging to this child or its shared envelope."""

    span: ByteSpan
    scope: EvidenceScope


@dataclass(frozen=True)
class OccurrenceValue:
    """A concrete, unmasked decoded value, with exact native correspondence.

    origins are ordered, possibly discontiguous original spans. No semantic
    role or supplied slot definition is inferred from this value. An absent
    template-declared OPTIONAL_KEY has empty text and a zero-width origin at
    the matched native boundary; normalization never inserts an optional.
    """

    text: str
    origins: tuple[EvidenceSpan, ...]

    def __post_init__(self) -> None:
        if not self.origins:
            raise ValueError("an occurrence value requires original correspondence")


@dataclass(frozen=True)
class RecoveredDiagnostic:
    """One child, retaining its parent and local/shared native boundaries.

    ordinal is zero-based within the parent. local_spans identify the child;
    shared_spans identify reused envelope evidence, including any shared
    header/locator. All spans are absolute, never child-relative. decoded_text
    is the unmasked recovered matching message. Recovery may attach values
    before normalization; extraction itself belongs to the recovery owner.
    """

    parent: Emission
    ordinal: int
    local_spans: tuple[ByteSpan, ...]
    shared_spans: tuple[ByteSpan, ...]
    decoded_text: str
    recovery_revision: str
    values: tuple[OccurrenceValue, ...] = ()

    def __post_init__(self) -> None:
        if self.ordinal < 0 or not self.local_spans:
            raise ValueError("a diagnostic requires child order and boundaries")
        if any(not self.parent.span.contains(s) for s in (*self.local_spans, *self.shared_spans)):
            raise ValueError("child evidence must lie within its parent emission")

    @property
    def identity(self) -> tuple[str, int, int]:
        return (*self.parent.identity, self.ordinal)


@dataclass(frozen=True)
class MatchingToken:
    """One literal token and its original byte origins.

    joined_to_previous preserves the absence of intervening whitespace. It
    describes lexical adjacency, not a slot boundary or a semantic type.
    """

    text: str
    origins: tuple[EvidenceSpan, ...]
    joined_to_previous: bool = False

    def __post_init__(self) -> None:
        if not self.origins:
            raise ValueError("a matching token requires original correspondence")


@dataclass(frozen=True)
class NormalizedValue:
    """Preserved value and its matcher-assigned token interval.

    None denotes recovery evidence that has not been assigned to a slot.
    """

    value: OccurrenceValue
    token_span: TokenSpan | None


@dataclass(frozen=True)
class NormalizedView:
    """Matching tokens plus original correspondence, available without rematching.

    values includes preserved recovery values and complete captures added by
    binding matcher-supplied spans. Normalization never preassigns slots.
    """

    diagnostic: RecoveredDiagnostic
    normalizer_revision: str
    tokens: tuple[MatchingToken, ...]
    values: tuple[NormalizedValue, ...] = ()

    def __post_init__(self) -> None:
        for value in self.values:
            if value.token_span is not None and value.token_span.end > len(self.tokens):
                raise ValueError("value lies outside normalized tokens")


@dataclass(frozen=True)
class NativeRegion:
    text: str
    pieces: tuple[tuple[str, str], ...]
    span: ByteSpan

    def __post_init__(self):
        if ''.join(value for _, value in self.pieces) != self.text:
            raise ValueError('parser pieces do not reproduce the native region')
        if len(self.text.encode('utf-8', 'surrogateescape')) != self.span.end - self.span.start:
            raise ValueError('native region byte length disagrees with its span')


@dataclass(frozen=True)
class NativeContinuation:
    body: NativeRegion
    prefix_span: ByteSpan
    label_span: ByteSpan
    value_span: ByteSpan
    emission_ordinal: int
    source_tag: str


@dataclass(frozen=True)
class NativeDiagnostic:
    original: OriginalAccess
    source_family: str
    source_tag: str
    emission_ordinal: int
    message_ordinal: int
    emission_span: ByteSpan
    body: NativeRegion
    context_kind: str
    contexts: tuple[tuple[str, NativeRegion], ...] = ()
    continuations: tuple[NativeContinuation, ...] = ()
    emission_ordinals: tuple[int, ...] = ()
    recovery_limitation: str | None = None


@dataclass(frozen=True)
class Capture:
    name: str
    type: str
    value: str | None
    span: ByteSpan | None  # relative to the matched region, before binding


@dataclass(frozen=True)
class NativeBinding:
    template_id: str
    region: str  # message, prefix or suffix
    name: str
    type: str
    value: str | None
    span: ByteSpan | None  # absolute source bytes; absence has no range


@dataclass(frozen=True)
class RegionMatch:
    template_id: str
    region: str
    capture_count: int
    witnesses: tuple[tuple[NativeBinding, ...], ...]

    @property
    def bindings(self) -> tuple[NativeBinding, ...]:
        return self.witnesses[0] if self.capture_count == 1 else ()


@dataclass(frozen=True)
class CandidateMatch:
    template_id: str
    status: str
    message: RegionMatch
    contexts: tuple[tuple[str, tuple[RegionMatch, ...]], ...]
    components: tuple[RegionMatch, ...] = ()

    @property
    def capture_count(self) -> int:
        count = self.message.capture_count
        for _, alternatives in self.contexts:
            count *= sum(match.capture_count for match in alternatives)
        for component in self.components:
            count *= component.capture_count
        return count

    @property
    def bindings(self) -> tuple[NativeBinding, ...]:
        if self.capture_count != 1:
            return ()
        return self.message.bindings + tuple(
            binding for _, alternatives in self.contexts for binding in alternatives[0].bindings) + tuple(
            binding for component in self.components for binding in component.bindings)


@dataclass(frozen=True)
class NativeClassification:
    diagnostic: NativeDiagnostic
    model_revision: str
    classifier_revision: str
    outcome: Literal['full', 'provisional', 'unknown']
    candidates: tuple[CandidateMatch, ...] = ()
    provisional_reasons: tuple[str, ...] = ()
    unresolved_reason: str | None = None
    error_type: str = 'unknown'
    selected: CandidateMatch | None = None
    selection: dict | None = None

    @property
    def template_id(self) -> str | None:
        return self.selected.template_id if self.selected is not None else None

    @property
    def bindings(self) -> tuple[NativeBinding, ...]:
        return self.selected.bindings if self.selected is not None else ()


@dataclass(frozen=True)
class UnresolvedEmission:
    original: OriginalAccess
    emission_ordinal: int
    source_family: str | None
    span: ByteSpan
    reason: str
