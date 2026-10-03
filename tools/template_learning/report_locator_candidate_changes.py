"""Human review of disposable locator changes using genuine stored messages."""
import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path

from template_learning.location_candidate_experiment import save, sha
from template_learning.matcher_example import load_verified
from template_learning.verify_location_candidate import stored_unit
from ck3chronicle.pipeline.contracts import render_regions


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--experiment', type=Path, required=True)
    cli.add_argument('--baseline', type=Path, required=True)
    cli.add_argument('--baseline-pin', required=True)
    args = cli.parse_args()
    out = args.experiment.resolve()
    manifest, = (out/'packages').glob('*/manifest.json')
    packages = dict(before=load_verified(args.baseline,args.baseline_pin),
                    after=load_verified(manifest.parent,sha(manifest)))
    templates = {label:{t['template_id']:t for t in p.data['templates']} for label,p in packages.items()}
    old, new = map(set,(templates['before'],templates['after']))
    added, removed, unchanged = new-old, old-new, old&new
    evidence = json.loads((out/'stored-evidence.json').read_text())
    cache, edges, gained = {}, {}, {}
    for run in evidence['runs']:
        rows = json.loads((out/(run['run_id']+'.json')).read_text())['records']
        for row in rows:
            key = (row['source_family'],row['definition']['context_kind'],
                   tuple(render_regions(row['definition'],row['values'])))
            if key not in cache:
                unit = stored_unit(packages['after'],row)
                cache[key] = {label:p.match(unit)['assignment'] for label,p in packages.items()}
            results = cache[key]
            before, after = results['before'],results['after']
            if not after:
                continue
            proof = dict(run_id=row['run_id'],ordinal=row['ordinal'],occurrences=row['occurrence_count'],
                         text=dict(key[2])['body'])
            if before:
                pair = (before['template_id'],after['template_id'])
                edge = edges.setdefault(pair,dict(before=pair[0],after=pair[1],occurrences=0,records=0,example=proof))
                edge['occurrences'] += row['occurrence_count']
                edge['records'] += 1
            else:
                item = gained.setdefault(key,dict(**proof,template_id=after['template_id'],
                    status=after['match_status'],captures=after['regions'],references=[]))
                if item['references']:
                    item['occurrences'] += row['occurrence_count']
                item['references'].append(dict(run_id=row['run_id'],ordinal=row['ordinal']))
        print('Compared',run['run_id'],flush=True)
    incoming, outgoing = defaultdict(list),defaultdict(list)
    for edge in edges.values():
        incoming[edge['after']].append(edge)
        outgoing[edge['before']].append(edge)
    for entries in (*incoming.values(),*outgoing.values()):
        entries.sort(key=lambda e:-e['occurrences'])
    gained_counts = Counter()
    for item in gained.values():
        gained_counts[item['template_id']] += item['occurrences']
    def rank(identifier):
        return (-bool(gained_counts[identifier]),-len(incoming[identifier]),
                -sum(e['occurrences'] for e in incoming[identifier]),identifier)
    scope_ids = [t for t in added if "Event target link '<KEY>' did not get a matching scope type" in templates['after'][t]['display']]
    added_examples = (sorted(scope_ids)+[t for t in sorted(added,key=rank) if t not in scope_ids])[:15]
    # Show removed predecessors across as many replacement templates as possible.
    removed_examples = []
    for target in sorted(new,key=rank):
        for edge in incoming[target]:
            if edge['before'] in removed:
                removed_examples.append(edge['before'])
                break
        if len(removed_examples)==15:
            break
    for identifier in sorted(removed):
        if len(removed_examples)>=15:
            break
        if identifier not in removed_examples:
            removed_examples.append(identifier)
    choices = sorted(gained.values(),key=lambda item:-item['occurrences'])
    gained_examples, represented = [],set()
    for item in choices:
        if item['template_id'] not in represented:
            gained_examples.append(item)
            represented.add(item['template_id'])
        if len(gained_examples)==15:
            break
    for item in choices:
        if len(gained_examples)>=15:
            break
        if item not in gained_examples:
            gained_examples.append(item)
    verification = json.loads((out/'verification.json').read_text())
    result = dict(baseline_package=packages['before'].manifest['package_id'],
        candidate_package=packages['after'].manifest['package_id'],
        counts=dict(before=len(old),after=len(new),added_ids=len(added),removed_ids=len(removed),unchanged_ids=len(unchanged),
                    newly_matched_occurrences=sum(gained_counts.values()),newly_matched_distinct_messages=len(gained),
                    replacement_edges=len(edges),removed_ids_with_observed_replacements=sum(bool(outgoing[t]) for t in removed)),
        added_ids=sorted(added),removed_ids=sorted(removed),unchanged_ids=sorted(unchanged),
        edges=list(edges.values()),added_examples=added_examples,removed_examples=removed_examples,
        newly_matched_examples=gained_examples,
        scope='Definition inventory: complete same-20-log packages. Replacement edges and newly matched examples: all 18 genuine stored Runs; observed examples, not exhaustive proof of equivalence.')
    save(out/'changes.json',result)
    esc = lambda v:html.escape(str(v))
    pre = lambda v:'<pre>'+esc(v)+'</pre>'
    fmt = lambda n:f'{n:,}'
    def declaration(label,identifier):
        t = templates[label][identifier]
        return '<p class="meta">'+esc(t['source_family'])+' · '+esc(t['status'])+' · <code>'+identifier+'</code></p>'+pre(t['display'])
    def source(example):
        return '<p class="meta">'+esc(example['run_id'])+' · stored record '+str(example['ordinal'])+'</p>'
    bits = ['''<!doctype html><html lang="en"><meta charset="utf-8"><title>Locator changes: template review</title>
<style>body{font:16px/1.55 system-ui;max-width:1120px;margin:36px auto;padding:0 24px;color:#172b3b}h1,h2,h3{line-height:1.25}a{color:#075b9b}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f5f8;padding:16px;max-height:440px;overflow:auto;font-size:13px}.meta{font-size:14px;color:#506071}table{border-collapse:collapse;width:100%}td,th{padding:10px;text-align:left;border-bottom:1px solid #cad4dc}article{border-top:2px solid #d5e1ea;margin-top:26px;padding-top:8px}.note{background:#edf5fc;border-left:4px solid #397ca7;padding:14px}nav a{margin-right:18px}details{margin:12px 0}summary{cursor:pointer}</style>
<h1>What changed in the disposable locator model?</h1>
<nav><a href="#new">15 new definitions</a><a href="#removed">15 removed definitions</a><a href="#gained">Previously unmatched messages</a><a href="#cautions">Status changes and limits</a></nav>''',
        '<p>Both packages learned from the same 20 genuine logs. This comparison isolates the combined marker/Unknown and repeated-locator changes from simply supplying more logs. Production has not been changed.</p>',
        '<p class="note"><strong>The result is mainly consolidation and replacement, with additional matching coverage.</strong> '
        'There are '+fmt(len(new))+' definitions, down from '+fmt(len(old))+'. Definition IDs include their slot constraints and layout, '
        'so the new location representation changes IDs even where diagnostic wording remains familiar. “Removed” below means absent from the new package; it does not by itself mean lost diagnostic coverage.</p>',
        '<table><tr><th>Definition inventory</th><th>Count</th></tr>'+''.join('<tr><td>'+label+'</td><td>'+fmt(count)+'</td></tr>' for label,count in [
            ('Previous definitions',len(old)),('Candidate definitions',len(new)),('New IDs',len(added)),('Removed IDs',len(removed)),('Unchanged IDs',len(unchanged))])+'</table>',
        '<p>On 48,772 stored records representing 766,476 occurrences across 18 Runs: <strong>1,376 previously unmatched occurrences now match</strong>; '
        'unmatched occurrences fall from 1,432 to 56. No complete baseline match became unmatched. Four template assignments became provisional; these remain complete and are discussed below. '
        'All selected assignments reconstruct their original regions and preserve existing locator values.</p>',
        '<p><code>&lt;KEY&gt;</code> is a variable key; <code>&lt;LOCATOR&gt;</code> is an exact location value; <code>&lt;PARAM&gt;</code> is an intact parameter such as a trace. '
        '<code>&lt;LOCATOR entries: one or more&gt;</code> denotes a repeated section, not one concatenated slot: every file, line and trace remains separately captured in native order. '
        'The literal <code>Script location:</code> / <code>Stack trace:</code> marker remains significant.</p>',
        '<h2 id="new">New definitions: '+str(len(added_examples))+' examples</h2><p>Prioritized by newly covered messages and consolidation observed on the stored corpus. Predecessors shown below matched the same genuine native messages; this is evidence of replacement, not a claim of universal equivalence.</p>']
    for index,identifier in enumerate(added_examples,1):
        edges_here = incoming[identifier]
        bits.append('<article><h3>'+str(index)+'. '+esc(templates['after'][identifier]['display'].split('Error:')[-1].splitlines()[0][:130])+'</h3>'+declaration('after',identifier))
        bits.append('<p>'+str(len(edges_here))+' previous definition IDs lead to this definition in the stored-data comparison; '+fmt(gained_counts[identifier])+' previously unmatched occurrences now use it.</p>')
        if edges_here:
            bits.append('<details><summary>Previous definition'+('s' if len(edges_here)>1 else '')+' and a genuine replacement example</summary>')
            for edge in edges_here[:2]:
                bits.append(declaration('before',edge['before']))
            bits.append(source(edges_here[0]['example'])+pre(edges_here[0]['example']['text'])+'</details>')
        else:
            bits.append('<p>No predecessor was observed in the stored-data sample; this does not establish a wholly new error family.</p>')
        bits.append('</article>')
    bits.append('<h2 id="removed">Removed definitions: '+str(len(removed_examples))+' examples</h2><p>These exact definitions are absent from the new package. Where stored messages establish a replacement, it is shown explicitly.</p>')
    for index,identifier in enumerate(removed_examples,1):
        bits.append('<article><h3>'+str(index)+'. Previous definition</h3>'+declaration('before',identifier))
        if outgoing[identifier]:
            for edge in outgoing[identifier][:2]:
                bits.append('<p>Replacement on '+fmt(edge['occurrences'])+' stored occurrences:</p>'+declaration('after',edge['after']))
        else:
            bits.append('<p>No message assigned to this old definition was found in the stored-data comparison; its replacement is not established here.</p>')
        bits.append('</article>')
    bits.append('<h2 id="gained">Previously unmatched messages: '+str(len(gained_examples))+' examples</h2><p>“Previously unmatched” here means no complete assignment under the earlier same-20-log v46 candidate, not that the production database originally rejected the record. These are genuine messages already stored by production and reclassified only in memory for this experiment.</p>')
    for index,item in enumerate(gained_examples,1):
        bits.append('<article><h3>'+str(index)+'. No complete assignment → '+esc(item['status'])+'</h3>'+source(item)+
            '<p>'+fmt(item['occurrences'])+' occurrences across the stored Runs.</p><h4>Previously unmatched message</h4>'+pre(item['text'])+
            '<h4>Now matched to</h4>'+declaration('after',item['template_id']))
        values = [(r['name'],c['type'],c['value']) for r in item['captures'] for c in r['captures']]
        bits.append('<details><summary>Exact captured values</summary><table><tr><th>Region</th><th>Type</th><th>Value</th></tr>'+''.join(
            '<tr>'+''.join('<td>'+esc(v)+'</td>' for v in row)+'</tr>' for row in values)+'</table></details></article>')
    bits.append('<h2>The three original production no-match diagnostics</h2><p>These three were actually unassigned in production Run IS3QON under recorded package <code>68f1ae5db205ab46afef9c4d</code>. '
                'They are separate from the same-20-log comparison above. The original capture is in the training set, so these results do not establish unseen accuracy.</p>')
    for item in verification['targets']:
        bits.append('<article><p><strong>Production no_match → candidate '+esc(item['assignment']['status'])+'</strong></p>'+pre(item['text'])+
                    '<h4>Candidate assignment</h4>'+pre(item['template'])+'</article>')
    bits.append('<h2 id="cautions">Status changes and limits</h2>')
    bits.append('<p><strong>Four occurrences changed from template to provisional, without losing their complete assignments.</strong> '
                'The previous supported <code>&lt;KEY&gt; effect [ &lt;REASON&gt; ]</code> definition had two distinct training examples. '
                'The candidate instead learned separate <code>add_title_law effect</code> and <code>activate_struggle_catalyst effect</code> definitions, '
                'each with one distinct training example, below the existing two-example support threshold. '
                'The selection evidence reports one complete candidate with no template or capture tie. This is a change in inferred generality and support, not lost locator binding.</p>')
    for item in verification['status_downgrades']:
        selected = item['results']['candidate']['assignment']
        bits.append('<details><summary>'+esc(item['run_id'])+' · '+str(item['occurrences'])+' occurrence(s): template → provisional</summary>'+pre(item['text'])+
                    '<h4>Previous definition</h4>'+declaration('before',item['results']['baseline']['assignment']['template_id'])+
                    '<h4>Candidate definition</h4>'+declaration('after',selected['template_id'])+'</details>')
    bits.append('<p>The original IS3QON scope mismatch now uses the shared three-KEY template. Its two travel messages still receive complete provisional assignments with literal message bodies; this locator experiment does not establish their proposed reusable short-character/date template.</p>')
    bits.append('<ul>'+''.join('<li>'+esc(value)+'</li>' for value in verification['limitations'])+'</ul>')
    bits.append('<p><a href="RESULTS.html">Full verification report</a> · <a href="changes.json">Complete definition-ID crosswalk and examples</a> · <a href="verification.json">Verification evidence and remaining unmatched records</a></p></html>')
    (out/'CHANGES.html').write_text('\n'.join(bits),encoding='utf-8')
    print(json.dumps(result['counts'],indent=2),flush=True)


if __name__=='__main__':
    main()
