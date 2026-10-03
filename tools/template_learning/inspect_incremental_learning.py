"""Inspect successive registry builds on complete captured logs.

This runs the existing learner without changing its inference rules. The two
explicit comparison logs are inspected at every checkpoint; they also enter
training in the supplied order and are not a holdout exercise.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

from template_learning import incremental_template_registry as registry
from template_learning import inventory, records
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.research_matching import evaluate_records
from template_learning.evidence_serialization import native_evidence_rows


def write_json(path, value):
    with path.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=True, indent=2)
        stream.write("\n")



def summarize_native_outcomes(step, output):
    """Read every complete native diagnostic and retain competing matches."""
    model=json.loads(Path(step["model_path"]).read_text(encoding="utf-8"))
    counts,by_source=Counter(),defaultdict(Counter)
    problems=[];distinct_rows=0
    for row,n in native_evidence_rows(Path(step["bundle"])/"native_evidence.json"):
        distinct_rows+=1;counts[row["outcome"]]+=n;by_source[row["source_family"]][row["outcome"]]+=n
        if row["outcome"]!="full":
            problems.append(dict(source_family=row["source_family"],native=row["native"],occurrences=n,
                outcome=row["outcome"],matches=row["matches"],capture_ambiguities=row['capture_ambiguities'],construction=row["construction"],
                first_occurrence=row["native_occurrences"][:1]))
    assert dict(counts)=={k:v for k,v in step["training_outcomes"].items() if v}
    selected=sorted(problems,key=lambda r:-r["occurrences"])[:20]
    ids={m["template_id"] for r in selected for m in [*r["matches"],*r['capture_ambiguities']]}
    result=dict(training_logs=step["training_logs"],revision_id=model["revision_id"],parser=model["parser"],
        counts=dict(counts),distinct_contextual_rows=distinct_rows,by_source={s:dict(c) for s,c in by_source.items()},
        problem_examples=selected,patterns={p["template_id"]:p for p in model["templates"] if p["template_id"] in ids})
    write_json(output,result)
    return result


def write_report(output, steps, order):
    lines=["# Incremental outer-diagnostic review","",
        "Each checkpoint rebuilds provisional candidates from accumulated complete native logs; confirmed contracts remain fixed.","",
        "| Logs | Messages | Templates | Full | Ambiguous | Unknown |","|---:|---:|---:|---:|---:|---:|"]
    for step in steps:
        c=step['training_outcomes']
        lines.append(f"| {step['training_logs']} | {step['messages']} | {step['templates']} | {c['full']} | {c['provisional']} | {c['unknown']} |")
    lines += ["","## Training order",""]
    lines += [f"{n}. `{item['path']}`" for n,item in enumerate(order,1)]
    (output/"REVIEW.md").write_text("\n".join(lines)+"\n",encoding="utf-8")


def inspect(corpus, first_logs, checkpoints, parser_manifest, output):
    if len(first_logs) != 2:
        raise ValueError("supply the two previously discussed logs in order")
    if output.exists() and any(output.iterdir()):
        raise ValueError("use a fresh inspection output directory")
    output.mkdir(parents=True, exist_ok=True)
    files = json.loads(corpus.read_text(encoding="utf-8"))["files"]
    by_path = {str(Path(row["path"]).resolve()): row for row in files}
    first = [by_path[str(path.resolve())] for path in first_logs]
    remaining = [row for row in files if row not in first]
    order = first + sorted(remaining, key=lambda row: (
        Path(row["path"]).stat().st_mtime_ns, row["path"]))
    checkpoints = sorted(set([*checkpoints, len(order)]))
    if checkpoints[0] < 1 or checkpoints[-1] > len(order):
        raise ValueError("checkpoint outside the supplied corpus")
    write_json(output / "training-order.json", order)

    parser = load_parser(reference_from_manifest(parser_manifest))
    comparisons = []
    for row in first:
        path = Path(row["path"])
        stat = path.stat()
        digest = inventory.sha256_file(path)
        item = inventory.ProtectedLog(digest, "protected", path, digest,
                                      stat.st_size, stat.st_mtime_ns)
        comparisons.append(records.collect_records([item], parser=parser))

    runtime, state = output / "inputs", output / "registry"
    steps, added = [], 0
    for count in checkpoints:
        started = time.monotonic()
        print(f"CHECKPOINT {count}/{len(order)}: adding complete logs", flush=True)
        for row in order[added:count]:
            target = runtime / "sessions" / row["sha256"] / "error.log"
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(row["path"], target)
        synced = registry.sync_registry(runtime, state, parser=parser, default_role="training")
        print(f"CHECKPOINT {count}: building from {synced['distinct_evidence']} logs", flush=True)
        subprocess.run([sys.executable, "-u", "-m",
            "template_learning.incremental_template_registry", "--state-root", str(state),
            "build", "--parser-manifest", str(parser_manifest)], check=True)
        revision = registry.load_registry(state)["current_revision"]
        bundle = state / "revisions" / revision
        build = dict(revision_id=revision, bundle=str(bundle.resolve()),
                     model_path=str((bundle / "empirical_template_model.json").resolve()))
        model = json.loads(Path(build["model_path"]).read_text(encoding="utf-8"))
        step = dict(training_logs=count, **build, **model["summary"], sync=synced, comparisons={})
        for n, (grouped, stats) in enumerate(comparisons, 1):
            print(f"CHECKPOINT {count}: inspecting comparison log {n}", flush=True)
            summary, rows, unresolved = evaluate_records(model, grouped, stats)
            path = output / f"step-{count:03d}-log-{n}.json"
            write_json(path, dict(model_revision=model["revision_id"],
                training_logs=count, evidence=stats, summary=summary,
                records=rows, unresolved=unresolved))
            step["comparisons"][str(n)] = dict(**summary, report=str(path.resolve()))
        step["elapsed_seconds"] = round(time.monotonic() - started, 2)
        steps.append(step)
        write_json(output / f"step-{count:03d}.json", step)
        write_json(output / "steps.json", steps)
        write_report(output, steps, order)
        print(f"COMPLETED {count}: " + json.dumps(dict(
            templates=step["templates"], unique_messages=step["unique_messages"],
            comparison_counts={k:v['counts'] for k,v in step['comparisons'].items()},
            elapsed_seconds=step["elapsed_seconds"])), flush=True)
        added = count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True,
                        help="Existing native survey summary with a files list.")
    parser.add_argument("--first-log", type=Path, action="append", required=True)
    parser.add_argument("--checkpoint", type=int, action="append", required=True)
    parser.add_argument("--parser-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inspect(args.corpus, args.first_log, args.checkpoint, args.parser_manifest, args.output)


if __name__ == "__main__":
    main()
