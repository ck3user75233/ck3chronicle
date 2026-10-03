"""Retire fixed KEY observations without re-inferring or broadening a template."""
from collections import defaultdict
import json

from template_learning.matching_primitives import pattern_identity
from template_learning.records import identity
from template_learning.matching_defaults import RULES
from template_learning.owner_rules import OWNER_RULES


def shape(parts):
    result = []
    for part in pattern_identity(parts):
        part = {k: v for k, v in part.items() if k != 'name'}
        if (part['kind'] == 'literal' and result and result[-1]['kind'] == 'literal'
                and 'alternatives' not in part and 'alternatives' not in result[-1]):
            result[-1]['text'] += part['text']
        elif part.get('text') != '':
            result.append(part)
    return result


def context_shape(template):
    return {name: sorted(json.dumps(shape(p['parts']), sort_keys=True) for p in patterns)
            for name, patterns in template['context_patterns'].items()}


def fixed_fields(general, narrow, general_match, narrow_match):
    """Prove symbolic specialization, not merely successful native coverage."""
    policy=OWNER_RULES['assignment_policy']['retirement']
    narrow_spans = [c['span'] for c in narrow_match['captures'] if c['span'] is not None]
    captures = {c['name']: c for c in general_match['captures']}
    replacement, fixed = [], {}
    for part in general['parts']:
        if part['kind'] in {'literal','repeat'}:
            replacement.append(part)
            continue
        capture = captures[part['name']]
        span = capture['span']
        overlaps = span is not None and any(a < span[1] and span[0] < b for a,b in narrow_spans)
        if overlaps or part['type'] not in policy['field_types']:
            replacement.append(part)
            continue
        diversity = len(part['observed_values']) + bool(part.get('observed_absence'))
        if diversity < policy['minimum_distinct_values_or_absence']:
            replacement.append(part)
            continue
        value = capture['value']
        fixed[part['name']] = value
        replacement.append(dict(kind='literal', text='' if value is None else
                                part['prefix'] + value + part['suffix']))
    return fixed if fixed and shape(replacement) == shape(narrow['parts']) else None


def retire_fixed_observations(templates, records, *, protected_template_ids=()):
    members = {identity(r.key): r for r in records}
    decisions, superseded = [], {}
    by_structure = defaultdict(list)
    for t in templates:
        key = (t['source_family'], t['context_kind'], t['construction_id'],
               tuple(t['parameter_structures']), json.dumps(context_shape(t), sort_keys=True))
        by_structure[key].append(t)
    for pool in by_structure.values():
        slot_count = lambda t: sum(p['kind']=='slot' for p in t['parts'])
        for narrow in sorted(pool, key=lambda t: (slot_count(t), t['template_id'])):
            if narrow['status']=='unresolved' or narrow['template_id'] in protected_template_ids:
                continue
            native = [members[rid] for rid in narrow['evidence_record_ids']]
            if not native:
                continue
            old = RULES.match_record(narrow, native[0])
            if old is None:
                continue
            options = []
            for general in pool:
                if general['status'] != 'supported' or slot_count(general) <= slot_count(narrow):
                    continue
                first = RULES.match_record(general, native[0])
                if first is None:
                    continue
                fixed = fixed_fields(general, narrow, first, old)
                if not fixed:
                    continue
                for record in native[1:]:
                    gm, nm = RULES.match_record(general, record), RULES.match_record(narrow, record)
                    if gm is None or nm is None or fixed_fields(general,narrow,gm,nm) != fixed:
                        break
                else:
                    options.append((general, fixed))
            if options:
                options.sort(key=lambda pair: (-slot_count(pair[0]),
                    -pair[0]['selection_evidence']['independent_examples'], pair[0]['template_id']))
                general, fixed = options[0]
                superseded[narrow['template_id']] = general['template_id']
                decisions.append(dict(retired_template_id=narrow['template_id'],
                    selected_template_id=general['template_id'], source=narrow['source_family'],
                    reason='fixed observation inside independently established KEY field',
                    fixed_fields=fixed, evidence_record_ids=narrow['evidence_record_ids'],
                    native_examples=len(native), occurrences=narrow['support_occurrences'],
                    retired_template=narrow))
    for decision in decisions:
        target = decision['selected_template_id']
        while target in superseded:
            target = superseded[target]
        decision['selected_template_id'] = target
    return [t for t in templates if t['template_id'] not in superseded], decisions
