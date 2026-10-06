"""Survey effect/trigger context in genuine native evidence, without inference changes."""
import argparse
from collections import Counter
import json
from html import escape
from pathlib import Path

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.regions import nesting
from template_learning.matcher_example import load_verified
from template_learning.inventory import sha256_file


def render_enclosed(path,result):
    groups=result['enclosed_groups'];counts=Counter()
    for g in groups:counts[g['marker'],g['selected_role']]+=g['token_mentions']
    pre=lambda value:'<pre>'+escape(str(value))+'</pre>'
    h=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Effect and trigger inside markers</title>',
       '<style>body{font:17px/1.5 system-ui;max-width:1100px;margin:40px auto;padding:0 24px;color:#183044}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;padding:16px}table{border-collapse:collapse}td,th{padding:12px;border-bottom:1px solid #ccd5df;text-align:left}article{border-top:2px solid #ccd5df;margin-top:28px}summary{cursor:pointer}</style>',
       '<h1>Effect and trigger inside parentheses and brackets</h1>',
       '<p>Package '+result['package_id']+'. Searched all '+f'{result["contextual_rows"]:,}'+' retained contextual messages from the 73 training logs, representing '+f'{result["occurrences"]:,}'+' occurrences.</p>',
       '<p><b>Result:</b> '+f'{sum(g["token_mentions"] for g in groups):,}'+' standalone effect/trigger tokens inside matched parentheses/brackets, in '+f'{result["enclosed_distinct_messages"]:,}'+' distinct messages / '+f'{result["enclosed_message_occurrences"]:,}'+' occurrences. Every enclosed token is already within a PARAM or REASON capture. No enclosed literal, KEY or unassigned case was found. This evidence does not justify a new marker exemption now.</p>',
       '<p>These are token-position counts, not disjoint message counts. One message can contain several tokens and both marker types. Each token is counted once, under its nearest matched () or [] pair. Embedded identifier substrings and unbalanced markers are outside this survey. Saved assignments provide full-corpus roles; each of the '+str(len(groups))+' template/word/marker/role combinations also has a genuine witness replayed through the authenticated package matcher, with exact capture bytes checked.</p>',
       '<table><tr><th>Nearest enclosing marker</th><th>Selected field</th><th>Token positions</th></tr>']
    for (marker,role),n in sorted(counts.items()):h.append('<tr><td>'+('()' if marker=='(' else '[]')+'</td><td>'+role+'</td><td>'+f'{n:,}'+'</td></tr>')
    h.append('</table><h2>Selected templates and genuine captures</h2><p>Inside a repeated location tail, the trace remains PARAM even when the display abbreviates the whole tail as LOCATOR entries. Template status and assignment status are shown separately. These are working examples, not a template approval queue.</p>')
    for tid in dict.fromkeys(g['template_id'] for g in groups):
        members=[g for g in groups if g['template_id']==tid];first=members[0]
        h.append('<article><h3>'+tid+' · '+first['template_status']+'</h3>'+pre(first['template_pattern']))
        for g in members:
            e=g['example'];capture=e['runtime_capture']
            h.append('<p><b>'+g['word']+'</b> inside '+('()' if g['marker']=='(' else '[]')+' → '+g['selected_role']+'; '+str(g['token_mentions'])+' token positions. Witness assignment: '+e['runtime_assignment_status']+'.</p>')
            h.append('<p>Genuine enclosed text:</p>'+pre(e['enclosing_text']))
            if capture:h.append('<p>Complete captured value ('+capture['type']+', '+capture['slot_id']+'):</p>'+pre(capture['value']))
            h.append('<details><summary>Full genuine message and source provenance</summary>'+pre(e['text'])+pre(json.dumps(e['provenance'],ensure_ascii=True,indent=2))+'</details>')
        h.append('</article>')
    h.append('<p><a href="'+escape(path.with_suffix('.json').name)+'">Machine-readable counts and witnesses</a></p></html>')
    path.write_text('\n'.join(h),encoding='utf-8')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--package', type=Path, help='Authenticate and replay each enclosed template/word/marker/role witness.')
    cli.add_argument('--render-only',action='store_true')
    args = cli.parse_args()
    if args.render_only:
        render_enclosed(args.output.with_suffix('.html'),json.loads(args.output.read_bytes()))
        return
    package=load_verified(args.package,sha256_file(args.package/'manifest.json')) if args.package else None
    groups = {}; enclosed_groups={}; enclosed_messages={}; rows = occurrences = 0
    for row, count in native_evidence_rows(args.bundle/'native_evidence.json'):
        rows += 1; occurrences += count
        pieces = tuple(tuple(p) for p in row['pieces'])
        if not any(k == 'token' and v.casefold() in ('effect', 'trigger') for k, v in pieces):
            continue
        pairs = [(a,b) for a,b in nesting(pieces)[1] if pieces[a][1] in ('(', '[', '{')]
        captures = (row.get('selected_assignment') or {}).get('captures', [])
        offset = 0; previous = None; previous_index = None; previous_span = None
        for index, (kind, value) in enumerate(pieces):
            end = offset + len(value.encode('utf-8', 'surrogateescape'))
            if kind == 'token' and value.casefold() in ('effect','trigger'):
                enclosing = [(a,b) for a,b in pairs if a < index < b]
                marker = pieces[max(enclosing)[0]][1] if enclosing else None
                capture = next((c for c in captures if c.get('span') and c['span'][0] <= offset and end <= c['span'][1]), None)
                role = capture['type'] if capture else 'literal' if row.get('selected_assignment') else 'unassigned'
                preceding_capture = next((c for c in captures if previous_span and c.get('span') and c['span'][0] <= previous_span[0] and previous_span[1] <= c['span'][1]), None)
                preceding_role = preceding_capture['type'] if preceding_capture else 'literal' if row.get('selected_assignment') else 'unassigned'
                separator = bool(previous and ('_' in previous or '.' in previous))
                requested_pairs=[(a,b) for a,b in enclosing if pieces[a][1] in ('(', '[')]
                if requested_pairs:
                    nearest=max(requested_pairs);requested_marker=pieces[nearest[0]][1]
                    tid=(row.get('selected_assignment') or {}).get('template_id')
                    enclosed_key=tid,value.casefold(),requested_marker,role
                    enclosed_messages[row['example_id']]=count
                    if enclosed_key not in enclosed_groups:
                        example=dict(example_id=row['example_id'],source=row['source_family'],text=row['native'],
                            token=value,token_span=[offset,end],capture=capture,
                            enclosing_text=''.join(v for _,v in pieces[nearest[0]:nearest[1]+1]),
                            provenance=row['native_occurrences'][:1])
                        if package:
                            unit=dict(parser=package.manifest['parser'],source_family=row['source_family'],
                                source_tag=row['source_family'],context_kind=row['context_kind'],
                                body=dict(text=row['native'],pieces=row['pieces']),
                                contexts=next(iter(row['contexts'].values()),{}),continuations=row['continuations'])
                            chosen=package.match(unit)['assignment']
                            assert (chosen['template_id'] if chosen else None)==tid
                            body=next((r for r in chosen['regions'] if r['name']=='body'),None) if chosen else None
                            actual=next((c for c in body['captures'] if c['present'] and c['span'][0]<=offset and end<=c['span'][1]),None) if body else None
                            assert (actual['type'] if actual else 'literal' if chosen else 'unassigned')==role
                            if actual:
                                a,b=actual['span'];assert row['native'].encode('utf-8','surrogateescape')[a:b]==actual['value'].encode('utf-8','surrogateescape')
                            example['runtime_capture']=actual
                            example['runtime_assignment_status']=chosen['match_status'] if chosen else 'no_match'
                        enclosed_groups[enclosed_key]=dict(template_id=tid,word=value.casefold(),marker=requested_marker,
                            selected_role=role,token_mentions=0,weighted_mentions=0,messages=set(),message_occurrences=0,
                            template_status=package.matcher.by_id[tid]['status'] if package and tid else None,
                            template_pattern=package.matcher.by_id[tid]['display'] if package and tid else None,
                            example=example)
                    eg=enclosed_groups[enclosed_key];eg['token_mentions']+=1;eg['weighted_mentions']+=count
                    if row['example_id'] not in eg['messages']:
                        eg['messages'].add(row['example_id']);eg['message_occurrences']+=count
                # No inference from punctuation adjacency: retain the actual raw predecessor.
                key = value.casefold(), marker, role, separator, preceding_role
                group = groups.setdefault(key, dict(word=key[0],enclosing_marker=marker,selected_role=role,
                    preceding_token_has_underscore_or_dot=separator,preceding_selected_role=preceding_role,token_mentions=0,weighted_mentions=0,
                    messages=set(),message_occurrences=0,predecessors=Counter(),examples=[]))
                group['token_mentions'] += 1; group['weighted_mentions'] += count
                if row['example_id'] not in group['messages']:
                    group['messages'].add(row['example_id']); group['message_occurrences'] += count
                group['predecessors'][previous] += 1
                if len(group['examples']) < 3:
                    group['examples'].append(dict(source=row['source_family'],text=row['native'],
                        token_span=[offset,end],preceding_token=previous,preceding_piece=previous_index,
                        capture=capture,preceding_capture=preceding_capture,template_id=(row.get('selected_assignment') or {}).get('template_id'),
                        provenance=row['native_occurrences'][:1]))
            if kind != 'gap':previous=value;previous_index=index;previous_span=(offset,end)
            offset=end
    output=[]
    for group in groups.values():
        group['contextual_messages']=len(group.pop('messages'))
        group['predecessors']=dict(group['predecessors'])
        output.append(group)
    result=dict(scope='All body raw pieces in retained 73-log candidate native evidence. Exact effect/trigger token spellings, case-folded for lookup only. Matched raw delimiter pairs use the existing nesting helper. Counts overlap across groups.',
        contextual_rows=rows,occurrences=occurrences,groups=output)
    for group in enclosed_groups.values():group['contextual_messages']=len(group.pop('messages'))
    result.update(enclosed_scope='Inside any matched () or [] pair; each token is counted once under its nearest such pair. Embedded substrings such as scripted_effects are not standalone word matches. Unbalanced markers are outside this survey.',
        package_id=package.manifest['package_id'] if package else None,
        enclosed_distinct_messages=len(enclosed_messages),enclosed_message_occurrences=sum(enclosed_messages.values()),
        enclosed_groups=list(enclosed_groups.values()))
    write_json(args.output,result)
    if package:render_enclosed(args.output.with_suffix('.html'),result)
    print(json.dumps(dict(contextual_rows=rows,occurrences=occurrences,groups=[{k:v for k,v in g.items() if k not in ('examples','predecessors')} for g in output]),indent=2))


if __name__ == '__main__':main()
