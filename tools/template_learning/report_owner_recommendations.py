"""Survey residual function-word KEYs and consolidate the owner's candidate review.

Review tooling only. Template IDs below identify inspected evidence, not learner rules.
"""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path

from template_learning.audit_key_bindings import capture_groups, hits
from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.report_function_words import GRAMMAR, review


RECOMMENDATIONS = {
    1: ('Present', 'Retain the complete parenthetical PARAM; preserve its exact contents.'),
    2: ('Partly consolidated', 'Retain the generic left/right KEY template. A literal left/scope template remains; check construction applicability before attempting to remove it.'),
    3: ('Present', 'Retain KEY trigger [REASON], with trigger literal.'),
    4: ('Present', 'Retain the quoted event-target KEY.'),
    5: ('Explained; owner acceptance pending', 'Keep the dedicated untyped construction for now. It is selected through construction applicability, not preference for more literals. Do not merge the constructions without proving equivalent extraction and matching.'),
    6: ('Present; location-layout change', 'Retain one-or-more trailing entries and exact ordered values. Report this separately from semantic consolidation.'),
    7: ('Requested PARAM still missing', 'Add the owner-directed field between has history and birth, won\'t execute. Capture after death / from before as one PARAM. Current candidate retains two literal phrases; do not report the requested correction as delivered.'),
    8: ('Separate, as in production', 'Retain colored/textured as separate literals for this candidate. The accepted broader grouping is optional, not a release requirement. No increased category-to-KEY sensitivity is demonstrated by the current production comparison.'),
    9: ('Separate, as in production', 'Retain Flag/Variable as separate literals. No need to force their optional consolidation. The original detailed sensitivity trace is still uncompleted, not superseded by a claim that the safeguard is proven sound.'),
    10: ('Rejected outcome absent from current candidate', 'Keep effect/trigger literal and retain these genuine cases as acceptance checks. Unknown remains literal here. The revision safeguard does not constrain initial slot typing; absence of the bad result does not prove all paths safe. A causal trace of the originally rejected outcome remains outstanding.'),
    11: ('Present', 'Retain all three quoted KEYs: target, expected scope and actual scope. Original war/casus_belli case is now classified.'),
    12: ('Accepted generalization not fully present', 'Current templates keep expected character and expected war literal. Generalize the expected-scope field using the observed scope values, while preserving the surrounding diagnostic wording; verify the current merge/applicability blocker before changing it.'),
    13: ('Present', 'Retain the complete quoted previous-holder display as PARAM.'),
    14: ('Accepted PARAM not present', 'Current candidate retains a KEY template and a separate literal control-character example. Capture the complete quoted formatting-tag field as PARAM, preserving every control character and line ending.'),
}


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--bundle',type=Path,required=True)
    args=cli.parse_args();root=args.evidence
    load=lambda name:json.loads((root/name).read_bytes())
    templates=load('removed-template-analysis.json')['templates']
    audit=load('function-word-audit.json')
    known={b['template_id'] for b in audit['bindings']}
    counts=defaultdict(Counter);groups=defaultdict(set);values=defaultdict(set)
    examples=defaultdict(list);total=affected=0;affected_occ=0
    for row,n in native_evidence_rows(args.bundle/'native_evidence.json'):
        total+=1;selected=row.get('selected_assignment')
        if not selected:continue
        found=[]
        for region,caps in capture_groups(selected):
            for cap in caps:
                if cap.get('type') in ('KEY','OPTIONAL_KEY') and cap.get('value') and hits(cap['value']):
                    found.append(dict(region=region,**cap))
        if not found:continue
        tid=selected['template_id'];assert tid in known
        category,note=review(tid,templates['candidate'][tid])
        counts[category]['messages']+=1;counts[category]['occurrences']+=n
        groups[category].add(tid);values[category].update(c['value'] for c in found)
        if len(examples[category])<8 and not any(e['template_id']==tid and e['values']==[c['value'] for c in found] for e in examples[category]):
            examples[category].append(dict(template_id=tid,text=row['native'],values=[c['value'] for c in found],captures=found,provenance=row['native_occurrences'][:1]))
        affected+=1;affected_occ+=n
        if total%20000==0:print('Surveyed',total,flush=True)
    assert total==audit['contextual_messages_scanned']
    assert (affected,affected_occ)==(audit['affected_contextual_messages'],audit['affected_occurrences'])
    survey=[dict(category=c,**counts[c],template_ids=sorted(groups[c]),values=sorted(values[c]),examples=examples[c]) for c in counts]
    # Use only the retained owner-case -> current-candidate IDs from the old index.
    # No fresh-model assignments, templates, or comparison results are used.
    cases=[];edges=load('training-corpus-comparison.json')['edges']
    for index in load('build-history-comparison.json')['cases']:
        number=index['number'];ids=index['incremental_templates'];es=[e for e in edges if e['after'] in ids]
        status,recommendation=RECOMMENDATIONS[number]
        cases.append(dict(number=number,title=index['title'],status=status,recommendation=recommendation,
            candidate_ids=ids,production_ids=sorted({e['before'] for e in es if e['before']}),
            contextual_messages=sum(e['messages'] for e in es),occurrences=sum(e['occurrences'] for e in es)))
    result=dict(scope='Production 68f1ae5db205ab46afef9c4d versus incremental candidate 83df10b8cfb86d1573f8e510 only; retained same 73 logs; no new model or inference changes.',
        limitation='Exhaustive review of the explicit function-word spelling inventory matches, not proof that every possible English grammatical misuse has been detected.',
        rows_scanned=total,flagged_rows=affected,flagged_occurrences=affected_occ,categories=survey,cases=cases)
    write_json(root/'owner-recommendations.json',result)
    esc=lambda s:html.escape(str(s))
    def pre(s):
        return '<pre>'+esc(''.join(c if c in '\r\n\t' or ord(c)>=32 else '\\u%04x'%ord(c) for c in str(s)))+'</pre>'
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Owner concerns: status and recommendations</title>',
        '<style>body{font:16px/1.5 system-ui;max-width:1200px;margin:32px auto;padding:0 24px;color:#243747}h1,h2{line-height:1.2}table{border-collapse:collapse;width:100%}td,th{padding:10px;vertical-align:top;text-align:left;border-bottom:1px solid #ccd6df}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;padding:12px;font-size:13px}.note{padding:18px;background:#fff0d7}details{margin:14px 0}summary{cursor:pointer}a{color:#075e91}</style>',
        '<h1>Owner concerns: status and recommendations</h1><p><a href="CHANGES.html">Template changes</a> · <a href="SEMANTICS.html">Production comparison</a> · <a href="FUNCTION-WORDS.html">All flagged KEY bindings</a> · <a href="owner-recommendations.json">Evidence</a></p>',
        '<p>'+esc(result['scope'])+'</p>',
        '<p class="note"><strong>Recommendation: retain the verified locator/date/character gains, but do not promote yet.</strong> Finish the phrase and whole-field typing corrections, resolve the two supported-template ties, and recheck accepted outcomes in the same incremental workflow. Better coverage alone does not close the owner’s semantic concerns.</p>',
        '<h2>Would hard-coding the two phrases be enough?</h2><p>For the grammatical diagnostic-wording defect found by this survey: yes, the remaining reviewed hits do not expose another English diagnostic phrase being split into KEYs. For all slot-typing issues: no. Multiword display names remain divided into KEY positions and need their own field-boundary correction. This is a bounded corpus finding, not a guarantee about unseen wording.</p>',
        '<p>Proposed contextual rule: in the observed <code>Parent (…) of … is … at file:</code> construction, capture <code>hasn’t been born</code> or <code>the wrong gender</code> as one PARAM, with the surrounding wording literal. Neither individual words nor every use of <code>is … at</code> become a global rule. This is a recommendation, not an already implemented correction. The separately directed history PARAM remains required.</p>',
        '<table><tr><th>Reviewed finding</th><th>Contextual messages</th><th>Occurrences</th><th>Templates</th></tr>']
    for s in survey:bits.append('<tr><td>'+esc(s['category'])+'</td><td>'+str(s['messages'])+'</td><td>'+str(s['occurrences'])+'</td><td>'+str(len(s['template_ids']))+'</td></tr>')
    bits.extend(['</table><p>Counts partition all '+str(affected)+' flagged rows; repeated words in a message do not multiply its count. All 313 flagged template/slot/value combinations across 33 templates were assigned a contextual review category. '+esc(result['limitation'])+'</p>',
        '<p>The 235 grammatical cases are 154 messages containing hasn’t been born and 81 containing the wrong gender, totaling 488 occurrences. Examples of residual field problems include Antiochia in Pisidien, Isle of Wight, The Isles, and marked-up names containing of Hampshire/of Suffolk. Preserve each complete field; a global ban on in/of/the would damage legitimate script and localization identifiers.</p>',
        '<p>Reported identifiers include if/not/this/after, GUI calls And/Not, and dotted localization keys. Other spelling matches include the month May, trait Just, and names In-mun/La-or. These are not English grammatical words in diagnostic wording. The complete per-binding examples are linked above.</p>',
        '<h2>All 14 owner-reviewed cases</h2><table><tr><th>Case</th><th>Current candidate status</th><th>Recommendation</th></tr>'])
    for case in cases:
        bits.append('<tr><td>'+esc(str(case['number'])+'. '+case['title'])+'</td><td>'+esc(case['status'])+'</td><td>'+esc(case['recommendation'])+'</td></tr>')
    bits.extend(['</table><h2>Other outstanding work and priorities</h2><ol>',
        '<li><strong>Phrase and field typing.</strong> Apply the two contextual phrase captures and the explicitly requested history PARAM. Capture the full formatting-tag field, including control characters. Correct multiword localization display fields as whole fields and investigate marked-up character-name boundaries using their actual formatting structure.</li>',
        '<li><strong>Two supported-template ties.</strong> di Urbino and di Rienzo still become provisional because the generic and literal-di templates tie with identical captures. Investigate safe retirement/subsumption of the overlapping template or a justified selection correction. Do not invent a blanket literal-preference rule.</li>',
        '<li><strong>Accepted generalizations.</strong> Finish the expected-scope field; inspect the surviving literal left/scope variant. Keep the untyped construction distinction pending owner acceptance. No need to force optional emblem or Flag/Variable consolidation.</li>',
        '<li><strong>Causal explanations remain incomplete.</strong> The current candidate avoids the originally rejected effect/trigger KEY outcome. That does not supply the requested exact initial-inference/merge/safeguard trace for the earlier failure. Do not label it fully explained or repeat a one-shot-versus-incremental comparison.</li>',
        '<li><strong>Verification.</strong> Freeze a new learner candidate after approved corrections; repeat the same 20+20+20+13 build and compare only with production on the same 73 training logs and 20 stored Runs. Report exact captures, all 14 cases, phrase/field residuals, overlapping templates and template removals. The 18 removed production IDs without selected witnesses remain unverified. No production activation or Run changes.</li></ol>',
        '<h2>What is already working</h2><p>All three original IS3QON diagnostics now receive supported assignments. Across the 20 stored Runs, 6,063 occurrences gained assignments and none lost one; 6,048 of those gains come from removing the trailing locator-count restriction, not broadening diagnostic wording. The 73-log check likewise loses no complete production assignments, but exposes the two template-to-provisional ties described above.</p>',
        '<p>Repeated locators retain all file/line/trace values and exact message identity. The date, short character identity, bounded receiver identity and line-ended default-location PARAM are present. Evidence-history duplication and bundle-writer memory corrections are in the current v54 build; the controlled incremental build completed. These remain disposable candidate results.</p>',
        '<h2>Current patterns and production predecessors</h2>'])
    for case in cases:
        bits.append('<details><summary>'+esc(str(case['number'])+'. '+case['title'])+'</summary><p>'+esc(str(case['contextual_messages'])+' training rows / '+str(case['occurrences'])+' occurrences')+'</p>')
        for label,ids in [('candidate',case['candidate_ids']),('production',case['production_ids'])]:
            for tid in ids:bits.append('<p>'+esc(label+' · '+tid)+'</p>'+pre(templates[label][tid]['display']))
        bits.append('</details>')
    bits.append('</html>');(root/'RECOMMENDATIONS.html').write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps([dict(category=s['category'],messages=s['messages'],occurrences=s['occurrences'],templates=len(s['template_ids'])) for s in survey],indent=2))


if __name__=='__main__':main()
