"""Review the rebuilt short-ID and complete-location candidate against v50."""
import argparse
from collections import Counter
import html
import json
from pathlib import Path


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--experiment',type=Path,required=True)
    cli.add_argument('--baseline',type=Path,required=True)
    args=cli.parse_args();out=args.experiment.resolve();old=args.baseline.resolve()
    read=lambda path:json.loads(path.read_text())
    v=read(out/'verification.json');all_rows=read(out/'all-short-identities.json');before=read(old/'all-short-identities.json');fields=read(out/'field-verification.json')
    new_path,=(out/'packages').glob('*/empirical_template_model.json')
    old_path,=(old/'packages').glob('*/empirical_template_model.json')
    new_model=read(new_path);old_model=read(old_path)
    a={t['template_id']:t for t in old_model['templates']};b={t['template_id']:t for t in new_model['templates']}
    changed=dict(added=[b[i] for i in sorted(b.keys()-a.keys())],removed=[a[i] for i in sorted(a.keys()-b.keys())],unchanged=len(a.keys()&b.keys()))
    new_by_text={r['text']:r for r in all_rows['rows']}
    repaired=[new_by_text[text] for text in before['unmatched_messages']]
    assert len(repaired)==19 and all(r['after']=='template' for r in repaired)
    assert all_rows['one_template_required'] and not all_rows['unmatched_messages']
    totals={label:Counter() for label in ['baseline','candidate']}
    for r in v['runs']:
        for label in totals:totals[label].update(r['counts'][label])
    summary=dict(package=v['candidate_package'],pin=v['candidate_pin'],model=new_model['revision_id'],
        repaired_messages=19,all_75_template=True,template_id=all_rows['rows'][0]['assignment']['values']['template_id'],
        inventory=dict(added=len(changed['added']),removed=len(changed['removed']),unchanged=changed['unchanged']),
        stored_counts=totals,stored_transitions=v['transitions'],failures=v['failures'],status_downgrades=v['status_downgrades'])
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    esc=lambda x:html.escape(str(x));pre=lambda x:'<pre>'+esc(x)+'</pre>'
    bits=['''<!doctype html><meta charset="utf-8"><title>Implemented candidate: short IDs and complete location names</title>
<style>body{font:16px/1.55 system-ui;max-width:1100px;margin:36px auto;padding:0 24px;color:#183040}h1,h2,h3{line-height:1.25}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f7;padding:15px;font-size:13px;max-height:440px;overflow:auto}table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #cbd7de;padding:10px;text-align:left}summary{cursor:pointer}article{border-top:2px solid #d2dfe7;margin-top:24px}.note{padding:16px;background:#eaf4fa;border-left:4px solid #36799c}</style>
<h1>Implemented candidate: short IDs and complete location names</h1>
<p class="note"><strong>All 75 genuine travel examples now receive complete template assignments through one shared definition.</strong> This includes all 19 messages previously rejected at their multiword final location. This report describes a freshly built, authenticated executable package. Production remains unchanged.</p>
<h2>What changed in executable recognition</h2>
<p>CHARACTER_ID_SHORT no longer requires a date. At the start of a body or after a colon field boundary, its first name word must begin capitalized; subsequent words are unrestricted. The numeric ID and first-capitalized display location inside parentheses identify the ending. The genuine leading transliteration modifier in ʾAmīr is accepted without altering the captured value. The rule has no source-family, mod, name or date whitelist. Applicability to an undated emitter is not demonstrated by this corpus: all 75 genuine examples happen to carry dates.</p>
<p>The text after default location is is now one complete PARAM, ending at the native line ending. Both Jianing and Golfo di Napoli occupy that same field. It represents a displayed place name; the existing KEY grammar and script LOCATOR fields are unchanged. Exact spelling, punctuation and whitespace remain reconstructible.</p>
<p>The receiver remains one PARAM bounded by its field markers. Plain Name of Place text alone is not globally classified as a character: genuine counterexamples include Coat of Arms, Child of Concubine and Duchy of Venice. Date KEY recognition remains format-constrained, and the following colon stays literal. The similarity threshold remains 0.72.</p>''']
    bits.append('<h2>Shared learned definition</h2><p>'+esc(summary['template_id'])+'</p>'+pre(all_rows['rows'][0]['definition']))
    bits.append('<h2>Genuine verification</h2><p>Fresh build on the same 20 complete logs (731,529 messages); corpus checks use all 75 inventoried short-ID examples from 104 distinct complete logs. Stored comparison uses the unchanged public-handler export of 18 Runs: 48,772 records / 766,476 occurrences. All examples retain exact native values and distinct identity digests. The original Run is included in training; these are corpus coverage checks, not an independent holdout accuracy claim.</p>')
    bits.append('<p>All-75 transitions from v50:</p>'+pre(json.dumps(all_rows['transitions'],indent=2)))
    bits.append('<p>Stored-Run transitions from v50:</p>'+pre(json.dumps(v['transitions'],indent=2)))
    bits.append('<p>Failed checks: '+str(len(v['failures']))+'. Status downgrades: '+str(len(v['status_downgrades']))+'. Existing LOCATOR values, full-ID recognition and hardcoded continuation examples are checked. Full-ID occurrence checks:</p>'+pre(json.dumps(fields['full_id_preserved_occurrences'],indent=2)))
    bits.append('<p>Export validation replays every actual training assignment and capture against the package:</p>'+pre(json.dumps(v['export_validation'],indent=2)))
    bits.append('<h2>The nineteen repaired examples</h2><p>Every item below was no_match under v50 and is template under this candidate. Text shown is the exact original message body; the outer timestamp/source header is separate.</p>')
    for row in repaired:
        bits.append('<details><summary>'+esc(row['text'].split('default location is ',1)[1].strip())+' — no_match → template</summary>'+pre(row['text'])+'<p>Captured final field:</p>'+pre(row['text'].split('default location is ',1)[1].rstrip('\r\n'))+'</details>')
    bits.append('<h2>Template inventory</h2>'+pre(json.dumps(summary['inventory'],indent=2)))
    bits.append('<p>The two removed definitions are replaced by the shared definition above: one required a final KEY, and the other fixed Mgikuyu Sabaki as literal text. The new final PARAM covers both and the nineteen formerly unmatched multiword values. All 56 previously matched corpus examples remain template assignments; these removals consolidate coverage.</p>')
    for label in ['added','removed']:
        bits.append('<details><summary>'+label.title()+' definitions</summary>'+''.join('<p>'+esc(t['template_id'])+'</p>'+pre(t['display']) for t in changed[label])+'</details>')
    bits.append('<h2>Original three review diagnostics</h2>')
    originals=read(out.parent/'locator-presence-candidate/travel-emission-check.json')
    for row in v['targets']:
        native=next(r for r in originals['targets'] if r['ordinal']==row['provenance']['emission_ordinals'][0]);assert native['body']==row['text']
        bits.append('<details><summary>Emission '+str(native['ordinal'])+' — '+row['assignment']['status']+'</summary><p>Complete original emission:</p>'+pre(native['raw_emission'])+'<p>Candidate body definition:</p>'+pre(row['template'])+'</details>')
    bits.append('<h2>Candidate identity and scope</h2>'+pre(json.dumps({k:summary[k] for k in ['package','pin','model']},indent=2)))
    bits.append('<p>Parser and production selection/catalogs are unchanged. No candidate ingestion, database modifications or runtime restarts. This verifies the available genuine corpus; it is not proof about every unseen spelling or emitter. The older repeated-entry line:/near line: equivalence gap is outside this correction.</p>')
    bits.append('<p><a href="summary.json">Result summary</a> · <a href="all-short-identities.json">All 75 complete assignments</a> · <a href="field-verification.json">Exact field checks</a> · <a href="verification.json">18-Run comparison</a> · <a href="release.json">Frozen learner</a> · <a href="learn-execution.json">Build execution</a> · <a href="publish-execution.json">Export execution</a> · <a href="../character-date-candidate/CHANGES.html">Historical v50 report</a>.</p>')
    (out/'CHANGES.html').write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
