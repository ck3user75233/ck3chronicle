"""Validate the shared model contract before native matching.

Structural checks follow the current schema-5 reader contract; no pipeline
imports, inference, current-rule globals or semantic classification.
"""
import math
import re
from .assignment import POLICY_VERSION
from .continuations import validate_contract
from .matching_primitives import (Rules, SLOT_TYPES, pattern_identity,
    MatcherDeclarationError, MatcherCompatibilityError)
CONSTRAINTS = frozenset({'parser_boundaries', 'literal_punctuation', 'literal_guidance',
    'single_token', 'key_joiners', 'location_value', 'numeric_text', 'line_reference',
    'balanced_pairs', 'declared_field', 'full_id'})


def _require(condition, detail):
    if not condition:
        raise MatcherDeclarationError(detail)


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


def _validate_template(template, declarations, parameter_ids, label_groups, *, source=None, context=None):
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
    for index, part in enumerate(pattern_identity(template['parts'])):
        if part['kind']=='repeat':
            from .location_sequences import validate
            validate(part)
            _require(index==len(template['parts'])-1,'repeated locations must end the body')
            continue
        if part['kind'] == 'literal':
            if 'alternatives' in part:
                _require(set(part) == {'kind', 'text', 'alternatives', 'location_label'},
                         'invalid literal choice representation')
                declared = label_groups.get(part['location_label'], {}).get('literal_alternatives')
                forms = part['alternatives']
                _require(_strings(forms) and len(forms) > 1 and forms == declared
                         and part['text'] == forms[0], 'literal choices differ from declared labels')
                _require(all(not a.startswith(b) for i, a in enumerate(forms)
                             for j, b in enumerate(forms) if i != j),
                         'literal choices must be distinct and prefix-free')
                following = template['parts'][index+1:]
                if following and following[0]['kind'] == 'literal':
                    _require(set(following[0]) == {'kind', 'text'}
                             and not following[0]['text'].strip(' \t'),
                             'location label must immediately introduce its field')
                    following = following[1:]
                _require(bool(following) and following[0].get('type') == 'LOCATOR'
                         and following[0]['constraints'].get('location_value') is True
                         and not following[0]['optional'],
                         'line label alternatives require a complete LOCATOR')
                continue
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
            _validate_template(pattern, declarations, parameter_ids, label_groups,
                               source=template['source_family'], context='context:' + name)


def validate_model(data):
    """Validate supplied published or unpublished schema-5 model declarations."""
    try:
        if (data['schema'], data['schema_version'], data['record_scope']) != (
                'ck3chronicle.native-message-model', 6, 'message'):
            raise MatcherCompatibilityError('unsupported native model schema')
        if data['parser']['version'] != 'ck3-lossless-v1.7':
            raise MatcherCompatibilityError('unsupported pinned parser')
        policy = data['assignment_policy']
        if policy['version'] != POLICY_VERSION:
            raise MatcherCompatibilityError('unsupported assignment policy')
        rules = data['owner_rules']
        _require(data['constructions'] == rules['constructions'], 'construction declarations disagree')
        _require(policy == rules['assignment_policy'], 'selector declarations disagree')
        _require(set(data['slot_definitions']) == set(SLOT_TYPES), 'unsupported slot definitions')
        _validate_rules(rules)
        declarations = {d['id']: d for d in rules['constructions']}
        parameters = {d['id']: d for d in rules['parameter_structures']}
        labels = {d['id']: d for d in rules['location_label_equivalences']['groups']}
        _require(len({t['template_id'] for t in data['templates']}) == len(data['templates']),
                 'duplicate template ID')
        _require(bool(policy['metrics']), 'empty selection metrics')
        for metric in policy['metrics']:
            _require(metric['direction'] in {'min', 'max'} and
                     type(metric['include_wrappers']) is bool, 'invalid selection metric')
        component_rules = {r['id']: r for r in rules['continuation_structures']}
        for template in data['templates']:
            _validate_template(template, declarations, parameters, labels)
            for pattern in [template, *[p for pool in template['context_patterns'].values() for p in pool]]:
                for metric in policy['metrics']:
                    value = pattern['selection_evidence'][metric['field']]
                    _require(type(value) in {int, float} and math.isfinite(value) and value >= 0,
                             'invalid or missing selection evidence')
            contract = template['continuation']
            validate_contract(contract)
            grouped = template['context_kind'].startswith('continuation:')
            _require(bool(contract) == grouped or template['status'] == 'unresolved',
                     'continuation template requires a complete component contract')
            if contract:
                rule = component_rules.get(contract['rule_id'])
                _require(rule is not None and rule['source'] == template['source_family'] and
                         'continuation:' + rule['recovery_structure'] == template['context_kind'],
                         'component source/recovery disagreement')
                _require(all(contract[k] == rule[k] for k in ('reference_type', 'value_type', 'minimum_entries'))
                         and all(v['label'] == rule['label'] for v in contract['layouts']),
                         'component declaration disagreement')
                _require(any(p.get('name') == contract['opening_slot'] and
                             p.get('type') == contract['reference_type'] for p in template['parts']),
                         'missing opening reference slot')
    except (MatcherDeclarationError, MatcherCompatibilityError):
        raise
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise MatcherDeclarationError(f'invalid model declaration: {exc}') from exc

