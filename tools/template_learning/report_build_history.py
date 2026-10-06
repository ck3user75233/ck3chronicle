"""Report production, fresh and mirrored incremental results on genuine evidence."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path

from template_learning.evidence_serialization import write_json


def read(path):
    return json.loads(path.read_bytes())


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--fresh-evidence', type=Path, required=True)
    cli.add_argument('--incremental-evidence', type=Path, required=True)
    cli.add_argument('--production', type=Path, required=True)
    args = cli.parse_args(); fresh = args.fresh_evidence; out = args.incremental_evidence
    cf, ci = read(fresh/'comparison.json'), read(out/'comparison.json')
    source = read(out/'build-history-training-summary.json')
    fresh_messages = {r['key']:r for r in read(fresh/'messages.json')}
    incremental_messages = {r['key']:r for r in read(out/'messages.json')}
    assert fresh_messages.keys() == incremental_messages.keys()
    trans = Counter(); changed = []
    for key, before in fresh_messages.items():
        after = incremental_messages[key]
        assert (before['source'],before['context'],before['native_regions'],before['occurrences']) == (
            after['source'],after['context'],after['native_regions'],after['occurrences'])
        assert before['results']['production'] == after['results']['production']
        a,b = before['results']['candidate'],after['results']['candidate']
        sa,sb = a['status'] if a else 'no_match',b['status'] if b else 'no_match'
        trans[sa+' -> '+sb] += before['occurrences']
        if a!=b:
            changed.append(dict(key=key,source=after['source'],text=after['text'],references=after['references'],
                occurrences=after['occurrences'],before_status=sa,after_status=sb,
                before=a['values']['template_id'] if a else None,after=b['values']['template_id'] if b else None))
    fresh_folder = fresh/'packages'/cf['candidate']['package_id']
    incremental_folder = out/'packages'/ci['candidate']['package_id']
    models = {k:read(folder/'empirical_template_model.json') for k,folder in (
        ('production',args.production),('fresh',fresh_folder),('incremental',incremental_folder))}
    templates = {k:{t['template_id']:t for t in m['templates']} for k,m in models.items()}
    basis = read(out/'build-basis.json'); checkpoints = read(out/'results.json')
    assert models['fresh']['algorithm']['learner_identity'] == models['incremental']['algorithm']['learner_identity']
    assert models['incremental']['algorithm']['build_strategy']=='same-version-additive-v1'
    previous = None
    for row,point in zip(checkpoints,basis['schedule'],strict=True):
        assert row['logs'] == point['logs'] and row['parent_revision'] == previous
        if previous:
            assert row['update']['parent_revision'] == previous
        previous = row['revision_id']
    fresh_edges = read(out/'fresh-training-comparison.json')['edges']
    by_fresh = defaultdict(list)
    for edge in fresh_edges:
        if edge['before']:
            by_fresh[edge['before']].append(edge)
    cases = [
        (1,'Comparison between different types','accepted','4615f2f0dcb62b0f22c0be03'),
        (2,'Invalid comparison side','accepted','6a524415fb61b4b721f826be'),
        (3,'Trigger failures','accepted','acf0016a118519e25fc1557c'),
        (4,'Unset event target','accepted','852a56cf859d95ff606ca8ed'),
        (5,'Untyped trigger','pending coexistence explanation','4ac751de53c2454d5094602a'),
        (6,'Invalid province','location layout only','b24b502f0302fb6b1a460756'),
        (7,'Character history','rejected: phrase must be PARAM','796ad48a3e5e8f97332f4427'),
        (8,'Emblem category','accepted with sensitivity concern','766cfec88e63687b63c5123d'),
        (9,'Flag / Variable','accepted with sensitivity concern','f7a161abe24ee04e2cd78b76'),
        (10,'Unknown effect / trigger','rejected: category became KEY','afac2b20cf8aab9ca59f9a09'),
        (11,'Scope mismatch','improvement','0213bb363ad56f39d7e953a5'),
        (12,'Compare-trigger expected scope','improvement','fdf9618e529ed22940169dec'),
        (13,'Previous holders','improvement','240299ab8871f53c5e7d04c4'),
        (14,'Formatting tag','improvement','b9164abd4185f3558666bf47'),
    ]
    case_rows = []
    for number,title,assessment,identifier in cases:
        edges = by_fresh[identifier]
        assert edges
        targets = sorted({e['after'] for e in edges if e['after']})
        same_display = [i for i in targets if templates['incremental'][i]['display']==templates['fresh'][identifier]['display']]
        case_rows.append(dict(number=number,title=title,owner_assessment=assessment,fresh_template=identifier,
            incremental_templates=targets,identical_display_successors=same_display,edges=edges))
    result = dict(same_frozen_learner=True,same_recorded_schedule=True,same_73_log_corpus_previously_established=True,
        inventory={k:len(v) for k,v in templates.items()},
        stored_counts=dict(production=ci['counts']['production'],fresh=cf['counts']['candidate'],incremental=ci['counts']['candidate']),
        stored_fresh_to_incremental=trans,training=source,cases=case_rows,
        changed_stored_messages=changed,checkpoints=[{k:v for k,v in r.items() if k!='update'} for r in checkpoints])
    inspected={r['number']:[templates['incremental'][i]['display'] for i in r['incremental_templates']] for r in case_rows}
    history_literals=(len(inspected[7])==2 and any('has history after death birth' in p for p in inspected[7])
                      and any('has history from before birth' in p for p in inspected[7]))
    unknown_literals=(len(inspected[10])==2 and any('Unknown effect:' in p for p in inspected[10])
                      and any('Unknown trigger:' in p for p in inspected[10]))
    result['semantic_observations']=dict(character_history_retains_two_literal_phrases=history_literals,
        unknown_effect_trigger_retains_literal_categories=unknown_literals)
    lost_fresh=[r for r in changed if r['before_status'] in ('template','provisional') and r['after_status']=='no_match']
    lost_groups=defaultdict(list)
    for row in lost_fresh:
        lost_groups[row['before']].append(row)
    result['lost_fresh_coverage']=dict(messages=len(lost_fresh),occurrences=sum(r['occurrences'] for r in lost_fresh),
        families=[dict(template_id=i,messages=len(rows),occurrences=sum(r['occurrences'] for r in rows)) for i,rows in lost_groups.items()])
    write_json(out/'build-history-comparison.json',result)
    esc = lambda v:html.escape(str(v))
    pre = lambda v:'<pre>'+esc(v)+'</pre>'
    def show(label,identifier):
        if identifier is None:
            return '<p>No complete assignment.</p>'
        t=templates[label][identifier]
        return '<p class="meta">'+esc(label)+' · '+esc(t['status'])+' · '+identifier+'</p>'+pre(t['display'])
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Controlled incremental comparison</title>',
        '<style>body{font:16px/1.55 system-ui;max-width:1160px;margin:32px auto;padding:0 22px;color:#203746}pre{white-space:pre-wrap;overflow-wrap:anywhere;padding:14px;background:#eef4f7;max-height:400px;overflow:auto;font-size:13px}table{width:100%;border-collapse:collapse}td,th{padding:9px;text-align:left;border-bottom:1px solid #cbd6df;vertical-align:top;overflow-wrap:anywhere}a{color:#086093}.meta{color:#586b78;font-size:13px}.note{padding:18px;background:#eaf3fa}.review{padding:18px;background:#fff1d9}summary{cursor:pointer}article{margin:25px 0;border-top:2px solid #cbd6df}</style>',
        '<h1>Production versus fresh and incremental v54</h1>',
        '<p><a href="CHANGES.html">15 added / 15 removed / newly classified messages</a> · <a href="#cases">Owner-reviewed examples</a> · <a href="#scope">Controlled scope</a></p>',
        '<p class="note">The incremental candidate follows production’s recorded <strong>20 + 20 + 20 + 13</strong> input batches and SHA-256 inventory order. It uses the <strong>same frozen learner as the fresh candidate</strong>, with no inference or rule changes. It begins with fresh same-version state; no production templates were imported.</p>',
        '<h2>Template inventory and coverage</h2><table><tr><th>Measure</th><th>Production</th><th>Fresh v54</th><th>Incremental v54</th></tr>']
    if history_literals and unknown_literals:
        bits.insert(-1,'<h2>Executive assessment: mixed</h2><p class="review">Matching production’s incremental schedule avoids both rejected KEY patterns in the reviewed genuine cases. <strong>Unknown effect / trigger retain their literal categories.</strong> Character history retains two literal phrases, so the erroneous two-KEY result disappears, but the requested shared PARAM is still absent. Emblem and Flag/Variable categories also remain separate literals. Against production, complete coverage improves with no lost assignments in either evaluated scope. Against fresh v54, however, '+f'{result["lost_fresh_coverage"]["occurrences"]:,}'+' stored-Run occurrences across '+str(len(lost_fresh))+' messages lose assignments. This establishes build-history sensitivity under identical learner bytes; it does not yet establish the exact safeguard branch responsible. Fewer templates and higher coverage are insufficient promotion criteria.</p><p><strong>Next steps:</strong> trace the initial and revision decisions for examples 7–10 and the two lost-coverage families, complete the 73-log contextual KEY audit, then implement and verify reusable phrase handling without losing the accepted generalizations. Keep this controlled candidate and production unchanged during that work.</p>')
    bits.append('<tr><td>Error templates, including provisionals</td>'+''.join('<td>'+str(len(templates[k]))+'</td>' for k in models)+'</tr>')
    for status in ['template','provisional','no_match','unresolved_recovery']:
        bits.append('<tr><td>20 stored Runs: '+status+'</td>'+''.join('<td>'+f'{result["stored_counts"][k].get(status,0):,}'+'</td>' for k in models)+'</tr>')
    for status in ['template','provisional','no_match']:
        bits.append('<tr><td>73 training logs: '+status+'</td>'+''.join('<td>'+f'{source["counts"][k].get(status,0):,}'+'</td>' for k in models)+'</tr>')
    bits.append('</table><p>Provisionals are valid complete classifications. Training and stored-Run scopes overlap in message content and are not added together. Neither coverage nor template count measures semantic correctness.</p>')
    bits.append('<h2>What changes when only the build method changes?</h2>'+pre(json.dumps(dict(stored_runs=trans,training_logs=source['transitions']['fresh']),indent=2)))
    bits.append('<h3>Fresh assignments absent from the incremental candidate</h3><p>These were also unmatched in production. Counts below are from the same 20 stored Runs, not added to training-corpus counts. A tooltip-specific construction can differ from a superficially similar ordinary script error; the displayed native wording is retained here.</p>')
    for identifier,rows in sorted(lost_groups.items(),key=lambda item:-sum(r['occurrences'] for r in item[1])):
        bits.append(show('fresh',identifier)+'<p><strong>'+f'{sum(r["occurrences"] for r in rows):,}'+' occurrences / '+str(len(rows))+' messages:</strong> no complete incremental assignment.</p>')
        for row in rows:
            bits.append('<details><summary>'+str(row['occurrences'])+' occurrences · '+esc(row['references'][0]['run_id'])+'</summary>'+pre(row['text'])+'</details>')
    for case in (r for r in case_rows if r['number'] in (7,10)):
        wording = ('The same rejected displayed pattern is still selected for at least some genuine messages.' if case['identical_display_successors'] else
                   'The incremental build selects different patterns for the genuine messages assigned to the rejected fresh template; inspect them below before judging resolution.')
        bits.append('<p class="review"><strong>Example '+str(case['number'])+': '+esc(case['title'])+'.</strong> '+wording+'</p>')
    bits.append('<p><strong>Interpretation.</strong> Fresh-versus-incremental differences here arise under identical retained learner bytes and the same native corpus. Comparing incremental v54 with production controls the recorded input schedule, but it does not isolate any single code change; the exact decision trace is still needed for causal attribution. A different or missing template ID alone does not establish that a rejected outcome is fixed.</p>')
    bits.append('<h2 id="cases">All 14 owner-reviewed comparisons</h2>')
    for case in case_rows:
        bits.append('<article id="case-'+str(case['number'])+'"><h3>'+str(case['number'])+'. '+esc(case['title'])+'</h3><p><strong>Owner assessment of the fresh result:</strong> '+esc(case['owner_assessment'])+'</p>'+show('fresh',case['fresh_template']))
        for target in case['incremental_templates']:
            edges=[e for e in case['edges'] if e['after']==target]
            bits.append('<h4>Actual incremental successor</h4>'+show('incremental',target)+'<p>'+f'{sum(e["messages"] for e in edges):,}'+' contextual messages / '+f'{sum(e["occurrences"] for e in edges):,}'+' occurrences in the training corpus map here.</p>')
            for edge in edges[:1]:
                bits.append('<details><summary>Genuine witness and original provenance</summary>'+pre(edge['example']['text'])+pre(json.dumps(edge['example']['provenance'],ensure_ascii=True,indent=2))+'</details>')
        for edge in case['edges']:
            if edge['after'] is None:
                bits.append('<p><strong>Lost complete assignment:</strong> '+str(edge['occurrences'])+' occurrences.</p>'+pre(edge['example']['text']))
        bits.append('</article>')
    bits.append('<h2 id="scope">Controlled scope and verification</h2><p>The shared 73-log corpus was already established. The saved production script and input manifest supply the order and batch boundaries. Outcomes are joined by contextual message IDs and occurrence counts. Each incremental checkpoint declares its preceding same-version model.</p><p>The registry operation uses the unchanged parser on copied inputs and merges cached native records; the historical runner filtered its complete native-recovery snapshot. Both invoke the existing cumulative build_model(previous_model=...) API. Separate repeated input checks were stopped at the owner’s direction.</p><p>The first post-build orchestration check used the runtime-export field name on a research bundle and stopped after the completed 20-log checkpoint. The check was corrected; the authenticated checkpoint was reused, not rebuilt. No learner code changed. Progress memory entries describe the Windows launcher PID, not the descendant worker’s peak memory.</p>')
    bits.append('<table><tr><th>Logs</th><th>Templates</th><th>Supported</th><th>Provisional</th><th>Revision</th></tr>'+''.join('<tr>'+''.join('<td>'+esc(v)+'</td>' for v in (r['logs'],r['summary']['templates'],r['summary']['supported_templates'],r['summary']['provisional_templates'],r['revision_id']))+'</tr>' for r in checkpoints)+'</table>')
    bits.append('<p><a href="build-history-comparison.json">Complete controlled comparison</a> · <a href="build-basis.json">Original schedule and frozen release</a> · <a href="training-corpus-comparison.json">Production → incremental mappings</a> · <a href="fresh-training-comparison.json">Fresh → incremental mappings</a> · <a href="completion.json">Build completion</a></p></html>')
    (out/'BUILD-HISTORY.html').write_text('\n'.join(bits),encoding='utf-8',newline='')
    print(json.dumps(dict(inventory=result['inventory'],stored_fresh_to_incremental=trans,
        rejected_cases=[{k:r[k] for k in ('number','incremental_templates','identical_display_successors')} for r in case_rows if r['number'] in (7,10)]),indent=2))


if __name__ == '__main__':
    main()
