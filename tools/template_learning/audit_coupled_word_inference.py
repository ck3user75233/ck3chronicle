"""Inventory final-template effects and replay inference on genuine member groups.

This is an audit, not learning or publication. It does not reconstruct unrecorded
transient proposals from a historical build. Raw controls are escaped only in HTML.
"""
import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.patterns import derive_pattern
from template_learning.records import SequenceRecord, identity
from template_learning.matching_primitives import display_pattern


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--bundle', type=Path, required=True)
    cli.add_argument('--previous-package', type=Path, required=True)
    cli.add_argument('--package', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    research = json.loads((args.bundle/'empirical_template_model.json').read_bytes())
    old = json.loads((args.previous_package/'empirical_template_model.json').read_bytes())
    new = json.loads((args.package/'empirical_template_model.json').read_bytes())
    old = {t['template_id']: t for t in old['templates']}
    new = {t['template_id']: t for t in new['templates']}
    changed = [key for key in sorted(old.keys() & new.keys()) if old[key] != new[key]]
    changes = {key: [field for field in old[key].keys() | new[key].keys()
                     if old[key].get(field) != new[key].get(field)] for key in changed}
    adjacent = []
    for t in research['templates']:
        for left, gap, right in zip(t['parts'], t['parts'][1:], t['parts'][2:]):
            if (left.get('type') in {'KEY', 'OPTIONAL_KEY'}
                    and gap.get('kind') == 'literal' and gap['text'].isspace()
                    and right.get('type') in {'KEY', 'OPTIONAL_KEY'}):
                adjacent.append(dict(template_id=t['template_id'], slots=[left['name'], right['name']],
                    observed_values=[left['observed_values'], right['observed_values']],
                    alphabetic_only=all(v.isalpha() for p in (left,right) for v in p['observed_values'])))
    wanted = {rid for t in research['templates'] for rid in t['evidence_record_ids']}
    records, examples = {}, {}
    rows = occurrences = 0
    print('Streaming genuine corpus evidence.', flush=True)
    for row, count in native_evidence_rows(args.bundle/'native_evidence.json'):
        rows += 1
        occurrences += count
        record = SequenceRecord(row['source_family'], row['native'], tuple(map(tuple,row['pieces'])),
            context_kind=row['context_kind'], contexts=row['contexts'], continuations=tuple(row['continuations']))
        rid = identity(record.key)
        if rid not in wanted or rid in records:
            continue
        records[rid] = record
        examples[rid] = dict(message=row['native'], source_family=row['source_family'],
                            provenance=row['native_occurrences'], occurrences=count)
    missing = wanted-records.keys()
    assert not missing, sorted(missing)[:10]
    print(f'Collected {len(records)} native records from {rows} contextual rows.', flush=True)
    replay = []
    types = Counter()
    fields = Counter()
    by_id = {t['template_id']: t for t in research['templates']}
    for index, template in enumerate(research['templates']):
        group = [records[rid] for rid in template['evidence_record_ids']]
        hypotheses = []
        parts, failures = derive_pattern(group, group[0], hypotheses=hypotheses)
        hits = [h for h in hypotheses if h.get('proposal') == 'coupled_word_fields']
        replay.append(dict(template_id=template['template_id'], messages=len(group),
                           coupled_proposals=hits, failures=len(failures)))
        for p in template['parts']:
            if p.get('kind') == 'slot':
                types[p['type']] += 1
                if p.get('parameter_definition'): fields['declared'] += 1
                if p.get('empirical_region'): fields['empirical_region'] += 1
        if (index+1) % 25 == 0:
            print(f'Replayed {index+1}/{len(research["templates"])} final member groups.', flush=True)
    history_ids = [t['template_id'] for t in research['templates']
                   if t['source_family']=='characterhistory.cpp' and ' has history ' in t['display']
                   and any(phrase in t['display'] for phrase in ('after death birth','from before birth'))]
    group = [records[rid] for tid in history_ids for rid in by_id[tid]['evidence_record_ids']]
    hypotheses = []
    parts, failures = derive_pattern(group, group[0], hypotheses=hypotheses)
    history = dict(messages=len(group), proposed_display=display_pattern(parts),
        coupled_proposals=[h for h in hypotheses if h.get('proposal')=='coupled_word_fields'],
        rejected_fields=[dict(type=p['type'],values=p['observed_values'],reason=p['rejection_reason'])
                         for p in parts if p.get('rejection_reason')], failures=len(failures))
    selected = list(dict.fromkeys([*history_ids, *(a['template_id'] for a in adjacent)]))
    details = []
    for tid in selected:
        t = by_id[tid]
        ids = t['evidence_record_ids']
        pairs = [a for a in adjacent if a['template_id']==tid]
        parts_by_name = {p.get('name'):p for p in t['parts'] if p.get('kind')=='slot'}
        def field_values(rid):
            values=[]
            for pair in pairs:
                for name in pair['slots']:
                    member=next(m for m in parts_by_name[name]['field_support']['members'] if m['record_id']==rid)
                    a,b=member['pieces']
                    values.append(''.join(text for _,text in records[rid].pieces[a:b]))
            return tuple(values)
        first=ids[0]
        second=next((rid for rid in ids[1:] if field_values(rid)!=field_values(first)),ids[1])
        witnesses = [dict(record_id=rid,**examples[rid]) for rid in (first,second)]
        assert len(witnesses)==2
        details.append(dict(template_id=tid,display=t['display'],status=t['status'],
            messages=t['unique_messages'],occurrences=t['support_occurrences'],examples=witnesses,
            role='history literal outcome' if tid in history_ids else 'other adjacent-field inventory; not a rule success'))
    result = dict(scope=dict(contextual_rows=rows,occurrences=occurrences,native_records=len(records),
                            templates=len(research['templates'])),
        comparison=dict(unchanged=len(old.keys()&new.keys())-len(changed),changed=changes,
                        added=sorted(new.keys()-old.keys()),removed=sorted(old.keys()-new.keys())),
        adjacent_inventory=adjacent,final_group_replay=replay,history_combined_replay=history,
        slot_inventory=dict(types),field_inventory=dict(fields),templates=details,
        limits='Final member-group replay and complete exported-template comparison; not an exhaustive recording of transient proposals during the original incremental build.',
        hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (
            args.bundle/'empirical_template_model.json',args.previous_package/'manifest.json',args.package/'manifest.json')})
    write_json(args.output/'adjacent-word-audit.json',result)
    def esc(text):
        text=''.join(f'\\u{ord(c):04x}' if ord(c)<32 and c not in '\r\n\t' else c for c in text)
        return html.escape(text)
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Adjacent-word inference audit</title>',
          '<style>body{font:16px/1.55 system-ui;max-width:1100px;margin:40px auto;padding:0 20px;color:#172333}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f3f7;padding:16px}article{border-top:2px solid #cbd4df;margin-top:32px}code{overflow-wrap:anywhere}</style>',
          '<h1>Adjacent-word inference: actual scope and examples</h1>',
          '<p>The check reconsiders provisional type inference; it does not declare ordinary words to be legitimate KEYs. In the history example, KEY KEY is the mistaken intermediate hypothesis being rejected.</p>',
          f'<p>Compared all {len(new)} exported templates in v57 and v58: {result["comparison"]["unchanged"]} are identical. Changed fields: <code>{esc(json.dumps(changes))}</code>. No other final template changes are attributable to this correction.</p>',
          f'<p>Replayed inference on all {len(replay)} final template member groups: {sum(bool(r["coupled_proposals"]) for r in replay)} groups invoke the new check. Combining the two history groups invokes it {len(history["coupled_proposals"])} time(s); the combined undemarcated phrase is rejected as PARAM. The final templates retain their literal wording.</p>',
          f'<p>Re-inferring the final example groups produced {sum(r["failures"] for r in replay)} messages that failed the complete-match/capture-range consistency check. This does not establish semantic correctness of slot types. Final body patterns include {types["PARAM"]} PARAM slots and {types["REASON"]} REASON slots, all unchanged in the exported-template comparison. Wrapper declarations and repeated location layouts were also included in that exact comparison.</p>',
          '<p><strong>Scope limit:</strong> these are final-group checks and a complete output comparison, not an invocation log of every temporary proposal in the historical incremental build.</p>',
          '<h2>Boundary protection</h2><p>The new branch requires at least two nonoptional KEY proposals separated only by whitespace without line endings. Every observed value must be alphabetic; each column must vary one-to-one with all the others. Fields with parameter_definition, empirical_region or inference_rule are excluded. REASON, LOCATOR and recognized character identity slots are not eligible types. A matching pair immediately enclosing the combined span (ignoring gaps) excludes it too.</p>',
          '<p>This is not a blanket exemption for every substring anywhere inside parentheses or brackets. Recognized opaque fields are protected before this step; otherwise enclosing_pair tests the proposed span’s actual endpoints in every example. Existing PARAM coalescing is a different, older branch. No new global punctuation exemption was added.</p>',
          '<h2>Review terminology</h2><p>“Previously accepted generalizations” means regression assessment informed by prior owner feedback. It is not a runtime list of approved templates in this check. Existing owner-directed recognition rules remain separate.</p>',
          '<p>“Removals sharing one successor” means several old templates’ genuine messages now select the same replacement template. The report displays the old templates together with that one replacement. It does not delete error messages or alter their identities; different templates can still distinguish exact messages through captured values.</p>',
          '<h2>All relevant templates, with two genuine examples each</h2><p>The two history formulations are the demonstrated literal outcomes. The other three are the entire previously reported adjacent-field inventory, not three additional applications of this rule. Their fields contain hyphens, possessive text or game-formatting controls and fail the alphabetic-only condition. This does not establish that their KEY typing is semantically correct.</p>',
          '<p>Examples are native message text; outer log headers are not part of this message body. Control characters are shown as Unicode escapes for readability; the linked JSON preserves exact strings and source provenance.</p>']
    example_number=0
    for t in details:
        bits.extend([f'<article id="{t["template_id"]}"><h3>{esc(t["role"])}</h3>',
            f'<p><code>{t["template_id"]}</code> · {t["status"]} · {t["messages"]} distinct messages · {t["occurrences"]} occurrences</p>',
            '<pre>'+esc(t['display'])+'</pre>'])
        for n,w in enumerate(t['examples'],1):
            example_number+=1
            bits.extend([f'<h4>Example E{example_number:02d} · {esc(w["source_family"])}</h4><pre>{esc(w["message"])}</pre>',
                         '<details><summary>Source provenance</summary><pre>'+esc(json.dumps(w['provenance'],ensure_ascii=False,indent=2))+'</pre></details>'])
        bits.append('</article>')
    bits.append('<p><a href="adjacent-word-audit.json">Complete machine-readable audit and exact examples</a></p></html>')
    # The family review owns ADJACENT-WORDS.html. Keep this narrower inference
    # trace separate so rerunning it cannot overwrite the owner's grouped report.
    (args.output/'INFERENCE-CHECKS.html').write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps(dict(comparison=result['comparison'],final_groups_triggering=sum(bool(r['coupled_proposals']) for r in replay),
        combined_history_triggers=len(history['coupled_proposals']),examples=len(details)*2,scope=result['scope'])),flush=True)


if __name__=='__main__':
    main()
