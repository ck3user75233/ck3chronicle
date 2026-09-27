"""Explicit wording guidance over existing raw-parser pieces, never slot types."""
from functools import lru_cache
from template_learning.owner_rules import LITERAL_GUIDANCE


LITERAL_WORDING = tuple(LITERAL_GUIDANCE["literals"])


def guided_ranges(pieces, wording):
    # Serialized wrapper pieces are lists; native message pieces are tuples.
    # Canonicalize only containers for caching, never their kind/text content.
    return _guided_ranges(tuple((kind,value) for kind,value in pieces),tuple(wording))


@lru_cache(maxsize=16384)
def _guided_ranges(pieces, wording):
    """Return exact character ranges aligned with complete existing pieces.

    `target_key` and `@target` stay intact: an interior substring cannot satisfy
    the boundary requirement. Multiword guidance retains its exact native gaps.
    """
    text = "".join(value for _,value in pieces)
    boundaries,offset = {0},0
    for _,value in pieces:
        offset += len(value)
        boundaries.add(offset)
    ranges = set()
    for literal in wording:
        start = text.find(literal)
        while start >= 0:
            end = start + len(literal)
            if start in boundaries and end in boundaries:
                ranges.add((start,end))
            start = text.find(literal,start+1)
    return tuple(sorted(ranges))


def guided_piece_indices(pieces):
    ranges = guided_ranges(tuple(pieces),LITERAL_WORDING)
    indices,offset = [],0
    for i,(_,value) in enumerate(pieces):
        end = offset+len(value)
        if any(offset < b and end > a for a,b in ranges):
            indices.append(i)
        offset = end
    return indices
