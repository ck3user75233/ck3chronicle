"""Shared model-backed matching of parser-recovered supporting components.

No lexer, recovery heuristics, name recognition or mutable owner-rule imports.
Every range is relative to its original component body, never a joined display.
"""


def native_layout(entry):
    raw = entry['text'].encode('utf-8', 'surrogateescape')
    if ''.join(v for _, v in entry['pieces']) != entry['text']:
        raise ValueError('continuation pieces do not reproduce native body')
    boundaries, cursor = {0}, 0
    for _, value in entry['pieces']:
        cursor += len(value.encode('utf-8', 'surrogateescape'))
        boundaries.add(cursor)
    a, b = entry['prefix_span']
    c, d = entry['label_span']
    e, f = entry['value_span']
    if not (0 <= a < b <= c < d == e < f <= len(raw)):
        raise ValueError('invalid continuation partition')
    if not {a, b, c, d, e, f} <= boundaries:
        raise ValueError('continuation range cuts a raw parser piece')
    decode = lambda value: value.decode('utf-8', 'surrogateescape')
    # Parser label_span excludes possessive framing before "title:". Preserve
    # that framing in the literal between the reference and value as well.
    return dict(leading=decode(raw[:a]), label=decode(raw[b:e]), trailing=decode(raw[f:])), decode(raw[a:b]), decode(raw[e:f])


def match_components(contract, entries, opening_captures):
    """Validate every entry and its association to this complete opening match."""
    if contract is None:
        return [] if not entries else None
    if len(entries) < contract['minimum_entries']:
        return None
    references = [c for c in opening_captures if c['name'] == contract['opening_slot']
                  and c['type'] == contract['reference_type'] and c['span'] is not None]
    if len(references) != 1:
        return None
    result = []
    for index, entry in enumerate(entries):
        layout, reference, value = native_layout(entry)
        if not any(all(layout[k] == v[k] for k in layout) for v in contract['layouts']):
            return None
        if reference != references[0]['value']:
            return None
        result.append(dict(index=index, captures=[
            dict(name='reference', type=contract['reference_type'], value=reference,
                 span=list(entry['prefix_span'])),
            dict(name='value', type=contract['value_type'], value=value,
                 span=list(entry['value_span']))]))
    return result


def validate_contract(contract):
    if contract is None:
        return
    if (set(contract) != {'rule_id', 'opening_slot', 'reference_type', 'value_type',
                         'minimum_entries', 'layouts'}
            or not isinstance(contract['rule_id'], str) or not contract['rule_id']
            or contract['reference_type'] != 'CHARACTER_FULL_ID'
            or contract['value_type'] != 'PARAM' or contract['minimum_entries'] != 1
            or not isinstance(contract['opening_slot'], str) or not contract['layouts']):
        raise ValueError('unsupported repeated-component contract')
    for layout in contract['layouts']:
        if set(layout) != {'leading', 'label', 'trailing'} or not all(isinstance(v, str) for v in layout.values()) or not layout['label']:
            raise ValueError('invalid repeated-component literal layout')
