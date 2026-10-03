"""Rebuild exactly a saved candidate's native corpus and compare all outcomes.

Reads validated selected-parser feature caches; never changes registry roles,
or current revision. Additional cached logs can be evaluated with
the resulting frozen candidate, without entering its training set.
"""
from __future__ import annotations
import argparse
from collections import Counter
import gc
import json
from pathlib import Path
import sys
import time

from template_learning import artifacts
from template_learning.incremental_template_registry import (
    combine_training_records, load_registry)
from template_learning.artifacts import all_patterns
from template_learning.literal_guidance import LITERAL_GUIDANCE
from template_learning.parsers import load_parser, reference_from_manifest
from template_learning.research_matching import evaluate_records
from template_learning.evidence_serialization import native_evidence_rows


def write_json(path, value):
    path.write_bytes(artifacts.canonical_bytes(value))


def row_key(row):
    return row["source_family"], row["native"], tuple(sorted(row["contexts"]))


def compact_review(rows, model):
    patterns = all_patterns(model)
    result = []
    for row in rows:
        if row["outcome"] == "full":
            continue
        ids = [m["template_id"] for m in row["matches"]]
        result.append(dict(source_family=row["source_family"],native=row["native"],
            context_ids=sorted(row["contexts"]),
            outcome=row["outcome"],occurrences=row.get("_occurrence_count",len(row["native_occurrences"])),
            first_occurrence=row["native_occurrences"][0],
            matches=[dict(display=patterns[i]["display"],template_id=i) for i in ids],
            capture_ambiguities=row['capture_ambiguities'],
            construction=row["construction"]))
    return result


def inspect(registry_root, baseline_bundle, parser_manifest, output, evaluate_remaining, saved_baseline_outcomes=False):
    started = time.monotonic()
    output.mkdir(parents=True,exist_ok=True)
    baseline,bundled_parser = artifacts.load_bundle(baseline_bundle)
    parser = load_parser(reference_from_manifest(parser_manifest))
    if (parser.reference.version,parser.reference.sha256) != (bundled_parser.reference.version,bundled_parser.reference.sha256):
        raise ValueError("comparison requires the baseline parser's exact version and bytes")
    registry = load_registry(registry_root)
    selected = set(baseline["evidence"])
    entries = [registry["evidence"][sha] for sha in sorted(selected)]
    print(f"Loading exactly {len(entries)} baseline logs with parser {parser.reference.version}",flush=True)
    grouped,stats = combine_training_records(registry_root,entries,parser=parser)
    assert set(stats) == selected
    if saved_baseline_outcomes:
        # Explicitly reuse the hash-verified bundle's native results, not a
        # different parser/model or a silently selected baseline cache.
        before_rows,counts = [],Counter({k:0 for k in baseline["summary"]["training_outcomes"]})
        for row,count in native_evidence_rows(baseline_bundle/"native_evidence.json"):
            row["_occurrence_count"] = count
            before_rows.append(row)
            counts[row["outcome"]] += count
        assert dict(counts) == baseline["summary"]["training_outcomes"]
        before = dict(counts=dict(counts),recovered_messages=sum(counts.values()),
            unresolved_emissions=baseline["summary"]["unresolved_emissions"],
            status="saved_hash_verified_baseline_native_outcomes")
    else:
        before,before_rows,_ = evaluate_records(baseline,grouped,stats)
    write_json(output/"baseline-summary.json",before)
    outcomes = {row_key(r):r["outcome"] for r in before_rows}
    write_json(output/"baseline-review.json",compact_review(before_rows,baseline))
    del before_rows
    gc.collect()
    print("Rebuilding candidate using current learner",flush=True)
    model,evidence = artifacts.build_model(grouped,stats,parser=parser,
        threshold=baseline["algorithm"]["cluster_threshold"])
    assert model["summary"]["messages"] == baseline["summary"]["messages"]
    assert model["summary"]["unique_messages"] == baseline["summary"]["unique_messages"]
    patterns = list(all_patterns(model).values())
    for pattern in patterns:
        if pattern["unsupported_members"] or pattern["status"] == "confirmed":
            continue
        for part in pattern["parts"]:
            if part["kind"] == "slot" and part["type"] != "REASON":
                values = part["observed_values"]
                assert not (len(values)>1 and len({v.casefold() for v in values})==1)
    transitions = Counter()
    for row in evidence["records"]:
        transitions[(outcomes[row_key(row)],row["outcome"])] += len(row["native_occurrences"])
    write_json(output/"training-review.json",compact_review(evidence["records"],model))
    print("Writing immutable comparison bundle",flush=True)
    bundle = artifacts.write_bundle(output/"revisions",model,evidence,parser=parser,
        build_command=[sys.executable,"-m","template_learning.inspect_candidate_revision",*sys.argv[1:]])
    result = dict(baseline_revision=baseline["revision_id"],revision_id=model["revision_id"],
        bundle=str(bundle.resolve()),parser=model["parser"],before=before,after=model["summary"],
        baseline_template_counts={k:baseline["summary"][k] for k in ("templates","unresolved_candidates")},
        transitions=[dict(before=a,after=b,occurrences=n) for (a,b),n in sorted(transitions.items())],
        refined_candidates=sum(bool(p.get("inference_refinements")) for p in patterns),
        literal_guidance=LITERAL_GUIDANCE,registry_unchanged=True,
        scope="Same-corpus structural comparison; not semantic acceptance or a held-out accuracy claim")
    write_json(output/"summary.json",result)
    del evidence,grouped,stats,patterns,outcomes
    gc.collect()
    if evaluate_remaining:
        remaining = [row for sha,row in registry["evidence"].items() if sha not in selected and row["role"]=="training"]
        print(f"Frozen evaluation of {len(remaining)} additional native logs",flush=True)
        grouped,stats = combine_training_records(registry_root,remaining,parser=parser)
        old_summary,rows,_ = evaluate_records(baseline,grouped,stats)
        previous = {row_key(r):r["outcome"] for r in rows}
        write_json(output/"additional-baseline-review.json",compact_review(rows,baseline))
        del rows
        gc.collect()
        summary,rows,_ = evaluate_records(model,grouped,stats)
        transitions = Counter()
        for row in rows:
            transitions[(previous[row_key(row)],row["outcome"])] += len(row["native_occurrences"])
        write_json(output/"additional-review.json",compact_review(rows,model))
        result["additional_logs"] = dict(logs=len(stats),before=old_summary,after=summary,
            evidence=stats,transitions=[dict(before=a,after=b,occurrences=n) for (a,b),n in sorted(transitions.items())],
            scope=f"Not used in this {len(selected)}-log build; already part of the owner's accumulated corpus, not a commissioned holdout")
    result["elapsed_seconds"] = round(time.monotonic()-started,1)
    write_json(output/"summary.json",result)
    print(json.dumps({k:result[k] for k in ("revision_id","before","after","elapsed_seconds")},ensure_ascii=True),flush=True)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--registry",type=Path,required=True)
    p.add_argument("--baseline-bundle",type=Path,required=True)
    p.add_argument("--parser-manifest",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--evaluate-remaining",action="store_true")
    p.add_argument("--saved-baseline-outcomes",action="store_true",
        help="Use the baseline bundle's hash-verified native training outcomes instead of evaluating it again")
    args=p.parse_args()
    inspect(args.registry,args.baseline_bundle,args.parser_manifest,args.output,args.evaluate_remaining,args.saved_baseline_outcomes)


if __name__ == "__main__":
    main()
