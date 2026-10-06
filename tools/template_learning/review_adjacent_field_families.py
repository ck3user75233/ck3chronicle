"""Review complete genuine message families and group predecessor/successor templates."""
import argparse
from collections import Counter, defaultdict
import hashlib
import html
import json
from copy import deepcopy
from pathlib import Path

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.matcher_example import load_verified


def family(text):
    if 'participating in activity' in text:
        return 'activity'
    if 'Failed to find any valid flavorization for character' in text:
        return 'flavorization'
    if 'already has the trait' in text:
        return 'trait'
    if ' has history ' in text and "won't execute" in text:
        return 'history'
    return None


def load(path):
    return load_verified(path, hashlib.sha256((path/'manifest.json').read_bytes()).hexdigest())


def collect(args):
    old, new = load(args.production), load(args.candidate)
    records=[]
    total=occurrences=0
    print('Scanning all retained contextual messages.',flush=True)
    for row,count in native_evidence_rows(args.bundle/'native_evidence.json'):
        total+=1; occurrences+=count
        kind=family(row['native'])
        if kind is None:continue
        unit=dict(source_family=row['source_family'],source_tag=row['source_family'],context_kind=row['context_kind'],
            body=dict(text=row['native'],pieces=row['pieces']),
            contexts=next(iter(row['contexts'].values()),{}),continuations=row['continuations'])
        outcomes={}
        for label,package in (('production',old),('candidate',new)):
            answer=package.match(dict(unit,parser=package.manifest['parser']),inspect=True)
            selected=answer['assignment']
            outcomes[label]=dict(selected=selected['template_id'] if selected else None,
                status=selected['match_status'] if selected else 'no_match',
                compatible=[m['template_id'] for m in answer['inspection']['matches']],
                regions=selected['regions'] if selected else [])
        records.append(dict(family=kind,example_id=row['example_id'],message=row['native'],pieces=row['pieces'],
            source=row['source_family'],occurrences=count,provenance=row['native_occurrences'],outcomes=outcomes))
    result=dict(scope=dict(contextual_rows=total,occurrences=occurrences),records=records,
        production_package=old.manifest['package_id'],candidate_package=new.manifest['package_id'],
        templates={label:{t['template_id']:dict(template_id=t['template_id'],display=t['display'],status=t['status'])
                          for t in package.data['templates'] if family(t['display'])}
                   for label,package in (('production',old),('candidate',new))})
    write_json(args.output/'families.json',result)
    print(json.dumps({k:dict(messages=sum(r['family']==k for r in records),occurrences=sum(r['occurrences'] for r in records if r['family']==k),
        candidate_assignments=dict(Counter(r['outcomes']['candidate']['selected'] for r in records if r['family']==k)))
                     for k in ('activity','flavorization','trait','history')},indent=2),flush=True)


def activity_probe(data, package):
    from template_learning.patterns import _slot, derive_pattern
    from template_learning import regions
    from template_learning.records import SequenceRecord, identity
    from template_learning.matching_primitives import display_pattern
    from template_learning.matching_defaults import analyze_match_pattern
    rows=[r for r in data['records'] if r['family']=='activity']
    left=' is aborting current travel plan while still participating in activity '
    right='. Use `remove_from_activity` to gracefully exit the activity before aborting.'
    records=[];spans=[];values=[];piece_values=[]
    for row in rows:
        text=row['message']; pieces=tuple(map(tuple,row['pieces']))
        start=text.index(left)+len(left); end=text.index(right,start)
        offsets=[0]
        for _,value in pieces:offsets.append(offsets[-1]+len(value))
        a,b=offsets.index(start),offsets.index(end)
        records.append(SequenceRecord(row['source'],text,pieces))
        spans.append((a,b));values.append(text[start:end]);piece_values.append(pieces[a:b])
    inferred=_slot(values,left,piece_values)
    assessment=regions.field_evidence(inferred,records,spans)
    full=next(deepcopy(p) for t in package.data['templates'] if t['template_id']=='ee7f96f3c3b501ac6180eed7'
              for p in t['parts'] if p.get('type')=='CHARACTER_FULL_ID')
    full['name']='character'
    param=deepcopy(inferred);param['name']='activity'
    tail=rows[0]['message'].split(right,1)[1]
    parts=[dict(kind='literal',text=' Activity participant '),full,dict(kind='literal',text=left),param,
           dict(kind='literal',text=right+tail)]
    matches=[]
    for record,expected in zip(records,values):
        result=analyze_match_pattern(parts,record.text,pieces=record.pieces)
        captures=result['captures']
        actual=next((c['value'] for c in captures if c['name']=='activity'),None) if captures else None
        assert actual==expected and result['count']==1,(record.text,result)
        matches.append(dict(message=record.text,value=actual,complete_assignments=result['count']))
    hypotheses=[]
    current,failures=derive_pattern(records,records[0],hypotheses=hypotheses)
    return dict(status='bounded proposal test only; not implemented or published',display=display_pattern(parts),
        messages=len(rows),matches=matches,inferred_whole_span_type=inferred['type'],
        current_boundary_assessment=assessment,current_group_display=display_pattern(current),
        current_group_rejected_fields=[dict(type=p['type'],values=p['observed_values'],reason=p['rejection_reason'])
                                      for p in current if p.get('rejection_reason')],
        current_group_consistency_failures=len(failures),current_group_hypotheses=hypotheses,
        consistency_examples=[dict(message=next(r.text for r in records if identity(r.key)==h['record_id']),**h)
                              for h in hypotheses if h.get('proposal') in {'capture_ambiguity','capture_replay'}],
        observed_periods_inside_values=sum('.' in v for v in values))


def render(args, data):
    def esc(text):
        return html.escape(''.join(f'\\u{ord(c):04x}' if ord(c)<32 and c not in '\r\n\t' else c for c in str(text)))
    pre=lambda text:'<pre>'+esc(text)+'</pre>'
    titles={'activity':'Activity descriptions','flavorization':'Character flavorization names',
            'trait':'Displayed trait names','history':'History diagnostic wording'}
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Adjacent-field family review</title>',
          '<style>body{font:16px/1.6 system-ui;max-width:1120px;margin:36px auto;padding:0 22px;color:#172333}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf2f6;padding:15px}article{border-top:2px solid #ccd7df;margin-top:34px}code{overflow-wrap:anywhere}a{color:#0759a5}</style>',
          '<h1>Adjacent fields: complete families, accurate counts, numbered examples</h1>',
          '<p>Comparison: production <code>'+data['production_package']+'</code> → candidate <code>'+data['candidate_package']+'</code>. '
          'Searched all 73 retained logs: 91,925 contextual records / 2,594,588 occurrences. Counts below describe selected classifications across that corpus, not the smaller example groups used to infer individual templates.</p>',
          '<h2>What the earlier “member failure” count meant</h2>',
          '<p>That was implementation terminology, not an owner-defined error category. It counted example messages for which an inferred pattern had no unique complete capture assignment, or whose matched field ranges differed from the ranges used to infer it; incompatible inferred boundaries also enter that list. The earlier test found zero such consistency failures when re-inferring the final 400 example groups. It did not establish that their slot types were semantically correct, that every corpus message matched, or that no proposals were rejected during learning. Bad KEY typing can pass this check.</p>',
          '<p>The behavior is documented in LEARNER_INFERENCE_RULES: complete matching must reproduce each example’s inferred field spans; failed unions are rejected and examples are retained for reconsideration. The phrase “member failure” itself adds no product taxonomy. It has been removed from the report’s success claim.</p>',
          '<h2>Why these names are not already whole PARAMs</h2>',
          '<p>Reaching the adjacent-word check is not the cause. The earlier type inference accepts a continuous token as KEY before considering PARAM. The new check only revisits all-alphabetic values varying together. Hyphens, formatting controls and possessive strings exclude these examples. A directly enclosing quote pair can also exclude the new check; it does not itself assign PARAM. Recognized fields are protected, but an unrecognized multiword name can still arrive here fragmented.</p>',
          '<p>For undeclared PARAMs, the current boundary check requires observed variation plus a matched enclosing pair. Stable sentence text on both sides alone is not accepted by that check. This is why an activity PARAM needs a deliberate boundary-rule improvement rather than an assertion that the existing protection already recognizes it.</p>',
          '<h2>Reading this report</h2><p>Each family appears once. Old templates are grouped with their actual candidate results; unchanged patterns are displayed once. Where multiple old templates share a candidate, all predecessors appear together. The history family intentionally retains two literal formulations. The activity family currently has three templates and two unmatched messages: a proposed single PARAM template is shown separately and is not misrepresented as the delivered candidate.</p>',
          '<p>Examples have unique global IDs (E01, E02, …). Repeated references link to the same example rather than duplicating its text. Game control bytes are shown as Unicode escapes; exact strings and provenance remain in <a href="families.json">the evidence JSON</a>.</p>']
    number=0
    for section,kind in enumerate(('activity','flavorization','trait','history'),1):
        rows=[r for r in data['records'] if r['family']==kind]
        # Connected components keep an old alternative from being repeated under
        # several successors. Compatibility evidence is not an occurrence count.
        graph=defaultdict(set)
        for r in rows:
            successor=('new',r['outcomes']['candidate']['selected'])
            graph[successor]
            for tid in r['outcomes']['production']['compatible']:
                before=('old',tid);graph[before].add(successor);graph[successor].add(before)
        components=[];seen=set()
        for node in sorted(graph,key=str):
            if node in seen:continue
            todo=[node];component=set()
            while todo:
                current=todo.pop()
                if current in component:continue
                component.add(current);todo.extend(graph[current]-component)
            seen.update(component);components.append(component)
        examples={}
        shown_patterns={}
        def pattern(text):
            if text in shown_patterns:
                anchor=shown_patterns[text]
                return f'<p>Same displayed pattern as <a href="#{anchor}">{anchor}</a> above.</p>'
            anchor=f'P{section}.{len(shown_patterns)+1}'
            shown_patterns[text]=anchor
            return f'<div id="{anchor}"><p><strong>{anchor}</strong></p>'+pre(text)+'</div>'
        def example(row):
            nonlocal number
            key=row['example_id']
            if key not in examples:
                number+=1;examples[key]=(f'E{number:02d}',row)
            label=examples[key][0]
            return f'<a href="#{label}">{label}</a>'
        bits.extend([f'<article id="{kind}"><h2>{section}. {titles[kind]}</h2>',
            f'<p><strong>{len(rows)} distinct messages / {sum(r["occurrences"] for r in rows)} occurrences</strong> across the 73 logs.</p>'])
        if kind=='activity':
            bits.append('<p>The earlier “2 distinct messages / 2 occurrences” described one template’s retained inference examples. In the complete corpus that template selects 4 messages. Family totals: 7 supported assignments, 1 provisional assignment, 2 unmatched. Production and candidate give the same results.</p>')
        for index,component in enumerate(components,1):
            before=sorted(tid for side,tid in component if side=='old')
            after=sorted((tid for side,tid in component if side=='new'),key=str)
            scoped=[r for r in rows if r['outcomes']['candidate']['selected'] in after]
            bits.append(f'<h3>{section}.{index}. Production → candidate</h3>')
            for tid in before:
                t=data['templates']['production'][tid]
                witness=next(r for r in scoped if tid in r['outcomes']['production']['compatible'])
                unchanged=tid in after and data['templates']['candidate'][tid]['display']==t['display']
                bits.append('<p>'+('Production and candidate — unchanged' if unchanged else 'Production')+
                            f' · <code>{tid}</code> · {t["status"]} · example {example(witness)}</p>'+pattern(t['display']))
            for tid in after:
                selected=[r for r in scoped if r['outcomes']['candidate']['selected']==tid]
                if tid is None:
                    bits.append('<p><strong>No candidate assignment</strong>: '+', '.join(example(r) for r in selected)+'</p>')
                    continue
                t=data['templates']['candidate'][tid]
                bits.append(f'<p>Candidate <code>{tid}</code>: {len(selected)} selected messages / '
                            f'{sum(r["occurrences"] for r in selected)} occurrences; '+', '.join(example(r) for r in selected[:2])+'.</p>')
                if tid not in before or data['templates']['production'][tid]['display']!=t['display']:
                    bits.append(pattern(t['display']))
        if kind=='activity':
            probe=data['activity_proposal']
            for failure in probe['consistency_examples']:
                witness=next(r for r in rows if r['message']==failure['message'])
                bits.extend(['<h3>A genuine example of the consistency check</h3>',
                    '<p>When all ten messages are inferred together with the existing rules, the proposed pattern splits the activity into two PARAMs around repeated game-formatting text. Example '+example(witness)+' permits two complete divisions:</p>'])
                for n,assignment in enumerate(failure.get('witnesses',[]),1):
                    values=[c['value'] for c in assignment if c['type']=='PARAM']
                    bits.append(f'<p>Division {n}</p>'+pre('\n'.join(f'PARAM {i}: {v}' for i,v in enumerate(values,1))))
                bits.append('<p>The check rejects that ambiguous division instead of selecting one arbitrarily. This is an inference experiment, not a new production outcome. The single whole-activity PARAM below has exactly one complete assignment for the same message.</p>')
            bits.extend(['<h3>Proposed one-template correction — bounded test, not published</h3>',pre(probe['display']),
                '<p>Capture the complete description after <code>participating in activity </code>, ending before <code>. Use `remove_from_activity`</code>. The period remains literal. All 10 genuine messages have one complete capture assignment with this proposed pattern, preserving the full CHARACTER_ID and every activity formatting byte. None of the 10 activity descriptions contains an internal period; using the observed following sentence gives a stronger boundary than stopping at an arbitrary period.</p>',
                '<p>The existing inference identifies the combined varying span as PARAM, but its ordinary boundary assessment rejects it because no enclosing pair exists. Recommendation: add a contextual field declaration using these verified markers; test it in the next disposable candidate. No learner rule or published package has been changed by this report.</p>',
                '<p>All ten activity examples: '+', '.join(example(r) for r in rows)+'.</p>'])
        bits.append('<h3>Genuine examples</h3>')
        for label,row in examples.values():
            message=(f'<p>This genuine message is identical to the all-literal pattern <a href="#{shown_patterns[row["message"]]}">{shown_patterns[row["message"]]}</a> above; its text is displayed there once.</p>'
                     if row['message'] in shown_patterns else pre(row['message']))
            bits.extend([f'<h4 id="{label}">{label} · {esc(row["source"])}</h4>',message,
                '<details><summary>Provenance and classifications</summary>'+pre(json.dumps(dict(provenance=row['provenance'],
                    occurrences=row['occurrences'],outcomes={k:{n:v for n,v in o.items() if n!='regions'} for k,o in row['outcomes'].items()}),ensure_ascii=False,indent=2))+'</details>'])
        bits.append('</article>')
    bits.append('<p><a href="adjacent-word-audit.json">Earlier final-group consistency evidence</a> · <a href="families.json">Full corpus family evidence and activity proposal test</a></p></html>')
    (args.output/'ADJACENT-WORDS.html').write_text('\n'.join(bits),encoding='utf-8')
    print(f'Rendered four families, {number} uniquely numbered examples.',flush=True)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--production',type=Path,required=True)
    cli.add_argument('--candidate',type=Path,required=True)
    cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--reuse-evidence',action='store_true')
    args=cli.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    if not args.reuse_evidence:collect(args)
    data=json.loads((args.output/'families.json').read_bytes())
    data['activity_proposal']=activity_probe(data,load(args.candidate))
    write_json(args.output/'families.json',data)
    render(args,data)


if __name__=='__main__':main()
