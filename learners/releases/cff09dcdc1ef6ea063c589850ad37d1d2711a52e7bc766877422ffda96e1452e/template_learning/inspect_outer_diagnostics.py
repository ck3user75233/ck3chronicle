"""Compare two saved outer-diagnostic native runs.

Reads saved native evidence; does not train, promote or reinterpret old models
through the current matcher. Only the new bundle is verified against current
inference code; the baseline is immutable comparison evidence.
"""
import argparse
from collections import Counter,defaultdict
import gc
import hashlib
import html
import json
from pathlib import Path

from template_learning.artifacts import load_bundle
from template_learning.inspect_incremental_learning import native_evidence_rows
from template_learning.matching_defaults import match_pattern


def row_key(row):
    return row['source_family'],row['native'],tuple(sorted(row['contexts']))


def inspect(baseline,bundle,output,focus_review=None,focus_cases=(),focus_text=()):
    output.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((baseline/'manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest['hashes'].items():
        path=(baseline/name).resolve()
        assert path.parent==baseline.resolve()
        assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,name
    previous=json.loads((baseline/'empirical_template_model.json').read_text(encoding='utf-8'))
    assert previous['schema_version']==3,'this report compares saved outer-diagnostic runs'
    old_patterns={p['template_id']:p['display'] for p in previous['templates']}
    focus_ids={}
    if focus_review:
        review=json.loads(focus_review.read_text(encoding='utf-8'))
        focus_ids={review['selected'][i-1]['record_id']:i for i in focus_cases}
    old_summary=previous['summary'];old_revision=previous['revision_id'];old_parser=previous['parser'];old_evidence=set(previous['evidence'])
    del previous;gc.collect()
    before={}
    for row,n in native_evidence_rows(baseline/'native_evidence.json'):
        before[row_key(row)]=dict(outcome=row['outcome'],templates=[old_patterns[m['template_id']] for m in row['matches']],
            matches=row['matches'],occurrences=n)
    model,_=load_bundle(bundle)
    assert model['parser']==old_parser
    assert set(model['evidence'])==old_evidence
    for name,digest in model['algorithm']['implementation_hashes'].items():
        assert hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()==digest,name
    patterns={p['template_id']:p for p in model['templates']}
    support_index={tid:{p['name']:{m['record_id']:m for m in p['field_support']['members']}
                       for p in template['parts'] if p['kind']=='slot'} for tid,template in patterns.items()}
    records={};transitions=Counter();examples={};problems=[];capture_checks=0;replays=0;capture_changes=Counter()
    reason_rows=0;relaxed_captures=[];support_mismatches=[];seen=set();source_rows=Counter();focused=[];text_examples={}
    for row,n in native_evidence_rows(bundle/'native_evidence.json'):
        k=row_key(row);seen.add(k);old=before[k];assert n==old['occurrences']
        transitions[old['outcome'],row['outcome']]+=n
        records[row['record_id']]=row
        source_rows[row['source_family']]+=1
        assert ''.join(t for _,t in row['pieces'])==row['native']
        raw=row['native'].encode('utf-8','surrogateescape');offsets=[0]
        for _,t in row['pieces']:offsets.append(offsets[-1]+len(t.encode('utf-8','surrogateescape')))
        boundaries=set(offsets)
        if row['construction'] and 'L2' in row['construction']['regions']:reason_rows+=1
        for match in row['matches']:
            pattern=patterns[match['template_id']]
            assert pattern['source_family']==row['source_family']
            actual=match_pattern(pattern['parts'],row['native'],pieces=row['pieces'])
            assert actual==match['captures']
            captures={c['name']:c for c in actual};assembled=[]
            for part in pattern['parts']:
                if part['kind']=='literal':assembled.append(part['text']);continue
                cap=captures[part['name']]
                own=support_index[pattern['template_id']][part['name']].get(row['record_id'])
                if own:
                    x,y=own['bytes']
                    expected=None if x==y and part['optional'] else [
                        x+len(part['prefix'].encode('utf-8','surrogateescape')),
                        y-len(part['suffix'].encode('utf-8','surrogateescape'))]
                    if cap['span']!=expected:
                        support_mismatches.append(dict(template=pattern['template_id'],record=row['record_id'],
                            field=part['name'],inferred=expected,matched=cap['span']))
                if cap['span'] is None:continue
                a,b=cap['span'];assert a in boundaries and b in boundaries
                assert raw[a:b].decode('utf-8','surrogateescape')==cap['value']
                assembled.extend((part['prefix'],cap['value'],part['suffix']));capture_checks+=1
                if row['record_id'] in pattern['evidence_record_ids']:
                    if cap['value'] not in part['observed_values']:
                        support_mismatches.append(dict(template=pattern['template_id'],record=row['record_id'],field=part['name'],value=cap['value']))
                if part['type']=='PARAM' and not part['constraints']['literal_guidance']:
                    from template_learning.literal_guidance import guided_ranges,LITERAL_WORDING
                    pieces=row['pieces'][offsets.index(a):offsets.index(b)]
                    words=guided_ranges(pieces,LITERAL_WORDING)
                    if words and len(relaxed_captures)<20:
                        relaxed_captures.append(dict(source=row['source_family'],native=row['native'],template=pattern['display'],value=cap['value'],guided_words=[cap['value'][x:y] for x,y in words]))
            assert ''.join(assembled)==row['native'];replays+=1
        displays=[patterns[m['template_id']]['display'] for m in [*row['matches'],*row['capture_ambiguities']]]
        old_captures=[m['captures'] for m in old['matches']]
        new_captures=[m['captures'] for m in row['matches']]
        if old_captures!=new_captures:
            capture_changes['contextual_rows']+=1;capture_changes['occurrences']+=n
        signature=(row['source_family'],tuple(old['templates']),tuple(displays),old['outcome'],row['outcome'])
        example=dict(source=row['source_family'],record_id=row['record_id'],native=row['native'],occurrences=n,before=old['outcome'],after=row['outcome'],
            previous_templates=old['templates'],previous_matches=old['matches'],templates=displays,matches=row['matches'],
            capture_ambiguities=row['capture_ambiguities'],provisional_reasons=row['provisional_reasons'],provenance=row['native_occurrences'][0])
        if row['record_id'] in focus_ids:
            example['previous_review_case']=focus_ids[row['record_id']];focused.append(example)
        for needle in focus_text:
            if needle in row['native'] and (needle not in text_examples or n>text_examples[needle]['occurrences']):
                text_examples[needle]=dict(example,focus_text=needle)
        if signature not in examples or n>examples[signature]['occurrences']:examples[signature]=example
        if row['outcome']!='full':problems.append(example)
    assert seen==set(before)
    field_ranges=0
    for p in patterns.values():
        members=set(p['evidence_record_ids'])
        for part in p['parts']:
            if part['kind']!='slot':continue
            assert {v['record_id'] for v in part['field_support']['members']}==members
            for v in part['field_support']['members']:
                row=records[v['record_id']];a,b=v['pieces'];x,y=v['bytes']
                assert ''.join(t for _,t in row['pieces'][a:b]).encode('utf-8','surrogateescape')==row['native'].encode('utf-8','surrogateescape')[x:y]
                field_ranges+=1
    selected=sorted(focused,key=lambda x:x['previous_review_case']);per_source=Counter()
    # Distinct formulation changes, not repeated location variants.
    ordered=sorted(examples.values(),key=lambda x:(x['before']==x['after'],-x['occurrences'],x['source'],x['native']))
    for needle in focus_text:
        if needle in text_examples:selected.append(text_examples[needle])
    for x in ordered:
        if per_source[x['source']]<3 and x['previous_templates']!=x['templates']:
            selected.append(x);per_source[x['source']]+=1
        if len(selected)>=25:break
    for needle in ['unlearn_language effect','Malformed token','Unexpected token','Wet Fields','Reason:','[@']:
        x=next((x for x in ordered if needle in x['native']),None)
        if x and x not in selected:selected.append(x)
    conflicts={}
    conflict_counts=Counter()
    for x in problems:
        if x['after']!='provisional':continue
        key=(x['source'],tuple(sorted(m['template_id'] for m in [*x['matches'],*x['capture_ambiguities']])))
        conflict_counts[key]+=x['occurrences']
        if key not in conflicts or x['occurrences']>conflicts[key]['occurrences']:conflicts[key]=x
    selected.extend(conflicts[k] for k,_ in conflict_counts.most_common())
    # Cover each unresolved candidate once, not the first ten person/location
    # variants of one failure. All native rows remain in the machine export.
    for p in patterns.values():
        if not p['unsupported_members']:continue
        members=set(p['evidence_record_ids'])
        choices=[x for x in problems if x['after']=='unknown' and x['record_id'] in members]
        if choices:selected.append(max(choices,key=lambda x:x['occurrences']))
    distinct={}
    for x in selected:
        key=(x['source'],x['before'],x['after'],tuple(x['previous_templates']),tuple(x['templates']),x.get('focus_text'))
        distinct.setdefault(key,x)
    selected=list(distinct.values())
    for example in selected:
        example['unresolved_candidates']=[dict(template_id=p['template_id'],display=p['display'],
            members=p['unique_messages'],failed_members=len(p['unsupported_members']),
            member_issues=[h for h in p['region_hypotheses'] if h.get('record_id')==example['record_id']
                           and h.get('proposal') in {'capture_ambiguity','capture_replay'}])
            for p in patterns.values() if p['status']=='unresolved' and example['record_id'] in p['evidence_record_ids']]
        example['field_details']=[]
        for match in example['matches']:
            p=patterns[match['template_id']]
            for part in p['parts']:
                if part.get('type')!='PARAM':continue
                support=part['field_support']
                values=sorted(part['observed_values'],key=lambda v:(len(v),v))
                example['field_details'].append(dict(template=p['template_id'],field=part['name'],
                    candidate_members=len(p['evidence_record_ids']),token_counts=support['token_counts'],
                    shortest=values[0],longest=values[-1],assessment=support['assessment']))
    word_only_fields=[dict(template_id=p['template_id'],source=p['source_family'],template=p['display'],
        status=p['status'],field=part['name'],assessment=part['field_support']['assessment'],
        token_counts=part['field_support']['token_counts'],observed_values=part['observed_values'])
        for p in patterns.values() for part in p['parts'] if part.get('type')=='PARAM'
        and part['field_support']['assessment']['word_only_review']]
    absorbed=Counter(tuple(h['absorbed_wording']) for p in patterns.values() for h in p['region_hypotheses']
        if h.get('proposal')=='punctuation_boundary_preference')
    summary=dict(baseline=old_revision,candidate=model['revision_id'],before=old_summary,after=model['summary'],
        transitions=[dict(before=a,after=b,occurrences=n) for (a,b),n in sorted(transitions.items())],
        complete_contextual_rows=len(seen),unique_messages=len(records),reason_rows=reason_rows,capture_checks=capture_checks,capture_changes=dict(capture_changes),
        reconstructed_matches=replays,candidate_local_field_ranges=field_ranges,support_mismatches=support_mismatches,
        relaxed_literal_examples=relaxed_captures,problems=problems,selected=selected,word_only_fields=word_only_fields,
        absorbed_word_boundaries=[dict(words=list(k),fields=n) for k,n in absorbed.most_common()],
        broad_effect_templates=[dict(template=p['display'],members=p['unique_messages']) for p in patterns.values() if 'Error: <KEY> effect [' in p['display']])
    (output/'comparison.json').write_text(json.dumps(summary,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
    def visible(t):return ''.join(c if ord(c)>=32 or c in '\n\r\t' else f'⟦U+{ord(c):04X}⟧' for c in t).rstrip('\r\n')
    def pre(t):return '<pre>'+html.escape(visible(t))+'</pre>'
    body=['<h1>Complete diagnostic learner: native comparison</h1>',
        '<p>Same complete native logs, before and after the learner change. Full now requires sufficient distinct learning examples as well as one template and one complete capture assignment. Provisional can mean insufficient evidence, not just ambiguity. Neither outcome is semantic approval; no model is promoted.</p>',
        '<p>Examples are selected by distinct before/after formulations, not random full-message rows with repeated locations. Display omits trailing line endings; native evidence remains exact.</p>',
        '<table><tr><th>Measure</th><th>Before</th><th>After</th></tr>']
    for key in ('templates','unresolved_candidates'):
        body.append(f'<tr><td>{key.replace("_"," ")}</td><td>{old_summary[key]:,}</td><td>{model["summary"][key]:,}</td></tr>')
    for key in ('full','provisional','unknown'):
        body.append(f'<tr><td>{key}</td><td>{old_summary["training_outcomes"][key]:,}</td><td>{model["summary"]["training_outcomes"][key]:,}</td></tr>')
    body.append('</table><h2>Transitions</h2><table><tr><th>Before outcome</th><th>After outcome</th><th>Occurrences</th></tr>')
    for (a,b),n in sorted(transitions.items()):body.append(f'<tr><td>{a}</td><td>{b}</td><td>{n:,}</td></tr>')
    body.append('</table>')
    for i,x in enumerate(selected,1):
        note=('The bracketed reason is captured intact as REASON; all displayed locations and traces belong to this complete candidate.' if any('<REASON>' in t for t in x['templates']) else 'Compare the retained literal wording and the typed variable fields below.')
        if 'insufficient_distinct_learning_examples' in x['provisional_reasons']:
            note+=' The formulation remains provisional: it lacks two distinct non-location learning examples.'
        if any(r in x['provisional_reasons'] for r in ('competing_templates','ambiguous_capture_boundaries')):
            note+=' Multiple templates or complete capture assignments remain; no preferred answer is selected.'
        if x['after']=='unknown':note+=' No complete candidate matches; this is an unresolved regression to inspect.'
        if x['templates']==x['previous_templates']:note+=' The written formulations are unchanged.'
        if any('Error: <KEY> effect [' in t for t in x['templates']):note+=' The effect name varies inside a complete outer template; supporting trace examples must belong to that same candidate.'
        if any('Reason: <PARAM>' in t for t in x['templates']) and any('Reason<PARAM>' in t for t in x['previous_templates']):note+=' The colon after Reason now remains literal outside PARAM.'
        label=f' (previous review {x["previous_review_case"]:02})' if 'previous_review_case' in x else ''
        body += [f'<article id="case-{i}"><h2>{i:02}. {html.escape(x["source"])}{label} — {x["occurrences"]:,} occurrences</h2>',pre(x['native']),'<p>'+note+'</p><div class="compare">']
        for label,field,status in [('Before','previous_templates',x['before']),('After','templates',x['after'])]:
            body.append('<section><h3>'+label+' — '+status+'</h3>'+(''.join(pre(t) for t in x[field]) or '<p>No matching candidate.</p>')+'</section>')
        body.append('</div>')
        if x.get('focus_text'):
            raw=records[x['record_id']]['pieces']
            body.append('<details><summary>Actual raw parser pieces of this complete message</summary>'+pre('\n'.join(f'{i}: {k} {t!r}' for i,(k,t) in enumerate(raw)))+'</details>')
            for match in x['matches']:
                pattern=patterns[match['template_id']]
                body.append('<p>Learning support: '+html.escape(str(pattern['learning_support']['distinct_diagnostic_examples']))+' distinct native examples, including slot variation; status '+html.escape(pattern['status'])+'.</p>')
                for part in pattern['parts']:
                    if part.get('type')!='PARAM':continue
                    values={}
                    for member in part['field_support']['members']:
                        row=records[member['record_id']];pieces=row['pieces'][slice(*member['pieces'])]
                        value=''.join(t for _,t in pieces)
                        values[value]=dict(pieces=pieces,record_id=member['record_id'])
                    basis=part.get('parameter_definition') or 'empirical candidate-member evidence'
                    body.append('<details><summary>'+html.escape(part['name']+' PARAM: '+str(len(values))+' observed values; '+basis)+'</summary><table><tr><th>Actual region value</th><th>Raw token count (gaps excluded)</th><th>Actual raw pieces; gaps shown explicitly</th><th>Evidence record</th></tr>')
                    for value,info in sorted(values.items(),key=lambda v:(sum(k=='token' for k,_ in v[1]['pieces']),v[0])):
                        pieces=info['pieces'];count=sum(k=='token' for k,_ in pieces)
                        body.append('<tr><td>'+pre(value)+'</td><td>'+str(count)+'</td><td>'+pre(' · '.join((k+': '+repr(t)) for k,t in pieces))+'</td><td>'+html.escape(info['record_id'])+'</td></tr>')
                    body.append('</table></details>')
        for proposal in x['unresolved_candidates']:
            body.append('<details><summary>Unresolved learned proposal ('+str(proposal['failed_members'])+' of '+str(proposal['members'])+' members fail validation)</summary>'+pre(proposal['display']))
            for issue in proposal['member_issues']:
                body.append('<p>'+html.escape(issue['reason'])+'</p>')
                for witness in issue.get('witnesses',[]):
                    body.append(pre('\n'.join(c['name']+' <'+c['type']+'> = '+repr(c['value']) for c in witness)))
            body.append('</details>')
        if x['previous_matches']:
            body.append('<details><summary>Before: actual captures</summary>')
            for match in x['previous_matches']:
                body.append(pre('\n'.join(c['name']+' <'+c['type']+'> = '+repr(c['value']) for c in match['captures'])))
            body.append('</details>')
        for ambiguity in x['capture_ambiguities']:
            body.append('<p>Capture ambiguity: '+str(ambiguity['count'])+' complete body assignments. Two witnesses:</p>')
            for witness in ambiguity['witnesses']:
                body.append(pre('\n'.join(c['name']+' <'+c['type']+'> = '+repr(c['value']) for c in witness)))
        if x['matches']:
            body.append('<details><summary>Actual captures in this native message</summary>')
            for match in x['matches']:
                body.append('<p>Candidate '+html.escape(match['template_id'])+'</p>')
                body.append(pre('\n\n'.join(c['name']+' <'+c['type']+'> = '+(c['value'] if c['value'] is not None else '(absent)') for c in match['captures'])))
            body.append('</details>')
        if x['field_details']:
            body.append('<details><summary>PARAM evidence from these candidates’ own complete messages</summary>')
            for field in x['field_details']:
                body.append('<p>Field '+html.escape(field['field'])+'; '+str(field['candidate_members'])+
                    ' distinct member messages; observed raw token counts '+html.escape(str(field['token_counts']))+
                    '. Shortest and longest observed values:</p>'+pre(field['shortest'])+pre(field['longest']))
            body.append('</details>')
        body.append('</article>')
    body.append('<h2>PARAMs without adjacent punctuation</h2><p>These remain suspect. The generic policy requires stronger variation evidence; each field is flagged for review, not treated as semantically approved.</p>')
    for field in word_only_fields:
        body.append('<details><summary>'+html.escape(field['source']+' — '+field['field']+' — '+field['status'])+'</summary>'+pre(field['template']))
        body.append('<p>Observed raw token lengths: '+html.escape(str(field['token_counts']))+'</p>')
        body.append(pre('\n'.join(repr(v) for v in field['observed_values'][:5]))+'</details>')
    css='body{font:16px/1.5 system-ui;max-width:1500px;margin:32px auto;padding:0 24px;background:#f6f8fa;color:#172a38}article{background:white;border:1px solid #ccd5dc;border-radius:8px;padding:20px;margin:24px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf1f4;padding:12px;font:14px/1.5 Consolas,monospace}.compare{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px}td,th{padding:6px 12px;text-align:left}@media(max-width:850px){.compare{grid-template-columns:1fr}}'
    (output/'REVIEW.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Outer diagnostic native review</title><style>'+css+'</style><body>'+''.join(body)+'</body></html>',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in {'before','problems','selected','relaxed_literal_examples','broad_effect_templates','support_mismatches','word_only_fields'}},indent=2))
    print('Support discrepancies:',len(support_mismatches),'guided content in PARAM examples:',len(relaxed_captures),'broad effect templates:',len(summary['broad_effect_templates']))
    assert not support_mismatches,'candidate-member capture spans disagree with inferred field support; see comparison.json'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',type=Path,required=True)
    parser.add_argument('--bundle',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--focus-review',type=Path)
    parser.add_argument('--focus-cases',type=int,nargs='*',default=[])
    parser.add_argument('--focus-text',action='append',default=[])
    args=parser.parse_args();inspect(args.baseline,args.bundle,args.output,args.focus_review,args.focus_cases,args.focus_text)


if __name__=='__main__':main()
