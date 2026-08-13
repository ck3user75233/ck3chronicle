"""Acceptance tests for the exact reviewed empirical model promoted from WIP."""

from __future__ import annotations

from pathlib import Path

from ck3chronicle.classification.inference import Classifier
from ck3chronicle.classification.model import load_model


MODEL_SHA256 = "3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3"
MODEL_PATH = (
    Path(__file__).parents[1]
    / "models"
    / "93196794a7e0115d"
    / "empirical_template_model.json"
)


def _classifier() -> Classifier:
    return Classifier(load_model(MODEL_PATH, expected_sha256=MODEL_SHA256))


def test_rmodel_001_exact_reviewed_artifact_loads() -> None:
    model = load_model(MODEL_PATH, expected_sha256=MODEL_SHA256)

    assert model.revision_id == "93196794a7e0115d"
    assert model.threshold == 0.72
    assert len(model.clusters) == 822


def test_rmodel_002_two_key_scope_contract_is_present_and_assignable() -> None:
    result = _classifier().classify(
        "jomini_script_system.cpp",
        "Script system error! Error: scope:actor.target trigger [ Failed context switch ]",
    )

    assert result.assignment_level == "full"
    assert result.contract_id == "1ca3d0b7aefad729"
    assert result.l1_template == (
        "Script system error ! Error : scope : <KEY> . <KEY> trigger"
    )


def test_rmodel_003_duplicate_localization_key_and_paths_are_parameters() -> None:
    classifier = _classifier()
    first = classifier.classify(
        "pdx_localize.cpp",
        "Duplicate localization key. Key 'Carthage' is defined in both "
        "'localization/english/a.yml' and 'mod/loc/b.yml'.",
    )
    second = classifier.classify(
        "pdx_localize.cpp",
        "Duplicate localization key. Key 'Alexandria' is defined in both "
        "'localization/french/c.yml' and 'common/loc/d.yml'.",
    )

    assert first.assignment_level == second.assignment_level == "full"
    assert first.contract_id == second.contract_id == "514c7f0349cf61eb"


def test_rmodel_004_unseen_source_cannot_borrow_a_known_phrase() -> None:
    result = _classifier().classify(
        "invented_source.cpp",
        "Script system error! Error: scope:actor.target trigger [ Failed context switch ]",
    )

    assert result.assignment_level == "unknown"
    assert result.contract_id is None
