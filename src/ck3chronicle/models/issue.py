"""Domain models for ck3chronicle parsed issues.

Phase 1 taxonomy is (category, error_type, tags). All categories are
snake_case strings. KNOWN_CATEGORIES is the curated registry.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


KNOWN_CATEGORIES: frozenset[str] = frozenset({
    "script_system",
    "localization",
    "descriptor",
    "persistent_reader",
    "asset_graphics",
    "gui_interface",
    "event_system",
    "database_reference",
    "history_setup",
    "culture_faith",
    "script_hygiene",
    "unclassified",
})


@dataclass
class IssueDraft:
    """Extractor output, pre-normalization.

    Field types intentionally match the Phase 1 acceptance tests:
    - tags is list[str] (constructed empty as [])
    - extra_json is dict (constructed empty as {})
    - confidence is float (tests pass 1.0)
    """

    category: str
    error_type: str
    tags: list[str]
    engine_source: str
    sample_message: str
    primary_file: str | None
    primary_line: int | None
    referenced_symbols: list[str]
    referenced_objects: list[str]
    extra_json: dict[str, Any]
    severity: str
    confidence: float
    raw_block: str
    log_relpath: str
    line_number: int


@dataclass
class NormalizedIssue:
    """Result of normalize(): masked message + deterministic signature.

    Mirrors the IssueDraft fields but adds signature and message_template,
    and exposes the (possibly enriched) referenced_symbols list.
    """

    signature: str
    message_template: str
    category: str
    error_type: str
    tags: list[str]
    engine_source: str
    sample_message: str
    primary_file: str | None
    primary_line: int | None
    referenced_symbols: list[str]
    referenced_objects: list[str]
    extra_json: dict[str, Any]
    severity: str
    confidence: float
    raw_block: str
    log_relpath: str
    line_number: int


@dataclass
class Issue:
    """Clustered issue row (one per (session_id, signature))."""

    issue_id: int | None
    session_id: int
    signature: str
    category: str
    error_type: str
    tags: list[str]
    engine_source: str
    severity: str
    confidence: float
    message_template: str
    sample_message: str
    primary_file: str | None
    primary_line: int | None
    referenced_symbols: list[str]
    referenced_objects: list[str]
    extra_json: dict[str, Any]
    occurrence_count: int = 1


@dataclass
class IssueOccurrence:
    """One row per raw timestamped block in a parsed session."""

    issue_occurrence_id: int | None
    session_id: int
    signature: str
    log_relpath: str
    line_number: int
    raw_block: str
    referenced_symbols: list[str]
    extra_json: dict[str, Any]
