"""Native literal/slot inference and research capture inspection.

Patterns are candidates. Type proposals describe observed native values and
positional cues; no source text is rewritten and no runtime classification runs.
"""
from __future__ import annotations
import difflib
from functools import lru_cache
import json
import re
import string
import unicodedata
from bisect import bisect_right
from template_learning.literal_guidance import LITERAL_WORDING, guided_piece_indices, guided_ranges
from template_learning.owner_rules import LOCATION_CUE, PATH_VALUE_CUE, FILE_VALUE_CUE, FILENAME_SUFFIXES, IDENTIFIER_CUE, INFERENCE_POLICY, LOCATION_LABEL_EQUIVALENCES
from template_learning import regions, constructions, parameter_structures
from template_learning.records import identity

SLOT_TYPES = ("KEY", "OPTIONAL_KEY", "PARAM", "LOCATOR", "VALUE", "REASON", "CHARACTER_FULL_ID", "HOUSE_FULL_ID", "TITLE_FULL_ID")
NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
LINE_REFERENCE = r"[0-9]+(?:-[0-9]+)?"
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

def key_piece_sequence(pieces, joiners=None):
    """One identifier or adjacent qualified identifiers; never retokenize."""
    joiners = INFERENCE_POLICY['key_syntax']['joiners'] if joiners is None else joiners
    return bool(pieces) and len(pieces) % 2 == 1 and all(
        k == 'token' and (t in joiners if i % 2 else not punctuation_piece(k, t))
        for i, (k, t) in enumerate(pieces))


@lru_cache(maxsize=16384)
def key_capture_ends(pieces, joiners):
    offsets=[0]
    for _,text in pieces: offsets.append(offsets[-1]+len(text))
    result={}
    for i,piece in enumerate(pieces):
        if not key_piece_sequence((piece,),joiners):continue
        ends=[offsets[i+1]];j=i+1
        while j+1<len(pieces) and pieces[j][0]=='token' and pieces[j][1] in joiners and key_piece_sequence((pieces[j+1],),joiners):
            ends.append(offsets[j+2]);j+=2
        result[offsets[i]]=tuple(ends)
    return result


def punctuation_piece(kind, text):
    """Classify an existing parser piece; never split or normalize its text."""
    return kind == "token" and bool(text) and all(
        c in string.punctuation or unicodedata.category(c).startswith("P") for c in text)


@lru_cache(maxsize=16384)
def path_piece_ranges(pieces):
    """Adjacent segment / segment ranges in the selected parser's own pieces.

    No gap may occur within a range. Slash syntax is evidence, not by itself
    a decision that prose such as province/barony/county is a location.
    """
    result, i = [], 0
    while i < len(pieces):
        j, segments, separators, previous_segment = i, [], 0, False
        while j < len(pieces):
            kind, text = pieces[j]
            if kind != "token":
                break
            if text == "/":
                separators += 1
                previous_segment = False
            elif not punctuation_piece(kind, text) or text in {".", ".."}:
                if previous_segment:
                    break
                segments.append(text)
                previous_segment = True
            else:
                break
            j += 1
        if separators and segments and not all(re.fullmatch(NUMBER, t) for t in segments):
            result.append((i, j))
        i = max(i + 1, j)
    return tuple(result)


def filename_shape(text):
    """Dotted filename shape; needs suffix evidence or explicit file context."""
    return re.fullmatch(r"[^/\s:]+\.[A-Za-z][A-Za-z0-9_-]*", text) is not None


def filename_sequence(pieces):
    return bool(pieces) and pieces[-1][0] == "token" and filename_shape(pieces[-1][1]) and all(
        kind == "gap" and text and not text.strip(" ")
        or kind == "token" and (not punctuation_piece(kind, text) or text in {"/", ".", ".."})
        for kind, text in pieces)


def filename_field_end(pieces, start):
    """First complete filename in an explicitly introduced file field.

    Spaces may occur inside a filename. Delimiters, line breaks and labels
    terminate this scan; it never consumes the remainder of a diagnostic line.
    """
    for end in range(start, len(pieces)):
        kind, text = pieces[end]
        if kind == "gap":
            if text.strip(" "):
                return None
        elif punctuation_piece(kind, text) and text not in {"/", ".", ".."}:
            return None
        elif filename_shape(text) and not (end + 1 < len(pieces) and pieces[end + 1] == ("token", "/")):
            return end + 1
    return None


def line_after_filename(pieces, end):
    index = end
    if index < len(pieces) and pieces[index][0] == "gap" and not pieces[index][1].strip(" "):
        index += 1
    if index >= len(pieces) or pieces[index] != ("token", ":"):
        return None
    index += 1
    if index < len(pieces) and pieces[index][0] == "gap" and not pieces[index][1].strip(" "):
        index += 1
    if index < len(pieces) and pieces[index][0] == "token" and re.fullmatch(LINE_REFERENCE, pieces[index][1]):
        return index
    return None


@lru_cache(maxsize=16384)
def location_piece_ranges(pieces):
    """Find paths, bare filenames and separate line fields in original pieces."""
    paths = dict(path_piece_ranges(pieces))
    result, before, i = [], "", 0
    while i < len(pieces):
        end = paths.get(i, i + 1)
        kind, text = pieces[i]
        is_path = i in paths
        ordinary = kind == "token" and not punctuation_piece(kind, text)
        file_end = filename_field_end(pieces, i) if ordinary and FILE_VALUE_CUE.search(before) else None
        if file_end is not None:
            end = file_end
        final = pieces[end-1][1]
        filename = filename_sequence(pieces[i:end])
        line_index = line_after_filename(pieces, end) if filename else None
        known_suffix = filename and any(final.casefold().endswith(ext) for ext in FILENAME_SUFFIXES)
        recognized = (file_end is not None or known_suffix or line_index is not None
            or is_path and (LOCATION_CUE.search(before) or PATH_VALUE_CUE.search(before) or filename)
            or not is_path and ordinary and LOCATION_CUE.search(before))
        if recognized:
            result.append((i, end))
            if line_index is not None:
                result.append((line_index, line_index+1))
        before += "".join(t for _, t in pieces[i:end])
        i = end
    return tuple(sorted(set(result)))


@lru_cache(maxsize=16384)
def location_piece_indices(pieces):
    return tuple(i for a, b in location_piece_ranges(pieces) for i in range(a, b))




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
                    for group in LOCATION_LABEL_EQUIVALENCES for form in group['forms']),
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
def parameter_piece_ranges(pieces,source):
    declared=constructions.field_ranges(source,''.join(t for _,t in pieces),pieces)
    return parameter_structures.declarations_for(pieces,[(a,v[0]) for a,v in declared.items()],source)


@lru_cache(maxsize=16384)
def _inference_units(pieces,source,region_first=True):
    locations = dict(location_piece_ranges(pieces))
    declared = constructions.field_ranges(source,"".join(t for _,t in pieces),pieces)
    parameters=parameter_piece_ranges(pieces,source)
    excluded=tuple([*locations.items(),*((a,v[0]) for a,v in declared.items()),
                    *((a,v[0]) for a,v in parameters.items())])
    envelopes={a+1:(b,pieces[a][1],pieces[b][1])
               for a,b in regions.candidate_envelopes(pieces,excluded)} if region_first else {}
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
        if parts and parts[-1]["kind"] == "literal":
            parts[-1]["text"] += text
        else:
            parts.append(dict(kind="literal", text=text))

    def add_slot(spans, *, location_field=False, declared_field=None, parameter_definition=None, empirical_region=None):
        piece_values = [r.pieces[a:b] for r, (a, b) in zip(records, spans)]
        values = ["".join(t for _, t in p) for p in piece_values]
        before = parts[-1]["text"] if parts and parts[-1]["kind"] == "literal" else ""
        part = typed_slot(spans, before, location_field=location_field,declared_field=declared_field,parameter_definition=parameter_definition,empirical_region=empirical_region)
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
            if ref[right] == ("location",):
                fields = [unit_spans[mapping[right]] for (_, unit_spans), mapping in zip(units, maps)]
                add_slot(fields, location_field=True)
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
    while i < len(parts):
        end = i
        if parts[i].get("type") in {"KEY", "OPTIONAL_KEY", "PARAM"} and not parts[i].get('parameter_definition') and not parts[i].get('empirical_region'):
            while (end+2 < len(parts) and parts[end+1]["kind"] == "literal"
                   and parts[end+1]["text"].isspace()
                   and parts[end+2].get("type") in {"KEY", "OPTIONAL_KEY", "PARAM"}
                   and not parts[end+2].get('parameter_definition') and not parts[end+2].get('empirical_region')):
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
    text_fields={'KEY','OPTIONAL_KEY','PARAM'}
    policy=INFERENCE_POLICY['param_boundary_preference']
    while i<len(parts):
        end=i
        if parts[i].get('type') in text_fields and not parts[i].get('parameter_definition') and not parts[i].get('empirical_region'):
            while (end+2<len(parts) and parts[end+1]['kind']=='literal'
                   and parts[end+2].get('type') in text_fields and not parts[end+2].get('parameter_definition') and not parts[end+2].get('empirical_region')):
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


def pattern_identity(parts):
    """Structural identity excludes example values and support frequencies."""
    return [{k:v for k,v in p.items() if k not in {"observed_values","observed_absence","inference_basis","field_support","rejection_reason","parameter_definition","empirical_region"}}
            for p in parts]


@lru_cache(maxsize=4096)
def _matching_plan(material):
    result = json.loads(material)
    if any(p["kind"] == "slot" and p["type"] not in SLOT_TYPES for p in result):
        raise ValueError("unsupported slot type")
    allowed = {"parser_boundaries", "literal_punctuation", "literal_guidance", "single_token", "key_joiners",
               "location_value", "numeric_text", "line_reference", "balanced_pairs", "declared_field", "full_id"}
    if any(set(p["constraints"]) - allowed for p in result if p["kind"] == "slot"):
        raise ValueError("unsupported slot constraint")
    return result


@lru_cache(maxsize=16384)
def _piece_index(pieces):
    boundaries, starts, punctuation, cursor = [0], {}, [], 0
    for kind,value in pieces:
        starts[cursor] = (kind,value)
        if punctuation_piece(kind,value):
            punctuation.append((cursor,cursor+len(value)))
        cursor += len(value)
        boundaries.append(cursor)
    return boundaries, starts, punctuation


@lru_cache(maxsize=16384)
def location_capture_ends(pieces):
    # Matching applies the same structural evidence as inference. An arbitrary
    # word must not satisfy a bare filename LOCATOR merely by being one token.
    offsets, cursor = [], 0
    for _, text in pieces:
        offsets.append(cursor)
        cursor += len(text)
    offsets.append(cursor)
    return {offsets[a]: offsets[b] for a, b in location_piece_ranges(pieces)}


def match_pattern(parts, text, start=0, *, pieces):
    """Return captures only when the complete assignment is unique."""
    return analyze_match_pattern(parts,text,start,pieces=pieces)['captures']


def analyze_match_pattern(parts, text, start=0, *, pieces, witness_limit=2):
    """Count every complete assignment in a memoized acyclic search.

    Two witnesses suffice to demonstrate ambiguity; witness_limit=None exports
    every complete assignment for deterministic selection. The count is exact and
    includes every successful branch. No inference spans or observed spellings
    are consulted, and a matching prefix is never a complete assignment.
    """
    if "".join(t for _,t in pieces) != text:
        raise ValueError("matching requires the selected parser's exact pieces")
    if parts and parts[0]["kind"] == "literal" and not text.startswith(parts[0]["text"]):
        return dict(count=0,captures=None,witnesses=[])
    plan = _matching_plan(json.dumps(pattern_identity(parts),sort_keys=True,ensure_ascii=True))
    pieces = tuple(tuple(p) for p in pieces)
    boundaries,starts,punctuation = _piece_index(pieces)
    boundary_set = set(boundaries)
    protected = {tuple(p["constraints"].get("literal_guidance",())) for p in plan if p["kind"] == "slot"}
    guides = {w:guided_ranges(pieces,w) for w in protected}

    @lru_cache(maxsize=None)
    def visit(index,position):
        if index == len(plan):
            return (1,((),)) if position == len(text) else (0,())
        part = plan[index]
        if part["kind"] == "literal":
            literal = part["text"]
            return visit(index+1,position+len(literal)) if text.startswith(literal,position) else (0,())
        prefix,suffix,c = part["prefix"],part["suffix"],part["constraints"]
        total,witnesses=0,[]
        a = position+len(prefix)
        if text.startswith(prefix,position) and a in boundary_set:
            if c.get("declared_field"):
                field=c['declared_field']
                span=constructions.capture_range(field['construction'],field['field'],text)
                ends=(span[1],) if span is not None and span[0]==a else ()
            elif c.get('full_id'):
                field=c['full_id']
                end=parameter_structures.FULL_IDS.capture_ends(pieces,field['source'],field['definition']).get(a)
                ends=(end,) if end is not None else ()
            elif c.get("location_value"):
                end = location_capture_ends(pieces).get(a)
                ends = (end,) if end is not None else ()
            elif c.get("single_token"):
                piece = starts.get(a)
                ends = (a+len(piece[1]),) if piece and piece[0] == "token" else ()
            elif 'key_joiners' in c:
                ends = key_capture_ends(pieces, tuple(c['key_joiners'])).get(a, ())
            else:
                ends = boundaries[bisect_right(boundaries,a):]
            forbidden = guides[tuple(c.get("literal_guidance",()))]
            if c.get("literal_punctuation"):
                forbidden = (*forbidden,*punctuation)
            limit = min((max(a,x) for x,y in forbidden if y>a),default=len(text))
            for b in ends:
                if b>limit:
                    break
                if not text.startswith(suffix,b):
                    continue
                if c.get("line_reference") and re.fullmatch(LINE_REFERENCE, text[a:b]) is None:
                    continue
                if c.get("numeric_text") and re.fullmatch(NUMBER,text[a:b]) is None:
                    continue
                if c.get("balanced_pairs") and not regions.balanced(
                        pieces[bisect_right(boundaries,a)-1:bisect_right(boundaries,b)-1],c["balanced_pairs"]):
                    continue
                count,remainder = visit(index+1,b+len(suffix))
                total+=count
                for tail in (remainder if witness_limit is None else remainder[:max(0,witness_limit-len(witnesses))]):
                    witnesses.append(((part["name"],part["type"],a,b),*tail))
        if part["optional"]:
            count,remainder = visit(index+1,position)
            total+=count
            for tail in (remainder if witness_limit is None else remainder[:max(0,witness_limit-len(witnesses))]):
                witnesses.append(((part["name"],part["type"],None,None),*tail))
        return total,tuple(witnesses)

    count,chosen = visit(0,0)
    witnesses=[[dict(name=name,type=kind,value=None if a is None else text[a:b],
                 span=None if a is None else [start+len(text[:a].encode("utf-8","surrogateescape")),
                                              start+len(text[:b].encode("utf-8","surrogateescape"))])
            for name,kind,a,b in witness] for witness in chosen]
    return dict(count=count,captures=witnesses[0] if count==1 else None,witnesses=witnesses)


def display_pattern(parts):
    return "".join(p["text"] if p["kind"]=="literal" else
        p["prefix"]+"<"+p["type"]+">"+p["suffix"] for p in parts)
