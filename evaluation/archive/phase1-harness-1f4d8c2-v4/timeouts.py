"""Frozen infrastructure safety ceilings; these are not scoring thresholds."""
from __future__ import annotations

from typing import Any


TIMEOUT_POLICY_SCHEMA = "ck3chronicle.phase1-timeout-policy"
PRODUCT_SUBPROCESS_DEFAULT_SECONDS = 300
NON_PERFORMANCE_CASE_SECONDS = 3600
SCRATCH_CASE_LIMIT_BYTES = 2 * 1024 * 1024 * 1024
PERFORMANCE_ACTION_SECONDS = {
    "perf_lexical": 30,
    "perf_parse": 90,
    "perf_runtime": 30,
    "perf_report_function": 30,
    "perf_report_report_text": 30,
    "perf_report_report_json": 30,
    "perf_report_latest_text": 30,
    "perf_report_latest_json": 30,
    "perf_report_errors_text": 30,
    "perf_report_errors_json": 30,
    "perf_pipeline": 600,
}
PERFORMANCE_CASE_SECONDS = {
    "perf_lexical": 300,
    "perf_parse": 900,
    "perf_runtime": 600,
    "perf_report_function": 600,
    "perf_report_report_text": 600,
    "perf_report_report_json": 600,
    "perf_report_latest_text": 600,
    "perf_report_latest_json": 600,
    "perf_report_errors_text": 600,
    "perf_report_errors_json": 600,
    "perf_pipeline": 4200,
}
PERFORMANCE_BUDGET_BASIS = {
    "perf_lexical": {"median_wall_seconds": 2, "fourth_wall_seconds": 3},
    "perf_parse": {"median_wall_seconds": 15, "fourth_wall_seconds": 20},
    "perf_runtime": {"median_wall_seconds": 1.5, "fourth_wall_seconds": 2},
    "perf_report_function": {"median_wall_seconds": 1.5, "fourth_wall_seconds": 2},
    "perf_report_report_text": {"median_wall_seconds": 1.5, "fourth_wall_seconds": 2},
    "perf_report_report_json": {"median_wall_seconds": 1.5, "fourth_wall_seconds": 2},
    "perf_report_latest_text": {"median_wall_seconds": 1.5, "fourth_wall_seconds": 2},
    "perf_report_latest_json": {"median_wall_seconds": 1.5, "fourth_wall_seconds": 2},
    "perf_report_errors_text": {"median_wall_seconds": 1.5, "fourth_wall_seconds": 2},
    "perf_report_errors_json": {"median_wall_seconds": 1.5, "fourth_wall_seconds": 2},
    "perf_pipeline": {"median_wall_seconds": 180, "fourth_wall_seconds": 240},
}
PERFORMANCE_CHILD_ACTION = {
    "perf_lexical": "lexical",
    "perf_parse": "parse",
    "perf_runtime": "runtime",
    "perf_report_function": "report_function",
    "perf_report_report_text": "report_cli",
    "perf_report_report_json": "report_cli",
    "perf_report_latest_text": "report_cli",
    "perf_report_latest_json": "report_cli",
    "perf_report_errors_text": "report_cli",
    "perf_report_errors_json": "report_cli",
    "perf_pipeline": "pipeline",
}


def _declared_action_boundary(action: str, overall_seconds: int, recipe: str, action_seconds: int | None) -> dict[str, Any]:
    boundary: dict[str, Any] = {
        "action": action,
        "boundary_kind": "outer_case_step",
        "ceiling_seconds": overall_seconds,
        "enforcement": "remaining_outer_case_process_tree_deadline",
    }
    invocation_count = 1 if action.startswith("run_one_") else 5 if action.startswith("run_five_") else None
    if action_seconds is not None and invocation_count is not None:
        boundary["boundary_kind"] = "measurement_invocation_group_with_outer_case_deadline"
        boundary["measurement_invocations"] = {
            "count": invocation_count,
            "child_action": PERFORMANCE_CHILD_ACTION[recipe],
            "per_invocation_ceiling_seconds": action_seconds,
            "enforcement": "dedicated_performance_child_process_tree_deadline",
        }
    return boundary


def timeout_policy(recipe: str, actions: list[str], *, private_placeholder: bool = False) -> dict[str, Any]:
    if private_placeholder:
        return {
            "schema": TIMEOUT_POLICY_SCHEMA,
            "schema_version": 1,
            "unassigned_unexecuted": True,
            "scoring_threshold": False,
        }
    action_seconds = PERFORMANCE_ACTION_SECONDS.get(recipe)
    overall_seconds = PERFORMANCE_CASE_SECONDS.get(recipe, NON_PERFORMANCE_CASE_SECONDS)
    policy: dict[str, Any] = {
        "schema": TIMEOUT_POLICY_SCHEMA,
        "schema_version": 1,
        "classification": "infrastructure_safety_ceiling_not_scoring_threshold",
        "scoring_threshold": False,
        "retry_on_timeout": False,
        "overall_case_seconds": overall_seconds,
        "product_subprocess_default_seconds": PRODUCT_SUBPROCESS_DEFAULT_SECONDS,
        "scratch_case_limit_bytes": SCRATCH_CASE_LIMIT_BYTES,
        "declared_actions": [_declared_action_boundary(action, overall_seconds, recipe, action_seconds) for action in actions],
    }
    if action_seconds is not None:
        policy["performance_action_seconds"] = action_seconds
        policy["performance_repetitions_maximum"] = 6
        policy["performance_budget_basis"] = PERFORMANCE_BUDGET_BASIS[recipe]
        policy["action_ceiling_multiple_of_fourth_wall"] = (
            action_seconds / PERFORMANCE_BUDGET_BASIS[recipe]["fourth_wall_seconds"]
        )
        policy["setup_and_observation_allowance_seconds"] = overall_seconds - (6 * action_seconds)
        policy["derivation"] = (
            "action ceiling is a conservative multiple of the frozen fourth-wall budget; "
            "overall ceiling adds six action ceilings plus outer-watchdog-bounded setup/observation allowance"
        )
    else:
        policy["derivation"] = (
            "one-hour outer ceiling bounds legacy multi-action cases; each product subprocess "
            "has a separately enforced five-minute ceiling"
        )
    return policy


def timeout_table() -> dict[str, Any]:
    performance_derivation = {
        recipe: {
            "action_ceiling_seconds": PERFORMANCE_ACTION_SECONDS[recipe],
            "fourth_wall_budget_seconds": PERFORMANCE_BUDGET_BASIS[recipe]["fourth_wall_seconds"],
            "action_ceiling_multiple_of_fourth_wall": (
                PERFORMANCE_ACTION_SECONDS[recipe] / PERFORMANCE_BUDGET_BASIS[recipe]["fourth_wall_seconds"]
            ),
            "maximum_action_invocations": 6,
            "overall_case_seconds": PERFORMANCE_CASE_SECONDS[recipe],
            "setup_and_observation_allowance_seconds": (
                PERFORMANCE_CASE_SECONDS[recipe] - (6 * PERFORMANCE_ACTION_SECONDS[recipe])
            ),
        }
        for recipe in PERFORMANCE_ACTION_SECONDS
    }
    return {
        "schema": "ck3chronicle.phase1-timeout-table",
        "schema_version": 1,
        "classification": "infrastructure_safety_ceilings_not_scoring_thresholds",
        "product_subprocess_default_seconds": PRODUCT_SUBPROCESS_DEFAULT_SECONDS,
        "non_performance_case_seconds": NON_PERFORMANCE_CASE_SECONDS,
        "scratch_case_limit_bytes": SCRATCH_CASE_LIMIT_BYTES,
        "performance_action_seconds": PERFORMANCE_ACTION_SECONDS,
        "performance_case_seconds": PERFORMANCE_CASE_SECONDS,
        "performance_budget_basis": PERFORMANCE_BUDGET_BASIS,
        "performance_derivation": performance_derivation,
        "retry_on_timeout": False,
    }
