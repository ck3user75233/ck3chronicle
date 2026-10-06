"""Review genuine formatted-reference assignments, grouped by successor template."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path

from template_learning.inventory import sha256_file
from template_learning.matcher_example import load_verified
from template_learning.evidence_serialization import write_json
from template_learning.verify_location_candidate import prepared
from template_learning.verify_parser_correspondence import evidence_unit
from ck3chronicle.pipeline.contracts import materialize_definitions


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--preflight',type=Path,required=True)
    cli.add_argument('--production',type=Path,required=True)
    cli.add_argument('--candidate',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    args=cli.parse_args()
    evidence=json.loads(args.preflight.read_bytes())
    packages={k:load_verified(p,sha256_file(p/'manifest.json')) for k,p in
              [('production',args.production),('candidate',args.candidate)]}
    contracts={k:materialize_definitions(p) for k,p in packages.items()}
    groups=defaultdict(list);transitions=Counter();records=[];failures=[]
    for row in evidence['records']:
        outcomes={}
        for label,p in packages.items():
            unit=dict(parser=p.manifest['parser'],source_family=row['source'],source_tag=row['source'],
                context_kind=row['context_kind'],body=dict(text=row['text'],pieces=row['pieces']),
                contexts=next(iter(row['contexts'].values()),{}),continuations=row['continuations'])
            answer=p.match(evidence_unit(p,unit),inspect=True);a=answer['assignment']
            materialized=prepared(p,answer,contracts[label])
            if materialized:
                native=dict(body=row['text'],**unit['contexts'])
                native={k:v['text'] if isinstance(v,dict) else v for k,v in native.items()}
                native.update({'continuation:'+str(i):r['text'] for i,r in enumerate(row['continuations'])})
                assert dict(materialized['rendered'])==native,(label,row['example_id'])
            outcomes[label]=dict(template_id=a['template_id'] if a else None,
                status=a['match_status'] if a else 'no_match',
                compatible=[m['template_id'] for m in answer['inspection']['matches']],
                captures=next(r['captures'] for r in a['regions'] if r['name']=='body') if a else [])
        new=outcomes['candidate']
        for f in row['fields']:
            if not any(c['type']=='PARAM' and c['value']==f['value'] for c in new['captures']):
                failures.append(dict(example_id=row['example_id'],expected=f))
        transitions[outcomes['production']['status']+' -> '+new['status']]+=row['occurrences']
        record=dict(row,outcomes=outcomes);records.append(record);groups[new['template_id']].append(record)
    result=dict(packages={k:p.manifest['package_id'] for k,p in packages.items()},
        scope=dict(logs=73,corpus_rows=evidence['rows'],affected_messages=len(records),
                   occurrences=sum(r['occurrences'] for r in records)),transitions=dict(transitions),
        failures=failures,records=records)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    write_json(args.output.with_suffix('.json'),result)
    esc=lambda s:html.escape(str(s))
    def pre(s):
        return '<pre>'+esc(''.join(c if c in '\r\n\t' or ord(c)>=32 else '\\u%04x'%ord(c) for c in s))+'</pre>'
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Formatted reference PARAMs</title>',
          '<style>body{font:16px/1.55 system-ui;max-width:1120px;margin:36px auto;padding:0 24px;color:#183040}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;padding:14px;font-size:13px}article{border-top:2px solid #b8c8d4;margin-top:30px}.meta{color:#4c6070;font-size:14px}</style>',
          '<h1>Formatted references become complete PARAMs</h1>',
          '<p><a href="CHANGES.html">Full production comparison and template samples</a></p>',
          '<p>The contextual ONCLICK/TOOLTIP opening sequence and complete consecutive reset run delimit a complete reference. Its metadata, displayed text and controls are captured together. The rule does not depend on names, word counts, traits, mods or emitters. Existing full identities, declared fields and larger quoted PARAMs retain their boundaries.</p>',
          '<p>The previous learner had no general declaration for this sequence. Name and trait words therefore reached ordinary slot inference; reset controls attached to the final word in the raw parser pieces also prevented ordinary punctuation-pair recognition from supplying the intended boundary. The new declaration recognizes a complete reference before word-slot inference. No parser change or broader KEY grammar was needed. Two-reset tooltip references receive the same treatment; additional resets closing surrounding formatting remain in the same opaque capture. Labels containing internal nested formatting remain outside this simple-field rule.</p>',
          '<p>Scope: all 73 training logs, '+str(evidence['rows'])+' contextual messages. '+str(sum(evidence['counts'].values()))+' newly recognized fields in '+str(len(records)-evidence['preserved_enclosing_params'])+' messages; '+str(evidence['preserved_enclosing_params'])+' additional messages verify preservation of larger quoted PARAMs.</p>',
          '<p>Control bytes are displayed below as Unicode escapes for readability. These are recovered message bodies; the outer log timestamp/header is not included. The learner preserves the original bytes and line endings.</p>',
          '<p>Production package <code>'+result['packages']['production']+'</code>; candidate <code>'+result['packages']['candidate']+'</code>. Production is unchanged.</p>',
          '<p>Exact PARAM capture checks: '+str(len(failures))+' failures. Assignment transitions count occurrences:</p>'+pre(json.dumps(dict(transitions),indent=2))]
    example=0;shown_old=set();shown_patterns={}
    def pattern(text):
        if text in shown_patterns:
            return '<p>Same template wording as <a href="#'+shown_patterns[text]+'">the pattern already shown above</a>.</p>'
        anchor='pattern-'+str(len(shown_patterns)+1);shown_patterns[text]=anchor
        return '<div id="'+anchor+'">'+pre(text)+'</div>'
    ordered=sorted(groups.items(),key=lambda x:(not any('already has the trait' in r['text'] for r in x[1]),-len(x[1]),str(x[0])))
    for number,(tid,rows) in enumerate(ordered,1):
        bits.append('<article><h2>'+str(number)+'. '+esc(rows[0]['source'])+'</h2><p>'+str(len(rows))+' distinct messages; '+str(sum(r['occurrences'] for r in rows))+' occurrences. Counts belong to this group, not to each compatible predecessor.</p>')
        old_ids=sorted({i for r in rows for i in r['outcomes']['production']['compatible']})
        bits.append('<h3>Production templates</h3>')
        for oid in old_ids:
            if oid in shown_old:
                bits.append('<p>Also covered by <a href="#old-'+oid+'">production template '+oid+'</a>, shown once above.</p>');continue
            shown_old.add(oid);t=packages['production'].matcher.by_id[oid]
            bits.append('<div id="old-'+oid+'"><p class="meta">'+oid+' · '+esc(t['status'])+'</p>'+pattern(t['display'])+'</div>')
        if not old_ids:bits.append('<p>No complete production template match.</p>')
        bits.append('<h3>Candidate template</h3>')
        if tid:
            t=packages['candidate'].matcher.by_id[tid]
            bits.append('<p class="meta">'+tid+' · '+esc(t['status'])+'</p>'+pattern(t['display']))
        else:bits.append('<p>No complete assignment.</p>')
        chosen=[]
        for label in ('Insightful Thinker','Misguided Warrior'):
            match=next((r for r in rows if label in r['text']),None)
            if match and match not in chosen:chosen.append(match)
        for r in rows:
            if len(chosen)>=2:break
            if r not in chosen:chosen.append(r)
        for r in chosen:
            example+=1
            body=('<p>The exact message body is the <a href="#'+shown_patterns[r['text']]+'">literal production pattern already shown above</a>.</p>'
                  if r['text'] in shown_patterns else pre(r['text']))
            bits.append('<h3>Example E'+str(example).zfill(2)+'</h3><p class="meta">'+str(r['occurrences'])+' occurrences of this exact contextual message.</p>'+body)
            bits.append('<details><summary>Exact expected PARAM values and genuine provenance</summary>'+pre(json.dumps(dict(fields=r['fields'],provenance=r['provenance']),ensure_ascii=False,indent=2))+'</details>')
        bits.append('</article>')
    bits.append('<p>Two previously unmatched activity messages remain outside this formatting rule: their activity text uses a different markup structure. That separate field-inference issue is not resolved by these results.</p></html>')
    args.output.write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
    assert not failures,failures


if __name__=='__main__':main()
