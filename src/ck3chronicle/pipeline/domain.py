"""Empirical processing interfaces, independent of diagnostic semantics.

Byte offsets are absolute in one protected original log; token offsets are
local to a normalized view. Both use half-open intervals. Decoded text is for
matching only: native review must read original bytes through OriginalAccess.
These types perform no lexing, extraction, normalization, or matching.
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

    origins are ordered, possibly discontiguous original spans. An absent
    optional value uses empty text and an explicit zero-width origin. No
    semantic role or learned slot definition is inferred from this value.
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
    """One normalized token and its original byte origins.

    Literal and masked tokens both carry correspondence. A synthetic token
    uses a zero-width origin at its insertion boundary. A token may map to
    multiple spans; byte lengths need not equal decoded or normalized lengths.
    """

    text: str
    origins: tuple[EvidenceSpan, ...]

    def __post_init__(self) -> None:
        if not self.origins:
            raise ValueError("a matching token requires original correspondence")


@dataclass(frozen=True)
class NormalizedValue:
    """Value captured before masking, and its resulting token interval.

    None means the value was removed from matching (e.g. a locator tail),
    rather than lost. An empty TokenSpan represents an optional empty slot.
    """

    value: OccurrenceValue
    token_span: TokenSpan | None


@dataclass(frozen=True)
class NormalizedView:
    """Matching tokens plus original correspondence, available without rematching.

    values includes preserved recovery values and values extracted during
    normalization. The normalizer owns this correspondence, not a later
    classifier searching the original message again.
    """

    diagnostic: RecoveredDiagnostic
    normalizer_revision: str
    tokens: tuple[MatchingToken, ...]
    values: tuple[NormalizedValue, ...] = ()

    def __post_init__(self) -> None:
        for value in self.values:
            if value.token_span is not None and value.token_span.end > len(self.tokens):
                raise ValueError("value lies outside normalized tokens")


StructuralPart = Literal["whole", "l1", "l2"]
AssignmentLevel = Literal["full", "l1_l2", "l1", "unknown"]


@dataclass(frozen=True)
class StructuralIdentity:
    """A cluster or one of its optional layers in a selected model revision.

    The artifact supplies no independent layer IDs. A layer reference names
    the cluster supplying its tokens; it does not invent a layer taxonomy or
    require both assigned layers to come from the same cluster.
    """

    model_revision: str
    cluster_id: str
    part: StructuralPart = "whole"


@dataclass(frozen=True)
class LearnedVariable:
    """A variable position in the referenced whole/layer template token tuple.

    token_index is zero-based in that template, not in the occurrence.
    placeholder is the learned token (e.g. <KEY> or <ALT:a|b>), never an
    observed example value. Validation rules remain model/classifier-owned.
    """

    structure: StructuralIdentity
    token_index: int
    placeholder: str

    def __post_init__(self) -> None:
        if self.token_index < 0:
            raise ValueError("invalid learned variable position")


@dataclass(frozen=True)
class OccurrenceBinding:
    """A learned variable bound to this occurrence's preserved original value."""

    variable: LearnedVariable
    occurrence: NormalizedValue


@dataclass(frozen=True)
class StructuralFailure:
    """Structural non-match/failure information, separate from assignment.

    code/detail are supplied by the matcher, not diagnostic issue categories.
    candidate may identify an unsuccessful candidate, never an assignment.
    """

    part: StructuralPart
    code: str
    detail: str
    candidate: StructuralIdentity | None = None


@dataclass(frozen=True)
class StructuralClassification:
    """Empirical assignment only; no diagnostic or persistence semantics.

    full requires a whole-template assignment, with optional layer facts.
    l1_l2 requires both assigned layers. l1 is an exact successful outer-layer
    assignment with unresolved L2, not a partial whole-template match.
    unknown has no assigned identity, but the view retains occurrence values.
    No layer metadata is required for a full result. The classifier owns
    evidence-based assignment; these checks enforce only result shape.
    """

    view: NormalizedView
    model_revision: str
    classifier_revision: str
    outcome: AssignmentLevel
    whole: StructuralIdentity | None = None
    l1: StructuralIdentity | None = None
    l2: StructuralIdentity | None = None
    bindings: tuple[OccurrenceBinding, ...] = ()
    failures: tuple[StructuralFailure, ...] = ()

    def __post_init__(self) -> None:
        shape = (self.whole is not None, self.l1 is not None, self.l2 is not None)
        valid = {
            "full": {(True, False, False), (True, True, True)},
            "l1_l2": {(False, True, True)},
            "l1": {(False, True, False)},
            "unknown": {(False, False, False)},
        }
        if shape not in valid.get(self.outcome, set()):
            raise ValueError("assignment identities disagree with outcome")
        for part, identity in (("whole", self.whole), ("l1", self.l1), ("l2", self.l2)):
            if identity is not None and (identity.part != part or identity.model_revision != self.model_revision):
                raise ValueError("assignment part or model revision disagrees")
        for binding in self.bindings:
            if binding.variable.structure not in (self.whole, self.l1, self.l2):
                raise ValueError("binding must refer to an assigned structure")
            if binding.occurrence not in self.view.values:
                raise ValueError("binding must use a preserved occurrence value")

    @property
    def source_family(self) -> str:
        return self.view.diagnostic.parent.source_family
