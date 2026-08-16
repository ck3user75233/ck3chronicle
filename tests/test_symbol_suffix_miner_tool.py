"""QC boundaries for underscore-suffix mining."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "template_learning"
    / "mine_symbol_suffixes.py"
)
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("mine_symbol_suffixes", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
miner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = miner
SPEC.loader.exec_module(miner)


def test_arbitrary_segment_effect_and_trigger_shapes_are_detected():
    assert miner.UNDERSCORE_IDENTIFIER_RE.fullmatch("had_sex_with_effect")
    assert miner.UNDERSCORE_IDENTIFIER_RE.fullmatch("is_valid_agent_standard_trigger")
    assert "had_sex_with_effect".rsplit("_", 1)[1] == "effect"
    assert "is_valid_agent_standard_trigger".rsplit("_", 1)[1] == "trigger"


def test_symbol_shape_in_masked_callsite_is_locator_evidence():
    tokens = (
        "Failed",
        "at",
        "file",
        ":",
        "<LOCATOR>",
        "(",
        "had_sex_with_effect",
        "[",
        "args#123",
        "]",
        ")",
    )
    assert miner.locator_context(tokens, 6)


def test_same_symbol_shape_in_semantic_message_is_not_excluded():
    tokens = ("Unknown", "effect", "had_sex_with_effect")
    assert not miner.locator_context(tokens, 2)
