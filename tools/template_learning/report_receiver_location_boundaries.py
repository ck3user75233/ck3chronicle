"""Report genuine verification of the owner-directed receiver/location boundaries."""
import argparse
from collections import Counter
import html
import json
from pathlib import Path


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--experiment', type=Path, required=True)
    cli.add_argument('--baseline', type=Path, required=True)
    cli.add_argument('--version', choices=['v52','v53'], default='v52')
    args = cli.parse_args()
    out, baseline = args.experiment.resolve(), args.baseline.resolve()
    baseline_label = 'v52' if args.version=='v53' else 'v51'
    read = lambda p: json.loads(p.read_text(encoding='utf-8'))
    v = read(out/'verification.json')
    fields = read(out/'field-verification.json')
    all_rows = read(out/'all-short-identities.json')
    inventory = read(out/'location-boundary-inventory.json')
    model = read(next((out/'packages').glob('*/empirical_template_model.json')))
    before = read(next((baseline/'packages').glob('*/empirical_template_model.json')))
    old = {t['template_id']: t for t in before['templates']}
    new = {t['template_id']: t for t in model['templates']}
    changes = dict(added=[new[k] for k in sorted(new.keys()-old.keys())],
                   removed=[old[k] for k in sorted(old.keys()-new.keys())],
                   unchanged=len(old.keys() & new.keys()))
    assert all_rows['one_template_required'] and not all_rows['unmatched_messages']
    assert not v['failures'] and not v['status_downgrades']
    assert all(t['assignment']['status']=='template' for t in v['targets'])
    if args.version=='v53':
        previous = {r['text']:r for r in read(baseline/'all-short-identities.json')['rows']}
        receiver_values = {r['text']:r['receiver'] for r in fields['fields']}
        preserved = 0
        for row in all_rows['rows']:
            flatten = lambda item: [(b['slot_id'],b['type'],b['value'],b['present']) for r in item['assignment']['values']['regions'] for b in r['bindings']]
            current = flatten(row)
            typed = [b for b in current if b[1]=='CHARACTER_ID_SUPER_SHORT']
            assert len(typed)==1 and typed[0][2]==receiver_values[row['text']]
            assert [(i,'PARAM' if t=='CHARACTER_ID_SUPER_SHORT' else t,value,present) for i,t,value,present in current]==flatten(previous[row['text']])
            assert row['assignment']['rendered']==previous[row['text']]['assignment']['rendered']
            preserved += 1
        (out/'receiver-type-transition.json').write_text(json.dumps(dict(messages=preserved,only_capture_change='receiver PARAM -> CHARACTER_ID_SUPER_SHORT',all_values_and_other_types_preserved=True),indent=2),encoding='utf-8')
    totals = Counter()
    for r in v['runs']:
        totals.update(r['counts']['candidate'])
    summary = dict(version=args.version, package=v['candidate_package'], pin=v['candidate_pin'], model=model['revision_id'],
                   all_75_template=True, template_id=all_rows['rows'][0]['assignment']['values']['template_id'],
                   definition_counts={k: len(changes[k]) for k in ('added','removed')},
                   unchanged_definitions=changes['unchanged'], stored_counts=totals,
                   stored_transitions=v['transitions'], original_run_counts=v['original_run_pipeline_counts'],
                   failures=v['failures'], status_downgrades=v['status_downgrades'])
    (out/'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    esc = lambda value: html.escape(str(value))
    pre = lambda value: '<pre>'+esc(value)+'</pre>'
    bits = ['''<!doctype html><meta charset="utf-8"><title>Owner-directed receiver and location boundaries</title>
<style>body{font:16px/1.55 system-ui;max-width:1080px;margin:36px auto;padding:0 24px;color:#183040}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eff4f7;padding:16px;font-size:13px}summary{cursor:pointer}.note{background:#eaf4fa;border-left:4px solid #36799c;padding:16px}</style>
<h1>Owner-directed receiver and location boundaries — v52</h1>
<p class="note">Executable owner rules have been updated and a fresh disposable candidate built. All 75 genuine travel messages retain complete assignments through one shared template. Production remains unchanged.</p>
<h2>Implemented boundaries</h2>
<p><code>default location is &lt;PARAM&gt;</code>: the first capitalized word immediately after the marker starts the field. The period ends the field and remains literal. Native line ending also ends it, because every genuine example in the 104-log search lacks a period. Complete multiword names and exact spelling are retained; trailing presentation whitespace stays outside the capture.</p>
<p><code>receiver is &lt;PARAM&gt;, default location is …</code>: the marker supplies the approved fallback for the shortest character display-name form. The existing executable rule captures the entire receiver, including titles and lowercase words. It already works for all 75 receivers; this update records the owner's explicit marker authorization. It does not mislabel the plain receiver as the numeric-parenthesis CHARACTER_ID_SHORT.</p>
<p>The numeric-parenthesis CHARACTER_ID_SHORT rule remains independent of a preceding date. Its exported description has been corrected to match that implementation. Date KEY recognition, full IDs, parser, locator handling and the 0.72 similarity threshold are unchanged.</p>''']
    if args.version=='v53':
        assert all_rows['receiver_type']=='CHARACTER_ID_SUPER_SHORT'
        bits = ['''<!doctype html><meta charset="utf-8"><title>Corrected location boundary and typed receiver — v53</title>
<style>body{font:16px/1.55 system-ui;max-width:1080px;margin:36px auto;padding:0 24px;color:#183040}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eff4f7;padding:16px;font-size:13px}summary{cursor:pointer}.note{background:#eaf4fa;border-left:4px solid #36799c;padding:16px}table{border-collapse:collapse;width:100%}td,th{padding:8px;text-align:left;border-bottom:1px solid #bbc}</style>
<h1>Corrected location boundary and typed receiver — v53</h1>
<p class="note">All 75 genuine travel messages have complete assignments with CHARACTER_ID_SUPER_SHORT for the receiver. The unsupported period boundary has been removed. This is a freshly built and verified executable candidate; production remains unchanged.</p>
<h2>Corrections</h2>
<p>All 75 genuine default-location values end at the native line ending, with no terminal period. That evidence should have corrected the earlier suggestion: v52 should not have introduced a speculative period terminator. v53 removes it. The capitalized-start default-location field remains PARAM, ending at the native line ending; periods have no special boundary role and trailing presentation whitespace stays outside the capture.</p>
<p>There was no dedicated super-short type in v52. It used an effective marker-bounded PARAM for the receiver. v53 reuses that verified recognition but emits CHARACTER_ID_SUPER_SHORT, preserving the complete displayed name between receiver is and the following comma/default-location marker. This is a bounded reusable rule, not a global capitalization/Name of Place recognizer. Numeric-parenthesis CHARACTER_ID_SHORT and full IDs remain separate and unchanged.</p>
<h2>Why the older report showed literal receiver names</h2>
<p>The locator-presence-candidate/CHANGES.html page is the v49 report. Its actual candidate definitions had literal receivers; this was not merely original-message display. The receiver became PARAM in v50 and remained PARAM through v52. It becomes CHARACTER_ID_SUPER_SHORT in v53. Earlier explanations should have identified that version difference explicitly. The old page now includes the current template and actual captures above its clearly labelled historical content.</p>''']
    bits.append('<h2>Shared learned definition</h2>'+pre(summary['template_id'])+pre(all_rows['rows'][0]['definition']))
    if args.version=='v53':
        bits.append('<h2>Actual current captures for the two original travel diagnostics</h2>')
        for target in v['targets']:
            if 'Starting travel with incorrect receiver' not in target['text']:continue
            bindings=[b for r in target['assignment']['values']['regions'] for b in r['bindings']]
            bits.append('<p>Original emission '+str(target['provenance']['emission_ordinals'][0])+' — '+esc(target['assignment']['status'])+'</p><table><tr><th>Slot type</th><th>Exact captured value</th></tr>'+''.join('<tr><td>'+esc(b['type'])+'</td><td>'+esc(b['value'])+'</td></tr>' for b in bindings)+'</table>')
    bits.append('<h2>Genuine verification</h2><p>Same 20 complete training logs: 731,529 messages. Corpus inventory: 104 logs. Stored comparison: unchanged public-handler export of 18 Runs, 48,772 records / 766,476 occurrences. The original Run is included in training; these are coverage checks, not an independent holdout accuracy claim.</p>')
    bits.append('<p>All-75 transitions from '+baseline_label+':</p>'+pre(json.dumps(all_rows['transitions'],indent=2)))
    bits.append('<p>Stored-Run transitions from '+baseline_label+':</p>'+pre(json.dumps(v['transitions'],indent=2)))
    bits.append('<p>Zero failed checks and zero downgrades. Every selected assignment reconstructs its native text. Existing LOCATOR values, original three diagnostics, continuation/wrapper witnesses and four earlier effect regressions pass. Exact date, short identity, receiver and location captures and distinct message identities pass for all 75 examples.</p>')
    bits.append('<p>Boundary inventory:</p>'+pre(json.dumps(inventory['counts'],indent=2)))
    limits = ('No period terminator is declared. Lowercase-start locations, undated numeric short IDs and super-short recognition outside the declared receiver markers are not established by this corpus.' if args.version=='v53' else 'No genuine period-terminated or lowercase-start default-location example was found. Those branches cannot be empirically verified here; no examples were invented. No undated short-ID emitter was found.')
    bits.append('<p>'+limits+' Full-ID preservation:</p>'+pre(json.dumps(fields['full_id_preserved_occurrences'],indent=2)))
    bits.append('<p>Package export parity:</p>'+pre(json.dumps(v['export_validation'],indent=2)))
    if args.version=='v53':
        bits.append('<p><a href="receiver-type-transition.json">Capture comparison with v52</a>: all 75 receivers change type only; their values, all other captured values/types (including trace PARAMs), and reconstructed text remain identical.</p>')
    bits.append('<h2>Definition changes versus '+baseline_label+'</h2>'+pre(json.dumps({k:summary[k] for k in ('definition_counts','unchanged_definitions')},indent=2)))
    bits.append('<p>'+('The shared travel definition now displays the dedicated receiver type. Exact receiver values and all previously matched travel examples are preserved.' if args.version=='v53' else 'The displayed templates remain unchanged because all observed location values already satisfy the new boundaries. The executable declaration inside the new package has changed; unchanged template counts do not mean this was documentation-only.')+'</p>')
    declarations = [d for d in model['owner_rules']['parameter_structures'] if d['id'] in {'default-location-name','receiver-before-default-location'}]
    bits.append('<details><summary>Actual declarations saved in the candidate</summary>'+pre(json.dumps(declarations,indent=2,ensure_ascii=False))+'</details>')
    for label in ('added','removed'):
        bits.append('<details><summary>'+label.title()+'</summary>'+''.join(pre(t['template_id']+'\n'+t['display']) for t in changes[label])+'</details>')
    historical = read(out.parent/'character-date-candidate/all-short-identities.json')
    repaired_texts = set(historical['unmatched_messages'])
    repaired = [r for r in all_rows['rows'] if r['text'] in repaired_texts]
    assert len(repaired)==19
    bits.append('<h2>The nineteen formerly unmatched examples</h2><p>These already improved in v51; all remain template assignments in '+args.version+'. Full original message bodies follow.</p>')
    for row in repaired:
        bits.append('<details><summary>'+esc(row['text'].split('default location is ',1)[1].strip())+' — template</summary>'+pre(row['text'])+'</details>')
    bits.append('<h2>Immutable candidate</h2>'+pre(json.dumps({k:summary[k] for k in ('package','pin','model')},indent=2)))
    bits.append('<p>No production selection/catalog changes, candidate database writes, protected-log edits or runtime restarts. The separate repeated-entry line:/near line: equivalence limitation is unchanged.</p>')
    bits.append('<p><a href="summary.json">Summary</a> · <a href="verification.json">Stored-Run checks</a> · <a href="all-short-identities.json">All 75 assignments</a> · <a href="location-boundary-inventory.json">Boundary inventory</a> · <a href="release.json">Frozen learner</a> · <a href="publish-execution.json">Export receipt</a> · <a href="../character-location-candidate/CHANGES.html">Historical v51 report</a></p>')
    (out/'CHANGES.html').write_text('\n'.join(bits), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
