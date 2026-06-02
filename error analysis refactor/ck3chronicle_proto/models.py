from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

Severity = Literal["Fatal", "High", "Medium", "Low", "Noise", "Unknown"]
Confidence = Literal["High", "Medium", "Low"]
SourceType = Literal["base_game", "workshop_mod", "local_mod", "unknown"]


@dataclass(slots=True)
class ScriptLocation:
    """A CK3 script location frame extracted from a log block."""

    file: str | None = None
    line: int | None = None
    symbol: str | None = None
    raw: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class CanonicalIssue:
    """Canonical issue record emitted by log parsers/extractors.

    Reports and analytics should consume this object, not raw log text.
    """

    schema_version: str
    source_log: str
    raw_block_hash: str
    normalized_signature: str
    category: str
    severity: Severity
    confidence: Confidence
    message: str
    raw_sample: str
    first_line_number: int | None = None
    last_line_number: int | None = None
    primary_file: str | None = None
    primary_line: int | None = None
    primary_symbol: str | None = None
    call_stack: list[ScriptLocation] = field(default_factory=list)
    extracted_file_paths: list[str] = field(default_factory=list)
    occurrence_count: int = 1

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["call_stack"] = [loc.to_dict() if hasattr(loc, "to_dict") else loc for loc in self.call_stack]
        return data


@dataclass(slots=True)
class SourceInstance:
    """One discovered instance of a game-relative file in base game or a mod."""

    source_name: str
    load_order: int
    path: Path
    modified_at: datetime
    source_type: SourceType = "unknown"

    @property
    def exists(self) -> bool:
        return self.path.exists()

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_name": self.source_name,
            "load_order": self.load_order,
            "path": str(self.path),
            "modified_at": self.modified_at.isoformat(timespec="minutes"),
            "source_type": self.source_type,
        }


@dataclass(slots=True)
class DiffSummary:
    added: int = 0
    removed: int = 0
    stale_warning: bool = False
    compared_to: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SourceResolution:
    """Override/source enrichment for a game-relative file path."""

    file_path: str
    instances: list[SourceInstance] = field(default_factory=list)
    winning_instance: SourceInstance | None = None
    our_submod_name: str | None = None
    our_submod_instance: SourceInstance | None = None
    our_submod_override: bool = False
    diff_vs_original: DiffSummary | None = None
    diff_vs_predecessor: DiffSummary | None = None
    recently_modified_cutoff_days: int = 10
    confidence: Confidence = "Low"
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_path": self.file_path,
            "instances": [i.to_dict() for i in self.instances],
            "winning_instance": self.winning_instance.to_dict() if self.winning_instance else None,
            "our_submod_name": self.our_submod_name,
            "our_submod_instance": self.our_submod_instance.to_dict() if self.our_submod_instance else None,
            "our_submod_override": self.our_submod_override,
            "diff_vs_original": self.diff_vs_original.to_dict() if self.diff_vs_original else None,
            "diff_vs_predecessor": self.diff_vs_predecessor.to_dict() if self.diff_vs_predecessor else None,
            "recently_modified_cutoff_days": self.recently_modified_cutoff_days,
            "confidence": self.confidence,
            "reason": self.reason,
        }


@dataclass(slots=True)
class FixabilityAssessment:
    file_path: str
    score: int
    recommendation: str
    confidence: Confidence
    reason: str
    highest_severity: Severity = "Unknown"
    issue_count: int = 0
    source_resolution: SourceResolution | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_path": self.file_path,
            "score": self.score,
            "recommendation": self.recommendation,
            "confidence": self.confidence,
            "reason": self.reason,
            "highest_severity": self.highest_severity,
            "issue_count": self.issue_count,
            "source_resolution": self.source_resolution.to_dict() if self.source_resolution else None,
        }
