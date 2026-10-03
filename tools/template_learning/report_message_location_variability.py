"""Render the measurement ledger; no parsing, matching or inferred classifications."""
import argparse
import html
import json
from pathlib import Path


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--review', type=Path, required=True)
    args = cli.parse_args()
    root = args.review
    data = json.loads((root / 'incidence.json').read_text())
    esc = lambda text: html.escape(str(text))
    fmt = lambda value: f'{value:,}'
    histogram = lambda counts: ', '.join(f'{n}: {fmt(counts[n])}' for n in sorted(counts, key=int))
    variable = [f for f in data['families'] if f['variable_count']]
    bits = ['''<!doctype html><meta charset="utf-8"><title>Location-count variability within the same diagnostic pattern</title>
<style>body{font:16px/1.55 system-ui;max-width:1200px;margin:40px auto;padding:0 24px;color:#192939}h1,h2{line-height:1.2}table{border-collapse:collapse;width:100%;margin:18px 0}td,th{border-bottom:1px solid #d3dde5;padding:10px;text-align:left;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f7;padding:16px;font-size:13px}code{overflow-wrap:anywhere}summary{cursor:pointer;font-weight:600}details{margin:14px 0}input{font:inherit;padding:8px;width:80%}.muted{color:#536679}</style>
<h1>Location-count variability within the same diagnostic pattern</h1>
<p>3 October 2026. Historical investigation. Recovered error messages are the unit of analysis; original emission provenance remains attached. The measurements below preceded the authorized disposable implementation. Production selection and existing Runs remain unchanged.</p>''']
    candidate_report = root.parent / 'locator-marker-candidate' / 'verification.json'
    if candidate_report.exists():
        candidate = json.loads(candidate_report.read_text())
        bits.append('<p><strong>Subsequent disposable test:</strong> both locator changes were implemented and tested against '
                    +fmt(candidate['totals']['stored_records'])+' stored records from '+str(len(candidate['runs']))+' genuine Runs. '
                    '<a href="../locator-marker-candidate/CHANGES.html">Read the human-readable template changes and newly matched examples</a>; '
                    '<a href="../locator-marker-candidate/RESULTS.html">full verification</a>. '
                    'Earlier pending-implementation statements below describe the investigation checkpoint.</p>')
    bits.append('<p><strong>Classification similarity and exact message identity are separate.</strong> '
                'Locator contents and count do not affect classification similarity. Both do count toward exact error-message identity: '
                'otherwise identical messages with different locator values or counts are distinct messages, even when they share a template. '
                'Preserve the full ordered values for storage, deduplication and occurrence counting; never use the locator-neutral comparison view as message identity.</p>')
    marker_path = root / 'location-markers.json'
    if marker_path.exists():
        marker_inventory = json.loads(marker_path.read_text(encoding='utf-8'))
        bits.append('<h2>Owner clarification: Unknown is a location value</h2>'
                    '<p><strong>Required behavior:</strong> keep <code>Script location:</code> literal and capture an explicitly emitted '
                    '<code>Unknown</code> as one present LOCATOR value. Preserve the exact text in storage. It is not an absent section, '
                    'SQL null, or invented file/line/trace subvalues. Unknown normally remains literal; only its immediate position after a recognized location marker '
                    '(also including <code>line:</code> and <code>near line:</code>) permits this LOCATOR interpretation. '
                    'This supersedes the older literal-Unknown rule; implementation remains pending.</p>'
                    '<p>The earlier count study below measures concrete file/line entries. Excluding Unknown from that particular count '
                    'does not mean Unknown should be excluded from location slots.</p>')
        bits.append('<table><tr><th>Marker</th><th>Explicit unavailable-value text</th><th>Occurrences</th></tr>')
        for item in marker_inventory['unavailable_candidates']:
            bits.append('<tr><td>'+esc(item['marker'])+'</td><td>'+esc(item['native_value_tail'])+'</td><td>'+fmt(item['count'])+'</td></tr>')
        bits.append('</table><p>The inventory examines '+str(marker_inventory['log_count'])+' logs. Counts are raw marker mentions, '
                    'not new message classifications. The probe checked Unknown, none, null, n/a and related quoted/bracketed spellings; '
                    'only the forms listed above were found after the inventoried markers. Empty filenames remain a separate observed case.</p>')
        bits.append('<details><summary>Inventoried marker spellings and native examples</summary><table><tr><th>Marker</th><th>Mentions</th><th>Value shapes</th></tr>')
        for label, item in marker_inventory['markers'].items():
            bits.append('<tr><td>'+esc(label)+'</td><td>'+fmt(item['count'])+'</td><td>'+esc(', '.join(k+': '+fmt(v) for k,v in item['shapes'].items()))+'</td></tr>')
        bits.append('</table></details><p><a href="location-markers.json">Full marker inventory and original byte locations</a> · '
                    '<a href="unknown-current-behavior.json">Recorded-package example: Unknown currently remains literal, with no LOCATOR capture</a>.</p>')
    continuation_path = root / 'continuation-overlap.json'
    if continuation_path.exists():
        audit = json.loads(continuation_path.read_text(encoding='utf-8'))
        bits.append('<h2>Double-check: existing continuation and recovery rules</h2>'
                    '<p>The current parser bytes and learner continuation declaration equal those in the recorded IS3QON package. '
                    'The audit used that verified parser on all '+str(len(audit['logs']))+' complete logs, preserving emission adjacency. '
                    'Every original emission was consumed exactly once. Counts below are recovery units and recovered messages, not template counts.</p>'
                    '<p><strong>Only one rule joins separate timestamped emissions:</strong> <code>history-colon-title-list-v1</code>. '
                    'It requires single-line E-level emissions from <code>history.cpp</code>: an opening ending in a colon, followed immediately by one or more '
                    '<code>&lt;reference&gt;\'s title: &lt;value&gt;</code> entries. The first reference must prefix the opening with a space boundary; '
                    'subsequent references must agree exactly. A new opening or incompatible emission stops the group. The learner validates the full character '
                    'reference against the opening capture and stores each whole title as PARAM; it does not treat title entries as LOCATORs.</p>'
                    '<p><strong>There is overlap with within-emission recovery:</strong> script-error, Stack trace, From, participant, and reader-wrapper structures '
                    'already contain location markers. Script errors, stack traces, From and participant forms remain one message. The participant example has file/line '
                    'on its opening line and Cheater:/With: on following lines. Reader wrappers split at their complete located '
                    'inner lines and retain shared wrapper context. Location-count neutrality must apply inside these already recovered messages and must '
                    'not merge wrapper siblings, reinterpret title entries, or consume another timestamped emission.</p>')
        meanings = {
            'history-colon-title-list-v1': 'Cross-header join; ordered supporting title entries.',
            'located-message-wrapper': 'Quoted Error wrapper: each inner line has one near line location; optional expanded-from annotation; shared file/near-line suffix. Current code checks numeric contents; owner requires marker-based LOCATOR recognition.',
            'script-error': 'Script system error opener, Error field, one Script location section with Unknown or file/line, then zero or more file/line entries. One message.',
            'single-line': 'One nonblank body line. One message.',
            'message-with-stack-trace': 'Diagnostic line, Stack trace:, then one or more file/line entries. One message.',
            'message-with-from-location': 'Diagnostic line and one From: quoted file/line entry. One message.',
            'message-with-scope-context': 'Opening ends for scope:, then Root: and Saved event targets:. One message.',
            'message-with-participants': 'jomini_effect_impl.cpp opening, then Cheater: and With:. One message.',
            'message-with-formatted-reason': 'faction.cpp or character_commands.cpp opening, then one formatting-control-prefixed line. One message.',
            'message-with-quoted-multiline-value': 'pdx_data_localize.cpp Data error in loc string or pdx_text_formatter.cpp Unknown formatting tag; native quoted multiline value. One message.',
            'unresolved': 'Existing rules did not establish a complete message structure.'}
        bits.append('<table><tr><th>Existing structure</th><th>Rule / effect</th><th>Recovery units</th><th>Recovered messages</th><th>Units mentioning location markers</th></tr>')
        for name, description in meanings.items():
            row = audit['structures'].get(name, {})
            bits.append('<tr><td>'+esc(name)+'</td><td>'+esc(description)+'</td><td>'+fmt(row.get('units', 0))+'</td><td>'+
                        fmt(row.get('messages', 0))+'</td><td>'+fmt(row.get('marker_units', 0))+'</td></tr>')
        bits.append('</table>')
        grouped = audit['structures'].get('history-colon-title-list-v1', {})
        bits.append('<p>Cross-emission title groups: '+fmt(grouped.get('units', 0))+' groups; '+fmt(grouped.get('attached_entries', 0))+
                    ' attached entries; '+fmt(grouped.get('marker_units', 0))+' groups containing an inventoried location marker. '
                    'Marker mentions are inventory findings, not LOCATOR assignments.</p>'
                    '<p>The local script-error envelope already accepts Unknown after Script location. Its old matcher typing is the defect under review. '
                    'The current reader-wrapper code checks numeric near-line values. That describes the implementation, not a required condition for LOCATOR recognition. '
                    '<strong>Owner clarification:</strong> the line:/near line: marker establishes the location field; whether its contents are numeric is not relevant to that recognition. '
                    'All 255,228 near-line mentions in the corpus had numeric values; there was no nonnumeric counterexample. '
                    'Correct marker/value handling while preserving the established message boundaries. Exact locator contents still determine message identity.</p>')
        for key, example in audit['examples'].items():
            bits.append('<details><summary>Genuine recovery example: '+esc(key)+'</summary><p>Log '+esc(example['log_sha256'])+'</p>')
            for emission in example['original_emissions']:
                bits.append('<p>Original emission '+str(emission['ordinal'])+'</p><pre>'+esc(emission['text'])+'</pre>')
            bits.append('<p>'+str(len(example['messages']))+' recovered message(s).</p></details>')
        bits.append('<p><a href="continuation-overlap.json">Complete continuation audit, native witnesses, marker intersections and source hashes</a>. '
                    'No recovery rules or executable learner/matcher behavior were changed.</p>')
    totals = data['totals']
    covered = sum(data['variable_family_message_counts'].values())
    many = sum(v for n, v in data['variable_family_message_counts'].items() if int(n) > 1)
    bits.append(f'<p><strong>{fmt(len(variable))} diagnostic wording/slot patterns show more than one trailing-location count.</strong> '
                f'Together they cover {fmt(covered)} distinct message occurrences counted once, including {fmt(many)} with multiple entries.</p>')
    target = next((f for f in variable if "did not get a matching scope type. Expected '<KEY>'" in f['pattern']['display']), None)
    if target:
        bits.append('<h2>The original scope-mismatch case</h2><pre>'+esc(target['pattern']['display'])+'</pre>')
        bits.append('<table><tr><th>Location entries</th><th>Message occurrences</th><th>Genuine example values</th></tr>')
        for count in sorted(target['counts'], key=int):
            wording = target['examples'][count]['text'].split('Error: ', 1)[1].split('\n', 1)[0]
            bits.append('<tr><td>'+count+'</td><td>'+fmt(target['counts'][count])+'</td><td>'+
                        esc(' / '.join(wording.split("'")[1::2]))+'</td></tr>')
        bits.append('</table><p>'+fmt(sum(target['counts'].values()))+' messages across '+str(len(target['logs']))+
                    ' logs. Model origins and contributing template IDs are listed in the detailed group below. '
                    'Matching this opening for measurement does not repair an original complete assignment.</p>')
    bits.append('<h2>Representative shared patterns</h2><table><tr><th>Pattern</th><th>Observed entry counts</th><th>Occurrences</th></tr>')
    for needle in ["Event target link '<KEY>' returned", 'Error: <KEY> trigger [ <REASON> ]',
                   'Error: <KEY> effect [ <REASON> ]', "Character with no location in link 'location'"]:
        family = next((f for f in variable if needle in f['pattern']['display'] and 'tooltip' not in f['pattern']['display']), None)
        if family is None:
            continue
        counts = list(map(int, family['counts']))
        label = family['pattern']['display'].split('Error: ', 1)[1].split('\n  Script location:', 1)[0]
        bits.append(f'<tr><td>{esc(label)}</td><td>{len(counts)} distinct counts; {min(counts)}–{max(counts)} entries</td>'
                    f'<td>{fmt(sum(family["counts"].values()))}</td></tr>')
    bits.append('</table>')
    recovery_path = root / 'recovery-examples.json'
    if recovery_path.exists():
        recovery = json.loads(recovery_path.read_text(encoding='utf-8'))
        bits.append('<h2>Message-level counts and existing recovery boundaries</h2>'
                    '<p>Fixed locator counts after an existing split cannot establish the absence of variability in the original emission. '
                    'The census above describes recovered messages only. Its scope-mismatch witnesses were checked against the pinned parser: '
                    'one, two and three location entries each remain inside one recovered script-error message, with respectively two, four and six body LOCATOR fields.</p>'
                    '<p>Existing recovery has different behaviors. The native wrapper example below contains two complete Unexpected token lines and becomes two messages with shared file context. '
                    'The history continuation example attaches two title entries to one opening error. The war example retains its two location entries within one error. '
                    'These examples support manual comparison; no new split or equivalence follows automatically from their shapes.</p>')
        for example in recovery['examples']:
            bits.append('<details><summary>'+esc(example['label'])+'</summary><p>Recovery: <code>'+esc(example['structure'])+
                        '</code>; '+str(len(example['original_emissions']))+' original emission(s) → '+
                        str(len(example['recovered_messages']))+' recovered message(s).</p>')
            for emission in example['original_emissions']:
                bits.append('<p>Original emission '+str(emission['ordinal'])+'</p><pre>'+esc(emission['text'])+'</pre>')
            for message in example['recovered_messages']:
                bits.append('<p>Recovered body; '+str(len(message['recognized_body_locators']))+' recognized body location fields; '+
                            str(len(message['continuations']))+' attached continuation entries. Shared wrapper fields are additional.</p><pre>'+esc(message['text'])+'</pre>')
            bits.append('</details>')
        bits.append('<p><a href="recovery-examples.json">Exact recovery examples and original spans</a>.</p>')
    bits.append('<h2>Scope and meaning of “same template”</h2>')
    bits.append(f'<p>{len(data["logs"])} distinct retained complete logs; {fmt(sum(l["emissions"] for l in data["logs"]))} original emissions; '
                f'{fmt(totals["messages"])} recovered error messages; {fmt(data["unique_contextual_messages"])} distinct contextual messages examined. '
                f'{fmt(totals.get("unresolved_recovery_units", 0))} unresolved recovery units.</p>')
    bits.append('<p>The current flat templates already bake in location-list length. Grouping by their IDs would hide the very variation being investigated. '
                'This review instead projects each existing template to its diagnostic prefix before a complete trailing location list. '
                'Its literal words, punctuation, slot types and constraints remain unchanged. The pinned shared matcher checks the native prefix against those parts. '
                'Slot values may differ; merely similar sentences are not combined. These groups are measurement views, not newly accepted complete templates.</p>')
    bits.append('<p>Reference models: '+', '.join('<code>'+esc(v)+'</code>' for v in data['models'])+'. '
                'The first is the package recorded for IS3QON; the second is the isolated corrected 20-log candidate. Every group below identifies the contributing definitions.</p>')
    bits.append('<p>A <code>file: … line: … (…)</code> entry counts as one location entry, with separate file and line LOCATOR fields and an optional parenthetical trace. '
                'Only a contiguous trailing sequence of complete file/infile plus line/near-line entries enters the entry-count comparison. '
                'Other location layouts are listed separately rather than presumed equivalent. Messages with no recognized trailing list, including literal Unknown, are outside this positive-entry comparison.</p>')
    bits.append(f'<p>{fmt(totals["messages_with_trailing_location_entries"])} messages have such a trailing list; '
                f'{fmt(totals["messages_with_multiple_trailing_entries"])} have more than one entry. '
                f'{fmt(totals.get("trailing_messages_without_template_prefix_group", 0))} trailing-list messages have no unambiguous applicable prefix pattern and remain outside the family comparison. '
                'Family rows can overlap, so their counts must not be added. The overview above counts covered message occurrences once.</p>')
    bits.append('<h2>Where within-pattern variability occurs</h2><table><tr><th>Emitter</th><th>Covered message occurrences</th></tr>')
    for source, count in sorted(data['variable_family_sources'].items(), key=lambda kv:-kv[1]):
        bits.append(f'<tr><td>{esc(source)}</td><td>{fmt(count)}</td></tr>')
    bits.append('</table><p>Entry count → occurrences across the variable families, deduplicated across overlapping groups: '+esc(histogram(data['variable_family_message_counts']))+'.</p>')
    for family in data['families']:
        if ('Stack trace:' in family['pattern']['display'] and not family['variable_count']
                and any(int(n) > 1 for n in family['counts'])):
            bits.append('<p>Another multi-location form, without observed count variability: <code>'+esc(family['pattern']['source'])+
                        '</code>, '+esc(histogram(family['counts']))+' (entries → occurrences) across '+str(len(family['logs']))+
                        ' logs.</p><pre>'+esc(family['pattern']['display'])+'</pre>')
    bits.append('<h2>Every variable diagnostic pattern</h2><p><input id="filter" placeholder="Filter by wording or emitter"></p>')
    for number, family in enumerate(variable, 1):
        pattern = family['pattern']
        bits.append(f'<section class="family"><details><summary>{number}. {esc(pattern["source"])} — '
                    f'{esc(pattern["display"].strip())}</summary>')
        bits.append(f'<p>Entries → message occurrences: <strong>{esc(histogram(family["counts"]))}</strong>. '
                    f'{fmt(family["distinct_bodies"])} distinct contextual bodies in {len(family["logs"])} logs. '
                    f'{family["distinct_literal_prefixes"]} different native prefixes fit these same literal/slot parts.</p>')
        bits.append('<pre>'+esc(pattern['display'])+'</pre><details><summary>Contributing template definitions</summary><pre>'+esc(json.dumps(pattern['definitions'], indent=2))+'</pre></details>')
        # All counts retain an exact witness; no invented or shortened native message.
        for count, example in sorted(family['examples'].items(), key=lambda kv:int(kv[0])):
            bits.append(f'<details><summary>Genuine example: {count} location entries</summary><p>{esc(example["source_tag"])}; '
                        f'log {esc(example["log_sha256"])}; original emission ordinal(s) '
                        f'{esc(example["provenance"]["emission_ordinals"])}; recovered message ordinal '
                        f'{esc(example["provenance"].get("message_ordinal"))}.</p><pre>{esc(example["text"])}</pre></details>')
        bits.append('</details></section>')
    bits.append('<h2>Other multi-location forms and unresolved measurement cases</h2><p>These examples are inventory findings, not proof of within-template count variability. '
                'The broad recognizer field counts include locations anywhere in the message and attached context. The preliminary nonnumeric-field counter is not an independently validated file count.</p>')
    for label, key in [('Other layouts', 'other_multilocation_examples'), ('Trailing lists without a prefix group', 'unmatched_prefix_examples')]:
        bits.append(f'<details><summary>{label}: {len(data[key])} representative source/count combinations</summary>')
        for example in data[key]:
            bits.append('<p>'+esc(example['source_tag'])+'; original emission(s) '+esc(example['provenance']['emission_ordinals'])+'</p><pre>'+esc(example['text'])+'</pre>')
        bits.append('</details>')
    annotations_path = root / 'reader-annotations.json'
    if annotations_path.exists():
        annotations = json.loads(annotations_path.read_text())
        bits.append('<h2>Reader errors: a different kind of additional location</h2><p>'+esc(annotations['interpretation'])+'</p>')
        bits.append('<table><tr><th>Core template</th><th>Plain</th><th>With expanded-from file/line</th><th>Expanded-from with empty filename</th></tr>')
        for row in annotations['patterns']:
            if not any(k.startswith('expanded') for k in row['counts']):
                continue
            bits.append('<tr><td>'+esc(row['display'])+'</td><td>'+fmt(row['counts'].get('plain', 0))+'</td><td>'+
                        fmt(row['counts'].get('expanded', 0))+'</td><td>'+fmt(row['counts'].get('expanded_missing_filename', 0))+'</td></tr>')
        bits.append('</table><p>This is variation in attached location context around a common core error. The literal annotation makes these different complete current templates; '
                    'it is not evidence of the same freely repeating list found in Script system errors. Empty filenames are missing location information, not another list-length observation.</p>')
        bits.append('<p><a href="reader-annotations.json">Reader counts and complete native examples with wrapper context</a>.</p>')
    check_path = root / 'location-count-crosscheck.json'
    if check_path.exists():
        check = json.loads(check_path.read_text())
        bits.append('<h2>Count verification</h2><p>The counter agrees with the earlier detailed location-field inventory on '+
                    fmt(check['message_occurrences'])+' genuine message occurrences / '+fmt(check['location_entries'])+
                    ' individual entries, with '+str(len(check['mismatches']))+' count mismatches. '
                    'This checks entry counting; it does not validate a future splitting policy.</p>')
    bits.append('<h2>Interpretation and open decision</h2><p>The measurements establish where the same diagnostic wording/slot pattern appears with different numbers of trailing locations. '
                'They do not establish that each location represents an independent error. Whether to retain one message with a location list or recover multiple messages requires interpreting those location entries in their native context. '
                'The earlier repeated-entry representation proposal is paused; neither that design nor splitting has been implemented.</p>')
    bits.append('<p>Corpus scope: '+esc(data['scope'])+'. The retained inventory records '+str(len(data['inaccessible']))+' access errors. '
                'Live logs, review shards, synthetic logs and duplicate copies are excluded. These findings describe the readable retained corpus, not all possible CK3 emissions.</p>')
    bits.append('<p><a href="incidence.json">Full measurement ledger and exact examples</a></p><script>document.querySelector("#filter").addEventListener("input",e=>{let q=e.target.value.toLowerCase();document.querySelectorAll(".family").forEach(n=>n.hidden=!n.textContent.toLowerCase().includes(q))})</script>')
    (root / 'REVIEW.html').write_text('\n'.join(bits), encoding='utf-8')
    print(json.dumps(dict(variable_families=len(variable), covered_messages=covered,
        multiple_entry_messages=many, variable_sources=data['variable_family_sources'],
        report=str((root / 'REVIEW.html').resolve()))))


if __name__ == '__main__':
    main()
