"""Fresh reboot acceptance tests for layered empirical classification."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from ck3chronicle.classification.inference import Classifier
from ck3chronicle.classification.model import ModelIntegrityError, load_model
from ck3chronicle.classification.normalize import diagnostic_lead

from classification_oracle import write_model


@pytest.fixture
def classifier(tmp_path: Path) -> Classifier:
    model_path = tmp_path / "model.json"
    write_model(model_path)
    digest = hashlib.sha256(model_path.read_bytes()).hexdigest()
    return Classifier(load_model(model_path, expected_sha256=digest))


def test_rclass_001_model_hash_is_verified_before_use(tmp_path: Path) -> None:
    """Oracle: altering one artifact byte invalidates the approved digest."""
    model_path = tmp_path / "model.json"
    write_model(model_path)
    approved = hashlib.sha256(model_path.read_bytes()).hexdigest()
    model_path.write_bytes(model_path.read_bytes() + b" ")

    with pytest.raises(ModelIntegrityError, match="SHA-256"):
        load_model(model_path, expected_sha256=approved)


def test_rclass_002_key_and_locator_values_do_not_split_localization_contract(
    classifier: Classifier,
) -> None:
    """Human oracle: Carthage and both filenames are slots, not semantics."""
    first = classifier.classify(
        "pdx_localize.cpp",
        "Localization key 'Carthage' is defined in both 'localization/english/carthage.yml' and 'localization/french/carthage.yml'",
    )
    second = classifier.classify(
        "pdx_localize.cpp",
        "Localization key 'Alexandria' is defined in both 'mod/loc/one.yml' and 'mod/loc/two.yml'",
    )

    assert diagnostic_lead(first.semantic_text) == ("localization", "key")
    assert first.assignment_level == "full", first.normalized_tokens
    assert second.assignment_level == "full"
    assert first.contract_id == second.contract_id == "fc12b3d364faee03"


def test_rclass_003_semantic_change_is_not_forced_into_localization_contract(
    classifier: Classifier,
) -> None:
    """Human oracle: a different repeatable phrase is a different contract."""
    result = classifier.classify(
        "pdx_localize.cpp",
        "Localization key 'Carthage' was removed before the database finished loading",
    )

    assert result.assignment_level == "unknown"
    assert result.contract_id is None


def test_rclass_004_scope_path_retains_two_related_key_slots(
    classifier: Classifier,
) -> None:
    """Human oracle: scope:actor.target is <KEY>.<KEY>, not one context slot."""
    result = classifier.classify(
        "jomini_script_system.cpp",
        "Script system error! Error: scope:actor.target trigger [ Entirely novel semantic cause ]",
    )

    assert result.assignment_level == "l1"
    assert result.contract_id is None
    assert result.l1_template == (
        "Script system error ! Error : scope : <KEY> . <KEY> trigger"
    )
    assert result.l2_template == "Entirely novel semantic cause"


def test_rclass_005_known_compatible_l1_and_l2_are_explicitly_composed(
    classifier: Classifier,
) -> None:
    """Human oracle: known scope L1 plus independently known reason is L1+L2."""
    result = classifier.classify(
        "jomini_script_system.cpp",
        "Script system error! Error: scope:actor.target trigger [ Wrong scope for trigger: character, expected culture ]",
    )

    assert result.assignment_level == "l1_l2"
    assert result.contract_id is not None
    assert result.l1_template.endswith("scope : <KEY> . <KEY> trigger")
    assert result.l2_template == (
        "Wrong scope for trigger : character , expected culture"
    )


def test_rclass_006_optional_historical_id_does_not_split_travel_contract(
    classifier: Classifier,
) -> None:
    """Human oracle: identity is <KEY> (<KEY> <OPTIONAL_KEY>)."""
    with_history = classifier.classify(
        "jomini_script_system.cpp",
        "Script system error! Error: cancel_travel effect [ Matilda of d_tuscany (Internal ID: 123 - Historical ID matilda_1)'s travel plan have no valid destinations ]",
    )
    without_history = classifier.classify(
        "jomini_script_system.cpp",
        "Script system error! Error: cancel_travel effect [ Matilda of d_tuscany (Internal ID: 123)'s travel plan have no valid destinations ]",
    )

    assert with_history.assignment_level == "full"
    assert without_history.assignment_level == "full"
    assert with_history.contract_id == without_history.contract_id == "63c6f785dd9cbc48"
    assert [slot["role"] for slot in with_history.structured_slots] == [
        "key",
        "key",
        "optional_key",
    ]
    assert with_history.structured_slots[-1]["present"] is True
    assert without_history.structured_slots[-1]["present"] is False


def test_rclass_007_location_chain_changes_never_change_contract(
    classifier: Classifier,
) -> None:
    """Human oracle: paths, frame labels, frame count, and lines are locators."""
    first = classifier.classify(
        "jomini_script_system.cpp",
        "Script system error! Error: check_scope trigger [ Failed context switch ] Script location: file: events/a.txt line: 10 (event_a:trigger)",
    )
    second = classifier.classify(
        "jomini_script_system.cpp",
        "Script system error! Error: check_scope trigger [ Failed context switch ] Script location: file: common/scripted_triggers/b.txt line: 999 (other) file: events/c.txt line: 2 (event_c)",
    )

    assert first.contract_id == second.contract_id == "33824ae4410d9837"
    assert first.location_evidence != second.location_evidence


def test_rclass_008_symbol_suffix_does_not_invent_a_contract(
    classifier: Classifier,
) -> None:
    """Human oracle: *_effect validates a slot only after template assignment."""
    result = classifier.classify(
        "previously_unseen_source.cpp",
        "missing thing mysterious_unregistered_effect in an unfamiliar phrase",
    )

    assert result.assignment_level == "unknown"
    assert result.contract_id is None


def test_rclass_009_token_bound_drops_l2_but_preserves_proven_l1(
    classifier: Classifier,
) -> None:
    """Human oracle: a truncated reason cannot erase or overclaim the L1 contract."""
    result = classifier.classify(
        "jomini_script_system.cpp",
        "Script system error! Error: scope:actor.target trigger [ "
        + " ".join(f"novel_{index}" for index in range(500))
        + " ]",
    )

    assert result.assignment_level == "l1"
    assert result.contract_id is None
    assert result.l1_template == (
        "Script system error ! Error : scope : <KEY> . <KEY> trigger"
    )
    assert result.l2_template is not None
    assert result.l2_template.endswith("<TRUNCATED_REASON>")
