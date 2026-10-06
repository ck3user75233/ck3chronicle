"""Human review of actual production outcomes versus an immutable learner candidate."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path

from template_learning.location_candidate_experiment import save


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--production',type=Path,required=True)
    cli.add_argument('--candidate',type=Path,required=True)
    cli.add_argument('--prior-evidence',type=Path,help='Earlier candidate comparison on exactly the same native evidence.')
    cli.add_argument('--include-build-history',action='store_true',help='Explicitly include the separate fresh/incremental control comparison.')
    cli.add_argument('--next-steps',help='Explicit owner-directed receiving guidance for this report.')
    args=cli.parse_args();out=args.evidence.resolve()
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    c=read(out/'comparison.json');messages=read(out/'messages.json');by_key={r['key']:r for r in messages}
    broad=read(out/'training-corpus-comparison.json') if (out/'training-corpus-comparison.json').exists() else None
    broad_edges=defaultdict(list)
    for edge in broad['edges'] if broad else []:
        if edge['before']:broad_edges[edge['before']].append(edge)
    models={k:read(p/'empirical_template_model.json') for k,p in [('production',args.production),('candidate',args.candidate)]}
    templates={k:{t['template_id']:t for t in m['templates']} for k,m in models.items()}
    gains=[r for r in messages if r['results']['production'] is None and r['results']['candidate']]
    losses=[r for r in messages if r['results']['production'] and r['results']['candidate'] is None]
    down=[r for r in messages if r['results']['production'] and r['results']['production']['status']=='template' and r['results']['candidate'] and r['results']['candidate']['status']=='provisional']
    original_reviews=[r for r in messages if any(ref['run_id']=='20261003-IS3QON' and ref['kind']=='review' for ref in r['references'])]
    original=[r for r in original_reviews if r in gains]
    incoming=defaultdict(list);outgoing=defaultdict(list);gain_counts=Counter()
    for edge in c['edges']:
        if edge['after']:incoming[edge['after']].append(edge)
        if edge['before']:outgoing[edge['before']].append(edge)
    for r in gains:gain_counts[r['results']['candidate']['values']['template_id']]+=r['occurrences']
    for edges in [*incoming.values(),*outgoing.values()]:edges.sort(key=lambda e:-e['occurrences'])
    added=[]
    for r in original:
        identifier=r['results']['candidate']['values']['template_id']
        if identifier in c['added'] and identifier not in added:added.append(identifier)
    rank=lambda i:(-gain_counts[i],-sum(e['occurrences'] for e in incoming[i]),i)
    added=(added+[i for i in sorted(c['added'],key=rank) if i not in added])[:15]
    coverage=c['removed_coverage'];removed=[]
    overall={}
    for identifier, info in coverage.items():
        edges=broad_edges[identifier]
        overall[identifier]=('has_lost_matches' if info['lost'] or any(e['after'] is None for e in edges) else
            'has_status_downgrades' if info['downgraded'] or any(e['before_status']=='template' and e['after_status']=='provisional' for e in edges) else
            'covered_by_replacements' if info['edges'] or edges else 'not_observed')
    for category,limit in [('has_lost_matches',4),('has_status_downgrades',4),('covered_by_replacements',5),('not_observed',2)]:
        pool=[i for i,v in overall.items() if v==category]
        pool.sort(key=lambda i:(-coverage[i]['lost'],-coverage[i]['downgraded'],-coverage[i]['occurrences'],i))
        removed.extend(pool[:limit])
    removed=(removed+[i for i in c['removed'] if i not in removed])[:15]
    # A many-to-one replacement is one review case. Include every removed
    # predecessor in that case, then display its successor exactly once.
    removal_groups=defaultdict(list)
    for identifier in c['removed']:
        edges=[*coverage[identifier]['edges'],*broad_edges[identifier]]
        successors={e['after'] for e in edges}
        group=('successor',next(iter(successors))) if len(successors)==1 and None not in successors else ('individual',identifier)
        removal_groups[group].append(identifier)
    group_for={identifier:key for key,ids in removal_groups.items() for identifier in ids}
    sampled_groups=[];sampled_ids=[]
    for identifier in [*removed,*c['removed']]:
        key=group_for[identifier];ids=removal_groups[key]
        if key not in sampled_groups and len(sampled_ids)+len(ids)<=15:
            sampled_groups.append(key);sampled_ids.extend(ids)
    removed=sampled_ids
    gained_examples=list(original);represented={r['results']['candidate']['values']['template_id'] for r in original}
    for r in sorted(gains,key=lambda r:(-r['occurrences'],r['key'])):
        identifier=r['results']['candidate']['values']['template_id']
        if identifier not in represented and len(gained_examples)<15:gained_examples.append(r);represented.add(identifier)
    for r in sorted(gains,key=lambda r:(-r['occurrences'],r['key'])):
        if len(gained_examples)>=15:break
        if r not in gained_examples:gained_examples.append(r)
    def diverse(rows,n):
        chosen=[];seen=set()
        for r in sorted(rows,key=lambda r:-r['occurrences']):
            identifier=r['results']['production']['values']['template_id']
            if identifier not in seen:chosen.append(r);seen.add(identifier)
            if len(chosen)==n:break
        return chosen
    samples=dict(added=added,removed=removed,gained=[r['key'] for r in gained_examples],lost=[r['key'] for r in diverse(losses,8)],downgraded=[r['key'] for r in diverse(down,8)])
    save(out/'review-samples.json',samples)
    n_gain=sum(r['occurrences'] for r in gains);n_loss=sum(r['occurrences'] for r in losses);n_down=sum(r['occurrences'] for r in down)
    assert not c['production_parity_mismatches']
    same_training=c.get('training_comparison',{}).get('exact_hash_set',False)
    training_counts={k:m['summary']['distinct_error_logs'] for k,m in models.items()}
    incremental=models['candidate']['algorithm'].get('build_strategy')=='same-version-additive-v1'
    versions={k:m['algorithm']['clusterer_version'].rsplit('-',1)[-1] for k,m in models.items()}
    broad_losses=sum(broad['transitions'].get(k,0) for k in ('template -> no_match','provisional -> no_match')) if broad else 0
    broad_down=broad['transitions'].get('template -> provisional',0) if broad else 0
    negative=bool(n_loss or n_down or broad_losses or broad_down)
    assessment=('Mixed: coverage gains with remaining regressions' if n_gain and negative else
                'Positive on the evaluated evidence: gains without observed regressions' if n_gain else
                'Negative on the evaluated evidence' if negative else 'No coverage or support-status change')
    history=read(out/'build-history-comparison.json') if args.include_build_history and (out/'build-history-comparison.json').exists() else None
    semantic_review=''
    if history:
        retained=[str(r['number']) for r in history['cases'] if r['number'] in (7,10) and r['identical_display_successors']]
        semantic_review=(' Owner-rejected wording remains selected in example(s) '+', '.join(retained)+'. ' if retained else
                         ' The rejected fresh patterns have different incremental successors; those changes still require semantic review. ')
        semantic_review+='Coverage does not establish resolution of the owner’s concerns. See the controlled build-history report for all 14 examples.'
        observations=history.get('semantic_observations',{})
        if observations.get('character_history_retains_two_literal_phrases') and observations.get('unknown_effect_trigger_retains_literal_categories'):
            semantic_review=(' The incremental build avoids both rejected KEY patterns: effect/trigger remain literal, '
                'and character history retains its two literal phrases. The requested shared history PARAM remains unimplemented. '
                'The exact learning decisions and contextual KEY audit remain to be investigated. See the controlled build-history report for all 14 examples.')
        fresh_loss=history.get('lost_fresh_coverage',{})
        if fresh_loss.get('occurrences'):
            semantic_review+=f' Compared with fresh v54, {fresh_loss["occurrences"]:,} occurrences across {fresh_loss["messages"]} messages lose assignments; these were also unmatched in production.'
        if n_gain:
            assessment='Mixed: coverage gains with unresolved semantic concerns'
    executive=(f'The candidate classifies {n_gain:,} previously unclassified production occurrences ({len(gains)} distinct messages). '
               f'{len(original)} of {len(original_reviews)} original Run IS3QON review messages now have complete assignments. '+
               (f'One previously classified occurrence loses its assignment. ' if n_loss==1 else f'{n_loss:,} previously classified occurrences lose their assignments. ')+
               (f'{n_down:,} occurrences move from template to provisional. ' if n_down else 'No template assignments become provisional in these Runs. ')+
               f'Provisional assignments remain complete and valid in the pipeline; they are not counted as lost matches. Net complete coverage improves by {n_gain-n_loss:,} occurrences. '
               + ('Both packages use the exact same training-log hash set. ' if same_training else 'The training sets differ, so training breadth confounds the comparison. ')
               + (f'The separate 73-log training-corpus check has {broad_losses:,} lost assignments and {broad_down:,} template-to-provisional occurrences. These overlapping scopes must not be added together. ' if broad else '')
               + ('Retain the fixes, but resolve or explicitly review the remaining regressions before promotion.' if negative else
                  'This is positive coverage evidence, not proof that every changed template generalizes correctly.')+semantic_review)
    next_steps=(('Resolve the lost marked-up character-name assignment and review the two support-downgrade families detailed below before promotion. ' if (out/'regression-investigation.json').exists() and negative else
                 'Resolve or explicitly accept the remaining coverage/support regressions before promotion. ' if negative else '')+
                ('Training breadth and the recorded incremental schedule are now matched; trace remaining differences through learner decisions. ' if same_training and incremental else
                 'Training breadth is now matched; investigate implementation and fresh-versus-additive build history for any remaining differences. ' if same_training else
                 'Rebuild on the exact production training corpus before attributing differences to the learner changes. ')+
                ('Use the completed full-corpus removal crosswalk to review remaining unsupported generalizations and any templates without witnesses. ' if broad else
                 'Exercise unobserved removed templates on the broader genuine corpus and review changed generalizations and slot captures. ')+
                'Submit the immutable candidate for owner release/pin approval only after that review. Production remains unchanged.')
    semantic_path=out/'production-semantic-review.json'
    semantics=read(semantic_path) if semantic_path.exists() else None
    if semantics:
        assessment=semantics['assessment']
        executive=semantics['executive_summary']
        next_steps=semantics['recommended_next_steps']
    if args.next_steps is not None:
        next_steps=args.next_steps
    summary=dict(assessment=assessment,executive_summary=executive,recommended_next_steps=next_steps,
                 gained_occurrences=n_gain,gained_distinct_messages=len(gains),lost_occurrences=n_loss,lost_distinct_messages=len(losses),
                 downgraded_occurrences=n_down,downgraded_distinct_messages=len(down),net_complete_gain=n_gain-n_loss,
                 training_corpus_lost_occurrences=broad_losses,training_corpus_downgraded_occurrences=broad_down,
                 removed_categories=Counter(v['category'] for v in coverage.values()),sample_counts={k:len(v) for k,v in samples.items()})
    summary['removed_categories_across_both_scopes']=Counter(overall.values())
    save(out/'executive-summary.json',summary)
    esc=lambda v:html.escape(str(v));fmt=lambda v:f'{v:,}'
    pre=lambda v:'<pre>'+esc(''.join(c if c in '\r\n\t' or ord(c)>=32 else '\\u%04x'%ord(c) for c in str(v)))+'</pre>'
    shown_templates=set();shown_patterns={};shown_examples={}
    def pattern(text):
        if text in shown_patterns:
            return '<p>Exact text already shown <a href="#'+shown_patterns[text]+'">above</a>.</p>'
        anchor='pattern-'+str(len(shown_patterns)+1);shown_patterns[text]=anchor
        return '<div id="'+anchor+'">'+pre(text)+'</div>'
    def template(label,identifier):
        t=templates[label][identifier];anchor='template-'+label+'-'+identifier
        state=('PRODUCTION BEFORE — removed from this candidate' if label=='production' and identifier in c['removed'] else
               'PRODUCTION BEFORE' if label=='production' else 'CANDIDATE AFTER — '+versions['candidate'])
        meta='<strong>'+esc(state)+'</strong> · '+esc(t['source_family'])+' · '+esc(t['status'])+' · <code>'+identifier+'</code>'
        if (label,identifier) in shown_templates:
            return '<p class="meta">'+meta+' · <a href="#'+anchor+'">template shown above</a></p>'
        shown_templates.add((label,identifier))
        return '<div id="'+anchor+'"><p class="meta">'+meta+'</p>'+pattern(t['display'])+'</div>'
    def body_example(text):
        if text in shown_examples:
            number=shown_examples[text]
            return '<p>Same exact body as <a href="#example-'+str(number)+'">Example E'+str(number).zfill(2)+'</a>.</p>'
        number=len(shown_examples)+1;shown_examples[text]=number
        return '<div id="example-'+str(number)+'"><h4>Example E'+str(number).zfill(2)+'</h4>'+pattern(text)+'</div>'
    def provenance(r):
        ref=r['references'][0]
        where=('review emission '+','.join(map(str,ref['emission_ordinals']))) if ref['kind']=='review' else 'stored record '+str(ref['ordinal'])
        return '<p class="meta">'+esc(ref['run_id'])+' · '+esc(where)+' · '+fmt(r['occurrences'])+' total occurrences across these Runs</p>'
    def message_example(r):return provenance(r)+'<details><summary>Exact genuine message body</summary>'+body_example(r['text'])+'</details>'
    title='Production '+versions['production']+' versus candidate '+versions['candidate']
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><title>'+esc(title)+'</title>', '''
<style>body{font:16px/1.55 system-ui;max-width:1140px;margin:34px auto;padding:0 24px;color:#183040}h1,h2,h3{line-height:1.25}a{color:#086093}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f7;padding:15px;font-size:13px;max-height:460px;overflow:auto}table{border-collapse:collapse;width:100%}th,td{padding:9px;border-bottom:1px solid #c6d2dc;text-align:left}.meta{font-size:13px;color:#506477}.note{background:#edf4fa;border-left:4px solid #377d9b;padding:16px}.mixed{background:#fff3db;border-left:4px solid #a86c09;padding:16px}article{border-top:2px solid #d8e0e8;margin-top:24px;padding-top:10px}summary{cursor:pointer}nav a{margin-right:14px}</style>
''', '<h1>'+esc(title)+'</h1>', '''
<nav><a href="#summary">Executive summary</a><a href="#added">15 added</a><a href="#removed">15 removed</a><a href="#gained">New classifications</a><a href="#regressions">Regressions</a><a href="#scope">Scope and evidence</a></nav>''']
    bits.extend(['<h2 id="summary">'+esc(assessment)+'</h2><p class="mixed">'+esc(executive)+'</p>',
                 '<p><strong>Recommended next steps.</strong> '+esc(next_steps)+'</p>',
                 '<p class="note">This compares the selected production package with the candidate on the same retained database backup and native review evidence used in the earlier comparison: '+str(len(c['runs']))+' Runs, '+fmt(c['checks']['stored_records'])+' stored records and '+fmt(sum(c['counts']['production'].values()))+' total message/recovery occurrences. Production replay agrees with every stored status and template assignment, and every no-match review route. Production remains unchanged.</p>'])
    if history:
        bits.append('<p><a href="BUILD-HISTORY.html">Production, fresh and incremental results: all 14 owner-reviewed examples</a></p>')
    if semantics:
        detail_page = 'FIXES.html' if (out/'FIXES.html').exists() else 'SEMANTICS.html'
        bits.append(f'<p><a href="{detail_page}">Production versus candidate: matching, captures and template corrections</a></p>')
    if (out/'REMOVALS.html').exists():
        bits.append('<p><a href="REMOVALS.html">Every many-to-one replacement, exact literal/slot changes, and removed templates without witnesses</a></p>')
    if (out/'removed-template-summary.json').exists():
        removal=read(out/'removed-template-summary.json')
        bits.append('<p class="mixed"><strong>Template quality follow-up.</strong> The inventory falls from 689 to 496 templates. '+
            str(removal['same_display_pairs'])+' removed templates have successors with identical displayed patterns; only location constraints and support metadata differ. '+
            'Other consolidations include meaningful category wording becoming KEY slots and explanatory clauses becoming PARAMs. Higher matching coverage does not establish that every such generalization is desirable. '+
            '<a href="CONSOLIDATIONS.html">Review each new template alongside all the old templates it replaces.</a> '+
            '<a href="REMOVED-TEMPLATES.html">Full thematic analysis and removal crosswalk.</a></p>')
    if args.prior_evidence:
        prior=read(args.prior_evidence/'messages.json')
        assert {r['key']:r['occurrences'] for r in prior}=={r['key']:r['occurrences'] for r in messages}
        groups=defaultdict(Counter);detail=[]
        for r in prior:
            production,previous=r['results']['production'],r['results']['candidate']
            kind=('lost' if production and not previous else 'downgraded' if production and previous and
                  production['status']=='template' and previous['status']=='provisional' else None)
            if kind:
                current=by_key[r['key']]['results']['candidate'];status=current['status'] if current else 'no_match'
                groups[kind][status+'_distinct_messages']+=1
                groups[kind][status+'_occurrences']+=r['occurrences']
                detail.append(dict(key=r['key'],previous_regression=kind,current_status=status))
        save(out/'prior-regression-resolution.json',dict(same_evaluation_evidence=True,groups=groups,messages=detail))
        recovered=sum(v for k,v in groups['lost'].items() if k in ('template_occurrences','provisional_occurrences'))
        restored=groups['downgraded'].get('template_occurrences',0)
        bits.append('<h2>What changed after expanding training</h2><p>On exactly the same evaluated messages and occurrence counts, '+fmt(recovered)+' of the earlier 60 lost occurrences regain complete assignments. All '+fmt(restored)+' earlier downgraded occurrences regain template status.</p><details><summary>Exact earlier-regression outcomes</summary>'+pre(json.dumps(groups,indent=2))+'</details>')
    bits.append('<table><tr><th>Outcome</th><th>Production</th><th>Candidate</th><th>Change</th></tr>')
    for status in ['template','provisional','no_match','unresolved_recovery']:
        a=c['counts']['production'].get(status,0);b=c['counts']['candidate'].get(status,0)
        bits.append('<tr><td>'+status+'</td><td>'+fmt(a)+'</td><td>'+fmt(b)+'</td><td>'+f'{b-a:+,}'+'</td></tr>')
    bits.append('</table><p>'+fmt(c['transitions'].get('provisional -> template',0))+' provisional occurrences also become template assignments. The one unresolved recovery remains unresolved; no parser change is claimed.</p>')
    bits.append('<h2>Template inventory and removal assessment</h2>'+pre(json.dumps(c['inventory'],indent=2)))
    bits.append('<p>Added/removed means exact template IDs, including provisional templates. A replacement or consolidation can change an ID without adding or losing an error family. '+
                f'Production has {len(templates["production"])} templates from {training_counts["production"]} logs; the candidate has {len(templates["candidate"])} from {training_counts["candidate"]} logs. '+
                ('All training hashes agree. This candidate follows the recorded production incremental schedule, controlling the build method for this production-to-candidate comparison.' if same_training and incremental else
                 'All training hashes agree. Production records an additive build history; this candidate is freshly learned with the corrected implementation, so identical inputs do not isolate build-history effects.' if same_training else
                 'Training sets differ; this combines implementation changes with training differences.')+'</p>')
    labels=dict(covered_by_replacements='Observed assignments preserved through replacements',has_lost_matches='At least one observed match lost',has_status_downgrades='Status downgrades, without observed match loss',not_observed='No selected witness in this scope; replacement unverified')
    bits.append('<table><tr><th>Removed templates</th><th>Count</th></tr>'+''.join('<tr><td>'+labels[k]+'</td><td>'+str(summary['removed_categories'].get(k,0))+'</td></tr>' for k in labels)+'</table><p>These categories are exclusive; a template with both loss and downgrade is counted under loss. Preserved observed assignments do not prove equivalence for every possible message. Unobserved templates cannot be called safe removals.</p>')
    if broad:
        combined=summary['removed_categories_across_both_scopes']
        bits.append('<h3>Removal assessment using both evidence scopes</h3><table><tr><th>Removed template outcome</th><th>Count</th></tr>'+''.join('<tr><td>'+labels[k]+'</td><td>'+str(combined.get(k,0))+'</td></tr>' for k in labels)+'</table><p>This incorporates the full training corpus as well as the stored Runs. A template is counted once; any observed loss takes precedence over a downgrade or replacement. "No selected witness" means the template was never the selected assignment in this evidence, not that it could not match anything.</p>')
    bits.append('<h2 id="added">15 added template examples</h2><p>Sample prioritizes the original fixes, newly classified production review messages, then observed replacement coverage. These are new templates relative to production, not necessarily new diagnostic families.</p>')
    bits.append('<p class="note"><strong>Reading the patterns.</strong> &lt;LOCATOR entries: one or more&gt; permits the complete trailing file/line/(trace) entries, with separate LOCATOR values and parenthetical PARAM traces retained in native order. Entry count does not affect classification similarity; exact values and count still distinguish message identities. Provisional templates are valid complete assignments in the pipeline. The travel emitter really places file/line/trace text before the in-game date in its native body; that ordering is visible in the genuine examples below.</p>')
    for number,identifier in enumerate(added,1):
        edges=incoming[identifier];predecessors=[e for e in edges if e['before']]
        predecessor_ids=sorted({e['before'] for e in [*edges,*(e for e in broad['edges'] if e['after']==identifier)] if e['before']}) if broad else sorted({e['before'] for e in predecessors})
        bits.append('<article><h3>'+str(number)+'. Candidate template</h3><p>'+fmt(gain_counts[identifier])+' previously unclassified occurrences in the stored Runs now use this template; '+str(len(predecessor_ids))+' selected predecessor templates across both evidence scopes.</p>')
        if predecessor_ids:
            bits.append('<p class="note"><strong>Before/after:</strong> the patterns below are production predecessors, not the new candidate pattern. '
                        '<a href="#template-candidate-'+identifier+'">Jump to the candidate successor</a>. '
                        'All predecessors are shown together so their changes can be compared with that one successor.</p>')
            bits.append('<h4>Before: production predecessors</h4>'+''.join(template('production',old_id) for old_id in predecessor_ids))
        bits.append('<h4>After: candidate successor</h4>'+template('candidate',identifier))
        if predecessors:
            bits.append(message_example(by_key[predecessors[0]['example_key']]))
        elif edges:bits.append(message_example(by_key[edges[0]['example_key']]))
        else:bits.append('<p>No assignment to this template is observed in these Runs; it is present in the candidate inventory.</p>')
        bits.append('</article>')
    bits.append('<h2 id="removed">'+str(len(removed))+' removed templates in '+str(len(sampled_groups))+' replacement cases</h2><p>All removed predecessors with the same single selected successor are grouped together; the candidate appears once after them. Complete groups exceeding the 15-template sample budget remain in the full crosswalk. Counts from the two evidence scopes overlap and are not added together.</p>')
    for number,key in enumerate(sampled_groups,1):
        ids=removal_groups[key]
        if key[0]=='successor':
            bits.append('<article><h3>'+str(number)+'. '+str(len(ids))+' production template(s) → one candidate template</h3>')
            for identifier in ids:
                info=coverage[identifier]
                bits.append(template('production',identifier)+'<p>'+fmt(info['occurrences'])+' selected occurrences in the 20 stored Runs; '+fmt(sum(e['occurrences'] for e in broad_edges[identifier]))+' in the separate training scope.</p>')
            bits.append('<h4>Shared successor</h4>'+template('candidate',key[1]))
            edges=[e for identifier in ids for e in coverage[identifier]['edges']]
            if edges:bits.append(message_example(by_key[max(edges,key=lambda e:e['occurrences'])['example_key']]))
            else:
                edge=max((e for identifier in ids for e in broad_edges[identifier]),key=lambda e:e['occurrences'])
                bits.append('<details><summary>Genuine training message</summary>'+body_example(edge['example']['text'])+'</details>')
            bits.append('</article>')
            continue
        identifier=ids[0]
        info=coverage[identifier];bits.append('<article><h3>'+str(number)+'. '+labels[overall[identifier]]+'</h3>'+template('production',identifier)+
            '<p>In the 20 stored Runs: '+fmt(info['occurrences'])+' observed occurrences; '+fmt(info['lost'])+' lost assignments; '+fmt(info['downgraded'])+' template → provisional.</p>')
        if not info['edges'] and not broad_edges[identifier]:bits.append('<p>This template was not selected in either scope. That alone is neither a classification loss nor a learner defect. Raw compatibility and competing selected templates establish whether this is catalog redundancy; it is not a request to approve an individual template.</p>')
        for edge in sorted(info['edges'],key=lambda e:(e['after'] is not None,-e['occurrences']))[:3]:
            bits.append('<p>'+fmt(edge['occurrences'])+' occurrences: '+esc(edge['before_status']+' → '+edge['after_status'])+'</p>')
            if edge['after']:bits.append(template('candidate',edge['after']))
            else:bits.append('<p><strong>No complete candidate assignment.</strong></p>')
            bits.append(message_example(by_key[edge['example_key']]))
        if not info['edges'] or overall[identifier]=='has_status_downgrades':
            for edge in sorted(broad_edges[identifier],key=lambda e:(e['after_status']!='provisional',-e['occurrences']))[:2]:
                bits.append('<p>In the separate 73-log corpus: '+fmt(edge['occurrences'])+' occurrences, '+esc(edge['before_status']+' → '+edge['after_status'])+'.</p>')
                if edge['after']:bits.append(template('candidate',edge['after']))
                bits.append('<details><summary>Genuine training-corpus example</summary>'+body_example(edge['example']['text'])+'</details>')
        bits.append('</article>')
    bits.append('<h2 id="gained">Previously unclassified production message examples</h2><p>Every example below came from an actual production no_match review route and is now completely classified. Together the '+str(len(gains))+' distinct gained messages use '+str(len(gain_counts))+' candidate templates. This sample covers '+str(len(represented))+' target templates and prioritizes the original IS3QON diagnostics. Exact slot values are available beneath each example.</p>')
    for number,r in enumerate(gained_examples,1):
        after=r['results']['candidate'];identifier=after['values']['template_id']
        bits.append('<article><h3>'+str(number)+'. Production no_match → '+esc(after['status'])+'</h3>'+provenance(r)+'<h4>Candidate template</h4>'+template('candidate',identifier)+'<h4>Previously unclassified message</h4>'+body_example(r['text']))
        bindings=[(v['name'],b['type'],b['value']) for v in after['values']['regions'] for b in v['bindings']]
        bits.append('<details><summary>Actual captured slot values</summary><table><tr><th>Region</th><th>Type</th><th>Value</th></tr>'+''.join('<tr>'+''.join('<td>'+esc(v)+'</td>' for v in row)+'</tr>' for row in bindings)+'</table></details></article>')
    bits.append('<h2 id="regressions">Coverage and support regressions</h2><p>'+f'There are {n_loss} lost complete assignments, covering {len(losses)} exact messages, plus {n_down} status downgrades over {len(down)} exact messages. '+'Provisional records remain valid complete classifications. The following examples distinguish actual missing coverage from a lower support status.</p>')
    for title,key in [('Lost-match examples','lost'),('Downgraded message examples','downgraded')]:
        bits.append('<h3>'+title+'</h3>')
        for digest in samples[key]:
            r=by_key[digest];a,b=r['results']['production'],r['results']['candidate']
            bits.append('<details><summary>'+esc(r['source'])+' · '+fmt(r['occurrences'])+' occurrences · '+('lost' if b is None else 'template → provisional')+'</summary>'+template('production',a['values']['template_id'])+message_example(r))
            if b:
                t=templates['candidate'][b['values']['template_id']]
                bits.append(template('candidate',t['template_id'])+'<p>Candidate learning support:</p>'+pre(json.dumps(t.get('learning_support',{}),indent=2)))
            bits.append('</details>')
    remaining=Counter()
    for r in messages:
        if r['results']['candidate'] is None:remaining[r['source']]+=r['occurrences']
    bits.append('<h3>Remaining unmatched occurrences by source</h3>'+pre(json.dumps(dict(remaining.most_common()),indent=2)))
    for r in sorted((r for r in messages if r['results']['candidate'] is None),key=lambda r:-r['occurrences'])[:3]:
        bits.append('<details><summary>Remaining unmatched: '+esc(r['source'])+' · '+fmt(r['occurrences'])+' occurrences</summary>'+message_example(r)+'</details>')
    locator_changes=c['checks']['messages_with_changed_locator_captures']
    bits.append('<h2 id="scope">Scope, verification and limits</h2><p>All selected assignments reconstruct their exact native regions. No distinct native messages collapse to one candidate identity. '+
                ('All existing LOCATOR captures are preserved on messages matched by both packages. ' if not locator_changes else
                 str(locator_changes)+' messages have changed existing LOCATOR captures and require review. ')+
                'Changed capture content/types occur in '+str(c['checks']['changed_capture_messages'])+' distinct messages and are retained in comparison.json; this includes intended date/name/trace generalization. These checks establish data fidelity, not exhaustive semantic correctness of all generalized templates.</p>')
    bits.append('<p>The review shards were reparsed with the unchanged authenticated parser, linked back to original emission ordinals and body spans, and hash-checked before and after. Production replay has zero differences from the stored template/status outcomes and native review no_match routes. The immutable database backup, review files and production selection/catalogs remain unchanged. No candidate ingestion, model activation or runtime-process restart occurred.</p>')
    overlap=sum(r['in_candidate_training'] for r in c['runs'])
    bits.append(f'<p>{overlap} evaluation Runs are in candidate training; {len(c["runs"])-overlap} are outside the exact training input set. This is an operational coverage comparison, not an independently commissioned holdout or an accuracy claim. Templates lacking selected predecessor witnesses require separate raw-evidence review; lack of a selected witness does not establish that a removal is bad or that no supporting raw message exists. See the owner corrections for reviewed exceptions.</p>')
    bits.append('<details><summary>Per-Run production/candidate counts and transitions</summary>'+pre(json.dumps(c['runs'],indent=2))+'</details>')
    bits.append('<h3>Package identities</h3>'+pre(json.dumps(dict(production=c['production'],candidate=c['candidate']),indent=2)))
    if (out/'training-corpus-comparison.json').exists():
        corpus=read(out/'training-corpus-comparison.json')
        corpus_edges=defaultdict(list)
        for edge in corpus['edges']:
            if edge['before']:corpus_edges[edge['before']].append(edge)
        categories=Counter()
        for identifier in c['removed']:
            edges=corpus_edges[identifier]
            category=('not_observed' if not edges else 'has_lost_matches' if any(e['after'] is None for e in edges) else
                      'has_status_downgrades' if any(e['before_status']=='template' and e['after_status']=='provisional' for e in edges) else
                      'covered_by_replacements')
            categories[category]+=1
        save(out/'removed-training-coverage.json',dict(scope=corpus['scope'],categories=categories,
            definitions={identifier:corpus_edges[identifier] for identifier in c['removed']}))
        bits.append('<h2>Broader check: all 73 training logs</h2><p>The preceding samples and counts compare the same 20 stored Runs. This separate check applies production to all '+fmt(corpus['contextual_messages'])+' distinct contextual messages in the shared training corpus and compares with the independently replayed candidate assignments. Repeated occurrences total '+fmt(sum(corpus['counts']['candidate'].values()))+'. This is training coverage, not independent accuracy.</p>'+
                    pre(json.dumps(dict(counts=corpus['counts'],transitions=corpus['transitions'],removed_template_categories=categories),indent=2))+
                    '<p><a href="training-corpus-comparison.json">Complete training-corpus comparison</a> · <a href="removed-training-coverage.json">Each removed template’s observed successors</a></p>')
    if (out/'regression-investigation.json').exists():
        investigation=read(out/'regression-investigation.json')
        bits.append('<h2>Why support regressions occurred in the training corpus</h2><p>'+esc(investigation['conclusion'])+'</p>')
        if investigation.get('operational_loss'):
            loss=investigation['operational_loss']
            bits.append('<h3>The lost assignment in the stored Runs</h3><p>'+esc(loss['run_id'])+' · stored record '+str(loss['ordinal'])+' · one occurrence.</p><p>'+esc(loss['explanation'])+'</p><p>'+str(loss['source_applicable_candidates'])+' source-applicable candidates were checked, including '+str(loss['family_candidates'])+' in this message family: zero complete matches and zero ambiguous-capture candidates. The exact message is absent from training.</p>'+pre(loss['native']))
        for finding in investigation['findings']:
            explanation=finding['explanation'].replace('definitions','templates').replace('definition','template')
            bits.append('<h3>'+esc(finding['title'])+'</h3><p>'+esc(explanation)+'</p>')
            for example in finding['examples']:
                bits.append('<details><summary>Genuine example and refinement history</summary>'+pre(example['example'])+pre(json.dumps(example['history'],indent=2))+'</details>')
        bits.append('<p><strong>Attribution limit.</strong> '+esc(investigation['attribution_limit'])+'</p><p><strong>Focused next step.</strong> '+esc(investigation['recommended_next_step'])+'</p><p><a href="regression-investigation.json">Detailed findings</a> · <a href="training-downgrade-lineage.json">Every downgraded training form and its actual refinement history</a></p>')
    if (out/'history-storage-verification.json').exists():
        storage=read(out/'history-storage-verification.json')
        bits.append('<h2>Research build storage correction</h2><p>Children now record local refinement decisions and parent references. The large rejected-field observation is stored once. Streamed writing and revision hashing avoid whole-file serialization buffers; the writer validates without reloading another model.</p>'+pre(json.dumps(storage,indent=2)))
    if (out/'verification.json').exists() and (out/'all-short-identities.json').exists():
        checked=read(out/'verification.json');characters=read(out/'all-short-identities.json')
        bits.append('<h3>Owner-directed checks</h3><p>'+str(len(checked['targets']))+' original IS3QON diagnostics were exercised through the pipeline classifier. The genuine one-, two- and three-entry location witnesses, wrapper/continuation behavior and the '+str(characters['messages'])+' short-character travel examples were checked separately.</p>'+
                    '<p><a href="RESULTS.html">Original diagnostics, location identity and continuation checks</a> · <a href="all-short-identities.json">All short-character/date/name captures</a></p>')
    if (out/'build-completion.json').exists():
        elapsed=read(out/'build-completion.json')['seconds']
        bits.append(f'<p>Fresh candidate learning and bundle creation took {elapsed/60:.1f} minutes; export and evaluation are separate. The large localization regrouping pass is a remaining build-performance concern.</p>')
    if (out/'training-parity.json').exists():
        bits.append('<p><a href="training-parity.json">Exact training-file hashes and per-log recovery comparison</a> · <a href="build-output.txt">Build output</a> · <a href="publish-execution.json">Authenticated export execution</a></p>')
    recovery=out/'recovered-release/completion.json'
    if recovery.exists():
        proof=read(out/'recovered-release/projection-provenance.json');validation=read(recovery)['validation']
        bits.append('<h3>Build and export recovery</h3><p>The frozen learner completed inference and wrote the research bundle, but its whole-file reload exceeded 56 GB private memory and was stopped. The original research artifact remains intact. '+
                    f'Its {proof["input_bytes"]:,} bytes include {proof["removed_bytes"].get("inference_refinements",0):,} bytes of inference-refinement history. '+
                    'A bounded-memory reader projected only the fields consumed by the unchanged owner compactor, authenticated every source payload, and verified the source learner bytes. '+
                    'The same adapter reproduced the previously published 20-log model exactly. The recovered compact release passed full native export parity before the unchanged frozen publisher packaged it through its existing source-release operation. No inference or matching rules changed.</p>'+
                    pre(json.dumps(validation,indent=2))+
                    '<p>The interrupted learn operation has no completed execution receipt; the written candidate manifest, full payload hashes, recovery provenance, complete native parity and completed publication receipt are retained. This memory problem remains an engineering limitation of normal fresh builds.</p>'+
                    '<p><a href="recovered-release/projection-provenance.json">Recovery provenance</a> · <a href="recovered-release/completion.json">Full export parity</a> · <a href="recovery-control-check.json">Exact 20-log control comparison</a> · <a href="model-section-sizes.json">Research artifact size inventory</a></p>')
    implementation_page='FIXES.html' if (out/'FIXES.html').exists() else '../super-short-character-candidate/CHANGES.html'
    bits.append('<p><a href="executive-summary.json">Executive summary data</a> · <a href="comparison.json">Full comparison, crosswalk and removed inventory</a> · <a href="messages.json">Every distinct message and complete assignments</a> · <a href="review-samples.json">Exact sample selections</a> · <a href="stored-evidence.json">Retained database snapshot provenance</a> · <a href="'+implementation_page+'">Candidate implementation details</a></p>')
    if (out/'report-verification.json').exists():
        bits.append('<p><a href="report-verification.json">Report verification, including rendering status</a>.</p>')
    bits.append('</html>')
    (out/'CHANGES.html').write_text('\n'.join(bits),encoding='utf-8',newline='')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
