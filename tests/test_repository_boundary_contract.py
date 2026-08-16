"""Repository-routing invariants that prevent parallel ck3chronicle trees."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEGACY_LEARNER_ROOTS = (
    ".ck3raven/wip/ck3chronicle/template_learning",
    ".ck3raven\\wip\\ck3chronicle\\template_learning",
)


def test_canonical_agent_guidance_and_owned_components_exist() -> None:
    required = (
        "AGENTS.md",
        "CLAUDE.md",
        ".github/copilot-instructions.md",
        ".github/prompts/continue-ck3chronicle.prompt.md",
        "docs/CURRENT_HANDOFF.md",
        "docs/PROJECT_PLAN.md",
        "docs/PROJECT_STATUS.md",
        "docs/PHASE1_EXIT_MATRIX.md",
        "docs/CAPABILITY_INVENTORY.md",
        "docs/WORKSPACE_ROUTING.md",
        "tools/template_learning/AGENTS.md",
        "tools/template_learning/learn_error_templates.py",
        "tools/template_learning/incremental_template_registry.py",
        "tools/template_learning/build_semantic_projection_catalog.py",
        "evaluation/AGENTS.md",
    )
    missing = [path for path in required if not (REPO_ROOT / path).is_file()]
    assert missing == []


def test_root_guidance_binds_standalone_repository_and_learner_home() -> None:
    guidance = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "https://github.com/ck3user75233/ck3chronicle.git" in guidance
    assert "tools/template_learning/" in guidance
    assert "Never implement, stage, commit, or generate ck3chronicle source" in guidance
    assert "not 100% L1/L2" in guidance


def test_active_authority_does_not_depend_on_legacy_wip_learner() -> None:
    active_files = (
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / ".github" / "copilot-instructions.md",
        REPO_ROOT / ".github" / "prompts" / "continue-ck3chronicle.prompt.md",
        REPO_ROOT / "README.md",
        REPO_ROOT / "docs" / "CURRENT_HANDOFF.md",
        REPO_ROOT / "docs" / "WORKSPACE_ROUTING.md",
        REPO_ROOT / "docs" / "PROJECT_PLAN.md",
        REPO_ROOT / "docs" / "PROJECT_STATUS.md",
        REPO_ROOT / "docs" / "REPOSITORY_AND_BACKUP.md",
        REPO_ROOT / "tools" / "template_learning" / "AGENTS.md",
        REPO_ROOT / "tools" / "template_learning" / "README.md",
    )
    violations: list[str] = []
    for path in active_files:
        text = path.read_text(encoding="utf-8").lower()
        if any(legacy.lower() in text for legacy in LEGACY_LEARNER_ROOTS):
            violations.append(path.relative_to(REPO_ROOT).as_posix())
    assert violations == []


def test_only_reboot_plan_is_active_and_evaluation_uses_fresh_tasks() -> None:
    obsolete = (
        "docs/ROADMAP.md",
        "docs/RESTART_HANDOFF_2026-08-14.md",
        "docs/RESOLVER_INPUT_AUDIT.md",
        "docs/PHASE1_LEXICAL_CALIBRATION_2026-08-14.md",
    )
    assert [path for path in obsolete if (REPO_ROOT / path).exists()] == []

    plan = (REPO_ROOT / "docs" / "PROJECT_PLAN.md").read_text(encoding="utf-8")
    assert "Reboot foundation" in plan
    assert "Phase 0" not in plan
    assert "Historical product Phase 0" not in plan
    assert "Product Phase 0" not in plan
    assert "fresh user-owned evaluator task" in plan
    assert "separate blind-runner task" in plan

    matrix = (REPO_ROOT / "docs" / "PHASE1_EXIT_MATRIX.md").read_text(
        encoding="utf-8"
    )
    assert "1f4d8c2f5a6e3ec1c5dc7a5324b0bbe4c4b233ac" in matrix
    assert "Public PASS | 23" in matrix
    assert "Product FAIL | 5" in matrix
    assert "Infrastructure/unscored | 6" in matrix
