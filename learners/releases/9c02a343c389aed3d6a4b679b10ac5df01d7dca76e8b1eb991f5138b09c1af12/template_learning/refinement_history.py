"""Creation-time refinement lineage: parents are references, children are deltas.

No content hashing or equality search is used to discover shared evidence. A split
creates its observation once; its children refer to that very same event.
"""
from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class Refinement:
    parents: tuple
    delta: dict


def refine(parents, **delta):
    return [Refinement(tuple(parents), delta)]


def merge(clusters, **delta):
    return refine((head for cluster in clusters for head in cluster.refinements), **delta)


def encode_history(model, previous=None):
    """Assign build-local sequential IDs once; never expand ancestor histories.

    Existing same-version IDs survive additive builds. Object identity tracks
    already visited events, not equal contents. Only reachable new events persist.
    """
    table = dict(previous or {})
    seen = {}

    def event(node):
        key = id(node)
        if key in seen:
            return seen[key]
        parents = [event(parent) for parent in node.parents]
        name = f'r{len(table) + 1}'
        table[name] = dict(parents=parents, delta=node.delta)
        seen[key] = name
        return name

    def visit(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == 'inference_refinements':
                    value[key] = [event(node) if isinstance(node, Refinement) else node for node in child]
                else:
                    visit(child)
        elif isinstance(value, (list, tuple)):
            for child in value:
                visit(child)

    visit(model)
    model['refinement_history'] = table
    validate_history(model)


def validate_history(model):
    table = model['refinement_history']
    visited, visiting = set(), set()

    def check(key):
        if key in visited:
            return
        if key in visiting or key not in table:
            raise ValueError('invalid refinement parent reference: ' + str(key))
        visiting.add(key)
        for parent in table[key]['parents']:
            check(parent)
        visiting.remove(key)
        visited.add(key)

    def visit(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key == 'inference_refinements':
                    for reference in child:
                        check(reference)
                elif key != 'refinement_history':
                    visit(child)
        elif isinstance(value, (list, tuple)):
            for child in value:
                visit(child)

    for key in table:
        check(key)
    visit(model)


def history_events(model, references):
    """Review one lineage once, in parent-first order; never duplicate ancestors."""
    seen = set()

    def visit(key):
        if key in seen:
            return
        seen.add(key)
        node = model['refinement_history'][key]
        for parent in node['parents']:
            yield from visit(parent)
        yield dict(refinement_id=key, **node)

    for key in references:
        yield from visit(key)
