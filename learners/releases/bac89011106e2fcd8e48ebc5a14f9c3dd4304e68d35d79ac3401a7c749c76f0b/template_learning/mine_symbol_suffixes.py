"""Inspect suffixes of complete native KEY captures in a candidate bundle."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
from template_learning.artifacts import load_bundle


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bundle",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    model,_=load_bundle(a.bundle)
    evidence=json.loads((a.bundle/"native_evidence.json").read_text(encoding="utf-8"))
    buckets=defaultdict(lambda:dict(values=set(),templates=set(),sources=set(),examples=[]))
    for row in evidence["records"]:
        for capture in row["captures"] or []:
            value=capture["value"]
            if capture["type"] not in {"KEY","OPTIONAL_KEY"} or not value or "_" not in value:
                continue
            suffix=value.rsplit("_",1)[-1]
            bucket=buckets[(row["source_family"],suffix)]
            bucket["values"].add(value)
            bucket["templates"].add(row["template_id"])
            bucket["sources"].add(row["source_family"])
            bucket["examples"].append(dict(record_id=row["record_id"],capture=capture))
    output=dict(model_revision=model["revision_id"],status="research_observations_not_slot_constraints",rows=[
        dict(source_family=source,suffix=suffix,**{key:sorted(value) if isinstance(value,set) else value for key,value in bucket.items()})
        for (source,suffix),bucket in sorted(buckets.items())])
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(output,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    main()
