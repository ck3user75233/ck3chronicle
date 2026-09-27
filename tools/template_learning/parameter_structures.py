"""Recognize declared opaque spans over native pieces.

Definitions are data in owner_rules.json. Recognition supplies inference ranges;
PARAM uses ordinary complete matching; full-ID types use shared structural bounds.
"""
from functools import lru_cache
import re
from template_learning.owner_rules import OWNER_RULES
from template_learning.full_ids import FullIdRules

DEFINITIONS=OWNER_RULES['parameter_structures']
BY_ID={d['id']:d for d in DEFINITIONS}
FULL_IDS=FullIdRules(DEFINITIONS)
COMPILED=[(d,re.compile(d['prefix']),re.compile(d['content']) if d['mechanic']=='line_sequence' else None)
          for d in DEFINITIONS if d['mechanic']!='full_id']


@lru_cache(maxsize=16384)
def field_ranges(pieces, protected=(), source=None):
    text=''.join(t for _,t in pieces)
    offsets=[0]
    for _,value in pieces:offsets.append(offsets[-1]+len(value))
    indices={offset:i for i,offset in enumerate(offsets)}
    fields=FULL_IDS.ranges(pieces,source,protected)
    for definition,prefix,content in COMPILED:
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


def declarations_for(pieces, protected, source):
    return field_ranges(tuple(pieces),tuple(protected),source)
