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


def test_rmodel_005_repeated_persistent_clauses_are_occurrences_not_templates() -> None:
    """Human oracle: repetition count changes cardinality, never base identity."""
    raw_block = (
        "[12:00:00][E][pdx_persistent_reader.cpp:7]: Error: \""
        "Unknown trigger: first_key, near line: 10 "
        "Unknown trigger: second_key, near line: 20 "
        "Unknown trigger: third_key, near line: 30"
        "\" in file: events/example.txt line: 40\n"
    )

    results = _classifier().classify_block("pdx_persistent_reader.cpp", raw_block)

    assert len(results) == 3
    assert {result.assignment_level for result in results} == {"full"}
    assert {result.contract_id for result in results} == {"21b477c6e94b1681"}
    assert {result.semantic_text for result in results} == {"Unknown trigger: <KEY>"}


def test_rmodel_006_single_persistent_clause_uses_the_same_base_contract() -> None:
    """Human oracle: cardinality one and cardinality three share identity."""
    raw_block = (
        "[12:00:00][E][pdx_persistent_reader.cpp:7]: Error: \""
        "Unknown trigger: only_key, near line: 10"
        "\" in file: events/example.txt line: 40\n"
    )

    results = _classifier().classify_block("pdx_persistent_reader.cpp", raw_block)

    assert len(results) == 1
    assert results[0].assignment_level == "full"
    assert results[0].contract_id == "21b477c6e94b1681"
    assert results[0].semantic_text == "Unknown trigger: <KEY>"
