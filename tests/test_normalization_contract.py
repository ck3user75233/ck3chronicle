"""Human-authored contracts for CK3 key, locator, and optional-key slots."""

from __future__ import annotations

from ck3chronicle.classification.normalize import (
    extract_structured_slots,
    tokenize,
)


def test_rnorm_001_trigger_description_key_and_path_do_not_change_semantics() -> None:
    first = tokenize(
        "alpha_trigger: Scope dependent values in localization inside an any "
        "trigger; consider using a custom_tooltip; at file: common/a.txt line: 7"
    )
    second = tokenize(
        "beta_trigger: Scope dependent values in localization inside an any "
        "trigger; consider using a custom_tooltip; at file: events/b.txt line: 999"
    )

    assert first == second
    assert first[:2] == ("<KEY>", ":")
    assert first[-3:] == ("file", ":", "<LOCATOR>")


def test_rnorm_002_activity_identity_is_four_key_slots_with_optional_history() -> None:
    with_history = (
        "Trying to trigger activity event 'hunt.001' for character Matilda of "
        "d_tuscany (Internal ID: 123 - Historical ID matilda_1), but the "
        "activity is invalid - skipping."
    )
    without_history = (
        "Trying to trigger activity event 'feast.009' for character Robert of "
        "k_france (Internal ID: 456), but the activity is invalid - skipping."
    )

    assert tokenize(with_history) == tokenize(without_history)
    first_slots = extract_structured_slots(with_history)
    second_slots = extract_structured_slots(without_history)
    assert [slot["name"] for slot in first_slots] == [
        "activity_event",
        "character_display",
        "internal_id",
        "historical_id",
    ]
    assert first_slots[-1]["present"] is True
    assert second_slots[-1]["present"] is False
