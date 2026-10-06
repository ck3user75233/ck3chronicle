"""Explain template inventory changes using authenticated genuine-match witnesses."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path

from template_learning.analyze_removed_templates import read
from template_learning.evidence_serialization import write_json


LABELS = {
    'no_complete_match': 'At least one complete assignment lost',
    'both_broader_and_narrower': 'Both literal-to-slot and slot-to-literal changes',
    'slot_words_become_literals': 'Slots become literal wording',
    'literal_words_become_slots': 'Literal wording becomes slots',
    'slot_types_change': 'Slot types change',
    'location_change_without_diagnostic_word_retyping': 'Location changes; diagnostic word roles unchanged',
    'no_diagnostic_word_retyping': 'Same displayed pattern; location constraints changed',
    'unobserved': 'No selected witness; replacement unverified',
}


def differences(a, b, path=''):
    if type(a) != type(b):
        yield path, a, b
    elif isinstance(a, dict):
        for key in a.keys() | b.keys():
            if key not in a or key not in b:
                yield path+'/'+key, a.get(key), b.get(key)
            else:
                yield from differences(a[key], b[key], path+'/'+key)
    elif isinstance(a, list):
        if len(a) != len(b):
            yield path+'/length', len(a), len(b)
        else:
            for x, y in zip(a, b):
                yield from differences(x, y, path+'/*')
    elif a != b:
        yield path, a, b


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence', type=Path, required=True)
    args = cli.parse_args(); out = args.evidence
    data = read(out/'removed-template-analysis.json'); summary = data['summary']
    templates = data['templates']; witnesses = data['witnesses']
    by_old, by_new = defaultdict(list), defaultdict(list)
    for row in witnesses:
        by_old[row['before']].append(row)
        if row['after']:
            by_new[row['after']].append(row)
    removed = set(by_old) | set(summary['unobserved_removed'])
    category = {i: next((k for k in LABELS if any(r['theme'] == k for r in by_old[i])), 'unobserved')
                for i in removed}
    counts = Counter(category.values())
    # Verify why apparently identical templates have different IDs. Do not infer
    # equivalence from the display string alone.
    identical_pairs = {(r['before'], r['after']) for r in witnesses if r['same_display']}
    constraint_paths = Counter()
    metadata = {'template_id', 'support_occurrences', 'unique_messages', 'learning_support', 'selection_evidence'}
    for before, after in identical_pairs:
        diffs = list(differences(templates['production'][before], templates['candidate'][after]))
        constraints = []
        for path, a, b in diffs:
            if any(part in metadata for part in path.split('/')):
                continue
            assert path.endswith(('/constraints/numeric_text', '/constraints/line_reference')), path
            assert a is True and b is None, (path, a, b)
            constraints.append(path)
        assert constraints
        constraint_paths.update(set(constraints))
    assert all(any(r['same_display'] for r in by_old[i]) for i in removed
               if category[i] == 'no_diagnostic_word_retyping')

    old_sources = Counter(t['source_family'] for t in templates['production'].values())
    new_sources = Counter(t['source_family'] for t in templates['candidate'].values())
    source_rows = [dict(source=k, production=old_sources[k], candidate=new_sources[k],
                        net=new_sources[k]-old_sources[k]) for k in old_sources.keys() | new_sources.keys()]
    source_rows.sort(key=lambda r: (r['net'], r['source']))
    same_pairs = len(identical_pairs)
    analysis = dict(exclusive_categories=counts, category_by_removed_template=category,
                    source_inventory=source_rows, same_display_pairs=same_pairs,
                    verified_constraint_changes=constraint_paths,
                    coverage_note='Coverage is not semantic accuracy. Broader category slots require review; no false positive is established by this analysis.')
    write_json(out/'removed-template-summary.json', analysis)

    esc = lambda x: html.escape(str(x))
    pre = lambda x: '<pre>'+esc(x)+'</pre>'
    def visible(text):
        # Keep exact native bytes in JSON; show otherwise invisible game markup.
        return ''.join('\\x%02x' % ord(c) if ord(c)<32 and c not in '\r\n\t' else c for c in text)
    def pattern(side, identifier):
        t = templates[side][identifier]
        return '<p class="meta">'+esc(side)+' · '+esc(t['source_family'])+' · '+esc(t['status'])+' · <code>'+identifier+'</code></p>'+pre(visible(t['display']))
    def diff_table(row):
        changes = [d for d in row['changes'] if d['words']]
        if not changes:
            return '<p>No word-bearing capture-role change on this witness. Location repetition, marker constraints, punctuation and template support may still differ.</p>'
        return '<table><tr><th>Exact text segment</th><th>Production → candidate</th><th>Region / role</th></tr>'+''.join(
            '<tr><td><code>'+esc(visible(d['text']))+'</code></td><td>'+esc(d['before']+' → '+d['after'])+'</td><td>'+esc(d['region']+(' / location or trace' if d['location'] else ' / diagnostic'))+'</td></tr>'
            for d in changes)+'</table>'
    def witness(row):
        return ('<p>'+esc('73 training logs' if row['scope']=='training' else '20 stored Runs')+': '+
            f'{row["messages"]:,} contextual messages / {row["occurrences"]:,} occurrences on this mapping. '+
            esc(row['before_status']+' → '+row['after_status'])+'. One witness shown.</p>'+diff_table(row)+
            '<details><summary>Genuine native witness and provenance</summary>'+pre(visible(row['native_regions']['body']))+
            pre(json.dumps(row['provenance'], ensure_ascii=True, indent=2))+'</details>')
    def samples_for(identifier, limit=2):
        rows = sorted(by_new[identifier], key=lambda r: (not bool(r['changes']), r['scope']!='training', -r['occurrences'], r['before']))
        picked = []; seen = set()
        for row in rows:
            if row['before'] not in seen:
                picked.append(row); seen.add(row['before'])
            if len(picked) == limit:
                break
        return picked

    bits = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Where the removed error templates went</title>', '''
<style>body{font:16px/1.55 system-ui;max-width:1160px;margin:32px auto;padding:0 22px;color:#203746}h1,h2,h3{line-height:1.25}a{color:#086093}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eff4f7;padding:14px;font-size:13px;max-height:420px;overflow:auto}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:9px;border-bottom:1px solid #cbd6df;vertical-align:top;overflow-wrap:anywhere}code{overflow-wrap:anywhere}.meta{font-size:13px;color:#526674}.note{background:#eaf3fa;padding:18px;border-left:4px solid #31748d}.review{background:#fff1d9;padding:18px;border-left:4px solid #ae751c}details{margin:15px 0}summary{cursor:pointer}article{border-top:2px solid #d4dfe6;margin-top:26px;padding-top:12px}.columns{display:grid;grid-template-columns:1fr 1fr;gap:20px;min-width:0}.columns>div{min-width:0}nav{display:flex;flex-wrap:wrap;gap:16px}@media(max-width:750px){.columns{grid-template-columns:1fr}table{font-size:13px}td,th{padding:6px}}</style>
''', '<h1>Where the removed error templates went</h1>',
        '<nav><a href="CHANGES.html">Main comparison: 15 added / 15 removed / new matches</a><a href="#drivers">Drivers</a><a href="#mergers">Largest consolidations</a><a href="#review">Wording to review</a><a href="#all">All 465 removed templates</a></nav>',
        '<h2>Executive assessment: mostly consolidation, with specific generalization risks</h2>',
        '<p class="review">The template inventory fell from <strong>689 to 496 (−193; −28.0%)</strong>. This is chiefly consolidation of script-system and travel patterns, not disappearance of 193 error families. However, higher matching coverage alone does not establish better classification: some replacements turn meaningful category words into slots, while a few narrow character/name handling and lose support or coverage. The overall recommendation remains <strong>mixed; review before promotion</strong>.</p>',
        '<p>“Templates” here includes provisional templates, which remain valid complete assignments. “Removed” means an old template ID is absent: 465 old IDs were replaced or removed, 272 IDs were added, and 224 persisted. An observed successor is the template actually selected for the same message; it does not imply learner ancestry.</p>',
        '<p><strong>442 of 465 removed templates</strong> have selected witnesses across the two evidence scopes. They map to <strong>218 candidate templates</strong>; 430 have one successful successor, and 12 have multiple successors. One of these also has a lost match. There are 38 many-to-one destinations involving 289 removed templates. The other 23 have no selected witness, so a successor is not established.</p>',
        '<p class="note"><strong>Scope.</strong> Complete coverage mappings cover all 91,925 contextual messages in the same 73 training logs, plus the earlier 20 stored Runs. For slot/literal analysis, both pinned public matchers replayed <strong>659 genuine witnesses covering every one of 475 observed mapping pairs</strong>, including a no-match destination. This is one witness per mapping per scope, not every message. All captured byte spans were checked against the exact native text. Counts from overlapping scopes are kept separate. Production and candidate packages were not modified.</p>',
        '<h2 id="drivers">What changed in the slot/literal mix?</h2>',
        '<table><tr><th>Primary observed change</th><th>Removed templates</th><th>Interpretation</th></tr>']
    explanations = {
        'no_diagnostic_word_retyping': 'Identical display patterns. Executable comparison confirms only removal of numeric_text / line_reference constraints, apart from IDs and support/selection metadata. This follows the owner’s location-marker correction; it is ID churn, not a lost error family.',
        'location_change_without_diagnostic_word_retyping': 'No diagnostic word switches between literal and slot in the selected witnesses. Repeated location tails and contextual Unknown account for location changes. This is the strongest consolidation evidence.',
        'literal_words_become_slots': 'Includes 35 travel predecessors moving to date/character/place slots. The other 130 include script keys, effect/trigger names, and category words that deserve separate review.',
        'slot_words_become_literals': 'Includes specialization of untyped effect/trigger wording and literal character/localization survivors. Narrowing is not automatically a loss, but the latter has observed support regressions.',
        'both_broader_and_narrower': 'A marked-up character family both generalizes target/root and specializes part of a name. Different successors have different behavior.',
        'slot_types_change': 'Two predecessors move KEY fields into bounded PARAMs: a title display name and a formatting tag.',
        'no_complete_match': 'One old marked-up had_sex_with_effect template has a lost stored occurrence, although other messages still have successors.',
        'unobserved': 'No selected production assignment in either scope. May be shadowed or unrepresented; do not count these as proven harmless removals.',
    }
    order = ['no_diagnostic_word_retyping','location_change_without_diagnostic_word_retyping','literal_words_become_slots',
             'slot_words_become_literals','both_broader_and_narrower','slot_types_change','no_complete_match','unobserved']
    for key in order:
        bits.append('<tr><td>'+LABELS[key]+'</td><td>'+str(counts[key])+'</td><td>'+esc(explanations[key])+'</td></tr>')
    bits.append('</table><p>These categories sum to 465. When a template has several successors, precedence is lost match, both directions, narrowing, broadening, type change, location change, unchanged word roles. Thus counts describe primary observed changes, not disjoint underlying mechanisms. “Diagnostic word” here means any word-bearing text outside LOCATOR/repeated-trace captures; it includes names and IDs. Word counting is an analysis aid, not the learner’s similarity score.</p>')
    bits.append('<h3>Where the net reduction occurs</h3><table><tr><th>Emitter</th><th>Production templates</th><th>Candidate templates</th><th>Net</th></tr>')
    for row in source_rows[:5]:
        bits.append('<tr><td>'+esc(row['source'])+'</td><td>'+str(row['production'])+'</td><td>'+str(row['candidate'])+'</td><td>'+str(row['net'])+'</td></tr>')
    bits.append('</table><p>Script-system templates account for −170; effect-implementation templates for −31. All other emitters together offset these with +8 net templates. The gross 465 removed count includes the 135 unchanged-pattern replacements above, which do not by themselves reduce the inventory.</p>')
    ranked = sorted((i for i in data['incoming'] if len(data['incoming'][i])>1),
                    key=lambda i: (-len(data['incoming'][i]), i))
    review_notes = {
        '796ad48a3e5e8f97332f4427': 'after death / from before becomes two independent KEYs. Review whether these wording pairs should remain constrained.',
        '6a524415fb61b4b721f826be': 'left / right becomes a generic KEY, alongside the compared script key. Review the intended category boundary.',
        '814029db8af7b4c002042955': 'The tooltip variant also generalizes the comparison side to KEY. Review alongside the ordinary variant.',
        'f7a161abe24ee04e2cd78b76': 'Flag / Variable becomes a category KEY. Decide whether one template should cover both categories.',
        'afac2b20cf8aab9ca59f9a09': 'effect / trigger becomes a category KEY. The unknown script name is a separate, ordinary KEY change.',
        '766cfec88e63687b63c5123d': 'colored / textured becomes a category KEY. Review the intended error-family granularity.',
        '4615f2f0dcb62b0f22c0be03': 'The entire parenthesized left-was/right-was clause becomes PARAM. Its internal explanatory wording is no longer required.',
    }
    upgrade_notes = {
        '0e4e3302cde2fc5e07a2227f': 'Date, character identities and place names become the requested reusable fields; the travel diagnostic wording stays fixed.',
        '0213bb363ad56f39d7e953a5': 'Event-target, expected-scope and actual-scope values become KEYs; the mismatch diagnostic wording stays fixed.',
        '240299ab8871f53c5e7d04c4': 'Title display names become a quote-bounded PARAM, while the no-previous-holders diagnostic remains literal.',
        'b9164abd4185f3558666bf47': 'The formatting-tag value becomes a quote-bounded PARAM. The unknown-formatting-tag diagnostic remains literal.',
        'aa5006572b738abb4dd55d58': 'Character references inside game markup become KEYs; the already-has-trait diagnostic remains fixed. This is still a character-specific template, not generic name recognition.',
        '470604baffe5d399524e4738': 'root / target becomes a KEY in the same had_sex_with_effect diagnostic. These predecessor messages remain classified; other forms in this family have separate regressions.',
        '4ac751de53c2454d5094602a': 'Location variants consolidate while untyped stays literal. Messages using named triggers select other templates; this is specialization within a preserved family.',
        'd64316cae0703a7c2e54bd57': 'Location variants consolidate while untyped stays literal. Named-effect messages select other templates.',
    }
    consolidations = []
    for identifier in ranked:
        predecessors = data['incoming'][identifier]
        rows = by_new[identifier]
        negative = [r for old in predecessors for r in by_old[old] if r['after'] is None or
                    (r['before_status']=='template' and r['after_status']=='provisional')]
        if negative:
            verdict = 'Mixed predecessor outcomes'
            note = 'This successor handles some messages, but a predecessor also sends other genuine messages to provisional templates. The narrowing of marked-up names must be reviewed with the consolidation.'
        elif identifier in review_notes:
            verdict = 'Needs wording review'; note = review_notes[identifier]
        else:
            verdict = 'Looks like an upgrade'
            changed_words = any(d['words'] and not d['location'] for r in rows for d in r['changes'])
            note = upgrade_notes.get(identifier, 'Script identifiers become reusable KEY slots and/or location tails consolidate; the surrounding error wording stays fixed.' if changed_words else
                'Location variants consolidate without diagnostic words changing between literals and slots in the checked witnesses.')
        consolidations.append(dict(candidate=identifier, predecessors=predecessors, verdict=verdict, note=note,
            other_predecessor_regressions=[{k:r[k] for k in ('scope','before','after','before_status','after_status','messages','occurrences')} for r in negative]))
    verdict_counts = Counter(r['verdict'] for r in consolidations)
    write_json(out/'consolidation-review.json', dict(scope=data['method'], verdict_counts=verdict_counts,
        assessment='Review judgments about observed replacements, not semantic accuracy measurements or release approval.',
        groups=consolidations))
    merger_bits = ['<h2 id="mergers">Review each new template against the old templates it replaces</h2>',
        '<p class="note"><strong>'+str(len(consolidations))+' many-to-one consolidations.</strong> '+
        str(verdict_counts['Looks like an upgrade'])+' look like upgrades; '+
        str(verdict_counts['Needs wording review'])+' need wording review; '+
        str(verdict_counts['Mixed predecessor outcomes'])+' has mixed predecessor outcomes'+
        '. These are review judgments from the genuine mappings and capture changes, not an accuracy score. Open a row to see the candidate and <strong>every</strong> removed predecessor.</p>',
        '<p>This view covers consolidations involving 289 removed templates. It does not replace the separate checks of one-to-one replacements, unobserved templates or lost matches. A predecessor may have additional successors; links below show its complete mappings. Scope counts are never added together.</p>',
        '<table><tr><th>Old → new</th><th>Assessment</th><th>Candidate pattern and explanation</th></tr>']
    for item in consolidations:
        identifier = item['candidate']
        merger_bits.append('<tr><td style="white-space:nowrap">'+str(len(item['predecessors']))+' → 1</td><td>'+esc(item['verdict'])+'</td><td><a href="#target-'+identifier+'">'+esc(templates['candidate'][identifier]['display'])+'</a><br>'+esc(item['note'])+'</td></tr>')
    merger_bits.append('</table>')
    for item in consolidations:
        identifier = item['candidate']
        merger_bits.append('<details class="consolidation" id="target-'+identifier+'"><summary>'+str(len(item['predecessors']))+' old templates → one candidate · '+esc(item['verdict'])+' · '+esc(templates['candidate'][identifier]['display'].split('Script location:')[0].strip())+'</summary><h3>Candidate template</h3>'+pattern('candidate',identifier)+'<p><strong>Assessment.</strong> '+esc(item['note'])+'</p><h3>All old templates mapping here</h3>')
        for predecessor in item['predecessors']:
            rows = [r for r in by_new[identifier] if r['before']==predecessor]
            merger_bits.append('<details class="predecessor" data-old="'+predecessor+'"><summary>'+esc(templates['production'][predecessor]['display'].split('Script location:')[0].strip())+' · '+predecessor+'</summary>'+pattern('production',predecessor))
            for row in rows:
                merger_bits.append(witness(row))
            merger_bits.append('<p><a href="REMOVED-TEMPLATES.html#old-'+predecessor+'">Every successor and outcome for this old template</a></p></details>')
        if item['other_predecessor_regressions']:
            merger_bits.append('<p><strong>Other messages from these predecessors have regressions:</strong></p>'+pre(json.dumps(item['other_predecessor_regressions'],indent=2)))
        merger_bits.append('</details>')
    merger_bits.append('<p><a href="consolidation-review.json">Group assessments and predecessor IDs</a> · <a href="REMOVED-TEMPLATES.html">Full thematic review and all removed templates</a> · <a href="CHANGES.html">Production comparison</a></p>')
    bits.extend(merger_bits)
    # Reuse the same review content in a focused entry point rather than forcing
    # readers through the inventory analysis to inspect a consolidation.
    focused = bits[:2]+['<h1>Old templates → new template</h1>']+merger_bits+['</html>']
    (out/'CONSOLIDATIONS.html').write_text('\n'.join(focused),encoding='utf-8',newline='')

    reviews = [
        ('796ad48a3e5e8f97332f4427', 'History timing becomes two unconstrained KEY slots',
         'The genuine formulations “after death” and “from before” now occupy two KEYs. The shared surrounding diagnostic remains fixed, and values are retained, but the template no longer encodes which wording pairs belong together. Decide whether these should remain distinct formulations or use constrained alternatives. Coverage cannot answer that taxonomy question.'),
        ('6a524415fb61b4b721f826be', 'Comparison side becomes a KEY',
         'left/right are categorical diagnostic content. Grouping them may be appropriate, but generic KEY admits more than those two words. 23 predecessors map here; 20 show literal-to-slot broadening in the checked witnesses. The tooltip variant has another such predecessor. The differing compared keys are an additional, ordinary slot change.'),
        ('f7a161abe24ee04e2cd78b76', 'Flag and Variable become a shared category slot',
         'These two labels now share one template. The setting/unused-trigger diagnostic remains fixed, and the category is retained as data. Review whether the two categories should be one template with a constrained category field.'),
        ('afac2b20cf8aab9ca59f9a09', 'Unknown effect and Unknown trigger share a template',
         'The category word effect/trigger becomes KEY as well as the unknown script key. This is a classification-granularity choice, not evidence of lost native data or an observed false positive.'),
        ('766cfec88e63687b63c5123d', 'Colored and textured emblems share a template',
         'colored/textured now occupy a category KEY. Review alongside the category slots above rather than interpreting the lower count as automatically better.'),
        ('4615f2f0dcb62b0f22c0be03', 'A whole explanatory clause becomes PARAM',
         'The parenthesized “left was …, right was …” text is now opaque PARAM. It stays bounded by the parentheses and the main different-types diagnostic stays literal. However, internal explanatory wording no longer constrains this template. Five predecessors map here; four show literal-to-PARAM changes.'),
        ('0213bb363ad56f39d7e953a5', 'Expected and actual scope types become KEYs',
         'This is the requested correction: house_head/story_owner and the expected/actual scope values become three KEY slots, while “did not get a matching scope type. Expected …, but got …” stays literal. The three observed predecessors now share the reusable template.'),
        ('0e4e3302cde2fc5e07a2227f', 'Travel names and dates no longer create separate templates',
         '35 selected old templates map to one reusable pattern. The date is format-constrained; the short and super-short character fields are distinct types; default location is a line-bounded PARAM. Diagnostic wording remains fixed. Seven additional travel templates have no selected witness and are not included in that 35.'),
    ]
    bits.append('<h2 id="review">Specific wording changes to review</h2><p>No new false-positive claim is made here. The first six examples expose generalization choices that the coverage percentage cannot validate; the last two illustrate requested improvements. Exact values remain stored as slots.</p>')
    for identifier, title, note in reviews:
        assert identifier in by_new
        bits.append('<article><h3>'+esc(title)+'</h3><p>'+esc(note)+'</p>'+pattern('candidate',identifier))
        for row in samples_for(identifier, 2):
            bits.append('<details><summary>Before/after slots on a genuine message</summary>'+pattern('production',row['before'])+witness(row)+'</details>')
        bits.append('</article>')
    bits.append('<h2>Observed regressions and recommended next steps</h2><p>The existing evaluation still has one lost complete occurrence in the stored Runs, plus 115 template-to-provisional occurrences in the training logs (30 forms). Provisionals remain complete classifications. Marked-up character/name fields becoming literals explains the narrowing concern; this is distinct from the category-slot broadening above.</p><ol><li>Keep the proven location/date/character improvements in the disposable candidate.</li><li>Review the categorical KEY and explanatory PARAM examples above. Choose the intended template granularity before adding constraints or splitting templates; this analysis does not authorize a new grammar.</li><li>Resolve the marked-up character and apostrophe-localization regressions, and investigate the 23 templates without selected witnesses.</li><li>If attribution remains important, compare an ordered incremental build with the fresh build. Both saw the same 73 input hashes; the present results do not isolate build history from changed learner rules.</li></ol><p>Do not promote on matching percentage alone. No retraining, rule change, package activation, database write or runtime restart was performed for this analysis.</p>')
    bits.append('<h2 id="all">Every removed template and its observed successors</h2><p>Use browser Find for any template ID or wording. Each entry includes every successor edge in both scopes; counts are kept separate. The genuine witness and exact literal/slot transfers are expandable.</p>')
    for identifier in sorted(removed, key=lambda i: (list(LABELS).index(category[i]), templates['production'][i]['source_family'], i)):
        rows = by_old[identifier]
        bits.append('<details class="old-template" id="old-'+identifier+'"><summary>'+esc(LABELS[category[identifier]])+' · '+esc(templates['production'][identifier]['source_family'])+' · '+identifier+'</summary>'+pattern('production',identifier))
        if not rows:
            bits.append('<p>No selected witness in either evidence scope. A replacement is not established.</p>')
        for row in sorted(rows, key=lambda r: (r['scope'], r['after'] or '')):
            bits.append('<details class="mapping"><summary>'+esc(row['scope'])+' → '+esc(row['after'] or 'no_match')+' · '+f'{row["occurrences"]:,}'+' occurrences</summary>')
            if row['after']:
                bits.append(pattern('candidate',row['after']))
            bits.append(witness(row)+'</details>')
        bits.append('</details>')
    bits.append('<h2>Evidence and verification</h2><p>'+esc(data['method'])+'</p><p>For identical-display pairs, recursive executable comparison checked that only numeric_text/line_reference location constraints were removed, excluding IDs and support/selection metadata. For changed captures, byte spans and exact values were checked in every region, including wrappers and continuations. The transfer tables suppress whitespace-only/punctuation-only segments; the complete JSON retains them. Game control characters are printed as \\xNN for readability; raw evidence remains unchanged.</p><p><a href="removed-template-analysis.json">Complete crosswalk, patterns, witnesses and byte-span transfers</a> · <a href="removed-template-summary.json">Derived counts and constraint checks</a> · <a href="regression-investigation.json">Existing regression root causes</a> · <a href="CHANGES.html">Main comparison</a></p></html>')
    if (out/'removed-report-verification.json').exists():
        bits.insert(-1, '<p><a href="removed-report-verification.json">Verification results and corrected check assumptions</a> · <a href="removed-report-desktop.png">Visually inspected desktop rendering</a></p>')
    (out/'REMOVED-TEMPLATES.html').write_text('\n'.join(bits), encoding='utf-8', newline='')
    print(json.dumps(analysis, indent=2))


if __name__ == '__main__':
    main()
