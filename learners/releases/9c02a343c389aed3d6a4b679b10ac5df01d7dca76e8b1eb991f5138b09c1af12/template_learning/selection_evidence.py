"""Export candidate-local native evidence for the standalone assignment policy."""
from template_learning import constructions, parameter_structures
from template_learning.matching_defaults import (match_pattern, location_piece_ranges,
                                        parameter_piece_ranges)
from template_learning.owner_rules import INFERENCE_POLICY
from template_learning import location_sequences


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
    fields = [(offsets[a],offsets[b],kind) for a,b,kind in [*locations,*opaque]]
    found = location_sequences.sequence(tuple(record.pieces))
    if found:
        fields = [f for f in fields if f[0]<offsets[found['start_piece']]]
        fields.extend((c['span'][0],c['span'][1],c['type']) for e in found['entries'] for c in e['captures'])
    return fields


def independent_support(cluster, minimum):
    """Slot variation is evidence diversity, without being wording evidence."""
    forms = {(record.text, tuple(e['text'] for e in record.continuations))
             for record in cluster.records}
    return dict(distinct_messages=len(forms),
                distinct_diagnostic_examples=len(forms),
                excluded_variation=['exact repetitions', 'native headers and occurrence provenance'],
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
            valid=(bool(constraints.get('parameter_structure')) or part.get('inference_rule') == INFERENCE_POLICY['date_keys']['id']
                   or len(part['observed_values'])+bool(part.get('observed_absence'))>=2)
        else:
            valid=bool(constraints.get('location_value') or constraints.get('full_id') or constraints.get('parameter_structure')
                       or constraints.get('declared_field') or kind=='VALUE')
        if not valid:unsupported.append(part['name'])
    return dict(maximum_location_losses=max_locations,
                maximum_declared_field_losses=max_declared,
                unsubstantiated_fields=len(unsupported),
                unsubstantiated_field_names=unsupported,
                independent_examples=support['distinct_diagnostic_examples'])
