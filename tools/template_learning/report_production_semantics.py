"""Explain production-to-candidate changes from exact match/capture evidence."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path

from template_learning.evidence_serialization import write_json


def read(path):return json.loads(Path(path).read_bytes())


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    args=cli.parse_args();out=args.evidence
    gains=read(out/'production-gain-traces.json');removed=read(out/'removed-template-analysis.json')
    comparison=read(out/'comparison.json');training=read(out/'training-corpus-comparison.json')
    audit=read(out/'key-binding-audit.json');downgrades=read(out/'production-downgrade-traces.json')
    inherited=read(out/'inherited-key-witnesses.json')
    templates=removed['templates'];rows=removed['witnesses'];by_old=defaultdict(list);by_new=defaultdict(list)
    for row in rows:
        by_old[row['before']].append(row)
        if row['after']:by_new[row['after']].append(row)
    categories=[('slot_words_become_literals','Some diagnostic slot content becomes literal'),
        ('literal_words_become_slots','Some diagnostic literal content becomes a slot'),
        ('slot_types_change','Slot typing changes'),
        ('location_change_without_diagnostic_word_retyping','Location layout changes; diagnostic word roles unchanged'),
        ('no_diagnostic_word_retyping','Identical displayed pattern; constraints or metadata differ')]
    primary=Counter(next(k for k,_ in categories if any(r['theme']==k for r in rs)) for rs in by_old.values())
    location_gains=[]
    for row in gains['messages']:
        peers=[t for t in row['production_peers'] if t['same_displayed_diagnostic']]
        if not peers:continue
        actual=row['production_parameter_structures'];other=[s for s in actual if s!='located-parenthetical']
        peers=[t for t in peers if [s for s in t['parameter_structures'] if s!='located-parenthetical']==other]
        assert peers and all(t['gates']['context'] and t['gates']['construction'] and not t['gates']['parameters'] for t in peers)
        assert all(t['parameter_structures'].count('located-parenthetical')!=actual.count('located-parenthetical') for t in peers)
        location_gains.append(row)
    gained=sum(r['occurrences'] for r in gains['messages']);location_count=sum(r['occurrences'] for r in location_gains)
    assert gained==6063 and location_count==6048
    many={i:sorted({r['before'] for r in rs}) for i,rs in by_new.items() if len({r['before'] for r in rs})>1}
    assessment='Mostly positive versus production; a template-overlap issue and name-field limitations remain'
    executive=(f'Of {gained:,} newly classified stored-Run occurrences, {location_count:,} ({location_count/gained:.2%}) use diagnostic patterns already present in production. '
        'Their production assignments fail at the exact ordered parameter-structure check because the number of trailing location traces differs. '
        'The repeated-locator correction resolves that structural restriction without broadening the diagnostic wording. '
        'The other gains are 13 travel messages using the owner-directed date/character/location fields, the original scope mismatch using three quoted KEY fields, and one marked-up-name message requiring further typing review. '
        'The rejected character-history and Unknown effect/trigger KEY generalizations do not drive these gains. '
        'No production complete assignments are lost in either evaluated scope. Two training occurrences become provisional because two supported templates tie, with unchanged selected captures. '
        'This is positive evidence for the locator and recognized-field changes, not approval of every template or a claim of measured semantic accuracy.')
    next_steps=('Keep the locator/date/character changes. Investigate the overlapping marked-up-name templates and their retention/selection decisions; '
        'review whole-name field handling before broadening it. Keep the requested history PARAM work separate from this comparison: the candidate currently retains production’s two literal phrases. '
        'Retain the 18 removed-template IDs without selected witnesses as unverified. Do not introduce a global function-word ban: the audit distinguishes script identifiers from inherited grammatical KEY fields. Production stays unchanged pending review.')
    write_json(out/'production-semantic-review.json',dict(assessment=assessment,executive_summary=executive,recommended_next_steps=next_steps,
        baseline=comparison['production'],candidate=comparison['candidate'],location_layout_gain_occurrences=location_count,
        location_layout_gain_messages=len(location_gains),other_gain_occurrences=gained-location_count,
        primary_removal_categories=primary,unobserved_removed=len(removed['summary']['unobserved_removed']),
        scope='Production versus incremental candidate only; 73-log training evidence and 20 stored Runs kept separate'))
    esc=lambda x:html.escape(str(x))
    def visible(s):return ''.join(c if c in '\n\r\t' or ord(c)>=32 else '\\u%04x'%ord(c) for c in s)
    def pre(s):return '<pre>'+esc(visible(str(s)))+'</pre>'
    def pattern(label,i):
        t=templates[label][i]
        return '<p class="meta">'+label+' · '+esc(t['source_family'])+' · '+esc(t['status'])+' · '+i+'</p>'+pre(t['display'])
    def changes(row):
        ds=[d for d in row['changes'] if d['words'] and not d['location']]
        return '<table><tr><th>Exact text</th><th>Production → candidate</th></tr>'+''.join('<tr><td>'+pre(d['text'])+'</td><td>'+esc(d['before']+' → '+d['after'])+'</td></tr>' for d in ds)+'</table>' if ds else '<p>No diagnostic word changes its literal/slot role on this witness.</p>'
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Production versus candidate: matching mechanics</title>',
        '<style>body{font:16px/1.55 system-ui;max-width:1160px;margin:32px auto;padding:0 22px;color:#203746}h1,h2,h3{line-height:1.25}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef4f7;padding:14px;font-size:13px;max-height:380px;overflow:auto}table{width:100%;border-collapse:collapse}td,th{padding:9px;text-align:left;border-bottom:1px solid #cbd6df;vertical-align:top}td pre{margin:0}a{color:#086093}.meta{font-size:13px;color:#526674}.note{background:#eaf3fa;padding:18px}.review{background:#fff1d9;padding:18px}article{margin-top:26px;border-top:2px solid #cbd6df}summary{cursor:pointer;padding:8px 0}nav{display:flex;gap:18px;flex-wrap:wrap}</style>',
        '<h1>Production versus candidate: what actually changed?</h1><nav><a href="CHANGES.html">15 added / 15 removed / new matches</a><a href="#gains">Every new-match family</a><a href="#removals">Template consolidation</a><a href="#concerns">Remaining concerns</a><a href="#audit">Initial KEY audit</a><a href="FUNCTION-WORDS.html">Expanded function-word and contraction audit</a></nav>',
        '<p class="meta">Production 68f1ae5db205ab46afef9c4d → incremental candidate 83df10b8cfb86d1573f8e510. Same established 73-log corpus and recorded 20+20+20+13 build schedule. No one-shot-build comparison is used here.</p>',
        '<h2>'+esc(assessment)+'</h2><p class="note">'+esc(executive)+'</p><p><strong>Recommended next steps.</strong> '+esc(next_steps)+'</p>',
        '<h2>The dominant change: a location-count gate</h2><ol><li>Production recognizes the message’s source, context and diagnostic construction.</li><li>It records each trailing parenthetical trace as another <code>located-parenthetical</code> entry. Matching requires that ordered parameter list to equal the template’s list exactly.</li><li>A three-entry native location stack therefore cannot use an otherwise equivalent one- or two-entry template. For the 6,048 occurrences counted here, the trace count is the only difference in this applicability list. They fail before body binding or final selection.</li><li>The candidate removes recognized trailing location entries from that fixed parameter list. The literal <code>Script location:</code> remains; its following repeat requires one or more entries.</li><li>The matcher expands those entries and checks every file, line and trace capture against the original native spans. Exact values and count still determine message identity.</li></ol>',
        '<p>Concrete example: 5,236 occurrences of <code>Event target link \'global_var\' returned an unset scope</code> have three trailing entries. Production has the same <code>Event target link \'&lt;KEY&gt;\' returned an unset scope</code> diagnostic with one or two entries. The candidate captures <code>global_var</code> as that same KEY and stores all three locations; it does not turn “returned an unset scope” into a slot.</p>',
        '<h2 id="gains">All 17 new-match families</h2><p>These are all 81 newly classified contextual messages, totaling 6,063 occurrences across the same 20 stored Runs. Every one was rechecked through both pinned public matchers. Each section shows actual captures and the relevant production failure; it does not infer the cause from no_match alone.</p>']
    location_keys={r['key'] for r in location_gains}
    for group in gains['groups']:
        identifier=group['template_id'];rs=[r for r in gains['messages'] if r['candidate_template']==identifier]
        representative=rs[0]
        location_only=all(r['key'] in location_keys for r in rs)
        note=('Same diagnostic frame; production rejects the trailing trace-count mismatch.' if location_only else
              'Owner-directed date, short identity, receiver identity and complete location-name fields; production has separate fixed word-count layouts.' if identifier=='0e4e3302cde2fc5e07a2227f' else
              'Target, expected scope and actual scope occupy separate quoted KEY fields. Production has fixed expected-scope literals, including character; casus_belli does not satisfy those literals.' if identifier=='0213bb363ad56f39d7e953a5' else
              'Review: the diagnostic sentence remains fixed, but marked-up names are still split into KEY positions, including particles and formatting bytes. This one-occurrence gain is not evidence that the name typing is ideal.')
        bits.append('<article><h3>'+f'{group["occurrences"]:,}'+' occurrences · '+str(group['messages'])+' messages</h3>'+pattern('candidate',identifier)+'<p>'+esc(note)+'</p>')
        captures=[c for c in group['captures'] if c['type']!='LOCATOR' and not c['slot'].startswith('locations_')]
        bits.append('<table><tr><th>Slot</th><th>Type</th><th>Actual captured values in newly matched messages</th></tr>'+''.join('<tr><td>'+esc(c['slot'])+'</td><td>'+esc(c['type'])+'</td><td>'+pre('\n'.join(c['values']))+'</td></tr>' for c in captures)+'</table>')
        peers=representative['production_peers']
        if location_only:
            peers=[x for x in peers if x['same_displayed_diagnostic']]
            bits.append('<p>Native trailing trace count(s): '+esc(sorted({r['production_parameter_structures'].count('located-parenthetical') for r in rs}))+'. Production counts for the same displayed diagnostic: '+esc(sorted({x['parameter_structures'].count('located-parenthetical') for r in rs for x in r['production_peers'] if x['same_displayed_diagnostic']}))+'.</p>')
        bits.append('<details><summary>Exact genuine message, provenance and all candidate captures</summary>'+pre(representative['native_regions']['body'])+pre(json.dumps(representative['references'],ensure_ascii=True,indent=2))+pre(json.dumps(representative['candidate_assignment']['regions'],ensure_ascii=True,indent=2))+'</details>')
        bits.append('<details><summary>Production candidates and actual failure steps</summary>')
        for peer in peers[:3]:
            bits.append(pattern('production',peer['template_id'])+pre(json.dumps({k:peer[k] for k in ('gates','parameter_structures','pattern_trace')},ensure_ascii=True,indent=2)))
        bits.append('</details></article>')
    bits.append('<h2 id="removals">What became of the production templates?</h2><p>689 → 467 templates: 448 old IDs are absent, 226 IDs are added and 241 persist. Of the removed IDs, 430 have selected witnesses mapping to 195 candidate templates; 18 have no selected witness. Public matchers reproduced 622 witnesses across 438 distinct predecessor/successor pairs. These are observed destinations, not inferred ancestry.</p>')
    bits.append('<table><tr><th>Primary change to a removed template</th><th>Old template IDs</th></tr>'+''.join('<tr><td>'+esc(label)+'</td><td>'+str(primary[k])+'</td></tr>' for k,label in categories)+'<tr><td>No selected witness</td><td>18</td></tr></table><p>Counts are disjoint per old ID; a more substantive role change takes precedence over a location change. Literal-to-slot changes include names, dates and identifiers, not just grammatical wording. Changes are measured on one genuine witness per mapping and scope.</p>')
    bits.append('<h3>27 many-to-one consolidations, involving 263 removed IDs</h3><p>Location-layout-only consolidation is labelled separately from diagnostic slot/literal changes. Open any group to see every observed predecessor.</p>')
    for identifier,old_ids in sorted(many.items(),key=lambda item:-len(item[1])):
        group_rows=by_new[identifier];diagnostic=any(d['words'] and not d['location'] for r in group_rows for d in r['changes'])
        bits.append('<details><summary>'+str(len(old_ids))+' old templates → '+esc(templates['candidate'][identifier]['display'].split('Script location:')[0].strip())+' · '+('diagnostic field changes present' if diagnostic else 'location/layout changes; diagnostic word roles unchanged')+'</summary>'+pattern('candidate',identifier))
        for old in old_ids:
            witness=next(r for r in group_rows if r['before']==old)
            bits.append(pattern('production',old)+changes(witness))
        bits.append('</details>')
    bits.append('<h2 id="concerns">What still needs attention?</h2><h3>Two provisional outcomes are a selection tie</h3><p>The selected template is still supported by two distinct examples. A second supported template also matches with the same evidence rank. The selector reports <code>deterministic_tie_break</code>, <code>template_tie=true</code>, and two complete assignments; captures are not ambiguous. It conservatively marks the selected assignment provisional.</p>')
    for item in downgrades:
        chosen=item['result']['inspection']['selected_assignment']
        for match in item['result']['inspection']['matches']:bits.append(pattern('candidate',match['template_id']))
        bits.append('<details><summary>Exact selection evidence and genuine witness</summary>'+pre(json.dumps(chosen['selection'],indent=2))+pre(item['witness']['native_regions']['body'])+'</details>')
    bits.append('<p>This is one overlap between a literal <code>di</code> surname particle and a KEY position that can also capture it. It is not a loss of the diagnostic or its values. Removing a template or preferring more literal wording without checking its other assignments would be premature.</p><h3>Owner-reviewed wording</h3><p>In this candidate, <code>Unknown effect:</code> and <code>Unknown trigger:</code> remain literal categories, as in production. Character history retains separate <code>after death</code> and <code>from before</code> literal phrases; the requested shared PARAM remains unimplemented. Emblem colored/textured and Flag/Variable categories also remain separate. The accepted scope, trigger/effect-name, comparison and title-field improvements appear in the observed mappings above. Untyped-trigger applicability remains a separately declared construction and retains its pending owner assessment.</p>')
    bits.append('<h2 id="audit">Full 73-log KEY spelling audit</h2><p>91,925 contextual messages / 2,594,588 occurrences examined. This is a declared inventory of function-word spellings plus effect/trigger, not an exhaustive linguistic classifier. Counts below deduplicate repeated uses of the same spelling within one message. Per-template/slot counts and exact witnesses are in the linked JSON.</p><table><tr><th>KEY value</th><th>Messages</th><th>Occurrences</th><th>Context</th></tr>')
    contexts={'after':'Event / namespace identifier; four messages, five slot bindings. Not the character-history phrase.',
        'been':'Ordinary grammar in CK3 messages beginning “Parent (…) of …”; production already uses the same KEY captures on verified witnesses.',
        'in':'Multiword localization text; the same template ID exists in production.',
        'do':'Multiword localization text; the same template ID exists in production.',
        'of':'Localization text or name particles; review name-field typing separately.',
        'if':'Script effect identifier or reported unexpected token.', 'this':'Event target / invalid comparison / reported unknown effect identifier.',
        'all':'Reported unexpected token.', 'not':'Script trigger identifier.', 'And':'Reported GUI call name.', 'Not':'Reported GUI call name.',
        'none':'Reported scope/type, shortcut name or unexpected token.', 'None':'Reported title display content.'}
    for row in audit['values']:bits.append('<tr><td>'+esc(row['value'])+'</td><td>'+str(row['messages'])+'</td><td>'+str(row['occurrences'])+'</td><td>'+esc(contexts[row['value']])+'</td></tr>')
    bits.append('</table><p><code>before</code>, <code>from</code>, <code>effect</code> and <code>trigger</code> were not selected body KEY values in this corpus. Phrase typing in CK3 messages beginning <code>Parent (…) of …</code> is a real follow-up issue, but it is inherited from production and does not explain this candidate’s added coverage. Here “Parent” is literal game text referring to a character’s parent; it does not name a diagnostic category or a relationship between error messages. No global stop-word rule is justified by these findings.</p>')
    for witness in inherited:bits.append('<details><summary>Production already captures “been” as KEY</summary>'+pattern('production',witness['production_template'])+pattern('candidate',witness['candidate_template'])+pre(witness['native'])+pre(json.dumps(witness['production_capture'],indent=2))+'</details>')
    bits.append('<h2>Scope and verification</h2><p>The 73 training logs and 20 stored Runs overlap; their counts are not summed. This investigation reuses established input hashes and saved native records. All 81 new matches were inspected; capture-role changes for removed templates use 622 selected witnesses. Unknown future false positives are not measured by replaying this corpus. Parser recovery, production packages, Runs, source logs and runtime processes were not changed. The analysis modifies no learner rules.</p><p><a href="production-semantic-review.json">Assessment data</a> · <a href="production-gain-traces.json">All 81 matcher traces</a> · <a href="removed-template-analysis.json">Complete removal mapping and capture changes</a> · <a href="production-downgrade-traces.json">Selection-tie evidence</a> · <a href="key-binding-audit.json">All KEY audit bindings and examples</a> · <a href="inherited-key-witnesses.json">Production phrase witnesses</a></p></html>')
    (out/'SEMANTICS.html').write_text('\n'.join(bits),encoding='utf-8',newline='')
    print(json.dumps(dict(assessment=assessment,location_gain_occurrences=location_count,primary_categories=primary,many_to_one=len(many)),indent=2))


if __name__=='__main__':main()
