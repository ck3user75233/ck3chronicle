"""Explain removed templates at family level using actual package assignments.

Direct applicability is deliberately distinguished from production selection.
All matching uses each immutable package's own authenticated matcher.
The owner reviews learner behavior, not individual template promotion decisions.
"""
import argparse
from collections import Counter, defaultdict
from html import escape
import json
from pathlib import Path

from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.matcher_example import load_verified
from template_learning.inventory import sha256_file
from template_learning.review_short_thresholds import record


def review_category(t):
    text=t['display']; source=t['source_family']
    if source=='pdx_locstring.cpp' and 'Key is missing localization:' in text:
        return 'addressed', 'Whole missing-localization value: owner-directed name-field correction; Ymerodraeth removal explicitly accepted.'
    if 'Starting travel with incorrect receiver' in text:
        return 'addressed', 'Owner-directed date equivalence, character identities and complete default-location field.'
    if 'house.house_head trigger [' in text:
        return 'addressed', 'Accepted trigger-name KEY and variable-count location tail.'
    if "No previous holders for '" in text:
        return 'addressed', 'Accepted whole quoted title PARAM (owner review 13).'
    if "Event target link 'scope' returned an unset scope" in text:
        return 'addressed', 'Accepted quoted event-target KEY (owner review 4).'
    return 'review', 'Family-level learner behavior not explained in the earlier report; not an individual template approval request.'


def family(source,text):
    if source=='characterhistory.cpp' and text.lstrip().startswith('Missing loc for name '):return 'missing_name'
    if source=='jomini_trigger_description.cpp' and 'Scope dependent values in localization inside an any trigger' in text:return 'scope_localization'
    if source=='pdx_gui_factory.cpp' and 'Failed parsing data statement ' in text:return 'gui_statement'
    return None


def template_summary(t):
    return {k:t[k] for k in ('template_id','source_family','display','status','selection_evidence')}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--evidence',type=Path,required=True)
    p.add_argument('--bundle',type=Path,required=True)
    p.add_argument('--production',type=Path,required=True)
    p.add_argument('--candidate',type=Path,required=True)
    p.add_argument('--render-only',action='store_true')
    a=p.parse_args()
    if a.render_only:
        render(a.evidence,json.loads((a.evidence/'unselected-removals-review.json').read_bytes()),
               json.loads((a.evidence/'removal-family-evidence.json').read_bytes()))
        return
    analysis=json.loads((a.evidence/'removed-template-analysis.json').read_bytes())
    ids=analysis['summary']['unobserved_removed']
    old=load_verified(a.production,sha256_file(a.production/'manifest.json'))
    new=load_verified(a.candidate,sha256_file(a.candidate/'manifest.json'))
    templates={t['template_id']:t for t in old.data['templates']}
    targets={}; by_source=defaultdict(list);families=defaultdict(list)
    for key in ids:
        t=templates[key]; status,reason=review_category(t)
        targets[key]=dict(template_id=key, source=t['source_family'], production_pattern=t['display'],
            production_template_status=t['status'], matching_example_ids=[],
            review_status=status, rationale=reason, direct_matching_messages=0, direct_matching_occurrences=0,
            successors={}, examples=[])
        by_source[t['source_family']].append(t)
    for i,(row,count) in enumerate(native_evidence_rows(a.bundle/'native_evidence.json'),1):
        if row['source_family'] not in by_source: continue
        r=record(row)
        matching=[t for t in by_source[r.source_family] if old.matcher.rules.match_record(t,r) is not None]
        category=family(r.source_family,r.text)
        if not matching and not category: continue
        unit=dict(parser=new.manifest['parser'],source_family=r.source_family,source_tag=r.source_family,
            context_kind=r.context_kind,body=dict(text=r.text,pieces=r.pieces),
            contexts=next(iter(r.contexts.values()),{}),continuations=r.continuations)
        chosen=new.match(unit)['assignment']
        if category:
            prior=old.match({**unit,'parser':old.manifest['parser']})['assignment']
            families[category].append(dict(example_id=row['example_id'],record_id=row['record_id'],
                text=r.text,contexts=r.contexts,continuations=r.continuations,occurrences=count,
                provenance=row['native_occurrences'],old_matching_removed_templates=[t['template_id'] for t in matching],
                production_assignment=prior,candidate_assignment=chosen))
        successor=chosen['template_id'] if chosen else 'no_match'
        for t in matching:
            result=targets[t['template_id']]
            result['direct_matching_messages']+=1;result['direct_matching_occurrences']+=count
            result['matching_example_ids'].append(row['example_id'])
            bucket=result['successors'].setdefault(successor,dict(messages=0,occurrences=0,
                status=new.matcher.by_id[successor]['status'] if chosen else None,
                pattern=new.matcher.by_id[successor]['display'] if chosen else None))
            bucket['messages']+=1;bucket['occurrences']+=count
            if len(result['examples'])<2:
                result['examples'].append(dict(example_id=row['example_id'],text=r.text,
                    provenance=row['native_occurrences'],candidate_assignment=chosen))
        if i%10000==0: print('Checked',i,flush=True)
    counts=Counter(v['review_status'] for v in targets.values())
    result=dict(scope='Direct complete applicability over all retained 73-log contextual messages; these production templates were not selected in either prior comparison.',
        production_package=old.manifest['package_id'],candidate_package=new.manifest['package_id'],
        counts=counts, templates=list(targets.values()))
    write_json(a.evidence/'unselected-removals-review.json',result)
    details=dict(families=dict(families),templates={label:[template_summary(t) for t in package.data['templates']
        if family(t['source_family'],t['display'])] for label,package in [('production',old),('candidate',new)]})
    write_json(a.evidence/'removal-family-evidence.json',details)
    render(a.evidence,result,details)
    print(json.dumps(dict(counts=counts,families={k:dict(messages=len(v),occurrences=sum(r['occurrences'] for r in v)) for k,v in families.items()}),indent=2))


def render(root,result,details):
    templates={label:{t['template_id']:t for t in values} for label,values in details['templates'].items()}
    pre=lambda text:'<pre>'+escape(text)+'</pre>'
    h=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Learner outcomes: three message families</title>',
       '<style>body{font:17px system-ui;max-width:1150px;margin:40px auto;line-height:1.55;padding:0 24px;color:#193045}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;padding:16px}article{border-top:1px solid #ccc;margin-top:30px}td,th{padding:10px;border-bottom:1px solid #ccc;text-align:left;vertical-align:top}table{border-collapse:collapse;width:100%}.note{background:#fff3dc;padding:18px}.consolidation{border:2px solid #8ca7b8;padding:20px;margin:20px 0}.replacement{border-top:2px solid #8ca7b8;margin-top:24px;padding-top:12px}summary{cursor:pointer}</style>',
       '<h1>Learner outcomes: three message families</h1>',
       '<p class="note"><b>Correction to the previous report:</b> this is an analysis of learner behavior, not a queue for the owner to approve individual templates. The previous page repeated overlapping old templates and reused witnesses, obscuring the actual selected results. “Candidate” means the disposable v57 model, package '+result['candidate_package']+'. Every displayed main template is already learner-designated <b>supported</b>, not provisional or rejected.</p>',
       '<p><b>Finding:</b> production and v57 select the same template wording, slot types, values and spans for every message in these three families. The seven removed IDs were unused alternatives, not seven classification failures. Removing them simplifies the catalog. There is no demonstrated message-identity or occurrence-count defect here.</p>',
       '<p>Scope: all matching families in the same 73-log native evidence, evaluated with each immutable package’s own matcher. Source logs and stored Runs were not changed. Counts below are distinct complete messages and total occurrences. Per-alternative compatibility counts overlap and must not be added.</p>',
       '<table><tr><th>Family</th><th>Distinct messages</th><th>Occurrences</th><th>Selected status, both models</th></tr>']
    labels=dict(missing_name='Missing loc for name',scope_localization='Scope-dependent localization',gui_statement='Failed parsing data statement')
    summaries={}
    for key in labels:
        rows=details['families'][key]
        assert len({r['example_id'] for r in rows})==len(rows)==len({r['text'] for r in rows})
        changed=[]
        for r in rows:
            old,new=(r[label+'_assignment'] for label in ('production','candidate'))
            assert old and new and old['match_status']==new['match_status']=='template'
            captures=lambda a:[(region['name'],c['type'],c['present'],c['span'],c['value']) for region in a['regions'] for c in region['captures']]
            if captures(old)!=captures(new):changed.append(r['example_id'])
            assert templates['production'][old['template_id']]['display']==templates['candidate'][new['template_id']]['display']
        assert not changed
        summary=dict(messages=len(rows),occurrences=sum(r['occurrences'] for r in rows),changed_captures=changed)
        summaries[key]=summary
        h.append(f'<tr><td>{labels[key]}</td><td>{summary["messages"]:,}</td><td>{summary["occurrences"]:,}</td><td>template / supported</td></tr>')
    h.append('</table>')
    for key,label in labels.items():
        rows=details['families'][key]
        chosen={r['candidate_assignment']['template_id'] for r in rows};assert len(chosen)==1
        tid=next(iter(chosen));t=templates['candidate'][tid]
        old_ids={r['production_assignment']['template_id'] for r in rows}
        predecessors=[r for r in result['templates'] if tid in r['successors']]
        assert predecessors and all(set(r['successors'])=={tid} for r in predecessors)
        summaries[key]['consolidation']=dict(removed_template_ids=[r['template_id'] for r in predecessors],replacement_template_id=tid)
        h.extend(['<article id="'+key+'"><h2>'+label+'</h2>',
            '<section class="consolidation" data-successor="'+tid+'"><h3>'+str(len(predecessors))+' removed production template'+('s' if len(predecessors)!=1 else '')+' → 1 replacement</h3>',
            '<p>All removed templates in this consolidation are shown below. They share the single replacement that follows.</p><ol>'])
        for r in predecessors:
            h.append('<li data-predecessor="'+r['template_id']+'">'+pre(r['production_pattern'])+'<small>'+r['template_id']+' · '+r['production_template_status']+'</small></li>')
        h.extend(['</ol><div class="replacement" data-role="replacement"><h3>One replacement in the candidate model</h3>',pre(t['display']),
            '<p>'+tid+' · learner status: <b>'+t['status']+'</b> · assignment status: <b>template</b>.</p></div></section>',
            '<p>This general pattern was already selected in production too (ID '+', '.join(sorted(old_ids))+'). The candidate retains its coverage while removing the alternatives above. This is one consolidation, not separate problems for each old template.</p>'])
        stored=[v for v in templates['candidate'].values() if family(v['source_family'],v['display'])==key and v['template_id']!=tid]
        if key=='missing_name':
            h.append('<p><b>These already form one selected group:</b> all 630 messages / 1,116 occurrences select template 5093f36599ce2356a1e6433e in both models. It captures 574 distinct complete names and 630 character identifiers. The old report compared five narrower, overlapping alternatives with this existing general template. It did not show production’s actual choice.</p>')
            old=predecessors
            sets={r['template_id']:set(r['matching_example_ids']) for r in old}
            union=set().union(*sets.values());common=set.intersection(*sets.values())
            assert len(union)==572 and len(common)==53
            h.append('<h3>Why the five counts differed</h3><p>Each row counted <em>all messages compatible with that old pattern</em>, not occurrences of its displayed witness and not selected assignments. All five totals overlap. Their union is 572 messages / 1,030 occurrences; 53 messages / 133 occurrences fit all five. The remaining 58 family messages fit none of these five alternatives, but still select the general template.</p><table><tr><th>Removed template, numbered above</th><th>Compatible messages</th><th>Compatible occurrences</th><th>Selected occurrences</th></tr>')
            for number,r in enumerate(old,1):
                assert not any(x['production_assignment']['template_id']==r['template_id'] for x in rows)
                h.append('<tr><td>'+str(number)+'. <small>'+r['template_id']+'</small></td><td>'+str(r['direct_matching_messages'])+'</td><td>'+str(r['direct_matching_occurrences'])+'</td><td>0</td></tr>')
            h.append('</table>')
            witness=next(r for r in rows if "name 'Abd al-Aziz'" in r['text'])
            assert len(witness['old_matching_removed_templates'])==5 and witness['occurrences']==3
            h.extend(['<h3>One exact message, repeated misleadingly in the previous report</h3>',pre(witness['text']),
                '<p>This exact message occurs <b>3 times</b>, has one evidence identity, and fits all five old alternatives. Both models select the same whole-name template. Production considered six complete alternatives and selected by its evidence ranking; v57 has one complete candidate for this message. The report duplicated the witness across its old-template rows; the learner did not create five separate message identities.</p>',
                '<p>Concrete boundary differences explain the totals: <code>Noriko </code> (trailing space) fits the optional-second-KEY form but not the mandatory two-KEY form. Twenty-one two-word-name messages have nonnumeric character identifiers, such as <code>1211Unlanded3</code>; they fit the character KEY form but not the VALUE form.</p>'])
        elif key=='scope_localization':
            h.append('<p>The evidence contains four leading identifiers: <code>character_this_equal</code>, <code>house_equal</code>, <code>is_attacker</code>, and <code>is_defender</code>. Both models already select the generalized KEY template. The removed house_equal-only template was an unused alternative. No per-template approval or demonstrated classification repair is outstanding.</p>')
            for r in rows:h.append(pre(r['text'])+f'<p>{r["occurrences"]:,} occurrences.</p>')
        else:
            values=defaultdict(lambda:dict(messages=0,occurrences=0));properties=set()
            for r in rows:
                caps=r['candidate_assignment']['regions'][0]['captures']
                value=next(c['value'] for c in caps if c['slot_id']=='s2');properties.add(next(c['value'] for c in caps if c['slot_id']=='s3'))
                values[value]['messages']+=1;values[value]['occurrences']+=r['occurrences']
            assert len(values)==35 and len(properties)==7
            h.append('<p><b>Not a singleton:</b> 41 distinct complete messages / 63 occurrences contain <b>35 different statement values</b> and seven property values. The previous page showed only the one message compatible with a removed literal alternative. Both production and v57 already select the whole-statement PARAM template on all 41 messages. The evidence supports a reusable field, including nested calls and quotes; it does not prove every future expression is covered.</p>')
            # Show diversity, not repeated copies of one expression at new lines.
            samples=[];seen_values=set();seen_properties=set()
            for r in rows:
                caps={c['slot_id']:c['value'] for c in r['candidate_assignment']['regions'][0]['captures']}
                if caps['s3'] not in seen_properties:
                    samples.append(r);seen_properties.add(caps['s3']);seen_values.add(caps['s2'])
            for r in sorted(rows,key=lambda r:-len(r['text'])):
                value=next(c['value'] for c in r['candidate_assignment']['regions'][0]['captures'] if c['slot_id']=='s2')
                if value not in seen_values and len(samples)<12:samples.append(r);seen_values.add(value)
            h.append('<h3>Twelve genuine variations</h3>')
            for r in samples:h.append(pre(r['text'])+f'<p>{r["occurrences"]} occurrences; selected as supported template.</p>')
            h.append('<details><summary>All 35 exact PARAM values and counts</summary><table><tr><th>Statement PARAM</th><th>Messages</th><th>Occurrences</th></tr>')
            for value,c in sorted(values.items()):h.append('<tr><td>'+pre(value)+'</td><td>'+str(c['messages'])+'</td><td>'+str(c['occurrences'])+'</td></tr>')
            h.append('</table></details>')
            summaries[key]['distinct_statement_values']=len(values);summaries[key]['distinct_properties']=len(properties)
        if stored:
            h.append('<details><summary>Catalog redundancy still present: '+str(len(stored))+' other v57 templates; none selected for this family’s messages</summary><p>These are actual learner outputs, not proposals awaiting owner approval. Their existence is a separate model-minimization question, not evidence of duplicate stored messages. Removing them safely requires a reusable containment/retirement rule, not deleting every template without selected witnesses in a finite corpus.</p>')
            for extra in stored:h.append('<p>'+extra['template_id']+' · '+extra['status']+'</p>'+pre(extra['display']))
            h.append('</details>')
        h.append('</article>')
    h.append('<h2>Code changes and remaining engineering questions</h2><p>The review tool now groups by message family, shows actual selected production/v57 assignments and status, checks exact capture equality, and labels overlapping alternative counts explicitly. It expands examples across the whole family instead of restricting them to one removed template. No learner/matcher behavior or production package changed for this correction. A general catalog-retirement improvement would require separate proof of preserved matching behavior; these observations alone do not justify deleting unselected templates.</p><p><a href="removal-family-evidence.json">Complete family evidence, statuses, assignments and provenance</a> · <a href="removal-family-summary.json">Verified family summary</a> · <a href="unselected-removals-review.json">Full 38-template compatibility crosswalk</a> · <a href="CHANGES.html">Production comparison</a></p></html>')
    write_json(root/'removal-family-summary.json',summaries)
    (root/'REMAINING-REMOVALS.html').write_text('\n'.join(h),encoding='utf-8')


if __name__=='__main__':main()
