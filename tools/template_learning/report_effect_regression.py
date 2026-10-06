"""Render genuine-evidence diagnosis without modifying learner artifacts."""
import argparse
import html
import json
import re
from pathlib import Path


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--review',type=Path,required=True)
    args=cli.parse_args()
    root=args.review
    trace=json.loads((root/'trace.json').read_text())
    before=json.loads((root/'v46-comparison.json').read_text())
    additive=json.loads((root/'v46-additive.json').read_text())
    ranking=json.loads((root/'ranking.json').read_text()) if (root/'ranking.json').exists() else None
    esc=lambda v:html.escape(str(v))
    pre=lambda v:'<pre>'+esc(v)+'</pre>'
    bits=['''<!doctype html><meta charset="utf-8"><title>Why the effect template split</title>
<style>body{font:16px/1.6 system-ui;max-width:1050px;margin:36px auto;padding:0 24px;color:#192b39}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f7;padding:16px}table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #cad5df;text-align:left}.note{padding:15px;background:#fff2d9;border-left:4px solid #af7213}summary{cursor:pointer}</style>
<h1>Confirmed discovery regression: the effect-name KEY</h1>
<p class="note">Owner follow-up confirmed an earlier implementation error: v48 removed repeated-location and trace slot-presence credit, although the recorded rule requires one typed position per recognized field regardless of its contents. Removing count dependence did not authorize removing presence credit. The missed candidate pairing described below is a downstream failure. This candidate is not ready for production approval.</p>
<h2>What the learner should infer</h2>''',pre(trace['joint_inference']['display']),
        '<p>Direct joint inference on the two original training members produces this definition with zero failed captures. Running ordinary discovery and regrouping on those two genuine members alone also produces the shared supported template. That inferred definition completely matches all four downgraded stored occurrences, including the catalyst examples. No template was hand-authored or inserted into a model.</p>',
        '<h2>Slot presence, short forms, and runtime matching</h2><p>The five inferred fields are KEY, REASON, file LOCATOR, line LOCATOR, and trace PARAM. All five have corresponding present fields in both examples. Literal <code>effect</code> also agrees. '
        'Before joint inference, the effect-name position is still compared as two different literal names. v48 additionally drops the three location/trace fields altogether, leaving only name, effect, REASON.</p>'
        '<p>A diagnostic calculation restoring those three typed presence units once, independent of repeated-entry count, scores this pair 0.85 before KEY inference. This is an illustrative calculation, not an implemented policy or a new model. '
        'The first correction to investigate is preserving field presence with count-independent weight; the bounded neighbor issue remains separately demonstrated.</p>'
        '<p>No general sliding scale is implemented. The current short-form exception admits equal-length comparisons of at most two units with at least 0.49 positional agreement. Longer comparisons use 0.72. This three-unit comparison missed the exception.</p>'
        '<p>Final runtime template matching uses no similarity percentage or sliding threshold. It requires complete literal, field-boundary/type, wrapper and continuation assignments. Values are captured and preserved; they are not compared against the observed training spelling of a slot.</p>',
        '<h2>Why the complete build missed it</h2><ol>',
        '<li>The old comparison counted the shared location fields and trace positions. Its score was '+f"{before['score']:.6f}"+'.</li>',
        '<li>Removing location influence leaves three comparison units: the effect name, literal <code>effect</code>, and a REASON field position. Two of the three agree. The score is '+f"{trace['raw_similarity']:.2f}"+', below the unchanged 0.72 threshold. Initial discovery therefore puts them in separate groups.</li>',
        '<li>The later regrouping step ranks candidates by an unordered set of wording/field labels and tries at most 12 neighbors. The full-build decision log contains 14 attempted unions involving these members, but no attempt to unite them with each other.</li>',
        '<li>They remain separate, each with one distinct example, and are labelled provisional. Binding, REASON extraction, and final selection did not cause the split; each has one complete assignment without a tie.</li></ol>',
        '<p>After recognized REASON and repeated-location regions are represented as units, the two native examples have 27 aligned units and differ at exactly one position: <code>activate_struggle_catalyst</code> versus <code>add_title_law</code>. This is direct evidence for the KEY slot. The fully inferred pair has identical comparison sequences and passes the existing regrouping threshold.</p>']
    if ranking:
        bits.append('<h3>Observed neighbor ranking in the genuine full source pool</h3>')
        for row in ranking['rankings']:
            peers=[p for p in row['candidates'] if p['target']]
            if peers:
                bits.append(pre(row['display'])+'<p>The matching partner ranked '+str(peers[0]['rank'])+' of '+str(len(row['candidates']))+' remaining candidates; the trial limit was 12. '
                            'The first 18 effect formulations tie under the coarse word-set similarity; template IDs break that tie. '
                            'When the later group is processed, only subsequent groups are searched, so this pair receives no second opportunity.</p>')
                bits.append('<details><summary>The first 12 candidates actually selected for consideration</summary>'+''.join(pre(p['display']) for p in row['candidates'][:12])+'</details>')
    bits.extend(['<h2>Does additive learning prevent this?</h2>',
        '<p><strong>Within v46, retention works.</strong> A focused source-API test using the authenticated v46 release and both genuine members retained the old supported template, with two settled records and zero reopened discovery records. This was not a full additive campaign.</p>',
        '<p><strong>It does not solve the v46-to-v48 change.</strong> The supported workflow requires identical learner implementation, rules, parser and threshold for additive continuation. The locator change altered that implementation, so a fresh model was required. Carrying the old model forward as a v48 seed is explicitly rejected. Starting additive work from this split v48 candidate has no old shared definition to preserve; more evidence is not a reliable remedy for a missed candidate pairing.</p>',
        '<h2>Corrections to investigate</h2><p>First restore recognized field-presence credit with weight independent of repetition count. Then evaluate the short-template scale and candidate retrieval: structurally aligned variants should receive a joint-inference trial using their ordered native structure. Keep complete native replay, field evidence and wording-preservation checks as the acceptance gates. The existing two examples suffice to verify this case; no additional logs or effect-name whitelist is required.</p>',
        '<p>This investigation changes research tools and documentation only. It does not implement a new grouping policy, rebuild a model, alter source logs or stored Runs, or activate a production package. The separately identified repeated-entry line/near-line equivalence gap remains outstanding.</p>',
        '<h2>Original training evidence</h2>'])
    for row in trace['native_examples']:
        bits.append(pre(row['text'])+'<p>Native record <code>'+row['record_id']+'</code>; '+str(row['occurrences'])+' occurrence(s).</p>')
    bits.append('<p><a href="slot-presence-check.json">Slot-presence check and illustrative score</a> · <a href="trace.json">Authenticated candidate evidence and inference trace</a> · <a href="v46-comparison.json">Old comparison units</a> · <a href="v46-additive.json">Focused additive check</a> · <a href="four-record-verification.json">All four downgraded occurrences match the jointly inferred definition</a> · <a href="../locator-marker-candidate/CHANGES.html">Template change report</a></p>')
    (root/'DIAGNOSIS.html').write_text('\n'.join(bits),encoding='utf-8')
    changes=root.parent/'locator-marker-candidate'/'CHANGES.html'
    if changes.exists():
        text=changes.read_text(encoding='utf-8')
        note='<p class="note" id="effect-regression"><strong>Confirmed discovery regression:</strong> repeated-location and trace slot-presence credit was mistakenly removed; the missed candidate pairing is a downstream failure. <a href="../effect-regression-review/DIAGNOSIS.html">Read the corrected diagnosis and short-template check</a>. This candidate is not ready for production approval.</p>'
        if 'id="effect-regression"' not in text:
            text=text.replace('</nav>','</nav>\n'+note,1)
        else:
            text=re.sub(r'<p class="note" id="effect-regression">.*?</p>',lambda _:note,text,count=1,flags=re.S)
        changes.write_text(text,encoding='utf-8')
    print(root/'DIAGNOSIS.html')


if __name__=='__main__':
    main()
