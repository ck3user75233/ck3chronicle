"""Export native candidate evidence for owner inspection, without an old oracle."""
import argparse
import json
from pathlib import Path
from template_learning.artifacts import load_bundle
from template_learning.artifacts import all_patterns
from template_learning.evidence_serialization import native_evidence_rows, write_json


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bundle",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    a=p.parse_args()
    model,_=load_bundle(a.bundle)
    metadata = {}
    templates=all_patterns(model)
    a.output_dir.mkdir(parents=True,exist_ok=True)
    definition_dir = a.output_dir/'templates'
    definition_dir.mkdir(exist_ok=True)
    for key, template in templates.items():
        write_json(definition_dir/(key+'.json'), template)
    write_json(a.output_dir/'refinement-history.json', model['refinement_history'])
    index=["# Native candidate examples","","Every complete supporting message variant; occurrence references and exact captures are retained.","",
        "| Source | Template | Example |","|---|---|---|"]
    for row, _ in native_evidence_rows(a.bundle/'native_evidence.json', retain_occurrences=True, metadata=metadata):
        filename=row["example_id"]+".md"
        selected=['- ['+m['template_id']+'](templates/'+m['template_id']+'.json)' for m in row['matches']]
        label=row["template_id"] or row["outcome"]
        text=["# "+row["source_family"],"","Template `"+label+"`","",
            "## Original message","","```text",row["native"],"```","",
            "## Matched complete diagnostic patterns","",*selected,"",
            "Definitions are stored once; their parent IDs resolve in [refinement history](refinement-history.json).","",
            "## Native captures, context, construction and all occurrences","","```json",json.dumps(row,ensure_ascii=True,indent=2),"```",""]
        (a.output_dir/filename).write_text("\n".join(text),encoding="utf-8")
        index.append(f"| {row['source_family']} | {label} | [native example]({filename}) |")
    (a.output_dir/"INDEX.md").write_text("\n".join(index)+"\n",encoding="utf-8")
    write_json(a.output_dir/'unresolved.json', metadata['unresolved'])


if __name__=="__main__":
    main()
