"""Exact empirical token matching and original-value binding.

Source families are hard partitions. Fixed tokens (including punctuation and
case) must match in order with complete coverage. Slot syntax follows the
retained learner's infer_slot: identifiers, numeric values, closed alternatives,
locator/punctuation spans and generic parameters. Grammar-created TYPE and
OPTIONAL_KEY masks match only their normalized markers; absent optionals have
an explicit marker and zero-width original value, not an invented epsilon rule.

No similarity threshold establishes an assignment. Competing structures or
multiple variable alignments remain unresolved. Equal layer token tuples share
one deterministic representative cluster; that choice adds no layer taxonomy.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

from .bindings import bind_matched_spans
from .domain import (LearnedVariable, NormalizedView, RecoveredDiagnostic,
                     StructuralClassification, StructuralFailure,
                     StructuralIdentity, TokenSpan)
from .model import EmpiricalModel, is_variable
from .normalization import NORMALIZER_REVISION, script_system_layers
from .diagnostics import RECOVERY_REVISION

CLASSIFIER_REVISION = "ck3-exact-empirical-classifier-v1"
_PUNCTUATION = frozenset("'\"`()[]{}:;,.=!?/\\")
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_#@-]*")


def _accepts(slot: str, tokens: tuple[str, ...]) -> bool:
    if tokens == (slot,):
        return True
    # These two typed masks come only from the actual normalization grammars.
    if slot in {"<OPTIONAL_KEY>", "<TYPE>"}:
        return False
    if slot == "<LOCATOR>":
        return "<LOCATOR>" in tokens and all(
            token == "<LOCATOR>" or token in _PUNCTUATION for token in tokens)
    meaningful = [t for t in tokens if t not in _PUNCTUATION and t != "<LOCATOR>"]
    if slot.startswith("<ALT:"):
        return len(meaningful) == 1 and meaningful[0] in slot[5:-1].split("|")
    if slot == "<KEY>":
        identifiers = bool(meaningful) and all(_IDENTIFIER.fullmatch(t) for t in meaningful)
        key_shape = len(meaningful) <= 4 or any(
            "_" in t or "." in t or any(c.isdigit() for c in t)
            or (t[:1].isupper() and t[1:].islower()) for t in meaningful)
        return identifiers and key_shape
    if slot == "<VALUE>":
        return bool(meaningful) and all(t.replace(".", "", 1).isdigit() for t in meaningful)
    # infer_slot's residual class has no narrower empirical type constraint.
    return slot == "<PARAM>" and bool(tokens)


def _align(template: tuple[str, ...], tokens: tuple[str, ...]):
    """Return up to two complete positional alignments, detecting ambiguity.

    Dynamic states are token positions, not recursive substring searches.
    Keeping two paths per state suffices: identical future suffixes cannot
    make two distinct prefixes unambiguous again. Nothing reads raw text.
    """
    states = {0: [()]}
    for index, atom in enumerate(template):
        following = {}
        variable = is_variable(atom)
        last_end = len(tokens) - (len(template) - index - 1)
        for start, paths in states.items():
            if variable:
                ends = (end for end in range(start + 1, last_end + 1)
                        if _accepts(atom, tokens[start:end]))
            else:
                ends = (start + 1,) if start < len(tokens) and tokens[start] == atom else ()
            for end in ends:
                bucket = following.setdefault(end, [])
                for path in paths:
                    expanded = (*path, (index, start, end)) if variable else path
                    if expanded not in bucket and len(bucket) < 2:
                        bucket.append(expanded)
        states = following
        if not states:
            break
    return tuple(states.get(len(tokens), ()))


@dataclass(frozen=True)
class _Structure:
    identity: StructuralIdentity
    tokens: tuple[str, ...]


class Classifier:
    """A frozen-model classifier; construction and classification never learn."""

    def __init__(self, model: EmpiricalModel):
        if model.normalizer_revision != NORMALIZER_REVISION or model.recovery_revision != RECOVERY_REVISION:
            raise ValueError("classifier/model grammar identity mismatch")
        self.model = model
        self._sources = {}
        self._layers = {c.cluster_id: c.layers for c in model.clusters if c.layers is not None}
        for cluster in model.clusters:
            parts = self._sources.setdefault(cluster.source_family, {"whole": {}, "l1": {}, "l2": {}})
            structures = [("whole", cluster.template_tokens)]
            if cluster.layers is not None:
                structures.extend((("l1", cluster.layers.l1), ("l2", cluster.layers.l2)))
            for part, tokens in structures:
                candidate = _Structure(StructuralIdentity(model.revision_id, cluster.cluster_id, part), tokens)
                existing = parts[part].get(tokens)
                if existing is None or candidate.identity.cluster_id < existing.identity.cluster_id:
                    parts[part][tokens] = candidate

    def classify(self, diagnostic: RecoveredDiagnostic, view: NormalizedView) -> StructuralClassification:
        """Classify this exact child/view; return preserved values and assignments.

        Result.view may extend values with multi-token span values constructed
        from its token origins. Existing tokens, values and diagnostic survive.
        No second normalization, semantic interpretation or raw-text rematch.
        """
        if view.diagnostic is not diagnostic:
            raise ValueError("normalized view belongs to another diagnostic")
        if view.normalizer_revision != self.model.normalizer_revision:
            raise ValueError("normalized view/model identity mismatch")
        if diagnostic.recovery_revision != self.model.recovery_revision:
            raise ValueError("diagnostic/model recovery identity mismatch")
        tokens = tuple(t.text for t in view.tokens)
        parts = self._sources.get(diagnostic.parent.source_family)
        failures = []

        def result(outcome, assignments=()):
            identities = {}
            matches = []
            for structure, alignment, offset in assignments:
                identities[structure.identity.part] = structure.identity
                matches.extend((LearnedVariable(structure.identity, index, structure.tokens[index]),
                                TokenSpan(start + offset, end + offset))
                               for index, start, end in alignment)
            bound_view, bindings = bind_matched_spans(view, matches)
            return StructuralClassification(bound_view, self.model.revision_id, CLASSIFIER_REVISION,
                outcome, bindings=bindings, failures=tuple(failures), **identities)

        if parts is None:
            failures.append(StructuralFailure("whole", "unknown_source", "No learned source partition."))
            return result("unknown")

        def select(part, candidate_tokens, offset=0):
            exact = []
            ambiguous = False
            for structure in parts[part].values():
                alignments = _align(structure.tokens, candidate_tokens)
                if len(alignments) > 1:
                    ambiguous = True
                    failures.append(StructuralFailure(part, "ambiguous_positions",
                        "More than one complete variable alignment.", structure.identity))
                elif alignments:
                    exact.append((structure, alignments[0], offset))
            if len(exact) == 1 and not ambiguous:
                return exact[0]
            if len(exact) > 1:
                failures.append(StructuralFailure(part, "ambiguous_structure",
                    "Multiple different learned structures match exactly."))
            elif not exact and not ambiguous:
                failures.append(StructuralFailure(part, "no_exact_match", "No complete learned structure matches."))
            return None

        whole = select("whole", tokens)
        if whole is not None:
            structure, _, _ = whole
            learned_layers = self._layers.get(structure.identity.cluster_id)
            occurrence_layers = script_system_layers(tokens) if learned_layers else None
            if occurrence_layers is not None and tokens[-1] == "]":
                facts = []
                for part, learned, occurrence, offset in (
                    ("l1", learned_layers.l1, occurrence_layers[0], 0),
                    ("l2", learned_layers.l2, occurrence_layers[1], len(occurrence_layers[0]) + 1),
                ):
                    alignment = _align(learned, occurrence)
                    if len(alignment) == 1:
                        identity = StructuralIdentity(self.model.revision_id, structure.identity.cluster_id, part)
                        facts.append((_Structure(identity, learned), alignment[0], offset))
                if len(facts) == 2:
                    return result("full", (whole, *facts))
            return result("full", (whole,))
        layers = script_system_layers(tokens)
        if layers is None:
            return result("unknown")
        l1 = select("l1", layers[0])
        if l1 is None:
            return result("unknown")
        # Incomplete reasons and trailing material cannot prove a complete L2.
        # The independently validated outer envelope remains a successful L1.
        if not tokens or tokens[-1] != "]":
            failures.append(StructuralFailure("l2", "incomplete_reason",
                "Reason lacks a terminal closing bracket; only L1 is assigned."))
            return result("l1", (l1,))
        l2 = select("l2", layers[1], len(layers[0]) + 1)
        return result("l1_l2", (l1, l2)) if l2 is not None else result("l1", (l1,))
