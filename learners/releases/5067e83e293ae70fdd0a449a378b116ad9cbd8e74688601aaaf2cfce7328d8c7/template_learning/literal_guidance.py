"""Explicit wording guidance over existing raw-parser pieces, never slot types."""
from .matching_primitives import guided_ranges
from functools import lru_cache
from template_learning.owner_rules import LITERAL_GUIDANCE


LITERAL_WORDING = tuple(LITERAL_GUIDANCE["literals"])


def guided_piece_indices(pieces):
    ranges = guided_ranges(tuple(pieces),LITERAL_WORDING)
    indices,offset = [],0
    for i,(_,value) in enumerate(pieces):
        end = offset+len(value)
        if any(offset < b and end > a for a,b in ranges):
            indices.append(i)
        offset = end
    return indices
