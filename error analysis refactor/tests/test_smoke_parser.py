from ck3chronicle_proto.log_parser import parse_script_error_blocks


def test_script_error_parser_emits_canonical_issue():
    sample = """
[04:03:16][E][jomini_script_system.cpp:303]: Script system error!
  Error: untyped trigger [ Scoped object of type 'character' is not valid ((no character) weak (Character - 18182)!) ]
  Script location: file: common/scripted_effects/TCT_scripted_effects.txt line: 275 (predict_new_cardinal)
    file: common/scripted_effects/TCT_scripted_effects.txt line: 315 (update_cardinal_window)
    file: common/on_action/tct_on_actions.txt line: 673 (tct_cardinal_update)
""".strip()
    issues = parse_script_error_blocks(sample)
    assert len(issues) == 1
    issue = issues[0]
    assert issue.schema_version == "ck3chronicle.issue.v1"
    assert issue.primary_file == "common/scripted_effects/TCT_scripted_effects.txt"
    assert issue.primary_line == 275
    assert issue.primary_symbol == "predict_new_cardinal"
    assert issue.category == "Script Execution"
    assert len(issue.call_stack) == 3
