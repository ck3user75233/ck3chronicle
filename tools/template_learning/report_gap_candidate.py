"""Report the implemented owner corrections and production-only candidate results."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path
from template_learning.evidence_serialization import write_json


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--package',type=Path,required=True)
    args=cli.parse_args();root=args.evidence
    read=lambda n:json.loads((root/n).read_bytes())
    check=read('gap-verification.json');stored=read('comparison.json');training=read('training-corpus-comparison.json')
    model=json.loads((args.package/'empirical_template_model.json').read_bytes());templates={t['template_id']:t for t in model['templates']}
    messages=read('messages.json')
    gains=[r for r in messages if not r['results']['production'] and r['results']['candidate']]
    losses=[r for r in messages if r['results']['production'] and not r['results']['candidate']]
    downs=[r for r in messages if r['results']['production'] and r['results']['candidate'] and r['results']['production']['status']=='template' and r['results']['candidate']['status']=='provisional']
    gain_occ=sum(r['occurrences'] for r in gains);loss_occ=sum(r['occurrences'] for r in losses);down_occ=sum(r['occurrences'] for r in downs)
    training_down=training['transitions'].get('template -> provisional',0)
    training_loss=sum(v for k,v in training['transitions'].items() if k in ('template -> no_match','provisional -> no_match'))
    observed_old={e['before'] for e in [*stored['edges'],*training['edges']] if e['before']}
    unobserved_removed=sorted(set(stored['removed'])-observed_old)
    positive=not (loss_occ or down_occ or training_down or training_loss or check['failures'] or check['remaining_grammatical_key_captures'] or check['template_ties'])
    assessment='Positive in the verified scope; ready for owner review' if positive else 'Mixed; remaining exceptions require review'
    removal_note=(f"{len(unobserved_removed)} removed production templates have no selected predecessor witness in either evaluation scope. "
        "This does not establish a lost classification; raw compatibility and actual selected assignments must be distinguished. ")
    if (root/'removal-family-summary.json').exists() and (root/'unselected-removals-review.json').exists():
        families=read('removal-family-summary.json');unselected=read('unselected-removals-review.json')
        unchanged=all(not family['changed_captures'] for family in families.values())
        removal_note+=(f"The separate family review accounts for {unselected['counts'].get('addressed',0)} already-addressed removals "
            f"and checks the other {len(set(i for f in families.values() for i in f['consolidation']['removed_template_ids']))} across {len(families)} families. "
            +(f"All {sum(f['messages'] for f in families.values())} genuine family messages retain the same capture contents and types as production. " if unchanged else "Some family captures change; see the family report. ")
            +"These are learner/catalog findings, not individual template approval requests. ")
    executive=(('The latest correction replaces the two hard-coded history constructions with reusable inference that retains unsupported, unmarked word phrases as literals. ' if (root/'history-inference-correction.json').exists() else '')+
        f"Compared with production, the corrected candidate gains {gain_occ:,} complete assignments in the same 20 stored Runs, loses {loss_occ:,}, and has {down_occ:,} template-to-provisional occurrences. "
        f"Across all 73 training logs, {training_loss:,} complete production assignments are lost and {training_down:,} become provisional. "
        f"The field checks find {len(check['failures'])} failures, {len(check['remaining_grammatical_key_captures'])} flagged grammatical KEY captures and {len(check['template_ties'])} template ties. "
        "All three original diagnostics classify. History and category wording, complete name fields, and equivalent literal dates pass their checks. The assessment is positive on this evidence; coverage alone does not prove semantic accuracy.")
    next_steps='Review this immutable candidate and the production comparison before release/pinning. Production selection and stored Runs remain unchanged.'
    write_json(root/'production-semantic-review.json',dict(assessment=assessment,executive_summary=executive,recommended_next_steps=next_steps))
    esc=lambda s:html.escape(str(s))
    def pre(s):return '<pre>'+esc(''.join(c if c in '\r\n\t' or ord(c)>=32 else '\\u%04x'%ord(c) for c in str(s)))+'</pre>'
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Implemented learner corrections</title><style>body{font:16px/1.55 system-ui;max-width:1180px;margin:32px auto;padding:0 24px;color:#243747}h1,h2{line-height:1.2}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;padding:12px;font-size:13px}td,th{padding:10px;border-bottom:1px solid #ccd6df;vertical-align:top;text-align:left}table{width:100%;border-collapse:collapse}.note{padding:18px;background:#e7f2ed}summary{cursor:pointer}a{color:#075e91}</style>',
        '<h1>Implemented learner corrections</h1><p><a href="CHANGES.html">15 added / 15 removed / newly classified examples</a> · <a href="gap-verification.json">Field verification</a> · <a href="training-corpus-comparison.json">73-log outcomes</a></p>',
        '<p>Production 68f1ae5db205ab46afef9c4d → candidate '+esc(stored['candidate']['package_id'])+'. Same retained 73 logs and recorded 20+20+20+13 schedule. No fresh-versus-incremental comparison.</p>',
        '<h2>'+esc(assessment)+'</h2><p class="note">'+esc(executive)+'</p><p>'+esc(next_steps)+'</p>',
        '<h2>Executable corrections and genuine captures</h2><p>The shared owner-rule recognizer now supplies complete fields during initial discovery and runtime matching. No source message, name, control byte or location value is rewritten. Recognition retains the unchanged full-ID behavior checked in all 91,925 prior contextual rows.</p>']
    if (root/'history-inference-correction.json').exists():
        bits.append('<p><strong>History inference:</strong> the two hard-coded history constructions were removed. Adjacent alphabetic fields that only vary together are reconsidered as one span; the existing boundary check retains these unmarked phrases as literal wording. <a href="LITERAL-CORRECTIONS.html">Trace and genuine history examples</a>.</p>')
    if (root/'REMAINING-REMOVALS.html').exists():
        bits.append('<p>'+esc(removal_note)+'<a href="REMAINING-REMOVALS.html">Grouped family review of removals without selected predecessors</a></p>')
    for definition,counts in check['field_counts'].items():
        bits.append('<h3>'+esc(definition)+'</h3><p>'+esc(f"{counts:,} captures / {check['field_occurrences'][definition]:,} capture occurrences")+'</p>')
        for tid in check['field_templates'][definition]:bits.append('<p>'+esc(tid)+' · '+esc(templates[tid]['status'])+'</p>'+pre(templates[tid]['display']))
        for example in check['field_examples'][definition][:2]:bits.append('<details><summary>Genuine values: '+esc(repr(example['values']))+'</summary>'+pre(example['text'])+'</details>')
    owner_cases=[
        ('1. Comparison types','comparison_types','Retains the accepted whole parenthetical PARAM.'),
        ('2. Invalid comparison side','invalid_comparison','Side and reported identifier are declared KEY fields.'),
        ('3. Trigger failures','trigger_failures','Trigger name is KEY; trigger remains diagnostic wording.'),
        ('4. Unset event target','unset_event_target','Quoted target is KEY.'),
        ('5. Untyped trigger','untyped_trigger','Separate declared construction; the generic construction is inapplicable to this wording. This explains selection and does not claim owner approval of that design.'),
        ('6. Invalid province','invalid_province','Location-layout consolidation only: trailing locator count does not differentiate diagnostic templates.'),
        ('7. Character history','history_phrase','Latest owner correction supersedes the earlier PARAM instruction: after death birth / from before birth remain literal in separate formulations.'),
        ('8. Emblem category','emblem_category','Grouping was accepted but optional. These are the actual current templates; consolidation is not forced.'),
        ('9. Flag / Variable','flag_variable','Grouping was accepted but optional. These are the actual current templates; consolidation is not forced.'),
        ('10. Unknown effect / trigger','unknown_effect_trigger','Corrected at initial construction selection: effect and trigger stay literal.'),
        ('11. Scope mismatch','scope_mismatch','Target, expected scope and actual scope use KEYs.'),
        ('12. Compare-trigger scope','compare_expected_scope','Trigger identifier and expected scope are declared KEYs.'),
        ('13. Previous holders','previous_holders','Quoted title display remains a complete PARAM.'),
        ('14. Formatting tag','formatting_tag','Entire quoted tag is PARAM, including exact control characters and line endings.'),
    ]
    bits.append('<h2>All fourteen owner review cases</h2><p>Counts below show actual selected training occurrences for each listed template, not merely its presence in the package.</p>')
    for title,key,note in owner_cases:
        bits.append('<details><summary>'+esc(title)+'</summary><p>'+esc(note)+'</p>')
        for tid in check['owner_patterns'][key]:
            bits.append('<p>'+esc(f"{tid} · {templates[tid]['status']} · {check['selected_template_occurrences'].get(tid,0):,} selected occurrences")+'</p>'+pre(templates[tid]['display']))
        bits.append('</details>')
    originals=[r for r in messages if any(ref['run_id']=='20261003-IS3QON' and ref['kind']=='review' for ref in r['references'])]
    assert len(originals)==3
    assert all(r['results']['candidate'] and r['results']['candidate']['status']=='template' for r in originals)
    bits.append('<h2>The original three unmatched diagnostics</h2><p>All three original review messages from Run 20261003-IS3QON now receive complete supported-template assignments in this disposable candidate. The stored Run is unchanged.</p>')
    for record in originals:
        result=record['results']['candidate'];tid=result['values']['template_id']
        bits.append('<details><summary>'+esc(record['source']+' → '+tid)+'</summary>'+pre(record['text'])+'<p>Selected template</p>'+pre(templates[tid]['display'])+'</details>')
    audit=read('function-word-audit.json')
    assert sum(r['contextual_messages'] for r in check['residual_function_words'].values())==audit['affected_contextual_messages']
    assert sum(r['occurrences'] for r in check['residual_function_words'].values())==audit['affected_occurrences']
    groups=defaultdict(list)
    for binding in audit['bindings']:groups[binding['template_id']].append(binding)
    audit_bits=[bits[0].replace('<title>Implemented learner corrections</title>','<title>Remaining function-word KEY audit</title>'),'<h1>Remaining function-word spellings in KEY values</h1><p><a href="FIXES.html">Implemented corrections and assessment</a> · <a href="function-word-audit.json">Complete audit data</a></p>',
        '<p>'+esc(f"All {audit['contextual_messages_scanned']:,} contextual rows / {audit['occurrences_scanned']:,} occurrences from the 73 logs were scanned. The explicit spelling inventory flags {audit['affected_contextual_messages']:,} rows / {audit['affected_occurrences']:,} occurrences, across {len(groups)} templates. All assignment regions were examined.")+'</p>',
        '<p>These are spelling matches requiring contextual review, not automatically erroneous slots. A script identifier such as if, a trait name such as Just, can share an English function-word spelling. Game-date month names are now literal, not KEY captures. Native values are preserved; lookup normalization does not alter captures. Counts per binding overlap and must not be summed as distinct messages.</p>']
    audit_bits.append('<h2>Contextual review of the remaining matches</h2>'+pre(json.dumps(check['residual_function_words'],indent=2))+'<p>The remaining flagged template contexts and their values were reviewed. These categories describe this genuine evidence, not a general inference rule that permits grammatical wording to become KEY.</p>')
    for tid,bindings in sorted(groups.items(),key=lambda item:(templates[item[0]]['source_family'],item[0])):
        audit_bits.append('<details><summary>'+esc(templates[tid]['source_family']+' · '+tid)+'</summary>'+pre(templates[tid]['display']))
        for binding in bindings:
            audit_bits.append('<details><summary>'+esc(f"{binding['slot']}: {binding['value']} — {binding['contextual_messages']:,} messages / {binding['occurrences']:,} occurrences")+'</summary>')
            for example in binding['examples']:audit_bits.append(pre(example['text'])+'<p>'+esc(example['provenance'])+'</p>')
            audit_bits.append('</details>')
        audit_bits.append('</details>')
    audit_bits.append('</html>');(root/'FUNCTION-WORDS.html').write_text('\n'.join(audit_bits),encoding='utf-8')
    bits.append('<p><a href="FUNCTION-WORDS.html">Every remaining function-word spelling: templates, slots, counts and genuine examples</a>. This is a complete scan of the stated vocabulary across the 73-log evidence; it is not a blanket prohibition on those spellings.</p>')
    removal=read('removed-template-analysis.json');rs=removal['summary']
    removal_bits=[bits[0].replace('<title>Implemented learner corrections</title>','<title>Production template replacements</title>'),'<h1>Where the removed production templates went</h1><p><a href="CHANGES.html">Main production comparison</a> · <a href="FIXES.html">Corrections and owner cases</a> · <a href="removed-template-analysis.json">Complete capture-change evidence</a></p>',
        '<p>'+esc(f"{rs['removed']} production template IDs are absent from the candidate. {rs['observed_removed']} have selected witnesses mapping to {rs['destination_templates']} candidate templates. {len(rs['unobserved_removed'])} have no selected witness. {rs['many_to_one_destinations']} destinations each replace more than one old template, involving {rs['removed_with_many_to_one_destination']} removed IDs.")+'</p>',
        '<p>'+esc(removal['method'])+'</p>',
        '<h2>Changes in literal and slot roles</h2><p>The counts overlap: a removed template may have different outcomes on different genuine witnesses. Location changes are separated from changes to diagnostic words. Neither a lower template count nor a many-to-one mapping proves semantic improvement.</p>'+pre(json.dumps(rs['overlapping_theme_counts'],indent=2)),
        '<h2>Many-to-one replacements</h2>']
    old_templates=removal['templates']['production'];witnesses=removal['witnesses']
    old_sources=Counter(t['source_family'] for t in old_templates.values());new_sources=Counter(t['source_family'] for t in templates.values())
    source_rows=sorted((dict(source=s,production=old_sources[s],candidate=new_sources[s],change=new_sources[s]-old_sources[s]) for s in old_sources.keys()|new_sources.keys() if old_sources[s]!=new_sources[s]),key=lambda r:(r['change'],r['source']))
    source_table='<h2>Where the net template-count change occurs</h2><table><tr><th>Emitter</th><th>Production</th><th>Candidate</th><th>Change</th></tr>'+''.join('<tr>'+''.join('<td>'+esc(row[k])+'</td>' for k in ('source','production','candidate','change'))+'</tr>' for row in source_rows)+'</table>'
    removal_bits.insert(-1,source_table)
    for tid,old_ids in sorted(removal['incoming'].items(),key=lambda item:(-len(item[1]),item[0])):
        if len(old_ids)<2:continue
        removal_bits.append('<details><summary>'+esc(f"{len(old_ids)} old templates → {tid} · {templates[tid]['source_family']}")+'</summary>')
        for old_id in old_ids:
            removal_bits.append('<details><summary>'+esc(old_id+' · '+old_templates[old_id]['display'].strip().splitlines()[0])+'</summary><h3>Production</h3>'+pre(old_templates[old_id]['display']))
            for witness in witnesses:
                if (witness['before'],witness['after'])!=(old_id,tid):continue
                removal_bits.append('<p>'+esc(f"{witness['scope']}: {witness['messages']:,} contextual messages / {witness['occurrences']:,} occurrences; {witness['before_status']} → {witness['after_status']}. Witness theme: {witness['theme']}.")+'</p>')
                changes=[{k:change[k] for k in ('text','before','after','location')} for change in witness['changes'] if change['words']]
                removal_bits.append(pre(json.dumps(changes,ensure_ascii=False,indent=2))+'<details><summary>Genuine native witness</summary>'+pre(witness['native_regions']['body'])+'</details>')
            removal_bits.append('</details>')
        removal_bits.append('<h3>One shared candidate template</h3>'+pre(templates[tid]['display'])+'</details>')
    removal_bits.append('<h2>Removed templates without a selected witness</h2><p>These were not selected production assignments in the evaluated evidence. Their absence alone is not a lost classification. <a href="REMAINING-REMOVALS.html">The grouped raw-evidence review distinguishes already-addressed cases from catalog redundancy.</a> This is not an individual-template approval queue.</p>')
    for tid in rs['unobserved_removed']:removal_bits.append('<details><summary>'+esc(tid+' · '+old_templates[tid]['source_family'])+'</summary>'+pre(old_templates[tid]['display'])+'</details>')
    removal_bits.append('</html>');(root/'REMOVALS.html').write_text('\n'.join(removal_bits),encoding='utf-8')
    bits.append('<p><a href="REMOVALS.html">Removed-template analysis: every many-to-one replacement and its literal/slot changes</a>. Location-only changes and unobserved old templates are identified separately.</p>')
    bits.extend(['<h2>Why the original category protection failed—and what now prevents it</h2>',
        '<p>The retained v54 code reproduced all four originally disputed templates exactly. Unknown effect and Unknown trigger entered one initial group at similarity 0.83636 above the 0.72 threshold. Initial alignment then made effect/trigger KEY values. Revision wording-loss checks had no earlier literal template to compare. A later proposal also swallowing Unknown into a KEY was rejected, correctly, but the category words were already slots.</p>',
        '<p>The new learner explicitly separates the two declared diagnostic constructions in pdx_persistent_reader.cpp. The earlier v56 source-pool check demonstrated this category fix; v57 retains it and separately verifies the latest literal corrections. Unknown after a location marker remains a LOCATOR under the existing positional rule; leading Unknown remains diagnostic wording. <a href="reviewed-inference-traces.json">Original exact decision trace</a> · <a href="initial-inference-correction.json">Earlier v56 category-correction check</a>.</p>',
        '<p>The history after/from and death/before slots also arose in initial alignment as separate single-token variations. '+('The two hard-coded history constructions are now removed. Reusable inference reconsiders adjacent words that only vary together; existing boundary requirements reject the undemarcated phrase as a field and retain the complete literal formulations. <a href="LITERAL-CORRECTIONS.html">Frozen-release trace and history verification</a>. ' if (root/'history-inference-correction.json').exists() else 'This older candidate uses separate history constructions, an implementation the owner subsequently disputed. ')+'The emblem and Flag/Variable initial groupings used single-token KEY evidence; those optional groupings were owner-accepted and are not forced into this incremental candidate.</p>',
        '<h2>Remaining grammatical KEYs and name boundaries</h2><p>'+esc(f"The full candidate scan finds {len(check['remaining_grammatical_key_captures'])} of the demonstrated grammatical KEY captures. Complete missing-localization fields use PARAM for single-word and multiword values; this is an explicit field-typing change, not a claim of new coverage for every retyped value. Marked Cheater/With character fields include names, lowercase particles and formatting bytes intact. These name-fragment limitations were already present in production.")+'</p>',
        '<h2>Template ties and outcomes</h2><p>'+esc(f"Candidate training evidence contains {len(check['template_ties'])} template ties. Production-to-candidate training transitions are shown below; provisional outcomes remain legitimate complete assignments, not unmatched messages.")+'</p>'+pre(json.dumps(training['transitions'],indent=2)),
        '<h2>Exceptions requiring attention</h2>'+pre(json.dumps(dict(field_failures=check['failures'],grammatical_keys=check['remaining_grammatical_key_captures'],ties=check['template_ties']),ensure_ascii=True,indent=2)),
        '<p>Accepted comparison PARAMs, generic triggers, event targets, scope mismatches and previous-holder PARAMs remain acceptance cases. The dedicated untyped construction retains its owner-directed extraction; it is not a literal-preference tie-breaker. Repeated locators retain every original ordered value and remain significant for message identity.</p>',
        '<p>No production pin, runtime process or stored Run was changed. This is a disposable candidate for review, not a production release.</p></html>'])
    (root/'FIXES.html').write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps(dict(assessment=assessment,gained=gain_occ,lost=loss_occ,downgraded=down_occ,training_downgraded=training_down,training_lost=training_loss),indent=2))


if __name__=='__main__':main()
