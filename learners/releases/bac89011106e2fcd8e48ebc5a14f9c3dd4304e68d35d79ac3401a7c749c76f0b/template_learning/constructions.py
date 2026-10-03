"""Consume owner-declared envelopes; never learn independent submessage pools."""
from functools import lru_cache
import re
from template_learning.owner_rules import CONSTRUCTIONS

DECLARATIONS = {d['id']: d for d in CONSTRUCTIONS}
COMPILED = [(d, re.compile(d['pattern'])) for d in CONSTRUCTIONS]


@lru_cache(maxsize=16384)
def recognize(source, text):
    matches = [(d,m) for d,p in COMPILED if d['source']==source and (m:=p.fullmatch(text))]
    matched_ids={d['id'] for d,_ in matches}
    matches=[(d,m) for d,m in matches if not matched_ids.intersection(d.get('excludes',()))]
    if len(matches)>1:
        raise ValueError('overlapping owner construction declarations')
    if not matches:
        return None
    declaration, matched = matches[0]
    return dict(id=declaration['id'], regions={name:dict(text=matched.group(name),
        characters=matched.span(name), span=[len(text[:p].encode('utf-8','surrogateescape'))
        for p in matched.span(name)]) for name in declaration['region_order']})


def field_ranges(source, text, pieces):
    found = recognize(source,text)
    if found is None:
        return {}
    offsets, cursor = {0:0},0
    for i,(_,value) in enumerate(pieces,1):
        cursor += len(value)
        offsets[cursor] = i
    result = {}
    for name,field in DECLARATIONS[found['id']]['fields'].items():
        start,end = found['regions'][name]['characters']
        if start not in offsets or end not in offsets:
            raise ValueError('declared field cuts through a raw parser piece')
        if start == end and not field.get('allow_empty', False):
            raise ValueError('declared field does not permit empty content')
        result[offsets[start]] = (offsets[end], found['id'], name, field['type'])
    return result


def comparison_ranges(source,text):
    found=recognize(source,text)
    return [found['regions'][name]['span'] for name in DECLARATIONS[found['id']]['comparison_regions']] if found else [[0,len(text.encode('utf-8','surrogateescape'))]]


def identity(source,text):
    found=recognize(source,text)
    return found['id'] if found else None


def capture_range(construction, field, text):
    declaration=DECLARATIONS[construction]
    found=recognize(declaration['source'],text)
    if found is None or found['id']!=construction:
        return None
    span = found['regions'][field]['characters']
    if span[0] == span[1] and not declaration['fields'][field].get('allow_empty', False):
        return None
    return span
