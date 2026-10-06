"""Native repeated location entries inside one recovered message.

This does not recover, split, or join emissions. Section introducers remain in
the diagnostic wording. Every entry is bounded and every value is preserved.
"""
from copy import deepcopy
from functools import lru_cache
import re

_SECTION = re.compile(r'(?:Script location:[ \t]*|Stack trace:[ \t\r\n]*)')
_ENTRY = re.compile(r'(?P<file_label>(?:file|infile):[ \t]+)(?P<file>[^\r\n]+?)'
                    r'(?P<line_label>[ \t]+(?:near line:|line:)[ \t]+)(?P<line>[^\s()]+)'
                    r'(?:(?P<trace_open>[ \t]+\()(?P<trace>[^\r\n]*)(?P<trace_close>\)))?'
                    r'(?P<trailing>[ \t]*(?:\r?\n[ \t\r\n]*)?)')
_UNKNOWN = re.compile(r'(?P<unknown>Unknown)(?P<trailing>[ \t\r\n]*)\Z')


def slot(name, kind):
    return dict(kind='slot', name=name, type=kind, optional=False, prefix='', suffix='',
                constraints=dict(parser_boundaries=True, literal_punctuation=False,
                                 literal_guidance=[], **({'location_value':True} if kind=='LOCATOR' else {})))


@lru_cache(maxsize=16384)
def sequence(pieces):
    """Return one complete trailing section with native piece/character ranges."""
    text = ''.join(t for _,t in pieces)
    offsets, cursor = {0:0}, 0
    for i, (_, value) in enumerate(pieces):
        cursor += len(value)
        offsets[cursor] = i+1
    for section in _SECTION.finditer(text):
        start = section.end()
        if start not in offsets:
            continue
        entries, position = [], start
        while position < len(text):
            match = _ENTRY.match(text, position) or _UNKNOWN.match(text, position)
            if match is None or match.end() == position:
                break
            fields = ['unknown'] if match.groupdict().get('unknown') is not None else ['file','line']
            if match.groupdict().get('trace') is not None:
                fields.append('trace')
            if any(match.start(f) not in offsets or match.end(f) not in offsets for f in fields):
                break
            parts, captures, at = [], [], position
            for name in fields:
                a,b = match.span(name)
                if a > at:
                    parts.append(dict(kind='literal', text=text[at:a]))
                kind = 'PARAM' if name=='trace' else 'LOCATOR'
                parts.append(slot(name,kind))
                captures.append(dict(name=name, type=kind, value=text[a:b],
                    span=[len(text[:a].encode('utf-8','surrogateescape')),len(text[:b].encode('utf-8','surrogateescape'))]))
                at = b
            if match.end() > at:
                parts.append(dict(kind='literal',text=text[at:match.end()]))
            entries.append(dict(parts=parts,captures=captures))
            position = match.end()
        if entries and position == len(text):
            return dict(start_piece=offsets[start], end_piece=len(pieces), start=start, entries=entries)
    return None


def declaration(sequences):
    layouts = []
    for found in sequences:
        for entry in found['entries']:
            if entry['parts'] not in layouts:
                layouts.append(entry['parts'])
    import json
    layouts.sort(key=lambda p:json.dumps(p,sort_keys=True))
    return dict(kind='repeat', name='locations', structure='location_entries', minimum=1, layouts=layouts)


def expand(parts, *, pieces=None, choices=None):
    """Expand native entry layouts; count lives only in the occurrence's layout."""
    repeat = [p for p in parts if p['kind']=='repeat']
    if not repeat:
        if choices:
            raise ValueError('repeat choices without a repeated part')
        return parts, [], []
    if len(repeat)!=1 or parts[-1] is not repeat[0]:
        raise ValueError('location sequence must be the sole final repeated part')
    part = repeat[0]
    captures = []
    if pieces is not None:
        found = sequence(tuple(map(tuple,pieces)))
        if found is None:
            return None, None, None
        choices = []
        for entry in found['entries']:
            if entry['parts'] not in part['layouts']:
                return None, None, None
            choices.append(part['layouts'].index(entry['parts']))
            captures.extend({**c,'name':part['name']+'_'+str(len(choices)-1)+'_'+c['name']} for c in entry['captures'])
    if not isinstance(choices,list) or len(choices)<part['minimum']:
        raise ValueError('missing repeated location entries')
    # Prefix parts are immutable to this operation. Inference parts can carry
    # thousands of evidence rows; copying those per match is quadratic work.
    result = list(parts[:-1])
    for index, choice in enumerate(choices):
        if type(choice) is not int or not 0 <= choice < len(part['layouts']):
            raise ValueError('invalid location entry layout')
        for child in deepcopy(part['layouts'][choice]):
            if child['kind']=='slot':
                child['name']=part['name']+'_'+str(index)+'_'+child['name']
            result.append(child)
    return result, choices, captures


def validate(part):
    if (set(part)!= {'kind','name','structure','minimum','layouts'} or part['kind']!='repeat'
            or part['name']!='locations' or part['structure']!='location_entries'
            or part['minimum']!=1 or not isinstance(part['layouts'],list) or not part['layouts']):
        raise ValueError('invalid repeated location declaration')
    for parts in part['layouts']:
        fields = [p for p in parts if p['kind']=='slot']
        if [p['name'] for p in fields] not in (['unknown'],['file','line'],['file','line','trace']):
            raise ValueError('invalid location fields')
        for p in parts:
            if p['kind']=='literal':
                if set(p)!= {'kind','text'} or not isinstance(p['text'],str):
                    raise ValueError('invalid entry literal')
            elif p!=slot(p['name'],'PARAM' if p['name']=='trace' else 'LOCATOR'):
                raise ValueError('invalid entry slot')
