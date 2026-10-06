"""Serializable Error Contract definitions/values, exact identity and rendering.

No parser, model loader, matcher or original log is needed to render. Preparation
consumes completed bindings and checks correspondence only; aggregation is later.
"""
from copy import deepcopy
import hashlib
import json
import re

from .domain import NativeClassification, ResultIntegrityError

CONTRACT_VERSION = 'error-contract-v1'


def materialize_definitions(package) -> dict[str, dict]:
    """Copy published render declarations once, keyed by existing template ID."""
    definitions = {}
    for template in package.data['templates']:
        definitions[template['template_id']] = {
            'contract_version': CONTRACT_VERSION,
            'model_revision': package.manifest['model_revision_id'],
            **{key: deepcopy(template[key]) for key in (
                'template_id', 'source_family', 'context_kind', 'construction_id',
                'parameter_structures', 'parts', 'continuation')},
            'context_patterns': {name: [
                {key: deepcopy(pattern[key]) for key in ('template_id', 'parts')}
                for pattern in patterns]
                for name, patterns in template['context_patterns'].items()},
        }
    return definitions


def _require(condition, message):
    if not condition:
        raise ResultIntegrityError(message)


def _parts(definition, region):
    layout = region['layout']
    _require(layout['template_id'] == definition['template_id'], 'layout template differs')
    name = region['name']
    if name == 'body':
        _require({k: v for k, v in layout.items() if k not in {'literal_choices','repeat_choices'}} ==
                 {'template_id': definition['template_id'], 'region': 'body'},
                 'invalid body layout')
        return _literal_parts(_repeat_parts(definition['parts'], layout), layout)
    if name in ('prefix', 'suffix'):
        _require(layout['region'] == name, 'wrapper region differs')
        patterns = [p for p in definition['context_patterns'][name]
                    if p['template_id'] == layout['wrapper_template_id']]
        _require(len(patterns) == 1, 'wrapper choice is not in definition')
        return _literal_parts(patterns[0]['parts'], layout)
    _require(layout['region'] == 'continuation', 'invalid component layout')
    index = layout['layout_index']
    contract = definition['continuation']
    _require(type(index) is int and 0 <= index < len(contract['layouts']),
             'component layout index is not in definition')
    selected = contract['layouts'][index]
    return [
        {'kind': 'literal', 'text': selected['leading']},
        {'kind': 'slot', 'name': 'reference', 'type': contract['reference_type'],
         'optional': False, 'prefix': '', 'suffix': ''},
        {'kind': 'literal', 'text': selected['label']},
        {'kind': 'slot', 'name': 'value', 'type': contract['value_type'],
         'optional': False, 'prefix': '', 'suffix': ''},
        {'kind': 'literal', 'text': selected['trailing']},
    ]


def _repeat_parts(parts, layout):
    """Render selected repeated-entry layouts, without recognizing source text."""
    repeats = [p for p in parts if p['kind']=='repeat']
    choices = layout.get('repeat_choices', [])
    if not repeats:
        _require(not choices, 'repeat choices without a repeated definition')
        return parts
    _require(len(repeats)==1 and parts[-1] is repeats[0], 'invalid repeated definition placement')
    part = repeats[0]
    _require(part['structure']=='location_entries' and isinstance(choices,list)
             and len(choices)>=part['minimum'], 'incomplete location-entry choices')
    result = deepcopy(parts[:-1])
    for index, choice in enumerate(choices):
        _require(type(choice) is int and 0 <= choice < len(part['layouts']), 'invalid location-entry choice')
        for child in deepcopy(part['layouts'][choice]):
            if child['kind']=='slot':
                child['name']=part['name']+'_'+str(index)+'_'+child['name']
            result.append(child)
    return result


def _literal_parts(parts, layout):
    """Resolve explicit layout choices only; never match or normalize text."""
    expected = [i for i, p in enumerate(parts) if 'alternatives' in p or 'literal_format' in p]
    choices = layout.get('literal_choices', [])
    _require(isinstance(choices, list) and all(isinstance(c, list) and len(c) == 2
             and type(c[0]) is int and type(c[1]) in (int, str) for c in choices), 'invalid literal choices')
    _require([i for i, _ in choices] == expected, 'incomplete or unordered literal choices')
    selected = dict(choices)
    result = []
    for index, part in enumerate(parts):
        if index in selected:
            choice = selected[index]
            if 'literal_format' in part:
                _require(isinstance(choice, str) and re.fullmatch(part['format_pattern'], choice) is not None,
                         'literal spelling does not conform to declared format')
                result.append({'kind': 'literal', 'text': choice})
            else:
                _require(type(choice) is int and 0 <= choice < len(part['alternatives']), 'literal choice is not in definition')
                result.append({'kind': 'literal', 'text': part['alternatives'][choice]})
        else:
            result.append(part)
    return result


def _checked_regions(definition, values):
    """Structural correspondence, not model-semantic validation or matching."""
    try:
        _require(definition['contract_version'] == values['contract_version'] == CONTRACT_VERSION,
                 'unsupported contract rules')
        _require(definition['template_id'] == values['template_id'], 'value template differs')
        regions = values['regions']
        contexts = ['prefix', 'suffix'] if definition['context_kind'] == 'located-message-wrapper' else []
        components = regions[1 + len(contexts):]
        names = ['body', *contexts, *('continuation:' + str(i) for i in range(len(components)))]
        _require([r['name'] for r in regions] == names, 'incomplete or unordered regions')
        contract = definition['continuation']
        _require(len(components) >= contract['minimum_entries'] if contract else not components,
                 'incomplete component data')
        for index, region in enumerate(regions):
            component_index = index - 1 - len(contexts) if index > len(contexts) else None
            _require(region['component_index'] == component_index, 'component order differs')
            parts = _parts(definition, region)
            slots = [p for p in parts if p['kind'] == 'slot']
            bindings = region['bindings']
            _require([(p['name'], p['type']) for p in slots] ==
                     [(b['slot_id'], b['type']) for b in bindings], 'ordered slots differ from layout')
            for slot, binding in zip(slots, bindings):
                _require(type(binding['present']) is bool, 'presence must be explicit')
                if binding['present']:
                    _require(isinstance(binding['value'], str), 'present value must be exact text')
                else:
                    _require(slot['optional'] and binding['value'] is None, 'invalid absent value')
            yield region, parts
    except (KeyError, TypeError, IndexError) as exc:
        raise ResultIntegrityError('incomplete contract data: ' + str(exc)) from exc


def prepare_record(definition: dict, result: NativeClassification) -> dict:
    """Prepare one eligible complete assignment; never read or bind native bytes."""
    try:
        _require(isinstance(result, NativeClassification) and result.selected is not None,
                 'record preparation requires a selected assignment')
        selected = result.selected
        _require(selected.match_status in {'template', 'provisional'}, 'invalid final status')
        _require(definition['model_revision'] == result.model_revision, 'definition revision differs')
        _require(definition['source_family'] == result.diagnostic.source_family and
                 definition['context_kind'] == result.diagnostic.unit['context_kind'],
                 'definition/input correspondence differs')
        values = {'contract_version': CONTRACT_VERSION, 'template_id': selected.template_id,
                  'regions': [
                      {'name': region.name, 'layout': deepcopy(region.layout),
                       'component_index': region.component_index,
                       'bindings': [{'slot_id': b.slot_id, 'type': b.type,
                                     'value': b.value, 'present': b.present} for b in region.bindings]}
                      for region in selected.regions]}
        list(_checked_regions(definition, values))
        provenance = deepcopy(result.diagnostic.provenance)
        _require(bool(provenance.get('emission_ordinals')) and bool(provenance.get('ordered_spans')),
                 'representative occurrence requires original emission provenance')
        provenance['regions'] = []
        for region in selected.regions:
            spans = []
            for binding in region.bindings:
                _require(binding.present == (binding.span is not None), 'binding presence/span differs')
                _require(binding.span is None or region.span.contains(binding.span),
                         'binding span lies outside representative region')
                spans.append([binding.span.start, binding.span.end] if binding.span else None)
            provenance['regions'].append({'name': region.name, 'span': [region.span.start, region.span.end],
                                          'binding_spans': spans})
        return {'values': values, 'match_status': selected.match_status, 'error_type': 'unknown',
                'occurrence_count': 1, 'provenance': provenance}
    except (KeyError, TypeError, AttributeError) as exc:
        raise ResultIntegrityError('incomplete completed assignment: ' + str(exc)) from exc


def identity_data(values: dict) -> dict:
    """Full deterministic equality data, scoped to one Run's definition revision.

    Use the full data for equality; the digest is only an index. Timestamp,
    provenance, source and final support status do not split equal errors.
    """
    return {'template_id': values['template_id'], 'regions': [
        {'name': r['name'], 'layout': deepcopy(r['layout']), 'component_index': r['component_index'],
         'bindings': [{k: b[k] for k in ('slot_id', 'type', 'value', 'present')}
                      for b in r['bindings']]} for r in values['regions']]}


def identity_digest(values: dict) -> str:
    encoded = json.dumps(identity_data(values), sort_keys=True, ensure_ascii=True,
                         separators=(',', ':')).encode('ascii')
    return hashlib.sha256(encoded).hexdigest()


def _rendered_regions(definition, values):
    """One rendering path for text and its stored literal/slot provenance."""
    rendered = {}
    for region, parts in _checked_regions(definition, values):
        bindings = iter(region['bindings'])
        segments = []

        def append(text, kind='literal', **origin):
            if text:
                segments.append(dict(text=text, kind=kind, region=region['name'], **origin))

        for part in parts:
            if part['kind'] == 'literal':
                append(part['text'])
            else:
                binding = next(bindings)
                if binding['present']:
                    append(part['prefix'])
                    append(binding['value'], 'slot', slot_id=binding['slot_id'], type=binding['type'])
                    append(part['suffix'])
        rendered[region['name']] = segments
    order = ['prefix', 'body', 'suffix'] if 'prefix' in rendered else ['body']
    order.extend(r['name'] for r in values['regions'] if r['component_index'] is not None)
    return [(name, rendered[name]) for name in order]


def render_regions(definition: dict, values: dict) -> list[tuple[str, str]]:
    """Exact original region text in framing order, from JSON-compatible data."""
    return [(name, ''.join(s['text'] for s in segments))
            for name, segments in _rendered_regions(definition, values)]


def render_segments(definition: dict, values: dict) -> list[dict]:
    """Rendered text segments with character offsets and stored literal/slot origin.

    Offsets are Python character indices, end-exclusive, in render()'s output.
    This exposes the existing assignment; it does not match or classify text.
    """
    result, offset = [], 0
    for _, segments in _rendered_regions(definition, values):
        for segment in segments:
            end = offset + len(segment['text'])
            result.append(dict(segment, start=offset, end=end))
            offset = end
    return result


def render(definition: dict, values: dict) -> str:
    """Render one complete error without log-header timestamps or extra separators."""
    return ''.join(text for _, text in render_regions(definition, values))


def run_lineage(package, *, application_revision: str) -> dict:
    """Processing fields for later Run metadata; storage owns its schema version."""
    from .classifier import CLASSIFIER_REVISION

    _require(isinstance(application_revision, str) and bool(application_revision),
             'explicit application revision required')
    manifest = package.manifest
    return {'contract_version': CONTRACT_VERSION, 'model_revision': manifest['model_revision_id'],
            'package_id': manifest['package_id'], 'package_manifest_sha256': package.manifest_sha256,
            'parser': deepcopy(manifest['parser']), 'matcher_api_version': manifest['matcher_api_version'],
            'selector_version': manifest['selector_version'],
            'classifier_revision': CLASSIFIER_REVISION, 'application_revision': application_revision}
