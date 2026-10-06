"""Human review of the owner's three corrections, with genuine raw witnesses."""
import argparse
import html
import json
from pathlib import Path

from template_learning.matcher_example import load_verified
from template_learning.inventory import sha256_file
from template_learning.records import SequenceRecord
from template_learning.evidence_serialization import write_json


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--production',type=Path,required=True)
    args=cli.parse_args();root=args.evidence
    read=lambda name:json.loads((root/name).read_bytes())
    verified=read('literal-corrections-verification.json');records=read('literal-corrections-evidence.json')
    dates=read('all-short-identities.json')
    assert dates['messages']==75 and not dates['unmatched_messages']
    assert all(r['after']=='template' for r in dates['rows'])
    check=read('comparison.json');training=read('training-corpus-comparison.json')
    package=load_verified(args.production,sha256_file(args.production/'manifest.json'))
    old_id='0ebbfabd31d46b3ad046b464';old_template=package.matcher.by_id[old_id]
    checked={r['example_id']:r for r in verified['checked']}
    raw_emissions={r['example_id']:r for r in read('localization-raw-emissions.json')}
    raw_examples=[]
    for r in records:
        if not r['localization']:continue
        record=SequenceRecord(r['source'],r['text'],tuple(map(tuple,r['pieces'])))
        old=package.matcher.rules.match_record(old_template,record);assert old is not None
        unit=dict(parser=package.manifest['parser'],source_family=r['source'],context_kind='body',
                  body=dict(text=r['text'],pieces=r['pieces']),contexts={},continuations=[])
        selected=package.match(unit)['assignment'];assert selected
        raw_examples.append(dict(text=r['text'],raw_emission=raw_emissions[r['example_id']]['raw_emission'],
            occurrences=r['occurrences'],provenance=r['provenance'],
            old_complete_captures=old['captures'],production_selected=package.matcher.by_id[selected['template_id']]['display'],
            candidate=checked[r['example_id']]['template']))
    assert old_id in check['removed']
    write_json(root/'reviewed-localization-removal.json',dict(old_template=old_template['display'],template_id=old_id,
        assessment='Owner accepts removal as an improvement; complete field replaces fragmented display-name layouts.',examples=raw_examples))
    esc=lambda value:html.escape(str(value))
    pre=lambda value:'<pre>'+esc(value)+'</pre>'
    bits=['<!doctype html><html><head><meta charset="utf-8"><title>Literal corrections and raw examples</title><style>body{font:17px/1.55 system-ui;max-width:1100px;margin:40px auto;padding:0 24px;color:#182638}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f7;padding:18px;border-radius:8px}h1,h2{line-height:1.25}a{color:#075db0}.note{background:#e3f2e8;padding:18px}details{margin:16px 0}</style></head><body>',
        '<h1>Owner corrections: literal dates and history wording</h1><p><a href="CHANGES.html">Full production comparison: 15 new, up to 15 removed, and newly classified examples</a></p>',
        '<p>The numbering below refers to the samples in the v56 CHANGES report, not the separate fourteen-case review.</p>',
        '<p class="note">Implemented and verified in a new disposable candidate. Game dates are equivalent literals, never KEY captures. History wording remains literal. The reviewed missing-localization removal is an improvement. Production selection, Runs and source logs are unchanged.</p>',
        '<h2>Removed sample 6 — improvement by removing an incorrect template</h2>',pre(old_template['display']),
        '<p>Both genuine messages below completely matched this old template, but production selected a different, also fragmented, three-KEY template. This explains why the removed template had no selected witness in the earlier crosswalk. The candidate preserves the whole reported value as PARAM. Neither example contains numeric ID parentheses, full-ID labels or character markup; these messages alone do not establish a character identity.</p>']
    for r in raw_examples:
        bits.extend([pre(r['raw_emission']),'<p>'+esc(str(r['occurrences'])+' occurrences; production selected:')+'</p>',pre(r['production_selected']),'<p>Candidate:</p>',pre(r['candidate'])])
    bits.append('<h2>Removed sample 11 — history wording restored to literals</h2>')
    if (root/'history-inference-correction.json').exists():
        trace=read('history-inference-correction.json')
        baseline=read('history-inference-baseline.json')
        bits.extend(['<p>The two hard-coded history constructions have been removed. The learner now checks adjacent ordinary alphabetic KEY proposals that always vary together. A space alone does not establish that they are independent fields. It reconsiders their complete span and applies the existing boundary requirements.</p>',
            '<p>Here, <code>after death</code> and <code>from before</code> lack a supported enclosure or declared field boundary. The combined field is rejected and literal refinement retains the two complete formulations. PARAM is only an intermediate rejected proposal; it is not an emitted slot in either final template. The rule contains no history phrases, emitter names or English stop-word list.</p>',
            '<h3>Reproduced failure without the old construction gates</h3>',pre(baseline['initial']['display']),
            '<p>Alignment kept the shared space, splitting the two-word variation into separate KEYs. Both word positions have only two observed, paired combinations. Recognized fields, quoted spans, identifiers with syntax, optional positions, line breaks and observed independently varying word columns are excluded from this correction.</p>',
            '<p><a href="history-inference-baseline.json">Baseline alignment and decisions</a> · <a href="history-inference-correction.json">Corrected inference, refinement lineage and adjacent-KEY inventory</a></p>'])
    else:
        bits.append('<p>The owner’s latest direction supersedes the earlier PARAM instruction. This older candidate uses separate construction applicability; that implementation was disputed and does not establish acceptance of the mechanism.</p>')
    for row in verified['inferred']:
        if 'has history ' in row['display']:bits.append(pre(row['display']))
    bits.append('<p>'+esc(f"Verified all {verified['counts']['history']} distinct history messages / {verified['occurrences']['history']} occurrences in the 73-log evidence.")+'</p>')
    bits.extend(['<h2>Newly classified sample 3 — equivalent literal date</h2>',
        '<p><code>{game date}</code> denotes a format-constrained literal position, not a slot. A date with the declared day/month/year spelling before the colon matches that position regardless of its value. The matcher saves the exact spelling in <code>literal_choices</code>; it remains part of rendering and message identity. The outer [HH:MM:SS] timestamp is unaffected.</p>'])
    travel=next(r for r in dates['rows'] if 'Wijayatunggadewi' in r['text'])
    bits.extend([pre(travel['text']),pre(travel['definition']),'<p>Exact selected layout, including the literal date:</p>',
        pre(json.dumps(travel['assignment']['values']['regions'][0]['layout'],ensure_ascii=False,indent=2)),
        '<p>All 63 date-prefixed training messages pass. The separate saved 75-example corpus check, including messages outside the 73 training logs, is linked below. No names, numeric IDs, traces or location values were rewritten.</p>'])
    bits.extend(['<h2>Verification and production comparison</h2>',pre(json.dumps(training['transitions'],indent=2)),
        '<p><a href="literal-corrections-verification.json">All exact literal/history/identity checks</a> · <a href="all-short-identities.json">All 75 genuine character/date messages</a> · <a href="reviewed-localization-removal.json">Raw localization evidence and old captures</a> · <a href="FIXES.html">Other accepted corrections</a></p>',
        '<p>The space-separated date spelling is verified. The previously requested hyphenated spelling has no genuine corpus witness and is not claimed as empirically verified. Template counts and coverage do not by themselves establish semantic correctness. Review the new immutable package before any release or pin change.</p></body></html>'])
    (root/'LITERAL-CORRECTIONS.html').write_text('\n'.join(bits),encoding='utf-8')
    page=root/'CHANGES.html';text=page.read_text(encoding='utf-8')
    note='<p class="note"><strong>Latest owner corrections:</strong> <a href="LITERAL-CORRECTIONS.html">Raw examples for prior removal 6; literal history wording for prior removal 11; equivalent literal dates for prior newly classified example 3.</a> The reviewed localization removal is an improvement, even though that particular old template had no selected witness.</p>'
    text=text.replace('<h1>',note+'<h1>',1)
    page.write_text(text,encoding='utf-8')
    print(json.dumps(dict(report=str(root/'LITERAL-CORRECTIONS.html'),raw_localization_messages=len(raw_examples))))


if __name__=='__main__':main()
