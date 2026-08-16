"""Executable CK3-specific invariants for the WIP template learner."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "template_learning"
    / "learn_error_templates.py"
)
SPEC = importlib.util.spec_from_file_location("learn_error_templates", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
learner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = learner
SPEC.loader.exec_module(learner)


def record(source: str, message: str, count: int = 1):
    units = learner.semantic_units(source, message)
    assert units
    unit = units[0]
    return learner.SequenceRecord(
        source_family=source,
        tokens=learner.tokenize(unit),
        semantic_lead=learner.diagnostic_lead(unit),
        occurrences=count,
        evidence_ids={"fixture"},
        examples=[unit],
    )


def test_locator_values_never_change_normalized_tokens():
    messages = [
        "Failed at file: common/scripted_effects/a.txt line: 12 (effect_a)",
        "Value of wrong type in 'file: events/a.txt line: 7 (a.1:option)'",
        r"Could not load C:\Users\name\mod\gfx\a.dds near line 42",
        "Unexpected localization token at line 93 and column 28 in localization/english/a.yml",
    ]
    for message in messages:
        assert learner.tokenize(learner.mutate_locators(message)) == learner.tokenize(
            message
        )


def test_duplicate_localization_keys_and_files_form_one_template():
    source = "localization_reader.cpp"
    messages = [
        "Duplicate localization key. Key 'Carthage' is defined in both "
        "'localization/english/a.yml' and 'localization/english/b.yml'",
        "Duplicate localization key. Key 'Rome' is defined in both "
        "'localization/english/c.yml' and 'localization/english/d.yml'",
        "Duplicate localization key. Key 'Alexandria' is defined in both "
        "'localization/english/e.yml' and 'localization/english/f.yml'",
    ]
    clusters = learner.cluster_source_records(
        source,
        [record(source, message) for message in messages],
        threshold=0.72,
    )
    assert len(clusters) == 1
    template = " ".join(clusters[0].template_tokens)
    assert "<KEY>" in template
    assert "<LOCATOR>" in template
    assert "Carthage" not in template
    assert "Rome" not in template


def test_source_prefix_is_part_of_template_identity():
    message = "Missing loc example_key"
    left = learner.cluster_source_records(
        "source_a.cpp", [record("source_a.cpp", message)], threshold=0.72
    )[0]
    right = learner.cluster_source_records(
        "source_b.cpp", [record("source_b.cpp", message)], threshold=0.72
    )[0]
    assert left.cluster_id != right.cluster_id


def test_ordered_semantic_lead_prevents_false_merge_inside_one_source():
    source = "pdx_persistent_reader.cpp"
    messages = [
        'Error: "Unknown trigger: adulterer, near line: 414" in file: "common/a.txt"',
        'Error: "Unknown trigger: sodomite, near line: 415" in file: "common/b.txt"',
        'Error: "Unexpected token: all, near line: 7" in file: "common/c.txt"',
    ]
    clusters = learner.cluster_source_records(
        source,
        [record(source, message) for message in messages],
        threshold=0.72,
    )
    assert len(clusters) == 2
    leads = {cluster.medoid.semantic_lead for cluster in clusters}
    assert leads == {("unknown", "trigger"), ("unexpected", "token")}


def test_flag_and_variable_remain_distinct_semantic_templates():
    source = "jomini_effect.cpp"
    suffix = "is set but is never used. Note that use in localization doesn't count"
    messages = [
        f"Flag 'existing' {suffix}",
        f"Flag 'another_flag' {suffix}",
        f"Variable 'some_value' {suffix}",
    ]
    clusters = learner.cluster_source_records(
        source,
        [record(source, message) for message in messages],
        threshold=0.72,
    )
    assert len(clusters) == 2
    leads = {cluster.medoid.semantic_lead for cluster in clusters}
    assert leads == {("flag", "is"), ("variable", "is")}


def test_complete_script_location_chain_never_fragments_undefined_target():
    source = "jomini_script_system.cpp"
    messages = [
        "Script system error! Error: Undefined event target 'realist' "
        "Script location: file: events/VIET_events_basic.txt line: 21649 "
        "(VIETmisc.0243:option)",
        "Script system error! Error: Undefined event target 'oathman_2' "
        "Script location: file: events/house_honor_events.txt line: 137 "
        "(house_honor.0001:immediate)",
        "Script system error! Error: Undefined event target 'local_prostitute_scope' "
        "Script location: file: common/scripted_effects/zzz_99_secret_effects.txt "
        "line: 325 (give_homosexual_secret_or_nothing_with_target_effect[args#1]) "
        "file: events/eps_travel_events.txt line: 717 (eps_travel_events.04:option)",
    ]
    clusters = learner.cluster_source_records(
        source,
        [record(source, message) for message in messages],
        threshold=0.72,
    )
    assert len(clusters) == 1
    template = " ".join(clusters[0].template_tokens)
    assert "Script location" not in template
    assert "VIETmisc" not in template
    assert "house_honor" not in template
    assert "<KEY>" in template


def test_complete_script_location_chain_never_fragments_unset_scope():
    source = "jomini_script_system.cpp"
    messages = [
        "Script system error! Error: Event target link 'scope' returned an unset scope "
        "Script location: file: common/scripted_effects/zzz_99_secret_effects.txt "
        "line: 325 (give_secret) file: events/a.txt line: 7 (a.1:option)",
        "Script system error! Error: Event target link 'capital_province' returned an unset scope "
        "Script location: file: common/scripted_effects/20_health_effects.txt "
        "line: 938 (contract_lovers_pox_from) file: common/scripted_effects/b.txt "
        "line: 969 (risk_of_std_from_effect) file: events/c.txt line: 8 (c.1:option)",
    ]
    clusters = learner.cluster_source_records(
        source,
        [record(source, message) for message in messages],
        threshold=0.72,
    )
    assert len(clusters) == 1
    assert "Script location" not in " ".join(clusters[0].template_tokens)


def test_different_script_semantics_remain_separate_after_location_removal():
    source = "jomini_script_system.cpp"
    messages = [
        "Script system error! Error: Undefined event target 'scope' "
        "Script location: file: events/a.txt line: 1 (a.1:option)",
        "Script system error! Error: Event target link 'scope' returned an unset scope "
        "Script location: file: events/a.txt line: 1 (a.1:option)",
    ]
    clusters = learner.cluster_source_records(
        source,
        [record(source, message) for message in messages],
        threshold=0.72,
    )
    assert len(clusters) == 2


def test_character_reference_preserves_optional_key_without_changing_identity():
    without_historical = (
        "Removing travel plan from the character Kumarapala Lowborn of "
        "(Internal ID 76492) owner when the travel plan is not ending normally."
    )
    with_historical = (
        "Removing travel plan from the character Yan_9854 Zhao of "
        "(Internal ID: 66759 - Historical ID han_9141) owner when the travel "
        "plan is not ending normally."
    )
    with_title_and_historical = (
        "Removing travel plan from the character Beorhtric of Gloucester of "
        "x_d_laamp_1168 (Internal ID: 59403 - Historical ID normandy_002) "
        "owner when the travel plan is not ending normally."
    )
    with_title_without_historical = (
        "Removing travel plan from the character Huaiguang Qu of x_d_laamp_1187 "
        "(Internal ID 81737) owner when the travel plan is not ending normally."
    )
    expected_tokens = learner.tokenize(without_historical)
    assert learner.tokenize(with_historical) == expected_tokens
    assert learner.tokenize(with_title_and_historical) == expected_tokens
    assert learner.tokenize(with_title_without_historical) == expected_tokens
    template = " ".join(learner.tokenize(with_historical))
    assert "<KEY>" in template
    assert "<OPTIONAL_KEY>" in template
    assert "Internal ID" not in template
    assert "Historical ID" not in template

    absent = learner.extract_structured_slots(without_historical)
    present = learner.extract_structured_slots(with_historical)
    assert [(slot["name"], slot["value"], slot["present"]) for slot in absent] == [
        ("character_display", "Kumarapala Lowborn", True),
        ("internal_id", "76492", True),
        ("historical_id", None, False),
    ]
    assert [(slot["name"], slot["value"], slot["present"]) for slot in present] == [
        ("character_display", "Yan_9854 Zhao", True),
        ("internal_id", "66759", True),
        ("historical_id", "han_9141", True),
    ]
    titled = learner.extract_structured_slots(with_title_and_historical)
    assert [(slot["name"], slot["value"], slot["present"]) for slot in titled] == [
        ("character_display", "Beorhtric of Gloucester of x_d_laamp_1168", True),
        ("internal_id", "59403", True),
        ("historical_id", "normandy_002", True),
    ]


def test_repeated_persistent_reader_clauses_are_occurrences_not_templates():
    source = "pdx_persistent_reader.cpp"
    message = (
        'Error: "Unknown trigger: adulterer, near line: 420 '
        "Unknown trigger: incestuous, near line: 421 "
        'Unknown trigger: sodomite, near line: 422" in file: '
        '"common/scripted_triggers/religious.txt" near line: 423'
    )
    units = learner.semantic_units(source, message)
    assert len(units) == 3
    assert units == ["Unknown trigger: <KEY>"] * 3
    assert len({learner.tokenize(unit) for unit in units}) == 1


def test_repeated_failed_key_references_are_one_base_template():
    source = "pdx_persistent_reader.cpp"
    message = (
        'Error: "Failed to read key reference: first: first, near line: 7 '
        'Failed to read key reference: second: second, near line: 8" '
        'in file: "save games/example.ck3" near line: 9'
    )
    units = learner.semantic_units(source, message)
    assert units == [
        "Failed to read key reference: <KEY> : <KEY>",
        "Failed to read key reference: <KEY> : <KEY>",
    ]


def test_block_message_never_truncates_a_repeated_clause_wrapper():
    continuations = [
        f"Failed to read key reference: key_{index}: key_{index}, near line: {index}"
        for index in range(1, 15)
    ]
    continuations.append('in file: "save games/example.ck3" near line: 15')
    block = SimpleNamespace(
        header_line='[00:00:00][pdx_persistent_reader.cpp:1]: Error: "',
        continuation_lines=continuations,
    )
    message = learner.block_message(block)
    assert "key_14" in message
    assert message.endswith('in file: "save games/example.ck3" near line: 15')


def test_scope_namespace_and_key_relationships_are_not_one_opaque_slot():
    message = (
        "Script system error! Error: scope:target.faith trigger "
        "[ Failed context switch ]"
    )
    tokens = learner.tokenize(message)
    assert tokens == (
        "Script",
        "system",
        "error",
        "!",
        "Error",
        ":",
        "scope",
        ":",
        "<KEY>",
        ".",
        "<KEY>",
        "trigger",
        "[",
        "Failed",
        "context",
        "switch",
        "]",
    )
    assert "target" not in tokens
    assert "faith" not in tokens


def test_scope_and_plain_failed_context_switches_are_distinct_structural_contracts():
    source = "jomini_script_system.cpp"
    messages = [
        "Script system error! Error: scope:target.faith trigger "
        "[ Failed context switch ]",
        "Script system error! Error: scope:holder.culture trigger "
        "[ Failed context switch ]",
        "Script system error! Error: capital_province trigger "
        "[ Failed context switch ]",
        "Script system error! Error: mother trigger [ Failed context switch ]",
    ]
    clusters = learner.cluster_source_records(
        source,
        [record(source, message) for message in messages],
        threshold=0.72,
    )
    assert len(clusters) == 2
    templates = {" ".join(cluster.template_tokens) for cluster in clusters}
    assert any("scope : <KEY> . <KEY> trigger" in template for template in templates)
    assert any("<KEY> trigger" in template and "scope" not in template for template in templates)


def test_script_system_role_words_are_semantic_not_slots():
    trigger = learner.tokenize(
        "Script system error! Error: prowess_diff trigger [ target was null ]"
    )
    effect = learner.tokenize(
        "Script system error! Error: every_house_member effect "
        "[ Scoped object is not valid ]"
    )
    assert "prowess_diff" not in trigger
    assert "every_house_member" not in effect
    assert "trigger" in trigger
    assert "effect" in effect
    assert trigger != effect


def test_script_system_parenthetical_prefix_is_part_of_contract_identity():
    source = "jomini_script_system.cpp"
    plain = "Script system error! Error: capital_province trigger [ Failed context switch ]"
    tooltip = (
        "Script system error! (while building tooltip/description) Error: "
        "capital_province trigger [ Failed context switch ]"
    )
    records = [record(source, plain), record(source, tooltip)]
    clusters = learner.cluster_source_records(source, records, threshold=0.72)
    assert len(clusters) == 2
    assert records[0].semantic_lead != records[1].semantic_lead


def test_script_system_brackets_define_reason_layer_not_outer_identity():
    first = learner.tokenize(
        "Script system error! Error: scope:target trigger "
        "[ Failed context switch ]"
    )
    second = learner.tokenize(
        "Script system error! Error: scope:recipient trigger "
        "[ Scoped object of type 'character' is not valid "
        "((no character) weak (Character - 16910423)!) ]"
    )
    first_layers = learner.script_system_layer_tokens(first)
    second_layers = learner.script_system_layer_tokens(second)
    assert first_layers is not None and second_layers is not None
    assert first_layers[0] == second_layers[0]
    assert first_layers[1] != second_layers[1]
    assert first_layers[0][-2:] == ("<KEY>", "trigger")
    assert first_layers[1] == ("Failed", "context", "switch")


def test_novel_script_reason_receives_l1_without_false_l2_assignment():
    source = "jomini_script_system.cpp"
    trained = record(
        source,
        "Script system error! Error: scope:target trigger "
        "[ Failed context switch ]",
    )
    clusters = learner.cluster_source_records(source, [trained], threshold=0.72)
    by_source = {source: clusters}
    novel_message = (
        "Script system error! Error: scope:recipient trigger "
        "[ Scoped object of type 'character' is not valid "
        "((no character) weak (Character - 16910423)!) ]"
    )
    novel_tokens = learner.tokenize(novel_message)
    full = learner.best_cluster(
        by_source,
        source,
        novel_tokens,
        learner.diagnostic_lead(novel_message),
        0.72,
    )
    layered = learner.best_layered_cluster(
        by_source,
        source,
        novel_tokens,
        learner.diagnostic_lead(novel_message),
        0.72,
    )
    assert full is None
    assert layered.cluster is None
    assert layered.outer_known is True
    assert layered.assignment_level == "L1"


def test_independently_known_outer_and_reason_compose_without_false_full_match():
    source = "jomini_script_system.cpp"
    training = [
        record(
            source,
            "Script system error! Error: scope:target trigger "
            "[ Failed context switch ]",
        ),
        record(
            source,
            "Script system error! Error: exists trigger "
            "[ Scoped object of type 'character' is not valid "
            "((no character) weak (Character - 16910423)!) ]",
        ),
    ]
    clusters = learner.cluster_source_records(source, training, threshold=0.72)
    by_source = {source: clusters}
    candidate = (
        "Script system error! Error: scope:recipient trigger "
        "[ Scoped object of type 'character' is not valid "
        "((no character) weak (Character - 16910423)!) ]"
    )
    match = learner.best_layered_cluster(
        by_source,
        source,
        learner.tokenize(candidate),
        learner.diagnostic_lead(candidate),
        0.72,
    )
    assert match.cluster is None
    assert match.outer_known is True
    assert match.reason_cluster is not None
    assert match.assignment_level == "L1+L2"


def test_reason_composition_rejects_conflicting_fixed_subtype_literals():
    candidate_layers = learner.script_system_layer_tokens(
        learner.tokenize(
            "Script system error! Error: scope:recipient trigger "
            "[ Scoped object of type 'character' is not valid "
            "((no character) weak (Character - 16910423)!) ]"
        )
    )
    compatible_reason = (
        "Scoped", "object", "of", "type", "'", "<KEY>", "'", "is",
        "not", "valid", "(", "<KEY>", "weak", "(", "<KEY>", "-",
        "<VALUE>", ")", "!", ")",
    )
    conflicting_layers = learner.script_system_layer_tokens(
        learner.tokenize(
            "Script system error! Error: scope:target.faith trigger "
            "[ Scoped object of type 'domicile' is not valid "
            "((null) weak (Domicile - 4294967295)!) ]"
        )
    )
    assert candidate_layers and conflicting_layers
    assert learner.template_fixed_semantics_are_ordered(
        compatible_reason, candidate_layers[1]
    )
    assert not learner.template_fixed_semantics_are_ordered(
        conflicting_layers[1], candidate_layers[1]
    )


def test_reason_semantics_remain_ordered_l2_contract_content():
    first = learner.script_system_layer_tokens(
        learner.tokenize(
            "Script system error! Error: has_opinion_modifier trigger "
            "[ trying to evaluate an opinion modifier trigger on a null target ]"
        )
    )
    second = learner.script_system_layer_tokens(
        learner.tokenize(
            "Script system error! Error: has_opinion_modifier trigger "
            "[ target was null while evaluating an opinion modifier trigger ]"
        )
    )
    assert first is not None and second is not None
    assert first[0] == second[0]
    assert first[1] != second[1]
    assert first[1] == (
        "trying",
        "to",
        "evaluate",
        "an",
        "opinion",
        "modifier",
        "trigger",
        "on",
        "a",
        "null",
        "target",
    )


def test_script_location_changes_neither_outer_nor_reason_layer():
    base = (
        "Script system error! Error: learn_language_of_culture effect "
        "[ Already knows language ]"
    )
    located = (
        base
        + " Script location: file: events/a.txt line: 17 (a.1:immediate) "
        + "file: common/scripted_effects/b.txt line: 99 (learn_language)"
    )
    assert learner.script_system_layer_tokens(learner.tokenize(base)) == (
        learner.script_system_layer_tokens(learner.tokenize(located))
    )


def test_travel_plan_reason_identity_is_structured_keys_not_template_semantics():
    variants = [
        "Script system error! Error: start_travel_plan effect [ Jixing "
        "Yuezheng of x_d_laamp_1190 (Internal ID 81880)'s travel plan have "
        "no valid destinations ]",
        "Script system error! Error: start_travel_plan effect [ Marwan "
        "Yamraid of x_d_laamp_1262 (Internal ID: 23938 - Historical ID "
        "73900)'s travel plan have no valid destinations ]",
    ]
    assert learner.tokenize(variants[0]) == learner.tokenize(variants[1])
    layers = learner.script_system_layer_tokens(learner.tokenize(variants[0]))
    assert layers is not None
    assert layers[1] == (
        "<KEY>",
        "(",
        "<KEY>",
        "<OPTIONAL_KEY>",
        ")",
        "'",
        "s",
        "travel",
        "plan",
        "have",
        "no",
        "valid",
        "destinations",
    )
    without_historical = learner.extract_structured_slots(variants[0])
    with_historical = learner.extract_structured_slots(variants[1])
    assert [(row["name"], row["present"]) for row in without_historical] == [
        ("character_display", True),
        ("internal_id", True),
        ("historical_id", False),
    ]
    assert [(row["name"], row["present"]) for row in with_historical] == [
        ("character_display", True),
        ("internal_id", True),
        ("historical_id", True),
    ]


def test_bounded_long_reason_preserves_l1_but_cannot_claim_l2():
    source = "jomini_script_system.cpp"
    trained_message = (
        "Script system error! Error: add_domicile_building effect "
        "[ Invalid database object 'building_a' ]"
    )
    clusters = learner.cluster_source_records(
        source, [record(source, trained_message)], threshold=0.72
    )
    long_message = (
        "Script system error! Error: add_domicile_building effect [ Cannot "
        "begin new construction when already constructing: "
        + " ".join(f"building_{index}" for index in range(500))
        + " ]"
    )
    tokens = learner.tokenize(long_message)
    assert "]" not in tokens
    layers = learner.script_system_layer_tokens(tokens)
    assert layers is not None
    assert layers[0][-2:] == ("<KEY>", "effect")
    assert layers[1][-1] == learner.TRUNCATED_REASON
    match = learner.best_layered_cluster(
        {source: clusters},
        source,
        tokens,
        learner.diagnostic_lead(long_message),
        0.72,
    )
    assert match.outer_known is True
    assert match.reason_cluster is None
    assert match.assignment_level == "L1"


def test_unclosed_logged_reason_still_normalizes_outer_symbol_for_l1():
    fragment = (
        "Script system error! Error: add_domicile_building effect [ Cannot "
        "begin new construction when already constructing: "
        "'east_asian_estate_examination_room_01' Current Buildings = { Slot {"
    )
    tokens = learner.tokenize(fragment)
    layers = learner.script_system_layer_tokens(tokens)
    assert layers is not None
    assert layers[0][-2:] == ("<KEY>", "effect")
    assert "add_domicile_building" not in layers[0]
    assert layers[1][-1] == learner.TRUNCATED_REASON


def test_script_system_prefix_identity_applies_without_trigger_effect_envelope():
    source = "jomini_script_system.cpp"
    plain = "Script system error! Error: Event target link 'scope' returned an unset scope"
    tooltip = (
        "Script system error! (while building tooltip/description) Error: "
        "Event target link 'scope' returned an unset scope"
    )
    records = [record(source, plain), record(source, tooltip)]
    clusters = learner.cluster_source_records(source, records, threshold=0.72)
    assert len(clusters) == 2
    assert records[0].semantic_lead != records[1].semantic_lead


def test_comparison_runtime_types_are_ck3_symbol_key_slots():
    variants = [
        "Script system error! Error: Left side and right side during comparison "
        "were of different types (left was 'culture_tradition', right was 'flag')",
        "Script system error! Error: Left side and right side during comparison "
        "were of different types (left was 'culture_pillar', right was 'flag')",
        "Script system error! Error: Left side and right side during comparison "
        "were of different types (left was 'flag', right was 'boolean')",
    ]
    tokenizations = {learner.tokenize(message) for message in variants}
    assert len(tokenizations) == 1
    tokens = next(iter(tokenizations))
    assert tokens.count("<KEY>") == 2


def test_trigger_description_key_and_location_form_one_contract():
    variants = [
        "character_this_equal: Scope dependent values in localization inside an "
        "any trigger; consider using a custom_tooltip; at file: events/a.txt "
        "line: 12 (a.1:option:trigger)",
        "house_equal: Scope dependent values in localization inside an any "
        "trigger; consider using a custom_tooltip; at file: common/b.txt "
        "line: 99 (house_check[args#1])",
    ]
    assert len({learner.tokenize(message) for message in variants}) == 1
    template = " ".join(learner.tokenize(variants[0]))
    assert template.startswith("<KEY> : Scope dependent values")
    assert "<LOCATOR>" in template


def test_flavorization_target_is_a_title_key_not_a_locator():
    messages = [
        "Failed to find any valid flavorization for title x_nf_1449",
        "Failed to find any valid flavorization for title x_script_2404",
    ]
    assert len({learner.tokenize(message) for message in messages}) == 1
    tokens = learner.tokenize(messages[0])
    assert tokens[-1] == "<OPTIONAL_KEY>"
    assert "<LOCATOR>" not in tokens


def test_activity_event_optional_character_metadata_does_not_split_contract():
    messages = [
        "Trying to trigger activity event 'siberia.0028' for character Longun "
        "Doplabunt of c_eman_amgun (Internal ID 16901394), but the activity is "
        "invalid - skipping.",
        "Trying to trigger activity event 'coronation_events.0311' for character "
        "Ioannes Doukas of e_byzantium (Internal ID: 56308 - Historical ID 1746), "
        "but the activity is invalid - skipping.",
    ]
    assert len({learner.tokenize(message) for message in messages}) == 1
    template = " ".join(learner.tokenize(messages[0]))
    assert "<KEY>" in template
    assert "<OPTIONAL_KEY>" in template
    assert "Internal ID" not in template
    assert "Historical ID" not in template


def test_known_ck3_key_grammars_preserve_semantics_and_mask_identifiers():
    variants = [
        (
            "pdxmesh [tibetan_walls_02_mesh] is out of sync with its meshsettings. "
            "[decal_planeShape] is not in use in file: gfx/models/a.mesh",
            "pdxmesh [western_walls_mesh] is out of sync with its meshsettings. "
            "[unused_shape] is not in use in file: gfx/models/b.mesh",
            2,
        ),
        (
            "estate_hire_agents_decisions has 'ai_check_interval'/'ai_check_interval_by_tier' "
            "that's negative or unset. Setting to 0 instead",
            "new_decision_key has 'ai_check_interval'/'ai_check_interval_by_tier' "
            "that's negative or unset. Setting to 0 instead",
            1,
        ),
        (
            "Unrecognized loc key roman_battle.0005.desc.hellenic.male. Near file: "
            "events/a.txt line: 10",
            "Unrecognized loc key different_event.7.desc. Near file: events/b.txt line: 99",
            1,
        ),
        (
            "Theme key pilgrimage_activity in event holy_stuff.0001 does not exist in "
            "the event theme database",
            "Theme key court_activity in event another_event.22 does not exist in the "
            "event theme database",
            2,
        ),
        ("Event betterbattles.0501 is orphaned", "Event any_namespace.99 is orphaned", 1),
        (
            "Event on_action_namespace.477 has been queued twice with the same data including delay",
            "Event replacement_event.2 has been queued twice with the same data including delay",
            1,
        ),
        (
            "Artifact '' (5573) has no feature in group generic_material_wood",
            "Artifact 'Crown' (16782794) has no feature in group generic_material_earthware",
            2,
        ),
    ]
    for first, second, key_count in variants:
        first_tokens = learner.tokenize(first)
        assert learner.tokenize(second) == first_tokens
        assert first_tokens.count("<KEY>") == key_count
    artifact_tokens = learner.tokenize(variants[-1][0])
    assert artifact_tokens.count("<OPTIONAL_KEY>") == 1


def test_scripted_effect_context_masks_source_effect_and_rendered_character_keys():
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

    first_tokens = learner.tokenize(first)
    assert learner.tokenize(second) == first_tokens
    assert learner.tokenize(learner.mutate_locators(first)) == first_tokens
    assert first_tokens.count("<LOCATOR>") == 1
    assert first_tokens.count("<KEY>") == 3
    assert "had_sex_with_effect" not in first_tokens
    assert "111312" not in first_tokens


def test_faith_and_religion_scope_failures_keep_the_semantic_target_distinct():
    first_faith = "Failed to scope to faith 'nicene' at file: events/a.txt line: 10"
    second_faith = "Failed to scope to faith 'chan' at file: common/b.txt line: 20"
    religion = "Failed to scope to religion 'mazdayasna_religion' at file: events/c.txt line: 30"

    assert learner.tokenize(first_faith) == learner.tokenize(second_faith)
    assert learner.diagnostic_lead(first_faith) == learner.diagnostic_lead(second_faith)
    assert learner.diagnostic_lead(first_faith) != learner.diagnostic_lead(religion)
    assert learner.tokenize(first_faith).count("<KEY>") == 1


def test_remaining_public_grammar_families_mask_only_values_and_locator_context():
    pairs = (
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
    for first, second in pairs:
        assert learner.tokenize(first) == learner.tokenize(second)


def test_line_locator_includes_its_parenthesized_script_frame():
    first = "Unrecognized loc key key_a. file: events/a.txt line: 10 (event_a.1:option)"
    second = "Unrecognized loc key key_b. file: events/b.txt line: 99 (event_b.7:trigger)"

    assert learner.tokenize(first) == learner.tokenize(second)
    assert learner.tokenize(first).count("<LOCATOR>") == 1


def test_empty_flavorization_title_is_one_optional_key_contract():
    assert learner.tokenize("Failed to find any valid flavorization for title ") == learner.tokenize(
        "Failed to find any valid flavorization for title x_title_1"
    )
    assert "<OPTIONAL_KEY>" in learner.tokenize(
        "Failed to find any valid flavorization for title "
    )


def test_tributary_reason_normalizes_character_identity_but_keeps_relationship_words():
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

    assert learner.tokenize(first) == learner.tokenize(second)
    assert "Tributary" in learner.tokenize(first)
