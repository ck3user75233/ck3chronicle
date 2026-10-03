"""Inventory punctuation-bearing native spans for manual grammar review.

Search buckets below are descriptive, not KEY recognition or learner rules.
Every span is made from the census's actual raw-parser pieces.
"""
import argparse
from collections import Counter,defaultdict
import json
import re
from pathlib import Path


def atom(piece):
    return piece[0]=='token' and any(c.isalnum() for c in piece[1])


def inspect(folder):
    colon=defaultdict(lambda:dict(rows=set(),occurrences=0,instances=0,values=Counter(),sources=Counter(),examples=[]))
    shapes=defaultdict(lambda:dict(rows=set(),occurrences=0,values=Counter(),examples=[]))
    for line in (folder/'native-messages.jsonl').open(encoding='utf-8'):
        row=json.loads(line);ps=row['pieces'];offsets=[0]
        for _,value in ps:offsets.append(offsets[-1]+len(value))
        found=defaultdict(list)
        for i in range(len(ps)-2):
            if not atom(ps[i]) or ps[i+1]!=['token',':'] or not atom(ps[i+2]):continue
            if i>=2 and ps[i-1]==['token',':'] and atom(ps[i-2]):continue
            j=i+3
            while j+1<len(ps) and ps[j]==['token',':'] and atom(ps[j+1]):j+=2
            start=offsets[i];end=offsets[j]
            prefix=row['native'][row['native'].rfind('\n',0,start)+1:start]
            context=('rich-text' if any(ord(c)<32 for _,t in ps[i:j] for c in t)
                     else 'trace-position' if 'file:' in prefix and 'line:' in prefix and '(' in prefix
                     else 'other')
            found[context,ps[i][1]].append((i,j))
        for key,spans in found.items():
            group=colon[key];group['rows'].add(row['record_id']);group['occurrences']+=row['occurrences']
            group['sources'][row['source']]+=row['occurrences'];group['instances']+=len(spans)*row['occurrences']
            for a,b in spans:
                value=''.join(t for _,t in ps[a:b]);group['values'][value]+=row['occurrences']
                if len(group['examples'])<3 and not any(x['value']==value for x in group['examples']):
                    group['examples'].append(dict(value=value,record_id=row['record_id'],source=row['source'],native=row['native'],pieces=ps[a:b],range=[a,b],provenance=row['example']))
        runs=[];a=0
        for i in range(len(ps)+1):
            if i==len(ps) or ps[i][0]=='gap':
                if i>a:runs.append((a,i))
                a=i+1
        per_shape=defaultdict(list)
        for a,b in runs:
            # Skip path runs in this separate inventory, never reinterpret them.
            if any(t in {'/','\\'} for _,t in ps[a:b]):continue
            while a<b and not atom(ps[a]):a+=1
            while b>a and not atom(ps[b-1]):b-=1
            if b-a<3:continue
            shape=' '.join('atom' if atom(p) else p[1] for p in ps[a:b])
            per_shape[row['source'],shape].append((a,b))
        for key,spans in per_shape.items():
            g=shapes[key];g['rows'].add(row['record_id']);g['occurrences']+=row['occurrences']
            for a,b in spans:
                v=''.join(t for _,t in ps[a:b]);g['values'][v]+=row['occurrences']
                if len(g['examples'])<2 and not any(x['value']==v for x in g['examples']):
                    g['examples'].append(dict(value=v,record_id=row['record_id'],native=row['native'],pieces=ps[a:b]))
    def save(groups,name,labels):
        result=[]
        for key,g in groups.items():
            result.append(dict(zip(labels,key),**{k:v for k,v in g.items() if k!='rows'},distinct_messages=len(g['rows']),distinct_values=len(g['values'])))
        result.sort(key=lambda g:-g['occurrences'])
        (folder/name).write_text(json.dumps(result,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
    save(colon,'colon-inventory.json',('context','left_atom'))
    save(shapes,'run-shapes.json',('source','shape'))
    print(f'{len(colon)} colon buckets, {len(shapes)} source/shape buckets; hypotheses only')


def selected_formulations(folder):
    """Report-only searches for observed fields; none are recognition rules.

    Delimiter queries describe the native evidence inspected in the report.
    They do not assign slot types, validate CK3 expressions, or feed learning.
    """
    groups=defaultdict(lambda:dict(rows=set(),occurrences=0,instances=0,
        sources=Counter(),values=Counter(),logs=set(),examples=[]))
    frame=re.compile(r'line:\s*\d+(?:-\d+)?\s+\(([^()\r\n]*)\)')
    for line in (folder/'native-messages.jsonl').open(encoding='utf-8'):
        row=json.loads(line);text=row['native'];ps=row['pieces'];offsets=[0]
        for _,value in ps:offsets.append(offsets[-1]+len(value))
        boundary={n:i for i,n in enumerate(offsets)}
        found=defaultdict(list)
        def add(group,a,b):
            assert a in boundary and b in boundary,(group,text[a:b])
            found[group].append((a,b))
        for m in frame.finditer(text):
            value=m[1]
            if ':' in value:add('Trace colon chains',*m.span(1))
            if '[args#' in value or '[hash#' in value:add('Decorated trace references',*m.span(1))
        # Find decorated spans beyond frames too, to test whether frame-only is
        # an adequate description rather than assuming it from the query above.
        for i in range(len(ps)-3):
            if not atom(ps[i]):continue
            j=i+1
            while (j+2<len(ps) and ps[j]==['token','['] and ps[j+2]==['token',']']
                   and re.fullmatch(r'(?:args|hash)#\d+',ps[j+1][1])):j+=3
            if j==i+1:continue
            while j+1<len(ps) and ps[j]==['token',':'] and atom(ps[j+1]):j+=2
            add('All decorated spans',offsets[i],offsets[j])
        if row['source']=='genedatabase.cpp':
            prefix='The following errors occurred when building attribute list for '
            if prefix in text:
                a=text.index(prefix)+len(prefix);b=len(text.rstrip('\r\n'))
                add('Gene attribute composite labels',a,b)
        if row['source'] in {'pdx_data_factory.cpp','pdx_gui_factory.cpp'}:
            a=b=None
            if 'Failed parsing data statement ' in text:
                lead="Failed parsing data statement '";tail="' for property '"
                if lead in text and tail in text:a=text.index(lead)+len(lead);b=text.index(tail,a)
            elif "Failed converting statement for '" in text:
                lead="Failed converting statement for '";a=text.index(lead)+len(lead);b=text.rfind("'")
            elif " in '" in text:
                a=text.index(" in '")+5;b=text.rfind("'")
            if a is not None and b>a and '(' in text[a:b] and ')' in text[a:b]:
                add('Diagnostic data-call expressions',a,b)
        if row['source']=='pdx_data_statementparser.cpp' and "Statement '" in text:
            a=text.index("Statement '")+len("Statement '");b=text.index("': ",a)
            add('Rejected statement with trailing content',a,b)
        if row['source']=='pdxassetutil.cpp' and 'for mesh [' in text:
            a=text.index('for mesh [')+len('for mesh [');b=text.index(']',a)
            if '|' in text[a:b]:add('Pipe-delimited mesh names',a,b)
        if row['source']=='pdx_gui_localize.cpp' and 'Failed parsing localized text: ' in text:
            a=text.index('Failed parsing localized text: ')+len('Failed parsing localized text: ')
            add('Localization expressions',a,len(text.rstrip('\r\n')))
        for i,(kind,value) in enumerate(ps):
            if kind=='token' and value.startswith('@') and any(c.isalnum() for c in value):
                add('Attached at-sign symbols',offsets[i],offsets[i+1])
        for name,spans in found.items():
            g=groups[name];g['rows'].add(row['record_id']);g['occurrences']+=row['occurrences'];g['sources'][row['source']]+=row['occurrences'];g['logs'].update(row['logs'])
            spans=sorted(set(spans));g['instances']+=len(spans)*row['occurrences']
            for a,b in spans:
                value=text[a:b];g['values'][value]+=row['occurrences']
                # Keep a native witness for every distinct spelling, so report
                # selection can favor informative variation over repetitions.
                if not any(e['value']==value for e in g['examples']):
                    left,right=boundary[a],boundary[b]
                    g['examples'].append(dict(value=value,native=text,source=row['source'],record_id=row['record_id'],
                        pieces=ps[left:right],range=[left,right],provenance=row['example']))
    output=[]
    for name,g in groups.items():
        output.append(dict(name=name,**{k:v for k,v in g.items() if k not in {'rows','logs'}},distinct_messages=len(g['rows']),distinct_values=len(g['values']),distinct_logs=len(g['logs'])))
    (folder/'selected-formulations.json').write_text(json.dumps(output,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
    for g in output:print(g['name'],g['occurrences'],g['distinct_values'],dict(g['sources']))


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--survey',type=Path,required=True)
    folder=cli.parse_args().survey
    inspect(folder)
    selected_formulations(folder)
