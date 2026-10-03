"""Export native candidate evidence for owner inspection, without an old oracle."""
import argparse
import json
from pathlib import Path
from template_learning.artifacts import load_bundle
from template_learning.incremental_template_registry import all_patterns


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--bundle",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    a=p.parse_args()
    model,_=load_bundle(a.bundle)
    evidence=json.loads((a.bundle/"native_evidence.json").read_text(encoding="utf-8"))
    templates=all_patterns(model)
    a.output_dir.mkdir(parents=True,exist_ok=True)
    index=["# Native candidate examples","","Every complete supporting message variant; occurrence references and exact captures are retained.","",
        "| Source | Template | Example |","|---|---|---|"]
    for row in evidence["records"]:
        filename=row["example_id"]+".md"
        selected=[templates[m["template_id"]] for m in row["matches"]]
        label=row["template_id"] or row["outcome"]
        text=["# "+row["source_family"],"","Template `"+label+"`","",
            "## Original message","","```text",row["native"],"```","",
            "## Matched complete diagnostic patterns","","```json",json.dumps(selected,ensure_ascii=True,indent=2),"```","",
            "## Native captures, context, construction and all occurrences","","```json",json.dumps(row,ensure_ascii=True,indent=2),"```",""]
        (a.output_dir/filename).write_text("\n".join(text),encoding="utf-8")
        index.append(f"| {row['source_family']} | {label} | [native example]({filename}) |")
    (a.output_dir/"INDEX.md").write_text("\n".join(index)+"\n",encoding="utf-8")
    (a.output_dir/"unresolved.json").write_text(json.dumps(evidence["unresolved"],ensure_ascii=True,indent=2)+"\n",encoding="utf-8")


if __name__=="__main__":
    main()
