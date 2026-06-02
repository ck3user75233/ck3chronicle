from __future__ import annotations

import difflib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

from .models import DiffSummary, SourceInstance, SourceResolution, SourceType
from .paths import safe_read_lines


class SourceProvider(Protocol):
    """Protocol used by OverrideResolver."""

    def iter_instances(self, rel_path: str) -> list[SourceInstance]:
        ...


@dataclass(slots=True)
class OverrideResolver:
    source_provider: SourceProvider
    our_submod_name: str = "Gambo+EC724 Submod"
    recent_days: int = 10

    def resolve(self, rel_path: str) -> SourceResolution:
        instances = sorted(self.source_provider.iter_instances(rel_path), key=lambda i: i.load_order)
        resolution = SourceResolution(
            file_path=rel_path,
            instances=instances,
            our_submod_name=self.our_submod_name,
            recently_modified_cutoff_days=self.recent_days,
        )

        if not instances:
            resolution.confidence = "Low"
            resolution.reason = "No matching file instances found in configured sources."
            return resolution

        winner = instances[-1]
        our_inst = next((i for i in instances if i.source_name == self.our_submod_name), None)

        resolution.winning_instance = winner
        resolution.our_submod_instance = our_inst
        resolution.our_submod_override = our_inst is not None

        if our_inst:
            original = instances[0]
            resolution.diff_vs_original = diff_summary(original, our_inst)
            our_idx = instances.index(our_inst)
            if our_idx > 0:
                predecessor = instances[our_idx - 1]
                if predecessor.path != our_inst.path:
                    resolution.diff_vs_predecessor = diff_summary(predecessor, our_inst)

        resolution.confidence = "High"
        if our_inst and our_inst == winner:
            resolution.reason = "Our submod has the winning override for this file."
        elif our_inst and our_inst != winner:
            resolution.reason = f"Our submod has an override, but {winner.source_name} wins later in load order."
        elif winner.source_type == "base_game":
            resolution.reason = "Base game file is winning; root cause may still be modded caller/data."
            resolution.confidence = "Medium"
        else:
            resolution.reason = f"{winner.source_name} is winning and our submod does not override this file."
            resolution.confidence = "Medium"

        return resolution


def diff_summary(a: SourceInstance, b: SourceInstance) -> DiffSummary:
    a_lines = safe_read_lines(a.path)
    b_lines = safe_read_lines(b.path)
    diff = list(difflib.unified_diff(a_lines, b_lines, lineterm=""))
    added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    return DiffSummary(
        added=added,
        removed=removed,
        stale_warning=removed > 50 and removed > added * 1.5,
        compared_to=a.source_name,
    )


class FilesystemSourceProvider:
    """Simple source provider for tests or non-SDK usage.

    Sources should be provided in load-order ascending.
    """

    def __init__(self, sources: list[tuple[str, int, Path, SourceType]]):
        self.sources = sources

    def iter_instances(self, rel_path: str) -> list[SourceInstance]:
        found: list[SourceInstance] = []
        for source_name, load_order, root, source_type in self.sources:
            path = root / rel_path
            if path.exists():
                found.append(
                    SourceInstance(
                        source_name=source_name,
                        load_order=load_order,
                        path=path,
                        modified_at=datetime.fromtimestamp(path.stat().st_mtime),
                        source_type=source_type,
                    )
                )
        return sorted(found, key=lambda i: i.load_order)
