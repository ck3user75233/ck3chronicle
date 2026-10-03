"""Strict JSON-compatible investigation queries; no expression language.

Fields within scope/refinement/selector objects are ANDed. Lists of template
references, exact identities, families and selectors are ORed. Binding predicates
are ANDed (each must match some binding). Text groups explicitly choose AND/OR.
Omitted fields impose no restriction; empty selector lists/groups are invalid.
"""
from copy import deepcopy
from dataclasses import dataclass, field
import json


class QueryError(ValueError):
    """The caller supplied an unsupported or contradictory query."""


def _object(value, allowed, label):
    if not isinstance(value, dict) or value.keys() - allowed:
        raise QueryError(f'{label}: expected object with fields {sorted(allowed)}')


def _string(value, label):
    if not isinstance(value, str) or not value:
        raise QueryError(f'{label}: nonempty string required')


def _integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise QueryError(f'{label}: integer >= {minimum} required')


def _list(value, label):
    if not isinstance(value, list) or not value:
        raise QueryError(f'{label}: nonempty list required; omit for unrestricted')


def validate_text(expression):
    if not isinstance(expression, dict):
        raise QueryError('text condition must be an object')
    if 'and' in expression or 'or' in expression:
        if len(expression) != 1:
            raise QueryError('a group must contain exactly one of and/or')
        children = next(iter(expression.values()))
        _list(children, 'text group')
        for child in children:
            validate_text(child)
        return
    _object(expression, {'contains', 'not_contains', 'case_sensitive'}, 'text condition')
    operations = expression.keys() & {'contains', 'not_contains'}
    if len(operations) != 1:
        raise QueryError('text condition requires exactly one contains/not_contains')
    _string(expression[next(iter(operations))], 'literal')
    if type(expression.get('case_sensitive', False)) is not bool:
        raise QueryError('case_sensitive must be boolean')


def evaluate_group(expression, contains, *, complete=True):
    """Shared AND/OR evaluator; None means unavailable absence evidence."""
    if expression is None:
        return True
    if 'and' in expression:
        values = [evaluate_group(child, contains, complete=complete) for child in expression['and']]
        return False if False in values else None if None in values else True
    if 'or' in expression:
        values = [evaluate_group(child, contains, complete=complete) for child in expression['or']]
        return True if True in values else None if None in values else False
    op = 'contains' if 'contains' in expression else 'not_contains'
    found = contains(expression[op], expression.get('case_sensitive', False))
    if not found and not complete:
        return None
    return found if op == 'contains' else not found


def evaluate_text(text: str, expression: dict | None) -> bool:
    """Evaluate a validated literal predicate. None means unrestricted."""
    return evaluate_group(expression, lambda literal, sensitive:
                          literal in text if sensitive else literal.casefold() in text.casefold())


SELECTOR_FIELDS = {'source_families', 'match_status', 'templates', 'identities',
                   'bindings', 'message', 'template_text', 'template_exact'}


def _selector(selector):
    _object(selector, SELECTOR_FIELDS, 'selector')
    if not selector:
        raise QueryError('empty selector is invalid; omit selectors for unrestricted')
    for name, value in selector.items():
        if name in {'message', 'template_text'}:
            validate_text(value)
        else:
            _list(value, name)
            for item in value:
                if name in {'source_families', 'match_status', 'template_exact'}:
                    _string(item, name)
                    if name == 'match_status' and item not in {'template', 'provisional'}:
                        raise QueryError('match_status must be template or provisional')
                elif name == 'templates':
                    _object(item, {'template_id', 'model_revision', 'contract_version'}, name)
                    if 'template_id' not in item:
                        raise QueryError('template reference requires template_id')
                    for part in item.values():
                        _string(part, name)
                elif name == 'identities':
                    _object(item, {'definition', 'equality'}, name)
                    if item.keys() != {'definition', 'equality'}:
                        raise QueryError('identity requires definition and full equality data')
                    _object(item['definition'], {'template_id', 'model_revision', 'contract_version'}, name)
                    if item['definition'].keys() != {'template_id', 'model_revision', 'contract_version'}:
                        raise QueryError('identity requires complete definition reference')
                    for part in item['definition'].values():
                        _string(part, name)
                    _object(item['equality'], {'template_id', 'regions'}, name)
                    if item['equality'].keys() != {'template_id', 'regions'}:
                        raise QueryError('identity requires contract equality data, not a digest')
                    _list(item['equality']['regions'], 'identity regions')
                    for region in item['equality']['regions']:
                        _object(region, {'name', 'layout', 'component_index', 'bindings'}, 'identity region')
                        if region.keys() != {'name', 'layout', 'component_index', 'bindings'}:
                            raise QueryError('incomplete identity region')
                        _string(region['name'], 'identity region name')
                        if not isinstance(region['layout'], dict) or not region['layout']:
                            raise QueryError('identity layout must be a nonempty object')
                        if region['component_index'] is not None:
                            _integer(region['component_index'], 'component_index')
                        if not isinstance(region['bindings'], list):
                            raise QueryError('identity bindings must be a list')
                        for binding in region['bindings']:
                            _object(binding, {'slot_id', 'type', 'value', 'present'}, 'identity binding')
                            if binding.keys() != {'slot_id', 'type', 'value', 'present'}:
                                raise QueryError('incomplete identity binding')
                            _string(binding['slot_id'], 'slot_id')
                            _string(binding['type'], 'binding type')
                            if type(binding['present']) is not bool or (
                                    binding['present'] and not isinstance(binding['value'], str)) or (
                                    not binding['present'] and binding['value'] is not None):
                                raise QueryError('invalid binding presence/value in identity')
                    # Validate structure by reusing the contract equality operation.
                    from ..pipeline.contracts import identity_data
                    try:
                        canonical = identity_data(item['equality'])
                    except (KeyError, TypeError) as exc:
                        raise QueryError('incomplete identity equality data') from exc
                    if canonical != item['equality'] or canonical['template_id'] != item['definition']['template_id']:
                        raise QueryError('identity must contain exact contract equality data')
                elif name == 'bindings':
                    _object(item, {'type', 'value', 'present', 'region', 'slot_id'}, name)
                    if 'type' not in item or 'value' not in item:
                        raise QueryError('binding requires type and exact value')
                    for key in ('type', 'region', 'slot_id'):
                        if key in item:
                            _string(item[key], key)
                    if type(item.get('present', True)) is not bool:
                        raise QueryError('binding present must be boolean')
                    if item.get('present', True):
                        if not isinstance(item['value'], str):
                            raise QueryError('present binding value must be a string')
                    elif item['value'] is not None:
                        raise QueryError('absent binding value must be null')


@dataclass
class InvestigationQuery:
    """Plain query sections. to_dict() validates and returns an independent copy.

    source is the 08A.2 extension boundary, never silently ignored. display.limit
    and historical_limit bound separate views, after complete totals/rollups.
    """
    scope: dict = field(default_factory=dict)
    refinement: dict = field(default_factory=dict)
    analytics: dict = field(default_factory=dict)
    display: dict = field(default_factory=dict)
    purpose: str = ''

    @classmethod
    def from_dict(cls, value: dict) -> 'InvestigationQuery':
        _object(value, {'scope', 'refinement', 'analytics', 'display', 'purpose'}, 'query')
        query = cls(**deepcopy(value))
        query.to_dict()
        return query

    def to_dict(self) -> dict:
        _object(self.scope, {'source_families', 'source'}, 'scope')
        if 'source_families' in self.scope:
            _selector({'source_families': self.scope['source_families']})
        if 'source' in self.scope:
            from .source_query import validate_source
            validate_source(self.scope['source'])
        _object(self.refinement, SELECTOR_FIELDS | {'selectors', 'occurrences', 'newly_observed'}, 'refinement')
        scalar = {k: v for k, v in self.refinement.items() if k in SELECTOR_FIELDS}
        if scalar:
            _selector(scalar)
        if 'selectors' in self.refinement:
            _list(self.refinement['selectors'], 'selectors')
            for selector in self.refinement['selectors']:
                _selector(selector)
        count = self.refinement.get('occurrences', {})
        _object(count, {'min', 'max'}, 'occurrences')
        for value in count.values():
            _integer(value, 'occurrences')
        if count.get('min', 0) > count.get('max', float('inf')):
            raise QueryError('occurrence minimum exceeds maximum')
        _object(self.analytics, {'history', 'trailing_runs', 'include_absent'}, 'analytics')
        for name in ('history', 'include_absent'):
            if type(self.analytics.get(name, True)) is not bool:
                raise QueryError(f'{name} must be boolean')
        if 'newly_observed' in self.refinement and type(self.refinement['newly_observed']) is not bool:
            raise QueryError('newly_observed must be boolean')
        if 'trailing_runs' in self.analytics:
            _integer(self.analytics['trailing_runs'], 'trailing_runs', 1)
        if not self.analytics.get('history', True) and (
                'trailing_runs' in self.analytics or 'newly_observed' in self.refinement
                or self.analytics.get('include_absent', False)):
            raise QueryError('history disabled but history-dependent option requested')
        _object(self.display, {'limit', 'historical_limit'}, 'display')
        for value in self.display.values():
            if value is not None:
                _integer(value, 'display limit')
        if not isinstance(self.purpose, str):
            raise QueryError('purpose must be text')
        result = deepcopy({'scope': self.scope, 'refinement': self.refinement,
                         'analytics': {'history': True, 'include_absent': self.analytics.get('history', True), **self.analytics},
                         'display': {'limit': None, 'historical_limit': None, **self.display},
                         'purpose': self.purpose})
        try:
            json.dumps(result, allow_nan=False)
        except (TypeError, ValueError) as exc:
            raise QueryError('query must contain JSON-compatible values') from exc
        return result
