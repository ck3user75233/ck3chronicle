"""Inference views using the shared declared-parameter matcher."""
from .matching_defaults import RULES
DEFINITIONS = RULES.declarations['parameter_structures']
BY_ID = RULES.parameter_definitions
FULL_IDS = RULES.full_ids
field_ranges = RULES.parameter_field_ranges

def declarations_for(pieces, protected, source):
    return field_ranges(tuple(pieces),tuple(protected),source)
