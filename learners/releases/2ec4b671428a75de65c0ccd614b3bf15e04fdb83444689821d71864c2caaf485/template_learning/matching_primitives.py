"""Extracted native matching mechanics; all executable declarations are supplied.

No inference, rule-file access, lexer or occurrence binding lives here.
"""
from bisect import bisect_right
from functools import lru_cache
import json
import re
import string
import unicodedata
from .full_ids import FullIdRules
from .continuations import match_components
from . import location_sequences, formatted_literals

SLOT_TYPES = ("KEY", "OPTIONAL_KEY", "PARAM", "LOCATOR", "VALUE", "REASON", "CHARACTER_FULL_ID", "HOUSE_FULL_ID", "TITLE_FULL_ID", "CHARACTER_ID_SHORT", "CHARACTER_ID_SUPER_SHORT")
NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
LINE_REFERENCE = r"[0-9]+(?:-[0-9]+)?"

class MatcherError(ValueError):
    """Base error; never ordinary no-match."""

class MatcherIntegrityError(MatcherError):
    """Pinned bytes or result/input correspondence disagree."""

class MatcherCompatibilityError(MatcherError):
    """Unsupported API, parser, model or selector."""

class MatcherDeclarationError(MatcherError):
    """Invalid or conflicting model declarations."""

class NativeInputError(MatcherError):
    """Incomplete input or a declaration boundary unavailable in native pieces."""


def punctuation_piece(kind, text):
    """Classify an existing parser piece; never split or normalize its text."""
    return kind == "token" and bool(text) and all(
        c in string.punctuation or unicodedata.category(c).startswith("P") for c in text)


@lru_cache(maxsize=16384)
def quoted_piece_ranges(pieces, quote="'", allow_multiline=False, allow_punctuated_close=False):
    """Locate unambiguous paired quote tokens in the original parser pieces.

    This establishes boundaries, never slot types. Nested, unmatched or ambiguous
    quotes abstain; word-internal apostrophes remain interior data. Discovery
    keeps its single-line restriction; field recognition can also defer to an
    enclosing multiline quotation without consuming its contents. Deferral can
    allow punctuation before a closing quote; discovery retains its stricter
    ambiguity check. This conservative deferral does not declare an outer PARAM.
    """
    ranges, opened = [], None
    for index, piece in enumerate(pieces):
        if piece != ('token', quote):
            continue
        left = pieces[index-1] if index else None
        right = pieces[index+1] if index+1 < len(pieces) else None
        can_open = left is None or left[0] == 'gap' or punctuation_piece(*left)
        can_close = right is None or right[0] == 'gap' or punctuation_piece(*right)
        if opened is None:
            if not can_open or (can_close and right != ('token', quote)):
                return (), 'ambiguous_quote_boundaries'
            opened = index
        elif can_close:
            if can_open and index != opened + 1 and not allow_punctuated_close:
                return (), 'ambiguous_quote_boundaries'
            if not allow_multiline and any('\n' in text or '\r' in text for _, text in pieces[opened+1:index]):
                return (), 'multiline_quote_boundaries'
            ranges.append((opened, index+1))
            opened = None
        elif can_open:
            return (), 'nested_quote_boundaries'
    if opened is not None:
        return (), 'unclosed_quote'
    return tuple(ranges), None


def key_piece_sequence(pieces, joiners):
    """One identifier or adjacent qualified identifiers; never retokenize."""
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


def pattern_identity(parts):
    """Structural identity excludes example values and support frequencies."""
    return [{k:v for k,v in p.items() if k not in {"observed_values","observed_absence","inference_basis","inference_rule","field_support","rejection_reason","parameter_definition","empirical_region"}}
            for p in parts]


@lru_cache(maxsize=4096)
def _matching_plan(material):
    result = json.loads(material)
    if any(p["kind"] == "slot" and p["type"] not in SLOT_TYPES for p in result):
        raise MatcherDeclarationError("unsupported slot type")
    allowed = {"parser_boundaries", "literal_punctuation", "literal_guidance", "single_token", "key_joiners",
               "location_value", "numeric_text", "line_reference", "balanced_pairs", "declared_field", "full_id", "parameter_structure"}
    if any(set(p["constraints"]) - allowed for p in result if p["kind"] == "slot"):
        raise MatcherDeclarationError("unsupported slot constraint")
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


def display_pattern(parts):
    return "".join('<LOCATOR entries: one or more>' if p['kind']=='repeat' else ('{' + '|'.join(p['alternatives']) + '}' if 'alternatives' in p else p['text']) if p["kind"]=="literal" or p['kind']=='repeat' else
        p["prefix"]+"<"+p["type"]+">"+p["suffix"] for p in parts)


def guided_ranges(pieces, wording):
    # Serialized wrapper pieces are lists; native message pieces are tuples.
    # Canonicalize only containers for caching, never their kind/text content.
    return _guided_ranges(tuple((kind,value) for kind,value in pieces),tuple(wording))


@lru_cache(maxsize=16384)
def _guided_ranges(pieces, wording):
    """Return exact character ranges aligned with complete existing pieces.

    `target_key` and `@target` stay intact: an interior substring cannot satisfy
    the boundary requirement. Multiword guidance retains its exact native gaps.
    """
    text = "".join(value for _,value in pieces)
    boundaries,offset = {0},0
    for _,value in pieces:
        offset += len(value)
        boundaries.add(offset)
    ranges = set()
    for literal in wording:
        start = text.find(literal)
        while start >= 0:
            end = start + len(literal)
            if start in boundaries and end in boundaries:
                ranges.add((start,end))
            start = text.find(literal,start+1)
    return tuple(sorted(ranges))


def balanced(pieces, pairs):
    mapping = dict(pairs)
    closers = set(mapping.values())
    stack = []
    for kind, text in pieces:
        if kind != "token":
            continue
        if text in mapping:
            stack.append(mapping[text])
        elif text in closers:
            if not stack or stack.pop() != text:
                return False
    return not stack



class Rules:
    """One model's supplied declarations, usable before or after publication."""
    def __init__(self, declarations):
        self.declarations = declarations
        constructions = declarations['constructions']
        self.constructions = {d['id']: d for d in constructions}
        self.compiled_constructions = [(d,re.compile(d['pattern'])) for d in constructions]
        definitions = declarations['parameter_structures']
        self.parameter_definitions = {d['id']: d for d in definitions}
        self.full_ids = FullIdRules(definitions)
        self.compiled_parameters = [(d,re.compile(d['prefix']),re.compile(d['content']) if d['mechanic']=='line_sequence' else None)
            for d in definitions if d['mechanic']!='full_id']
        cues = declarations['slot_position_cues']
        flags = 0 if cues['case_sensitive'] else re.I
        self.location_cue = re.compile(cues['location_pattern'],flags)
        self.unavailable_location_cue = re.compile(cues['unavailable_location_pattern'], flags)
        self.path_value_cue = re.compile(cues['path_value_context_pattern'])
        self.file_value_cue = re.compile(cues['filename_context_pattern'],flags)
        self.filename_suffixes = frozenset(cues['filename_suffixes'])


    @lru_cache(maxsize=16384)
    def location_piece_ranges(self, pieces):
        """Find paths, bare filenames and separate line fields in original pieces."""
        paths = dict(path_piece_ranges(pieces))
        result, before, i = ([], '', 0)
        while i < len(pieces):
            end = paths.get(i, i + 1)
            kind, text = pieces[i]
            is_path = i in paths
            ordinary = kind == 'token' and (not punctuation_piece(kind, text))
            file_end = filename_field_end(pieces, i) if ordinary and self.file_value_cue.search(before) else None
            if file_end is not None:
                end = file_end
            final = pieces[end - 1][1]
            filename = filename_sequence(pieces[i:end])
            line_index = line_after_filename(pieces, end) if filename else None
            known_suffix = filename and any((final.casefold().endswith(ext) for ext in self.filename_suffixes))
            recognized = file_end is not None or known_suffix or line_index is not None or (is_path and (self.location_cue.search(before) or self.path_value_cue.search(before) or filename)) or (not is_path and ordinary and self.location_cue.search(before))
            # Section markers can introduce the explicit unavailable value.
            # Do not capture the nested "file" label in Script location: file:.
            if (ordinary and text == 'Unknown'
                    and self.unavailable_location_cue.search(before)):
                recognized = True
            if recognized:
                result.append((i, end))
                if line_index is not None:
                    result.append((line_index, line_index + 1))
            before += ''.join((t for _, t in pieces[i:end]))
            i = end
        return tuple(sorted(set(result)))


    @lru_cache(maxsize=16384)
    def location_piece_indices(self, pieces):
        return tuple((i for a, b in self.location_piece_ranges(pieces) for i in range(a, b)))


    @lru_cache(maxsize=16384)
    def location_capture_ends(self, pieces):
        offsets, cursor = ([], 0)
        for _, text in pieces:
            offsets.append(cursor)
            cursor += len(text)
        offsets.append(cursor)
        return {offsets[a]: offsets[b] for a, b in self.location_piece_ranges(pieces)}


    @lru_cache(maxsize=16384)
    def parameter_piece_ranges(self, pieces, source):
        declared = self.field_ranges(source, ''.join((t for _, t in pieces)), pieces)
        fields = self.parameter_field_ranges(tuple(pieces), tuple(((a, v[0]) for a, v in declared.items())), source)
        found = location_sequences.sequence(tuple(pieces))
        return {a:v for a,v in fields.items() if found is None or a < found['start_piece']}


    def analyze_match_pattern(self, parts, text, start=0, *, pieces, witness_limit=2):
        """Count every complete assignment in a memoized acyclic search.

        Two witnesses suffice to demonstrate ambiguity; witness_limit=None exports
        every complete assignment for deterministic selection. The count is exact and
        includes every successful branch. No inference spans or observed spellings
        are consulted, and a matching prefix is never a complete assignment.
        """
        if ''.join((t for _, t in pieces)) != text:
            raise NativeInputError("matching requires the selected parser's exact pieces")
        if any(p['kind']=='repeat' for p in parts):
            expanded, _, expected = location_sequences.expand(parts,pieces=pieces)
            if expanded is None:
                return dict(count=0,captures=None,witnesses=[])
            assessment = self.analyze_match_pattern(expanded,text,start,pieces=pieces,witness_limit=None)
            witnesses = [w for w in assessment['witnesses']
                         if [c for c in w if c['name'].startswith('locations_')]==expected]
            return dict(count=len(witnesses),captures=witnesses[0] if len(witnesses)==1 else None,witnesses=witnesses)
        if (parts and parts[0]['kind'] == 'literal'
                and 'literal_format' not in parts[0]
                and not text.startswith(tuple(parts[0].get('alternatives', [parts[0]['text']])))):
            return dict(count=0, captures=None, witnesses=[])
        plan = _matching_plan(json.dumps(pattern_identity(parts), sort_keys=True, ensure_ascii=True))
        pieces = tuple((tuple(p) for p in pieces))
        boundaries, starts, punctuation = _piece_index(pieces)
        boundary_set = set(boundaries)
        protected = {tuple(p['constraints'].get('literal_guidance', ())) for p in plan if p['kind'] == 'slot'}
        guides = {w: guided_ranges(pieces, w) for w in protected}

        @lru_cache(maxsize=None)
        def visit(index, position):
            if index == len(plan):
                return (1, ((),)) if position == len(text) else (0, ())
            part = plan[index]
            if part['kind'] == 'literal':
                if 'literal_format' in part:
                    value = formatted_literals.spelling(part, text, position)
                    return visit(index + 1, position + len(value)) if value is not None and position in boundary_set and position+len(value) in boundary_set else (0, ())
                # Validated choices are nonempty, prefix-free declared labels.
                literal = next((s for s in part.get('alternatives', [part['text']])
                                if text.startswith(s, position)), None)
                return visit(index + 1, position + len(literal)) if literal is not None else (0, ())
            prefix, suffix, c = (part['prefix'], part['suffix'], part['constraints'])
            total, witnesses = (0, [])
            a = position + len(prefix)
            if text.startswith(prefix, position) and a in boundary_set:
                if c.get('declared_field'):
                    field = c['declared_field']
                    span = self.capture_range(field['construction'], field['field'], text)
                    ends = (span[1],) if span is not None and span[0] == a else ()
                elif c.get('full_id'):
                    field = c['full_id']
                    end = self.full_ids.capture_ends(pieces, field['source'], field['definition']).get(a)
                    ends = (end,) if end is not None else ()
                elif c.get('parameter_structure'):
                    field = c['parameter_structure']
                    end = self.parameter_capture_ends(pieces, field['source'], field['definition']).get(a)
                    ends = (end,) if end is not None else ()
                elif c.get('location_value'):
                    end = self.location_capture_ends(pieces).get(a)
                    ends = (end,) if end is not None else ()
                elif c.get('single_token'):
                    piece = starts.get(a)
                    ends = (a + len(piece[1]),) if piece and piece[0] == 'token' else ()
                elif 'key_joiners' in c:
                    ends = key_capture_ends(pieces, tuple(c['key_joiners'])).get(a, ())
                else:
                    ends = boundaries[bisect_right(boundaries, a):]
                forbidden = guides[tuple(c.get('literal_guidance', ()))]
                if c.get('literal_punctuation'):
                    forbidden = (*forbidden, *punctuation)
                limit = min((max(a, x) for x, y in forbidden if y > a), default=len(text))
                for b in ends:
                    if b > limit:
                        break
                    if not text.startswith(suffix, b):
                        continue
                    if c.get('line_reference') and re.fullmatch(LINE_REFERENCE, text[a:b]) is None:
                        continue
                    if c.get('numeric_text') and re.fullmatch(NUMBER, text[a:b]) is None:
                        continue
                    if c.get('balanced_pairs') and (not balanced(pieces[bisect_right(boundaries, a) - 1:bisect_right(boundaries, b) - 1], c['balanced_pairs'])):
                        continue
                    count, remainder = visit(index + 1, b + len(suffix))
                    total += count
                    for tail in remainder if witness_limit is None else remainder[:max(0, witness_limit - len(witnesses))]:
                        witnesses.append(((part['name'], part['type'], a, b), *tail))
            if part['optional']:
                count, remainder = visit(index + 1, position)
                total += count
                for tail in remainder if witness_limit is None else remainder[:max(0, witness_limit - len(witnesses))]:
                    witnesses.append(((part['name'], part['type'], None, None), *tail))
            return (total, tuple(witnesses))
        count, chosen = visit(0, 0)
        witnesses = [[dict(name=name, type=kind, value=None if a is None else text[a:b], span=None if a is None else [start + len(text[:a].encode('utf-8', 'surrogateescape')), start + len(text[:b].encode('utf-8', 'surrogateescape'))]) for name, kind, a, b in witness] for witness in chosen]
        return dict(count=count, captures=witnesses[0] if count == 1 else None, witnesses=witnesses)


    def match_pattern(self, parts, text, start=0, *, pieces):
        """Return captures only when the complete assignment is unique."""
        return self.analyze_match_pattern(parts, text, start, pieces=pieces)['captures']


    @lru_cache(maxsize=16384)
    def recognize(self, source, text):
        matches = [(d, m) for d, p in self.compiled_constructions if d['source'] == source and (m := p.fullmatch(text))]
        matched_ids = {d['id'] for d, _ in matches}
        matches = [(d, m) for d, m in matches if not matched_ids.intersection(d.get('excludes', ()))]
        if len(matches) > 1:
            raise MatcherDeclarationError('overlapping owner construction declarations')
        if not matches:
            return None
        declaration, matched = matches[0]
        return dict(id=declaration['id'], regions={name: dict(text=matched.group(name), characters=matched.span(name), span=[len(text[:p].encode('utf-8', 'surrogateescape')) for p in matched.span(name)]) for name in declaration['region_order']})


    def field_ranges(self, source, text, pieces):
        found = self.recognize(source, text)
        if found is None:
            return {}
        offsets, cursor = ({0: 0}, 0)
        for i, (_, value) in enumerate(pieces, 1):
            cursor += len(value)
            offsets[cursor] = i
        result = {}
        for name, field in self.constructions[found['id']]['fields'].items():
            start, end = found['regions'][name]['characters']
            if start not in offsets or end not in offsets:
                raise NativeInputError('declared field cuts through a raw parser piece')
            if start == end and (not field.get('allow_empty', False)):
                raise NativeInputError('declared field does not permit empty content')
            result[offsets[start]] = (offsets[end], found['id'], name, field['type'])
        return result


    def capture_range(self, construction, field, text):
        declaration = self.constructions[construction]
        found = self.recognize(declaration['source'], text)
        if found is None or found['id'] != construction:
            return None
        span = found['regions'][field]['characters']
        if span[0] == span[1] and (not declaration['fields'][field].get('allow_empty', False)):
            return None
        return span


    @lru_cache(maxsize=16384)
    def parameter_field_ranges(self, pieces, protected=(), source=None):
        text = ''.join((t for _, t in pieces))
        offsets = [0]
        for _, value in pieces:
            offsets.append(offsets[-1] + len(value))
        indices = {offset: i for i, offset in enumerate(offsets)}
        fields = self.full_ids.ranges(pieces, source, protected)
        for definition, prefix, content in self.compiled_parameters:
            if definition.get('source') and definition['source'] != source:
                continue
            for match in prefix.finditer(text):
                start = match.end()
                if start not in indices:
                    continue
                a = indices[start]
                if definition['mechanic'] == 'line_sequence':
                    found = content.match(text, start)
                    if found is None or found.end() not in indices:
                        continue
                    if any(not found.group(group).lstrip(definition.get('leading_modifiers', ''))[:1].isupper()
                           for group in definition.get('capitalized_starts', ())):
                        continue
                    b = indices[found.end()]
                elif definition['mechanic'] == 'balanced_interior':
                    opening, closing = definition['delimiters']
                    depth = 1
                    b = None
                    for i in range(a, len(pieces)):
                        kind, value = pieces[i]
                        if '\n' in value or '\r' in value:
                            break
                        if kind == 'token' and value == opening:
                            depth += 1
                        elif kind == 'token' and value == closing:
                            depth -= 1
                            if depth == 0:
                                b = i
                                break
                    if b is None:
                        continue
                elif definition['mechanic'] == 'through_balanced_suffix':
                    opening, closing = definition['delimiters']
                    depth = 0
                    b = None
                    for i in range(a, len(pieces)):
                        kind, value = pieces[i]
                        if '\n' in value or '\r' in value:
                            break
                        if kind == 'token' and value == opening:
                            depth += 1
                        elif kind == 'token' and value == closing:
                            if depth == 0:
                                break
                            depth -= 1
                            if depth == 0:
                                b = i + 1
                                break
                    if b is None:
                        continue
                    if not re.search(definition['content_required'], text[start:offsets[b]]):
                        continue
                else:
                    raise MatcherDeclarationError('unknown declared parameter mechanic')
                if a == b or any((x < b and a < y for x, y in (*protected, *((x, y[0]) for x, y in fields.items())))):
                    continue
                # A new inner reference must not split a larger quoted field.
                # Whole-interior references remain eligible. No slot is inferred
                # merely from a quotation; ordinary empirical inference owns it.
                enclosing = [
                    (left, right) for quote in definition.get('defer_inside_quotes', ())
                    for left, right in quoted_piece_ranges(pieces, quote, True, True)[0]
                    if left < a and b <= right - 1
                    and any(kind != 'gap' for kind, _ in (*pieces[left+1:a], *pieces[b:right-1]))]
                if enclosing:
                    continue
                fields[a] = (b, definition['id'])
        return fields


    @lru_cache(maxsize=16384)
    def parameter_capture_ends(self, pieces, source, definition):
        offsets = [0]
        for _, value in pieces:
            offsets.append(offsets[-1] + len(value))
        return {offsets[a]: offsets[b] for a, (b, d) in self.parameter_field_ranges(pieces, (), source).items()
                if d == definition}

    def applies_to_record(self, template, record):
        """Shared source/construction/field-structure gates before body matching."""
        if template['status'] == 'unresolved' or template['source_family'] != record.source_family:
            return False
        if template['context_kind'] != record.context_kind:
            return False
        construction = self.recognize(record.source_family, record.text)
        if template['construction_id'] != (construction['id'] if construction else None):
            return False
        structures = [v[1] for _, v in sorted(self.parameter_piece_ranges(record.pieces, record.source_family).items())]
        return template['parameter_structures'] == structures

    def match_record(self, template, record, *, capture_ambiguities=None):
        if not self.applies_to_record(template, record):
            return None
        assessment = self.analyze_match_pattern(template['parts'], record.text, pieces=record.pieces, witness_limit=None)
        captures = assessment['captures']
        if not assessment['count']:
            return None
        component_witnesses = []
        kept = []
        for witness in assessment['witnesses']:
            components = match_components(template.get('continuation'), record.continuations, witness)
            if components is not None:
                kept.append(witness)
                component_witnesses.append(components)
        if not kept:
            return None
        assessment = dict(count=len(kept), witnesses=kept, captures=kept[0] if len(kept) == 1 else None)
        captures = assessment['captures']
        contexts = {}
        ambiguous = assessment['count'] > 1
        for context_id, context in record.contexts.items():
            regions = {}
            for name in ('prefix', 'suffix'):
                possible = []
                for pattern in template['context_patterns'].get(name, []):
                    if pattern['status'] == 'unresolved':
                        continue
                    structures = [v[1] for _, v in sorted(self.parameter_piece_ranges(tuple(map(tuple, context[name]['pieces'])), record.source_family).items())]
                    if pattern['parameter_structures'] != structures:
                        continue
                    result = self.analyze_match_pattern(pattern['parts'], context[name]['text'], pieces=context[name]['pieces'], witness_limit=None)
                    if result['count']:
                        possible.append(dict(template_id=pattern['template_id'], captures=result['captures'], capture_count=result['count'], capture_witnesses=result['witnesses']))
                ambiguous = ambiguous or len(possible) > 1 or any((p['capture_count'] > 1 for p in possible))
                regions[name] = possible
            if not all(regions.values()):
                return None
            contexts[context_id] = regions
        if ambiguous:
            if capture_ambiguities is not None:
                capture_ambiguities.append(dict(template_id=template['template_id'], context_matches=contexts, component_witnesses=component_witnesses, **assessment))
            return None
        return dict(template_id=template['template_id'], captures=captures, context_matches=contexts, template_status=template['status'], component_witnesses=component_witnesses)

