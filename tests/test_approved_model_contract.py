"""Acceptance tests for the exact reviewed empirical model promoted from WIP."""

from __future__ import annotations

from ck3chronicle.classification.catalog import (
    APPROVED_MODEL_REVISION,
    APPROVED_MODEL_SHA256,
    approved_model_path,
)
from ck3chronicle.classification.inference import Classifier
from ck3chronicle.classification.model import load_model


MODEL_SHA256 = APPROVED_MODEL_SHA256
MODEL_PATH = approved_model_path()


def _classifier() -> Classifier:
    return Classifier(load_model(MODEL_PATH, expected_sha256=MODEL_SHA256))


def test_rmodel_001_exact_reviewed_artifact_loads() -> None:
    model = load_model(MODEL_PATH, expected_sha256=MODEL_SHA256)

    assert model.revision_id == APPROVED_MODEL_REVISION
    assert model.threshold == 0.72
    assert len(model.clusters) == 891


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


def test_rmodel_007_exact_semantic_literal_retains_reviewed_contract() -> None:
    """Authentic spelling satisfies the reviewed supported-version contract."""
    result = _classifier().classify(
        "dlc_descriptor.cpp",
        "Invalid supported_version in file: mod/ugc_2218867072.mod line: 7",
    )

    assert result.assignment_level == "full"
    assert result.contract_id == "868cec87cc2a93d0"


def test_rmodel_008_semantic_literal_case_near_miss_is_not_full_contract() -> None:
    """One changed literal byte must not inherit the authentic contract."""
    result = _classifier().classify(
        "dlc_descriptor.cpp",
        "invalid supported_version in file: mod/ugc_2218867072.mod line: 7",
    )

    assert result.assignment_level == "unknown"
    assert result.contract_id is None


def test_rmodel_009_key_and_locator_case_remain_outside_literal_identity() -> None:
    """Exact semantic matching must not constrain typed slot values."""
    result = _classifier().classify(
        "pdx_localize.cpp",
        "Duplicate localization key. Key 'CARTHAGE' is defined in both "
        "'LOCALIZATION/ENGLISH/A.YML' and 'MOD/LOC/B.YML'.",
    )

    assert result.assignment_level == "full"
    assert result.contract_id == "514c7f0349cf61eb"
