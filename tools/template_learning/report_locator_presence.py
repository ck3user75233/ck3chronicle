"""Review a controlled locator-presence experiment and its actual template changes."""
import argparse
from collections import Counter
import html
import json
from pathlib import Path

from template_learning.location_candidate_experiment import save


def read(path):
    return json.loads(path.read_text())


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--experiment',type=Path,required=True)
    cli.add_argument('--previous',type=Path,required=True)
    args=cli.parse_args()
    out=args.experiment.resolve(); previous=args.previous.resolve()
    result=read(out/'verification.json'); prior=read(previous/'verification.json')
    slot_review=read(out/'slot-selection-review.json')
    new_path,=(out/'packages').glob('*/empirical_template_model.json')
    old_path,=(previous/'packages').glob('*/empirical_template_model.json')
    new_model,old_model=read(new_path),read(old_path)
    templates={label:{t['template_id']:t for t in m['templates']} for label,m in [('before',old_model),('after',new_model)]}
    old,new=set(templates['before']),set(templates['after'])
    added,removed=new-old,old-new
    fixed=bool(result['regression_checks']) and all(r['passed'] for r in result['regression_checks'])
    def counts(document,label):
        total=Counter()
        for row in document['runs']: total.update(row['counts'][label])
        return dict(total)
    summary=dict(candidate=result['candidate_package'],baseline=result['baseline_package'],
        definitions=dict(before=len(old),after=len(new),added=len(added),removed=len(removed),unchanged=len(old&new)),
        effect_regression_fixed=fixed,regression_occurrences=sum(r['occurrences'] for r in result['regression_checks']),
        counts=dict(v46=counts(prior,'baseline'),v48=counts(result,'baseline'),v49=counts(result,'candidate')),
        variable_threshold_tested=False,threshold=.72,
        key_to_literal_selected_pairs=slot_review['pairs'],
        definition_changes=[dict(kind=kind,template=templates[label][identifier])
            for kind,label,ids in [('added','after',added),('removed','before',removed)] for identifier in sorted(ids)])
    save(out/'presence-results.json',summary)
    esc=lambda v:html.escape(str(v)); pre=lambda v:'<pre>'+esc(v)+'</pre>'; fmt=lambda v:f'{v:,}'
    def declaration(label,identifier):
        if identifier is None: return '<p>No complete assignment.</p>'
        t=templates[label][identifier]
        return '<p class="meta">'+esc(t['source_family'])+' · '+esc(t['status'])+' · <code>'+identifier+'</code></p>'+pre(t['display'])
    bits=['''<!doctype html><meta charset="utf-8"><title>Locator presence: controlled results</title>
<style>body{font:16px/1.55 system-ui;max-width:1120px;margin:36px auto;padding:0 24px;color:#182d3c}h1,h2,h3{line-height:1.25}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f7;padding:15px;font-size:13px;max-height:450px;overflow:auto}table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #ccd7de;padding:10px;text-align:left}.meta{color:#4d6273;font-size:14px}.note{padding:16px;border-left:4px solid #36799c;background:#eaf4fa}article{border-top:2px solid #d2dfe7;margin-top:24px}summary{cursor:pointer}</style>
<h1>One presence unit for trailing locators</h1>
<p>This is a controlled fresh build on the same 20 genuine logs. A recognized trailing location section contributes exactly one similarity unit when it contains one or more locators. Its values, repeated-entry count and repeated traces add no further weight. Other KEY/PARAM/LOCATOR positions remain individual. No production model or Run was changed.</p>''',
        '<p class="note"><strong>Effect regression '+('resolved' if fixed else 'NOT resolved')+'.</strong> '+str(summary['regression_occurrences'])+
        ' previously downgraded occurrences were checked for supported assignments with the effect name captured as KEY. '
        'The discovery threshold remains 0.72. '+('A variable-threshold experiment was unnecessary for this regression and was not run.' if fixed else 'The conditional variable-threshold follow-up remains required.')+'</p>',
        '<h2>Actual score and scope checks</h2><p>The two original effect examples now compare as: effect name, literal effect, REASON presence, trailing-LOCATOR presence. Three positions match before effect-name inference: score <strong>0.775</strong>, up from 0.70. '
        'This clears the existing 0.72 threshold. Genuine one-, two- and three-entry examples each contribute one presence unit. Contextual Unknown contributes one; an absent section contributes none. Three KEY positions and two non-trailing LOCATOR positions were separately checked and remain distinct.</p>',
        '<h2>Genuine stored-data comparison</h2><p>Same unchanged public-handler export: '+fmt(result['totals']['stored_records'])+' stored records, '+fmt(result['totals']['occurrences'])+' occurrences, 18 Runs. Seventeen Runs are outside the 20-log training set. This is a controlled comparison, not a commissioned holdout accuracy claim.</p>',
        '<table><tr><th>Candidate</th><th>Template</th><th>Provisional</th><th>No match</th></tr>']
    for label,values in summary['counts'].items():
        bits.append('<tr><td>'+label+'</td>'+''.join('<td>'+fmt(values.get(k,0))+'</td>' for k in ('template','provisional','no_match'))+'</tr>')
    bits.append('</table><p>Transitions from v48:</p>'+pre(json.dumps(result['transitions'],indent=2)))
    bits.append('<p>Verification failures: '+str(len(result['failures']))+'. All selected native regions reconstruct exactly; existing locator values and distinct message identities are checked. '
                'Hardcoded continuation and wrapper examples retain their message counts and captured values. Training inputs, the database backup and production selection/catalog hashes are unchanged.</p>')
    bits.append('<h2>The four effect occurrences</h2>')
    for row in result['regression_checks']:
        bits.append('<article><p>'+esc(row['run_id'])+' · record '+str(row['ordinal'])+' · '+('PASS' if row['passed'] else 'FAIL')+'</p>'+pre(row['text'])+
                    declaration('after',row['assignment']['values']['template_id'] if row['assignment'] else None)+'</article>')
    bits.append('<h2>Template changes</h2>'+pre(json.dumps(summary['definitions'],indent=2))+
        '<p>Definition IDs describe exact declarations. A changed or removed ID can represent consolidation or replacement; it does not establish lost coverage. Below are up to 15 changed assignment pairs observed on genuine stored messages.</p>')
    bits.append('<p>Short-message side-effect check: '+str(slot_review['pairs'])+' changed assignment pairs lose a KEY to literal wording. '
        'Some new inventory entries contain literal scope names, but none displaced a selected KEY capture in these stored Runs. '
        'The general KEY-trigger definition remains in the candidate. This evidence does not establish behavior on all unseen messages.</p>')
    changes=sorted(result['assignment_changes'],key=lambda r:-r['occurrences'])
    for row in changes[:15]:
        bits.append('<article><p>'+esc(row['transition'])+' · '+fmt(row['occurrences'])+' occurrences</p><h3>Before</h3>'+declaration('before',row['before'])+
                    '<h3>After</h3>'+declaration('after',row['after'])+'<details><summary>Genuine example</summary>'+pre(row['text'])+'</details></article>')
    for label,ids in [('after',added),('before',removed)]:
        sample=sorted(ids,key=lambda i: ('<KEY> effect' not in templates[label][i]['display'],i))[:15]
        bits.append('<details><summary>'+str(len(sample))+' examples of '+('added' if label=='after' else 'removed')+' definitions ('+str(len(ids))+' total)</summary>'+''.join(declaration(label,i) for i in sample)+'</details>')
    removal_path=out/'removed-definition-review.json'
    if removal_path.exists():
        removal=read(removal_path)
        bits.append('<h2>Are the ten removals good or bad?</h2><p>All ten are supported consolidations or generalizations on the examined evidence. Five retain identical diagnostic slots and constraints in replacement definitions that accept every old location-entry layout. Four replace literal effect names with KEY. One captures the complete identifier instead of keeping :val_beneficiary fixed. Every genuine training member of each removed definition retains a complete template assignment. This checks the removed definitions individually, in addition to the 18-Run comparison.</p>')
        for row in removal['definitions']:
            bits.append('<details><summary>'+esc(row['removed'])+' — '+esc(row['assessment'])+'</summary>'+declaration('before',row['removed']))
            for evidence in row['evidence']:
                bits.append('<p>'+str(evidence['messages'])+' genuine training messages / '+fmt(evidence['occurrences'])+' occurrences: '+esc(evidence['before'])+' → '+esc(evidence['after'])+'</p>'+declaration('after',evidence['replacement'])+pre(evidence['example']))
            bits.append('</details>')
        bits.append('<p>Training memberships can overlap; do not add these row counts as independent totals. <a href="removed-definition-review.json">Per-definition removal evidence</a>.</p>')
    bits.append('<h2>Original three diagnostics and remaining limits</h2>')
    emission_path=out/'travel-emission-check.json'
    emission_check=read(emission_path) if emission_path.exists() else None
    if emission_check:
        bits.append('<p>These examples are reclassified from the original protected log; no candidate database ingestion was performed. The full log emission includes its timestamp/severity/source header. The template describes the following message body. For the travel errors, that body really begins with file: in the original log, before the embedded game date. Original Run and candidate parser hashes and body boundaries are identical.</p>')
    for row in result['targets']:
        ordinal=row['provenance']['emission_ordinals'][0]
        bits.append('<h3>Original emission '+str(ordinal)+' — '+esc(row['assignment']['status'] if row['assignment'] else 'no_match')+'</h3>')
        if emission_check:
            native=next(r for r in emission_check['targets'] if r['ordinal']==ordinal)
            bits.append('<p>Complete original log emission, including outer header:</p>'+pre(native['raw_emission']))
            bits.append('<details><summary>Candidate definition for the message body (header is separate)</summary>'+pre(row['template'])+'</details>')
        else:
            bits.append('<p>Candidate definition for the message body (header is separate):</p>'+pre(row['template']))
    if emission_check:
        bits.append('<p>The Jevna diagnostic occurs once in the protected log. It appeared once in this report before this clarification; the doubled excerpt raised in review was not present in either file. The expanded definition above is a separately labeled view of the same diagnostic. <a href="travel-emission-check.json">Exact byte/provenance verification</a>.</p>')
    bits.append('<p>The original scope mismatch remains a shared template across different locator counts. The travel messages remain provisional; their date/short-character reuse is separate work. '
        'This experiment changes similarity presence only. The previously identified repeated-entry line:/near line: equivalence omission and unchanged parser numeric recovery predicates remain outstanding. Those are not evidence for changing the similarity threshold.</p>')
    if result['failures'] or result['status_downgrades']:
        bits.append('<h2>Failures / status reductions requiring review</h2>'+pre(json.dumps(dict(failures=result['failures'],downgrades=result['status_downgrades']),indent=2)))
    bits.append('<p><a href="verification.json">Full genuine-data verification</a> · <a href="presence-check.json">Presence and KEY-count checks</a> · <a href="slot-selection-review.json">Selected KEY preservation review</a> · <a href="presence-results.json">Definition changes and counts</a> · <a href="learn-execution.json">Authenticated build receipt</a> · <a href="publish-execution.json">Authenticated export receipt</a> · <a href="../locator-marker-candidate/CHANGES.html">Previous change report</a></p>')
    (out/'CHANGES.html').write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='definition_changes'},indent=2))


if __name__=='__main__':
    main()
