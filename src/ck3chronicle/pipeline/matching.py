"""Runtime constraint mechanics over unchanged pieces from the pinned parser.

Consumes only the selected release declarations. These matching mechanics follow
schema v3; learner inference and its mutable rule registry are not imported.
"""
from bisect import bisect_right
from functools import lru_cache
import re
import string
import unicodedata

NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
LINE_REFERENCE = r"[0-9]+(?:-[0-9]+)?"


class DeclarationBoundaryError(ValueError):
    """A selected declaration cannot address this message's native pieces."""


def punctuation_piece(kind, text):
    """Classify an existing parser piece; never split or normalize its text."""
    return kind == "token" and bool(text) and all(
        c in string.punctuation or unicodedata.category(c).startswith("P") for c in text)


def key_piece_sequence(pieces, joiners):
    """One identifier or adjacent qualified identifiers; never retokenize."""
    return bool(pieces) and len(pieces) % 2 == 1 and all(
        k == 'token' and (t in joiners if i % 2 else not punctuation_piece(k, t))
        for i, (k, t) in enumerate(pieces))


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


def _piece_index(pieces):
    boundaries, starts, punctuation, cursor = [0], {}, [], 0
    for kind,value in pieces:
        starts[cursor] = (kind,value)
        if punctuation_piece(kind,value):
            punctuation.append((cursor,cursor+len(value)))
        cursor += len(value)
        boundaries.append(cursor)
    return boundaries, starts, punctuation


def guided_ranges(pieces, wording):
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
    """Compiled matching declarations owned by one immutable model selection."""

    def __init__(self, rules):
        from template_learning.full_ids import FullIdRules
        self.full_ids = FullIdRules(rules['parameter_structures'])
        self.declarations = {d['id']: d for d in rules['constructions']}
        self.constructions = tuple((d, re.compile(d['pattern'])) for d in rules['constructions'])
        self.parameters = tuple((d, re.compile(d['prefix']),
            re.compile(d['content']) if d['mechanic'] == 'line_sequence' else None)
            for d in rules['parameter_structures'] if d['mechanic'] != 'full_id')
        cues = rules['slot_position_cues']
        flags = 0 if cues['case_sensitive'] else re.I
        self.location_cue = re.compile(cues['location_pattern'], flags)
        self.path_cue = re.compile(cues['path_value_context_pattern'])
        self.file_cue = re.compile(cues['filename_context_pattern'], flags)
        self.filename_suffixes = tuple(cues['filename_suffixes'])

    def recognize(self, source, text):
        matches = [(d,m) for d,p in self.constructions if d['source']==source and (m:=p.fullmatch(text))]
        matched_ids={d['id'] for d,_ in matches}
        matches=[(d,m) for d,m in matches if not matched_ids.intersection(d.get('excludes',()))]
        if len(matches)>1:
            raise DeclarationBoundaryError('overlapping owner construction declarations')
        if not matches:
            return None
        declaration, matched = matches[0]
        return dict(id=declaration['id'], regions={name:dict(text=matched.group(name),
            characters=matched.span(name), span=[len(text[:p].encode('utf-8','surrogateescape'))
            for p in matched.span(name)]) for name in declaration['region_order']})

    def field_ranges(self, source, text, pieces):
        found = self.recognize(source,text)
        if found is None:
            return {}
        offsets, cursor = {0:0},0
        for i,(_,value) in enumerate(pieces,1):
            cursor += len(value)
            offsets[cursor] = i
        result = {}
        for name,field in self.declarations[found['id']]['fields'].items():
            start,end = found['regions'][name]['characters']
            if start not in offsets or end not in offsets:
                raise DeclarationBoundaryError('declared field cuts through a raw parser piece')
            if start == end and not field.get('allow_empty', False):
                raise DeclarationBoundaryError('declared field does not permit empty content')
            result[offsets[start]] = (offsets[end], found['id'], name, field['type'])
        return result

    def capture_range(self, construction, field, text):
        declaration=self.declarations[construction]
        found=self.recognize(declaration['source'],text)
        if found is None or found['id']!=construction:
            return None
        span = found['regions'][field]['characters']
        if span[0] == span[1] and not declaration['fields'][field].get('allow_empty', False):
            raise DeclarationBoundaryError('declared field does not permit empty content')
        return span

    def parameter_ranges(self, pieces, protected=(), source=None):
        text=''.join(t for _,t in pieces)
        offsets=[0]
        for _,value in pieces:offsets.append(offsets[-1]+len(value))
        indices={offset:i for i,offset in enumerate(offsets)}
        fields=self.full_ids.ranges(tuple(pieces),source,protected)
        for definition,prefix,content in self.parameters:
            if definition.get('source') and definition['source']!=source:continue
            for match in prefix.finditer(text):
                start=match.end()
                if start not in indices:continue
                a=indices[start]
                if definition['mechanic']=='line_sequence':
                    found=content.match(text,start)
                    if found is None or found.end() not in indices:continue
                    b=indices[found.end()]
                elif definition['mechanic']=='balanced_interior':
                    opening,closing=definition['delimiters']
                    depth=1;b=None
                    for i in range(a,len(pieces)):
                        kind,value=pieces[i]
                        if '\n' in value or '\r' in value:break
                        if kind=='token' and value==opening:depth+=1
                        elif kind=='token' and value==closing:
                            depth-=1
                            if depth==0:b=i;break
                    if b is None:continue
                elif definition['mechanic']=='through_balanced_suffix':
                    opening,closing=definition['delimiters']
                    depth=0;b=None
                    for i in range(a,len(pieces)):
                        kind,value=pieces[i]
                        if '\n' in value or '\r' in value:break
                        if kind=='token' and value==opening:depth+=1
                        elif kind=='token' and value==closing:
                            if depth==0:break
                            depth-=1
                            if depth==0:b=i+1;break
                    if b is None:continue
                    if not re.search(definition['content_required'],text[start:offsets[b]]):continue
                else:
                    raise ValueError('unknown declared parameter mechanic')
                if a==b or any(x<b and a<y for x,y in (*protected,*((x,y[0]) for x,y in fields.items()))):
                    continue
                fields[a]=(b,definition['id'])
        return fields

    def structure(self, source, text, pieces):
        construction = self.recognize(source, text)
        declared = self.field_ranges(source, text, pieces)
        parameters = self.parameter_ranges(pieces,
            tuple((a, v[0]) for a, v in declared.items()), source)
        return (construction['id'] if construction else None,
                tuple(value[1] for _, value in sorted(parameters.items())))

    def location_piece_ranges(self, pieces):
        """Find paths, bare filenames and separate line fields in original pieces."""
        paths = dict(path_piece_ranges(pieces))
        result, before, i = [], "", 0
        while i < len(pieces):
            end = paths.get(i, i + 1)
            kind, text = pieces[i]
            is_path = i in paths
            ordinary = kind == "token" and not punctuation_piece(kind, text)
            file_end = filename_field_end(pieces, i) if ordinary and self.file_cue.search(before) else None
            if file_end is not None:
                end = file_end
            final = pieces[end-1][1]
            filename = filename_sequence(pieces[i:end])
            line_index = line_after_filename(pieces, end) if filename else None
            known_suffix = filename and any(final.casefold().endswith(ext) for ext in self.filename_suffixes)
            recognized = (file_end is not None or known_suffix or line_index is not None
                or is_path and (self.location_cue.search(before) or self.path_cue.search(before) or filename)
                or not is_path and ordinary and self.location_cue.search(before))
            if recognized:
                result.append((i, end))
                if line_index is not None:
                    result.append((line_index, line_index+1))
            before += "".join(t for _, t in pieces[i:end])
            i = end
        return tuple(sorted(set(result)))

    def location_capture_ends(self, pieces):
        # Matching applies the same structural evidence as inference. An arbitrary
        # word must not satisfy a bare filename LOCATOR merely by being one token.
        offsets, cursor = [], 0
        for _, text in pieces:
            offsets.append(cursor)
            cursor += len(text)
        offsets.append(cursor)
        return {offsets[a]: offsets[b] for a, b in self.location_piece_ranges(pieces)}

    def analyze(self, parts, text, start=0, *, pieces, witness_limit=None):
        """Count every complete assignment in a memoized acyclic search.

        Two witnesses suffice to demonstrate ambiguity; the count is exact and
        includes every successful branch. No inference spans or observed spellings
        are consulted, and a matching prefix is never a complete assignment.
        """
        if "".join(t for _,t in pieces) != text:
            raise ValueError("matching requires the selected parser's exact pieces")
        if parts and parts[0]["kind"] == "literal" and not text.startswith(parts[0]["text"]):
            return dict(count=0,captures=None,witnesses=[])
        plan = parts
        pieces = tuple(tuple(p) for p in pieces)
        boundaries,starts,punctuation = _piece_index(pieces)
        boundary_set = set(boundaries)
        protected = {tuple(p["constraints"].get("literal_guidance",())) for p in plan if p["kind"] == "slot"}
        guides = {w:guided_ranges(pieces,w) for w in protected}
        locations = self.location_capture_ends(pieces) if any(
            p['kind'] == 'slot' and p['constraints'].get('location_value') for p in plan) else {}
        joins = {tuple(p['constraints']['key_joiners']) for p in plan
                 if p['kind'] == 'slot' and 'key_joiners' in p['constraints']}
        keys = {joiners: key_capture_ends(pieces, joiners) for joiners in joins}

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
                    span=self.capture_range(field['construction'],field['field'],text)
                    ends=(span[1],) if span is not None and span[0]==a else ()
                elif c.get('full_id'):
                    field=c['full_id']
                    end=self.full_ids.capture_ends(pieces,field['source'],field['definition']).get(a)
                    ends=(end,) if end is not None else ()
                elif c.get("location_value"):
                    end = locations.get(a)
                    ends = (end,) if end is not None else ()
                elif c.get("single_token"):
                    piece = starts.get(a)
                    ends = (a+len(piece[1]),) if piece and piece[0] == "token" else ()
                elif 'key_joiners' in c:
                    ends = keys[tuple(c['key_joiners'])].get(a, ())
                else:
                    ends = boundaries[bisect_right(boundaries,a):]
                forbidden = guides[tuple(c.get("literal_guidance",()))]
                if c.get("literal_punctuation"):
                    forbidden = (*forbidden,*punctuation)
                limit = min((max(a,x) for x,y in forbidden if y>a),default=len(text))
                for b in ends:
                    if b>limit:
                        break
                    # Constraints compose: choosing a narrow set of candidate
                    # ends above must not bypass another declared restriction.
                    if b not in boundary_set:
                        continue
                    if c.get('location_value') and locations.get(a) != b:
                        continue
                    if 'key_joiners' in c and b not in keys[tuple(c['key_joiners'])].get(a, ()):
                        continue
                    if c.get('single_token') and (starts.get(a, (None, ''))[0] != 'token'
                                                 or b != a + len(starts[a][1])):
                        continue
                    if not text.startswith(suffix,b):
                        continue
                    if c.get("line_reference") and re.fullmatch(LINE_REFERENCE, text[a:b]) is None:
                        continue
                    if c.get("numeric_text") and re.fullmatch(NUMBER,text[a:b]) is None:
                        continue
                    if c.get("balanced_pairs") and not balanced(
                            pieces[bisect_right(boundaries,a)-1:bisect_right(boundaries,b)-1],c["balanced_pairs"]):
                        continue
                    count,remainder = visit(index+1,b+len(suffix))
                    total+=count
                    for tail in remainder if witness_limit is None else remainder[:max(0,witness_limit-len(witnesses))]:
                        witnesses.append(((part["name"],part["type"],a,b),*tail))
            if part["optional"]:
                count,remainder = visit(index+1,position)
                total+=count
                for tail in remainder if witness_limit is None else remainder[:max(0,witness_limit-len(witnesses))]:
                    witnesses.append(((part["name"],part["type"],None,None),*tail))
            return total,tuple(witnesses)

        count,chosen = visit(0,0)
        witnesses=[[dict(name=name,type=kind,value=None if a is None else text[a:b],
                     span=None if a is None else [start+len(text[:a].encode("utf-8","surrogateescape")),
                                                  start+len(text[:b].encode("utf-8","surrogateescape"))])
                for name,kind,a,b in witness] for witness in chosen]
        return dict(count=count,captures=witnesses[0] if count==1 else None,witnesses=witnesses)
