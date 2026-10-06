"""Report the isolated threshold experiment and the current owner review items."""
import argparse
from collections import Counter
from html import escape
import json
from os.path import relpath
from pathlib import Path

from template_learning.evidence_serialization import write_json
from template_learning.records import identity
from template_learning.review_short_thresholds import record


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--experiment',type=Path,required=True)
    p.add_argument('--candidate-review',type=Path,required=True)
    a=p.parse_args(); root=a.experiment
    read=lambda path:json.loads(path.read_bytes())
    scope=read(root/'scope.json'); runs={k:read(root/(k+'.json')) for k in ('fixed','gentle','lower')}
    base={t['template_id']:t for t in runs['fixed']['templates']}
    assert len(base)==len(runs['fixed']['templates'])
    members={m:t for t in base.values() for m in t['members']}
    assert len(members)==sum(len(t['members']) for t in base.values())==scope['underlying_short_messages']
    results={}
    for name in ('gentle','lower'):
        data=runs[name]; templates={t['template_id']:t for t in data['templates']}
        new_members={m:t for t in templates.values() for m in t['members']}
        assert set(new_members)==set(members)
        assert len(new_members)==sum(len(t['members']) for t in templates.values())
        edges={}
        for key,before in members.items():
            after=new_members[key]
            if before['template_id']==after['template_id']:continue
            edge=edges.setdefault((before['template_id'],after['template_id']),dict(
                source=before['source'],before=before['template_id'],after=after['template_id'],
                before_pattern=before['display'],after_pattern=after['display'],messages=0,
                before_slots=before['slots'],after_slots=after['slots'],examples=[],record_ids=[]))
            edge['messages']+=1
            edge['record_ids'].append(key)
        results[name]=dict(templates=len(templates), added=sorted(templates.keys()-base.keys()),
            removed=sorted(base.keys()-templates.keys()), changed_messages=sum(e['messages'] for e in edges.values()),
            newly_admitted_comparisons=len(data['newly_admitted']),edges=list(edges.values()),
            rerun_sources=sorted({t['source'] for t in templates.values()}-set(data['reused_sources'])),
            reused_sources=data['reused_sources'])
    wanted={key for result in results.values() for e in result['edges'] for key in e['record_ids']}
    witnesses={}
    with (root/'short-records.jsonl').open(encoding='utf-8') as f:
        for line in f:
            row=json.loads(line)['row']; key=identity(record(row).key)
            if key in wanted:witnesses[key]=dict(text=row['native'],record_id=key,provenance=row['native_occurrences'])
    assert set(witnesses)==wanted
    for result in results.values():
        for e in result['edges']:
            e['examples']=[witnesses[key] for key in e['record_ids'][:3]]
    write_json(root/'comparison.json',dict(scope=scope,baseline_templates=len(base),results=results))
    pre=lambda s:'<pre>'+escape(str(s))+'</pre>'
    h=['<!doctype html><html><head><meta charset="utf-8"><title>Owner review and threshold experiment</title>',
       '<style>body{font:17px/1.5 system-ui;max-width:1100px;margin:40px auto;padding:0 24px;color:#192c3b}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;padding:18px}td,th{border:1px solid #ccd4db;padding:10px;text-align:left}table{border-collapse:collapse}article{border-top:1px solid #ccc;margin-top:30px}h1,h2{line-height:1.2}</style></head><body>',
       '<h1>Owner review: open objections and measured experiments</h1>',
       '<p><b>Assessment:</b> history implementation remains disputed; untyped applicability is explained. The seven removed alternatives have now been explained at family level: production and v57 already select the same generalized patterns and captures for all their messages. They are not a queue for individual template approval. Sliding thresholds simplify initial discovery, but the actual production and v57 packages already classify all 15 affected messages using the same whole-expression PARAM template. This test therefore demonstrates no improvement to current selected classifications and does not justify changing the production threshold.</p>',
       '<h2>History wording: implementation rejected, not approved</h2>',
       '<p>The v57 candidate removed the phrase PARAM and hard-coded two separate constructions for “after death birth” and “from before birth”. That produces literal wording, but successful checks do not establish approval of the mechanism. The owner has rejected this implementation. It has not been revised again while clarification is pending. The separate Parent-state PARAM is unchanged.</p>',
       '<h2>Variable similarity: executed experiment</h2>',
       f'<p>Scanned all {scope["counts"]["contextual_rows"]:,} contextual rows from the same 73 logs. Tested {scope["underlying_short_messages"]:,} distinct underlying messages with at most eight non-quoted-value comparison units. These represent {scope["counts"]["short_occurrences"]:,} occurrences. A recognized field contributes one unit; repeated ending locators contribute one; quoted value contents earn no similarity credit.</p>',
       '<p>This is an isolated initial-discovery and refinement experiment, not a published model, incremental build, or runtime coverage claim. Each policy uses identical messages, code and rules. Ordered similarity, inference, applicability boundaries and wording-loss guards are unchanged. Every member must completely match its inferred body pattern. Existing ≤2-unit special handling is retained. Runtime complete matching has no sliding threshold.</p>',
       '<p><b>The existing short-message rule was retained in every arm:</b> equal-length sequences of one or two comparison units, with no quoted-value position, require at least one equal unit in the same position and a shared-position fraction ≥0.49. Thus one of two positions agreeing qualifies. This is a separate positional test, not a 0.49 cutoff on the weighted similarity score. The quoted-value branch bypasses that special case; unequal lengths also use the weighted score.</p>',
       '<table><tr><th>Comparison length (longer side)</th><th>Existing policy</th><th>Gentle trial</th><th>Lower trial</th></tr>',
       '<tr><td>Equal lengths ≤2, no quoted-value position</td><td>Existing ≥0.49 positional fraction</td><td>Unchanged</td><td>Unchanged</td></tr>',
       '<tr><td>Other comparisons with length ≤2</td><td>0.72 weighted score</td><td>Unchanged</td><td>Unchanged</td></tr>']
    for n in (3,4,5,6,7,8):h.append(f'<tr><td>{n}</td><td>0.72</td><td>{runs["gentle"]["thresholds"].get(str(n),.72):.2f}</td><td>{runs["lower"]["thresholds"].get(str(n),.72):.2f}</td></tr>')
    h.append('</table><p>The experimental length is the longer sequence after excluding quoted-value placeholders; values inside recognized fields are not counted as words. These are two experimental curves, not an owner-prescribed or calibrated optimum. All other lengths retain 0.72. The baseline records every comparison: source pools with no changed admission decision are reused; affected source pools run all discovery/refinement steps afresh. Anchor-based proposal retrieval and construction boundaries remain fixed: this tests threshold changes on existing proposal paths, not a new search strategy.</p>')
    h.append(f'<p>Fixed experiment: {len(base)} inferred templates. These counts belong to the short-message experiment and must not be compared with the complete production/candidate template counts.</p>')
    h.append('<p><b>Observed result:</b> both curves consolidate 15 messages into the already inferred whole-expression PARAM template, <code>Failed converting statement for &apos;&lt;PARAM&gt;&apos;</code>. Fourteen previously had KEY/PARAM/KEY expression fragments; one retained its complete expression literally. The outer diagnostic words remain literal. This is a positive field-boundary change in this experiment, not evidence of additional runtime coverage.</p>')
    h.append('<p>The decisive initial comparison scored 0.713333, below 0.72 but above the gentle five-unit threshold of 0.70. One side had the four diagnostic words plus a quoted-value position; the other had those four words plus And, with the surrounding balanced expression treated differently by discovery. The lower curve also admitted an audio stop/check-isPlaying pair at 0.6725; later inference kept its two formulations separate. It produced no further final change. If taken to a complete candidate experiment, prefer the gentler curve; there is no demonstrated benefit to the lower curve here.</p>')
    runtime=read(root/'changed-message-runtime-check.json')
    assert len(runtime)==15 and all(r[k]['status']=='template' and r[k]['pattern'].strip()=="Failed converting statement for '<PARAM>'" for r in runtime for k in ('production','candidate'))
    h.append('<p><b>Actual package check:</b> production 68f1ae5db205ab46afef9c4d and candidate 53c4fdd5e5d0265714016450 already select the whole-expression PARAM template as a supported template for every one of these 15 messages. No coverage or selected-template improvement has been demonstrated. <a href="changed-message-runtime-check.json">All 15 exact runtime comparisons</a>.</p>')
    for name,result in results.items():
        h.append('<h3>'+name.title()+'</h3><p>'+escape(f'{result["templates"]} templates; {len(result["added"])} added, {len(result["removed"])} removed; {result["changed_messages"]} messages change inferred template; {result["newly_admitted_comparisons"]} distinct extra comparisons admitted.')+'</p>')
        for e in result['edges']:
            h.extend(['<article><b>'+escape(e['source'])+f' · {e["messages"]} messages</b><p>Fixed:</p>',pre(e['before_pattern']),'<p>Variable:</p>',pre(e['after_pattern'])])
            for x in e['examples']:h.append('<details><summary>Genuine member</summary>'+pre(x['text'])+'</details>')
            h.append('</article>')
    h.append('<p>Limits: short-message subset, initial discovery rather than the full incremental schedule; body-pattern coverage, not selected complete assignments with wrappers/continuations. No production pin or runtime behavior has changed. Hard construction boundaries—including the disputed history separation—are not affected by lowering similarity.</p><p><a href="comparison.json">Machine-readable results</a></p>')
    untyped=read(a.candidate_review/'untyped-applicability-review.json')
    h.extend(['<h2>Why untyped has its own construction</h2>',
        '<p>The declaration records owner authority dated 2026-09-27 for the complete formulation with opaque bracketed REASON. The dedicated untyped-trigger rule recognizes the plain header exactly. The generic script-system-reason rule explicitly excludes messages recognized by that dedicated rule. Thus the plain message has only the dedicated complete candidate; literal specificity does not decide a competition.</p>',
        '<p>The tooltip/description header is a different path: the exact dedicated rule does not recognize it, so the generic trigger template can capture untyped as KEY. This distinction remains pending owner review; it is not evidence that untyped must universally be literal.</p>'])
    for form,e in untyped.items():
        h.append('<h3>'+escape(form)+'</h3>'+pre(e['native'])+'<table><tr><th>Template</th><th>Applicable</th><th>Complete</th></tr>')
        for t in e['templates']:h.append('<tr><td>'+pre(t['pattern'])+escape(t['id'])+'</td><td>'+str(t['applicable'])+'</td><td>'+str(t['complete'])+'</td></tr>')
        h.append('</table>')
    families=read(a.candidate_review/'removal-family-summary.json')
    h.extend(['<h2>Seven removed alternatives: family-level explanation</h2>',
        '<p>The prior per-template report was misleading. Five overlapping Missing-loc-for-name alternatives repeated the same witnesses under different compatibility totals. They were not five separate classification failures. All 630 name messages / 1,116 occurrences already select the same supported whole-name template in both production and v57.</p>',
        '<p>The scope-dependent localization family has five messages / 180,998 occurrences. The GUI parsing family has 41 messages / 63 occurrences, with 35 distinct statement values. Both models already select identical generalized template wording and captures across all these messages. These removals simplify redundant alternatives; no individual template approval is requested.</p>',
        '<p><a href="'+escape(Path(relpath(a.candidate_review/'REMAINING-REMOVALS.html',root)).as_posix())+'">Corrected family report, count explanation and twelve GUI variations</a></p>'])
    assert all(not f['changed_captures'] for f in families.values())
    h.append('</body></html>')
    (root/'REVIEW.html').write_text('\n'.join(h),encoding='utf-8')
    print(json.dumps({name:{k:v for k,v in result.items() if k not in ('edges','reused_sources')} for name,result in results.items()},indent=2))


if __name__=='__main__':main()
