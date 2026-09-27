"""Compare native builds and render inspectable single-assignment changes."""
import argparse
from collections import Counter, defaultdict
import hashlib
import html
import importlib.util
import json
from pathlib import Path
from types import MappingProxyType

from template_learning.artifacts import load_bundle
from template_learning.inspect_incremental_learning import native_evidence_rows
from template_learning.publish_native_model import compact_model, compact_template
from ck3chronicle.pipeline.model import EmpiricalModel, _freeze, _validate_rules, _validate_template
from ck3chronicle.pipeline.classifier import Classifier


def check_layout(pattern, captures, text):
    raw=text.encode('utf-8','surrogateescape'); slots={c['name']:c for c in captures}
    cursor=0; rendered=[]
    for part in pattern['parts']:
        if part['kind']=='literal':
            value=part['text'].encode('utf-8','surrogateescape')
        else:
            capture=slots[part['name']]
            if capture['span'] is None:
                assert part['optional'] and capture['value'] is None
                value=b''
            else:
                prefix=part['prefix'].encode('utf-8','surrogateescape')
                body=capture['value'].encode('utf-8','surrogateescape')
                a,b=capture['span'];assert (a,b)==(cursor+len(prefix),cursor+len(prefix)+len(body))
                assert raw[a:b]==body
                value=prefix+body+part['suffix'].encode('utf-8','surrogateescape')
        assert raw[cursor:cursor+len(value)]==value
        rendered.append(value);cursor+=len(value)
    assert b''.join(rendered)==raw and cursor==len(raw)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--selection',type=Path,required=True)
    args=ap.parse_args();args.output.mkdir(exist_ok=True,parents=True)
    old=json.loads((args.before/'empirical_template_model.json').read_text())
    new,parser=load_bundle(args.after)
    spec=importlib.util.spec_from_file_location('frozen_assignment',args.after/'assignment.py')
    frozen=importlib.util.module_from_spec(spec);spec.loader.exec_module(frozen)
    component_spec=importlib.util.spec_from_file_location('frozen_components',args.after/'continuations.py')
    components=importlib.util.module_from_spec(component_spec);component_spec.loader.exec_module(components)
    oldtemplates={t['template_id']:t for t in old['templates']};templates={t['template_id']:t for t in new['templates']}
    _validate_rules(new['owner_rules'])
    declarations={d['id']:d for d in new['owner_rules']['constructions']}
    definitions={d['id']:d for d in new['owner_rules']['parameter_structures']}
    for t in templates.values():_validate_template(compact_template(t),declarations,definitions)
    compact=compact_model(new);data=_freeze(compact)
    by_source={s:tuple(t for t in data['templates'] if t['source_family']==s) for s in new['by_source']}
    classifier=Classifier(EmpiricalModel(new['revision_id'],'unpublished-research',data,parser,MappingProxyType(by_source),
                                        frozen.select_assignment,components.match_components))
    previous={r['example_id']:(r,n) for r,n in native_evidence_rows(args.before/'native_evidence.json')}
    input_rows=json.loads(args.selection.read_text())['logs'];paths={r['sha256']:r['path'] for r in input_rows}
    weights={}
    weightpath=args.selection.parent/'same-30-results.jsonl'
    if weightpath.exists():
        for line in weightpath.open():
            w=json.loads(line);weights[w['example_id']]=w['weights']
    transitions=Counter();cohorts=defaultdict(Counter);stats=Counter();groups={};failures=[]
    retired={r['retired_template_id']:r for r in new['template_retirement']}
    for r,n in native_evidence_rows(args.after/'native_evidence.json'):
        before,bn=previous.pop(r['example_id']);assert n==bn
        selected=r['selected_assignment'];stats['rows']+=1;stats['occurrences']+=n
        assert selected is not None, 'unexpected loss of previously matched native input'
        prior_assignment=next(m for m in before['matches'] if m['template_id']==selected['template_id'])
        assert prior_assignment['captures']==selected['captures'], 'selection changed an existing binding'
        stats['selected_existing_capture_assignment']+=n
        assert not r['unmatched_complete_message']
        stats['selected_'+selected['selection']['reason']]+=n
        contexts=tuple((name,c[name]['text'],tuple(map(tuple,c[name]['pieces'])))
                       for c in r['contexts'].values() for name in ('prefix','suffix'))
        matches,issue=classifier._match_content(r['source_family'],r['context_kind'],r['native'],tuple(map(tuple,r['pieces'])),contexts)
        assert issue is None
        actual=[]
        for tid,status,body,wrapper in matches:
            kept=[];component_witnesses=[]
            for witness in body['witnesses']:
                values=components.match_components(templates[tid]['continuation'],r['continuations'],witness)
                if values is not None:kept.append(witness);component_witnesses.append(values)
            if kept:
                actual.append(dict(template_id=tid,body=dict(count=len(kept),witnesses=kept),
                    component_witnesses=component_witnesses,
                    contexts={name:[dict(template_id=pid,**a) for pid,a in alts] for name,alts in wrapper}))
        assert {m['template_id'] for m in actual}=={m['template_id'] for m in [*r['matches'],*r['capture_ambiguities']]}
        replay=frozen.select_assignment(compact,actual)
        assert replay==selected, r['example_id']
        assert frozen.select_assignment(compact,list(reversed(actual)))==selected
        check_layout(templates[selected['template_id']],selected['captures'],r['native'])
        for name,assignment in selected['context_matches'].items():
            pattern=next(p for p in templates[selected['template_id']]['context_patterns'][name] if p['template_id']==assignment['template_id'])
            native_context=next(iter(r['contexts'].values()))[name]['text']
            check_layout(pattern,assignment['captures'],native_context)
        stats['body_captures_verified']+=len(selected['captures'])
        transitions[(before['outcome'],r['outcome'])]+=n
        rowweights=weights.get(r['example_id'],{'this_corpus':n})
        if new['summary']['distinct_error_logs']==10 and 'original10' in rowweights:
            rowweights={'original10':rowweights['original10']}
        assert sum(rowweights.values())==n
        for cohort,weight in rowweights.items():
            cohorts[cohort][(before['outcome'],r['outcome'])]+=weight
        oldids=tuple(m['template_id'] for m in before['matches'])
        removed=[tid for tid in oldids if tid in retired]
        if removed:
            category='Redundant fixed-value template retired'
            reason='The unchanged general template retains its learned identifier field. Fixed observed values no longer compete as separate templates.'
        elif len(oldids)>1:
            category='Winner selected among remaining candidates'
            reason='Remaining complete candidates are ranked by exported native field evidence and independent examples. '+selected['selection']['reason'].replace('_',' ')+'.'
        elif before['outcome']!=r['outcome']:
            category='Support status corrected'
            reason='Location or declared-trace-only variation no longer supplies additional independent examples. The template and its captures remain available as provisional.'
        else:
            category='Unchanged formulation; explicit assignment now returned'
            reason='The same complete template is selected. A provisional template remains provisional; returning one assignment is not promotion.'
        changed=bool(removed or len(oldids)>1 or before['outcome']!=r['outcome'])
        stats['changed_occurrences']+=n if changed else 0
        key=(r['source_family'],category,oldids,selected['template_id'],before['outcome'],r['outcome'])
        item=dict(source=r['source_family'],native=r['native'],pieces=r['pieces'],
                  occurrence_example=r['native_occurrences'][0],category=category,reason=reason,
                  before_outcome=before['outcome'],after_outcome=r['outcome'],before=before['matches'],
                  selected=selected,retired=removed,occurrences=n,rows=1)
        if key not in groups:groups[key]=item
        else:
            groups[key]['occurrences']+=n;groups[key]['rows']+=1
    assert not previous
    ordered=sorted(groups.values(),key=lambda r:(r['category'].startswith('Unchanged'),-r['occurrences'],r['source'],r['native']))
    selected=[];seen=set()
    # Different mechanisms and sources; never repeat only locations/timestamps.
    for prefix,limit in [('Redundant',8),('Winner',5),('Support',7),('Unchanged',5)]:
        pool=[item for item in ordered if item['category'].startswith(prefix)]
        chosen=[];sources=set()
        for item in pool:
            if item['source'] not in sources:
                chosen.append(item);sources.add(item['source'])
            if len(chosen)==limit:break
        for item in pool:
            if len(chosen)==limit:break
            if item not in chosen:chosen.append(item)
        for item in chosen:
            if item['native'] not in seen:
                selected.append(item);seen.add(item['native'])
    for item in ordered:
        if len(selected)==25:break
        if item['native'] not in seen:selected.append(item);seen.add(item['native'])
    assert len(selected)==25
    # Verify each displayed message against its actual protected source file.
    verified={}
    for item in selected:
        ref=item['occurrence_example'];path=Path(paths[ref['evidence_sha256']]);raw=path.read_bytes()
        digest=hashlib.sha256(raw).hexdigest();assert digest==ref['evidence_sha256']
        a,b=ref['span'];assert raw[a:b].decode('utf-8','surrogateescape')==item['native']
        item['native_path']=str(path);verified[str(path)]=digest
    result=dict(before=old['summary'],after=new['summary'],before_revision=old['revision_id'],after_revision=new['revision_id'],
        retired_templates=len(retired),counts=dict(stats),transitions=[dict(before=a,after=b,occurrences=n) for (a,b),n in transitions.items()],
        cohorts={k:[dict(before=a,after=b,occurrences=n) for (a,b),n in values.items()] for k,values in cohorts.items()},
        pipeline_scope='Read-only existing runtime matcher plus independently loaded frozen selector. Pipeline adapter/pin not changed.',
        verified_display_files=verified)
    (args.output/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.output/'examples.json').write_text(json.dumps(selected,ensure_ascii=True,indent=2)+'\n')
    (args.output/'all-change-groups.json').write_text(json.dumps(list(groups.values()),ensure_ascii=True,indent=2)+'\n')
    esc=lambda s:html.escape(str(s))
    def pre(s):
        visible=''.join(f'\\u{ord(c):04x}' if (ord(c)<32 and c not in '\r\n\t') or 0xD800<=ord(c)<=0xDFFF else c for c in s)
        return '<pre>'+esc(visible)+'</pre>'
    out=['<!doctype html><meta charset="utf-8"><title>Single template assignment — native review</title>',
         '<style>body{font:16px system-ui;max-width:1350px;margin:30px auto;padding:0 20px;color:#182533}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f5f8;padding:12px;line-height:1.45}.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}article{border-top:2px solid #abc;margin-top:30px}table{border-collapse:collapse;width:100%}td,th{padding:8px;border:1px solid #ccd;text-align:left}summary{cursor:pointer;padding:10px}.note{background:#fff1cf;padding:14px}@media(max-width:800px){.cols{display:block}}</style>',
         '<h1>One selected template per matched message</h1>',
         '<p class="note">The earlier provisional figure was not a no-match count. This comparison uses complete native logs and the same parser v1.6; no synthetic messages, edited templates or occurrence-weighted learning. These are training-corpus results, not accuracy estimates. Nonprinting native controls are displayed as escaped code points; stored bytes are unchanged.</p>',
         '<table><tr><th></th><th>Before</th><th>After</th></tr>']
    for label,key in [('Active templates','templates'),('Supported templates','supported_templates'),('Provisional templates','provisional_templates')]:
        out.append(f'<tr><td>{label}</td><td>{old["summary"][key]:,}</td><td>{new["summary"][key]:,}</td></tr>')
    for key in ('full','provisional','unknown'):
        out.append(f'<tr><td>{key} occurrences</td><td>{old["summary"]["training_outcomes"][key]:,}</td><td>{new["summary"]["training_outcomes"][key]:,}</td></tr>')
    out+=['</table>',f'<p>{len(retired)} redundant formulations retired. Every native row replayed through the existing runtime matching mechanics and the frozen selector; selected literals/captures reconstruct each complete message and wrapper.</p>',
          '<p>Sample: 25 exact distinct native messages, selected to cover sources, mechanisms and competing formulations. Counts shown apply to the comparison group, not just the displayed spelling. This is a diagnostic sample, not random or frequency representative.</p>']
    for i,item in enumerate(selected,1):
        s=item['selected'];out += [f'<article><h2>{i:02d} · {esc(item["source"])} · {esc(item["category"])}</h2>',f'<p>{esc(item["reason"])} Group: {item["occurrences"]:,} occurrences / {item["rows"]:,} contextual rows.</p>','<h3>Original native message</h3>',pre(item['native']),'<div class="cols"><section><h3>Before · '+esc(item['before_outcome'])+'</h3>']
        for match in item['before']:
            t=oldtemplates[match['template_id']];out += [f'<p>{esc(match["template_status"])} · {esc(t["template_id"])}</p>',pre(t['display'])]
            if t['template_id'] in templates:
                e=templates[t['template_id']]['selection_evidence']
                out.append(f'<p>Current evidence: {e["independent_examples"]:,} distinct examples after excluding locations and declared traces; {e["maximum_location_losses"]} location losses, {e["maximum_declared_field_losses"]} declared-field losses, {e["unsubstantiated_fields"]} fields lacking positive support.</p>')
        out+=['</section><section><h3>After · '+esc(item['after_outcome'])+' · one selected assignment</h3>',pre(templates[s['template_id']]['display']),'<p>Selection: '+esc(s['selection']['reason'])+'. Template support: '+esc(s['template_status'])+'.</p></section></div>',
              '<table><tr><th>Slot</th><th>Type</th><th>Actual selected value</th></tr>']
        for capture in s['captures']:out.append('<tr><td>'+esc(capture['name'])+'</td><td>'+esc(capture['type'])+'</td><td>'+pre(capture['value'] if capture['value'] is not None else '(absent)')+'</td></tr>')
        out+=['</table><details><summary>Evidence ranking, raw pieces and provenance</summary>',pre(json.dumps(s['selection'],indent=2)),pre(' | '.join(json.dumps(v,ensure_ascii=False) for _,v in item['pieces'])),pre(item['native_path']),pre(json.dumps(item['occurrence_example'],indent=2)),'</details></article>']
    out+=['<h2>Remaining quality limits</h2>',
          '<p>Single assignment is not a claim that every winning template is semantically correct. UI-formatted character/name fragments still appear in some KEY captures; this change does not repair that existing typing. Malformed-brace identifier binding remains separate. Fixed prefixes inside an otherwise variable identifier may also leave competitors; they are selected, not automatically retired.</p>',
          '<p>In the ten-log build, four native occurrences require a deterministic evidence tie-break. The thirty-log build has no such ties. More evidence changes these decisions, but this is not an accuracy benchmark. The production pipeline adapter and model pin have not been changed.</p>',
          '<h2>Complete comparison and limits</h2>',pre(json.dumps(result,indent=2))]
    (args.output/'REVIEW.html').write_text('\n'.join(out),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
