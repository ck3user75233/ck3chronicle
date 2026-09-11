"""C1 canonical parse records shared by the parser and persistence layer."""
from __future__ import annotations

from dataclasses import dataclass

from .issue import NormalizedIssue


@dataclass(frozen=True)
class SourceBlockRecord:
    source_block_id: str
    log_relpath: str
    start_line: int
    end_line: int
    timestamp: str
    level: str
    source_tag: str
    source_family: str
    raw_block_sha256: str
    raw_byte_length: int
    raw_block: str
    issue_count: int


@dataclass(frozen=True)
class OccurrenceRecord:
    source_block_id: str
    issue_ordinal: int
    issue: NormalizedIssue


@dataclass(frozen=True)
class ClusterRecord:
    issue: NormalizedIssue
    occurrence_count: int


@dataclass(frozen=True)
class ParseCounters:
    source_blocks: int
    preamble_blocks: int
    issue_occurrences: int
    issue_clusters: int
    unclassified_occurrences: int
    multi_issue_blocks: int
    silently_dropped_blocks: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "source_blocks": self.source_blocks,
            "preamble_blocks": self.preamble_blocks,
            "issue_occurrences": self.issue_occurrences,
            "issue_clusters": self.issue_clusters,
            "unclassified_occurrences": self.unclassified_occurrences,
            "multi_issue_blocks": self.multi_issue_blocks,
            "silently_dropped_blocks": self.silently_dropped_blocks,
        }


@dataclass(frozen=True)
class ParseResult:
    session_id: int
    parser_contract_version: str
    counters: ParseCounters
    mutated: bool
