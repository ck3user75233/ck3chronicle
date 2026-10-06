"""Render the genuine short-character/date investigation and candidate results."""
import argparse
from collections import Counter
import html
import json
from pathlib import Path


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--experiment',type=Path,required=True)
    args=cli.parse_args();out=args.experiment.resolve()
    read=lambda name:json.loads((out/name).read_text())
    corpus=read('corpus.json');fields=read('field-verification.json');v=read('verification.json');all_rows=read('all-short-identities.json')
    esc=lambda x:html.escape(str(x));pre=lambda x:'<pre>'+esc(x)+'</pre>'
    bits=['''<!doctype html><meta charset="utf-8"><title>Game dates and short character identities</title>
<style>body{font:16px/1.55 system-ui;max-width:1100px;margin:36px auto;padding:0 24px;color:#183040}h1,h2,h3{line-height:1.25}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f7;padding:15px;font-size:13px;max-height:420px;overflow:auto}table{border-collapse:collapse;width:100%}th,td{border-bottom:1px solid #cbd7de;padding:10px;text-align:left}summary{cursor:pointer}article{border-top:2px solid #d2dfe7;margin-top:24px}.note{padding:16px;background:#eaf4fa;border-left:4px solid #36799c}</style>
<h1>Game dates, short character identities, and receiver names</h1>
<p>The previous candidate omitted the earlier requested word-month date and short-character recognition. This disposable candidate adds those fields through the existing declared-parameter mechanism. The parser, production selection, stored Runs and runtime processes are unchanged.</p>''']
    bits.append('<h2>What the genuine corpus contains</h2><p>'+str(corpus['logs'])+' distinct complete retained logs, '+f"{corpus['bytes']:,}"+' bytes, each hash verified. The search covers day/month/year strings with space or hyphen separators, numeric-comma parenthesis endings, receiver markers, and possible capitalized name-of-place expressions outside labelled full-ID and numeric short-ID lines. It is a bounded syntax inventory, not a universal character-name census.</p>')
    bits.append('<p><strong>75 date/short-ID messages, all in one family:</strong> Starting travel with incorrect receiver, from jomini_effect_impl.cpp. No second diagnostic family with those date or numeric-comma short-ID forms was found. All observed dates use spaces and three-letter month names: 19 have three-digit years, 56 have four-digit years. Hyphenated dates are owner-requested and accepted by the declaration, but have no genuine witness here.</p>')
    bits.append('<table><tr><th>Words in complete display name</th><th>Occurrences</th></tr>'+''.join('<tr><td>'+n+'</td><td>'+str(c)+'</td></tr>' for n,c in sorted(fields['name_word_counts'].items(),key=lambda x:int(x[0])))+'</table><p>These are whitespace-separated display-name words, not raw parser token counts or separate entities.</p>')
    bits.append('<p>Using the actual parser token count instead, there are '+str(fields['name_raw_token_counts']['1'])+' one-token names and '+str(fields['name_raw_token_counts']['3'])+' three-token names; punctuation accounts for the difference. Complete raw-token histogram:</p>'+pre(json.dumps(fields['name_raw_token_counts'],sort_keys=True)))
    for count in (1,3,6):
        r=next(r for r in fields['fields'] if r['name_words']==count)
        bits.append(pre(r['identity']))
    bits.append('<h2>Exact recognition and full-form comparison</h2><p>The existing implementation is named CHARACTER_FULL_ID (28 declared contexts across 17 source families). It consumes the entire variable-length name, terminal of plus zero/one key, and parentheses beginning with Internal ID. Historical ID is optional within that opaque content. It does not require capitalization or independently capture the internal fields.</p>')
    bits.append('<p>The short form is CHARACTER_ID_SHORT: the entire display name plus (numeric ID, display location). Genuine short names can contain titles and of components, lowercase particles, apostrophes and untranslated dynasty keys. The current v50 rule uses the preceding format-locked date and following colon; it names no source family, mod, character or travel-error wording. The complete identity remains one exact opaque slot.</p>')
    bits.append('<p><strong>Correction following owner review:</strong> the proposed capitalization test concerns the first name word, with unrestricted later words. Viviana de Torres and Akurat Misibsen of Nabel satisfy that rule; they only refute an all-words-capitalized rule, which was not the owner\'s proposal. A literal first-character-uppercase test for name and location passes 74 of 75 examples. The remaining name begins ʾAmīr: uppercase A follows a leading transliteration modifier. All 75 numeric-comma endings in the 104-log scan belong to this character formulation; no non-character counterexample was found. This supports the proposed shape in the observed emitter/context. The date guard in v50 is conservative, not a necessity established by these examples.</p>')
    bits.append('<p>The date becomes one KEY with a declared date-format constraint. All recognized date values contribute the same single similarity unit; the colon stays literal, exact date spelling remains stored and contributes to message identity. Dotted-date handling remains unchanged. Game dates are separate from the outer [HH:MM:SS] log timestamp.</p>')
    bits.append('<h2>Receiver names: why a bounded PARAM was needed</h2><p>Before this change, the 75 receiver examples had '+str(fields['baseline_receiver_capture_counts'].get('literal',0))+' literal receivers and '+str(fields['baseline_receiver_capture_counts'].get('no_match',0))+' unmatched messages; none captured the receiver as PARAM. After adding only date and short-ID recognition, the two target messages exceeded the similarity threshold but still split because the existing owner-directed rules reject unmarked multiword PARAM inference.</p>')
    bits.append('<p>The new receiver declaration captures the complete value between receiver is and , default location is. It is a PARAM, without guessing a character from its name, and applies across source families. Both field markers remain literal.</p>')
    bits.append('<p>The broader scan found 187 candidate name-of-place expressions outside full/short identity lines (154 distinct source/line/position witnesses). Their previous captures were:</p>'+pre(json.dumps(fields['plain_titled_capture_counts'],indent=2))+'<p>These counts include non-character expressions. Real character references often occur inside intact REASON fields. Quoted title names can be PARAMs. Child of Concubine and Coat of Arms demonstrate why the text shape alone must not imply a character.</p>')
    for category in ('REASON','PARAM','literal','no_match'):
        r=next(r for r in fields['plain_titled_examples'] if category in r['capture_categories'])
        bits.append('<details><summary>'+category+' — '+esc(r['value'])+'</summary>'+pre(r['text'])+'</details>')
    bits.append('<h2>Fresh candidate and genuine verification</h2>'+pre(json.dumps(dict(package=v['candidate_package'],pin=v['candidate_pin'],training=v['training_summary'],stored_totals=v['totals'],stored_transitions=v['transitions'],failures=v['failures'],downgrades=len(v['status_downgrades']),full_id_fields_preserved=fields['full_id_preserved_occurrences']),indent=2)))
    bits.append('<p>Same 20-log build as v49; same 18-Run public-handler export/unchanged backup. Seventeen stored Runs are outside the training set. Complete capture reconstruction, exact identity distinction, existing locator values, continuation examples and the four previous effect regressions are checked. No synthetic examples or production ingestion.</p>')
    bits.append('<p>Verification-tool correction: the first all-75 replay asserted a list-of-lists against the renderer\'s list-of-tuples and failed on representation type. The assertion was corrected to the actual API shape; the complete rerun checks exact text and all three field values. No native-text mismatch was found.</p>')
    changes=read('definition-changes.json')
    bits.append('<h2>Template inventory changes</h2><p>'+str(changes['added'])+' shared definitions replace '+str(changes['removed'])+' former literal-heavy travel definitions; '+str(changes['unchanged'])+' definition IDs are unchanged. Every added/removed definition belongs to this travel family.</p>')
    for t in changes['added_definitions']:
        bits.append('<p>'+esc(t['status'])+' · '+esc(t['template_id'])+'</p>'+pre(t['display']))
    bits.append('<details><summary>Ten replaced definitions</summary>'+''.join(pre(t['display']) for t in changes['removed_definitions'])+'</details><p><a href="definition-changes.json">Complete definition comparison</a>.</p>')
    bits.append('<h2>Original three diagnostics</h2>')
    original=json.loads((out.parent/'locator-presence-candidate/travel-emission-check.json').read_text())
    for row in v['targets']:
        native=next(r for r in original['targets'] if r['ordinal']==row['provenance']['emission_ordinals'][0])
        assert native['body']==row['text']
        bits.append('<article><p>'+esc(row['assignment']['status'] if row['assignment'] else 'no_match')+'</p><p>Complete original emission, including the outer log header:</p>'+pre(native['raw_emission'])+'<p>Candidate definition for its message body:</p>'+pre(row['template']))
        if row['assignment']:
            bindings=[{k:b[k] for k in ('type','value')} for region in row['assignment']['values']['regions'] for b in region['bindings']]
            bits.append('<details><summary>Exact captured values</summary>'+pre(json.dumps(bindings,indent=2,ensure_ascii=False))+'</details>')
        bits.append('</article>')
    bits.append('<h2>All 75 short identities: coverage and remaining limitation</h2>'+pre(json.dumps(all_rows['transitions'],indent=2)))
    bits.append('<p>All 75 have correct date, whole short-identity and whole receiver recognition. Complete-template coverage is measured separately above. Multiword default-location display names remain subject to existing inference and may retain literal formulations or remain unmatched. The target values Vepsamaa and Jianing are ordinary KEYs once the preceding fields are recognized. This experiment does not declare all location display names to be single-token KEYs or script LOCATORs.</p>')
    for r in [r for r in all_rows['rows'] if r['before']=='no_match' and r['after']!='no_match'][:15]:
        bits.append('<details><summary>Previously unmatched → '+esc(r['after'])+'</summary>'+pre(r['text'])+pre(r['definition'])+'</details>')
    if all_rows['unmatched_messages']:
        bits.append('<details><summary>Remaining unmatched genuine travel messages</summary>'+''.join(pre(t) for t in all_rows['unmatched_messages'])+'</details>')
    bits.append('<p>Evidence: <a href="corpus.json">104-log syntax inventory</a> · <a href="field-verification.json">Field boundaries / full-ID preservation / receiver survey</a> · <a href="all-short-identities.json">All 75 candidate outcomes</a> · <a href="verification.json">18-Run verification</a> · <a href="learn-execution.json">Build receipt</a> · <a href="publish-execution.json">Export receipt</a> · <a href="../locator-presence-candidate/CHANGES.html">Previous candidate report</a>.</p>')
    (out/'CHANGES.html').write_text('\n'.join(bits),encoding='utf-8')
    print(out/'CHANGES.html')


if __name__=='__main__':main()
