from __future__ import annotations

from datetime import datetime
from typing import Iterable, Callable

from .fixability import assess_fixability
from .issue_aggregator import top_files
from .models import CanonicalIssue, FixabilityAssessment, SourceResolution


def build_error_file_analysis_report(
    issues: Iterable[CanonicalIssue],
    *,
    playset_name: str = "unknown",
    log_source: str = "unknown",
    source_resolutions: dict[str, SourceResolution] | None = None,
    top_n: int = 25,
) -> str:
    issues = list(issues)
    source_resolutions = source_resolutions or {}

    buckets = top_files(issues, limit=top_n)
    assessments: list[FixabilityAssessment] = []
    for bucket in buckets:
        assessments.append(
            assess_fixability(
                bucket,
                source_resolutions.get(bucket.file_path),
                known_noise=all(i.severity in ("Low", "Noise") for i in bucket.issues),
            )
        )

    by_count = sorted(zip(buckets, assessments), key=lambda pair: pair[0].count, reverse=True)

    out: list[str] = []
    W = out.append
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    W("=" * 78)
    W("ERROR FILE DEEP ANALYSIS")
    W(f"Generated  : {now}")
    W(f"Playset    : {playset_name}")
    W(f"Log source : {log_source}")
    W(f"Top files  : {top_n}  |  Total canonical issues: {len(issues):,}")
    W("=" * 78)
    W("")
    W("RANK  ERRORS  SCORE  FILE")
    W("─" * 78)
    for rank, (bucket, assessment) in enumerate(by_count, 1):
        W(f"  {rank:>2}  {bucket.count:>5}  {assessment.score:>5}  {bucket.file_path}")
    W("")

    for rank, (bucket, assessment) in enumerate(by_count, 1):
        W("=" * 78)
        W(f"#{rank}  [{bucket.count} errors | score {assessment.score}]  {bucket.file_path}")
        W("=" * 78)
        W("")

        resolution = assessment.source_resolution
        if resolution and resolution.instances:
            write_source_section(W, resolution)
        else:
            W("  SOURCE / OVERRIDE CONTEXT:")
            W("    No matching file instances found or source resolver not configured.")
            W("")

        W("  RECOMMENDATION:")
        W(f"    {assessment.recommendation}")
        W(f"    Confidence: {assessment.confidence}")
        W(f"    Reason: {assessment.reason}")
        W("")

        W("  SAMPLE ERRORS (up to 5 unique messages):")
        for sample in bucket.sample_messages(limit=5):
            W(f"    - {sample}")
        W("")

    W("=" * 78)
    W(f"END OF ANALYSIS  |  {len(buckets)} files  |  {len(issues):,} total canonical issues")
    W("=" * 78)
    return "\n".join(out)


def write_source_section(W: Callable[[str], None], resolution: SourceResolution) -> None:
    W(f"  OVERRIDE CHAIN  ({len(resolution.instances)} instance(s), load order ascending):")
    winner = resolution.winning_instance
    for inst in resolution.instances:
        flags: list[str] = []
        if winner and inst.source_name == winner.source_name and inst.load_order == winner.load_order:
            flags.append("WINNER")
        if resolution.our_submod_name and inst.source_name == resolution.our_submod_name:
            flags.append("OUR SUBMOD")
        flag_str = "  <<< " + ", ".join(flags) if flags else ""
        W(f"    [{inst.load_order:>3}] {inst.source_name}{flag_str}")
        W(f"           {inst.path}")
        W(f"           Modified: {inst.modified_at.strftime('%Y-%m-%d %H:%M')}")
    W("")

    if winner:
        W(f"  WINNING MOD  : {winner.source_name}  (load order {winner.load_order})")
        W(f"  CURRENT WINNING FILE: {winner.path}")
        W("")

    if resolution.our_submod_override:
        W("  OUR SUBMOD OVERRIDE: YES")
        if resolution.diff_vs_original:
            diff = resolution.diff_vs_original
            W(f"  DIFF vs ORIGINAL [{diff.compared_to}]: +{diff.added} added / -{diff.removed} removed")
            if diff.stale_warning:
                W("  *** STALE PATCH WARNING: our override removes substantially more than it adds.")
        if resolution.diff_vs_predecessor:
            diff = resolution.diff_vs_predecessor
            W(f"  DIFF vs PREDECESSOR [{diff.compared_to}]: +{diff.added} added / -{diff.removed} removed")
            if diff.stale_warning:
                W("  *** PREDECESSOR STALE WARNING: predecessor may have new content we overwrite.")
    else:
        W("  OUR SUBMOD OVERRIDE: NO")
        W("  ACTION: consider creating an override in our submod if fix is needed.")
    W("")
