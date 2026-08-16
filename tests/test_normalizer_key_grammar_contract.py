"""Invented regressions for CK3 grammar-bound key and locator normalization."""

from __future__ import annotations

from ck3chronicle.classification.normalize import extract_structured_slots, tokenize


def test_rnorm_001_known_key_grammars_are_value_invariant() -> None:
    variants = (
        (
            "pdxmesh [tibetan_walls_02_mesh] is out of sync with its meshsettings. "
            "[decal_planeShape] is not in use in file: gfx/models/a.mesh",
            "pdxmesh [western_walls_mesh] is out of sync with its meshsettings. "
            "[unused_shape] is not in use in file: gfx/models/b.mesh",
        ),
        (
            "estate_hire_agents_decisions has 'ai_check_interval'/'ai_check_interval_by_tier' "
            "that's negative or unset. Setting to 0 instead",
            "new_decision_key has 'ai_check_interval'/'ai_check_interval_by_tier' "
            "that's negative or unset. Setting to 0 instead",
        ),
        (
            "Unrecognized loc key roman_battle.0005.desc.hellenic.male. Near file: "
            "events/a.txt line: 10",
            "Unrecognized loc key different_event.7.desc. Near file: events/b.txt line: 99",
        ),
        (
            "Theme key pilgrimage_activity in event holy_stuff.0001 does not exist in "
            "the event theme database",
            "Theme key court_activity in event another_event.22 does not exist in the "
            "event theme database",
        ),
        ("Event betterbattles.0501 is orphaned", "Event any_namespace.99 is orphaned"),
        (
            "Event on_action_namespace.477 has been queued twice with the same data including delay",
            "Event replacement_event.2 has been queued twice with the same data including delay",
        ),
        (
            "Artifact '' (5573) has no feature in group generic_material_wood",
            "Artifact 'Crown' (16782794) has no feature in group generic_material_earthware",
        ),
    )

    for first, second in variants:
        assert tokenize(first) == tokenize(second)


def test_rnorm_002_structured_slots_retain_concrete_values() -> None:
    theme = extract_structured_slots(
        "Theme key pilgrimage_activity in event holy_stuff.0001 does not exist in "
        "the event theme database"
    )
    artifact = extract_structured_slots(
        "Artifact '' (5573) has no feature in group generic_material_wood"
    )

    assert [(slot["name"], slot["value"]) for slot in theme] == [
        ("event_theme", "pilgrimage_activity"),
        ("event", "holy_stuff.0001"),
    ]
    assert artifact == (
        {
            "role": "optional_key",
            "name": "artifact_display",
            "value": None,
            "present": False,
        },
        {"role": "key", "name": "artifact_id", "value": "5573", "present": True},
        {
            "role": "key",
            "name": "feature_group",
            "value": "generic_material_wood",
            "present": True,
        },
    )


def test_rnorm_003_scripted_effect_source_and_character_values_are_not_semantics() -> None:
    first = (
        "file: common/scripted_effects/a.txt line: 37 "
        "(had_sex_with_effect[args#1882226522]): had_sex_with_effect: root cheated "
        "on a partner that they wouldn't have Cheater: \x15ONCLICK:CHARACTER,111312 "
        "\x15TOOLTIP:CHARACTER,111312 \x15L \x15high Thado\x15!\x15! With: "
        "\x15ONCLICK:CHARACTER,16825798 \x15TOOLTIP:CHARACTER,16825798 \x15L "
        "\x15high Thuganda\x15!\x15!"
    )
    second = (
        "file: common/scripted_effects/b.txt line: 54 "
        "(different_effect[args#7]): different_effect: target cheated on a partner "
        "that they wouldn't have Cheater: \x15ONCLICK:CHARACTER,9 "
        "\x15TOOLTIP:CHARACTER,9 \x15L \x15high Other\x15!\x15! With: "
        "\x15ONCLICK:CHARACTER,10 \x15TOOLTIP:CHARACTER,10 \x15L \x15high Person\x15!\x15!"
    )

    assert tokenize(first) == tokenize(second)
    assert [(slot["name"], slot["value"]) for slot in extract_structured_slots(first)] == [
        ("scripted_effect", "had_sex_with_effect"),
        ("character_id", "111312"),
        ("character_id", "16825798"),
    ]


def test_rnorm_004_faith_and_religion_are_distinct_semantics_with_key_slots() -> None:
    faith = "Failed to scope to faith 'nicene' at file: events/a.txt line: 10"
    another_faith = "Failed to scope to faith 'chan' at file: common/b.txt line: 20"
    religion = "Failed to scope to religion 'mazdayasna_religion' at file: events/c.txt line: 30"

    assert tokenize(faith) == tokenize(another_faith)
    assert tokenize(faith) != tokenize(religion)
    assert extract_structured_slots(faith)[0]["value"] == "nicene"
    assert extract_structured_slots(religion)[0]["value"] == "mazdayasna_religion"


def test_rnorm_005_remaining_reviewed_key_grammars_are_value_invariant() -> None:
    variants = (
        (
            "PostValidate of effect 'create_noble_family_effect' returned false at file: "
            "common/a.txt line: 73 (event.1:on_accept)",
            "PostValidate of effect 'select_local_animal_effect' returned false at file: "
            "events/b.txt line: 1161 (event.2:immediate)",
        ),
        (
            "Failed to create material with shader  (in gfx/FX/court_scene.shader) for "
            "mesh [templeShape] in gfx/models/a.mesh",
            "Failed to create material with shader court_shader (in gfx/FX/other.shader) "
            "for mesh [wallShape] in gfx/models/b.mesh",
        ),
        (
            "Localization key hash collision. Key 'first.1.key' and 'second_key' have "
            "the same hash: 706125019.",
            "Localization key hash collision. Key 'other.9.key' and 'new_key' have the "
            "same hash: -12.",
        ),
        (
            "PdxAudio2: couldn't get event info '@msg_bad_soundeffect' (The requested "
            "event, parameter, bus or vca could not be found.).",
            "PdxAudio2: couldn't get event info 'event:/new_sound' (The requested event, "
            "parameter, bus or vca could not be found.).",
        ),
        (
            'Error: "Unexpected token: none, near line: 22738825" in file: "" near line: 22738825',
            'Error: "Unexpected token: invalid_key, near line: 12" in file: "a.txt" near line: 12',
        ),
    )

    for first, second in variants:
        assert tokenize(first) == tokenize(second)


def test_rnorm_006_line_locator_owns_its_parenthesized_script_frame() -> None:
    first = "Unrecognized loc key key_a. file: events/a.txt line: 10 (event_a.1:option)"
    second = "Unrecognized loc key key_b. file: events/b.txt line: 99 (event_b.7:trigger)"

    assert tokenize(first) == tokenize(second)
    assert tokenize(first).count("<LOCATOR>") == 1


def test_rnorm_007_empty_flavorization_title_is_an_optional_key() -> None:
    empty = "Failed to find any valid flavorization for title "
    present = "Failed to find any valid flavorization for title x_title_1"

    assert tokenize(empty) == tokenize(present)
    assert tokenize(empty)[-1] == "<OPTIONAL_KEY>"
    assert extract_structured_slots(empty) == (
        {
            "role": "optional_key",
            "name": "title",
            "value": None,
            "present": False,
        },
    )


def test_rnorm_008_tributary_reason_masks_identity_but_retains_relationship() -> None:
    first = (
        "Script system error! Error: make_tributary effect [ Tried to make 'Mengi Lowborn "
        "of c_shor (Internal ID 33689379)' a Tributary contract with Suzerain 'Zhyrgal "
        "Enisey of e_kirghiz (Internal ID: 22292 - Historical ID 303239)', but they are "
        "already a vassal of Zhyrgal Enisey of e_kirghiz (Internal ID: 22292 - "
        "Historical ID 303239). ]"
    )
    second = (
        "Script system error! Error: another_effect effect [ Tried to make 'Other Person "
        "of c_other (Internal ID 1 - Historical ID 2)' a Tributary contract with Suzerain "
        "'New Ruler of e_new (Internal ID: 3)', but they are already a vassal of New Ruler "
        "of e_new (Internal ID: 3). ]"
    )

    assert tokenize(first) == tokenize(second)
    assert "Tributary" in tokenize(first)
    slots = extract_structured_slots(first)
    assert len(slots) == 12
    assert slots[0]["value"] == "Mengi Lowborn"
    assert slots[3]["present"] is False
    assert slots[7]["value"] == "303239"
