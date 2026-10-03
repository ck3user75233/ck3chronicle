"""Shared recognition of JSON-declared opaque entity references over raw pieces.

This module has no learner/model imports. Both matching routes supply the same
model-owned declarations. Names and ID values are never classified or normalized.
"""
from functools import lru_cache
import re

FULL_ID_TYPES = frozenset({'CHARACTER_FULL_ID', 'HOUSE_FULL_ID', 'TITLE_FULL_ID'})


class FullIdRules:
    def __init__(self, definitions):
        self.definitions = {}
        self.contexts = []
        for d in definitions:
            if d['mechanic'] != 'full_id':
                continue
            if d['id'] in self.definitions or d['slot_type'] not in FULL_ID_TYPES:
                raise ValueError('invalid full-ID declaration identity/type')
            if (len(d['delimiters']) != 2 or any(len(v) != 1 for v in d['delimiters'])
                    or not d['id_label'] or not all(isinstance(v, str) and v for v in d['id_label'])):
                raise ValueError('invalid full-ID marker tokens')
            tail = d['name_tail']
            if tail is not None and (not isinstance(tail['separator'], str)
                    or list(tail['value_token_counts']) != [0, 1]):
                raise ValueError('unsupported full-ID name tail')
            self.definitions[d['id']] = d
            if not d['contexts']:
                raise ValueError('full-ID recognition requires emitter contexts')
            for context in d['contexts']:
                if not isinstance(context['source'], str) or not context['source']:
                    raise ValueError('full-ID context requires a source')
                self.contexts.append((d, context['source'], re.compile(context['prefix']),
                    re.compile(context['guard']), re.compile(context['suffix'])))

    @lru_cache(maxsize=16384)
    def inspect(self, pieces, source):
        text = ''.join(t for _, t in pieces)
        offsets = [0]
        for _, value in pieces:
            offsets.append(offsets[-1] + len(value))
        indices = {value: i for i, value in enumerate(offsets)}
        tokens = [(i, value) for i, (kind, value) in enumerate(pieces) if kind == 'token']
        token_indices = {i: n for n, (i, _) in enumerate(tokens)}
        candidates = set()
        for d, family, prefix, guard, suffix in self.contexts:
            if family != source or guard.search(text) is None:
                continue
            opening, closing = d['delimiters']
            for match in prefix.finditer(text):
                a = indices.get(match.end())
                if a is None:
                    continue  # A declaration cannot divide a raw whitespace run.
                while a < len(pieces) and pieces[a][0] == 'gap':
                    a += 1  # Whole presentation gaps stay outside; never trim bytes.
                if a == len(pieces):
                    continue
                # The first parenthesis must be the ID suffix, not an earlier
                # reference or diagnostic clause. Lowercase name words are opaque.
                o = a
                while o < len(pieces):
                    kind, value = pieces[o]
                    if '\n' in value or '\r' in value or (kind == 'token' and value in (opening, closing)):
                        break
                    o += 1
                if o == len(pieces) or pieces[o] != ('token', opening):
                    continue
                n = token_indices[o]
                label = tuple(d['id_label'])
                if tuple(v for _, v in tokens[n+1:n+1+len(label)]) != label:
                    continue
                before = [(i, v) for i, v in tokens[:n] if i >= a]
                tail = d['name_tail']
                if tail is not None:
                    counts = [count for count in tail['value_token_counts']
                        if len(before) > count + 1 and before[-count-1][1] == tail['separator']]
                    if len(counts) != 1:
                        continue
                elif not before:
                    continue
                depth = 1
                b = o + 1
                while b < len(pieces):
                    kind, value = pieces[b]
                    if '\n' in value or '\r' in value:
                        break
                    if kind == 'token' and value == opening:
                        depth += 1
                    elif kind == 'token' and value == closing:
                        depth -= 1
                        if depth == 0:
                            if suffix.match(text, offsets[b+1]) is not None:
                                candidates.add((a, b+1, d['id']))
                            break
                    b += 1
        ordered = tuple(sorted(candidates))
        uncertain = tuple(x for x in ordered if any(x != y and x[0] < y[1] and y[0] < x[1] for y in ordered))
        return tuple(x for x in ordered if x not in uncertain), uncertain

    def ranges(self, pieces, source, protected=()):
        accepted, _ = self.inspect(tuple(pieces), source)
        return {a: (b, definition) for a, b, definition in accepted
                if not any(x < b and a < y for x, y in protected)}

    @lru_cache(maxsize=16384)
    def capture_ends(self, pieces, source, definition):
        offsets = [0]
        for _, value in pieces:
            offsets.append(offsets[-1] + len(value))
        return {offsets[a]: offsets[b] for a, (b, d) in self.ranges(pieces, source).items()
                if d == definition}
