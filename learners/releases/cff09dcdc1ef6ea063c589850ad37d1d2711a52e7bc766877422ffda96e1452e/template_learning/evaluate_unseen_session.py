"""Research-only inspection of a protected log against a native candidate bundle.

This is not the runtime pipeline inspector. It does not train, mutate the
candidate, or process SQL. The candidate selects its exact parser artifact.
"""
import argparse
import json
from pathlib import Path
from template_learning.artifacts import load_bundle
from template_learning.inventory import ProtectedLog, sha256_file
from template_learning.records import collect_records
from template_learning.research_matching import evaluate_records


def evaluate(log_path, bundle):
    model,parser=load_bundle(bundle)
    digest=sha256_file(log_path)
    stat=log_path.stat()
    grouped,stats=collect_records([ProtectedLog(digest,"protected",log_path,digest,stat.st_size,stat.st_mtime_ns)],parser=parser)
    summary,rows,unresolved=evaluate_records(model,grouped,stats)
    return dict(schema="ck3chronicle.native-candidate-inspection",model_revision=model["revision_id"],
        parser=model["parser"],evidence=stats,summary=summary,records=rows,unresolved=unresolved)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--log",type=Path,required=True)
    p.add_argument("--bundle",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=evaluate(a.log,a.bundle)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result["summary"],indent=2))


if __name__=="__main__":
    main()
