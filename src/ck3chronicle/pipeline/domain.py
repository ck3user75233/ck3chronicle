"""Native byte correspondence and selected complete assignments.

Shared types for selected classification, native review and Run storage.
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


class OriginalAccess(Protocol):
    """Read-only access supplied by the input owner, valid during processing.

    Implementations return exactly the requested original bytes or raise;
    they never re-encode decoded text or silently return a short read.
    """

    def read_bytes(self, span: ByteSpan) -> bytes: ...


class ResultIntegrityError(ValueError):
    """Selected assignment, original binding or contract data disagree."""


@dataclass(frozen=True)
class NativeDiagnostic:
    original: OriginalAccess
    unit: dict

    @property
    def source_family(self):
        return self.unit['source_family']

    @property
    def source_tag(self):
        return self.unit['source_tag']

    @property
    def provenance(self):
        return self.unit['provenance']


@dataclass(frozen=True)
class NativeBinding:
    slot_id: str
    type: str
    value: str | None
    present: bool
    span: ByteSpan | None  # absolute original bytes; absence has no range


@dataclass(frozen=True)
class SelectedRegion:
    name: str
    layout: dict
    bindings: tuple[NativeBinding, ...]
    span: ByteSpan
    component_index: int | None = None


@dataclass(frozen=True)
class SelectedAssignment:
    template_id: str
    template_status: str
    match_status: Literal['template', 'provisional']
    regions: tuple[SelectedRegion, ...]
    selection: dict


@dataclass(frozen=True)
class NativeClassification:
    diagnostic: NativeDiagnostic
    model_revision: str
    classifier_revision: str
    selected: SelectedAssignment | None
    review_reason: str | None = None

    @property
    def outcome(self):
        return self.selected.match_status if self.selected else 'no_match'

    @property
    def disposition(self):
        return 'record' if self.selected else 'native_review'


@dataclass(frozen=True)
class NativeReview:
    """Unresolved recovery or explicit native-input failure, with intact evidence."""
    original: OriginalAccess
    unit: dict
    reason: str
    error: Exception | None = None
    disposition: str = 'native_review'

    @property
    def source_family(self):
        if 'source_family' in self.unit:
            return self.unit['source_family']
        return self.unit['recovery'].parent.source_family

    @property
    def source_tag(self):
        return self.unit['provenance']['source_tag']

    @property
    def provenance(self):
        return self.unit['provenance']


@dataclass(frozen=True)
class DiagnosticRecord:
    """One Run-scoped exact identity; provenance belongs to its first occurrence."""
    definition: dict
    values: dict
    match_status: Literal['template', 'provisional']
    occurrence_count: int
    error_type: Literal['unknown']
    provenance: dict


@dataclass(frozen=True)
class RunAccounting:
    """Reconciled storage counters; see ReviewWriter.accounting and Task 06 handoff."""
    counts: dict[str, int]


@dataclass(frozen=True)
class ReviewMetadata:
    log_reference: str
    manifest_reference: str
    log_sha256: str
    log_bytes: int
    emission_count: int
    unit_count: int
    availability: Literal['available']
    routing_counts: dict[str, int]
    source_counts: dict[str, int]


@dataclass(frozen=True)
class RunResult:
    """Returned only after SQLite commit and both review files are published."""
    run_id: str
    database_id: str
    log_sha256: str
    accounting: RunAccounting
    review: ReviewMetadata
