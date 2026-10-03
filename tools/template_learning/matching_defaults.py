"""Learner-only explicit construction of shared mechanics from current rules."""
from .owner_rules import OWNER_RULES
from .matching_primitives import Rules, key_piece_sequence as _key_piece_sequence

RULES = Rules(OWNER_RULES)
analyze_match_pattern = RULES.analyze_match_pattern
match_pattern = RULES.match_pattern
parameter_piece_ranges = RULES.parameter_piece_ranges
location_piece_ranges = RULES.location_piece_ranges
location_piece_indices = RULES.location_piece_indices
location_capture_ends = RULES.location_capture_ends

def key_piece_sequence(pieces, joiners=None):
    return _key_piece_sequence(pieces, OWNER_RULES['inference_policy']['key_syntax']['joiners'] if joiners is None else joiners)
