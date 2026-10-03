"""Evaluate candidate data using only the explicitly selected learner distribution."""
import argparse
import json
from pathlib import Path
import sys

from template_learning.inventory import ProtectedLog, sha256_file
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.records import collect_records, identity
from template_learning.research_matching import evaluate_records


def evaluate(log, bundle):
    context = sys.modules.get('_ck3_learner_execution')
    if context is None:
        raise ValueError('explicit authenticated learner release required')
    manifest = json.loads((bundle / 'manifest.json').read_bytes())
    for name, expected in manifest['hashes'].items():
        path = (bundle / name).resolve()
        if path.parent != bundle.resolve() or sha256_file(path) != expected:
            raise ValueError('candidate artifact disagreement: ' + name)
    model = json.loads((bundle / 'empirical_template_model.json').read_bytes())
    if (model['revision_id'] != manifest['revision_id'] or
            identity({k:v for k,v in model.items() if k!='revision_id'})[:24] != model['revision_id']):
        raise ValueError('candidate model identity disagreement')
    if model['parser'] != manifest['parser']:
        raise ValueError('candidate parser manifest disagreement')
    if model.get('status') == 'published':
        raise ValueError('published model evaluation requires its runtime package')
    if model['algorithm'].get('learner_identity') != context.manifest['learner_identity']:
        raise ValueError('candidate learner differs from selected distribution')
    parser = load_parser(reference_from_manifest(Path(__file__).parent / 'parsers/v1_7/manifest.json'))
    if any(model['parser'][k] != parser.reference.to_dict()[k] for k in ('sha256','version')):
        raise ValueError('candidate parser differs from selected distribution')
    digest = sha256_file(log)
    stat = log.stat()
    grouped, stats = collect_records([ProtectedLog(digest,'protected',log,digest,stat.st_size,stat.st_mtime_ns)],parser=parser)
    summary, rows, unresolved = evaluate_records(model,grouped,stats)
    return dict(model_revision=model['revision_id'],input_sha256=digest,parser=model['parser'],
        learner_release=dict(release_id=context.manifest['release_id'],manifest_sha256=context.pin,
            learner_identity=context.manifest['learner_identity']['sha256']),
        evidence=stats,summary=summary,records=rows,unresolved=unresolved)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle',type=Path,required=True);p.add_argument('--log',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=evaluate(a.log,a.bundle)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['summary']))


if __name__=='__main__':
    main()
