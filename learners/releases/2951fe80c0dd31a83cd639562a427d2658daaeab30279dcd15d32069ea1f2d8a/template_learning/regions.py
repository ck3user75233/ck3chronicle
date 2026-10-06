"""Empirical boundary evidence over aligned native pieces; no CK3 format rules."""
from .matching_primitives import balanced, punctuation_piece
import string
import unicodedata
from functools import lru_cache
from template_learning.owner_rules import INFERENCE_POLICY

PAIRS = {a:b for a,b in INFERENCE_POLICY['marker_pairs'].items() if a!=b}
# These are proposal exclusions, not lexer separators or deleted literals.
EXCLUDED_MARKERS = frozenset(INFERENCE_POLICY['excluded_region_markers'])


@lru_cache(maxsize=16384)
def discovery_quote_ranges(pieces):
    """Propose unambiguous single-quoted ranges for discovery comparison only.

    Interior words provide no similarity evidence. No slot type is established
    here: inference still sees every native piece. Nested, unmatched or ambiguous
    quotes abstain for the message; word-internal apostrophes inside a proposed
    quotation remain interior data. Existing opaque-field ownership is checked
    by the comparison consumer.
    """
    ranges, opened = [], None
    for index, piece in enumerate(pieces):
        if piece != ('token', "'"):
            continue
        left = pieces[index-1] if index else None
        right = pieces[index+1] if index+1 < len(pieces) else None
        can_open = left is None or left[0] == 'gap' or punctuation_piece(*left)
        can_close = right is None or right[0] == 'gap' or punctuation_piece(*right)
        if opened is None:
            if not can_open or (can_close and right != ('token', "'")):
                return (), 'ambiguous_quote_boundaries'
            opened = index
        elif can_close:
            if can_open and index != opened + 1:
                return (), 'ambiguous_quote_boundaries'
            if any('\n' in text or '\r' in text for _, text in pieces[opened+1:index]):
                return (), 'multiline_quote_boundaries'
            ranges.append((opened, index+1))
            opened = None
        elif can_open:
            return (), 'nested_quote_boundaries'
    if opened is not None:
        return (), 'unclosed_quote'
    return tuple(ranges), None


def enclosing_pair(records, spans):
    """Corresponding complete raw separators, not characters at string edges.

    Asymmetric separators must be an actual matched pair in every member.
    Quotes are weaker: aligned endpoints propose them, and complete capture
    replay must still disambiguate their use. Interior quotes are not stripped.
    """
    observed = set()
    for record, (start, end) in zip(records, spans):
        left, right = start - 1, end
        while left >= 0 and record.pieces[left][0] == 'gap':
            left -= 1
        while right < len(record.pieces) and record.pieces[right][0] == 'gap':
            right += 1
        if left < 0 or right >= len(record.pieces):
            return None
        a, b = record.pieces[left], record.pieces[right]
        if a[0] != 'token' or b[0] != 'token' or INFERENCE_POLICY['marker_pairs'].get(a[1]) != b[1]:
            return None
        if a[1] != b[1] and (left, right) not in nesting(record.pieces)[1]:
            return None
        observed.add((a[1], b[1]))
    return next(iter(observed)) if len(observed) == 1 else None


def field_evidence(part,records,spans):
    """Assess a varying field in its own candidate, not in a source-wide pool."""
    values=part['observed_values']
    pair=enclosing_pair(records,spans)
    paired=pair is not None
    structured=all(any(not c.isalnum() and not c.isspace() for c in v) for v in values)
    observed_variation=len({v for v in values if v.strip()})>=INFERENCE_POLICY['param_min_distinct_nonempty']
    supported=observed_variation and paired
    return dict(observed_variation=observed_variation,paired_boundaries=paired,
                enclosing_pair=pair, enclosure_strength=('brackets' if pair[0]!=pair[1] else 'aligned_quotes') if pair else None,
                structured_values=structured, word_only_review=not paired,
                supported=supported)


@lru_cache(maxsize=16384)
def marker(unit):
    return (len(unit) == 2 and unit[0] == "token" and bool(unit[1])
            and all(c in string.punctuation or unicodedata.category(c).startswith("P") for c in unit[1]))


@lru_cache(maxsize=16384)
def nesting(sequence):
    """Observed nesting coordinates; unmatched markers carry no paired evidence."""
    stack, coordinates, pairs = [], {}, []
    for index, unit in enumerate(sequence):
        if len(unit) != 2 or unit[0] != "token":
            continue
        text = unit[1]
        if text in PAIRS:
            stack.append((index, text))
        elif text in PAIRS.values():
            if stack and PAIRS[stack[-1][1]] == text:
                start, opener = stack.pop()
                position = tuple(t for _, t in stack)
                coordinates[start] = ("open", opener, position)
                coordinates[index] = ("close", opener, position)
                pairs.append((start, index))
            else:
                stack.clear()
    return coordinates, pairs


@lru_cache(maxsize=16384)
def candidate_envelopes(pieces, excluded=()):
    """Propose outer balanced interiors before comparing any interior wording.

    These are hypotheses, not typed fields. Existing declared fields and
    locations retain ownership. Nested interiors stay inside the outer proposal.
    Symmetric quotes continue through the existing rank-based quote handling;
    nesting alone cannot disambiguate their endpoints.
    """
    selected = []
    for left, right in sorted(nesting(pieces)[1], key=lambda p: (p[0], -p[1])):
        if right <= left + 1:
            continue
        if any(a <= left and right <= b for a, b in selected):
            continue
        if any(a < right + 1 and left < b for a, b in excluded):
            continue
        selected.append((left, right))
    return tuple(selected)


def envelope_support(piece_values, *, atomic):
    """Assess member spans before aligning their interior wording.

    Boundaries propose a region; distinct values and raw multi-token content
    provide evidence, not proof of unbounded variation. Equal observed lengths
    are retained as evidence, never treated as a fixed-length constraint.
    KEY/LOCATOR precedence and complete boundary validation are separate.
    """
    return span_variation(piece_values,atomic=atomic)


def span_variation(piece_values, *, atomic):
    """Positive raw-span evidence; no whitespace or nesting prerequisites."""
    values={''.join(t for _,t in pieces) for pieces in piece_values}
    distinct=len({v for v in values if v.strip()})
    lengths=sorted({sum(k=='token' for k,_ in pieces) for pieces in piece_values})
    # A qualified KEY has several raw pieces, but already has a simpler type.
    # It must not supply PARAM evidence merely because another member fails KEY.
    multi=any(sum(k=='token' for k,_ in p)>1 and not single
              for p,single in zip(piece_values,atomic))
    return dict(supported=distinct>=INFERENCE_POLICY['param_min_distinct_nonempty'] and multi,
                distinct_nonempty=distinct,raw_token_counts=lengths,multi_token_content=multi,
                observed_length_variation=len(lengths)>1)


def supported_anchors(sequences, maps, stable, mandatory):
    """Repeated separators are not fixed boundaries merely because LCS aligned them.

    Keep aligned word evidence. A marker also needs consistent occurrence/rank
    between those words, or corresponding balanced nesting across observations.
    This operates only after observing a comparable pool; it hides no raw region.
    """
    ref = sequences[0]
    wording = [-1, *(i for i in stable if not marker(ref[i]) and ref[i][0] != "gap"), len(ref)]
    coords = [nesting(sequence)[0] for sequence in sequences]
    retained, decisions = [], []
    for index in stable:
        unit = ref[index]
        if index in mandatory or not marker(unit):
            retained.append(index)
            continue
        left = max(i for i in wording if i < index)
        right = min(i for i in wording if i > index)
        counts, ranks, reverse_ranks, positions, adjacency = [], [], [], [], []
        for seq, mapping, coordinate in zip(sequences, maps, coords):
            a = mapping[left]+1 if left >= 0 else 0
            b = mapping[right] if right < len(ref) else len(seq)
            point = mapping[index]
            counts.append(sum(u == unit for u in seq[a:b]))
            ranks.append(sum(u == unit for u in seq[a:point]))
            reverse_ranks.append(sum(u == unit for u in seq[point+1:b]))
            positions.append(coordinate.get(point))
            adjacency.append((left>=0 and all(u[0]=='gap' for u in seq[a:point]),
                              right<len(ref) and all(u[0]=='gap' for u in seq[point+1:b])))
        # Interior occurrences do not invalidate an aligned outer separator.
        # Both directions matter: a closing quote remains last even when the
        # native field contains additional quotes. No quote text is stripped.
        invariant = len(set(ranks)) == 1 or len(set(reverse_ranks)) == 1
        paired = positions[0] is not None and all(p == positions[0] for p in positions)
        adjacent=INFERENCE_POLICY['marker_adjacency'] and (
            all(a for a,_ in adjacency) or all(b for _,b in adjacency))
        if invariant or paired or adjacent:
            retained.append(index)
        else:
            decisions.append(dict(decision="rejected_boundary", marker=unit[1],
                reference_unit=index, counts=sorted(set(counts)),
                reason="separator count/rank varies between stable wording and has no shared nesting coordinate"))
    return retained, decisions


def supported_balance(piece_values):
    """Record only nesting properties actually supported by every observed value."""
    pairs = [list(pair) for pair in PAIRS.items()]
    return pairs if any(t in PAIRS or t in PAIRS.values() for p in piece_values for _, t in p) and all(
        balanced(p, pairs) for p in piece_values) else []


def evidence(records, spans):
    from template_learning.records import identity
    values, counts, punctuation, members = [], [], [], []
    for record, (a, b) in zip(records, spans):
        if not hasattr(record,'_evidence_offsets'):
            offsets=[0]
            for _,text in record.pieces:
                offsets.append(offsets[-1]+len(text.encode('utf-8','surrogateescape')))
            record._evidence_offsets=offsets
            record._evidence_identity=identity(record.key)
        pieces = record.pieces[a:b]
        value = "".join(t for _, t in pieces)
        values.append(value)
        counts.append(sum(k == "token" for k, _ in pieces))
        punctuation.append(tuple(t for k, t in pieces if marker((k, t))))
        members.append(dict(record_id=record._evidence_identity, pieces=[a,b],
                            bytes=[record._evidence_offsets[a],record._evidence_offsets[b]]))
    return dict(distinct_values=len(set(values)), nonempty_values=len(set(v for v in values if v)),
                token_counts=sorted(set(counts)), punctuation_patterns=[list(p) for p in sorted(set(punctuation))],
                members=members)


def envelope_review(records, sequences, maps, spans, stable, slots):
    """Inspect marker envelopes without assigning the envelope a slot type.

    Proposals require actual enclosing pairs and can occur anywhere. Stable interior
    wording and smaller inferred fields decide whether an envelope is divided,
    narrowed, accepted, or remains literal. Word-bounded proposals are recorded
    by the ordinary alignment's slot/constant assessment.
    """
    ref = sequences[0]
    markers = [i for i in stable if marker(ref[i]) and ref[i][1] not in EXCLUDED_MARKERS]
    possible = {(a,b) for a,b in nesting(ref)[1] if a in markers and b in markers}
    # Quotes are secondary aligned candidates; arbitrary adjacent punctuation
    # (including colon pairs and sentence endings) never proposes an envelope.
    for quote in (a for a,b in INFERENCE_POLICY['marker_pairs'].items() if a==b):
        positions=[i for i in markers if ref[i][1]==quote]
        possible.update(zip(positions[::2],positions[1::2]))
    result=[]
    for left,right in sorted(possible):
        if right-left <= 1:
            continue
        fields=[(bounds[mapping[left]][1],bounds[mapping[right]][0]) for bounds,mapping in zip(spans,maps)]
        if enclosing_pair(records,fields) is None:
            continue
        facts=evidence(records,fields)
        literals=[ref[i][1] for i in stable if left<i<right and ref[i][0]=='token' and not marker(ref[i])]
        inside=[(part,bounds) for part,bounds in slots if all(a<=x and y<=b for (a,b),(x,y) in zip(fields,bounds))]
        types=[p['type'] for p,_ in inside]
        if facts['distinct_values']==1:
            decision,reason='rejected','no observed variation supports a new slot for this envelope; existing location fields remain independently recognized'
        elif any(p['type']=='PARAM' and p['optional'] and len(p['observed_values'])==1 for p,_ in inside):
            decision,reason='insufficient','one nonempty spelling plus absence does not establish variable interior content'
        elif literals:
            decision,reason='divided','recurring interior wording remains literal; assess only smaller varying spans'
        elif len(inside)==1 and fields == inside[0][1]:
            decision,reason='accepted','ordinary slot assessment supports the variable interior'
        else:
            decision,reason='narrowed','alignment retains internal boundaries or several smaller fields'
        result.append(dict(proposal='marker_envelope',left=ref[left][1],right=ref[right][1],
                           decision=decision,reason=reason,interior_literals=literals,slot_types=types,**facts))
    return result
