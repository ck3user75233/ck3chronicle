"""Integrity-checked reader for a published native-message model, schema 4."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import types
from types import MappingProxyType
from typing import Mapping

from template_learning.parsers import ParserReference, SelectedParser, load_parser

from .matching import Rules

BASE_SLOT_TYPES = frozenset({'KEY', 'OPTIONAL_KEY', 'VALUE', 'LOCATOR', 'PARAM', 'REASON'})
SLOT_TYPES = BASE_SLOT_TYPES | {'CHARACTER_FULL_ID', 'HOUSE_FULL_ID', 'TITLE_FULL_ID'}
CONSTRAINTS = frozenset({'parser_boundaries', 'literal_punctuation', 'literal_guidance',
    'single_token', 'key_joiners', 'location_value', 'numeric_text', 'line_reference',
    'balanced_pairs', 'declared_field', 'full_id'})
ARTIFACTS = frozenset({'empirical_template_model.json', 'parser.py',
    'parser-manifest.json', 'owner_rules.json', 'native-validation.json', 'assignment.py', 'continuations.py'})


class ModelIntegrityError(ValueError):
    """Selected bytes or mutually pinned identities disagree."""


class ModelCompatibilityError(ValueError):
    """A release asks for semantics this reader cannot implement."""


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ModelIntegrityError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(payload: bytes):
    return json.loads(payload, object_pairs_hook=_object)


def _freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(v) for v in value)
    return value


def _require(condition, detail):
    if not condition:
        raise ModelCompatibilityError(detail)


def _strings(value):
    return isinstance(value, list) and all(isinstance(v, str) and v for v in value)


def _validate_rules(rules):
    _require((rules.get('schema'), rules.get('version')) ==
             ('ck3chronicle.learner-owner-rules', 1), 'unsupported owner-rule schema')
    declarations = rules['constructions']
    ids = [d['id'] for d in declarations]
    _require(len(ids) == len(set(ids)), 'duplicate construction ID')
    for declaration in declarations:
        compiled = re.compile(declaration['pattern'])
        names = set(compiled.groupindex)
        _require(set(declaration['region_order']) == names,
                 'construction regions disagree with named captures')
        _require((set(declaration['fields']) | set(declaration['comparison_regions'])) <= names,
                 'construction refers to an absent region')
        excluded = set(declaration.get('excludes', ()))
        _require(declaration['id'] not in excluded and excluded <= set(ids),
                 'invalid construction exclusions')
        _require(all(field['type'] in SLOT_TYPES for field in declaration['fields'].values()),
                 'unsupported declared field type')
        _require(all(type(field.get('allow_empty', False)) is bool
                     for field in declaration['fields'].values()),
                 'invalid declared empty-field permission')
    parameters = rules['parameter_structures']
    parameter_ids = [d['id'] for d in parameters]
    _require(len(parameter_ids) == len(set(parameter_ids)), 'duplicate parameter structure ID')
    for definition in parameters:
        mechanic = definition['mechanic']
        _require(mechanic in {'line_sequence', 'balanced_interior', 'through_balanced_suffix', 'full_id'},
                 'unsupported parameter structure mechanic')
        if mechanic == 'full_id':
            continue  # Shared FullIdRules validates these declarations below.
        re.compile(definition['prefix'])
        if mechanic == 'line_sequence':
            re.compile(definition['content'])
        else:
            _require(_strings(definition['delimiters']) and len(definition['delimiters']) == 2,
                     'invalid declared delimiters')
            if mechanic == 'through_balanced_suffix':
                re.compile(definition['content_required'])
    cues = rules['slot_position_cues']
    _require(type(cues['case_sensitive']) is bool and _strings(cues['filename_suffixes']),
             'invalid location cues')
    # Compile all executable declarations before loading parser code.
    Rules(rules)


def _validate_template(template, declarations, parameter_ids, *, source=None, context=None):
    _require(re.fullmatch(r'[0-9a-f]{24}', template['template_id']) is not None, 'invalid template ID')
    _require(isinstance(template['source_family'], str) and template['source_family'],
             'template requires a source family')
    _require(template['status'] in {'supported', 'confirmed', 'provisional', 'unresolved'},
             'unsupported template support status')
    if source is not None:
        _require(template['source_family'] == source and template['context_kind'] == context,
                 'wrapper pattern source/context disagreement')
    else:
        _require(template['context_kind'] in {'body', 'located-message-wrapper'} or template['context_kind'].startswith('continuation:'),
                 'unsupported template context')
    construction = template['construction_id']
    _require(construction is None or construction in declarations, 'unknown construction reference')
    if construction is not None:
        _require(declarations[construction]['source'] == template['source_family'],
                 'construction source disagreement')
    _require(isinstance(template['parameter_structures'], list) and
             set(template['parameter_structures']) <= set(parameter_ids), 'unknown parameter structure')
    _require(isinstance(template['parts'], list) and template['parts'], 'empty template parts')
    names = set()
    for part in template['parts']:
        if part['kind'] == 'literal':
            _require(set(part) == {'kind', 'text'} and isinstance(part['text'], str),
                     'invalid literal part')
            continue
        _require(part['kind'] == 'slot' and
                 set(part) == {'kind', 'name', 'type', 'optional', 'prefix', 'suffix', 'constraints'},
                 'unsupported native part representation')
        _require(isinstance(part['name'], str) and part['name'] and part['name'] not in names,
                 'duplicate or invalid slot name')
        names.add(part['name'])
        _require(part['type'] in SLOT_TYPES, 'unsupported slot type')
        _require(type(part['optional']) is bool, 'invalid slot optionality')
        _require(isinstance(part['prefix'], str) and isinstance(part['suffix'], str),
                 'invalid slot prefix/suffix')
        constraints = part['constraints']
        _require(isinstance(constraints, dict) and not set(constraints) - CONSTRAINTS,
                 'unsupported slot constraint')
        _require(constraints.get('parser_boundaries') is True, 'raw parser boundaries are required')
        for key in ('literal_punctuation', 'single_token', 'location_value', 'numeric_text', 'line_reference'):
            if key in constraints:
                _require(type(constraints[key]) is bool, f'invalid {key} constraint')
        for key in ('literal_guidance', 'key_joiners'):
            if key in constraints:
                _require(_strings(constraints[key]), f'invalid {key} constraint')
        if 'balanced_pairs' in constraints:
            pairs = constraints['balanced_pairs']
            _require(isinstance(pairs, list) and all(_strings(p) and len(p) == 2 for p in pairs),
                     'invalid balance constraint')
            _require(len({p[0] for p in pairs}) == len(pairs), 'duplicate balance opener')
        field = constraints.get('declared_field')
        if field is not None:
            _require(isinstance(field, dict) and set(field) == {'construction', 'field'},
                     'invalid declared field reference')
            _require(field['construction'] == construction and construction in declarations,
                     'slot construction disagreement')
            declared = declarations[construction]['fields'].get(field['field'])
            _require(declared is not None and declared['type'] == part['type'],
                     'slot declared field/type disagreement')
        if part['type'] == 'REASON':
            _require(field is not None, 'REASON requires a declared field')
        full_id = constraints.get('full_id')
        if full_id is not None:
            _require(isinstance(full_id, dict) and set(full_id) == {'definition', 'source'},
                     'invalid full-ID constraint')
            definition = parameter_ids.get(full_id['definition'])
            _require(definition is not None and definition['mechanic'] == 'full_id',
                     'unknown full-ID structure')
            _require(definition['slot_type'] == part['type'] and not part['optional']
                     and not part['prefix'] and not part['suffix'], 'full-ID type/boundary disagreement')
            _require(full_id['definition'] in template['parameter_structures']
                     and full_id['source'] == template['source_family']
                     and any(c['source'] == full_id['source'] for c in definition['contexts']),
                     'full-ID emitter disagreement')
        if part['type'] in {'CHARACTER_FULL_ID', 'HOUSE_FULL_ID', 'TITLE_FULL_ID'}:
            _require(full_id is not None, 'full-ID slot requires structural recognition')
    contexts = template['context_patterns']
    expected = {'prefix', 'suffix'} if template['context_kind'] == 'located-message-wrapper' else set()
    _require(isinstance(contexts, dict) and set(contexts) == expected, 'incomplete wrapper patterns')
    for name, patterns in contexts.items():
        _require(isinstance(patterns, list) and patterns, 'empty wrapper alternatives')
        _require(len({p['template_id'] for p in patterns}) == len(patterns), 'duplicate wrapper alternative')
        for pattern in patterns:
            _validate_template(pattern, declarations, parameter_ids,
                               source=template['source_family'], context='context:' + name)


@dataclass(frozen=True)
class EmpiricalModel:
    revision_id: str
    manifest_sha256: str
    data: Mapping
    parser: SelectedParser
    templates_by_source: Mapping
    select_assignment: object
    match_components: object

    @property
    def templates(self):
        return self.data['templates']


def load_model(folder: str | Path, *, expected_manifest_sha256: str) -> EmpiricalModel:
    """Load one complete pinned release; never reinterpret an older schema."""
    folder = Path(folder).resolve()
    manifest_bytes = (folder / 'manifest.json').read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != expected_manifest_sha256:
        raise ModelIntegrityError('selected manifest SHA-256 mismatch')
    try:
        manifest = read_json(manifest_bytes)
        _require((manifest.get('schema'), manifest.get('schema_version')) ==
                 ('ck3chronicle.native-model-release', 1), 'unsupported native release')
        _require(set(manifest['hashes']) == ARTIFACTS, 'incomplete release artifact set')
        payloads = {}
        for name, digest in manifest['hashes'].items():
            payload = (folder / name).read_bytes()
            if hashlib.sha256(payload).hexdigest() != digest:
                raise ModelIntegrityError(f'selected artifact SHA-256 mismatch: {name}')
            payloads[name] = payload
        data = read_json(payloads['empirical_template_model.json'])
        _require((data.get('schema'), data.get('schema_version'), data.get('status'),
                  data.get('record_scope')) == ('ck3chronicle.native-message-model', 4, 'published', 'message'),
                 'unsupported published model schema/status/scope')
        canonical = json.dumps({k: v for k, v in data.items() if k != 'revision_id'},
                               ensure_ascii=True, sort_keys=True, separators=(',', ':')).encode()
        revision = hashlib.sha256(canonical).hexdigest()[:24]
        if revision != data['revision_id'] or revision != manifest['revision_id']:
            raise ModelIntegrityError('model/manifest revision identity disagreement')
        reference = read_json(payloads['parser-manifest.json'])
        if (reference != data['parser'] or reference != manifest['parser'] or
                reference['artifact'] != 'parser.py' or reference['sha256'] != manifest['hashes']['parser.py']):
            raise ModelIntegrityError('release parser disagreement')
        rules = read_json(payloads['owner_rules.json'])
        if rules != data['owner_rules'] or rules['constructions'] != data['constructions']:
            raise ModelIntegrityError('release declaration disagreement')
        declared_types = {d['slot_type'] for d in rules['parameter_structures'] if d['mechanic'] == 'full_id'}
        _require(set(data['slot_definitions']) == BASE_SLOT_TYPES | declared_types
                 and declared_types <= SLOT_TYPES, 'unsupported slot definitions')
        _validate_rules(rules)
        declarations = {d['id']: d for d in rules['constructions']}
        parameter_ids = {d['id']: d for d in rules['parameter_structures']}
        _require(len({t['template_id'] for t in data['templates']}) == len(data['templates']),
                 'duplicate template ID')
        for template in data['templates']:
            _validate_template(template, declarations, parameter_ids)
        # Hash-verified, standalone artifacts: no mutable learner policy imports.
        selector = types.ModuleType('ck3_release_assignment_' + revision)
        exec(compile(payloads['assignment.py'],str(folder/'assignment.py'),'exec'),selector.__dict__)
        components = types.ModuleType('ck3_release_components_' + revision)
        exec(compile(payloads['continuations.py'],str(folder/'continuations.py'),'exec'),components.__dict__)
        _require(data['assignment_policy']['version'] == selector.POLICY_VERSION,
                 'assignment policy version disagreement')
        component_rules = {r['id']:r for r in rules['continuation_structures']}
        for template in data['templates']:
            contract = template['continuation']
            components.validate_contract(contract)
            grouped = template['context_kind'].startswith('continuation:')
            _require(bool(contract) == grouped or template['status']=='unresolved',
                     'continuation template requires its complete component contract')
            if contract:
                rule = component_rules.get(contract['rule_id'])
                _require(rule is not None and rule['source']==template['source_family'] and
                         'continuation:'+rule['recovery_structure']==template['context_kind'],
                         'component source/recovery disagreement')
                _require(all(contract[k]==rule[k] for k in ('reference_type','value_type','minimum_entries')) and
                         all(v['label']==rule['label'] for v in contract['layouts']),
                         'component declaration disagreement')
                _require(any(p.get('name')==contract['opening_slot'] and p.get('type')==contract['reference_type']
                             for p in template['parts']), 'missing opening reference slot')
        frozen = _freeze(data)
        by_source = {}
        for template in frozen['templates']:
            by_source.setdefault(template['source_family'], []).append(template)
        # All artifact hashes and executable declarations have passed before exec.
        parser = load_parser(ParserReference(reference['version'], (folder / 'parser.py').as_uri(),
                                             reference['sha256']))
        return EmpiricalModel(revision, expected_manifest_sha256, frozen, parser,
                              MappingProxyType({s: tuple(v) for s, v in by_source.items()}),
                              selector.select_assignment, components.match_components)
    except (KeyError, TypeError, re.error) as exc:
        raise ModelCompatibilityError(f'invalid native model: {exc}') from exc
