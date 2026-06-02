from __future__ import annotations

from .issue_aggregator import FileIssueBucket
from .models import FixabilityAssessment, SourceResolution

SEVERITY_WEIGHT = {
    "Fatal": 50,
    "High": 35,
    "Medium": 20,
    "Low": 8,
    "Noise": 0,
    "Unknown": 5,
}


def assess_fixability(
    bucket: FileIssueBucket,
    source_resolution: SourceResolution | None = None,
    *,
    is_new_or_regression: bool = False,
    crash_adjacent: bool = False,
    known_noise: bool = False,
) -> FixabilityAssessment:
    score = 0
    reasons: list[str] = []

    highest = bucket.highest_severity
    score += SEVERITY_WEIGHT.get(highest, 0)
    reasons.append(f"highest severity={highest}")

    count_weight = min(bucket.count, 100) // 5
    score += count_weight
    reasons.append(f"{bucket.count} issue occurrence(s)")

    if is_new_or_regression:
        score += 20
        reasons.append("new/regression")

    if crash_adjacent:
        score += 25
        reasons.append("crash-adjacent")

    if source_resolution and source_resolution.winning_instance:
        winner = source_resolution.winning_instance
        if source_resolution.our_submod_instance and source_resolution.our_submod_instance == winner:
            score += 25
            reasons.append("our submod is winning")
        elif source_resolution.our_submod_instance and source_resolution.our_submod_instance != winner:
            score += 10
            reasons.append("our submod has override but is not winning")
        elif winner.source_type != "base_game":
            score -= 8
            reasons.append("upstream mod is winning")
        elif winner.source_type == "base_game":
            score -= 4
            reasons.append("base game is winning")

        if source_resolution.diff_vs_predecessor and not source_resolution.diff_vs_predecessor.stale_warning:
            score += 5
            reasons.append("small/non-stale predecessor diff")
        if source_resolution.diff_vs_original and source_resolution.diff_vs_original.stale_warning:
            score += 15
            reasons.append("possible stale patch")

    if known_noise:
        score -= 30
        reasons.append("known noise")

    score = max(score, 0)

    recommendation, confidence = recommend(bucket, source_resolution)

    return FixabilityAssessment(
        file_path=bucket.file_path,
        score=score,
        recommendation=recommendation,
        confidence=confidence,  # type: ignore[arg-type]
        reason="; ".join(reasons),
        highest_severity=highest,  # type: ignore[arg-type]
        issue_count=bucket.count,
        source_resolution=source_resolution,
    )


def recommend(bucket: FileIssueBucket, source_resolution: SourceResolution | None) -> tuple[str, str]:
    if not source_resolution or not source_resolution.winning_instance:
        return ("Inspect the referenced file/path if available; source ownership could not be resolved.", "Low")

    winner = source_resolution.winning_instance

    if source_resolution.our_submod_instance and source_resolution.our_submod_instance == winner:
        if source_resolution.diff_vs_original and source_resolution.diff_vs_original.stale_warning:
            return (
                "Our submod is winning, but the diff suggests a possible stale override. Review against original/predecessor before editing.",
                "High",
            )
        return ("Inspect/fix directly in our submod override.", "High")

    if source_resolution.our_submod_instance and source_resolution.our_submod_instance != winner:
        return (
            f"Our override exists but {winner.source_name} wins later in load order. Inspect load order or create a later-loading patch.",
            "Medium",
        )

    if winner.source_type == "base_game":
        return (
            "Base game file is winning. Inspect caller chain and modded data before creating a submod override.",
            "Medium",
        )

    return (
        f"{winner.source_name} is winning and our submod does not override this file. Assess whether to patch in our submod or report upstream.",
        "Medium",
    )
