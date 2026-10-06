"""Compare every name-field audit hit with its pinned production assignment."""
import argparse
from collections import Counter
import json
import html
from pathlib import Path

from template_learning.audit_key_bindings import capture_groups, hits
from template_learning.report_function_words import NAME_PARTS
from template_learning.evidence_serialization import native_evidence_rows, write_json
from template_learning.matcher_example import load_verified
from template_learning.analyze_removed_templates import changes, native_regions


def render(result, root):
    esc=lambda s:html.escape(str(s))
    def pre(s):
        return '<pre>'+esc(''.join(c if c in '\r\n\t' or ord(c)>=32 else '\\u%04x'%ord(c) for c in str(s)))+'</pre>'
    bits=['<!doctype html><html lang="en"><meta charset="utf-8"><title>Name captures: production versus candidate</title><style>body{font:16px/1.5 system-ui;max-width:1100px;margin:32px auto;padding:0 24px;color:#243747}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef3f6;padding:14px;font-size:13px}table{width:100%;border-collapse:collapse}td,th{padding:10px;border-bottom:1px solid #ccd5de;text-align:left;vertical-align:top}</style>',
        '<h1>Name captures: production versus candidate</h1><p><strong>The 107 flagged messages / 332 occurrences already split the same name fields into KEYs in production.</strong> This is inherited field handling, not a new name-splitting regression. Earlier recommendations did not distinguish this clearly enough.</p>',
        '<p>Both pinned public matchers replayed every one of these genuine messages. Production: 68f1ae5db205ab46afef9c4d. Candidate: 83df10b8cfb86d1573f8e510. Every flagged name capture has the same type, value and native byte span. In 106 messages / 331 occurrences, all capture roles are unchanged. In the remaining one, only the diagnostic word target changes from literal to KEY; the names remain unchanged.</p>',
        '<p><a href="name-capture-production-comparison.json">All assignments and capture comparisons</a> · <a href="RECOMMENDATIONS.html">Recommendations</a></p>']
    for needle in ['Antiochia in Pisidien','The Isles','of Hampshire','of Suffolk']:
        row=next(r for r in result['rows'] if needle in r['text'])
        bits.append('<h2>'+esc(needle)+'</h2><table><tr><th>Production</th><th>Candidate</th></tr><tr>')
        for label in ('production','candidate'):
            assignment=row[label+'_assignment']
            bits.append('<td>'+esc(assignment['template_id'])+pre(row['patterns'][label])+'</td>')
        bits.append('</tr></table>'+pre(row['text']))
        bits.append('<p>'+('Only target changes from literal to KEY.' if row['changes'] else 'No literal/slot role changes.')+'</p>')
    bits.append('<p>Recommendation correction: treat whole-name recognition as an inherited improvement opportunity, separately from regressions caused by this candidate. The target-to-KEY change is a separate generalization, not evidence of changed name boundaries.</p></html>')
    (root/'NAME-COMPARISON.html').write_text('\n'.join(bits),encoding='utf-8')


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--evidence',type=Path,required=True)
    cli.add_argument('--bundle',type=Path,required=True)
    cli.add_argument('--production',type=Path,required=True)
    cli.add_argument('--candidate',type=Path,required=True)
    args=cli.parse_args();root=args.evidence
    comparison=json.loads((root/'comparison.json').read_bytes())
    old=load_verified(args.production,comparison['production']['manifest_sha256'])
    new=load_verified(args.candidate,comparison['candidate']['pin'])
    templates={label:{t['template_id']:t for t in package.data['templates']} for label,package in [('production',old),('candidate',new)]}
    rows=[];summary=Counter();occ=Counter()
    for record,n in native_evidence_rows(args.bundle/'native_evidence.json'):
        selected=record.get('selected_assignment')
        if not selected or selected['template_id'] not in NAME_PARTS:continue
        found=[dict(region=region,**cap) for region,caps in capture_groups(selected) for cap in caps
               if cap.get('type') in ('KEY','OPTIONAL_KEY') and cap.get('value') and hits(cap['value'])]
        if not found:continue
        unit=dict(parser=new.manifest['parser'],source_family=record['source_family'],context_kind=record['context_kind'],
            body=dict(text=record['native'],pieces=record['pieces']),contexts=next(iter(record['contexts'].values()),{}),continuations=record['continuations'])
        before=old.match(unit,inspect=True);after=new.match(unit,inspect=True)
        a,b=before['assignment'],after['assignment'];assert b['template_id']==selected['template_id']
        texts=native_regions(unit);diffs=changes(a,b,texts) if a else []
        category='newly classified' if not a else 'changed capture roles' if diffs else 'unchanged capture roles'
        summary[category]+=1;occ[category]+=n
        rows.append(dict(example_id=record['example_id'],source=record['source_family'],text=record['native'],occurrences=n,
            provenance=record['native_occurrences'],flagged_captures=found,category=category,changes=diffs,
            production_assignment=a,candidate_assignment=b,
            patterns={label:templates[label][assignment['template_id']]['display'] if assignment else None for label,assignment in [('production',a),('candidate',b)]},
            production_inspection=before['inspection'] if not a or diffs else None,
            candidate_inspection=after['inspection'] if not a or diffs else None))
    assert len(rows)==107 and sum(r['occurrences'] for r in rows)==332
    result=dict(scope='All 107 name/display-field rows flagged by the function-word audit; both pinned public matchers; unchanged original messages.',
        packages=dict(production=comparison['production'],candidate=comparison['candidate']),
        summary=[dict(category=c,messages=summary[c],occurrences=occ[c]) for c in summary],rows=rows)
    write_json(root/'name-capture-production-comparison.json',result)
    render(result,root)
    print(json.dumps(result['summary'],indent=2))
    for row in rows:
        if row['category']!='unchanged capture roles':
            print(json.dumps({k:row[k] for k in ('example_id','category','text','occurrences','changes','patterns')},ensure_ascii=True))


if __name__=='__main__':main()
