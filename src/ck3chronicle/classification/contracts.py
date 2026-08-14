"""Post-assignment validation for empirical error-template contracts.

Locator grammar is recognized during normalization, before any template is
considered. This validator therefore treats ``<LOCATOR>`` as a distinct typed
token that no key/value slot may consume.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence

from .normalize import KEY, LOCATOR, OPTIONAL_KEY, TYPE


VALUE = "<VALUE>"
PARAM = "<PARAM>"
SLOT_TOKENS = frozenset({KEY, OPTIONAL_KEY, LOCATOR, TYPE, VALUE, PARAM})


@dataclass(frozen=True)
class ValidatedSlot:
    role: str
    ordinal: int
    value: str | None
    present: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "role": self.role,
            "name": f"template_{self.role}_{self.ordinal}",
            "value": self.value,
            "present": self.present,
        }


@dataclass(frozen=True)
class TemplateValidation:
    valid: bool
    reason: str
    slots: tuple[ValidatedSlot, ...] = ()


def _literal_equal(left: str, right: str) -> bool:
    return left.casefold() == right.casefold()


def validate_template_tokens(
    candidate_tokens: Sequence[str],
    template_tokens: Sequence[str],
) -> TemplateValidation:
    """Validate literal order and typed slots after candidate assignment.

    Semantic literals must match exactly in order. Key/value/parameter/type
    slots may cover one or more non-placeholder tokens. A locator slot matches
    only the locator token produced by the earlier locator-normalization pass;
    conversely no other slot can absorb a locator. Optional keys may be absent.
    Ambiguous slot boundaries are rejected rather than guessed.
    """

    candidate = tuple(candidate_tokens)
    template = tuple(template_tokens)

    # Each solution is a tuple of (template placeholder, candidate start, end).
    # Retaining only two is sufficient to distinguish unique from ambiguous.
    @lru_cache(maxsize=None)
    def match(
        template_index: int, candidate_index: int
    ) -> tuple[tuple[tuple[str, int, int], ...], ...]:
        if template_index == len(template):
            return ((),) if candidate_index == len(candidate) else ()

        expected = template[template_index]
        if expected not in SLOT_TOKENS:
            if candidate_index >= len(candidate) or not _literal_equal(
                candidate[candidate_index], expected
            ):
                return ()
            return match(template_index + 1, candidate_index + 1)

        if expected == LOCATOR:
            if candidate_index >= len(candidate) or candidate[candidate_index] != LOCATOR:
                return ()
            tails = match(template_index + 1, candidate_index + 1)
            return tuple(
                ((expected, candidate_index, candidate_index + 1), *tail)
                for tail in tails
            )[:2]

        solutions: list[tuple[tuple[str, int, int], ...]] = []
        if expected == OPTIONAL_KEY:
            for tail in match(template_index + 1, candidate_index):
                solutions.append(((expected, candidate_index, candidate_index), *tail))
                if len(solutions) == 2:
                    return tuple(solutions)

        if candidate_index < len(candidate) and candidate[candidate_index] == expected:
            ends = (candidate_index + 1,)
        else:
            ends = tuple(
                end
                for end in range(candidate_index + 1, len(candidate) + 1)
                if not any(token in SLOT_TOKENS for token in candidate[candidate_index:end])
            )
        for end in ends:
            for tail in match(template_index + 1, end):
                solutions.append(((expected, candidate_index, end), *tail))
                if len(solutions) == 2:
                    return tuple(solutions)
        return tuple(solutions)

    solutions = match(0, 0)
    if not solutions:
        return TemplateValidation(False, "template_shape_mismatch")
    if len(solutions) > 1:
        return TemplateValidation(False, "ambiguous_slot_boundaries")

    ordinals: dict[str, int] = {}
    slots: list[ValidatedSlot] = []
    for placeholder, start, end in solutions[0]:
        role = placeholder[1:-1].casefold()
        ordinal = ordinals.get(role, 0) + 1
        ordinals[role] = ordinal
        present = end > start
        value = " ".join(candidate[start:end]) if present else None
        slots.append(ValidatedSlot(role, ordinal, value, present))
    return TemplateValidation(True, "validated", tuple(slots))
