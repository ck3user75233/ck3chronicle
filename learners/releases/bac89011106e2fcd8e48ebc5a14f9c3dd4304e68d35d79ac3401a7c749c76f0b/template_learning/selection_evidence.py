"""Export candidate-local native evidence for the standalone assignment policy."""
from template_learning import constructions, parameter_structures
from template_learning.patterns import (match_pattern, location_piece_ranges,
                                        parameter_piece_ranges)


def native_fields(record):
    offsets = [0]
    for _, text in record.pieces:
        offsets.append(offsets[-1]+len(text.encode('utf-8','surrogateescape')))
    declared = constructions.field_ranges(record.source_family,record.text,record.pieces)
    opaque = [(a,b,kind) for a,(b,_,_,kind) in declared.items()]
    for a,(b,definition) in parameter_piece_ranges(record.pieces,record.source_family).items():
        opaque.append((a,b,parameter_structures.BY_ID[definition].get('slot_type','PARAM')))
    locations = [(a,b,'LOCATOR') for a,b in location_piece_ranges(record.pieces)
                 if not any(x<=a and b<=y for x,y,_ in opaque)]
    return [(offsets[a],offsets[b],kind) for a,b,kind in [*locations,*opaque]]


def independent_support(cluster, minimum):
    """Occurrence, locator and declared-trace repetition are not new examples."""
    forms = set()
    for record in cluster.records:
        raw = record.text.encode('utf-8','surrogateescape')
        ranges = [(a,b,kind) for a,b,kind in native_fields(record) if kind in {'LOCATOR','PARAM'}]
        cursor, form = 0, []
        for a,b,kind in sorted(ranges):
            if a<cursor:
                continue
            form.extend((raw[cursor:a],kind));cursor=b
        form.append(raw[cursor:])
        if record.continuations:
            form.append(tuple(e['text'] for e in record.continuations))
        forms.add(tuple(form))
    return dict(distinct_messages=len(cluster.records),
                distinct_nonlocation_examples=len(forms),
                distinct_diagnostic_examples=len(forms),
                excluded_variation=['LOCATOR','declared trace PARAM'],
                minimum_distinct_examples=minimum,eligible=len(forms)>=minimum)


def selection_evidence(cluster, support):
    max_locations = max_declared = 0
    for record in cluster.records:
        captures = match_pattern(cluster.parts,record.text,pieces=record.pieces)
        matched = {(c['span'][0],c['span'][1],c['type']) for c in captures or []
                   if c['span'] is not None}
        missing = [f for f in native_fields(record) if f not in matched]
        max_locations=max(max_locations,sum(f[2]=='LOCATOR' for f in missing))
        max_declared=max(max_declared,sum(f[2]!='LOCATOR' for f in missing))
    unsupported=[]
    for part in cluster.parts:
        if part['kind']!='slot':continue
        kind=part['type']; constraints=part['constraints']
        if kind=='PARAM':
            valid=bool(part.get('parameter_definition') or
                       part.get('field_support',{}).get('assessment',{}).get('supported'))
        elif kind in {'KEY','OPTIONAL_KEY'}:
            valid=len(part['observed_values'])+bool(part.get('observed_absence'))>=2
        else:
            valid=bool(constraints.get('location_value') or constraints.get('full_id')
                       or constraints.get('declared_field') or kind=='VALUE')
        if not valid:unsupported.append(part['name'])
    return dict(maximum_location_losses=max_locations,
                maximum_declared_field_losses=max_declared,
                unsubstantiated_fields=len(unsupported),
                unsubstantiated_field_names=unsupported,
                independent_examples=support['distinct_diagnostic_examples'])
