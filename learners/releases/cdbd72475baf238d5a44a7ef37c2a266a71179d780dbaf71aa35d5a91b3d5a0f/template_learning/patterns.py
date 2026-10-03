"""Native literal/slot inference and research capture inspection.

Patterns are candidates. Type proposals describe observed native values and
positional cues; no source text is rewritten and no runtime classification runs.
"""
from __future__ import annotations
from .matching_primitives import (punctuation_piece, path_piece_ranges,
    filename_sequence, pattern_identity, display_pattern, SLOT_TYPES, NUMBER, LINE_REFERENCE)
from .matching_defaults import (key_piece_sequence, location_piece_ranges,
    location_piece_indices, parameter_piece_ranges, analyze_match_pattern, match_pattern)
import difflib
from functools import lru_cache
import re
from template_learning.literal_guidance import LITERAL_WORDING, guided_piece_indices, guided_ranges
from template_learning.owner_rules import LOCATION_CUE, PATH_VALUE_CUE, FILE_VALUE_CUE, FILENAME_SUFFIXES, IDENTIFIER_CUE, INFERENCE_POLICY, LOCATION_LABEL_EQUIVALENCES
from template_learning import regions, constructions, parameter_structures
from template_learning.records import identity

DATE_KEY_PATTERN = re.compile(INFERENCE_POLICY['date_keys']['token_pattern'])


def date_key_piece_indices(pieces):
    """Recognize complete native tokens, without splitting or calendar validation."""
    return tuple(i for i, (kind, text) in enumerate(pieces)
                 if kind == 'token' and DATE_KEY_PATTERN.fullmatch(text))


SLOT_DEFINITIONS = {
    "CHARACTER_FULL_ID": "Complete variable-length character name, of/optional key and ID parentheses; owner-declared emitter boundaries; exact opaque content.",
    "TITLE_FULL_ID": "Complete variable-length title name and ID parentheses; owner-declared emitter boundaries; exact opaque content without rank or key-value classification.",
    "HOUSE_FULL_ID": "Complete variable-length house name and ID parentheses; owner-declared emitter boundaries; exact opaque content including empty internal values.",
    "REASON": "Intact native content of a field in an owner-declared diagnostic construction; not independently classified.",
    "KEY": "A complete native identifier, including owner-approved adjacent qualified segments across raw separator tokens.",
    "OPTIONAL_KEY": "A complete KEY or absence, with any optional enclosing whitespace explicitly declared.",
    "PARAM": "Variable text bounded by surrounding native literals; may span tokens and lines.",
    "LOCATOR": "A location value recognized by labels or path syntax/context; surrounding wording remains literal.",
    "VALUE": "A native numeric-text value at a variable position; never implicitly converted.",
}


class UnsupportedField(ValueError):
    """No slot type is supported; the candidate must retain native alternatives."""

    def __init__(self, values):
        super().__init__('no positive slot-type evidence for the aligned native field')
        self.values = values
        self.spans = None


def field_structure(pieces):
    """Partition incompatible observations using raw syntax, never word lists.

    Ordinary identifier spellings share a shape. Delimiters remain exact and
    whitespace is structural; punctuation-only values cannot broaden identifiers.
    This is discovery grouping, not replacement tokenization or a KEY grammar.
    """
    a,b=0,len(pieces)
    while a<b and pieces[a][0]=='gap':a+=1
    while b>a and pieces[b-1][0]=='gap':b-=1
    return tuple(('punctuation',t) if punctuation_piece(k,t) else
                 ('gap',) if k=='gap' else ('token',) for k,t in pieces[a:b])


def literal_anchor_indices(record):
    fields = set(location_piece_indices(record.pieces))
    for start,(end,*_) in constructions.field_ranges(record.source_family,record.text,record.pieces).items():
        fields.update(range(start,end))
    for start,(end,*_) in parameter_piece_ranges(record.pieces,record.source_family).items():
        fields.update(range(start,end))
    # Retain supplied wording evidence inside every proposed region.
    return sorted(set(guided_piece_indices(record.pieces)) - fields)


def literal_anchor_signature(record):
    return tuple(record.pieces[i] for i in literal_anchor_indices(record))


def _slot(values, before, piece_values, *, location_field=False, declared_field=None, parameter_definition=None, empirical_region=None, source=None):
    if empirical_region is not None:
        constraints=dict(parser_boundaries=True,literal_punctuation=False,literal_guidance=[])
        balance=regions.supported_balance(piece_values)
        if balance:
            constraints['balanced_pairs']=balance
        return dict(kind='slot',type='PARAM',optional=False,prefix='',suffix='',
            constraints=constraints,observed_values=sorted(set(values)),observed_absence=False,
            empirical_region=empirical_region,
            inference_basis='varying balanced outer region established before interior alignment')
    if parameter_definition is not None:
        definition=parameter_structures.BY_ID[parameter_definition]
        full_id=definition['mechanic']=='full_id'
        constraints=dict(parser_boundaries=True,literal_punctuation=False,literal_guidance=[])
        if full_id:
            constraints['full_id']={'definition':parameter_definition,'source':source}
        return dict(kind='slot',type=definition['slot_type'] if full_id else 'PARAM',optional=False,prefix='',suffix='',
            constraints=constraints,
            observed_values=sorted(set(values)),observed_absence=False,
            parameter_definition=parameter_definition,
            inference_basis='owner-declared complete opaque full-ID structure' if full_id else 'owner-declared parameter structure; ordinary PARAM matching')
    if declared_field is not None:
        construction,field,kind=declared_field
        return dict(kind="slot",type=kind,optional=False,prefix="",suffix="",
            constraints=dict(parser_boundaries=True,literal_punctuation=False,literal_guidance=[],
                declared_field=dict(construction=construction,field=field)),
            observed_values=sorted(set(values)),observed_absence=False,
            inference_basis="owner-declared intact field; no separate reason template inference")
    nonempty = [s for s in values if s]
    optional = len(nonempty) != len(values)
    # Whitespace around an optional value is part of its declared presence,
    # rather than part of a KEY capture or unrecorded normalization.
    leading = [s[:len(s)-len(s.lstrip())] for s in nonempty]
    trailing = [s[len(s.rstrip()):] for s in nonempty]
    prefix = leading[0] if leading and len(set(leading)) == 1 else ""
    suffix = trailing[0] if trailing and len(set(trailing)) == 1 else ""
    cores = [s[len(prefix):len(s)-len(suffix) if suffix else None] for s in nonempty]
    if any(not core for core in cores):
        prefix, suffix, cores = "", "", nonempty
    core_pieces = []
    for pieces, value in zip(piece_values, values):
        if not value:
            continue
        a, b = 0, len(pieces)
        while a < b and pieces[a][0] == "gap":
            a += 1
        while b > a and pieces[b-1][0] == "gap":
            b -= 1
        core_pieces.append(tuple(pieces[a:b]))
    continuous = bool(cores) and all(key_piece_sequence(p) for p in core_pieces)
    paths = [path_piece_ranges(p) == ((0, len(p)),) for p in core_pieces]
    complete_fields = bool(core_pieces) and all(
        is_path or filename_sequence(p) or len(p) == 1 and not punctuation_piece(*p[0])
        for p, is_path in zip(core_pieces, paths))
    location = location_field or LOCATION_CUE.search(before) or (
        PATH_VALUE_CUE.search(before) and all(paths))
    identifier = IDENTIFIER_CUE.search(before)
    numeric = bool(cores) and all(re.fullmatch(NUMBER,s) for s in cores)
    path_values = bool(core_pieces) and all(
        filename_sequence(p) and (is_path or any(p[-1][1].casefold().endswith(ext) for ext in FILENAME_SUFFIXES))
        for p, is_path in zip(core_pieces, paths))
    if complete_fields and (location or path_values):
        kind, basis = "LOCATOR", "location label or path formulation identifies the field" if location else "complete file-path syntax identifies the field"
    elif numeric and not identifier:
        kind, basis = "VALUE", "all observed variable values are native numeric text"
    elif continuous:
        kind, basis = ("OPTIONAL_KEY" if optional else "KEY"), "observed variable values are complete continuous strings"
    elif regions.span_variation(core_pieces,atomic=[key_piece_sequence(p) for p in core_pieces])['supported']:
        kind, basis = "PARAM", "distinct observed raw multi-token spans; surrounding boundaries require separate validation"
    else:
        raise UnsupportedField(values)
    constraints = {"parser_boundaries": True, "literal_punctuation": kind != "PARAM",
                   "literal_guidance": list(LITERAL_WORDING)}
    if kind == "PARAM":
        balance = regions.supported_balance(piece_values)
        if balance:
            constraints["balanced_pairs"] = balance
    if kind in {"KEY","OPTIONAL_KEY"}:
        constraints["key_joiners"] = INFERENCE_POLICY['key_syntax']['joiners']
        constraints["literal_punctuation"] = False
    if kind == "LOCATOR":
        # Only a complete adjacent path sequence or one labelled value is valid.
        # Separators and symbol words within this range belong to its value.
        constraints["literal_guidance"] = []
        constraints["literal_punctuation"] = False
        constraints["location_value"] = True
        if numeric:
            constraints["numeric_text"] = True
        if cores and all(re.fullmatch(LINE_REFERENCE, value) for value in cores):
            constraints["line_reference"] = True
    if kind == "VALUE":
        constraints["numeric_text"] = True
    return dict(kind="slot", type=kind, optional=optional, prefix=prefix, suffix=suffix,
        constraints=constraints, inference_basis=basis,
        observed_values=sorted(set(cores)), observed_absence=optional)


def inference_units(record, *, region_first=True):
    """Align recognized fields as ranges; retain original pieces for captures.

    This is an inference view, not replacement tokenization or normalized text.
    Each unit maps directly to a half-open range of the selected raw pieces.
    """
    return _inference_units(record.pieces,record.source_family,region_first)


def location_label_forms(record):
    """Declared equivalent labels, retaining their exact native spellings.

    Locations must already be recognized. Traverse the ordinary inference view
    so labels inside declared opaque fields cannot affect outer formulations.
    Neither native text nor OPTIONAL_KEY evidence is changed here.
    """
    units, spans = inference_units(record, region_first=False)
    forms = sorted(((group['id'], tuple(form))
                    for group in LOCATION_LABEL_EQUIVALENCES if not group.get('literal_alternatives')
                    for form in group['forms']),
                   key=lambda item: -len(item[1]))
    result = []
    for index, (unit, (start, _)) in enumerate(zip(units, spans)):
        if unit != ('location',):
            continue
        for group, form in forms:
            cursor = index - 1
            for expected in reversed(form):
                while cursor >= 0 and units[cursor][0] == 'gap' and not units[cursor][1].strip(' \t'):
                    cursor -= 1
                if cursor < 0 or units[cursor] != ('token', expected):
                    break
                cursor -= 1
            else:
                a = spans[cursor + 1][0]
                label = ''.join(text for _, text in record.pieces[a:start]).rstrip(' \t')
                ordinal = sum(u == ('location',) for u in units[:index])
                result.append((ordinal, group, label))
                break
    return tuple(result)


@lru_cache(maxsize=16384)
def _inference_units(pieces,source,region_first=True):
    locations = dict(location_piece_ranges(pieces))
    declared = constructions.field_ranges(source,"".join(t for _,t in pieces),pieces)
    parameters=parameter_piece_ranges(pieces,source)
    excluded=tuple([*locations.items(),*((a,v[0]) for a,v in declared.items()),
                    *((a,v[0]) for a,v in parameters.items())])
    # A label is structural literal wording, not a field. Recognize it only
    # beside a complete numeric location and outside every opaque field.
    labels = {}
    opaque = [(a, v[0]) for a, v in declared.items()] + [(a, v[0]) for a, v in parameters.items()]
    for start, end in locations.items():
        if any(a < end and start < b for a, b in opaque):
            continue
        if not re.fullmatch(LINE_REFERENCE, ''.join(t for _, t in pieces[start:end])):
            continue
        stop = start
        while stop and pieces[stop-1][0] == 'gap' and not pieces[stop-1][1].strip(' \t'):
            stop -= 1
        for group in LOCATION_LABEL_EQUIVALENCES:
            for spelling in group.get('literal_alternatives', ()):
                a, text = stop, ''
                while a and len(text) < len(spelling):
                    a -= 1
                    text = pieces[a][1] + text
                if text == spelling and not any(x < stop and a < y for x, y in excluded):
                    labels[a] = (stop, group['id'])
    # Prefer the whole "near line:" over its suffix "line:".
    labels = {a: value for a, value in labels.items()
              if not any(x < a < y for x, (y, _) in labels.items())}
    dates = {i for i in date_key_piece_indices(pieces)
             if not any(a <= i < b for a, b in excluded)}
    envelopes={a+1:(b,pieces[a][1],pieces[b][1])
               for a,b in regions.candidate_envelopes(pieces,(*excluded, *((i,i+1) for i in dates)))} if region_first else {}
    keys, bounds, i = [], [], 0
    while i < len(pieces) or i in declared:
        if i in declared:
            # An explicitly empty field consumes no raw pieces. Emit its unit
            # once, then process the unchanged boundary (e.g. the closing ]).
            end,construction,field,kind=declared.pop(i)
            keys.append(("declared",construction,field,kind))
            bounds.append((i,end))
            i=end
            continue
        if i in parameters:
            end,definition=parameters[i]
            keys.append(('parameter',definition));bounds.append((i,end));i=end
            continue
        if i in labels:
            end, group = labels[i]
            keys.append(('location-label', group)); bounds.append((i, end)); i=end
            continue
        if i in dates:
            keys.append(('date-key',));bounds.append((i,i+1));i+=1
            continue
        if i in envelopes:
            end,opener,closer=envelopes[i]
            keys.append(('region',opener,closer));bounds.append((i,end));i=end
            continue
        end = locations.get(i, i + 1)
        keys.append(("location",) if i in locations else pieces[i])
        bounds.append((i, end))
        i = end
    return tuple(keys), tuple(bounds)


def derive_pattern(records, reference, *, hypotheses=None):
    """Consensus wording and complete location ranges in native order."""
    if not any(r is reference for r in records):
        raise ValueError("alignment reference must be an observed member")
    records = [reference, *(r for r in records if r is not reference)]
    ref, ref_spans = inference_units(reference)
    units = [inference_units(r) for r in records]
    sequences = [u[0] for u in units]

    maps = []
    for seq,spans in units:
        mapping = {}
        for block in difflib.SequenceMatcher(None,ref,seq,autojunk=False).get_matching_blocks():
            mapping.update((block.a+i,block.b+i) for i in range(block.size))
        maps.append(mapping)
    stable = [i for i in range(len(ref)) if all(i in m for m in maps)]
    guided=set(literal_anchor_indices(reference))
    mandatory={i for i,(a,b) in enumerate(ref_spans) if a in guided and i in stable}
    stable, marker_decisions = regions.supported_anchors(sequences, maps, stable, mandatory)
    if hypotheses is not None:
        hypotheses.extend(marker_decisions)
    parts, boundary_failures, slot_ranges = [], [], {}
    proposed_slots = []

    def typed_slot(spans, before, **kwargs):
        pieces=[r.pieces[a:b] for r,(a,b) in zip(records,spans)]
        values=[''.join(t for _,t in p) for p in pieces]
        try:
            return _slot(values,before,pieces,source=reference.source_family,**kwargs)
        except UnsupportedField as exc:
            # Preserve association with this exact candidate, including records
            # reordered to put its alignment reference first.
            exc.spans={identity(r.key):(a,b) for r,(a,b) in zip(records,spans)}
            raise

    def literal(text):
        if not text:
            return
        if parts and parts[-1]["kind"] == "literal" and 'alternatives' not in parts[-1]:
            parts[-1]["text"] += text
        else:
            parts.append(dict(kind="literal", text=text))

    def add_slot(spans, *, location_field=False, declared_field=None, parameter_definition=None, empirical_region=None, date_key=False):
        piece_values = [r.pieces[a:b] for r, (a, b) in zip(records, spans)]
        values = ["".join(t for _, t in p) for p in piece_values]
        before = parts[-1]["text"] if parts and parts[-1]["kind"] == "literal" else ""
        part = typed_slot(spans, before, location_field=location_field,declared_field=declared_field,parameter_definition=parameter_definition,empirical_region=empirical_region)
        if date_key:
            # The owner declaration supplies field evidence even for one value.
            # Matching remains the existing KEY grammar, with no date constraint.
            part.update(type='KEY', inference_rule=INFERENCE_POLICY['date_keys']['id'],
                        inference_basis='owner-declared native date token is KEY, including constant observations')
            part['constraints'] = dict(parser_boundaries=True, literal_punctuation=False,
                                       literal_guidance=[], key_joiners=INFERENCE_POLICY['key_syntax']['joiners'])
        if part["type"] not in {"LOCATOR", "PARAM", "REASON", "KEY", "OPTIONAL_KEY", "CHARACTER_FULL_ID", "HOUSE_FULL_ID", "TITLE_FULL_ID"} and any(
                punctuation_piece(k, t) for pieces in piece_values for k, t in pieces):
            boundary_failures.extend(r.text for r in records)
        part["name"] = f"s{len(slot_ranges)}"
        part['field_support']=regions.evidence(records,spans)
        slot_ranges[part["name"]] = spans
        parts.append(part)
        proposed_slots.append((part,spans))
        if hypotheses is not None:
            facts = regions.evidence(records, spans)
            insufficient = part['type']=='PARAM' and part['optional'] and facts['nonempty_values']<2
            hypotheses.append(dict(proposal="aligned_variation", decision="insufficient" if insufficient else "accepted",
                reason="one nonempty spelling plus absence does not establish variable interior content" if insufficient else part["inference_basis"], slot_type=part["type"],
                preceding_literal=before, **facts))

    boundaries = [-1, *stable, len(ref)]
    for left, right in zip(boundaries, boundaries[1:]):
        spans = [(unit_spans[mapping[left]][1] if left >= 0 else 0,
                  unit_spans[mapping[right]][0] if right < len(ref) else len(record.pieces))
                 for record, (_, unit_spans), mapping in zip(records, units, maps)]
        values = ["".join(t for _, t in r.pieces[a:b]) for r, (a, b) in zip(records, spans)]
        if len(set(values)) == 1:
            literal(values[0])
        elif any(values):
            add_slot(spans)
        if right < len(ref):
            if ref[right][0] == 'location-label':
                group = next(g for g in LOCATION_LABEL_EQUIVALENCES if g['id'] == ref[right][1])
                forms = group['literal_alternatives']
                parts.append(dict(kind='literal', text=forms[0], alternatives=list(forms),
                                  location_label=group['id']))
            elif ref[right] == ("location",):
                fields = [unit_spans[mapping[right]] for (_, unit_spans), mapping in zip(units, maps)]
                add_slot(fields, location_field=True)
            elif ref[right] == ('date-key',):
                fields = [unit_spans[mapping[right]] for (_, unit_spans), mapping in zip(units, maps)]
                add_slot(fields, date_key=True)
            elif ref[right][0] == "declared":
                fields = [unit_spans[mapping[right]] for (_,unit_spans),mapping in zip(units,maps)]
                add_slot(fields,declared_field=ref[right][1:])
            elif ref[right][0]=='parameter':
                fields=[unit_spans[mapping[right]] for (_,unit_spans),mapping in zip(units,maps)]
                add_slot(fields,parameter_definition=ref[right][1])
            elif ref[right][0]=='region':
                fields=[unit_spans[mapping[right]] for (_,unit_spans),mapping in zip(units,maps)]
                interiors=[r.pieces[a:b] for r,(a,b) in zip(records,fields)]
                values=[''.join(t for _,t in pieces) for pieces in interiors]
                support=regions.envelope_support(interiors,atomic=[key_piece_sequence(p) for p in interiors])
                if len(set(values))==1:
                    literal(values[0])
                elif support['supported'] and not all(key_piece_sequence(p) for p in interiors):
                    add_slot(fields,empirical_region=dict(opener=ref[right][1],closer=ref[right][2],**support))
                else:
                    add_slot(fields)
                if hypotheses is not None:
                    hypotheses.append(dict(proposal='region_first_envelope',
                        decision='accepted' if support['supported'] and not all(key_piece_sequence(p) for p in interiors) else 'ordinary_interior',
                        reason='outer boundary considered before interior wording',
                        opener=ref[right][1],closer=ref[right][2],**support,**regions.evidence(records,fields)))
            else:
                a, b = ref_spans[right]
                literal("".join(t for _, t in reference.pieces[a:b]))
    if hypotheses is not None:
        hypotheses.extend(regions.envelope_review(records,sequences,maps,[u[1] for u in units],stable,proposed_slots))
    # A PARAM and adjacent variable slots separated only by whitespace have
    # no learned literal boundary establishing independent fields. Re-infer
    # their complete native span together; preserve every gap in that span.
    coalesced, i = [], 0
    def coalescible(part):
        return (part.get('type') in {'KEY', 'OPTIONAL_KEY', 'PARAM'}
                and not part.get('parameter_definition') and not part.get('empirical_region')
                and not part.get('inference_rule'))
    while i < len(parts):
        end = i
        if coalescible(parts[i]):
            while (end+2 < len(parts) and parts[end+1]["kind"] == "literal"
                   and parts[end+1]["text"].isspace()
                   and coalescible(parts[end+2])):
                end += 2
        if end > i and any(p.get("type") == "PARAM" for p in parts[i:end+1]):
            spans = [(a[0],b[1]) for a,b in zip(slot_ranges[parts[i]["name"]],slot_ranges[parts[end]["name"]])]
            values = ["".join(t for _,t in r.pieces[a:b]) for r,(a,b) in zip(records,spans)]
            piece_values = [r.pieces[a:b] for r,(a,b) in zip(records,spans)]
            before = coalesced[-1]["text"] if coalesced and coalesced[-1]["kind"] == "literal" else ""
            joined=typed_slot(spans,before)
            joined['field_support']=regions.evidence(records,spans)
            coalesced.append(joined)
            i = end+1
        else:
            coalesced.append(parts[i])
            i += 1
    parts = coalesced
    # A joint span may be reconsidered only within a real enclosing pair,
    # reusing native member ranges. One adjacent punctuation mark is not an
    # enclosure and cannot justify swallowing an intervening literal word.
    # Longer literal runs and LOCATOR/VALUE/REASON fields remain separate.
    coalesced, i = [], 0
    policy=INFERENCE_POLICY['param_boundary_preference']
    while i<len(parts):
        end=i
        if coalescible(parts[i]):
            while (end+2<len(parts) and parts[end+1]['kind']=='literal'
                   and coalescible(parts[end+2])):
                connector=parts[end+1]['text']
                words=connector.split()
                if (not words or len(words)>policy['weak_connector_max_words']
                        or not all(w.isalpha() for w in words) or '\n' in connector or '\r' in connector):
                    break
                end+=2
        before=coalesced[-1]['text'] if coalesced and coalesced[-1]['kind']=='literal' else ''
        after=parts[end+1]['text'] if end+1<len(parts) and parts[end+1]['kind']=='literal' else ''
        spans=None
        if end>i and any(p.get('type')=='PARAM' for p in parts[i:end+1]):
            first={m['record_id']:m['pieces'] for m in parts[i]['field_support']['members']}
            last={m['record_id']:m['pieces'] for m in parts[end]['field_support']['members']}
            spans=[(first[identity(r.key)][0],last[identity(r.key)][1]) for r in records]
        if spans is not None and regions.enclosing_pair(records,spans) is not None:
            piece_values=[r.pieces[a:b] for r,(a,b) in zip(records,spans)]
            joined=typed_slot(spans,before)
            joined['field_support']=regions.evidence(records,spans)
            if hypotheses is not None:
                hypotheses.append(dict(proposal='paired_envelope_coalescing',decision='accepted',
                    absorbed_wording=[p['text'] for p in parts[i:end+1] if p['kind']=='literal'],
                    reason='joint variable span has corresponding enclosing raw-token pairs; field evidence and complete capture replay still required',
                    **joined['field_support']))
            coalesced.append(joined)
            i=end+1
        else:
            coalesced.append(parts[i]);i+=1
    parts=coalesced
    for number,part in enumerate(p for p in parts if p["kind"] == "slot"):
        part["name"] = f"s{number}"
    for i,part in enumerate(parts):
        if part['kind']!='slot' or part['type'] in {'LOCATOR','REASON','VALUE','CHARACTER_FULL_ID','HOUSE_FULL_ID', 'TITLE_FULL_ID'}:
            continue
        before=parts[i-1]['text'] if i and parts[i-1]['kind']=='literal' else ''
        after=parts[i+1]['text'] if i+1<len(parts) and parts[i+1]['kind']=='literal' else ''
        if part['type']=='PARAM':
            members={m['record_id']:m['pieces'] for m in part['field_support']['members']}
            spans=[members[identity(r.key)] for r in records]
            evidence=regions.field_evidence(part,records,spans)
            if part.get('parameter_definition'):
                evidence.update(supported=True,declared_structure=part['parameter_definition'])
            part['field_support']['assessment']=evidence
            if not evidence['supported']:
                part['rejection_reason']='no supported enclosing raw-token pair or owner-declared PARAM structure'
            elif INFERENCE_POLICY['field_local_literal_guidance'] and evidence['paired_boundaries']:
                part['constraints']['literal_guidance']=[]
                part['field_support']['presumed_literals']='captured content inside this empirically supported field only'
        # Supplied wording remains protected unless field evidence above permits it.
        if part['constraints']['literal_guidance']:
            members={x['record_id']:x for x in part['field_support']['members']}
            for record in records:
                a,b=members[identity(record.key)]['pieces']
                if guided_ranges(record.pieces[a:b],part['constraints']['literal_guidance']):
                    part['rejection_reason']='presumed literal has no supported field-local interpretation'
                    break
    # No supported member may disappear due to majority literals or an
    # incorrect optional boundary. A failed candidate is reported explicitly.
    failures=list(boundary_failures)
    support={p['name']:{m['record_id']:m['bytes'] for m in p['field_support']['members']}
             for p in parts if p['kind']=='slot'}
    fields={p['name']:p for p in parts if p['kind']=='slot'}
    for record in records:
        assessment=analyze_match_pattern(parts,record.text,pieces=record.pieces)
        captures=assessment['captures']
        if captures is None:
            failures.append(record.text)
            if hypotheses is not None and assessment['count']>1:
                hypotheses.append(dict(proposal='capture_ambiguity',decision='rejected',record_id=identity(record.key),
                    reason='multiple complete capture assignments; none selected',
                    count=assessment['count'],witnesses=assessment['witnesses']))
            continue
        rid=identity(record.key)
        mismatches=[]
        for capture in captures:
            p=fields[capture['name']];a,b=support[p['name']][rid]
            expected=None if a==b and p['optional'] else [
                a+len(p['prefix'].encode('utf-8','surrogateescape')),
                b-len(p['suffix'].encode('utf-8','surrogateescape'))]
            if capture['span']!=expected:
                mismatches.append(dict(field=p['name'],inferred=expected,matched=capture['span']))
        if mismatches:
            failures.append(record.text)
            if hypotheses is not None:
                hypotheses.append(dict(proposal='capture_replay',decision='rejected',record_id=rid,
                    reason='complete matching must reproduce the candidate member spans used for field inference',
                    mismatches=mismatches))
    failures=sorted(set(failures))
    return parts, failures
