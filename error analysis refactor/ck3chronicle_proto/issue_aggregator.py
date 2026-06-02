from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable

from .models import CanonicalIssue


@dataclass(slots=True)
class FileIssueBucket:
    file_path: str
    issues: list[CanonicalIssue] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.issues)

    @property
    def highest_severity(self) -> str:
        order = {"Fatal": 5, "High": 4, "Medium": 3, "Low": 2, "Noise": 1, "Unknown": 0}
        if not self.issues:
            return "Unknown"
        return max((i.severity for i in self.issues), key=lambda s: order.get(s, 0))

    def sample_messages(self, limit: int = 5) -> list[str]:
        seen: set[str] = set()
        samples: list[str] = []
        for issue in self.issues:
            key = issue.message[:160]
            if key not in seen:
                seen.add(key)
                samples.append(issue.message[:240])
            if len(samples) >= limit:
                break
        return samples


def group_by_primary_file(issues: Iterable[CanonicalIssue]) -> dict[str, FileIssueBucket]:
    buckets: dict[str, FileIssueBucket] = {}
    for issue in issues:
        file_path = issue.primary_file or (issue.extracted_file_paths[0] if issue.extracted_file_paths else "unknown")
        if file_path not in buckets:
            buckets[file_path] = FileIssueBucket(file_path=file_path)
        buckets[file_path].issues.append(issue)
    return buckets


def top_files(issues: Iterable[CanonicalIssue], limit: int = 25) -> list[FileIssueBucket]:
    buckets = group_by_primary_file(issues)
    return sorted(buckets.values(), key=lambda b: b.count, reverse=True)[:limit]


def signature_counts(issues: Iterable[CanonicalIssue]) -> Counter[str]:
    return Counter(issue.normalized_signature for issue in issues)


def category_counts(issues: Iterable[CanonicalIssue]) -> Counter[str]:
    return Counter(issue.category for issue in issues)
