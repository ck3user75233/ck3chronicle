"""Build a source-partitioned native-message candidate from explicit evidence."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from template_learning import artifacts, inventory, records
from template_learning.parsers import load_parser, reference_from_manifest


def parse_args():
    p=argparse.ArgumentParser(description=__doc__)
    inputs=p.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--log",type=Path,action="append",help="Complete protected log; repeat for several inputs.")
    inputs.add_argument("--runtime-root",type=Path)
    p.add_argument("--parser-manifest",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--threshold",type=float,default=.72)
    p.add_argument("--exclude-sha256",action="append",default=[])
    return p.parse_args()


def main():
    args=parse_args()
    if args.log:
        logs,duplicates,seen=[],[],set()
        for path in args.log:
            path=path.resolve()
            digest=inventory.sha256_file(path)
            if digest in seen:
                duplicates.append(dict(path=str(path),sha256=digest))
                continue
            seen.add(digest)
            stat=path.stat()
            logs.append(inventory.ProtectedLog(digest,"protected",path,digest,stat.st_size,stat.st_mtime_ns))
    else:
        logs,duplicates=inventory.protected_error_logs(args.runtime_root)
    excluded={s.casefold() for s in args.exclude_sha256}
    omitted=[dict(sha256=e.sha256,path=str(e.path)) for e in logs if e.sha256 in excluded]
    logs=[e for e in logs if e.sha256 not in excluded]
    if not logs:
        raise SystemExit("no protected evidence selected")
    parser=load_parser(reference_from_manifest(args.parser_manifest))
    grouped,stats=records.collect_records(logs,parser=parser)
    model,evidence=artifacts.build_model(grouped,stats,parser=parser,threshold=args.threshold,
        duplicates=duplicates,excluded_evidence=omitted)
    folder=artifacts.write_bundle(args.output_dir,model,evidence,parser=parser,
        build_command=[sys.executable,"-m","template_learning.learn_error_templates",*sys.argv[1:]])
    print(json.dumps(dict(bundle=str(folder),**model["summary"]),indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
